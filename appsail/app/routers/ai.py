from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import joblib
import os
import numpy as np
import logging

from app.ai.chatbot import Chatbot
from app.ai.rag_engine import RAGEngine
# from app.ai.voice_processor import VoiceProcessor
import app.ai.multilingual as multilingual

router = APIRouter(
    prefix="/api/ai",
    tags=["AI Modules"]
)

# Initialize AI Components
rag_engine = RAGEngine()
chatbot = Chatbot(rag_engine=rag_engine)
# voice_processor = VoiceProcessor()

# Load models and encoders lazily
detector = None
encoders = None
logger = logging.getLogger(__name__)

def load_models():
    global detector, encoders
    if detector is None:
        try:
            model_path = os.path.join(os.path.dirname(__file__), "..", "ai", "trained_model.pkl")
            encoder_path = os.path.join(os.path.dirname(__file__), "..", "ai", "label_encoders.pkl")
            detector = joblib.load(model_path)
            encoders = joblib.load(encoder_path)
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load models: {e}")

class ChatRequest(BaseModel):
    message: str

class FIRRequest(BaseModel):
    raw_summary: str

class PredictRequest(BaseModel):
    latitude: float
    longitude: float
    Year: int
    Month: int
    AgeYear: float
    GenderID: str
    CrimeHead: str

@router.post("/chat")
def chat(request: ChatRequest):
    try:
        response = chatbot.chat(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draft_fir")
def draft_fir(request: FIRRequest):
    try:
        prompt = f"Convert the following raw summary into a professional legal FIR (First Information Report) draft. Structure it properly with necessary legal headings and formal language.\n\nSummary:\n{request.raw_summary}"
        response = rag_engine.llm.invoke(prompt)
        
        # Handle Gemini 3.1 Flash Lite list output format
        if isinstance(response.content, list):
            text_response = response.content[0].get("text", str(response.content))
        else:
            text_response = str(response.content)
            
        return {"response": text_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict_risk")
def predict_risk(request: PredictRequest):
    load_models()
    if detector is None or encoders is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
        
    try:
        # Encode categoricals
        gender_encoded = encoders['GenderID'].transform([request.GenderID])[0]
        
        # Handle unknown CrimeHead safely
        crime_head = request.CrimeHead
        if crime_head not in encoders['CrimeHead'].classes_:
            # fallback to the first class if unseen to prevent crash
            crime_head = encoders['CrimeHead'].classes_[0]
            
        crime_encoded = encoders['CrimeHead'].transform([crime_head])[0]
        
        features = np.array([[
            request.latitude,
            request.longitude,
            request.Year,
            request.Month,
            request.AgeYear,
            gender_encoded,
            crime_encoded
        ]])
        
        is_hotspot = detector.predict_hotspot(features)[0]
        risk_score = detector.calculate_risk_score(features)[0]
        
        return {
            "is_hotspot": bool(is_hotspot),
            "risk_score": float(risk_score)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice_to_text")
def process_voice(file: UploadFile = File(...)):
    # In a real app, save the file temporarily and pass to whisper
    # Here we simulate the process
    try:
        temp_path = f"/tmp/temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
            
        text = voice_processor.speech_to_text(temp_path)
        os.remove(temp_path)
        return {"text": text}
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

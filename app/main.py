from fastapi import FastAPI

from app.database.database import Base, engine

# Models
from app.models.user import User
from app.models.police_station import PoliceStation
from app.models.crime_type import CrimeType
from app.models.location import Location
from app.models.fir import FIR
from app.models.victim import Victim
from app.models.accused import Accused
from app.models.officer import Officer
from app.models.evidence import Evidence
from app.models.investigation_status import InvestigationStatus
from app.models.arrest_surrender import ArrestSurrender
from app.routers import reports

# Routers
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.fir import router as fir_router
from app.routers.victim import router as victim_router
from app.routers.accused import router as accused_router
from app.routers.evidence import router as evidence_router
from app.routers.police_station import router as police_station_router
from app.routers.investigation_status import router as investigation_status_router
from app.routers.crime_type import router as crime_type_router
from app.routers.ai import router as ai_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Police AI Crime Intelligence Platform",
    description="AI-powered Crime Database and Investigation System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(fir_router)
app.include_router(victim_router)
app.include_router(accused_router)
app.include_router(evidence_router)
app.include_router(police_station_router)
app.include_router(investigation_status_router)
app.include_router(crime_type_router)
app.include_router(reports.router)
app.include_router(ai_router)
@app.get("/")
def home():
    return {
        "message": "Police AI Backend is Running Successfully"
    }

from app.routers.ai import rag_engine
import logging

@app.on_event("startup")
def startup_event():
    logger = logging.getLogger(__name__)
    logger.info("Ingesting text files into RAG FAISS Vector Store...")
    try:
        rag_engine.ingest_text_files("data")
        logger.info("Successfully ingested case files into RAG memory!")
    except Exception as e:
        logger.error(f"Failed to ingest files for RAG: {e}")
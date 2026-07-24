import os
import whisper
from gtts import gTTS

def speech_to_text(audio_file_path: str, model_name: str = "base") -> str:
    """
    Converts speech from an audio file to text using OpenAI's Whisper model.
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
    # Load the Whisper model (will download the first time if not cached)
    model = whisper.load_model(model_name)
    
    # Transcribe the audio
    result = model.transcribe(audio_file_path)
    return result["text"].strip()

def text_to_speech(text: str, output_file_path: str, lang: str = "kn") -> str:
    """
    Converts text to speech using gTTS and saves it to an audio file.
    Default language is Kannada ('kn'). Can also use 'en' for English.
    
    Returns the path to the generated audio file.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
        
    # Generate speech
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Ensure directory exists
    output_dir = os.path.dirname(output_file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    tts.save(output_file_path)
    return output_file_path

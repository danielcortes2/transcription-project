# Endpoint para transcripción de audio
from fastapi import APIRouter, UploadFile, File, HTTPException
import openai
import tempfile
import os
from pydub import AudioSegment

router = APIRouter()

# Clave de API de OpenAI (puedes almacenarla en un .env y leerla con dotenv)
OPENAI_API_KEY = "tu-api-key"

@router.post("/transcribe/")

async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name
 
        # Convertir a formato WAV (si es necesario)
        audio = AudioSegment.from_file(temp_audio_path)
        wav_path = temp_audio_path.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")
 
        # Usar Whisper para transcribir
        openai.api_key = OPENAI_API_KEY
        with open(wav_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
 
        # Limpiar archivos temporales
        os.remove(temp_audio_path)
        os.remove(wav_path)
        return {"text": transcript["text"]}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
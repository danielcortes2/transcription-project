from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
from pydub import AudioSegment
import requests

router = APIRouter()

# URL de la API de DeepSeek (ajústala según la documentación de DeepSeek)
DEEPSEEK_API_URL = "https://api.deepseek.ai/transcribe"
DEEPSEEK_API_KEY = "sk-749a3ee548f64a078b82e56785966c07"


@router.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):  # Renombramos la función para claridad
    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # Convertir a formato WAV (DeepSeek podría requerir un formato específico)
        audio = AudioSegment.from_file(temp_audio_path)
        wav_path = temp_audio_path.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")

        # Subir el archivo a DeepSeek para transcripción
        with open(wav_path, "rb") as audio_file:
            headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
            files = {"audio": audio_file}
            response = requests.post(DEEPSEEK_API_URL, headers=headers, files=files)

        # Limpiar archivos temporales
        os.remove(temp_audio_path)
        os.remove(wav_path)

        # Manejar la respuesta de DeepSeek
        if response.status_code == 200:
            transcript = response.json()
            return {"text": transcript.get("text", "No se pudo obtener el texto de la transcripción.")}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException

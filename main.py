from fastapi import FastAPI
from app.api.transcribe import router as transcribe_router  # Importamos el router

app = FastAPI(title="API de Transcripción de Audio")

# Incluimos el router del módulo transcribe.py
app.include_router(transcribe_router, prefix="/api", tags=["Transcripción"])

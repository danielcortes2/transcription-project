from fastapi import FastAPI
from api import transcribe
 
app = FastAPI(title="API de Transcripción de Audio")
 
app.include_router(transcribe.router, prefix="/audio")
 
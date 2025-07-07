from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pathlib
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

from models import Query
from extraction import parse, FlightSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()
CLIENT_DIR = BASE_DIR / "client"

app.mount("/static", StaticFiles(directory=str(CLIENT_DIR)), name="static")

@app.get("/")
async def get_index():
    return FileResponse(str(CLIENT_DIR / "index.html"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/extract", response_model=FlightSearch)
async def extract(query: Query):
    result = parse(query.query)
    return jsonable_encoder(result)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not client.api_key:
        logger.error("OpenAI API key not configured")
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
    try:
        logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        temp_file_path = "temp_audio.webm"
        try:
            content = await file.read()
            logger.info(f"File size: {len(content)} bytes")
            
            with open(temp_file_path, "wb") as buffer:
                buffer.write(content)
            
            logger.info(f"File saved to {temp_file_path}")
            
            with open(temp_file_path, "rb") as audio_file:
                logger.info("Sending file to Whisper API")
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                logger.info("Received transcript from Whisper API")
            
            return {"text": transcript.text}
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.info(f"Cleaned up {temp_file_path}")
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

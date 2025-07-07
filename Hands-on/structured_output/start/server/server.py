from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pathlib
import logging
from dotenv import load_dotenv

load_dotenv()

from models import Query
from extraction import parse, FlightSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()
CLIENT_DIR = BASE_DIR / "client"

app.mount("/static", StaticFiles(directory=str(CLIENT_DIR)), name="static")

@app.get("/")
async def get_index():
    return FileResponse(str(CLIENT_DIR / "index.html"))

@app.post("/extract", response_model=FlightSearch)
async def extract(query: Query):
    result = parse(query.query)
    return jsonable_encoder(result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from routing.files import router as files_routing
from routing.files import SHARED_FOLDER_PATH
from contextlib import asynccontextmanager
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    SHARED_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Shared folder initialized at: {SHARED_FOLDER_PATH}")
    yield 
    print("Shutting down...")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:\t(%(asctime)s) : %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()            
    ]
)
logger = logging.getLogger(__name__)
logging.info(f'Start')
app=FastAPI(
    lifespan=lifespan,
    openapi_url="/openapi.json",
    docs_url="/docs"
    )



app.include_router(files_routing)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
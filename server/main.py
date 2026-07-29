import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.routes import router

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outbreak-predictor")

app = FastAPI(
    title="Epidemiological Intelligence API",
    version="3.0.0",
    description="Multi-agent decision-support API for infectious disease risk assessment.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

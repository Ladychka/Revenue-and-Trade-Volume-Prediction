from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.v2.routes import health, analytics

# Ensure environment vars are available if .env exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Initialize application
app = FastAPI(
    title="Customs Analytics V2",
    description="Mathematical Forecasting and Deterministic Scenario Simulation Engine for Customs Revenues",
    version="2.0.0",
    docs_url="/api/v2/docs",
    openapi_url="/api/v2/openapi.json"
)

# CORS Policy - allowing strictly defined analytics UI origins
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly disallow destructive methods like DELETE
    allow_headers=["*"],
)

# Wire routers
app.include_router(health.router, prefix="/api/v2")
app.include_router(analytics.router, prefix="/api/v2")

@app.get("/")
def root():
    return {"message": "Customs Analytics V2 Engine Active. Proceed to /api/v2/docs."}

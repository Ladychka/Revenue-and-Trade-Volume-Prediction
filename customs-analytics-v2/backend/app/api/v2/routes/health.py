from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health", tags=["System"])
async def check_health():
    """
    Basic health check for V2 API.
    """
    return {
        "status": "healthy",
        "api_generation": "V2 Analytical Module",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": "postgresql+asyncpg",
        "forecasting_engine_available": True
    }

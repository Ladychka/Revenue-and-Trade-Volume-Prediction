"""
FastAPI Application - Customs Revenue Analytics API
Phase 8 - API Implementation

Safe by design:
- Read-only endpoints only
- Aggregated data only (no raw identifiers)
- All access logged
- No declaration-level or importer-level data exposed
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import logging

# Import route modules
from .routes import revenue, trade, compliance, metadata
from .dependencies import init_db_pool, close_db_pool, is_db_available

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application metadata
app = FastAPI(
    title="Customs Revenue Analytics API",
    description="""Read-only analytics API for customs revenue and trade data.
    
    **Safety Features:**
    - All endpoints return aggregated data only
    - No individual declaration or importer identifiers exposed
    - Minimum threshold: 5 records per aggregation
    - All API access is logged
    
    **API Freeze Status:** v1.0-demo - ENDPOINT CONTRACTS FROZEN
    No new endpoints can be added without governance approval.
    
    **Data Mode:** Connects to PostgreSQL when available; falls back to
    demonstration data when database is not running.
    """,
    version="1.0.0-demo",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers with prefixes
app.include_router(
    revenue.router, 
    prefix="/api/v1/revenue",
    tags=["Revenue Analytics"]
)
app.include_router(
    trade.router, 
    prefix="/api/v1/trade", 
    tags=["Trade Analytics"]
)
app.include_router(
    compliance.router, 
    prefix="/api/v1/compliance", 
    tags=["Compliance Analytics"]
)
app.include_router(
    metadata.router, 
    prefix="/api/v1/metadata", 
    tags=["Metadata"]
)


# ============================================================================
# Security: API Access Logging Middleware
# ============================================================================

@app.middleware("http")
async def log_api_access(request: Request, call_next):
    """Log all API access events"""
    start_time = datetime.now(timezone.utc)
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    # Log access (in production, this would go to a logging service)
    logger.info(
        f"API_ACCESS: method={request.method} "
        f"path={request.url.path} "
        f"status={response.status_code} "
        f"duration={duration:.3f}s "
        f"client={request.client.host if request.client else 'unknown'}"
    )
    
    return response


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "database_connected": is_db_available(),
        "data_mode": "live" if is_db_available() else "demo"
    }


# ============================================================================
# Safe API Response Wrapper
# ============================================================================

def safe_response(data: dict, message: str = "Success"):
    """Wrap API responses with metadata"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def error_response(message: str, status_code: int = 400):
    """Return error response"""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return error_response(exc.detail, exc.status_code)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return error_response("Internal server error", 500)


# ============================================================================
# Startup / Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("Starting Customs Revenue Analytics API")
    logger.info("API Safety: Read-only, Aggregated data only, All access logged")
    await init_db_pool()
    if is_db_available():
        logger.info("DATA MODE: LIVE — connected to PostgreSQL")
    else:
        logger.info("DATA MODE: DEMO — returning demonstration data")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    await close_db_pool()
    logger.info("Shutting down Customs Revenue Analytics API")


# ============================================================================
# Run Instructions (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
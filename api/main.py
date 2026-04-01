"""
FastAPI Application - Customs Revenue Analytics API
Phase 8 - API Implementation

Safe by design:
- Read-only endpoints only
- Aggregated data only (no raw identifiers)
- All access logged
- No declaration-level or importer-level data exposed
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
import logging

# Import route modules
from .routes import revenue, trade, compliance, metadata

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
    start_time = datetime.utcnow()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.utcnow() - start_time).total_seconds()
    
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
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
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
        "timestamp": datetime.utcnow().isoformat()
    }


def error_response(message: str, status_code: int = 400):
    """Return error response"""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
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
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("Starting Customs Revenue Analytics API")
    logger.info("API Safety: Read-only, Aggregated data only, All access logged")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("Shutting down Customs Revenue Analytics API")


# ============================================================================
# Run Instructions (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
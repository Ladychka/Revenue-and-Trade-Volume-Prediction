"""
Metadata Routes
Phase 8 - API Endpoint Implementation

Safe endpoints for API documentation and system information.
"""

from fastapi import APIRouter
from datetime import datetime

# Router instance
router = APIRouter()


@router.get("/info")
async def get_api_info():
    """Get API metadata and safety information"""
    return {
        "name": "Customs Revenue Analytics API",
        "version": "1.0.0",
        "description": "Read-only analytics API for customs revenue and trade data",
        "safety_features": {
            "read_only": True,
            "aggregated_data_only": True,
            "no_individual_identifiers": True,
            "minimum_threshold": "5 records",
            "access_logging": True
        }
    }


@router.get("/endpoints")
async def get_endpoints():
    """List available API endpoints"""
    return {
        "revenue": [
            "/api/v1/revenue/summary",
            "/api/v1/revenue/monthly",
            "/api/v1/revenue/by-port",
            "/api/v1/revenue/by-tax-type",
            "/api/v1/revenue/trends"
        ],
        "trade": [
            "/api/v1/trade/summary",
            "/api/v1/trade/by-country",
            "/api/v1/trade/by-hs",
            "/api/v1/trade/time-series"
        ],
        "compliance": [
            "/api/v1/compliance/risk-summary",
            "/api/v1/compliance/variance-summary"
        ]
    }
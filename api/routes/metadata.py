"""
Metadata Routes
Phase 8 - API Endpoint Implementation

Safe endpoints for API documentation and system information.
"""

from fastapi import APIRouter
from datetime import datetime, timezone

from ..dependencies import fetch_rows, is_db_available

# Router instance
router = APIRouter()


@router.get("/info")
async def get_api_info():
    """Get API metadata and safety information"""
    return {
        "name": "Customs Revenue Analytics API",
        "version": "1.0.0",
        "description": "Read-only analytics API for customs revenue and trade data",
        "data_mode": "live" if is_db_available() else "demo",
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
            "/api/v1/trade/time-series",
            "/api/v1/trade/top-importers"
        ],
        "compliance": [
            "/api/v1/compliance/risk-summary",
            "/api/v1/compliance/variance-summary",
            "/api/v1/compliance/high-risk-entities"
        ],
        "metadata": [
            "/api/v1/metadata/info",
            "/api/v1/metadata/endpoints",
            "/api/v1/metadata/ports",
            "/api/v1/metadata/countries",
            "/api/v1/metadata/hs-codes"
        ]
    }


@router.get("/ports")
async def get_ports():
    """Get list of customs ports (reference data)"""
    if is_db_available():
        rows = await fetch_rows("SELECT port_code, port_name, region, port_type FROM port_reference ORDER BY port_code")
        if rows:
            return [dict(r) for r in rows]

    return [
        {"port_code": f"PORT{i:03d}", "port_name": f"Customs Port {i}", "region": "Central", "port_type": "Sea"}
        for i in range(1, 11)
    ]


@router.get("/countries")
async def get_countries():
    """Get list of trading partner countries (reference data)"""
    if is_db_available():
        rows = await fetch_rows("SELECT country_code, country_name, region FROM country_reference ORDER BY country_code")
        if rows:
            return [dict(r) for r in rows]

    countries = {
        "CN": "China", "JP": "Japan", "US": "United States", "KR": "South Korea",
        "TH": "Thailand", "ID": "Indonesia", "MY": "Malaysia", "AU": "Australia",
        "DE": "Germany", "SG": "Singapore", "VN": "Vietnam", "TW": "Taiwan",
    }
    return [
        {"country_code": code, "country_name": name, "region": "Asia-Pacific" if code not in ("US", "DE") else "Other"}
        for code, name in countries.items()
    ]


@router.get("/hs-codes")
async def get_hs_codes():
    """Get HS code reference data"""
    if is_db_available():
        rows = await fetch_rows("SELECT hs_code, description, duty_rate, vat_rate FROM hs_code_reference ORDER BY hs_code")
        if rows:
            return [dict(r) for r in rows]

    return [
        {"hs_code": "8471300000", "description": "Portable digital computers", "duty_rate": 0.0, "vat_rate": 0.17},
        {"hs_code": "8517120000", "description": "Smartphones", "duty_rate": 0.0, "vat_rate": 0.17},
        {"hs_code": "8703235010", "description": "Vehicles 1500-3000cc", "duty_rate": 0.25, "vat_rate": 0.17},
        {"hs_code": "6204620000", "description": "Women's trousers (cotton)", "duty_rate": 0.1675, "vat_rate": 0.07},
        {"hs_code": "6203420000", "description": "Men's trousers (cotton)", "duty_rate": 0.1675, "vat_rate": 0.07},
        {"hs_code": "3002150000", "description": "Immunological products", "duty_rate": 0.0, "vat_rate": 0.0},
        {"hs_code": "3004900000", "description": "Medicaments", "duty_rate": 0.0, "vat_rate": 0.0},
        {"hs_code": "3926900000", "description": "Plastic articles", "duty_rate": 0.065, "vat_rate": 0.17},
        {"hs_code": "9403610000", "description": "Wooden furniture", "duty_rate": 0.0, "vat_rate": 0.17},
        {"hs_code": "8541400000", "description": "Photosensitive semiconductor devices", "duty_rate": 0.0, "vat_rate": 0.17},
    ]
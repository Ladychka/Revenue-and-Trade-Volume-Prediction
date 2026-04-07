"""
Trade Analytics Routes
Phase 8 - API Endpoint Implementation

Safe endpoints:
- Trade summaries (aggregated)
- Trade by country (aggregated)
- Trade by HS code (aggregated)
- Time-series data (monthly)
- NO individual importer or declaration data
"""

from fastapi import APIRouter, Query
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field

from ..dependencies import fetch_rows, fetch_row, is_db_available

# Router instance
router = APIRouter()


# ============================================================================
# Response Models (Safe - Aggregated Only)
# ============================================================================

class TradeByCountry(BaseModel):
    """Trade by country - Aggregated, no individual identifiers"""
    country_code: str = Field(..., description="ISO country code")
    country_name: str = Field(..., description="Country name")
    
    # Aggregated metrics
    total_declarations: int = Field(..., description="Total declarations (aggregated)")
    total_customs_value: Decimal = Field(..., description="Total trade value")
    total_duty_collected: Decimal = Field(..., description="Total duty collected")


class TradeByHS(BaseModel):
    """Trade by HS code - Aggregated at chapter level"""
    hs_chapter: str = Field(..., description="HS chapter (2-digit)")
    chapter_description: str = Field(..., description="Chapter description")
    
    # Aggregated metrics
    total_declarations: int
    total_customs_value: Decimal
    total_duty_collected: Decimal


class TradeTimeSeries(BaseModel):
    """Trade time-series - Monthly aggregates only"""
    period: str
    total_declarations: int
    total_customs_value: Decimal
    total_duty_collected: Decimal


class TradeSummary(BaseModel):
    """Overall trade summary - Aggregated"""
    period_start: str
    period_end: str
    data_mode: str = "demo"
    
    # Aggregated totals
    total_declarations: int
    total_items: int
    total_customs_value: Decimal
    total_duty_collected: Decimal
    
    # Averages
    average_shipment_value: Decimal


# ============================================================================
# Country Name Helper
# ============================================================================

COUNTRY_NAMES = {
    "CN": "China", "JP": "Japan", "US": "United States", "KR": "South Korea",
    "TH": "Thailand", "ID": "Indonesia", "MY": "Malaysia", "AU": "Australia",
    "DE": "Germany", "SG": "Singapore", "VN": "Vietnam", "TW": "Taiwan",
}

HS_CHAPTER_NAMES = {
    "84": "Machinery and mechanical appliances",
    "85": "Electrical machinery and equipment",
    "87": "Vehicles other than railway",
    "62": "Articles of apparel, not knit or crochet",
    "30": "Pharmaceutical products",
    "39": "Plastics and articles thereof",
    "94": "Furniture; bedding, mattresses",
    "54": "Man-made filaments",
}


# ============================================================================
# Demo Fallback Data
# ============================================================================

def _demo_trade_summary() -> TradeSummary:
    return TradeSummary(
        period_start="2024-01-01", period_end="2025-12-31", data_mode="demo",
        total_declarations=50000, total_items=150000,
        total_customs_value=Decimal("3750000000.00"),
        total_duty_collected=Decimal("187500000.00"),
        average_shipment_value=Decimal("75000.00"),
    )


def _demo_trade_by_country(limit: int) -> List[TradeByCountry]:
    countries = [
        {"country_code": "CN", "country_name": "China",         "total_declarations": 15000, "total_customs_value": Decimal("1312500000.00"), "total_duty_collected": Decimal("65625000.00")},
        {"country_code": "JP", "country_name": "Japan",         "total_declarations": 7500,  "total_customs_value": Decimal("562500000.00"),  "total_duty_collected": Decimal("28125000.00")},
        {"country_code": "US", "country_name": "United States", "total_declarations": 6000,  "total_customs_value": Decimal("450000000.00"),  "total_duty_collected": Decimal("22500000.00")},
        {"country_code": "KR", "country_name": "South Korea",   "total_declarations": 5000,  "total_customs_value": Decimal("375000000.00"),  "total_duty_collected": Decimal("18750000.00")},
        {"country_code": "TH", "country_name": "Thailand",      "total_declarations": 4000,  "total_customs_value": Decimal("300000000.00"),  "total_duty_collected": Decimal("15000000.00")},
    ]
    return [TradeByCountry(**c) for c in countries[:limit]]


def _demo_trade_by_hs(limit: int) -> List[TradeByHS]:
    chapters = [
        {"hs_chapter": "84", "chapter_description": "Machinery and mechanical appliances",      "total_declarations": 12500, "total_customs_value": Decimal("937500000.00"),  "total_duty_collected": Decimal("46875000.00")},
        {"hs_chapter": "85", "chapter_description": "Electrical machinery and equipment",        "total_declarations": 10000, "total_customs_value": Decimal("750000000.00"),  "total_duty_collected": Decimal("37500000.00")},
        {"hs_chapter": "87", "chapter_description": "Vehicles other than railway",               "total_declarations": 5000,  "total_customs_value": Decimal("375000000.00"),  "total_duty_collected": Decimal("93750000.00")},
        {"hs_chapter": "62", "chapter_description": "Articles of apparel, not knit or crochet",  "total_declarations": 6000,  "total_customs_value": Decimal("225000000.00"),  "total_duty_collected": Decimal("16875000.00")},
        {"hs_chapter": "30", "chapter_description": "Pharmaceutical products",                   "total_declarations": 4000,  "total_customs_value": Decimal("300000000.00"),  "total_duty_collected": Decimal("0.00")},
    ]
    return [TradeByHS(**c) for c in chapters[:limit]]


def _demo_time_series() -> List[TradeTimeSeries]:
    return [
        TradeTimeSeries(period="2024-01", total_declarations=2083, total_customs_value=Decimal("156225000.00"), total_duty_collected=Decimal("7811250.00")),
        TradeTimeSeries(period="2024-02", total_declarations=2166, total_customs_value=Decimal("162450000.00"), total_duty_collected=Decimal("8122500.00")),
        TradeTimeSeries(period="2024-03", total_declarations=2250, total_customs_value=Decimal("168750000.00"), total_duty_collected=Decimal("8437500.00")),
    ]


# ============================================================================
# Endpoint Implementations — Live DB + Demo Fallback
# ============================================================================

@router.get("/summary", response_model=TradeSummary)
async def get_trade_summary(
    year: Optional[int] = Query(None, description="Filter by year")
):
    """
    Get overall trade summary.
    
    **Safety**: Returns aggregated data only, no individual declaration IDs.
    """
    if is_db_available():
        where_clause = "WHERE status = 'CLEARED'"
        args = []
        if year:
            where_clause += " AND EXTRACT(YEAR FROM declaration_date) = $1"
            args.append(year)

        query = f"""
            SELECT
                MIN(declaration_date)::TEXT AS period_start,
                MAX(declaration_date)::TEXT AS period_end,
                COUNT(*)::INT AS total_declarations,
                SUM(total_items)::INT AS total_items,
                COALESCE(SUM(total_customs_value), 0) AS total_customs_value,
                COALESCE(SUM(total_customs_duty), 0) AS total_duty_collected,
                COALESCE(AVG(total_customs_value), 0) AS average_shipment_value
            FROM declarations
            {where_clause}
        """
        row = await fetch_row(query, *args)
        if row and row["total_declarations"] > 0:
            return TradeSummary(
                period_start=row["period_start"] or "N/A",
                period_end=row["period_end"] or "N/A",
                data_mode="live",
                total_declarations=row["total_declarations"],
                total_items=row["total_items"] or 0,
                total_customs_value=row["total_customs_value"],
                total_duty_collected=row["total_duty_collected"],
                average_shipment_value=round(row["average_shipment_value"], 2),
            )

    return _demo_trade_summary()


@router.get("/by-country", response_model=List[TradeByCountry])
async def get_trade_by_country(
    limit: int = Query(20, ge=1, le=50, description="Number of countries"),
    min_value: Optional[Decimal] = Query(None, description="Minimum trade value filter")
):
    """
    Get trade breakdown by origin country.
    
    **Safety**: Aggregated by country, no individual importer identifiers.
    """
    if is_db_available():
        having = "HAVING COUNT(*) >= 5"
        if min_value:
            having += f" AND SUM(di.customs_value) >= {min_value}"

        query = f"""
            SELECT
                di.origin_country AS country_code,
                COUNT(DISTINCT di.declaration_id)::INT AS total_declarations,
                COALESCE(SUM(di.customs_value), 0) AS total_customs_value,
                COALESCE(SUM(di.customs_duty), 0) AS total_duty_collected
            FROM declaration_items di
            JOIN declarations d ON d.declaration_id = di.declaration_id
            WHERE d.status = 'CLEARED'
            GROUP BY di.origin_country
            {having}
            ORDER BY total_customs_value DESC
            LIMIT {limit}
        """
        rows = await fetch_rows(query)
        if rows:
            return [
                TradeByCountry(
                    country_code=r["country_code"],
                    country_name=COUNTRY_NAMES.get(r["country_code"], r["country_code"]),
                    total_declarations=r["total_declarations"],
                    total_customs_value=r["total_customs_value"],
                    total_duty_collected=r["total_duty_collected"],
                )
                for r in rows
            ]

    return _demo_trade_by_country(limit)


@router.get("/by-hs", response_model=List[TradeByHS])
async def get_trade_by_hs(
    level: str = Query("chapter", pattern="^(chapter|heading|subheading)$"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get trade breakdown by HS code.
    
    **Safety**: Aggregated at chapter level by default, minimum threshold 5+ declarations.
    """
    if is_db_available():
        query = f"""
            SELECT
                LEFT(di.hs_code, 2) AS hs_chapter,
                COUNT(DISTINCT di.declaration_id)::INT AS total_declarations,
                COALESCE(SUM(di.customs_value), 0) AS total_customs_value,
                COALESCE(SUM(di.customs_duty), 0) AS total_duty_collected
            FROM declaration_items di
            JOIN declarations d ON d.declaration_id = di.declaration_id
            WHERE d.status = 'CLEARED'
            GROUP BY LEFT(di.hs_code, 2)
            HAVING COUNT(*) >= 5
            ORDER BY total_customs_value DESC
            LIMIT {limit}
        """
        rows = await fetch_rows(query)
        if rows:
            return [
                TradeByHS(
                    hs_chapter=r["hs_chapter"],
                    chapter_description=HS_CHAPTER_NAMES.get(r["hs_chapter"], f"HS Chapter {r['hs_chapter']}"),
                    total_declarations=r["total_declarations"],
                    total_customs_value=r["total_customs_value"],
                    total_duty_collected=r["total_duty_collected"],
                )
                for r in rows
            ]

    return _demo_trade_by_hs(limit)


@router.get("/time-series", response_model=List[TradeTimeSeries])
async def get_trade_time_series(
    period: str = Query("monthly", pattern="^(daily|weekly|monthly|quarterly)$"),
    year: Optional[int] = Query(None, description="Filter by year")
):
    """
    Get trade time-series data.
    
    **Safety**: Time-series aggregates only, no individual data points.
    """
    if is_db_available():
        where_clause = ""
        args = []
        if year:
            where_clause = "WHERE year = $1"
            args.append(year)

        query = f"""
            SELECT month_label AS period,
                   total_declarations,
                   total_customs_value,
                   total_customs_duty AS total_duty_collected
            FROM mv_monthly_revenue
            {where_clause}
            ORDER BY year, month
        """
        rows = await fetch_rows(query, *args)
        if rows:
            return [
                TradeTimeSeries(
                    period=r["period"],
                    total_declarations=r["total_declarations"],
                    total_customs_value=r["total_customs_value"],
                    total_duty_collected=r["total_duty_collected"],
                )
                for r in rows
            ]

    return _demo_time_series()


@router.get("/top-importers")
async def get_top_importers(
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get top importers by trade volume.
    
    **Safety**: Aggregated rankings only, no individual importer IDs in response.
    """
    if is_db_available():
        query = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY SUM(total_customs_value) DESC)::INT AS rank,
                SUM(total_customs_value) AS total_value,
                COUNT(*)::INT AS declaration_count
            FROM declarations
            WHERE status = 'CLEARED'
            GROUP BY declarant_id
            HAVING COUNT(*) >= 5
            ORDER BY total_value DESC
            LIMIT {limit}
        """
        rows = await fetch_rows(query)
        if rows:
            return {
                "data_mode": "live",
                "rankings": [
                    {"rank": r["rank"], "total_value": float(r["total_value"]), "declaration_count": r["declaration_count"]}
                    for r in rows
                ],
                "note": "Aggregated rankings only - individual identifiers not exposed"
            }

    return {
        "data_mode": "demo",
        "rankings": [
            {"rank": 1, "total_value": 75000000.00, "declaration_count": 1000},
            {"rank": 2, "total_value": 60000000.00, "declaration_count": 800},
            {"rank": 3, "total_value": 45000000.00, "declaration_count": 600},
        ],
        "note": "Aggregated rankings only - individual identifiers not exposed"
    }
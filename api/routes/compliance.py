"""
Compliance Analytics Routes
Phase 8 - API Endpoint Implementation

Safe endpoints:
- Risk scores (aggregated)
- Variance summaries (aggregated)
- NO individual declaration data exposed
"""

from fastapi import APIRouter, Query
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

from ..dependencies import fetch_rows, fetch_row, is_db_available

# Router instance
router = APIRouter()


class RiskSummary(BaseModel):
    """Risk assessment summary - Aggregated only"""
    high_risk_count: int
    elevated_risk_count: int
    standard_risk_count: int
    low_risk_count: int
    
    total_declarations: int
    flagged_percentage: float
    data_mode: str = "demo"


class VarianceSummary(BaseModel):
    """Variance analysis - Aggregated"""
    total_analyzed: int
    variance_detected: int
    variance_percentage: float
    average_variance_amount: Decimal
    data_mode: str = "demo"


# ============================================================================
# Demo Fallback Data
# ============================================================================

def _demo_risk_summary() -> RiskSummary:
    return RiskSummary(
        high_risk_count=500, elevated_risk_count=1500,
        standard_risk_count=35000, low_risk_count=13000,
        total_declarations=50000, flagged_percentage=4.0,
        data_mode="demo",
    )


def _demo_variance_summary() -> VarianceSummary:
    return VarianceSummary(
        total_analyzed=50000, variance_detected=750,
        variance_percentage=1.5,
        average_variance_amount=Decimal("5000.00"),
        data_mode="demo",
    )


# ============================================================================
# Endpoint Implementations — Live DB + Demo Fallback
# ============================================================================

@router.get("/risk-summary", response_model=RiskSummary)
async def get_risk_summary():
    """
    Get risk assessment summary.
    
    **Safety**: Aggregated risk categories only, no individual IDs.
    """
    if is_db_available():
        query = """
            SELECT
                COUNT(*) FILTER (WHERE total_tax_liability > (
                    SELECT AVG(total_tax_liability) * 3 FROM declarations WHERE status = 'CLEARED'
                ))::INT AS high_risk_count,
                COUNT(*) FILTER (WHERE total_tax_liability > (
                    SELECT AVG(total_tax_liability) * 2 FROM declarations WHERE status = 'CLEARED'
                ) AND total_tax_liability <= (
                    SELECT AVG(total_tax_liability) * 3 FROM declarations WHERE status = 'CLEARED'
                ))::INT AS elevated_risk_count,
                COUNT(*)::INT AS total_declarations
            FROM declarations
            WHERE status = 'CLEARED'
        """
        row = await fetch_row(query)
        if row and row["total_declarations"] > 0:
            total = row["total_declarations"]
            high = row["high_risk_count"]
            elevated = row["elevated_risk_count"]
            standard = total - high - elevated
            low = int(standard * 0.27)
            standard = standard - low
            flagged = round((high + elevated) / total * 100, 2)
            return RiskSummary(
                high_risk_count=high,
                elevated_risk_count=elevated,
                standard_risk_count=standard,
                low_risk_count=low,
                total_declarations=total,
                flagged_percentage=flagged,
                data_mode="live",
            )

    return _demo_risk_summary()


@router.get("/variance-summary", response_model=VarianceSummary)
async def get_variance_summary(
    threshold: Optional[float] = Query(0.10, ge=0.01, le=1.0)
):
    """
    Get variance detection summary.
    
    **Safety**: Aggregated variance metrics only.
    """
    if is_db_available():
        query = f"""
            WITH avg_stats AS (
                SELECT
                    AVG(total_customs_duty) AS avg_duty,
                    STDDEV(total_customs_duty) AS std_duty,
                    COUNT(*)::INT AS total_analyzed
                FROM declarations
                WHERE status = 'CLEARED' AND total_customs_duty > 0
            ),
            variance_flags AS (
                SELECT d.declaration_id,
                       ABS(d.total_customs_duty - a.avg_duty) AS variance_amount
                FROM declarations d, avg_stats a
                WHERE d.status = 'CLEARED'
                  AND d.total_customs_duty > 0
                  AND ABS(d.total_customs_duty - a.avg_duty) > a.std_duty * {threshold * 10}
            )
            SELECT
                (SELECT total_analyzed FROM avg_stats) AS total_analyzed,
                COUNT(*)::INT AS variance_detected,
                COALESCE(AVG(variance_amount), 0) AS average_variance_amount
            FROM variance_flags
        """
        row = await fetch_row(query)
        if row and row["total_analyzed"] and row["total_analyzed"] > 0:
            total = row["total_analyzed"]
            detected = row["variance_detected"]
            return VarianceSummary(
                total_analyzed=total,
                variance_detected=detected,
                variance_percentage=round(detected / total * 100, 2),
                average_variance_amount=round(row["average_variance_amount"], 2),
                data_mode="live",
            )

    return _demo_variance_summary()


@router.get("/high-risk-entities")
async def get_high_risk_entities(limit: int = Query(10)):
    """
    Get high-risk entity summary.
    
    **Safety**: Aggregated entity counts only, no identifiers.
    """
    if is_db_available():
        query = """
            WITH avg_stats AS (
                SELECT AVG(total_customs_value) AS avg_value,
                       STDDEV(total_customs_value) AS std_value
                FROM declarations WHERE status = 'CLEARED'
            )
            SELECT
                COUNT(DISTINCT d.declarant_id)::INT AS count,
                COALESCE(SUM(d.total_customs_value), 0) AS total_flagged_value
            FROM declarations d, avg_stats a
            WHERE d.status = 'CLEARED'
              AND d.total_customs_value > a.avg_value + 2 * a.std_value
        """
        row = await fetch_row(query)
        if row:
            return {
                "data_mode": "live",
                "count": row["count"],
                "total_flagged_value": float(row["total_flagged_value"]),
                "note": "Aggregated counts only - individual entities not identified"
            }

    return {
        "data_mode": "demo",
        "count": 500,
        "total_flagged_value": 25000000.00,
        "note": "Aggregated counts only - individual entities not identified"
    }
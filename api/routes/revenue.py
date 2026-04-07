"""
Revenue Analytics Routes
Phase 8 - API Endpoint Implementation

Safe endpoints:
- Revenue summaries (aggregated)
- Time-series data (monthly)
- By port breakdown
- By tax type breakdown
- NO individual declaration data
"""

from fastapi import APIRouter, Query
from typing import Optional, List
from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field
from ..dependencies import fetch_rows, fetch_row, is_db_available

# Router instance
router = APIRouter()


# ============================================================================
# Response Models (Safe - Aggregated Only)
# ============================================================================

class MonthlyRevenueSummary(BaseModel):
    """Monthly revenue aggregation - NO individual IDs"""
    year: int
    month: int
    month_label: str
    
    # Aggregated metrics only
    total_declarations: int = Field(..., description="Number of cleared declarations")
    total_customs_value: Decimal = Field(..., description="Total customs value")
    total_customs_duty: Decimal = Field(..., description="Total duty collected")
    total_vat: Decimal = Field(..., description="Total VAT collected")
    total_tax_liability: Decimal = Field(..., description="Total tax liability")
    effective_duty_rate: Decimal = Field(..., description="Effective duty rate")


class RevenueByPort(BaseModel):
    """Revenue by port - Aggregated only"""
    port_code: str
    port_name: str
    
    # Aggregated metrics
    total_declarations: int
    total_customs_value: Decimal
    total_customs_duty: Decimal
    total_vat: Decimal


class RevenueByTaxType(BaseModel):
    """Revenue breakdown by tax type - Aggregated"""
    tax_type: str
    total_amount: Decimal
    percentage_of_total: Decimal


class RevenueSummary(BaseModel):
    """Overall revenue summary - Aggregated"""
    period_start: str
    period_end: str
    data_mode: str = Field(default="demo", description="'live' or 'demo'")
    
    # Aggregated totals
    total_declarations: int
    total_customs_value: Decimal
    total_customs_duty: Decimal
    total_excise: Decimal
    total_vat: Decimal
    total_tax_liability: Decimal
    
    # Averages
    average_declaration_value: Decimal
    average_tax_per_declaration: Decimal


# ============================================================================
# Demo Fallback Data
# ============================================================================

def _demo_revenue_summary(year: Optional[int], month: Optional[int]) -> RevenueSummary:
    return RevenueSummary(
        period_start="2024-01-01",
        period_end="2025-12-31",
        data_mode="demo",
        total_declarations=50000,
        total_customs_value=Decimal("3750000000.00"),
        total_customs_duty=Decimal("187500000.00"),
        total_excise=Decimal("0.00"),
        total_vat=Decimal("637000000.00"),
        total_tax_liability=Decimal("824500000.00"),
        average_declaration_value=Decimal("75000.00"),
        average_tax_per_declaration=Decimal("16490.00")
    )


def _demo_monthly_revenue(year: Optional[int], limit: int) -> List[MonthlyRevenueSummary]:
    months = []
    for i in range(1, min(limit + 1, 13)):
        months.append(MonthlyRevenueSummary(
            year=year or 2024,
            month=i,
            month_label=f"{year or 2024}-{i:02d}",
            total_declarations=4000 + (i * 100),
            total_customs_value=Decimal(f"{(280000000 + i * 20000000):.2f}"),
            total_customs_duty=Decimal(f"{(14000000 + i * 1000000):.2f}"),
            total_vat=Decimal(f"{(47600000 + i * 3400000):.2f}"),
            total_tax_liability=Decimal(f"{(61600000 + i * 4400000):.2f}"),
            effective_duty_rate=Decimal("0.0500")
        ))
    return months


def _demo_revenue_by_port(limit: int) -> List[RevenueByPort]:
    port_names = [
        "Sihanoukville", "Phnom Penh", "Poipet", "Bavet",
        "Siem Reap", "Koh Kong", "Stung Treng", "Battambang",
        "Kampot", "Preah Vihear"
    ]
    ports = []
    for i in range(1, min(limit + 1, 11)):
        ports.append(RevenueByPort(
            port_code=f"PORT{i:03d}",
            port_name=f"Customs Port {port_names[i-1]}" if i <= len(port_names) else f"Customs Port {i}",
            total_declarations=5000 - (i * 200),
            total_customs_value=Decimal(f"{(500000000 - i * 30000000):.2f}"),
            total_customs_duty=Decimal(f"{(25000000 - i * 1500000):.2f}"),
            total_vat=Decimal(f"{(85000000 - i * 5100000):.2f}")
        ))
    return ports


def _demo_revenue_by_tax_type() -> List[RevenueByTaxType]:
    return [
        RevenueByTaxType(tax_type="Customs Duty", total_amount=Decimal("187500000.00"), percentage_of_total=Decimal("0.2275")),
        RevenueByTaxType(tax_type="Value-Added Tax", total_amount=Decimal("637000000.00"), percentage_of_total=Decimal("0.7725")),
        RevenueByTaxType(tax_type="Excise Duty", total_amount=Decimal("0.00"), percentage_of_total=Decimal("0.0000")),
    ]


# ============================================================================
# Endpoint Implementations — Live DB + Demo Fallback
# ============================================================================

@router.get("/summary", response_model=RevenueSummary)
async def get_revenue_summary(
    year: Optional[int] = Query(None, description="Filter by year"),
    month: Optional[int] = Query(None, description="Filter by month (1-12)")
):
    """
    Get overall revenue summary.
    
    **Safety**: Returns aggregated data only, no individual declaration IDs.
    """
    # Try live database first
    if is_db_available():
        where_clauses = ["status = 'CLEARED'"]
        args = []
        idx = 1
        if year:
            where_clauses.append(f"EXTRACT(YEAR FROM declaration_date) = ${idx}")
            args.append(year)
            idx += 1
        if month:
            where_clauses.append(f"EXTRACT(MONTH FROM declaration_date) = ${idx}")
            args.append(month)
            idx += 1

        where_sql = " AND ".join(where_clauses)
        query = f"""
            SELECT
                MIN(declaration_date)::TEXT AS period_start,
                MAX(declaration_date)::TEXT AS period_end,
                COUNT(*)::INT AS total_declarations,
                COALESCE(SUM(total_customs_value), 0) AS total_customs_value,
                COALESCE(SUM(total_customs_duty), 0) AS total_customs_duty,
                COALESCE(SUM(total_excise), 0) AS total_excise,
                COALESCE(SUM(total_vat), 0) AS total_vat,
                COALESCE(SUM(total_tax_liability), 0) AS total_tax_liability,
                COALESCE(AVG(total_customs_value), 0) AS average_declaration_value,
                COALESCE(AVG(total_tax_liability), 0) AS average_tax_per_declaration
            FROM declarations
            WHERE {where_sql}
        """
        row = await fetch_row(query, *args)
        if row:
            return RevenueSummary(
                period_start=row["period_start"] or "N/A",
                period_end=row["period_end"] or "N/A",
                data_mode="live",
                total_declarations=row["total_declarations"],
                total_customs_value=row["total_customs_value"],
                total_customs_duty=row["total_customs_duty"],
                total_excise=row["total_excise"],
                total_vat=row["total_vat"],
                total_tax_liability=row["total_tax_liability"],
                average_declaration_value=round(row["average_declaration_value"], 2),
                average_tax_per_declaration=round(row["average_tax_per_declaration"], 2),
            )

    return _demo_revenue_summary(year, month)


@router.get("/monthly", response_model=List[MonthlyRevenueSummary])
async def get_monthly_revenue(
    year: Optional[int] = Query(None, description="Filter by year"),
    limit: int = Query(12, ge=1, le=24, description="Number of months to return")
):
    """
    Get monthly revenue time-series.
    
    **Safety**: Returns monthly aggregates, no daily or declaration-level data.
    """
    if is_db_available():
        where_clause = ""
        args = []
        if year:
            where_clause = "WHERE year = $1"
            args.append(year)

        query = f"""
            SELECT year, month, month_label,
                   total_declarations, total_customs_value, total_customs_duty,
                   total_vat, total_tax_liability, effective_duty_rate
            FROM mv_monthly_revenue
            {where_clause}
            ORDER BY year, month
            LIMIT {limit}
        """
        rows = await fetch_rows(query, *args)
        if rows:
            return [
                MonthlyRevenueSummary(
                    year=r["year"], month=r["month"], month_label=r["month_label"],
                    total_declarations=r["total_declarations"],
                    total_customs_value=r["total_customs_value"],
                    total_customs_duty=r["total_customs_duty"],
                    total_vat=r["total_vat"],
                    total_tax_liability=r["total_tax_liability"],
                    effective_duty_rate=round(r["effective_duty_rate"], 4),
                )
                for r in rows
            ]

    return _demo_monthly_revenue(year, limit)


@router.get("/by-port", response_model=List[RevenueByPort])
async def get_revenue_by_port(
    limit: int = Query(10, ge=1, le=50, description="Number of ports")
):
    """
    Get revenue breakdown by port.
    
    **Safety**: Aggregated by port, no individual declaration data.
    """
    if is_db_available():
        query = f"""
            SELECT
                d.office_code AS port_code,
                COALESCE(pr.port_name, d.office_code) AS port_name,
                COUNT(*)::INT AS total_declarations,
                SUM(d.total_customs_value) AS total_customs_value,
                SUM(d.total_customs_duty) AS total_customs_duty,
                SUM(d.total_vat) AS total_vat
            FROM declarations d
            LEFT JOIN port_reference pr ON pr.port_code = d.office_code
            WHERE d.status = 'CLEARED'
            GROUP BY d.office_code, pr.port_name
            HAVING COUNT(*) >= 5
            ORDER BY SUM(d.total_customs_value) DESC
            LIMIT {limit}
        """
        rows = await fetch_rows(query)
        if rows:
            return [
                RevenueByPort(
                    port_code=r["port_code"], port_name=r["port_name"],
                    total_declarations=r["total_declarations"],
                    total_customs_value=r["total_customs_value"],
                    total_customs_duty=r["total_customs_duty"],
                    total_vat=r["total_vat"],
                )
                for r in rows
            ]

    return _demo_revenue_by_port(limit)


@router.get("/by-tax-type", response_model=List[RevenueByTaxType])
async def get_revenue_by_tax_type(
    year: Optional[int] = Query(None, description="Filter by year")
):
    """
    Get revenue breakdown by tax type.
    
    **Safety**: Aggregated tax type breakdown only.
    """
    if is_db_available():
        where_clause = "WHERE status = 'CLEARED'"
        args = []
        if year:
            where_clause += " AND EXTRACT(YEAR FROM declaration_date) = $1"
            args.append(year)

        query = f"""
            SELECT
                SUM(total_customs_duty) AS duty,
                SUM(total_vat) AS vat,
                SUM(total_excise) AS excise,
                SUM(total_tax_liability) AS total
            FROM declarations
            {where_clause}
        """
        row = await fetch_row(query, *args)
        if row and row["total"] and row["total"] > 0:
            total = row["total"]
            return [
                RevenueByTaxType(
                    tax_type="Customs Duty",
                    total_amount=row["duty"],
                    percentage_of_total=round(row["duty"] / total, 4),
                ),
                RevenueByTaxType(
                    tax_type="Value-Added Tax",
                    total_amount=row["vat"],
                    percentage_of_total=round(row["vat"] / total, 4),
                ),
                RevenueByTaxType(
                    tax_type="Excise Duty",
                    total_amount=row["excise"],
                    percentage_of_total=round(row["excise"] / total, 4),
                ),
            ]

    return _demo_revenue_by_tax_type()


@router.get("/trends")
async def get_revenue_trends(
    period: str = Query("monthly", pattern="^(daily|weekly|monthly|quarterly)$")
):
    """
    Get revenue trends over time.
    
    **Safety**: Time-series aggregates only, no individual data points.
    """
    if is_db_available():
        query = """
            SELECT month_label AS period,
                   total_tax_liability AS value
            FROM mv_monthly_revenue
            ORDER BY year, month
        """
        rows = await fetch_rows(query)
        if rows:
            data_points = []
            prev_val = None
            for r in rows:
                val = float(r["value"])
                trend = "stable"
                if prev_val is not None:
                    trend = "up" if val > prev_val else ("down" if val < prev_val else "stable")
                data_points.append({"period": r["period"], "value": val, "trend": trend})
                prev_val = val
            avg_value = sum(d["value"] for d in data_points) / len(data_points) if data_points else 0
            return {
                "period_type": period,
                "data_mode": "live",
                "data_points": data_points,
                "summary": {
                    "total_periods": len(data_points),
                    "average_value": round(avg_value, 2),
                    "trend_direction": data_points[-1]["trend"] if data_points else "stable"
                }
            }

    return {
        "period_type": period,
        "data_mode": "demo",
        "data_points": [
            {"period": "2024-01", "value": 61600000, "trend": "up"},
            {"period": "2024-02", "value": 65800000, "trend": "up"},
            {"period": "2024-03", "value": 70200000, "trend": "up"},
        ],
        "summary": {
            "total_periods": 24,
            "average_value": 68666667,
            "trend_direction": "stable"
        }
    }
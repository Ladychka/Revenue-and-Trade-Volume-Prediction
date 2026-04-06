#!/usr/bin/env python3
"""
Revenue API Schemas - Pydantic Models for Revenue Endpoints
Phase 8 - API Implementation

Contains request/response schemas for revenue-related API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ============================================================================
# Revenue Summary Response
# ============================================================================

class RevenueSummary(BaseModel):
    """Revenue summary response"""
    total_revenue: Decimal
    total_duty: Decimal
    total_vat: Decimal
    total_excise: Decimal
    total_declarations: int
    period: str


# ============================================================================
# Monthly Revenue Response
# ============================================================================

class MonthlyRevenue(BaseModel):
    """Monthly revenue data"""
    year: int
    month: int
    month_label: str
    total_revenue: Decimal
    total_duty: Decimal
    total_vat: Decimal
    total_excise: Decimal
    declaration_count: int


# ============================================================================
# Revenue by Port Response
# ============================================================================

class RevenueByPort(BaseModel):
    """Revenue breakdown by port"""
    port_code: str
    port_name: Optional[str] = None
    total_revenue: Decimal
    total_duty: Decimal
    total_vat: Decimal
    declaration_count: int
    percentage: Optional[float] = None


# ============================================================================
# Revenue by Tax Type Response
# ============================================================================

class RevenueByTaxType(BaseModel):
    """Revenue breakdown by tax type"""
    tax_type: str  # CUSTOMS_DUTY, VAT, EXCISE
    total_amount: Decimal
    declaration_count: int
    average_amount: Optional[Decimal] = None
    percentage: Optional[float] = None


# ============================================================================
# Revenue Trend Response
# ============================================================================

class RevenueTrend(BaseModel):
    """Revenue trend over time"""
    period: str
    current_value: Decimal
    previous_value: Optional[Decimal] = None
    change_absolute: Optional[Decimal] = None
    change_percentage: Optional[float] = None
    trend_direction: Optional[str] = None  # UP, DOWN, STABLE


# ============================================================================
# Revenue Comparison Response
# ============================================================================

class RevenueComparison(BaseModel):
    """Comparison of revenue between periods"""
    current_period: str
    previous_period: str
    current_revenue: Decimal
    previous_revenue: Decimal
    variance_absolute: Decimal
    variance_percentage: float


# ============================================================================
# Revenue Calculation Request
# ============================================================================

class RevenueCalculationRequest(BaseModel):
    """Request for revenue calculation"""
    customs_value: float = Field(..., gt=0, description="Customs value")
    hs_code: str = Field(..., min_length=4, max_length=10, description="HS code")
    origin_country: Optional[str] = Field(None, max_length=2, description="Origin country code")
    currency_code: str = Field(default="USD", max_length=3, description="Currency code")


# ============================================================================
# Revenue Calculation Response
# ============================================================================

class RevenueCalculationResponse(BaseModel):
    """Response with calculated revenue breakdown"""
    customs_value: Decimal
    hs_code: str
    duty_rate: float
    customs_duty: Decimal
    vat_rate: float
    vat_amount: Decimal
    excise_rate: Optional[float] = None
    excise_amount: Optional[Decimal] = None
    total_tax_liability: Decimal
    currency_code: str


# ============================================================================
# Revenue Report Request
# ============================================================================

class RevenueReportRequest(BaseModel):
    """Request for revenue report generation"""
    start_date: date
    end_date: date
    group_by: str = Field(default="month", description="Group by: month, port, tax_type")
    include_details: bool = Field(default=False, description="Include detailed breakdown")
    min_records: int = Field(default=5, ge=1, description="Minimum aggregation threshold")


# ============================================================================
# Revenue Report Response
# ============================================================================

class RevenueReportResponse(BaseModel):
    """Revenue report response"""
    period_start: date
    period_end: date
    group_by: str
    total_revenue: Decimal
    records: List[dict]
    record_count: int
    generated_at: datetime


# ============================================================================
# Revenue Statistics Response
# ============================================================================

class RevenueStatistics(BaseModel):
    """Revenue statistics summary"""
    total_revenue: Decimal
    average_revenue: Decimal
    max_revenue: Decimal
    min_revenue: Decimal
    median_revenue: Decimal
    standard_deviation: Optional[Decimal] = None
    record_count: int


# ============================================================================
# Revenue Export Response
# ============================================================================

class RevenueExportResponse(BaseModel):
    """Revenue data export response"""
    export_format: str
    record_count: int
    file_size_bytes: Optional[int] = None
    download_url: Optional[str] = None
    expires_at: Optional[datetime] = None


# ============================================================================
# Revenue Aggregation Request
# ============================================================================

class RevenueAggregationRequest(BaseModel):
    """Request for revenue aggregation"""
    dimensions: List[str] = Field(..., description="Dimensions to aggregate by")
    measures: List[str] = Field(..., description="Measures to calculate")
    filters: Optional[dict] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


# ============================================================================
# Revenue Time Series Request
# ============================================================================

class RevenueTimeSeriesRequest(BaseModel):
    """Request for revenue time series data"""
    start_date: date
    end_date: date
    frequency: str = Field(default="month", description="Frequency: day, week, month, quarter, year")
    metric: str = Field(default="total_revenue", description="Metric to track")
    interpolation: str = Field(default="linear", description="Interpolation method")
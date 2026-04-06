#!/usr/bin/env python3
"""
Trade API Schemas - Pydantic Models for Trade Endpoints
Phase 8 - API Implementation

Contains request/response schemas for trade-related API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ============================================================================
# Trade Summary Response
# ============================================================================

class TradeSummary(BaseModel):
    """Trade summary response"""
    total_value: Decimal
    total_declarations: int
    total_items: int
    period: str
    top_origin_country: Optional[str] = None
    top_destination_port: Optional[str] = None


# ============================================================================
# Trade by Country Response
# ============================================================================

class TradeByCountry(BaseModel):
    """Trade breakdown by country"""
    country_code: str
    country_name: Optional[str] = None
    total_value: Decimal
    total_declarations: int
    total_items: int
    percentage: Optional[float] = None
    top_hs_chapters: Optional[List[dict]] = None


# ============================================================================
# Trade by HS Code Response
# ============================================================================

class TradeByHSCode(BaseModel):
    """Trade breakdown by HS code"""
    hs_code: str
    hs_description: Optional[str] = None
    chapter: str
    total_value: Decimal
    total_declarations: int
    total_quantity: Optional[Decimal] = None
    quantity_unit: Optional[str] = None
    average_value: Optional[Decimal] = None
    percentage: Optional[float] = None


# ============================================================================
# Trade Time Series Response
# ============================================================================

class TradeTimeSeries(BaseModel):
    """Trade time series data"""
    period: str
    total_value: Decimal
    total_declarations: int
    change_percentage: Optional[float] = None
    trend_direction: Optional[str] = None


# ============================================================================
# Top Importers Response
# ============================================================================

class TopImporter(BaseModel):
    """Top importer data"""
    rank: int
    declarant_id: str  # Aggregated, not specific
    total_value: Decimal
    total_declarations: int
    dominant_country: Optional[str] = None
    dominant_hs_chapter: Optional[str] = None


# ============================================================================
# Trade Trend Response
# ============================================================================

class TradeTrend(BaseModel):
    """Trade trend analysis"""
    period: str
    current_value: Decimal
    previous_value: Optional[Decimal] = None
    change_absolute: Optional[Decimal] = None
    change_percentage: Optional[float] = None
    trend_direction: Optional[str] = None
    trend_strength: Optional[str] = None


# ============================================================================
# Trade Forecast Response
# ============================================================================

class TradeForecast(BaseModel):
    """Trade forecast data"""
    forecast_period: str
    forecast_value: Decimal
    confidence_lower: Decimal
    confidence_upper: Decimal
    methodology: str
    forecast_periods: int


# ============================================================================
# Trade Comparison Response
# ============================================================================

class TradeComparison(BaseModel):
    """Comparison of trade between periods"""
    current_period: str
    previous_period: str
    current_value: Decimal
    previous_value: Decimal
    variance_absolute: Decimal
    variance_percentage: float


# ============================================================================
# Port Performance Response
# ============================================================================

class PortPerformance(BaseModel):
    """Port performance metrics"""
    port_code: str
    port_name: Optional[str] = None
    total_declarations: int
    total_value: Decimal
    average_clearance_time: Optional[float] = None
    clearance_rate: Optional[float] = None
    revenue_generated: Optional[Decimal] = None


# ============================================================================
# HS Chapter Aggregation Response
# ============================================================================

class HSChapterAggregation(BaseModel):
    """HS chapter aggregation"""
    chapter: str
    chapter_description: Optional[str] = None
    total_declarations: int
    total_value: Decimal
    total_duty: Decimal
    top_countries: Optional[List[dict]] = None
    top_ports: Optional[List[dict]] = None


# ============================================================================
# Trade Statistics Response
# ============================================================================

class TradeStatistics(BaseModel):
    """Trade statistics summary"""
    total_value: Decimal
    average_value: Decimal
    max_value: Decimal
    min_value: Decimal
    median_value: Decimal
    value_standard_deviation: Optional[Decimal] = None
    total_declarations: int
    unique_countries: int
    unique_hs_chapters: int


# ============================================================================
# Trade Aggregation Request
# ============================================================================

class TradeAggregationRequest(BaseModel):
    """Request for trade aggregation"""
    dimensions: List[str] = Field(..., description="Dimensions: country, hs_chapter, port, month")
    measures: List[str] = Field(..., description="Measures: value, declarations, items, duty")
    filters: Optional[dict] = None
    order_by: Optional[str] = None
    order_direction: str = Field(default="desc", description="asc or desc")
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


# ============================================================================
# Trade Export Response
# ============================================================================

class TradeExportResponse(BaseModel):
    """Trade data export response"""
    export_format: str
    record_count: int
    file_size_bytes: Optional[int] = None
    download_url: Optional[str] = None
    expires_at: Optional[datetime] = None


# ============================================================================
# Trade Volume Metrics
# ============================================================================

class TradeVolumeMetrics(BaseModel):
    """Trade volume metrics"""
    total_quantity: Decimal
    quantity_unit: str
    average_quantity: Optional[Decimal] = None
    max_quantity: Optional[Decimal] = None
    min_quantity: Optional[Decimal] = None
    shipment_count: int


# ============================================================================
# Trade Flow Response
# ============================================================================

class TradeFlow(BaseModel):
    """Trade flow between countries"""
    origin_country: str
    destination_country: str
    total_value: Decimal
    declaration_count: int
    primary_hs_chapters: List[str]


# ============================================================================
# Trade Analysis Request
# ============================================================================

class TradeAnalysisRequest(BaseModel):
    """Request for trade analysis"""
    start_date: date
    end_date: date
    analysis_type: str = Field(..., description="Type: trend, forecast, comparison")
    group_by: Optional[str] = None
    metric: str = Field(default="total_value")


# ============================================================================
# Trade Analysis Response
# ============================================================================

class TradeAnalysisResponse(BaseModel):
    """Trade analysis response"""
    analysis_type: str
    period_start: date
    period_end: date
    results: List[dict]
    summary: dict
    generated_at: datetime
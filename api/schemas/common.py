#!/usr/bin/env python3
"""
Common API Schemas - Shared Pydantic Models
Phase 8 - API Implementation

Contains shared schemas used across all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ============================================================================
# Common Response Wrappers
# ============================================================================

class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = True
    message: str = "Success"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    success: bool = True
    message: str = "Success"
    data: List[dict]
    pagination: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Date Range Parameters
# ============================================================================

class DateRangeParams(BaseModel):
    """Date range query parameters"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# ============================================================================
# Aggregation Parameters
# ============================================================================

class AggregationParams(BaseModel):
    """Common aggregation parameters"""
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Maximum results")
    offset: Optional[int] = Field(default=0, ge=0, description="Pagination offset")
    min_records: int = Field(default=5, description="Minimum aggregation threshold")


# ============================================================================
# Filter Parameters
# ============================================================================

class FilterParams(BaseModel):
    """Common filter parameters"""
    port_code: Optional[str] = None
    country_code: Optional[str] = None
    hs_code: Optional[str] = None
    declarant_id: Optional[str] = None
    status: Optional[str] = None


# ============================================================================
# Time Period Parameters
# ============================================================================

class TimePeriodParams(BaseModel):
    """Time period parameters for trend analysis"""
    period: str = Field(..., description="Period identifier (e.g., '2024-01')")
    value: float = Field(..., description="Value for the period")


# ============================================================================
# Metadata Models
# ============================================================================

class PortReference(BaseModel):
    """Port reference data"""
    port_code: str
    port_name: str
    region: Optional[str] = None
    port_type: Optional[str] = None


class CountryReference(BaseModel):
    """Country reference data"""
    country_code: str
    country_name: str
    region: Optional[str] = None


class HSCodeReference(BaseModel):
    """HS code reference data"""
    hs_code: str
    description: str
    duty_rate: Optional[float] = None
    vat_rate: Optional[float] = None
    unit: Optional[str] = None


# ============================================================================
# Error Models
# ============================================================================

class ApiError(BaseModel):
    """API error response"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Health Check
# ============================================================================

class HealthStatus(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str


# ============================================================================
# Export Config
# ============================================================================

class ExportConfig(BaseModel):
    """Configuration for data export"""
    format: str = Field(default="json", description="Export format")
    include_metadata: bool = Field(default=True, description="Include response metadata")
    compression: Optional[str] = Field(default=None, description="Compression type")
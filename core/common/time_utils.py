"""
Common Time Utilities
Phase 5 - Utility Functions
"""

from datetime import datetime, date
from typing import Optional


def get_month_label(year: int, month: int) -> str:
    """Generate month label (e.g., '2024-01')"""
    return f"{year:04d}-{month:02d}"


def get_fiscal_year(dt: datetime) -> int:
    """Get fiscal year (assuming Jan-Dec calendar)"""
    return dt.year


def get_quarter(dt: datetime) -> int:
    """Get quarter (1-4)"""
    return (dt.month - 1) // 3 + 1


def format_date_iso(dt: date) -> str:
    """Format date as ISO string"""
    return dt.isoformat()


def parse_date(date_str: str) -> Optional[date]:
    """Parse date string safely"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def is_business_day(dt: datetime) -> bool:
    """Check if date is a business day (Mon-Fri)"""
    return dt.weekday() < 5

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func
from datetime import date
from typing import List, Dict, Any

from ..models import MonthlyRevenue, TradeVolume, TaxTypeBreakdown

class RevenueRepository:
    """
    Repository handling all Data Access layer operations for Revenue Analytics.
    Strictly query-only to maintain the boundary of the V2 analytical scope.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_monthly_revenue_series(self, start_year: int = 2020) -> List[MonthlyRevenue]:
        """
        Fetch the entire monthly revenue timeseries for forecasting models.
        """
        stmt = select(MonthlyRevenue).where(MonthlyRevenue.year >= start_year).order_by(MonthlyRevenue.year, MonthlyRevenue.month)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_tax_breakdown(self, start_date: date, end_date: date) -> List[TaxTypeBreakdown]:
        """
        Fetch grouped tax breakdowns to understand excise vs vat vs duty ratios.
        """
        stmt = select(TaxTypeBreakdown).where(
            TaxTypeBreakdown.date >= start_date,
            TaxTypeBreakdown.date <= end_date
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_trade_volume_series(self) -> List[TradeVolume]:
        """
        Fetch the aggregated trade volume throughput for volume modeling.
        """
        stmt = select(TradeVolume).order_by(TradeVolume.date)
        result = await self.session.execute(stmt)
        return result.scalars().all()

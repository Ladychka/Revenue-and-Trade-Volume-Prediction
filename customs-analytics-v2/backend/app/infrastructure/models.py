from sqlalchemy import Column, Integer, String, Float, Date, BigInteger, Numeric, ForeignKey, UniqueConstraint
from datetime import date
from .db import Base

class MonthlyRevenue(Base):
    """
    Time-series table tracking aggregated revenue collected by month.
    Designed specifically for the SARIMA and Holt-Winters forecasting engines.
    """
    __tablename__ = "monthly_revenue"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    
    # Financial metrics (using Numeric for precise decimal arithmetic)
    total_revenue = Column(Numeric(15, 2), nullable=False)
    customs_duty = Column(Numeric(15, 2), nullable=False)
    vat = Column(Numeric(15, 2), nullable=False)
    excise_tax = Column(Numeric(15, 2), nullable=False)
    
    # Operational metrics
    declaration_count = Column(Integer, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('year', 'month', name='uix_monthly_revenue_year_month'),
    )

    def __repr__(self):
        return f"<MonthlyRevenue {self.year}-{self.month:02d}: ${self.total_revenue}>"


class TradeVolume(Base):
    """
    Aggregated trade volume metrics for forecasting non-revenue throughput.
    """
    __tablename__ = "trade_volume"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True, unique=True)
    
    # Volume metrics
    total_customs_value = Column(Numeric(15, 2), nullable=False)
    total_items = Column(Integer, nullable=False)
    total_declarations = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<TradeVolume {self.date}: {self.total_declarations} decls>"


class TaxTypeBreakdown(Base):
    """
    Granular breakdown of taxes collected, specifically built to 
    address the V1 gap related to missing/zero excise taxes.
    """
    __tablename__ = "tax_type_breakdown"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    
    tax_category = Column(String(50), nullable=False, index=True) # e.g., 'DUTY', 'VAT', 'EXCISE_ALCOHOL', 'EXCISE_FUEL'
    amount_collected = Column(Numeric(15, 2), nullable=False)
    
    def __repr__(self):
        return f"<TaxBreakdown {self.date} [{self.tax_category}]: ${self.amount_collected}>"

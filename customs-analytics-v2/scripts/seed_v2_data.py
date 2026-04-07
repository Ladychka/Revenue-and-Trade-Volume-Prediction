import asyncio
import os
import sys
from datetime import date, timedelta
import random
from decimal import Decimal

# Add backend directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.infrastructure.db import engine, Base, AsyncSessionLocal
from app.infrastructure.models import MonthlyRevenue, TradeVolume, TaxTypeBreakdown

async def init_db():
    print("Creating database tables...")
    async with engine.begin() as conn:
        # Drop and recreate for a clean slate
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

async def seed_data():
    print("Seeding synthetic data...")
    random.seed(42)  # Deterministic generation
    
    session = AsyncSessionLocal()
    
    try:
        # Generate 4 years of monthly revenue data (2020-2023)
        print("Seeding MonthlyRevenue...")
        base_revenue = 10000000  # $10M base
        for year in range(2020, 2024):
            for month in range(1, 13):
                # Add seasonality (higher in Q4) and trend (growing over years)
                seasonality = 1.2 if month in [10, 11, 12] else 1.0
                trend = 1.0 + ((year - 2020) * 0.1)
                random_noise = random.uniform(0.9, 1.1)
                
                rev_val = Decimal(str(round(base_revenue * seasonality * trend * random_noise, 2)))
                duty = rev_val * Decimal('0.30')
                vat = rev_val * Decimal('0.50')
                # Explicitly seed excise tax to fix the V1 gap
                excise = rev_val * Decimal('0.20') 
                
                decls = random.randint(5000, 8000)
                
                mr = MonthlyRevenue(
                    year=year,
                    month=month,
                    total_revenue=rev_val,
                    customs_duty=duty,
                    vat=vat,
                    excise_tax=excise,
                    declaration_count=decls
                )
                session.add(mr)
        
        # Generate 30 days of trade volume for short term metrics
        print("Seeding TradeVolume and TaxTypeBreakdown...")
        start_date = date(2024, 1, 1)
        for i in range(30):
            current_date = start_date + timedelta(days=i)
            tv = TradeVolume(
                date=current_date,
                total_customs_value=Decimal(str(random.uniform(500000, 1500000))),
                total_items=random.randint(500, 1500),
                total_declarations=random.randint(100, 300)
            )
            session.add(tv)
            
            # Tax breakdown per day
            taxes = [
                ('DUTY', Decimal(str(random.uniform(10000, 50000)))),
                ('VAT', Decimal(str(random.uniform(20000, 80000)))),
                ('EXCISE_ALCOHOL', Decimal(str(random.uniform(5000, 15000)))),
                ('EXCISE_TOBACCO', Decimal(str(random.uniform(3000, 10000)))),
                ('EXCISE_FUEL', Decimal(str(random.uniform(10000, 30000))))
            ]
            
            for tax_type, amount in taxes:
                ttb = TaxTypeBreakdown(
                    date=current_date,
                    tax_category=tax_type,
                    amount_collected=amount
                )
                session.add(ttb)
        
        await session.commit()
        print("Seeding completed successfully.")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        await session.rollback()
    finally:
        await session.close()
        # Dispose the engine so the script can exit cleanly
        await engine.dispose()

async def main():
    await init_db()
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())

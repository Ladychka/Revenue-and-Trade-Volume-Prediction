import pandas as pd
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Architecture imports
from app.infrastructure.db import get_db_session
from app.infrastructure.repositories.revenue_repo import RevenueRepository
from app.core.forecasting.base import ForecastResult
from app.core.forecasting.sarima import SARIMAForecaster
from app.core.forecasting.holt_winters import HoltWintersForecaster
from app.core.forecasting.moving_average import MovingAverageForecaster
from app.core.calculations.scenario_engine import ScenarioEngine, ScenarioParameters

router = APIRouter()

async def get_repository(session: AsyncSession = Depends(get_db_session)) -> RevenueRepository:
    return RevenueRepository(session)


@router.get("/forecast", response_model=ForecastResult, tags=["Analytics"])
async def generate_baseline_forecast(
    model: str = Query("sarima", description="Forecasting algorithm to use: 'sarima' or 'holt'"),
    horizon: int = Query(6, ge=1, le=24, description="Months ahead to forecast"),
    repo: RevenueRepository = Depends(get_repository)
):
    """
    Generates a deterministic financial forecast using the specified algorithm.
    Reads historical data directly from the read-only PostgreSQL views layer.
    """
    try:
        data = await repo.get_monthly_revenue_series()
        if not data:
            raise HTTPException(status_code=404, detail="No analytical data found to forecast")

        # Convert ORM to pandas DataFrame
        df = pd.DataFrame([{
            'date': f"{r.year}-{r.month:02d}-01", 
            'total_revenue': float(r.total_revenue)
        } for r in data])

        # Instantiate algorithm dynamically
        forecaster_cls = SARIMAForecaster
        if model.lower() == "holt":
            forecaster_cls = HoltWintersForecaster
        elif model.lower() == "moving_average":
            forecaster_cls = MovingAverageForecaster
            
        engine = forecaster_cls(data=df, target_column='total_revenue')

        return engine.forecast(horizon=horizon)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting engine error: {str(e)}")


@router.post("/simulate", response_model=ForecastResult, tags=["Scenario Engine"])
async def simulate_what_if_scenario(
    params: ScenarioParameters,
    model: str = Query("sarima", description="Base forecasting algorithm"),
    horizon: int = Query(6, ge=1, le=24),
    repo: RevenueRepository = Depends(get_repository)
):
    """
    Performs a deterministic What-if scenario.
    First generates the baseline forecast (ex: +5% growth naturally), 
    then applies policy modifications (e.g., +2% tax, -0.1 elasticity) on top of it.
    """
    try:
        # Step 1: Get baseline forecast
        baseline = await generate_baseline_forecast(model=model, horizon=horizon, repo=repo)
        
        # Step 2: Apply scenario engine modifiers deterministically
        return ScenarioEngine.simulate(baseline, params)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

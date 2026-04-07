import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.forecasting.evaluator import ForecastEvaluator
from app.core.forecasting.base import ForecastResult, ForecastPoint
from app.core.calculations.scenario_engine import ScenarioEngine, ScenarioParameters

def test_evaluator_metrics():
    actuals = [100.0, 110.0, 120.0]
    preds = [100.0, 105.0, 125.0]
    
    metrics = ForecastEvaluator.calculate_metrics(actuals, preds)
    
    assert "mae" in metrics
    assert "rmse" in metrics
    assert "mape_percent" in metrics
    
    # Hand calculation:
    # Errors: 0, 5, -5
    # Absolute Errors: 0, 5, 5. Mean MAE = 10/3 = 3.33
    assert metrics['mae'] == 3.33

def test_evaluator_zero_division_guard():
    # Attempting to divide by 0 in MAPE should not crash
    actuals = [0.0, 0.0]
    preds = [10.0, 10.0]
    metrics = ForecastEvaluator.calculate_metrics(actuals, preds)
    assert metrics['mape_percent'] == 0.0

def test_scenario_engine_elasticity():
    # Setup dummy baseline
    base = ForecastResult(
        model_name="Test Model",
        horizon_months=1,
        historical_dates=[], historical_values=[],
        forecast_points=[
            ForecastPoint(period="2025-01", point_forecast=100.0, confidence_lower=90.0, confidence_upper=110.0)
        ]
    )
    
    # Increase tax rate by 10% (0.10)
    # Elasticity is -0.5, meaning volume should drop by 5% (-0.05)
    params = ScenarioParameters(
        tax_rate_delta=0.10,
        volume_shock=0.0,
        elasticity_factor=-0.5,
        scenario_name="Tax Hike"
    )
    
    simulated = ScenarioEngine.simulate(base, params)
    
    # Expected volume modifier: 1.0 + 0.0 + (0.10 * -0.5) = 0.95
    # Expected revenue modifier: 0.95 * (1.0 + 0.10) = 1.045
    # New point forecast: 100 * 1.045 = 104.5
    
    new_point = simulated.forecast_points[0]
    assert abs(new_point.point_forecast - 104.5) < 0.01 
    assert "Tax Hike" in simulated.model_name

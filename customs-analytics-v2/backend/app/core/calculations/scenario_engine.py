from pydantic import BaseModel, Field
from typing import Optional
from copy import deepcopy

# Import the strict interfaces we set up in Phase 2
from app.core.forecasting.base import ForecastResult, ForecastPoint


class ScenarioParameters(BaseModel):
    """
    Deterministic parameters for What-If scenario simulations.
    These deltas are applied procedurally on top of base algorithmic forecasts.
    """
    # Rate Adjustments (+/- percentage points)
    # e.g., 0.05 means increasing a tax rate by 5%
    tax_rate_delta: float = Field(default=0.0, description="Percentage point change in tax rate")
    
    # Macro Shocks
    # e.g., -0.15 means an unexpected 15% drop in overall trade volume 
    volume_shock: float = Field(default=0.0, description="Percentage shock to total volume/value")
    
    # Demand Elasticity
    # e.g., If elasticity is -0.5, a 10% increase in tax rate drops volume by 5%
    elasticity_factor: float = Field(default=0.0, description="Price elasticity of demand coefficient")
    
    scenario_name: Optional[str] = Field(default="Custom Simulation")


class ScenarioEngine:
    """
    Applies custom scenario shocks and policy changes to baseline forecasts.
    """

    @staticmethod
    def simulate(baseline: ForecastResult, params: ScenarioParameters) -> ForecastResult:
        """
        Takes a statistically generated baseline forecast and deterministically
        mutates the financial projections based on policy parameters.
        Returns a brand new, fully-conforming ForecastResult object.
        """
        
        # We deepcopy to avoid mutating the baseline cache in memory
        simulated_result = deepcopy(baseline)
        
        # Update metadata so the frontend knows this is a simulation
        simulated_result.model_name = f"{baseline.model_name} | Scenario: {params.scenario_name}"
        
        # Calculate elasticity impact
        # Example: Tax rate goes up 10% (0.1), elasticity is -0.5. Volume drops by 5%.
        # Total impact incorporates the direct volume shock plus the elasticity effect.
        elasticity_impact = params.tax_rate_delta * params.elasticity_factor
        total_volume_modifier = 1.0 + params.volume_shock + elasticity_impact
        
        # Ensure volume doesn't drop below 0 mathematically
        total_volume_modifier = max(0.0, total_volume_modifier)

        # Revenue modifier = (New Volume) * (1 + Tax Delta)
        # Assuming the baseline forecast represents a 1.0 base rate mapping
        # E.g., volume drops to 0.95, but tax rate increases by 10%. 0.95 * 1.10 = 1.045
        revenue_modifier = total_volume_modifier * (1.0 + params.tax_rate_delta)

        # Apply deterministic mutations to the future points
        for point in simulated_result.forecast_points:
            point.point_forecast = point.point_forecast * revenue_modifier
            point.confidence_lower = point.confidence_lower * revenue_modifier
            point.confidence_upper = point.confidence_upper * revenue_modifier

        return simulated_result

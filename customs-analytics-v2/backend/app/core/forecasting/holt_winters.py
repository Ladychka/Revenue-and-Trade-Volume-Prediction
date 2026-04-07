import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from .base import BaseForecaster, ForecastResult, ForecastPoint
from .evaluator import ForecastEvaluator

class HoltWintersForecaster(BaseForecaster):
    """
    Exponential Smoothing (Holt-Winters) model.
    Excellent for capturing obvious trends and seasonality in time-series data
    without demanding the heavy computational overhead of SARIMA.
    """

    def forecast(self, horizon: int = 6) -> ForecastResult:
        
        # We need a proper frequency on the index for statsmodels.
        # Assuming monthly data since this is customs analytics.
        ts_data = self.data[self.target_column].asfreq('MS', method='bfill')
        
        # Fit Holt-Winters
        # Trend=add and seasonal=add as default safe parameters for revenue
        # Seasonal periods=12 assuming yearly cycles in monthly data
        model = ExponentialSmoothing(
            ts_data, 
            trend="add", 
            seasonal="add", 
            seasonal_periods=12,
            initialization_method="estimated"
        )
        fitted_model = model.fit()

        # Forecast
        forecast_values = fitted_model.forecast(horizon)
        
        # HoltWinters doesn't give clean confidence intervals out of the box in statsmodels
        # We will approximate an 80% interval using the residuals standard deviation
        rmse = fitted_model.resid.std()
        
        points = []
        for dt, val in forecast_values.items():
            dt_str = dt.strftime("%Y-%m")
            # 1.28 represents 80% confidence bound multiplier
            lower = max(0.0, float(val - (1.28 * rmse)))
            upper = float(val + (1.28 * rmse))
            
            points.append(
                ForecastPoint(
                    period=dt_str,
                    point_forecast=float(val),
                    confidence_lower=lower,
                    confidence_upper=upper
                )
            )

        # In sample metrics
        metrics = ForecastEvaluator.calculate_metrics(
            actuals=ts_data.tolist(),
            predictions=fitted_model.fittedvalues.tolist()
        )

        return ForecastResult(
            model_name="Holt-Winters Exponential Smoothing",
            horizon_months=horizon,
            historical_dates=[d.strftime("%Y-%m") for d in ts_data.index],
            historical_values=[float(v) for v in ts_data.values],
            forecast_points=points,
            metrics=metrics
        )

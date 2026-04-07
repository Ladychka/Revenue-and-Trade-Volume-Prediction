import pandas as pd
from typing import List
from .base import BaseForecaster, ForecastResult, ForecastPoint
from .evaluator import ForecastEvaluator
import numpy as np

class MovingAverageForecaster(BaseForecaster):
    """
    Moving Average forecasting model.
    Provides a simple baseline trend analysis by averaging the last 'window_size' months.
    """

    def forecast(self, horizon: int = 6) -> ForecastResult:
        window_size = 3
        
        ts_data = self.data[self.target_column].asfreq('MS', method='bfill')
        values = ts_data.values.tolist()
        
        # Calculate in-sample predictions for evaluation
        # Shifted by 1 so prediction for month T relies on [T-window : T-1]
        in_sample_preds = [0.0] * len(values)
        for i in range(len(values)):
            if i < window_size:
                in_sample_preds[i] = values[i]
            else:
                in_sample_preds[i] = np.mean(values[i-window_size:i])

        forecast_points = []
        
        # Generate future points
        last_values = values[-window_size:]
        current_date = ts_data.index[-1]
        
        # Calculate a basic standard deviation of residuals for confidence intervals
        residuals = np.array(values[window_size:]) - np.array(in_sample_preds[window_size:])
        rmse = np.std(residuals) if len(residuals) > 0 else 0

        for i in range(1, horizon + 1):
            next_val = np.mean(last_values)
            next_date = current_date + pd.DateOffset(months=i)
            
            # Simple confidence bounds
            lower = max(0.0, float(next_val - (1.28 * rmse)))
            upper = float(next_val + (1.28 * rmse))
            
            forecast_points.append(
                ForecastPoint(
                    period=next_date.strftime("%Y-%m"),
                    point_forecast=float(next_val),
                    confidence_lower=lower,
                    confidence_upper=upper
                )
            )
            
            # Slide window forward
            last_values.pop(0)
            last_values.append(next_val)

        metrics = ForecastEvaluator.calculate_metrics(
            actuals=values[window_size:],  # ignore initial warm-up period
            predictions=in_sample_preds[window_size:]
        )

        return ForecastResult(
            model_name=f"Moving Average ({window_size}-Month)",
            horizon_months=horizon,
            historical_dates=[d.strftime("%Y-%m") for d in ts_data.index],
            historical_values=[float(v) for v in ts_data.values],
            forecast_points=forecast_points,
            metrics=metrics
        )

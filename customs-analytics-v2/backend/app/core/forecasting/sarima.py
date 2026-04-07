import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from .base import BaseForecaster, ForecastResult, ForecastPoint
from .evaluator import ForecastEvaluator

class SARIMAForecaster(BaseForecaster):
    """
    Seasonal Auto-Regressive Integrated Moving Average (SARIMA).
    The gold standard for statistical forecasting of complex, multi-seasonal
    revenue signals within the customs domain.
    """

    def forecast(self, horizon: int = 6) -> ForecastResult:
        
        ts_data = self.data[self.target_column].asfreq('MS', method='bfill')
        
        # Hardcoding the (p,d,q) x (P,D,Q,m) parameters for this V2 implementation.
        # In a heavier system, this would be auto_arima, but we want deterministic speed.
        # (1,1,1) x (1,1,1,12) is a very standard starting point for monthly financial data.
        model = SARIMAX(
            ts_data,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 12),
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        
        fitted_model = model.fit(disp=False)
        
        # Get forecast with confidence intervals
        forecast_obj = fitted_model.get_forecast(steps=horizon)
        predictions = forecast_obj.predicted_mean
        conf_int = forecast_obj.conf_int(alpha=0.10) # 90% confidence
        
        points = []
        for i, (dt, val) in enumerate(predictions.items()):
            dt_str = dt.strftime("%Y-%m")
            # Columns in conf_int are typically 'lower <target>' and 'upper <target>'
            lower_col = conf_int.columns[0]
            upper_col = conf_int.columns[1]
            
            lower = max(0.0, float(conf_int.iloc[i][lower_col]))
            upper = float(conf_int.iloc[i][upper_col])
            
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
            model_name="SARIMA (1,1,1)x(1,1,1,12)",
            horizon_months=horizon,
            historical_dates=[d.strftime("%Y-%m") for d in ts_data.index],
            historical_values=[float(v) for v in ts_data.values],
            forecast_points=points,
            metrics=metrics
        )

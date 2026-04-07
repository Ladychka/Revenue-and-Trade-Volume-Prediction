import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from typing import Dict, List

class ForecastEvaluator:
    """
    Evaluator to track and calculate deterministic accuracy metrics 
    for the forecasting pipelines.
    """

    @staticmethod
    def calculate_metrics(actuals: List[float], predictions: List[float]) -> Dict[str, float]:
        """
        Calculates MAE, MSE, and RMSE.
        """
        if not actuals or not predictions or len(actuals) != len(predictions):
            return {"mae": 0.0, "mse": 0.0, "rmse": 0.0, "mape": 0.0}

        y_true = np.array(actuals)
        y_pred = np.array(predictions)

        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        
        # Mean Absolute Percentage Error
        # Avoid division by zero
        non_zero_idx = y_true != 0
        if np.any(non_zero_idx):
            mape = np.mean(np.abs((y_true[non_zero_idx] - y_pred[non_zero_idx]) / y_true[non_zero_idx])) * 100
        else:
            mape = 0.0

        return {
            "mae": round(float(mae), 2),
            "mse": round(float(mse), 2),
            "rmse": round(float(rmse), 2),
            "mape_percent": round(float(mape), 2)
        }

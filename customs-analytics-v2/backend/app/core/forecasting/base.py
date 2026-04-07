from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import pandas as pd

class ForecastPoint(BaseModel):
    """
    A single point in a forecast result, typically representing a future month.
    """
    period: str  # YYYY-MM
    point_forecast: float
    confidence_lower: float
    confidence_upper: float

class ForecastResult(BaseModel):
    """
    Standardized payload returned by any forecasting model in the V2 engine.
    Ensures that the API and Frontend receive a predictable structure regardless 
    of the underlying data science model utilized.
    """
    model_name: str
    horizon_months: int
    historical_dates: List[str]
    historical_values: List[float]
    forecast_points: List[ForecastPoint]
    metrics: Optional[Dict[str, float]] = None


class BaseForecaster(ABC):
    """
    Abstract Base Class enforcing the Forecasting Engine interface.
    Every new algorithmic model built must implement this interface.
    """
    
    def __init__(self, data: pd.DataFrame, target_column: str, date_column: str = 'date'):
        """
        Expects a pandas DataFrame containing a strict time-series.
        """
        self.data = data
        self.target_column = target_column
        self.date_column = date_column
        
        # Ensure dates are in the correct format and sorted
        self.data[self.date_column] = pd.to_datetime(self.data[self.date_column])
        self.data.sort_values(by=self.date_column, inplace=True)
        self.data.set_index(self.date_column, inplace=True)

    @abstractmethod
    def forecast(self, horizon: int = 6) -> ForecastResult:
        """
        Executes the forecast and returns the standardized ForecastResult schema.
        """
        pass

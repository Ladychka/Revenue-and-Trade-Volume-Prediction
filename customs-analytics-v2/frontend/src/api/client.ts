import axios from 'axios';

// The proxy in vite.config.ts handles mapping this to http://localhost:8000
const apiClient = axios.create({
  baseURL: '/api/v2',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ForecastPoint {
  period: string;
  point_forecast: number;
  confidence_lower: number;
  confidence_upper: number;
}

export interface ForecastResult {
  model_name: string;
  horizon_months: number;
  historical_dates: string[];
  historical_values: number[];
  forecast_points: ForecastPoint[];
  metrics: Record<string, number> | null;
}

export interface ScenarioParams {
  tax_rate_delta: number;
  volume_shock: number;
  elasticity_factor: number;
  scenario_name: string;
}

export const getBaselineForecast = async (model: string = 'sarima', horizon: number = 6) => {
  const response = await apiClient.get<ForecastResult>('/forecast', {
    params: { model, horizon }
  });
  return response.data;
};

export const simulateScenario = async (params: ScenarioParams, model: string = 'sarima', horizon: number = 6) => {
  const response = await apiClient.post<ForecastResult>('/simulate', params, {
    params: { model, horizon }
  });
  return response.data;
};

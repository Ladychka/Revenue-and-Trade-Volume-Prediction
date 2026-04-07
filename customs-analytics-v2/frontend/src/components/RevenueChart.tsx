import { useMemo } from 'react';
import {
  ComposedChart, Line, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import type { ForecastResult } from '../api/client';

interface RevenueChartProps {
  data: ForecastResult | null;
  baseData?: ForecastResult | null; // For comparison
  isLoading: boolean;
}

const formatter = (value: number) => `$${(value / 1000000).toFixed(2)}M`;

export const RevenueChart: React.FC<RevenueChartProps> = ({ data, baseData, isLoading }) => {
  
  const chartData = useMemo(() => {
    if (!data) return [];
    
    // Process historical data
    const hist = data.historical_dates.map((date, i) => ({
      period: date,
      historical: data.historical_values[i],
    }));

    // Process forecast data
    const fore = data.forecast_points.map((point) => ({
      period: point.period,
      forecast: point.point_forecast,
      lowerBound: point.confidence_lower,
      upperBound: point.confidence_upper,
      // If we are comparing against a baseline scenario
      baselineForecast: baseData ? baseData.forecast_points.find(p => p.period === point.period)?.point_forecast : undefined
    }));

    return [...hist, ...fore];
  }, [data, baseData]);

  if (isLoading) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-slate-50/50 rounded-2xl glass-panel shadow-sm">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-slate-50/50 rounded-2xl glass-panel shadow-sm text-slate-400">
        No forecast data available. Configure parameters to begin.
      </div>
    );
  }

  return (
    <div className="w-full h-96 p-6 rounded-2xl glass-panel shadow-sm bg-white border border-slate-100">
      <h3 className="text-lg font-semibold text-slate-800 mb-6">{data.model_name}</h3>
      <ResponsiveContainer width="100%" height="85%">
        <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.2}/>
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorHist" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#94a3b8" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
          <XAxis 
            dataKey="period" 
            tick={{ fill: '#64748b', fontSize: 12 }}
            axisLine={false}
            tickLine={false}
            dy={10}
            minTickGap={30}
          />
          <YAxis 
            tickFormatter={formatter}
            tick={{ fill: '#64748b', fontSize: 12 }}
            axisLine={false}
            tickLine={false}
            dx={-10}
          />
          <Tooltip 
            formatter={(value: number) => formatter(value)}
            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          
          {/* Historical Data Area */}
          <Area 
            type="monotone" 
            dataKey="historical" 
            stroke="#94a3b8" 
            strokeWidth={2}
            fill="url(#colorHist)" 
            name="Historical Revenue"
          />
          
          {/* Base Forecast Line (If comparing) */}
          {baseData && (
            <Line 
              type="monotone" 
              dataKey="baselineForecast" 
              stroke="#cbd5e1" 
              strokeWidth={2} 
              strokeDasharray="5 5"
              name="Baseline Forecast" 
              dot={false}
            />
          )}

          {/* Active Forecast Range Area */}
          <Area 
            type="monotone" 
            dataKey="upperBound" 
            stroke="none" 
            fill="#e0e7ff" 
            fillOpacity={0.5} 
            name="Confidence Upper"
            legendType="none"
          />
          <Area 
            type="monotone" 
            dataKey="lowerBound" 
            stroke="none" 
            fill="#fff" 
            fillOpacity={1} 
            name="Confidence Lower"
            legendType="none"
          />

          {/* Active Forecast Line */}
          <Line 
            type="monotone" 
            dataKey="forecast" 
            stroke="#4f46e5" 
            strokeWidth={3} 
            name="Simulated Output" 
            dot={{ r: 4, fill: '#4f46e5', strokeWidth: 0 }}
            activeDot={{ r: 6, stroke: '#c7d2fe', strokeWidth: 4 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

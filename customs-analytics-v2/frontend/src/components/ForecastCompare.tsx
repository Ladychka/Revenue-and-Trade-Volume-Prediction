import type React from 'react';
import type { ForecastResult } from '../api/client';
import { Target, Activity, Sigma } from 'lucide-react';

interface ForecastCompareProps {
  baselineData: ForecastResult | null;
  activeData: ForecastResult | null;
}

export const ForecastCompare: React.FC<ForecastCompareProps> = ({ baselineData, activeData }) => {
  if (!activeData || !activeData.metrics) return null;
  
  const isSimulated = activeData !== baselineData && baselineData !== null;
  const metrics = activeData.metrics;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-100 flex flex-col md:flex-row gap-8 justify-between mt-4">
      <div className="flex-1">
        <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-4 flex items-center gap-2">
          <Activity size={16} /> Data Science Evaluation
        </h3>
        
        <div className="grid grid-cols-3 gap-6">
          <div>
            <p className="text-xs font-semibold text-slate-400 mb-1 flex items-center gap-1">
              <Target size={12}/> MAPE
            </p>
            <p className="text-2xl font-bold text-slate-800">{metrics.mape_percent}%</p>
            <p className="text-xs text-slate-400 mt-1">Mean Absolute Percentage Error</p>
          </div>
          
          <div>
            <p className="text-xs font-semibold text-slate-400 mb-1 flex items-center gap-1">
              <Sigma size={12}/> MAE
            </p>
            <p className="text-xl font-bold text-slate-700">{metrics.mae}</p>
            <p className="text-xs text-slate-400 mt-1">Mean Absolute Error</p>
          </div>

          <div>
            <p className="text-xs font-semibold text-slate-400 mb-1 flex items-center gap-1">
              <Target size={12}/> RMSE
            </p>
            <p className="text-xl font-bold text-slate-700">{metrics.rmse}</p>
            <p className="text-xs text-slate-400 mt-1">Root Mean Squared Error</p>
          </div>
        </div>
      </div>

      {isSimulated && (
        <div className="md:border-l md:border-slate-200 md:pl-8 flex-1">
           <h3 className="text-sm font-bold text-indigo-500 uppercase tracking-wider mb-4">
            Scenario active
          </h3>
          <p className="text-slate-600 text-sm">
            You are currently viewing a deterministic simulation.<br/>
            Baseline Model: <span className="font-semibold">{baselineData?.model_name || 'N/A'}</span>
          </p>
        </div>
      )}
    </div>
  );
};

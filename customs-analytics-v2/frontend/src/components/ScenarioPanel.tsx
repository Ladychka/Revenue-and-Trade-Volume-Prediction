import React, { useState } from 'react';
import { Activity, TrendingUp, Sliders } from 'lucide-react';
import type { ScenarioParams } from '../api/client';

interface ScenarioPanelProps {
  onSimulate: (params: ScenarioParams) => void;
  onReset: () => void;
  isSimulating: boolean;
}

export const ScenarioPanel: React.FC<ScenarioPanelProps> = ({ onSimulate, onReset, isSimulating }) => {
  const [taxDelta, setTaxDelta] = useState<number>(0);
  const [volShock, setVolShock] = useState<number>(0);
  const [elasticity, setElasticity] = useState<number>(-0.5); // Default reasonable elasticity
  
  const handleSimulate = () => {
    onSimulate({
      tax_rate_delta: taxDelta / 100, // Converting % to decimal
      volume_shock: volShock / 100,
      elasticity_factor: elasticity,
      scenario_name: "Custom Deterministic Scenario"
    });
  };

  const handleReset = () => {
    setTaxDelta(0);
    setVolShock(0);
    setElasticity(-0.5);
    onReset();
  };

  return (
    <div className="w-full glass-panel rounded-2xl p-6 bg-white shadow-sm border border-slate-100 h-full">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
          <Sliders size={20} />
        </div>
        <h2 className="text-xl font-bold text-slate-800 tracking-tight">Scenario Engine</h2>
      </div>

      <div className="space-y-8">
        {/* Control: Tax Delta */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
              <TrendingUp size={16} className="text-emerald-500" />
              Tax Rate Adjustment
            </label>
            <span className="text-sm font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
              {taxDelta > 0 ? '+' : ''}{taxDelta}%
            </span>
          </div>
          <input 
            type="range" 
            min="-20" max="20" step="1"
            value={taxDelta}
            onChange={(e) => setTaxDelta(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
          />
          <p className="text-xs text-slate-400 mt-2">Adjust statutory rate directly.</p>
        </div>

        {/* Control: Macro Volume Shock */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
              <Activity size={16} className="text-rose-500" />
              Macro Volume Shock
            </label>
            <span className="text-sm font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
              {volShock > 0 ? '+' : ''}{volShock}%
            </span>
          </div>
          <input 
            type="range" 
            min="-50" max="50" step="1"
            value={volShock}
            onChange={(e) => setVolShock(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-rose-500"
          />
          <p className="text-xs text-slate-400 mt-2">Simulate an external supply chain shock.</p>
        </div>

        {/* Control: Demand Elasticity */}
        <div className="pt-4 border-t border-slate-100">
          <div className="flex justify-between items-center mb-2">
            <label className="text-sm font-semibold text-slate-700">Demand Elasticity</label>
            <span className="text-sm font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
              {elasticity}
            </span>
          </div>
          <input 
            type="range" 
            min="-2.0" max="0" step="0.1"
            value={elasticity}
            onChange={(e) => setElasticity(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-600"
          />
          <p className="text-xs text-slate-400 mt-2 leading-relaxed">
            Market sensitivity to tax changes. <br/>(e.g., -0.5 = 5% volume drop per 10% tax hike)
          </p>
        </div>

      </div>

      <div className="mt-10 flex gap-3">
        <button 
          onClick={handleSimulate}
          disabled={isSimulating}
          className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-xl shadow-md hover:shadow-lg transition-all active:scale-95 disabled:opacity-50"
        >
          {isSimulating ? 'Simulating...' : 'Run Simulation'}
        </button>
        <button 
          onClick={handleReset}
          className="px-6 bg-slate-100 hover:bg-slate-200 text-slate-600 font-semibold py-3 rounded-xl transition-all active:scale-95"
        >
          Reset
        </button>
      </div>

    </div>
  );
};

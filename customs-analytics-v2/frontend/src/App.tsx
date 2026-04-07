import { useState, useEffect } from 'react';
import { Network } from 'lucide-react';
import { RevenueChart } from './components/RevenueChart';
import { ScenarioPanel } from './components/ScenarioPanel';
import { ForecastCompare } from './components/ForecastCompare';
import { getBaselineForecast, simulateScenario } from './api/client';
import type { ForecastResult, ScenarioParams } from './api/client';

function App() {
  const [baselineData, setBaselineData] = useState<ForecastResult | null>(null);
  const [activeData, setActiveData] = useState<ForecastResult | null>(null);
  
  const [isInitializing, setIsInitializing] = useState(true);
  const [isSimulating, setIsSimulating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initial load
  useEffect(() => {
    const fetchBaseline = async () => {
      try {
        const data = await getBaselineForecast('sarima', 6);
        setBaselineData(data);
        setActiveData(data);
        setError(null);
      } catch (err) {
        setError('Failed to connect to the Analytics Engine. Ensure the backend database and API are running.');
        console.error(err);
      } finally {
        setIsInitializing(false);
      }
    };
    fetchBaseline();
  }, []);

  const handleSimulate = async (params: ScenarioParams) => {
    setIsSimulating(true);
    try {
      const data = await simulateScenario(params, 'sarima', 6);
      setActiveData(data);
      setError(null);
    } catch (err) {
      setError('Simulation failed. Please verify your connection.');
      console.error(err);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setActiveData(baselineData);
  };

  return (
    <div className="min-h-screen w-full font-sans text-slate-800 p-8 flex flex-col items-center">
      
      {/* Header */}
      <header className="w-full max-w-7xl mb-8 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-2.5 rounded-xl shadow-md">
            <Network className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900 leading-tight">
              Customs Analytics
            </h1>
            <p className="text-sm text-slate-500 font-medium">Deterministic Scenario Engine • V2</p>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="w-full max-w-7xl grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Chart */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {error && (
            <div className="bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-xl shadow-sm text-sm font-medium">
              ⚠️ {error}
            </div>
          )}
          
          <RevenueChart 
            data={activeData} 
            baseData={activeData !== baselineData ? baselineData : null} 
            isLoading={isInitializing} 
          />
          
          <ForecastCompare 
              baselineData={baselineData} 
              activeData={activeData} 
          />
        </div>

        {/* Right Column: Scenario Controls */}
        <div className="lg:col-span-4">
          <ScenarioPanel 
            onSimulate={handleSimulate} 
            onReset={handleReset} 
            isSimulating={isSimulating} 
          />
        </div>

      </main>
    </div>
  );
}

export default App;

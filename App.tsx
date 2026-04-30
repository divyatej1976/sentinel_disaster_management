import React, { useState } from 'react';
import { Header } from './components/Header';
import { ControlsPanel } from './components/ControlsPanel';
import { PredictionPanel } from './components/PredictionPanel';
import { AnalysisPanel } from './components/AnalysisPanel';
import { TabNavigation } from './components/TabNavigation';
import { ComparisonPanel } from './components/ComparisonPanel';

import { AlertCircle, History, RefreshCcw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { Evidence, Prediction } from './types';
import { getOutbreakPrediction } from './services/geminiService';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'prediction' | 'analysis' | 'comparison'>('prediction');
  const [loading, setLoading] = useState(false);
  const [evidence, setEvidence] = useState<Evidence>({
    Weather: 1,
    PopulationDensity: 1,
    Sanitation: 2,
    RecentCases: 0,
  });
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [baseline, setBaseline] = useState<{ evidence: Evidence; prediction: Prediction } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getOutbreakPrediction(evidence, 'gemini-2.0-flash');
      setPrediction(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const saveAsBaseline = () => {
    if (prediction) {
      setBaseline({ evidence: { ...evidence }, prediction: { ...prediction } });
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

          {/* Sidebar */}
          <aside className="lg:col-span-4 xl:col-span-3 space-y-4">
            <div className="panel p-6">
              <div className="flex items-center gap-2 mb-6">
                <div className="w-1.5 h-4 bg-blue-600 rounded-full" />
                <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Simulation Controls</h2>
              </div>
              <ControlsPanel
                evidence={evidence}
                onChange={setEvidence}
                onPredict={handlePredict}
                loading={loading}
              />
            </div>

            <AnimatePresence>
              {prediction && (
                <motion.button
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -8 }}
                  onClick={saveAsBaseline}
                  className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-white border border-slate-200 rounded-xl text-sm font-medium text-slate-600 hover:bg-slate-50 hover:border-slate-300 transition-all shadow-sm"
                >
                  <History className="w-4 h-4 text-blue-500" />
                  Set as Comparison Baseline
                </motion.button>
              )}
            </AnimatePresence>

            {/* Info sidebar card */}
            <div className="panel p-5 bg-gradient-to-br from-blue-950 to-slate-900 border-none text-white space-y-3">
              <p className="text-[10px] font-bold uppercase tracking-widest text-blue-400">About the Engine</p>
              <p className="text-xs text-slate-300 leading-relaxed">
                Three AI expert agents - Epidemiologist, Environmental Scientist, and Public Health Strategist - each independently assess risk. The final score is a weighted consensus with an explainable disagreement index.
              </p>
              <div className="grid grid-cols-3 gap-2 pt-1">
                {['Epidemiology', 'Environment', 'Response'].map((role) => (
                  <div key={role} className="bg-white/5 border border-white/10 rounded-lg p-2 text-center">
                    <p className="text-[9px] font-bold text-blue-300 leading-tight">{role}</p>
                  </div>
                ))}
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <div className="lg:col-span-8 xl:col-span-9 space-y-5">
            {/* Tab bar + status */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <TabNavigation
                activeTab={activeTab}
                onTabChange={setActiveTab}
                hasBaseline={!!baseline}
              />
              <AnimatePresence>
                {loading && (
                  <motion.div
                    initial={{ opacity: 0, x: 8 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 8 }}
                    className="flex items-center gap-2 text-blue-600 text-sm font-medium bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-100"
                  >
                    <RefreshCcw className="w-3.5 h-3.5 animate-spin" />
                    Processing Neural Consensus...
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Error banner */}
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="bg-red-50 border border-red-100 rounded-xl p-4 flex gap-3 items-start text-red-700"
                >
                  <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                  <div>
                    <p className="font-bold">System Error</p>
                    <p className="text-sm opacity-90">{error}</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Panel switcher */}
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.25 }}
              >
                {activeTab === 'prediction' && (
                  <PredictionPanel prediction={prediction} loading={loading} />
                )}
                {activeTab === 'analysis' && (
                  <AnalysisPanel prediction={prediction} />
                )}
                {activeTab === 'comparison' && baseline && prediction && (
                  <ComparisonPanel baseline={baseline} current={{ evidence, prediction }} />
                )}
              </motion.div>
            </AnimatePresence>


          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-slate-400">
          <p>Copyright 2026 Epidemic.Intel - Epidemiological Decision Support System</p>
          <div className="flex items-center gap-5">
            <span className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              Consensus Engine v2.0
            </span>
            <span>Gemini 2.0 Flash Integration</span>
            <span className="px-2 py-0.5 bg-slate-100 rounded text-slate-500 font-mono">Multi-Agent</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

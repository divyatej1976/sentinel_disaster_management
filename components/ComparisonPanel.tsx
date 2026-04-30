import React from 'react';
import { ArrowRight, TrendingDown, TrendingUp, Minus, GitCompare, CheckCircle2, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import type { Evidence, Prediction } from '../types';

interface Props {
  baseline: { evidence: Evidence; prediction: Prediction };
  current: { evidence: Evidence; prediction: Prediction };
}

const LABELS = {
  Weather: ['Clear', 'Mild', 'Humid', 'Adverse'],
  PopulationDensity: ['Low', 'Medium', 'High', 'Very High'],
  Sanitation: ['Poor', 'Moderate', 'Good'],
  RecentCases: ['< 100', '101–1k', '1k–5k', '> 5k'],
};

export const ComparisonPanel: React.FC<Props> = ({ baseline, current }) => {
  const probDiff = current.prediction.final_probability - baseline.prediction.final_probability;
  const isBetter = probDiff < 0;
  const isNeutral = probDiff === 0;

  const baselinePct = Math.round(baseline.prediction.final_probability * 100);
  const currentPct = Math.round(current.prediction.final_probability * 100);
  const diffPct = Math.round(Math.abs(probDiff) * 100);

  const metrics = [
    {
      label: 'Risk Probability',
      baseline: `${baselinePct}%`,
      current: `${currentPct}%`,
      improved: isBetter,
      neutral: isNeutral,
    },
    {
      label: 'Disagreement Index',
      baseline: `${(baseline.prediction.disagreement_index * 100).toFixed(0)}%`,
      current: `${(current.prediction.disagreement_index * 100).toFixed(0)}%`,
      improved: current.prediction.disagreement_index < baseline.prediction.disagreement_index,
      neutral: current.prediction.disagreement_index === baseline.prediction.disagreement_index,
    },
    {
      label: 'Confidence Score',
      baseline: `${(baseline.prediction.confidence_score * 100).toFixed(0)}%`,
      current: `${(current.prediction.confidence_score * 100).toFixed(0)}%`,
      improved: current.prediction.confidence_score > baseline.prediction.confidence_score,
      neutral: current.prediction.confidence_score === baseline.prediction.confidence_score,
    },
  ];

  const paramRows = [
    { label: 'Weather', base: LABELS.Weather[baseline.evidence.Weather], curr: LABELS.Weather[current.evidence.Weather], changed: baseline.evidence.Weather !== current.evidence.Weather },
    { label: 'Density', base: LABELS.PopulationDensity[baseline.evidence.PopulationDensity], curr: LABELS.PopulationDensity[current.evidence.PopulationDensity], changed: baseline.evidence.PopulationDensity !== current.evidence.PopulationDensity },
    { label: 'Sanitation', base: LABELS.Sanitation[baseline.evidence.Sanitation], curr: LABELS.Sanitation[current.evidence.Sanitation], changed: baseline.evidence.Sanitation !== current.evidence.Sanitation },
    { label: 'Case Load', base: LABELS.RecentCases[baseline.evidence.RecentCases], curr: LABELS.RecentCases[current.evidence.RecentCases], changed: baseline.evidence.RecentCases !== current.evidence.RecentCases },
  ];

  const changedCount = paramRows.filter(r => r.changed).length;

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header card */}
      <div className="panel p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-slate-500 mb-2">
              <GitCompare className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-widest">Scenario Delta Analysis</span>
            </div>
            <h3 className="text-xl font-bold text-slate-900">
              {isBetter ? '✓ Intervention effective' : isNeutral ? '— No change detected' : '⚠ Risk increased'}
            </h3>
            <p className="text-sm text-slate-500 max-w-md">
              {changedCount === 0
                ? 'No parameters were changed from the baseline.'
                : `${changedCount} parameter${changedCount > 1 ? 's' : ''} changed. Comparing consensus outputs to quantify intervention impact.`}
            </p>
          </div>

          {/* Big delta display */}
          <div className="flex items-center gap-5 px-6 py-4 bg-slate-50 border border-slate-200 rounded-2xl shrink-0">
            <div className="text-center">
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Baseline</p>
              <p className="text-3xl font-bold text-slate-400 tabular-nums">{baselinePct}%</p>
            </div>
            <ArrowRight className="w-5 h-5 text-slate-300 shrink-0" />
            <div className="text-center">
              <p className="text-[10px] font-bold text-blue-600 uppercase tracking-widest mb-1">Current</p>
              <p className="text-3xl font-bold text-slate-900 tabular-nums">{currentPct}%</p>
            </div>
            <div className={`ml-2 px-4 py-2 rounded-xl flex items-center gap-2 font-bold text-lg ${
              isBetter ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' :
              isNeutral ? 'bg-slate-100 text-slate-500' :
              'bg-red-50 text-red-600 border border-red-100'
            }`}>
              {isBetter ? <TrendingDown className="w-5 h-5" /> : isNeutral ? <Minus className="w-5 h-5" /> : <TrendingUp className="w-5 h-5" />}
              {isNeutral ? '0%' : `${isBetter ? '-' : '+'}${diffPct}%`}
            </div>
          </div>
        </div>
      </div>

      {/* Metric comparison cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {metrics.map((metric, i) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="panel p-5"
          >
            <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-3">{metric.label}</p>
            <div className="flex items-end justify-between">
              <div>
                <p className="text-xs text-slate-400 line-through mb-1">{metric.baseline}</p>
                <p className="text-2xl font-bold text-slate-900 tabular-nums">{metric.current}</p>
              </div>
              <div className={`flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-lg ${
                metric.neutral ? 'bg-slate-100 text-slate-500' :
                metric.improved ? 'bg-emerald-50 text-emerald-600' :
                'bg-red-50 text-red-600'
              }`}>
                {metric.neutral ? <Minus className="w-3 h-3" /> : metric.improved ? <CheckCircle2 className="w-3 h-3" /> : <AlertTriangle className="w-3 h-3" />}
                {metric.neutral ? 'Unchanged' : metric.improved ? 'Improved' : 'Worse'}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Parameter diff + consensus shift */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="panel p-6">
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-5">Parameter Changes</h4>
          <div className="space-y-3">
            {paramRows.map((row, i) => (
              <motion.div
                key={row.label}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 + i * 0.07 }}
                className={`flex items-center justify-between py-2.5 px-3 rounded-lg ${row.changed ? 'bg-blue-50 border border-blue-100' : 'border border-transparent'}`}
              >
                <span className={`text-xs font-bold uppercase ${row.changed ? 'text-blue-600' : 'text-slate-400'}`}>{row.label}</span>
                <div className="flex items-center gap-2.5">
                  <span className="text-xs text-slate-400 line-through">{row.base}</span>
                  <ArrowRight className="w-3 h-3 text-slate-300" />
                  <span className={`text-xs font-bold ${row.changed ? 'text-blue-700' : 'text-slate-600'}`}>{row.curr}</span>
                  {row.changed && <span className="text-[9px] font-black text-blue-400 bg-blue-100 px-1.5 py-0.5 rounded">CHANGED</span>}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="panel p-6 space-y-5">
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Consensus Integrity Shift</h4>
          
          {/* Baseline consensus bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-slate-400">
              <span>Baseline Consensus</span>
              <span>{(100 - baseline.prediction.disagreement_index * 100).toFixed(0)}%</span>
            </div>
            <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-slate-400 rounded-full" style={{ width: `${(1 - baseline.prediction.disagreement_index) * 100}%` }} />
            </div>
          </div>

          {/* Current consensus bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-slate-400">
              <span>Current Consensus</span>
              <span className={current.prediction.disagreement_index < baseline.prediction.disagreement_index ? 'text-emerald-600' : 'text-slate-400'}>
                {(100 - current.prediction.disagreement_index * 100).toFixed(0)}%
              </span>
            </div>
            <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-blue-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${(1 - current.prediction.disagreement_index) * 100}%` }}
                transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
              />
            </div>
          </div>

          <blockquote className="text-xs text-slate-500 italic leading-relaxed border-l-2 border-blue-200 pl-3">
            "{current.prediction.confidence_explanation}"
          </blockquote>
        </div>
      </div>
    </motion.div>
  );
};

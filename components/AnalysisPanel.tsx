import React from 'react';
import { Quote, UserCheck, Scale, AlertCircle, CheckCircle2, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';
import type { Prediction } from '../types';

interface Props {
  prediction: Prediction | null;
}

const agentColors = [
  { ring: 'ring-blue-200', bg: 'bg-blue-50', text: 'text-blue-600', bar: 'bg-blue-500' },
  { ring: 'ring-violet-200', bg: 'bg-violet-50', text: 'text-violet-600', bar: 'bg-violet-500' },
  { ring: 'ring-teal-200', bg: 'bg-teal-50', text: 'text-teal-600', bar: 'bg-teal-500' },
];

export const AnalysisPanel: React.FC<Props> = ({ prediction }) => {
  if (!prediction) return null;

  const agreementScore = Math.round((1 - prediction.disagreement_index) * 100);
  const topFactor = Object.entries(prediction.critical_factors)
    .sort((a, b) => b[1] - a[1])[0];

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Interpretability header */}
      <div className="panel p-6 border-l-4 border-l-blue-600">
        <div className="flex flex-col md:flex-row justify-between gap-6">
          <div className="flex-1 space-y-3">
            <div className="flex items-center gap-2 text-blue-600">
              <Scale className="w-5 h-5" />
              <h3 className="font-bold text-base">Model Interpretability Report</h3>
            </div>
            <p className="text-slate-600 leading-relaxed italic text-sm">
              "{prediction.confidence_explanation}"
            </p>
            <p className="text-xs text-slate-400">{prediction.architecture_note}</p>
          </div>

          {/* Consensus stat block */}
          <div className="flex flex-row md:flex-col gap-4 md:gap-3 md:w-52 shrink-0">
            <div className="flex-1 md:flex-none bg-slate-50 rounded-xl p-4 space-y-2">
              <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Agent Agreement</p>
              <div className="flex items-end gap-2">
                <span className="text-2xl font-bold text-slate-900 tabular-nums">{agreementScore}%</span>
                <TrendingUp className="w-4 h-4 text-blue-500 mb-1" />
              </div>
              <div className="h-1.5 w-full bg-slate-200 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-blue-500 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${agreementScore}%` }}
                  transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
                />
              </div>
            </div>
            <div className="flex-1 md:flex-none bg-slate-50 rounded-xl p-4 space-y-1">
              <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Top Driver</p>
              <p className="text-sm font-bold text-slate-900 capitalize">{topFactor[0]}</p>
              <p className="text-xs text-blue-600 font-bold">{topFactor[1].toFixed(0)}% weight</p>
            </div>
          </div>
        </div>
      </div>

      {/* Expert opinion cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {prediction.expert_opinions.map((opinion, idx) => {
          const color = agentColors[idx % agentColors.length];
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + idx * 0.1 }}
              className={`panel p-5 flex flex-col ring-1 ${color.ring}`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center ring-1 ${color.bg} ${color.ring}`}>
                    <UserCheck className={`w-4 h-4 ${color.text}`} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">{opinion.expert}</p>
                    <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">{opinion.role}</p>
                  </div>
                </div>
                <span className={`rounded-lg px-2.5 py-1 text-xs font-black ${color.bg} ${color.text}`}>
                  {opinion.risk_rating}/10
                </span>
              </div>

              {/* Weight bar */}
              <div className="mb-3">
                <div className="flex justify-between text-[10px] font-bold text-slate-400 mb-1.5">
                  <span>Agent Weight</span>
                  <span>{(opinion.weight * 100).toFixed(0)}%</span>
                </div>
                <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full rounded-full ${color.bar}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${opinion.weight * 100}%` }}
                    transition={{ delay: 0.3 + idx * 0.1, duration: 0.8, ease: 'easeOut' }}
                  />
                </div>
              </div>

              <div className="relative flex-1 mb-4">
                <Quote className={`w-5 h-5 absolute -top-1 -left-1 opacity-20 ${color.text}`} />
                <p className="text-xs text-slate-500 leading-relaxed pl-3">{opinion.opinion}</p>
              </div>

              <div className={`rounded-lg p-3 ${color.bg}`}>
                <p className={`text-[10px] font-bold uppercase tracking-widest mb-1 ${color.text}`}>
                  Recommendation
                </p>
                <p className="text-xs leading-relaxed text-slate-700">{opinion.recommendation}</p>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Risk drivers + mitigation 2-col */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="panel p-6">
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-5">Ranked Risk Drivers</h4>
          <div className="space-y-3">
            {prediction.top_risk_drivers.map((driver, index) => (
              <motion.div
                key={driver}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 + index * 0.08 }}
                className="flex items-center gap-3"
              >
                <span className={`flex h-7 w-7 items-center justify-center rounded-lg text-xs font-black shrink-0 ${
                  index === 0 ? 'bg-red-50 text-red-500' : index === 1 ? 'bg-amber-50 text-amber-500' : 'bg-slate-100 text-slate-500'
                }`}>
                  {index + 1}
                </span>
                <span className="text-sm font-semibold text-slate-700">{driver}</span>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="panel p-6">
          <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-5">Mitigation Playbook</h4>
          <div className="space-y-3">
            {prediction.mitigation_strategies.map((strategy, i) => (
              <motion.div
                key={strategy}
                initial={{ opacity: 0, x: 8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 + i * 0.08 }}
                className="flex gap-3"
              >
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
                <p className="text-sm leading-relaxed text-slate-600">{strategy}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Systemic conclusion */}
      <div className="panel p-6 bg-slate-900 border-none">
        <div className="flex items-center gap-3 mb-4 text-amber-400">
          <AlertCircle className="w-5 h-5" />
          <h4 className="font-bold text-sm uppercase tracking-widest">Systemic Conclusion</h4>
        </div>
        <p className="text-sm text-slate-300 leading-relaxed">
          The multi-agent consensus concludes a{' '}
          <span className="font-bold text-white underline decoration-blue-500 underline-offset-4">
            {prediction.risk_level.toLowerCase()} outbreak threat
          </span>
          . The dominant uncertainty driver is the{' '}
          <span className="font-bold text-blue-400">{topFactor[0]}</span> factor, contributing{' '}
          {topFactor[1].toFixed(0)}% to the final probability score. Expert agreement stands at{' '}
          <span className="font-bold text-emerald-400">{agreementScore}%</span>.
        </p>
      </div>
    </motion.div>
  );
};

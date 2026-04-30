import React from 'react';
import {
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar, BarChart, Bar, XAxis, YAxis, Tooltip, Cell,
} from 'recharts';
import { Info, AlertTriangle, CheckCircle, ShieldAlert, Database, Brain } from 'lucide-react';
import { motion } from 'framer-motion';
import { TiltCard } from '@/components/ui/tilt-card';
import type { Prediction } from '../types';

interface Props {
  prediction: Prediction | null;
  loading: boolean;
}

const RISK_COLORS: Record<string, string> = {
  High: '#ef4444',
  Medium: '#f59e0b',
  Low: '#10b981',
};

export const PredictionPanel: React.FC<Props> = ({ prediction, loading }) => {
  if (loading) return <LoadingState />;
  if (!prediction) return <EmptyState />;

  const chartData = [
    { subject: 'Weather', A: prediction.critical_factors.weather },
    { subject: 'Density', A: prediction.critical_factors.density },
    { subject: 'Sanitation', A: prediction.critical_factors.sanitation },
    { subject: 'Cases', A: prediction.critical_factors.cases },
  ];

  const riskMeta = {
    Low: { color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-100', ringColor: '#10b981', icon: <CheckCircle className="w-4 h-4" /> },
    Medium: { color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-100', ringColor: '#f59e0b', icon: <AlertTriangle className="w-4 h-4" /> },
    High: { color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-100', ringColor: '#ef4444', icon: <ShieldAlert className="w-4 h-4" /> },
  }[prediction.risk_level] ?? { color: 'text-slate-600', bg: 'bg-slate-50', border: 'border-slate-100', ringColor: '#94a3b8', icon: <Info className="w-4 h-4" /> };

  const ringColor = RISK_COLORS[prediction.risk_level] ?? '#94a3b8';
  const dashOffset = 440 * (1 - prediction.final_probability);

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Row 1: Risk Score + Radar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* TiltCard risk score */}
        <TiltCard
          className="panel p-8 flex flex-col items-center justify-center text-center"
          spotlight
          tiltLimit={12}
        >
          <div className="relative w-36 h-36 mb-5">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 160 160">
              <circle cx="80" cy="80" r="70" stroke="#f1f5f9" strokeWidth="10" fill="none" />
              <motion.circle
                cx="80" cy="80" r="70"
                stroke={ringColor}
                strokeWidth="10"
                strokeDasharray={440}
                initial={{ strokeDashoffset: 440 }}
                animate={{ strokeDashoffset: dashOffset }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
                strokeLinecap="round"
                fill="none"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <motion.span
                className="text-4xl font-bold text-slate-900 tabular-nums"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                {(prediction.final_probability * 100).toFixed(0)}%
              </motion.span>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Outbreak Risk</span>
            </div>
          </div>
          <div className={`flex items-center gap-2 px-4 py-1.5 rounded-full border ${riskMeta.bg} ${riskMeta.border} ${riskMeta.color} text-xs font-bold`}>
            {riskMeta.icon}
            {prediction.risk_level.toUpperCase()} THREAT LEVEL
          </div>
        </TiltCard>

        {/* Factor Radar */}
        <div className="panel p-6 col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider">Factor Contribution Analysis</h3>
            <div className="flex items-center gap-1.5 text-xs text-slate-400">
              <Info className="w-3.5 h-3.5" />
              <span>Relative Weighted Impact</span>
            </div>
          </div>
          <div className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11, fontWeight: 600 }} />
                <Radar name="Impact" dataKey="A" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.15} />
                <Tooltip
                  contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)', fontSize: '12px' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 2: Horizontal Bar Chart */}
      <div className="panel p-6">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between mb-6">
          <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider">Detailed Factor Breakdown</h3>
          {prediction.demo_mode && (
            <span className="w-fit rounded-full bg-amber-50 border border-amber-100 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-amber-700">
              Demo fallback mode
            </span>
          )}
        </div>
        <div className="h-[180px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ left: 0, right: 16 }}>
              <XAxis type="number" hide />
              <YAxis
                dataKey="subject"
                type="category"
                tick={{ fill: '#64748b', fontSize: 11, fontWeight: 600 }}
                width={76}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{ borderRadius: '10px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                cursor={{ fill: '#f8fafc' }}
              />
              <Bar dataKey="A" radius={[0, 6, 6, 0]} barSize={20}>
                {chartData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#3b82f6' : '#818cf8'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Row 3: Expert Agent Cards with stagger */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {prediction.expert_opinions.map((opinion, i) => (
          <motion.div
            key={opinion.agent_id}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 + i * 0.1 }}
            className="panel p-5 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 bg-blue-50 border border-blue-100 rounded-lg flex items-center justify-center">
                  <Brain className="w-4 h-4 text-blue-500" />
                </div>
                <div>
                  <p className="text-sm font-bold text-slate-900">{opinion.role}</p>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                    Weight: {(opinion.weight * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
              <span className={`rounded-lg px-2.5 py-1 text-xs font-black ${
                opinion.risk_rating >= 7 ? 'bg-red-50 text-red-600' :
                opinion.risk_rating >= 4 ? 'bg-amber-50 text-amber-600' :
                'bg-emerald-50 text-emerald-600'
              }`}>
                {opinion.risk_rating.toFixed(1)}/10
              </span>
            </div>
            {/* Weight bar */}
            <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden mb-4">
              <motion.div
                className="h-full bg-blue-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${opinion.weight * 100}%` }}
                transition={{ delay: 0.3 + i * 0.1, duration: 0.8, ease: 'easeOut' }}
              />
            </div>
            <div className="flex flex-wrap gap-1.5">
              {opinion.primary_factors.map((factor) => (
                <span key={factor} className="inline-flex rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-500">
                  {factor}
                </span>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

const LoadingState = () => (
  <motion.div
    className="panel p-20 flex flex-col items-center justify-center space-y-5"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
  >
    <div className="relative w-14 h-14">
      <div className="absolute inset-0 rounded-full border-4 border-blue-100" />
      <div className="absolute inset-0 rounded-full border-4 border-t-blue-600 animate-spin" />
      <Brain className="absolute inset-0 m-auto w-5 h-5 text-blue-400" />
    </div>
    <div className="text-center space-y-1">
      <p className="text-slate-900 font-bold">Synthesizing Expert Consensus</p>
      <p className="text-slate-400 text-sm">Querying 3 agent personas for risk validation...</p>
    </div>
    <div className="flex gap-1.5">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-blue-400"
          animate={{ y: [0, -6, 0] }}
          transition={{ repeat: Infinity, duration: 0.9, delay: i * 0.2 }}
        />
      ))}
    </div>
  </motion.div>
);

const EmptyState = () => (
  <motion.div
    className="panel p-20 flex flex-col items-center justify-center text-center space-y-6"
    initial={{ opacity: 0, scale: 0.97 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.4 }}
  >
    <div className="w-16 h-16 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center">
      <Database className="w-7 h-7 text-slate-300" />
    </div>
    <div className="space-y-2">
      <h3 className="text-lg font-bold text-slate-900">System Awaiting Input</h3>
      <p className="text-slate-500 text-sm max-w-xs mx-auto leading-relaxed">
        Configure environmental telemetry in the sidebar and run a consensus simulation to generate risk scores.
      </p>
    </div>
  </motion.div>
);

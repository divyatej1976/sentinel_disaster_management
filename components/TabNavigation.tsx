import React from 'react';
import { LayoutDashboard, FileText, GitCompare } from 'lucide-react';
import { motion } from 'framer-motion';

interface Props {
  activeTab: 'prediction' | 'analysis' | 'comparison';
  onTabChange: (tab: 'prediction' | 'analysis' | 'comparison') => void;
  hasBaseline: boolean;
}

type Tab = {
  id: 'prediction' | 'analysis' | 'comparison';
  label: string;
  icon: React.ReactNode;
};

export const TabNavigation: React.FC<Props> = ({ activeTab, onTabChange, hasBaseline }) => {
  const tabs: Tab[] = [
    { id: 'prediction', label: 'Risk Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { id: 'analysis', label: 'Expert Analysis', icon: <FileText className="w-4 h-4" /> },
    ...(hasBaseline ? [{ id: 'comparison' as const, label: 'Scenario Comparison', icon: <GitCompare className="w-4 h-4" /> }] : []),
  ];

  return (
    <div className="relative flex bg-white border border-slate-200 p-1 rounded-xl shadow-sm gap-1">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`relative flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors z-10 ${
            activeTab === tab.id
              ? 'text-blue-600'
              : 'text-slate-500 hover:text-slate-800'
          }`}
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="active-tab-bg"
              className="absolute inset-0 bg-blue-50 rounded-lg border border-blue-100"
              transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            />
          )}
          <span className="relative z-10 flex items-center gap-2">
            {tab.icon}
            {tab.label}
          </span>
        </button>
      ))}
    </div>
  );
};

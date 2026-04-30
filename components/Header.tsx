import React, { useState, useEffect } from 'react';
import { Shield, Activity, Globe, Wifi } from 'lucide-react';

export const Header: React.FC = () => {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="bg-slate-950 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex items-center gap-4">
          <div className="relative w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white shadow-lg shadow-blue-900/50">
            <Globe className="w-5 h-5" />
            {/* Live pulse ring */}
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-white leading-none tracking-tight">EPIDEMIC.INTEL</h1>
            <p className="text-[10px] font-bold text-blue-400 uppercase tracking-widest mt-0.5">Decision Support System</p>
          </div>
        </div>

        {/* Status Bar */}
        <div className="hidden md:flex items-center gap-5">
          {/* Live clock */}
          <div className="flex items-center gap-2">
            <Wifi className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-xs font-mono text-slate-300 tabular-nums">
              {time.toLocaleTimeString('en-US', { hour12: false })} UTC+5:30
            </span>
          </div>

          <div className="h-5 w-px bg-slate-700" />

          <div className="flex items-center gap-2">
            <Activity className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-xs font-medium text-slate-400">Gemini 2.0 Flash</span>
          </div>

          <div className="h-5 w-px bg-slate-700" />

          {/* Agent Secure badge */}
          <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-950 border border-emerald-800 rounded-full">
            <Shield className="w-3 h-3 text-emerald-400" />
            <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Multi-Agent Active</span>
          </div>
        </div>
      </div>
    </header>
  );
};

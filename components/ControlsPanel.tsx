import React, { useState } from 'react';
import { Cloud, Users, Droplets, Activity, ChevronRight, Zap, MapPin, Thermometer, Loader2, Wifi } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { Evidence } from '../types';
import { fetchLiveWeather, type WeatherData } from '../services/weatherService';

interface Props {
  evidence: Evidence;
  onChange: (evidence: Evidence) => void;
  onPredict: () => void;
  loading: boolean;
}

export const ControlsPanel: React.FC<Props> = ({ evidence, onChange, onPredict, loading }) => {
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherInfo, setWeatherInfo] = useState<WeatherData | null>(null);
  const [weatherError, setWeatherError] = useState<string | null>(null);

  const updateEvidence = (key: keyof Evidence, value: number) => {
    onChange({ ...evidence, [key]: value });
  };

  const handleFetchWeather = async () => {
    setWeatherLoading(true);
    setWeatherError(null);
    try {
      const data = await fetchLiveWeather();
      setWeatherInfo(data);
      // Auto-set the Weather control to live data
      onChange({ ...evidence, Weather: data.weatherLevel });
    } catch (err) {
      setWeatherError(err instanceof Error ? err.message : 'Failed to fetch weather.');
    } finally {
      setWeatherLoading(false);
    }
  };

  const controls = [
    {
      key: 'Weather' as keyof Evidence,
      icon: <Cloud className="w-4 h-4" />,
      label: 'Weather Pattern',
      options: ['Clear', 'Mild', 'Humid', 'Adverse'],
      color: 'text-sky-500',
      isLive: !!weatherInfo,
    },
    {
      key: 'PopulationDensity' as keyof Evidence,
      icon: <Users className="w-4 h-4" />,
      label: 'Population Density',
      options: ['Low', 'Medium', 'High', 'Very High'],
      color: 'text-violet-500',
      isLive: false,
    },
    {
      key: 'Sanitation' as keyof Evidence,
      icon: <Droplets className="w-4 h-4" />,
      label: 'Sanitation Level',
      options: ['Poor', 'Moderate', 'Good'],
      color: 'text-teal-500',
      isLive: false,
    },
    {
      key: 'RecentCases' as keyof Evidence,
      icon: <Activity className="w-4 h-4" />,
      label: 'Case Velocity',
      options: ['< 100', '101–1k', '1k–5k', '> 5k'],
      color: 'text-rose-500',
      isLive: false,
    },
  ];

  // Compute a live "threat indicator" from current values
  const threatScore = Math.round(
    ((evidence.Weather + evidence.PopulationDensity + (2 - evidence.Sanitation) + evidence.RecentCases) / 10) * 100
  );

  return (
    <div className="space-y-6">

      {/* Live Weather Button */}
      <div className="space-y-2">
        <button
          onClick={handleFetchWeather}
          disabled={weatherLoading}
          className={`w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl border text-xs font-bold uppercase tracking-wider transition-all ${
            weatherInfo
              ? 'bg-sky-50 border-sky-200 text-sky-700 hover:bg-sky-100'
              : 'bg-white border-slate-200 text-slate-600 hover:border-blue-300 hover:text-blue-600'
          }`}
        >
          {weatherLoading ? (
            <><Loader2 className="w-3.5 h-3.5 animate-spin" /> Fetching location...</>
          ) : weatherInfo ? (
            <><Wifi className="w-3.5 h-3.5" /> Live: {weatherInfo.locationName} · {weatherInfo.temperature}°C</>
          ) : (
            <><MapPin className="w-3.5 h-3.5" /> Auto-fill from My Location</>
          )}
        </button>

        {/* Live weather detail chip */}
        <AnimatePresence>
          {weatherInfo && !weatherLoading && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden"
            >
              <div className="grid grid-cols-3 gap-1.5 pt-1">
                <div className="bg-sky-50 rounded-lg p-2 text-center">
                  <Thermometer className="w-3 h-3 text-sky-500 mx-auto mb-0.5" />
                  <p className="text-[10px] font-bold text-sky-700">{weatherInfo.temperature}°C</p>
                  <p className="text-[9px] text-sky-400">Temp</p>
                </div>
                <div className="bg-sky-50 rounded-lg p-2 text-center">
                  <Droplets className="w-3 h-3 text-sky-500 mx-auto mb-0.5" />
                  <p className="text-[10px] font-bold text-sky-700">{weatherInfo.humidity}%</p>
                  <p className="text-[9px] text-sky-400">Humidity</p>
                </div>
                <div className="bg-sky-50 rounded-lg p-2 text-center">
                  <Cloud className="w-3 h-3 text-sky-500 mx-auto mb-0.5" />
                  <p className="text-[10px] font-bold text-sky-700">{weatherInfo.precipitation}mm</p>
                  <p className="text-[9px] text-sky-400">Rain</p>
                </div>
                <div className="bg-sky-50 rounded-lg p-2 text-center">
                  <Cloud className="w-3 h-3 text-sky-500 mx-auto mb-0.5" />
                  <p className="text-[10px] font-bold text-sky-700">{weatherInfo.cloudCover}%</p>
                  <p className="text-[9px] text-sky-400">Cloud</p>
                </div>
                <div className="bg-sky-50 rounded-lg p-2 text-center">
                  <Wifi className="w-3 h-3 text-sky-500 mx-auto mb-0.5" />
                  <p className="text-[10px] font-bold text-sky-700">{(weatherInfo.visibility / 1000).toFixed(1)}km</p>
                  <p className="text-[9px] text-sky-400">Visibility</p>
                </div>
                <div className="bg-sky-50 rounded-lg p-2 text-center">
                  <Activity className="w-3 h-3 text-sky-500 mx-auto mb-0.5" />
                  <p className="text-[10px] font-bold text-sky-700">{weatherInfo.windSpeed}km/h</p>
                  <p className="text-[9px] text-sky-400">Wind</p>
                </div>
              </div>
              <p className="text-[10px] text-sky-600 text-center mt-1.5 font-medium">
                Weather set to <strong>{weatherInfo.weatherLabel}</strong> from real data
              </p>
            </motion.div>
          )}
          {weatherError && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-[10px] text-red-500 text-center"
            >
              {weatherError}
            </motion.p>
          )}
        </AnimatePresence>
      </div>

      {/* Threat bar */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-widest">
          <span className="text-slate-400">Live Risk Estimate</span>
          <span className={`font-mono ${threatScore > 65 ? 'text-red-500' : threatScore > 35 ? 'text-amber-500' : 'text-emerald-500'}`}>
            {threatScore}%
          </span>
        </div>
        <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
          <motion.div
            className={`h-full rounded-full ${threatScore > 65 ? 'bg-red-500' : threatScore > 35 ? 'bg-amber-500' : 'bg-emerald-500'}`}
            animate={{ width: `${Math.min(threatScore, 100)}%` }}
            transition={{ type: 'spring', stiffness: 120, damping: 20 }}
          />
        </div>
      </div>

      {/* Control items */}
      <div className="space-y-5">
        {controls.map((ctrl, i) => (
          <motion.div
            key={ctrl.key}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="space-y-2"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className={ctrl.color}>{ctrl.icon}</span>
                <span className="text-xs font-bold text-slate-600 uppercase tracking-wide">{ctrl.label}</span>
              </div>
              {ctrl.isLive && (
                <span className="text-[9px] font-black uppercase tracking-wider text-sky-600 bg-sky-50 border border-sky-100 px-1.5 py-0.5 rounded-full flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-pulse inline-block" />
                  LIVE
                </span>
              )}
            </div>
            <div className="flex bg-slate-50 p-1 rounded-lg border border-slate-100 gap-0.5">
              {ctrl.options.map((opt, idx) => (
                <button
                  key={opt}
                  onClick={() => updateEvidence(ctrl.key, idx)}
                  className={`relative flex-1 text-[10px] font-bold py-1.5 px-1 rounded-md transition-all ${
                    evidence[ctrl.key] === idx ? 'text-blue-600' : 'text-slate-400 hover:text-slate-600'
                  }`}
                >
                  {evidence[ctrl.key] === idx && (
                    <motion.div
                      layoutId={`ctrl-active-${ctrl.key}`}
                      className="absolute inset-0 bg-white shadow-sm border border-slate-200 rounded-md"
                      transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                    />
                  )}
                  <span className="relative z-10">{opt}</span>
                </button>
              ))}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Run button */}
      <motion.button
        onClick={onPredict}
        disabled={loading}
        whileHover={{ scale: loading ? 1 : 1.02 }}
        whileTap={{ scale: loading ? 1 : 0.98 }}
        className="btn-primary w-full py-3 mt-1 relative overflow-hidden"
      >
        {loading ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            <span>Synthesizing Consensus...</span>
          </>
        ) : (
          <>
            <Zap className="w-4 h-4" />
            <span>Run Consensus Simulation</span>
            <ChevronRight className="w-4 h-4" />
          </>
        )}
      </motion.button>
    </div>
  );
};

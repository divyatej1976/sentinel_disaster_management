import React from 'react';
import { Cloud, Users, Droplets, Activity, CloudRain, Waves, ShieldAlert } from 'lucide-react';
import type { Evidence } from '../types';

export interface ControlConfig {
  key: string;
  icon: React.ReactNode;
  label: string;
  options: string[];
  color: string;
  isLive: boolean;
}

export const HAZARD_CONTROLS: Record<string, { label: string; controls: ControlConfig[] }> = {
  disease: {
    label: "Disease Outbreak",
    controls: [
      {
        key: 'Weather',
        icon: <Cloud className="w-4 h-4" />,
        label: 'Weather Pattern',
        options: ['Clear', 'Mild', 'Humid', 'Adverse'],
        color: 'text-sky-500',
        isLive: false, // will dynamically set this in the component if needed, or handle live weather separately
      },
      {
        key: 'PopulationDensity',
        icon: <Users className="w-4 h-4" />,
        label: 'Population Density',
        options: ['Low', 'Medium', 'High', 'Very High'],
        color: 'text-violet-500',
        isLive: false,
      },
      {
        key: 'Sanitation',
        icon: <Droplets className="w-4 h-4" />,
        label: 'Sanitation Level',
        options: ['Poor', 'Moderate', 'Good'],
        color: 'text-teal-500',
        isLive: false,
      },
      {
        key: 'RecentCases',
        icon: <Activity className="w-4 h-4" />,
        label: 'Case Velocity',
        options: ['< 100', '101–1k', '1k–5k', '> 5k'],
        color: 'text-rose-500',
        isLive: false,
      },
    ]
  },
  flood: {
    label: "Flood",
    controls: [
      {
        key: 'RainfallIntensity',
        icon: <CloudRain className="w-4 h-4" />,
        label: 'Rainfall Intensity',
        options: ['Light', 'Moderate', 'Heavy', 'Extreme'],
        color: 'text-blue-500',
        isLive: false,
      },
      {
        key: 'RiverLevel',
        icon: <Waves className="w-4 h-4" />,
        label: 'River Level',
        options: ['Normal', 'Elevated', 'Near Flood Stage', 'Flooding'],
        color: 'text-cyan-500',
        isLive: false,
      },
      {
        key: 'PopulationDensity',
        icon: <Users className="w-4 h-4" />,
        label: 'Population Density',
        options: ['Low', 'Medium', 'High', 'Very High'],
        color: 'text-violet-500',
        isLive: false,
      },
      {
        key: 'DrainageCapacity',
        icon: <ShieldAlert className="w-4 h-4" />,
        label: 'Drainage Capacity',
        options: ['Excellent', 'Good', 'Poor', 'Failing'],
        color: 'text-indigo-500',
        isLive: false,
      },
    ]
  }
};

export const getDefaultEvidence = (hazard: string): Evidence => {
  const config = HAZARD_CONTROLS[hazard];
  if (!config) return {};
  
  const defaultEvidence: Evidence = {};
  config.controls.forEach(ctrl => {
    // Default to index 1 (Medium/Mild/etc)
    defaultEvidence[ctrl.key] = 1;
  });
  return defaultEvidence;
};

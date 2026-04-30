export interface Evidence {
  Weather: number;
  PopulationDensity: number;
  Sanitation: number;
  RecentCases: number;
}

export interface ExpertOpinion {
  agent_id: string;
  expert: string;
  role: string;
  weight: number;
  opinion: string;
  risk_rating: number;
  primary_factors: string[];
  recommendation: string;
  factor_impacts: {
    weather: number;
    density: number;
    sanitation: number;
    cases: number;
  };
}

export interface Prediction {
  final_probability: number;
  confidence_score: number;
  risk_level: string;
  disagreement_index: number;
  confidence_explanation: string;
  expert_opinions: ExpertOpinion[];
  critical_factors: {
    weather: number;
    density: number;
    sanitation: number;
    cases: number;
  };
  top_risk_drivers: string[];
  mitigation_strategies: string[];
  architecture_note: string;
  demo_mode: boolean;
}

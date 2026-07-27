from typing import Dict, List
from pydantic import BaseModel, Field

class ExpertOpinion(BaseModel):
    agent_id: str
    expert: str
    role: str
    weight: float
    opinion: str
    risk_rating: float = Field(..., ge=0, le=10)
    primary_factors: List[str]
    recommendation: str
    factor_impacts: Dict[str, float]

class RiskAssessmentResponse(BaseModel):
    final_probability: float = Field(..., ge=0, le=1)
    confidence_score: float = Field(..., ge=0, le=1)
    risk_level: str
    disagreement_index: float = Field(..., ge=0, le=1)
    confidence_explanation: str
    expert_opinions: List[ExpertOpinion]
    critical_factors: Dict[str, float]
    top_risk_drivers: List[str]
    mitigation_strategies: List[str]
    architecture_note: str
    demo_mode: bool
    reasoning: List[str]

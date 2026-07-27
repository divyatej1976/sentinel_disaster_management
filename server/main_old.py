import json
import logging
import math
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, field_validator

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outbreak-predictor")

raw_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY") or ""
api_key = raw_api_key.strip()
has_gemini_key = bool(api_key) and "your_gemini_api_key_here" not in api_key.lower()
client = genai.Client(api_key=api_key if has_gemini_key else " ")

app = FastAPI(
    title="Epidemiological Intelligence API",
    version="3.0.0",
    description="Multi-agent decision-support API for infectious disease risk assessment.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

evidence_labels = {
    "Weather": ["Clear", "Mild", "Humid", "Adverse"],
    "PopulationDensity": ["Low", "Medium", "High", "Very High"],
    "Sanitation": ["Poor", "Moderate", "Good"],
    "RecentCases": ["< 100", "101 - 1k", "1k - 5k", "> 5k"],
}

agent_specs = [
    {
        "id": "epidemiologist",
        "expert": "Dr. Aris",
        "role": "Epidemiologist",
        "weight": 0.45,
        "focus": "pathogen transmission, case velocity, and density-driven spread",
    },
    {
        "id": "environmental_scientist",
        "expert": "Prof. Lyra",
        "role": "Environmental Scientist",
        "weight": 0.30,
        "focus": "weather, sanitation, climate stress, and infrastructure exposure",
    },
    {
        "id": "public_health_strategist",
        "expert": "Gen. Vance",
        "role": "Public Health Strategist",
        "weight": 0.25,
        "focus": "response capacity, public controls, escalation risk, and mitigation priority",
    },
]


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


class ConsensusResponse(BaseModel):
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


class PredictRequest(BaseModel):
    evidence: Dict[str, int]
    model: str = "gemini-2.0-flash"

    @field_validator("evidence")
    @classmethod
    def validate_evidence(cls, value: Dict[str, int]) -> Dict[str, int]:
        required = {"Weather", "PopulationDensity", "Sanitation", "RecentCases"}
        missing = required - value.keys()
        if missing:
            raise ValueError(f"Missing required evidence fields: {missing}")

        bounds = {
            "Weather": (0, 3),
            "PopulationDensity": (0, 3),
            "Sanitation": (0, 2),
            "RecentCases": (0, 3),
        }
        for key, (minimum, maximum) in bounds.items():
            if not isinstance(value[key], int) or not minimum <= value[key] <= maximum:
                raise ValueError(f"{key} must be an integer between {minimum} and {maximum}")
        return value


agent_schema = {
    "type": "OBJECT",
    "properties": {
        "opinion": {"type": "STRING"},
        "risk_rating": {"type": "NUMBER"},
        "primary_factors": {"type": "ARRAY", "items": {"type": "STRING"}},
        "recommendation": {"type": "STRING"},
        "factor_impacts": {
            "type": "OBJECT",
            "properties": {
                "weather": {"type": "NUMBER"},
                "density": {"type": "NUMBER"},
                "sanitation": {"type": "NUMBER"},
                "cases": {"type": "NUMBER"},
            },
            "required": ["weather", "density", "sanitation", "cases"],
        },
    },
    "required": ["opinion", "risk_rating", "primary_factors", "recommendation", "factor_impacts"],
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def evidence_prompt(evidence: Dict[str, int]) -> str:
    return "\n".join(
        [
            f"- Weather: {evidence_labels['Weather'][evidence['Weather']]}",
            f"- Population Density: {evidence_labels['PopulationDensity'][evidence['PopulationDensity']]}",
            f"- Sanitation: {evidence_labels['Sanitation'][evidence['Sanitation']]}",
            f"- Recent Case Load: {evidence_labels['RecentCases'][evidence['RecentCases']]}",
        ]
    )


def deterministic_agent(spec: Dict[str, Any], evidence: Dict[str, int]) -> ExpertOpinion:
    weather = evidence["Weather"]
    density = evidence["PopulationDensity"]
    sanitation_risk = 2 - evidence["Sanitation"]
    cases = evidence["RecentCases"]

    if spec["id"] == "epidemiologist":
        rating = 1.4 + cases * 2.0 + density * 1.15 + weather * 0.35
        factors = ["recent case load", "population density"]
        recommendation = "Prioritize rapid testing, cluster tracing, and targeted isolation in dense areas."
    elif spec["id"] == "environmental_scientist":
        rating = 1.2 + weather * 1.4 + sanitation_risk * 1.85 + density * 0.45
        factors = ["sanitation", "weather pattern"]
        recommendation = "Improve sanitation access, water safety, and weather-sensitive public advisories."
    else:
        rating = 1.0 + cases * 1.25 + density * 0.85 + sanitation_risk * 0.95
        factors = ["system response load", "case velocity"]
        recommendation = "Prepare phased response protocols, public alerts, and resource allocation triggers."

    factor_impacts = {
        "weather": clamp(weather / 3 * 100, 0, 100),
        "density": clamp(density / 3 * 100, 0, 100),
        "sanitation": clamp(sanitation_risk / 2 * 100, 0, 100),
        "cases": clamp(cases / 3 * 100, 0, 100),
    }
    rating = clamp(rating, 0, 10)

    return ExpertOpinion(
        agent_id=spec["id"],
        expert=spec["expert"],
        role=spec["role"],
        weight=spec["weight"],
        opinion=(
            f"{spec['role']} assessment: current telemetry indicates a "
            f"{'controlled' if rating < 4 else 'watchlist' if rating < 7 else 'high-alert'} risk profile."
        ),
        risk_rating=round(rating, 2),
        primary_factors=factors,
        recommendation=recommendation,
        factor_impacts=factor_impacts,
    )


def call_agent(model_name: str, spec: Dict[str, Any], evidence: Dict[str, int]) -> ExpertOpinion:
    if not has_gemini_key:
        return deterministic_agent(spec, evidence)

    prompt = f"""
You are {spec['expert']}, a {spec['role']} in a disease outbreak risk council.
Focus only on {spec['focus']}. Do not produce the final consensus.

Telemetry:
{evidence_prompt(evidence)}

Return a concise expert opinion, risk rating from 0-10, top primary factors,
one mitigation recommendation, and factor impact scores from 0-100.
"""
    try:
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=agent_schema,
            temperature=0.25,
        )
        response = client.models.generate_content(model=model_name, contents=prompt, config=config)
        data = json.loads(response.text.strip())
        return ExpertOpinion(
            agent_id=spec["id"],
            expert=spec["expert"],
            role=spec["role"],
            weight=spec["weight"],
            opinion=data["opinion"],
            risk_rating=clamp(float(data["risk_rating"]), 0, 10),
            primary_factors=data["primary_factors"][:3],
            recommendation=data["recommendation"],
            factor_impacts={
                key: clamp(float(data["factor_impacts"][key]), 0, 100)
                for key in ["weather", "density", "sanitation", "cases"]
            },
        )
    except Exception as exc:
        logger.warning("Agent %s failed, using deterministic fallback: %s", spec["id"], exc)
        return deterministic_agent(spec, evidence)


def aggregate_consensus(opinions: List[ExpertOpinion], demo_mode: bool) -> ConsensusResponse:
    weighted_rating = sum(opinion.risk_rating * opinion.weight for opinion in opinions)
    final_probability = clamp(weighted_rating / 10, 0, 1)

    ratings = [opinion.risk_rating for opinion in opinions]
    mean_rating = sum(ratings) / len(ratings)
    variance = sum((rating - mean_rating) ** 2 for rating in ratings) / len(ratings)
    disagreement_index = clamp(math.sqrt(variance) / 5, 0, 1)
    confidence_score = clamp(0.92 - disagreement_index * 0.55, 0.35, 0.95)

    if final_probability < 0.35:
        risk_level = "Low"
    elif final_probability < 0.65:
        risk_level = "Medium"
    else:
        risk_level = "High"

    critical_factors = {
        key: round(sum(op.factor_impacts[key] * op.weight for op in opinions), 1)
        for key in ["weather", "density", "sanitation", "cases"]
    }
    top_risk_drivers = [
        key.replace("_", " ").title()
        for key, _ in sorted(critical_factors.items(), key=lambda item: item[1], reverse=True)[:3]
    ]
    mitigation_strategies = list(dict.fromkeys(opinion.recommendation for opinion in opinions))

    confidence_explanation = (
        f"The consensus engine combined {len(opinions)} independent expert assessments using "
        f"weighted aggregation. Expert disagreement is {disagreement_index * 100:.0f}%, "
        f"so confidence is {confidence_score * 100:.0f}%."
    )

    return ConsensusResponse(
        final_probability=round(final_probability, 3),
        confidence_score=round(confidence_score, 3),
        risk_level=risk_level,
        disagreement_index=round(disagreement_index, 3),
        confidence_explanation=confidence_explanation,
        expert_opinions=opinions,
        critical_factors=critical_factors,
        top_risk_drivers=top_risk_drivers,
        mitigation_strategies=mitigation_strategies,
        architecture_note=(
            "Separate Gemini expert agents evaluate the same telemetry independently; "
            "the API then computes weighted consensus, disagreement, confidence, and drivers."
        ),
        demo_mode=demo_mode,
    )


@app.post("/api/predict", response_model=ConsensusResponse)
async def predict(body: PredictRequest):
    logger.info("Processing multi-agent risk assessment for inputs: %s", body.evidence)
    try:
        opinions = [call_agent(body.model, spec, body.evidence) for spec in agent_specs]
        return aggregate_consensus(opinions, demo_mode=not has_gemini_key)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Consensus generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Unable to generate consensus risk assessment")


@app.get("/api/health")
def health():
    return {
        "status": "operational",
        "version": "3.0.0",
        "mode": "gemini" if has_gemini_key else "demo-fallback",
        "agents": [spec["id"] for spec in agent_specs],
    }

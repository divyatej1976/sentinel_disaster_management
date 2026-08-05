from typing import Any, Dict, List
import math
import os
import yaml
from pydantic import BaseModel, field_validator
from .base import HazardModule

# Load config once at module level
config_path = os.path.join(os.path.dirname(__file__), "..", "config", "disease.yaml")
with open(config_path, "r") as f:
    DISEASE_CONFIG = yaml.safe_load(f)

evidence_labels = {
    "Weather": ["Clear", "Mild", "Humid", "Adverse"],
    "PopulationDensity": ["Low", "Medium", "High", "Very High"],
    "Sanitation": ["Poor", "Moderate", "Good"],
    "RecentCases": ["< 100", "101 - 1k", "1k - 5k", "> 5k"],
}

class DiseaseInput(BaseModel):
    Weather: int
    PopulationDensity: int
    Sanitation: int
    RecentCases: int

    @field_validator("Weather", "PopulationDensity", "Sanitation", "RecentCases", mode="before")
    @classmethod
    def validate_bounds(cls, value: int, info) -> int:
        bounds = {
            "Weather": (0, 3),
            "PopulationDensity": (0, 3),
            "Sanitation": (0, 2),
            "RecentCases": (0, 3),
        }
        minimum, maximum = bounds[info.field_name]
        if not isinstance(value, int) or not minimum <= value <= maximum:
            raise ValueError(f"{info.field_name} must be an integer between {minimum} and {maximum}")
        return value

class DiseaseHazard:
    name = "disease"
    input_schema = DiseaseInput
    knowledge_corpus_path = "server/data/knowledge/disease"

    personas = [
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

    def risk_prompts(self, data: dict) -> list[str]:
        prompts = []
        evidence_text = "\n".join(
            [
                f"- Weather: {evidence_labels['Weather'][data['Weather']]}",
                f"- Population Density: {evidence_labels['PopulationDensity'][data['PopulationDensity']]}",
                f"- Sanitation: {evidence_labels['Sanitation'][data['Sanitation']]}",
                f"- Recent Case Load: {evidence_labels['RecentCases'][data['RecentCases']]}",
            ]
        )
        
        for spec in self.personas:
            prompt = f"""
You are {spec['expert']}, a {spec['role']} in a disease outbreak risk council.
Focus only on {spec['focus']}. Do not produce the final consensus.

Telemetry:
{evidence_text}

Return a concise expert opinion, risk rating from 0-10, top primary factors,
one mitigation recommendation, and factor impact scores from 0-100.
"""
            prompts.append(prompt)
        return prompts

    def deterministic_opinion(self, persona_id: str, data: dict) -> dict:
        weather = data["Weather"]
        density = data["PopulationDensity"]
        sanitation_risk = 2 - data["Sanitation"]
        cases = data["RecentCases"]

        def clamp(value: float, minimum: float, maximum: float) -> float:
            return max(minimum, min(maximum, value))

        spec = next((p for p in self.personas if p["id"] == persona_id), None)
        if not spec:
            raise ValueError(f"Unknown persona_id: {persona_id}")

        if persona_id == "epidemiologist":
            rating = 1.4 + cases * 2.0 + density * 1.15 + weather * 0.35
            factors = ["recent case load", "population density"]
            recommendation = "Prioritize rapid testing, cluster tracing, and targeted isolation in dense areas."
        elif persona_id == "environmental_scientist":
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

        return {
            "opinion": (
                f"{spec['role']} assessment: current telemetry indicates a "
                f"{'controlled' if rating < 4 else 'watchlist' if rating < 7 else 'high-alert'} risk profile."
            ),
            "risk_rating": round(rating, 2),
            "primary_factors": factors,
            "recommendation": recommendation,
            "factor_impacts": factor_impacts,
        }

    def resource_formulas(self, risk_level: str, population: int) -> dict:
        if risk_level not in DISEASE_CONFIG:
            raise ValueError(f"Invalid risk_level '{risk_level}'. Must be one of {list(DISEASE_CONFIG.keys())}")
        
        rates = DISEASE_CONFIG[risk_level]
        resources = {}
        for category, rate in rates.items():
            base_name = category.replace("_per_100k", "")
            resources[base_name] = math.ceil(rate * (population / 100000.0))
            
        return resources

    def report_context(self, risk: dict, resources: dict, knowledge: dict) -> dict:
        return {
            "hazard_title": "Disease Outbreak",
            "hazard_context": "Telemetry and expert consensus indicate biological contagion risks requiring coordinated public health measures."
        }

# Verify DiseaseHazard implements HazardModule
_: HazardModule = DiseaseHazard()

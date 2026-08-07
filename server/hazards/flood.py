from typing import Any, Dict, List
import math
import os
import yaml
from pydantic import BaseModel, field_validator
from .base import HazardModule

# Load config once at module level
config_path = os.path.join(os.path.dirname(__file__), "..", "config", "flood.yaml")
with open(config_path, "r") as f:
    FLOOD_CONFIG = yaml.safe_load(f)

evidence_labels = {
    "RainfallIntensity": ["Light", "Moderate", "Heavy", "Extreme"],
    "RiverLevel": ["Normal", "Elevated", "Near Flood Stage", "Flooding"],
    "PopulationDensity": ["Low", "Medium", "High", "Very High"],
    "DrainageCapacity": ["Excellent", "Good", "Poor", "Failing"],
}

class FloodInput(BaseModel):
    RainfallIntensity: int
    RiverLevel: int
    PopulationDensity: int
    DrainageCapacity: int

    @field_validator("RainfallIntensity", "RiverLevel", "PopulationDensity", "DrainageCapacity", mode="before")
    @classmethod
    def validate_bounds(cls, value: int, info) -> int:
        bounds = {
            "RainfallIntensity": (0, 3),
            "RiverLevel": (0, 3),
            "PopulationDensity": (0, 3),
            "DrainageCapacity": (0, 3),
        }
        minimum, maximum = bounds[info.field_name]
        if not isinstance(value, int) or not minimum <= value <= maximum:
            raise ValueError(f"{info.field_name} must be an integer between {minimum} and {maximum}")
        return value

class FloodHazard:
    name = "flood"
    input_schema = FloodInput
    knowledge_corpus_path = "server/data/knowledge/flood"

    personas = [
        {
            "id": "hydrologist",
            "expert": "Dr. Rivers",
            "role": "Hydrologist",
            "weight": 0.45,
            "focus": "rainfall accumulation, river catchment levels, and flow velocity",
        },
        {
            "id": "infrastructure_engineer",
            "expert": "Eng. Silva",
            "role": "Infrastructure Engineer",
            "weight": 0.30,
            "focus": "drainage systems, dam structural integrity, and urban runoff",
        },
        {
            "id": "emergency_strategist",
            "expert": "Cmdr. Torres",
            "role": "Emergency Management Strategist",
            "weight": 0.25,
            "focus": "evacuation routes, population exposure, and rescue logistics",
        },
    ]

    def risk_prompts(self, data: dict) -> list[str]:
        prompts = []
        evidence_text = "\n".join(
            [
                f"- Rainfall Intensity: {evidence_labels['RainfallIntensity'][data['RainfallIntensity']]}",
                f"- River Level: {evidence_labels['RiverLevel'][data['RiverLevel']]}",
                f"- Population Density: {evidence_labels['PopulationDensity'][data['PopulationDensity']]}",
                f"- Drainage Capacity: {evidence_labels['DrainageCapacity'][data['DrainageCapacity']]}",
            ]
        )
        
        for spec in self.personas:
            prompt = f"""
You are {spec['expert']}, a {spec['role']} in a flood risk council.
Focus only on {spec['focus']}. Do not produce the final consensus.

Telemetry:
{evidence_text}

Return a concise expert opinion, risk rating from 0-10, top primary factors,
one mitigation recommendation, and factor impact scores from 0-100.
"""
            prompts.append(prompt)
        return prompts

    def deterministic_opinion(self, persona_id: str, data: dict) -> dict:
        rainfall = data["RainfallIntensity"]
        river = data["RiverLevel"]
        density = data["PopulationDensity"]
        drainage_risk = data["DrainageCapacity"] # 3 is Failing, highest risk

        def clamp(value: float, minimum: float, maximum: float) -> float:
            return max(minimum, min(maximum, value))

        spec = next((p for p in self.personas if p["id"] == persona_id), None)
        if not spec:
            raise ValueError(f"Unknown persona_id: {persona_id}")

        if persona_id == "hydrologist":
            rating = 1.0 + rainfall * 1.5 + river * 1.5
            factors = ["rainfall accumulation", "river catchment"]
            recommendation = "Deploy sandbags at key river bends and monitor water gauges."
        elif persona_id == "infrastructure_engineer":
            rating = 1.0 + drainage_risk * 1.8 + rainfall * 1.2
            factors = ["drainage capacity", "urban runoff"]
            recommendation = "Clear storm drains immediately and deploy portable water pumps."
        else:
            rating = 1.0 + density * 1.5 + river * 1.0 + drainage_risk * 0.5
            factors = ["population exposure", "evacuation routes"]
            recommendation = "Pre-position rescue boats and open elevated emergency shelters."

        factor_impacts = {
            "rainfall": clamp(rainfall / 3 * 100, 0, 100),
            "river": clamp(river / 3 * 100, 0, 100),
            "density": clamp(density / 3 * 100, 0, 100),
            "drainage": clamp(drainage_risk / 3 * 100, 0, 100),
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
        if risk_level not in FLOOD_CONFIG:
            raise ValueError(f"Invalid risk_level '{risk_level}'. Must be one of {list(FLOOD_CONFIG.keys())}")
        
        rates = FLOOD_CONFIG[risk_level]
        resources = {}
        for category, rate in rates.items():
            base_name = category.replace("_per_100k", "")
            resources[base_name] = math.ceil(rate * (population / 100000.0))
            
        return resources

    def report_context(self, risk: dict, resources: dict, knowledge: dict) -> dict:
        return {
            "hazard_title": "Flood Event",
            "hazard_context": "Hydrological data indicates significant water accumulation requiring infrastructure defense and potential evacuation."
        }

# Verify FloodHazard implements HazardModule
_: HazardModule = FloodHazard()

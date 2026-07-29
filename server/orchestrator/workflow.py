from server.hazards import HAZARDS
from server.agents import risk_agent

def run_assessment(hazard: str, data: dict, model: str = "gemini-2.0-flash") -> dict:
    hazard_module = HAZARDS.get(hazard)
    if hazard_module is None:
        raise ValueError(f"Unknown hazard: {hazard}")
    validated = hazard_module.input_schema(**data)
    return risk_agent.run(hazard_module, validated.model_dump(), model)

from typing import Protocol, Type, List, Dict, Any
from pydantic import BaseModel

class HazardModule(Protocol):
    name: str
    input_schema: Type[BaseModel]
    personas: List[Dict[str, Any]]

    def risk_prompts(self, data: dict) -> list[str]:
        """Prompts for each of the 3 consensus personas, tailored to this hazard."""
        ...

    def deterministic_opinion(self, persona_id: str, data: dict) -> dict:
        """
        Rule-based fallback opinion for one persona, used when the LLM call fails or no API key
        is configured. Returns a dict shaped like: opinion, risk_rating, primary_factors,
        recommendation, factor_impacts — same fields the Risk Agent expects from an LLM response.
        """
        ...

    def resource_formulas(self, risk_level: str, population: int) -> dict:
        """Deterministic resource calculation for this hazard."""
        ...

    knowledge_corpus_path: str

    def report_context(self, risk: dict, resources: dict, knowledge: dict) -> dict:
        """Any hazard-specific framing for the report templates."""
        ...

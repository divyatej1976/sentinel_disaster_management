from typing import Protocol, Type
from pydantic import BaseModel

class HazardModule(Protocol):
    name: str
    input_schema: Type[BaseModel]

    def risk_prompts(self, data: dict) -> list[str]:
        """Prompts for each of the 3 consensus personas, tailored to this hazard."""
        ...

    def resource_formulas(self, risk_level: str, population: int) -> dict:
        """Deterministic resource calculation for this hazard."""
        ...

    knowledge_corpus_path: str

    def report_context(self, risk: dict, resources: dict, knowledge: dict) -> dict:
        """Any hazard-specific framing for the report templates."""
        ...

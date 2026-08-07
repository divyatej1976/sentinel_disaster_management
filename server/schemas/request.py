from typing import Any, Dict
from pydantic import BaseModel

class RiskAssessmentRequest(BaseModel):
    hazard: str
    location: str
    data: Dict[str, Any]
    model: str = "gemini-2.0-flash"
    template: str = "officer"
    include_knowledge_question: str | None = None
    # GAP: Population is currently not collected in the frontend App.tsx/ControlsPanel.
    # Defaulting server-side to 100000 for now.
    population: int = 100000

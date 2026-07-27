from typing import Any, Dict
from pydantic import BaseModel

class RiskAssessmentRequest(BaseModel):
    hazard: str
    location: str
    data: Dict[str, Any]
    model: str = "gemini-2.0-flash"

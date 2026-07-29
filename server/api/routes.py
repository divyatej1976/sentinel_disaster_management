import logging
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from server.schemas.request import RiskAssessmentRequest
from server.schemas.response import RiskAssessmentResponse
from server.orchestrator import workflow
from server.hazards import HAZARDS
from server.agents.risk_agent import has_gemini_key

logger = logging.getLogger("outbreak-predictor")
router = APIRouter()

@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess(request: RiskAssessmentRequest):
    logger.info("Processing multi-agent risk assessment for hazard: %s", request.hazard)
    try:
        result = workflow.run_assessment(request.hazard, request.data, request.model)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        logger.exception("Assessment generation failed: %s", e)
        raise HTTPException(status_code=500, detail="Unable to generate risk assessment")

@router.get("/health")
def health():
    return {
        "status": "operational",
        "version": "3.0.0",
        "mode": "gemini" if has_gemini_key else "demo-fallback",
        "agents": list(HAZARDS.keys()),
    }

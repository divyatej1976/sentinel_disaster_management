import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
import json
from sqlalchemy.orm import Session
from server.db.database import get_db
from server.db.models import AssessmentRecord

from server.schemas.request import RiskAssessmentRequest
from server.schemas.response import RiskAssessmentResponse
from server.orchestrator import workflow
from server.hazards import HAZARDS
from server.agents.risk_agent import has_gemini_key
import uuid
from server.logging_context import request_id_var

logger = logging.getLogger("outbreak-predictor")
router = APIRouter()

@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess(request: RiskAssessmentRequest):
    request_id_var.set(uuid.uuid4().hex[:8])
    logger.info("Processing multi-agent risk assessment for hazard: %s", request.hazard)
    try:
        result = workflow.run_assessment(request.hazard, request.data, request.model)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Assessment generation failed: %s", e)
        raise HTTPException(status_code=500, detail="Unable to generate risk assessment")

from pydantic import BaseModel
from server.schemas.response import AskResponse

class AskRequest(BaseModel):
    hazard: str
    question: str
    model: str = "gemini-2.0-flash"

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    request_id_var.set(uuid.uuid4().hex[:8])
    logger.info("Processing knowledge retrieval for hazard: %s", request.hazard)
    try:
        result = workflow.answer_question(request.hazard, request.question, request.model)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Knowledge retrieval failed: %s", e)
        raise HTTPException(status_code=500, detail="Unable to retrieve knowledge")

@router.post("/report")
async def report(request: RiskAssessmentRequest):
    request_id_var.set(uuid.uuid4().hex[:8])
    logger.info("Processing full report for hazard: %s with template: %s", request.hazard, request.template)
    try:
        # Note: We intentionally do NOT use a response_model for this endpoint
        # because the response shape varies drastically based on the requested template
        # (officer vs citizen vs executive). We rely on Pydantic to validate the input,
        # but leave the output schema flexible.
        result = workflow.run_full_assessment(
            hazard=request.hazard,
            data=request.data,
            population=request.population,
            template=request.template,
            model=request.model,
            knowledge_question=request.include_knowledge_question
        )
        return result
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Report generation failed: %s", e)
        raise HTTPException(status_code=500, detail="Unable to generate full report")

@router.get("/health")
def health():
    return {
        "status": "operational",
        "version": "3.0.0",
        "mode": "gemini" if has_gemini_key else "demo-fallback",
        "agents": list(HAZARDS.keys()),
    }

@router.get("/history")
def get_history(hazard: str = None, db: Session = Depends(get_db)):
    try:
        query = db.query(AssessmentRecord)
        if hazard:
            query = query.filter(AssessmentRecord.hazard == hazard)
        records = query.order_by(AssessmentRecord.created_at.desc()).limit(20).all()
        
        result = []
        for r in records:
            result.append({
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "hazard": r.hazard,
                "risk_level": r.risk_level,
                "final_probability": r.final_probability,
                "template": r.template,
                "result_json": json.loads(r.result_json) if r.result_json else None
            })
        return result
    except Exception as e:
        logger.exception("History fetch failed: %s", e)
        raise HTTPException(status_code=500, detail="Unable to fetch history")

import json
import logging
import os
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .consensus import compute_consensus

load_dotenv()

logger = logging.getLogger("outbreak-predictor")

raw_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY") or ""
api_key = raw_api_key.strip()
has_gemini_key = bool(api_key) and "your_gemini_api_key_here" not in api_key.lower()
client = genai.Client(api_key=api_key if has_gemini_key else " ")

agent_schema = {
    "type": "OBJECT",
    "properties": {
        "opinion": {"type": "STRING"},
        "risk_rating": {"type": "NUMBER"},
        "primary_factors": {"type": "ARRAY", "items": {"type": "STRING"}},
        "recommendation": {"type": "STRING"},
        "factor_impacts": {
            "type": "OBJECT",
        },
    },
    "required": ["opinion", "risk_rating", "primary_factors", "recommendation", "factor_impacts"],
}

def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))

def run(hazard, data: dict, model: str = "gemini-2.0-flash") -> dict:
    prompts = hazard.risk_prompts(data)
    opinions = []
    
    for persona, prompt in zip(hazard.personas, prompts):
        opinion_dict = None
        
        if has_gemini_key:
            try:
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=agent_schema,
                    temperature=0.25,
                )
                response = client.models.generate_content(model=model, contents=prompt, config=config)
                raw_data = json.loads(response.text.strip())
                
                # Format exactly as expected by consensus
                opinion_dict = {
                    "opinion": raw_data["opinion"],
                    "risk_rating": clamp(float(raw_data["risk_rating"]), 0, 10),
                    "primary_factors": raw_data["primary_factors"][:3],
                    "recommendation": raw_data["recommendation"],
                    "factor_impacts": {
                        key: clamp(float(val), 0, 100)
                        for key, val in raw_data["factor_impacts"].items()
                    }
                }
            except Exception as exc:
                logger.warning("Agent %s failed, using deterministic fallback: %s", persona["id"], exc)
            
        if not opinion_dict:
            opinion_dict = hazard.deterministic_opinion(persona["id"], data)
            
        # Merge with persona metadata
        opinion_dict.update({
            "id": persona["id"],
            "expert": persona["expert"],
            "role": persona["role"],
            "weight": persona["weight"]
        })
        
        opinions.append(opinion_dict)
        
    consensus_result = compute_consensus(opinions)
    
    expert_opinions = []
    for op in opinions:
        mapped_op = op.copy()
        mapped_op["agent_id"] = mapped_op.pop("id")
        expert_opinions.append(mapped_op)
        
    architecture_note = (
        "Separate Gemini expert agents evaluate the same telemetry independently; "
        "the API then computes weighted consensus, disagreement, confidence, and drivers."
    )
    
    consensus_result.update({
        "expert_opinions": expert_opinions,
        "architecture_note": architecture_note,
        "demo_mode": not has_gemini_key,
    })
    
    return consensus_result

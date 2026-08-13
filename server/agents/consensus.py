import math
from typing import List, Dict, Any

def compute_consensus(opinions: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not opinions:
        raise ValueError("Cannot compute consensus with zero opinions.")

    def clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))

    weighted_rating = sum(opinion["risk_rating"] * opinion["weight"] for opinion in opinions)
    final_probability = clamp(weighted_rating / 10.0, 0.0, 1.0)

    ratings = [opinion["risk_rating"] for opinion in opinions]
    mean_rating = sum(ratings) / len(ratings)
    variance = sum((rating - mean_rating) ** 2 for rating in ratings) / len(ratings)
    disagreement_index = clamp(math.sqrt(variance) / 5.0, 0.0, 1.0)
    confidence_score = clamp(0.92 - disagreement_index * 0.55, 0.35, 0.95)

    if final_probability < 0.35:
        risk_level = "Low"
    elif final_probability < 0.65:
        risk_level = "Medium"
    else:
        risk_level = "High"

    all_factor_keys = list(dict.fromkeys(
        key for opinion in opinions for key in opinion["factor_impacts"].keys()
    ))

    critical_factors = {
        key: round(sum(op["factor_impacts"].get(key, 0) * op["weight"] for op in opinions), 1)
        for key in all_factor_keys
    }

    top_risk_drivers = [
        key.replace("_", " ").title()
        for key, _ in sorted(critical_factors.items(), key=lambda item: item[1], reverse=True)[:3]
    ]
    
    mitigation_strategies = list(dict.fromkeys(opinion["recommendation"] for opinion in opinions))

    confidence_explanation = (
        f"The consensus engine combined {len(opinions)} independent expert assessments using "
        f"weighted aggregation. Expert disagreement is {disagreement_index * 100:.0f}%, "
        f"so confidence is {confidence_score * 100:.0f}%."
    )

    reasoning = [f"{opinion['role']}: {opinion['opinion']}" for opinion in opinions]
    reasoning.append(confidence_explanation)

    return {
        "final_probability": round(final_probability, 3),
        "confidence_score": round(confidence_score, 3),
        "risk_level": risk_level,
        "disagreement_index": round(disagreement_index, 3),
        "confidence_explanation": confidence_explanation,
        "critical_factors": critical_factors,
        "top_risk_drivers": top_risk_drivers,
        "mitigation_strategies": mitigation_strategies,
        "reasoning": reasoning,
    }

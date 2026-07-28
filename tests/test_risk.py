import pytest
from server.agents.consensus import compute_consensus

def create_opinion(
    role="Role", 
    opinion_text="Opinion", 
    risk_rating=5.0, 
    weight=0.33, 
    factor_impacts=None
):
    if factor_impacts is None:
        factor_impacts = {"weather": 50, "cases": 50}
        
    return {
        "id": role.lower().replace(" ", "_"),
        "expert": f"Expert {role}",
        "role": role,
        "weight": weight,
        "opinion": opinion_text,
        "risk_rating": risk_rating,
        "primary_factors": list(factor_impacts.keys())[:3],
        "recommendation": f"Recommendation from {role}",
        "factor_impacts": factor_impacts,
    }

def test_agreement():
    opinions = [
        create_opinion(role="A", risk_rating=5.0, weight=0.34),
        create_opinion(role="B", risk_rating=5.0, weight=0.33),
        create_opinion(role="C", risk_rating=5.0, weight=0.33),
    ]
    result = compute_consensus(opinions)
    assert result["disagreement_index"] == 0.0
    assert result["confidence_score"] == 0.92

def test_disagreement():
    opinions = [
        create_opinion(role="A", risk_rating=1.0, weight=0.34),
        create_opinion(role="B", risk_rating=5.0, weight=0.33),
        create_opinion(role="C", risk_rating=9.0, weight=0.33),
    ]
    result = compute_consensus(opinions)
    assert result["disagreement_index"] > 0.0
    assert result["confidence_score"] < 0.92

def test_weighted_calculation():
    opinions = [
        create_opinion(role="A", risk_rating=8.0, weight=0.5),
        create_opinion(role="B", risk_rating=4.0, weight=0.3),
        create_opinion(role="C", risk_rating=2.0, weight=0.2),
    ]
    result = compute_consensus(opinions)
    assert result["final_probability"] == 0.56
    assert result["risk_level"] == "Medium"

def test_hazard_agnostic_aggregation():
    opinions = [
        create_opinion(role="A", weight=0.5, factor_impacts={"rainfall": 80, "river_level": 40}),
        create_opinion(role="B", weight=0.5, factor_impacts={"rainfall": 20, "drainage": 90}),
    ]
    result = compute_consensus(opinions)
    
    assert "rainfall" in result["critical_factors"]
    assert "river_level" in result["critical_factors"]
    assert "drainage" in result["critical_factors"]
    
    assert result["critical_factors"]["rainfall"] == 50.0
    assert result["critical_factors"]["river_level"] == 20.0
    assert result["critical_factors"]["drainage"] == 45.0

def test_empty_opinions():
    with pytest.raises(ValueError, match="zero opinions"):
        compute_consensus([])

def test_reasoning_length():
    opinions = [
        create_opinion(role="A"),
        create_opinion(role="B"),
        create_opinion(role="C"),
    ]
    result = compute_consensus(opinions)
    assert len(result["reasoning"]) == len(opinions) + 1
    assert result["reasoning"][-1] == result["confidence_explanation"]

import pytest
from pydantic import BaseModel
from typing import Type

from server.hazards import HAZARDS

# Helper to generate dummy data that passes basic validation
def generate_minimal_data(schema: Type[BaseModel]) -> dict:
    # Use 1 for all fields as both disease and flood use bounds that include 1 (e.g. 0-3 or 1-4)
    if hasattr(schema, "model_fields"):
        return {field_name: 1 for field_name in schema.model_fields}
    # Fallback for older pydantic
    return {field_name: 1 for field_name in schema.__fields__}

# Parametrize all tests over the registered HAZARDS
pytestmark = pytest.mark.parametrize("hazard_name, hazard", HAZARDS.items())

def test_module_attributes(hazard_name, hazard):
    """
    1. name, input_schema, knowledge_corpus_path exist and are non-empty / correct type.
    """
    assert hasattr(hazard, "name")
    assert isinstance(hazard.name, str)
    assert len(hazard.name) > 0
    
    assert hasattr(hazard, "input_schema")
    assert issubclass(hazard.input_schema, BaseModel)
    
    assert hasattr(hazard, "knowledge_corpus_path")
    assert isinstance(hazard.knowledge_corpus_path, str)
    assert len(hazard.knowledge_corpus_path) > 0

def test_personas_validity(hazard_name, hazard):
    """
    2. personas is a non-empty list; every persona has "id" and "weight" keys; 
       weights sum to 1.0 (within floating-point tolerance).
    """
    assert hasattr(hazard, "personas")
    assert isinstance(hazard.personas, list)
    assert len(hazard.personas) > 0
    
    total_weight = 0.0
    for p in hazard.personas:
        assert "id" in p
        assert "weight" in p
        total_weight += p["weight"]
        
    assert abs(total_weight - 1.0) < 0.001

def test_risk_prompts(hazard_name, hazard):
    """
    3. risk_prompts(data) — returns a list whose length equals len(personas).
    """
    data = generate_minimal_data(hazard.input_schema)
    prompts = hazard.risk_prompts(data)
    
    assert isinstance(prompts, list)
    assert len(prompts) == len(hazard.personas)

def test_deterministic_opinion(hazard_name, hazard):
    """
    4. deterministic_opinion(persona_id, data) returns exactly the expected keys.
       Also confirms an unknown persona_id raises ValueError.
    """
    data = generate_minimal_data(hazard.input_schema)
    expected_keys = {"opinion", "risk_rating", "primary_factors", "recommendation", "factor_impacts"}
    
    for p in hazard.personas:
        opinion_result = hazard.deterministic_opinion(p["id"], data)
        assert isinstance(opinion_result, dict)
        assert set(opinion_result.keys()) == expected_keys
        
    with pytest.raises(ValueError):
        hazard.deterministic_opinion("invalid_persona_id_xyz", data)

def test_resource_formulas(hazard_name, hazard):
    """
    5. resource_formulas(risk_level, population) returns a non-empty dict of non-negative values
       for "Low", "Medium", "High".
    """
    population = 100000
    for risk_level in ["Low", "Medium", "High"]:
        resources = hazard.resource_formulas(risk_level, population)
        assert isinstance(resources, dict)
        assert len(resources) > 0
        for val in resources.values():
            assert val >= 0

def test_report_context(hazard_name, hazard):
    """
    6. report_context(risk, resources, knowledge) returns a dict without raising.
    """
    risk = {"risk_level": "Medium"}
    resources = {"resource_a": 10}
    
    # Test with knowledge=None
    context_no_knowledge = hazard.report_context(risk, resources, None)
    assert isinstance(context_no_knowledge, dict)
    
    # Test with knowledge dict
    context_with_knowledge = hazard.report_context(risk, resources, {"answer": "test"})
    assert isinstance(context_with_knowledge, dict)

from server.hazards import HAZARDS
from server.agents import risk_agent

def run_assessment(hazard: str, data: dict, model: str = "gemini-2.0-flash") -> dict:
    hazard_module = HAZARDS.get(hazard)
    if hazard_module is None:
        raise ValueError(f"Unknown hazard: {hazard}")
    validated = hazard_module.input_schema(**data)
    return risk_agent.run(hazard_module, validated.model_dump(), model)

def answer_question(hazard: str, question: str, model: str = "gemini-2.0-flash") -> dict:
    from server.agents import knowledge_agent
    from server.rag.index_cache import get_or_build_index
    
    hazard_module = HAZARDS.get(hazard)
    if hazard_module is None:
        raise ValueError(f"Unknown hazard: {hazard}")
        
    index = get_or_build_index(hazard_module.name, hazard_module.knowledge_corpus_path)
    return knowledge_agent.run(question, index, model=model)

def run_full_assessment(hazard: str, data: dict, population: int, template: str, model: str, knowledge_question: str | None) -> dict:
    from server.agents import resource_agent, report_agent
    from server.rag.index_cache import get_or_build_index
    from server.agents import knowledge_agent
    
    hazard_module = HAZARDS.get(hazard)
    if hazard_module is None:
        raise ValueError(f"Unknown hazard: {hazard}")
        
    validated = hazard_module.input_schema(**data)
    
    # 1. Risk
    risk_result = risk_agent.run(hazard_module, validated.model_dump(), model)
    
    # 2. Resources
    resources_result = resource_agent.run(hazard_module, risk_level=risk_result["risk_level"], population=population)
    
    # 3. Knowledge (optional)
    knowledge_result = None
    if knowledge_question:
        index = get_or_build_index(hazard_module.name, hazard_module.knowledge_corpus_path)
        knowledge_result = knowledge_agent.run(knowledge_question, index, model=model)
        
    # 4. Report
    return report_agent.run(hazard_module, risk_result, resources_result, knowledge_result, template)

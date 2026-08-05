from server.hazards.disease import DiseaseHazard
from server.agents import resource_agent, report_agent
import json

def run_tests():
    hazard = DiseaseHazard()

    from server.agents import risk_agent
    
    # Real evidence input for disease
    evidence = {
        "Weather": 2, # Humid
        "PopulationDensity": 2, # High
        "Sanitation": 1, # Moderate
        "RecentCases": 3 # > 5k
    }
    
    # Real Risk Result (demo_mode logic triggers deterministic_opinion)
    risk_result = risk_agent.run(hazard, evidence)
    
    print("--- REAL REASONING LIST ---")
    print(json.dumps(risk_result.get("reasoning", []), indent=2))
    print("---------------------------\n")

    # Real Resource Result
    resources_result = resource_agent.run(hazard, risk_level="High", population=500000)

    # Constructed Knowledge Result
    knowledge_result = {
        "question": "What should be done during a cholera outbreak?",
        "answer": "Cholera outbreaks require rapid hydration and sanitation measures.",
        "citations": [
            {"id": "doc1", "citation": "WHO Guidelines pg 45", "text": "Rapid rehydration is key.", "score": 0.89}
        ],
        "demo_mode": True
    }

    print("--- OFFICER TEMPLATE ---")
    officer_report = report_agent.run(hazard, risk_result, resources_result, knowledge_result, "officer")
    print(json.dumps(officer_report, indent=2))

    print("\n--- CITIZEN TEMPLATE ---")
    citizen_report = report_agent.run(hazard, risk_result, resources_result, knowledge_result, "citizen")
    print(json.dumps(citizen_report, indent=2))

    print("\n--- EXECUTIVE TEMPLATE ---")
    executive_report = report_agent.run(hazard, risk_result, resources_result, knowledge_result, "executive")
    print(json.dumps(executive_report, indent=2))

if __name__ == "__main__":
    run_tests()

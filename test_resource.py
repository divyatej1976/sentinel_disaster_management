from server.hazards.disease import DiseaseHazard
from server.agents import resource_agent

if __name__ == "__main__":
    hazard = DiseaseHazard()
    
    # Test through the agent wrapper
    print("Testing via resource_agent.py wrapper...")
    resources = resource_agent.run(hazard, risk_level="High", population=500000)
    print("Resources for High risk, 500k population:")
    print(resources)
    
    # Let's also test another case
    resources_medium = resource_agent.run(hazard, risk_level="Medium", population=150000)
    print("\nResources for Medium risk, 150k population:")
    print(resources_medium)

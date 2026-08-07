from server.hazards import HAZARDS

def test_flood():
    flood = HAZARDS.get("flood")
    if not flood:
        print("Flood module not loaded!")
        return

    data = {
        "RainfallIntensity": 3,
        "RiverLevel": 3,
        "PopulationDensity": 2,
        "DrainageCapacity": 3
    }
    
    print("Testing Prompts:")
    prompts = flood.risk_prompts(data)
    print(f"Generated {len(prompts)} prompts")
    
    print("\nTesting Deterministic Opinion (Hydrologist):")
    res = flood.deterministic_opinion("hydrologist", data)
    print(res)
    
    print("\nTesting Resources (High, 200k pop):")
    resources = flood.resource_formulas("High", 200000)
    print(resources)
    
if __name__ == "__main__":
    test_flood()

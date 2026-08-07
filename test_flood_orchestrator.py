import json
from server.hazards import HAZARDS
from server.orchestrator import workflow

def test_flood_integration():
    flood = HAZARDS["flood"]
    
    # 4. Confirm personas weights sum
    weights = [p["weight"] for p in flood.personas]
    total_weight = sum(weights)
    print("--- PERSONA WEIGHTS ---")
    print(f"Weights: {weights}")
    print(f"Sum: {total_weight}")
    
    # 5. Confirm resource_formulas
    print("\n--- RESOURCE FORMULAS ---")
    pop = 150000
    res = flood.resource_formulas("Medium", pop)
    # Medium config: boats=5, shelter=250, pumps=10 (per 100k)
    # expected at 1.5 multiplier: boats=8 (ceil(7.5)), shelter=375, pumps=15
    print(f"Computed for Medium risk, {pop} population:")
    print(json.dumps(res, indent=2))
    print(f"Expected: {{'rescue_boats': 8, 'shelter_capacity': 375, 'water_pumps': 15}}")
    
    # 3. Call orchestrator entry point
    print("\n--- ORCHESTRATOR EXECUTION ---")
    data = {
        "RainfallIntensity": 3,
        "RiverLevel": 3,
        "PopulationDensity": 2,
        "DrainageCapacity": 3
    }
    
    # Run risk assessment only to see risk result
    risk_result = workflow.run_assessment("flood", data, model="gemini-2.0-flash")
    
    print("Full Risk Result:")
    print(json.dumps(risk_result, indent=2))
    
    print("\nCritical Factors Verification:")
    print("Critical Factors:", risk_result.get("critical_factors", {}))
    print("Top Risk Drivers:", risk_result.get("top_risk_drivers", []))

if __name__ == "__main__":
    test_flood_integration()

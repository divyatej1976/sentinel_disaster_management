import json
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_report_endpoint_no_population():
    # Base request payload WITHOUT population
    payload = {
        "hazard": "disease",
        "location": "Test Zone",
        "data": {
            "Weather": 2, 
            "PopulationDensity": 2,
            "Sanitation": 1,
            "RecentCases": 3
        },
        "template": "officer"
    }

    print("--- OFFICER TEMPLATE RESPONSE (DEFAULT POPULATION) ---")
    response = client.post("/api/report", json=payload)
    if response.status_code != 200:
        print(f"ERROR {response.status_code}: {response.text}")
    else:
        print(json.dumps(response.json(), indent=2))
    print("\n")

if __name__ == "__main__":
    test_report_endpoint_no_population()

import json
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_report_endpoint():
    # Base request payload
    base_payload = {
        "hazard": "disease",
        "location": "Test Zone",
        "data": {
            "Weather": 2, 
            "PopulationDensity": 2,
            "Sanitation": 1,
            "RecentCases": 3
        },
        "population": 150000,
        "include_knowledge_question": "What should be done during a cholera outbreak?"
    }

    templates = ["officer", "citizen", "executive"]

    for t in templates:
        print(f"--- {t.upper()} TEMPLATE RESPONSE ---")
        payload = base_payload.copy()
        payload["template"] = t
        
        response = client.post("/api/report", json=payload)
        if response.status_code != 200:
            print(f"ERROR {response.status_code}: {response.text}")
        else:
            print(json.dumps(response.json(), indent=2))
        print("\n")

if __name__ == "__main__":
    test_report_endpoint()

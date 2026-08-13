import requests

print("Sending Request 1...")
res1 = requests.post("http://localhost:8001/api/report", json={
    "hazard": "disease",
    "location": "Unknown",
    "data": {"Weather": 1, "PopulationDensity": 1, "Sanitation": 1, "RecentCases": 1},
    "model": "gemini-2.0-flash",
    "template": "citizen",
    "include_knowledge_question": "What is the recommended sanitation protocol?",
})
print("Report 1 Status:", res1.status_code)

print("\nSending Request 2...")
res2 = requests.post("http://localhost:8001/api/report", json={
    "hazard": "disease",
    "location": "Unknown",
    "data": {"Weather": 1, "PopulationDensity": 1, "Sanitation": 1, "RecentCases": 1},
    "model": "gemini-2.0-flash",
    "template": "citizen",
    "include_knowledge_question": "What is the recommended sanitation protocol?",
})
print("Report 2 Status:", res2.status_code)

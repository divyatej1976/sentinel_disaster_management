import logging
import sys

# Configure basic logging to see the logger.info lines from index_cache
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_ask():
    print("--- FIRST CALL ---")
    response1 = client.post("/api/ask", json={"hazard": "disease", "question": "what should be done during a cholera outbreak"})
    import json
    print(json.dumps(response1.json(), indent=2))

if __name__ == "__main__":
    test_ask()

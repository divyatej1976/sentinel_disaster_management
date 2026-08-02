import os
from typing import List, Optional

from dotenv import load_dotenv
from google import genai

load_dotenv()

raw_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY") or ""
api_key = raw_api_key.strip()
has_gemini_key = bool(api_key) and "your_gemini_api_key_here" not in api_key.lower()

client = genai.Client(api_key=api_key if has_gemini_key else " ")

def embed_texts(texts: List[str]) -> Optional[List[List[float]]]:
    """
    Uses the Gemini embedding model if has_gemini_key is true.
    Returns None if no key is configured or if embedding fails.
    """
    if not has_gemini_key:
        return None
    try:
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=texts,
        )
        return [emb.values for emb in response.embeddings]
    except Exception as e:
        print(f"Warning: embedding failed: {e}")
        return None

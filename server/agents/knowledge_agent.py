import logging
from typing import Dict, List, Any

from google.genai import types

from server.rag.retriever import retrieve
from server.rag.embeddings import has_gemini_key, client

logger = logging.getLogger("outbreak-predictor")

def _format_citation(chunk: dict) -> str:
    """
    Format citation by document title + page number.
    e.g. "According to the GOARN National Outbreak Response Handbook, page 16..."
    Section can be mentioned as supplementary color only if short.
    """
    title = chunk.get("title", chunk.get("source", "Unknown Document"))
    page = chunk.get("page", "?")
    section = chunk.get("section", "").strip()
    
    citation = f"{title}, page {page}"
    # Include a section only if it does NOT end in ':' or ',', 
    # does NOT start with a lowercase letter, and is 8 words or fewer.
    if section:
        is_valid_shape = (
            not section.endswith((':', ',')) and 
            not section[0].islower() and 
            len(section.split()) <= 8
        )
        if is_valid_shape:
            citation += f" (Section: {section})"
        
    return citation

def run(question: str, index: dict, top_k: int = 3, model: str = "gemini-2.0-flash") -> dict:
    """
    Takes a question, calls retriever.retrieve() for the top-k chunks, and generates an answer.
    If has_gemini_key is false, skips the LLM call entirely and returns the top retrieved chunks
    directly with their citations.
    """
    chunks = retrieve(index, question, top_k=top_k)
    
    if not chunks:
        return {
            "question": question,
            "answer": "No relevant information found in the knowledge base.",
            "citations": [],
            "demo_mode": not has_gemini_key
        }
        
    citations = []
    context_texts = []
    
    for i, chunk in enumerate(chunks):
        cite_text = _format_citation(chunk)
        citations.append({
            "id": chunk.get("chunk_id", str(i)),
            "citation": cite_text,
            "text": chunk.get("text", ""),
            "score": chunk.get("score", 0.0)
        })
        context_texts.append(f"[{cite_text}]\n{chunk.get('text', '')}")
        
    if not has_gemini_key:
        return {
            "question": question,
            "answer": "Demo mode active (no LLM). Returning top retrieved chunks directly.",
            "citations": citations,
            "demo_mode": True
        }
        
    references_block = ""
    for c in context_texts:
        references_block += f"--- REFERENCE ---\n{c}\n\n"
        
    prompt = f"""You are an expert disaster management AI. 
Answer the following question using ONLY the provided reference chunks.
Cite your sources in your answer using the provided citation brackets (e.g. [Document Title, page X]).
If the provided chunks do not contain enough information to answer the question, state that clearly.

Question: {question}

References:
{references_block}
"""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
            )
        )
        answer = response.text.strip()
    except Exception as exc:
        logger.warning("Knowledge agent generation failed: %s", exc)
        answer = "Error generating answer. Please review the cited chunks directly."
        
    return {
        "question": question,
        "answer": answer,
        "citations": citations,
        "demo_mode": False
    }

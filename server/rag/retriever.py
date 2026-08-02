import math
from typing import List, Dict
from server.rag.embeddings import embed_texts

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0: 
        return 0.0
    return dot / (norm_a * norm_b)

def build_index(chunks: List[Dict]) -> Dict:
    """
    Tries embed_texts() on all chunk texts. If it returns real embeddings, store them
    alongside the chunks. If None, store chunks without embeddings.
    """
    texts = [c["content"] for c in chunks]
    
    # Batch embeddings to stay within limits if corpus is large
    batch_size = 100
    all_embeddings = []
    has_failed = False
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_emb = embed_texts(batch)
        if batch_emb is None:
            has_failed = True
            break
        all_embeddings.extend(batch_emb)
        
    if has_failed or not all_embeddings:
        all_embeddings = None
        
    return {
        "chunks": chunks,
        "embeddings": all_embeddings
    }

def _tokenize(text: str) -> set:
    return set(word.strip(".,;:!?()[]{}\"'").lower() for word in text.split() if word)

def retrieve(index: Dict, query: str, top_k: int = 3) -> List[Dict]:
    """
    If the index has embeddings: rank chunks by cosine similarity.
    If the index has no embeddings (demo mode): rank chunks by simple keyword overlap.
    """
    chunks = index.get("chunks", [])
    embeddings = index.get("embeddings")
    
    scored_chunks = []
    
    if embeddings is not None:
        query_emb_list = embed_texts([query])
        if query_emb_list:
            query_emb = query_emb_list[0]
            for i, chunk in enumerate(chunks):
                score = cosine_similarity(query_emb, embeddings[i])
                scored_chunks.append((score, chunk))
        else:
            embeddings = None
            
    if embeddings is None:
        # Keyword fallback
        query_tokens = _tokenize(query)
        for chunk in chunks:
            chunk_tokens = _tokenize(chunk["content"])
            overlap = query_tokens.intersection(chunk_tokens)
            if len(chunk_tokens) == 0:
                score = 0.0
            else:
                score = len(overlap) / len(chunk_tokens)
            scored_chunks.append((score, chunk))
            
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for score, chunk in scored_chunks[:top_k]:
        res = chunk.copy()
        res["score"] = score
        results.append(res)
        
    return results

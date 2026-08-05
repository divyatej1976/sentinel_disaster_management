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
    texts = [c["text"] for c in chunks]
    
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

STOPWORDS = {
    "how", "does", "is", "are", "the", "a", "an", "of", "in", "to", "and", "or", 
    "that", "this", "what", "when", "where", "which", "who", "why", "will", "with",
    "for", "on", "as", "by", "at", "it", "be", "from", "can", "was", "were"
}

def _tokenize(text: str) -> set:
    tokens = set()
    for word in text.split():
        clean_word = word.strip(".,;:!?()[]{}\"'").lower()
        if clean_word and clean_word not in STOPWORDS:
            tokens.add(clean_word)
    return tokens

def retrieve(index: Dict, query: str, top_k: int = 3) -> List[Dict]:
    """
    If the index has embeddings: rank chunks by cosine similarity.
    If the index has no embeddings (demo mode): rank chunks by simple keyword overlap.
    Note: Acronym/synonym expansion (e.g. NDMA -> National Disaster Management Authority)
    is an accepted limitation of the demo mode fallback and is left to real embeddings.
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
            chunk_tokens = _tokenize(chunk["text"])
            overlap = query_tokens.intersection(chunk_tokens)
            # Score is primarily raw overlap count. We add a tiny decimal based on 
            # inverse chunk length as a tiebreaker so shorter chunks win ties.
            raw_overlap = len(overlap)
            tiebreaker = 1.0 / (len(chunk_tokens) + 1)
            score = float(raw_overlap) + tiebreaker
            scored_chunks.append((score, chunk))
            
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for score, chunk in scored_chunks[:top_k]:
        res = chunk.copy()
        res["score"] = score
        results.append(res)
        
    return results

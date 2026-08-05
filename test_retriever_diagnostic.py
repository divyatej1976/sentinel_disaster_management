import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document
from server.rag.retriever import build_index, retrieve, _tokenize

def test():
    print("Loading corpus...")
    pages = load_disease_corpus()
    
    docs = defaultdict(list)
    for p in pages:
        docs[p["source"]].append(p)
        
    all_chunks = []
    for source, doc_pages in docs.items():
        chunks = chunk_document(doc_pages)
        all_chunks.extend(chunks)
        
    print("Building index...")
    index = build_index(all_chunks)
    
    chunks = index["chunks"]
    print("\n" + "="*80)
    print("=== 1. Chunk Count by Source ===")
    counts = defaultdict(int)
    for c in chunks:
        counts[c["source"]] += 1
    for source, count in counts.items():
        print(f"{source}: {count} chunks")
        
    print("\n" + "="*80)
    print("=== 2. Top-5 Results & Target Chunk Score ===")
    
    queries_tests = [
        {
            "query": "what should be done during a cholera outbreak",
            "target_chunk_id": "who_managing_epidemics.pdf:106:0"
        },
        {
            "query": "how does NDMA coordinate international response",
            "target_chunk_id": "ndma_biological_disasters.pdf:95:0"
        }
    ]
    
    for qt in queries_tests:
        query = qt["query"]
        target_id = qt["target_chunk_id"]
        
        print("\n" + "-"*80)
        print(f"Query: {query}")
        query_tokens = _tokenize(query)
        print(f"Query Tokens: {query_tokens}")
        
        scored_chunks = []
        for chunk in chunks:
            chunk_tokens = _tokenize(chunk["content"])
            overlap = query_tokens.intersection(chunk_tokens)
            raw_overlap = len(overlap)
            tiebreaker = 1.0 / (len(chunk_tokens) + 1)
            score = float(raw_overlap) + tiebreaker
            scored_chunks.append({
                "chunk": chunk,
                "score": score,
                "raw_overlap": raw_overlap,
                "chunk_len": len(chunk_tokens),
                "overlap_tokens": overlap
            })
            
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        
        print("\nTop 5 Results:")
        for i in range(5):
            res = scored_chunks[i]
            c = res["chunk"]
            print(f"[{i+1}] Score: {res['score']:.4f} | Chunk: {c['chunk_id']}")
            print(f"    Raw match words: {res['raw_overlap']} / {res['chunk_len']}")
            print(f"    Matched tokens: {res['overlap_tokens']}")
            
        print(f"\nTarget Chunk Ranking ({target_id}):")
        target_rank = -1
        target_res = None
        for i, res in enumerate(scored_chunks):
            if res["chunk"]["chunk_id"] == target_id:
                target_rank = i + 1
                target_res = res
                break
                
        if target_res:
            print(f"Rank: {target_rank}")
            print(f"Score: {target_res['score']:.4f} | Chunk: {target_res['chunk']['chunk_id']}")
            print(f"Raw match words: {target_res['raw_overlap']} / {target_res['chunk_len']}")
            print(f"Matched tokens: {target_res['overlap_tokens']}")
        else:
            print("Target chunk not found in index.")
    
if __name__ == "__main__":
    test()

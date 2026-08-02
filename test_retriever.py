import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document
from server.rag.retriever import build_index, retrieve
from server.rag.embeddings import has_gemini_key

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
        
    print(f"Loaded {len(all_chunks)} total chunks.")
    
    print("Building index...")
    index = build_index(all_chunks)
    
    if index["embeddings"]:
        print("\n=> MODE: REAL EMBEDDINGS (GEMINI_API_KEY is set and working)")
    else:
        print("\n=> MODE: DEMO (KEYWORD FALLBACK)")
        
    queries = [
        "what should be done during a cholera outbreak",
        "how does NDMA coordinate international response"
    ]
    
    for q in queries:
        print("\n" + "="*80)
        print(f"Query: {q}")
        results = retrieve(index, q, top_k=3)
        for i, res in enumerate(results):
            preview = res['content'].replace('\n', ' ')[:100]
            print(f"[{i+1}] Score: {res['score']:.4f} | Chunk ID: {res['chunk_id']}")
            print(f"    Source: {res['source']} (Page {res['page']})")
            print(f"    Text: {preview}...")

if __name__ == "__main__":
    test()

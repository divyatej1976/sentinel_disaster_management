import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document

def main():
    pages = load_disease_corpus()
    docs = defaultdict(list)
    for p in pages:
        docs[p["source"]].append(p)
        
    all_chunks = []
    for source, doc_pages in docs.items():
        chunks = chunk_document(doc_pages)
        all_chunks.extend(chunks)
        
    target_ids = {
        "who_managing_epidemics.pdf:223:0",
        "ndma_biological_disasters.pdf:68:0",
        "ndma_biological_disasters.pdf:94:0"
    }
    
    for c in all_chunks:
        if c["chunk_id"] in target_ids:
            print("\n" + "="*80)
            print(f"--- Chunk ID: {c['chunk_id']} ---")
            print(f"Section: {c['section']}")
            print(f"Source: {c['source']} (Page {c['page']})")
            print("Full Text:")
            print(c["content"])

if __name__ == "__main__":
    main()

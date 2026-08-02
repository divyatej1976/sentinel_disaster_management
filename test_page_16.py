import sys
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document

def test():
    print("Loading corpus...")
    pages = load_disease_corpus()
    
    # Extract goarn pages
    goarn_pages = [p for p in pages if "goarn" in p["source"].lower()]
    
    chunks = chunk_document(goarn_pages, target_tokens=400, overlap_tokens=80)
    
    print("\n" + "="*80)
    print("=== GOARN Page 16 Verification ===")
    
    page_16_chunks = [c for c in chunks if c["page"] == 16]
    
    if not page_16_chunks:
        print("No chunks found for physical page index 16.")
    
    for c in page_16_chunks:
        print(f"\n--- Chunk ID: {c['chunk_id']} ---")
        print(f"Section: {c['section']}")
        print(f"Length: {len(c['content'].split())} words")
        print("Content:")
        print(c["content"])

if __name__ == "__main__":
    test()

import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document

def test():
    print("Loading corpus...")
    pages = load_disease_corpus()
    
    docs = defaultdict(list)
    for p in pages:
        docs[p["source"]].append(p)
        
    print(f"\nLoaded {len(docs)} documents.")
    
    for source, doc_pages in docs.items():
        print(f"\n" + "="*80)
        print(f"=== Document: {source} ===")
        
        chunks = chunk_document(doc_pages, target_tokens=400, overlap_tokens=80)
        
        if not chunks:
            print("No chunks produced.")
            continue
            
        total_chunks = len(chunks)
        avg_size = sum(len(c["content"].split()) for c in chunks) / total_chunks
        
        print(f"Total Pages Input: {len(doc_pages)}")
        print(f"Total Chunks Output: {total_chunks}")
        print(f"Average Chunk Size: {avg_size:.1f} words")
        print("\nExample Chunks (showing overlap):")
        
        # show chunk :0 (the very first surviving chunk)
        first_chunk = None
        for c in chunks:
            if c["chunk_id"].endswith(":0"):
                first_chunk = c
                break
                
        if first_chunk is not None:
            c = first_chunk
            print(f"\n--- First Surviving Chunk ID: {c['chunk_id']} ---")
            print(f"Section: {c['section']}")
            print(f"Length: {len(c['content'].split())} words")
            print("Content Preview:")
            content = c["content"]
            words = content.split()
            if len(words) > 80:
                preview = " ".join(words[:40]) + "\n[ ... ]\n" + " ".join(words[-40:])
            else:
                preview = content
            print(preview)
        else:
            print("No chunks found.")

if __name__ == "__main__":
    test()

import sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document
from server.rag.retriever import build_index
from server.agents.knowledge_agent import run

def test():
    print("Loading corpus and building index...")
    pages = load_disease_corpus()
    
    docs = defaultdict(list)
    for p in pages:
        docs[p["source"]].append(p)
        
    all_chunks = []
    for source, doc_pages in docs.items():
        chunks = chunk_document(doc_pages)
        all_chunks.extend(chunks)
        
    index = build_index(all_chunks)
    
    question = "what should be done during a cholera outbreak"
    print(f"\nQuestion: {question}")
    
    result = run(question, index)
    
    print("\n=== Answer ===")
    print(result["answer"])
    
    print("\n=== Citations ===")
    for c in result["citations"]:
        print(f"- {c['citation']} (Score: {c['score']:.4f})")
        print(f"  Preview: {c['text'][:100]}...")

if __name__ == "__main__":
    test()

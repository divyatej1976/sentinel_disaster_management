from server.hazards.disease import DiseaseHazard
from server.rag.index_cache import get_or_build_index
from server.rag.retriever import retrieve
import json

def run_retrieval():
    hazard_module = DiseaseHazard()
    index = get_or_build_index(hazard_module.name, hazard_module.knowledge_corpus_path)
    question = "What should be done during a cholera outbreak?"
    chunks = retrieve(index, question)
    
    # We want to print the raw chunk dicts, every field, unformatted
    for c in chunks:
        print(json.dumps(c, indent=2))

if __name__ == "__main__":
    run_retrieval()

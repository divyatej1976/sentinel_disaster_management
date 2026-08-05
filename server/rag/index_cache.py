from typing import Dict, Any
from server.rag.loader import load_disease_corpus
from server.rag.chunker import chunk_document
from server.rag.retriever import build_index
import logging

logger = logging.getLogger("outbreak-predictor")

# Cache to store built index for each hazard by name
_INDEX_CACHE: Dict[str, dict] = {}

def get_or_build_index(hazard_name: str, corpus_path: str) -> dict:
    """
    Returns the cached index for the given hazard if it exists.
    Otherwise, builds it (load -> chunk -> build_index), caches it, and returns it.
    """
    if hazard_name in _INDEX_CACHE:
        logger.info(f"Reusing cached index for hazard: {hazard_name}")
        return _INDEX_CACHE[hazard_name]
        
    logger.info(f"Building index for hazard: {hazard_name} from {corpus_path}...")
    
    # Currently hardcoded to use disease loader, but ideally would map
    # loaders dynamically based on hazard or use a generic loader
    if hazard_name == "disease":
        pages = load_disease_corpus(corpus_path)
    else:
        # Fallback or generic logic if we add more hazards in the future
        pages = []
        
    chunks = chunk_document(pages)
    index = build_index(chunks)
    
    _INDEX_CACHE[hazard_name] = index
    logger.info(f"Successfully cached index for hazard: {hazard_name} (Total chunks: {len(chunks)})")
    
    return index

"""
Manifest for the disease corpus.

Defines the first physical page (1-based index) of actual content for each curated PDF document.
These values were manually verified against real document content (e.g., chapter/part openings),
not inferred heuristically. See ARCHITECTURE.md section 7 (RAG grounding) for curation details.
"""

CONTENT_START_PAGE = {
    "ndma_biological_disasters.pdf": 33,
    "who_managing_epidemics.pdf": 11,
    "goarn_national_outbreak_response_handbook.pdf": 11,
}

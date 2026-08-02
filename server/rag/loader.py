import os
import fitz
from collections import defaultdict
from server.rag.corpus_manifest import CONTENT_START_PAGE

def extract_chunks_from_pdf(filepath: str) -> list[dict]:
    """
    Parses a PDF and extracts text per page, preserving metadata.
    Attempts to identify basic section headings, with 2-pass boilerplate filtering.
    """
    doc = fitz.open(filepath)
    title = doc.metadata.get("title")
    filename = os.path.basename(filepath)
    
    if filename not in CONTENT_START_PAGE:
        print(f"WARNING: Document '{filename}' is not in corpus_manifest.py. Skipping entirely to enforce manual curation.")
        return []
        
    start_page_index = CONTENT_START_PAGE[filename] - 1
    
    if not title:
        title = os.path.splitext(filename)[0].replace("_", " ").title()
        
    num_pages = len(doc)
    
    # --- Pass 1: Build frequent lines set for margin and body ---
    margin_page_counts = defaultdict(set)
    body_page_counts = defaultdict(set)
    
    pages_blocks = []
    page_heights = []
    
    for page_num in range(start_page_index, num_pages):
        page = doc.load_page(page_num)
        page_height = page.rect.height
        page_heights.append(page_height)
        
        blocks = page.get_text("dict").get("blocks", [])
        pages_blocks.append(blocks)
        
        for b in blocks:
            if b.get("type") == 0:
                for l in b.get("lines", []):
                    bbox = l.get("bbox", (0, 0, 0, 0))
                    # Check if line center is in top 10% or bottom 10% of page
                    y_center = (bbox[1] + bbox[3]) / 2.0
                    is_margin = (y_center < page_height * 0.1) or (y_center > page_height * 0.9)
                    
                    line_text = "".join(s.get("text", "") for s in l.get("spans", []))
                    normalized = line_text.strip()
                    if normalized:
                        if is_margin:
                            margin_page_counts[normalized].add(page_num)
                        else:
                            body_page_counts[normalized].add(page_num)
                            
    frequent_margin_lines = set()
    frequent_body_lines = set()
    
    margin_threshold = num_pages * 0.15
    body_threshold = num_pages * 0.4
    
    for line, pages in margin_page_counts.items():
        if len(pages) > margin_threshold:
            frequent_margin_lines.add(line)
            
    for line, pages in body_page_counts.items():
        if len(pages) > body_threshold:
            frequent_body_lines.add(line)
            
    # --- Pass 2: Process pages with filtering ---
    chunks = []
    current_section = "Introduction"
    
    for idx, blocks in enumerate(pages_blocks):
        page_num = start_page_index + idx
        page_height = page_heights[idx]
        page_lines = []
        for b_idx, b in enumerate(blocks):
            if b.get("type") == 0:
                for l in b.get("lines", []):
                    bbox = l.get("bbox", (0, 0, 0, 0))
                    y_center = (bbox[1] + bbox[3]) / 2.0
                    is_margin = (y_center < page_height * 0.1) or (y_center > page_height * 0.9)
                    
                    spans = l.get("spans", [])
                    line_text = "".join(s.get("text", "") for s in spans)
                    normalized = line_text.strip()
                    if normalized:
                        is_frequent = (normalized in frequent_margin_lines) if is_margin else (normalized in frequent_body_lines)
                        page_lines.append({
                            "block_idx": b_idx,
                            "text": line_text,
                            "normalized": normalized,
                            "spans": spans,
                            "is_margin": is_margin,
                            "is_frequent": is_frequent
                        })
                        
        filtered_lines = []
        i = 0
        while i < len(page_lines):
            if page_lines[i]["is_frequent"]:
                run_length = 0
                j = i
                band_type = page_lines[i]["is_margin"]
                # The contiguous-run stripping logic applies within each band separately
                while j < len(page_lines) and page_lines[j]["is_frequent"] and page_lines[j]["is_margin"] == band_type:
                    run_length += 1
                    j += 1
                    
                # We use min_run=2 for both to strictly respect "only strip contiguous multi-line runs"
                # as requested, which applies within each band separately.
                if run_length >= 2 or band_type: # For margins, strip single frequent lines too (headers/footers are often 1 line)
                    i = j
                    continue
                else:
                    filtered_lines.append(page_lines[i])
                    i += 1
            else:
                filtered_lines.append(page_lines[i])
                i += 1
                
        page_text = []
        current_block_idx = -1
        block_text = ""
        
        for line in filtered_lines:
            for s in line["spans"]:
                clean_text = s.get("text", "").strip()
                if clean_text:
                    is_bold = "bold" in s.get("font", "").lower()
                    size = s.get("size", 10)
                    if (size > 11.5 or is_bold) and len(clean_text) < 100:
                        if not clean_text.isdigit():
                            current_section = clean_text
                            
            if line["block_idx"] != current_block_idx:
                if block_text.strip():
                    page_text.append(block_text.strip())
                block_text = line["text"]
                current_block_idx = line["block_idx"]
            else:
                block_text += "\n" + line["text"]
                
        if block_text.strip():
            page_text.append(block_text.strip())
            
        content = "\n\n".join(page_text)
        
        # --- Quality filter ---
        alnum_count = sum(c.isalnum() for c in content)
        if alnum_count < 50:
            print(f"Skipping {filename} page {page_num + 1} (alnum count {alnum_count} < 50)")
            continue
            
        if content.strip():
            chunks.append({
                "source": filename,
                "title": title,
                "section": current_section,
                "page": page_num + 1,
                "content": content
            })
            
    return chunks

def load_disease_corpus() -> list[dict]:
    """
    Loads all real PDF documents in the disease knowledge corpus.
    Returns a list of chunk dictionaries containing page-level text and metadata.
    """
    # Use relative path from the project root (where main.py typically runs)
    data_dir = os.path.join("server", "data", "knowledge", "disease")
    all_chunks = []
    
    if not os.path.exists(data_dir):
        return all_chunks
        
    for file in os.listdir(data_dir):
        if file.lower().endswith(".pdf"):
            filepath = os.path.join(data_dir, file)
            chunks = extract_chunks_from_pdf(filepath)
            all_chunks.extend(chunks)
            
    return all_chunks

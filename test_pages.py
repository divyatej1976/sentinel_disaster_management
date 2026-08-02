import sys
import os
import fitz
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

def diagnostic_extract():
    filepath = os.path.join("server", "data", "knowledge", "disease", "goarn_national_outbreak_response_handbook.pdf")
    doc = fitz.open(filepath)
    num_pages = len(doc)
    
    # Pass 1
    margin_page_counts = defaultdict(set)
    body_page_counts = defaultdict(set)
    pages_blocks = []
    page_heights = []
    
    for page_num in range(num_pages):
        page = doc.load_page(page_num)
        page_height = page.rect.height
        page_heights.append(page_height)
        blocks = page.get_text("dict").get("blocks", [])
        pages_blocks.append(blocks)
        for b in blocks:
            if b.get("type") == 0:
                for l in b.get("lines", []):
                    bbox = l.get("bbox", (0, 0, 0, 0))
                    y_center = (bbox[1] + bbox[3]) / 2.0
                    is_margin = (y_center < page_height * 0.1) or (y_center > page_height * 0.9)
                    line_text = "".join(s.get("text", "") for s in l.get("spans", []))
                    normalized = line_text.strip()
                    if normalized:
                        if is_margin: margin_page_counts[normalized].add(page_num)
                        else: body_page_counts[normalized].add(page_num)
                        
    frequent_margin_lines = set(line for line, pages in margin_page_counts.items() if len(pages) > num_pages * 0.15)
    frequent_body_lines = set(line for line, pages in body_page_counts.items() if len(pages) > num_pages * 0.4)
    
    print("="*80)
    print("=== GOARN Physical Pages 1-15 Diagnostic ===")
    
    # Pass 2 - strictly using the first 15 pages in loop order
    for page_num in range(15):
        blocks = pages_blocks[page_num]
        page_height = page_heights[page_num]
        page_lines = []
        
        raw_text = doc.load_page(page_num).get_text("text").strip()
        raw_preview = raw_text[:80].replace("\n", " ")
        
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
                while j < len(page_lines) and page_lines[j]["is_frequent"] and page_lines[j]["is_margin"] == band_type:
                    run_length += 1
                    j += 1
                if run_length >= 2 or band_type:
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
        alnum_count = sum(c.isalnum() for c in content)
        
        status = "KEPT"
        reason = ""
        if alnum_count < 50:
            status = "SKIPPED"
            reason = f"(alnum count {alnum_count} < 50)"
        
        # Use 1-based indexing for humans (e.g. physical page 1)
        print(f"Physical Page Index: {page_num + 1} | Status: {status} {reason}")
        print(f"Raw preview: {raw_preview}")
        print("-" * 80)

diagnostic_extract()

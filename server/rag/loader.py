import os
import fitz

def extract_chunks_from_pdf(filepath: str) -> list[dict]:
    """
    Parses a PDF and extracts text per page, preserving metadata.
    Attempts to identify basic section headings.
    """
    doc = fitz.open(filepath)
    title = doc.metadata.get("title")
    filename = os.path.basename(filepath)
    
    if not title:
        # Fallback to filename without extension
        title = os.path.splitext(filename)[0].replace("_", " ").title()
        
    chunks = []
    current_section = "Introduction"
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # get_text("dict") provides detailed font and size info needed for headings
        blocks = page.get_text("dict").get("blocks", [])
        
        page_text = []
        for b in blocks:
            if b.get("type") == 0:  # text block
                block_text = ""
                for l in b.get("lines", []):
                    for s in l.get("spans", []):
                        text = s.get("text", "")
                        clean_text = text.strip()
                        
                        if clean_text:
                            # Heuristic: Text is a heading if it's bold or significantly larger than body text (usually ~10pt),
                            # and is short enough (not a whole paragraph). 
                            is_bold = "bold" in s.get("font", "").lower()
                            size = s.get("size", 10)
                            
                            if (size > 11.5 or is_bold) and len(clean_text) < 100:
                                # Exclude standalone numbers (like page numbers) from becoming sections
                                if not clean_text.isdigit():
                                    current_section = clean_text
                                    
                        block_text += text
                
                # Append cleaned block text
                if block_text.strip():
                    page_text.append(block_text.strip())
                    
        content = "\n\n".join(page_text)
        
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

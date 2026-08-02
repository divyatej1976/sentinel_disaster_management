def chunk_document(pages: list[dict], target_tokens: int = 400, overlap_tokens: int = 80) -> list[dict]:
    """
    Splits page text into chunks of approximately `target_tokens` words,
    with `overlap_tokens` words of overlap between consecutive chunks.
    Does not merge text across pages, preserving page-level metadata.
    """
    chunks = []
    
    for page in pages:
        source = page.get("source")
        title = page.get("title")
        section = page.get("section")
        page_num = page.get("page")
        content = page.get("content", "")
        
        words = content.split()
        
        if not words:
            continue
            
        step = target_tokens - overlap_tokens
        if step <= 0:
            step = target_tokens
            
        index_within_page = 0
        for i in range(0, len(words), step):
            chunk_words = words[i:i + target_tokens]
            chunk_content = " ".join(chunk_words)
            
            alnum_count = sum(c.isalnum() for c in chunk_content)
            if alnum_count < 50:
                print(f"Skipping chunk {source}:{page_num}:{index_within_page} (alnum count {alnum_count} < 50)")
            else:
                chunks.append({
                    "source": source,
                    "title": title,
                    "section": section,
                    "page": page_num,
                    "chunk_id": f"{source}:{page_num}:{index_within_page}",
                    "content": chunk_content
                })
                
            index_within_page += 1
            if i + target_tokens >= len(words):
                break
                
    return chunks

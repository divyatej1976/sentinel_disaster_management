import sys
import os
import fitz

sys.stdout.reconfigure(encoding='utf-8')

def diagnostic_pages(filename, num_pages_to_check):
    filepath = os.path.join("server", "data", "knowledge", "disease", filename)
    doc = fitz.open(filepath)
    
    print("="*80)
    print(f"=== {filename} Physical Pages 1-{num_pages_to_check} Diagnostic ===")
    
    for page_num in range(min(num_pages_to_check, len(doc))):
        raw_text = doc.load_page(page_num).get_text("text").strip()
        raw_preview = raw_text[:80].replace("\n", " ")
        print(f"Physical Page Index: {page_num + 1}")
        print(f"Raw preview: {raw_preview}")
        print("-" * 80)

diagnostic_pages("ndma_biological_disasters.pdf", 40)
print("\n")
diagnostic_pages("who_managing_epidemics.pdf", 20)

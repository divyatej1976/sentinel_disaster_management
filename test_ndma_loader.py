import sys
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus

chunks = load_disease_corpus()
ndma_chunks = [c for c in chunks if "ndma" in c["source"].lower()]

if not ndma_chunks:
    print("No NDMA chunks found.")
    exit()

print("\n" + "="*80)
print("=== 1. Text-heavy content page ===")
for c in ndma_chunks:
    # Skip early pages which might be TOC/Foreword/Abbreviations
    if c["page"] > 35 and len(c["content"]) > 1500:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== 2. Title/cover page ===")
for c in ndma_chunks:
    if c["page"] in (1, 2, 3):
        # Let's print the first page that actually has text
        if len(c["content"]) > 20:
            print(f"Source: {c['source']}")
            print(f"Title: {c['title']}")
            print(f"Section: {c['section']}")
            print(f"Page: {c['page']}")
            print("-" * 40)
            print(c['content'])
            break

print("\n" + "="*80)
print("=== 3. Middle page ===")
middle_page_num = len(ndma_chunks) // 2
for c in ndma_chunks:
    if c["page"] >= middle_page_num:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

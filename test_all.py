import sys
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus

# The quality filter logs will print automatically from load_disease_corpus
chunks = load_disease_corpus()

print("\n" + "="*80)
print("=== NDMA PAGE 95 ===")
for c in chunks:
    if "ndma" in c["source"].lower() and c["page"] == 95:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== NDMA COVER PAGE (1-3) ===")
ndma_cover = [c for c in chunks if "ndma" in c["source"].lower() and c["page"] in (1, 2, 3)]
if not ndma_cover:
    print("SUCCESS: Cover pages (1-3) were correctly skipped by the quality filter!")
else:
    for c in ndma_cover:
        print(f"FAILURE: Found page {c['page']} which should have been skipped:\n{c['content']}")

print("\n" + "="*80)
print("=== GOARN PAGE 16 ===")
for c in chunks:
    if "goarn" in c["source"].lower() and c["page"] == 16:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== GOARN 'Background' Page (Page 5) ===")
# Use page 5 based on previous output
for c in chunks:
    if "goarn" in c["source"].lower() and c["page"] == 5:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== Managing Epidemics PAGE 23 ===")
for c in chunks:
    if "epidemics" in c["source"].lower() and c["page"] == 23:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

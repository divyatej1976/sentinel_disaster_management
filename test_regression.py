import sys
sys.stdout.reconfigure(encoding='utf-8')

from server.rag.loader import load_disease_corpus

chunks = load_disease_corpus()

print("\n" + "="*80)
print("=== 1. Epidemics Page 23 Mismatch Verification ===")
for c in chunks:
    if "epidemics" in c["source"].lower() and c["page"] == 23:
        print(f"Source: {c['source']} | Physical Page Index: {c['page']}")
        print(f"Section: {c['section']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== 2. NDMA Page 95 Mismatch Verification ===")
for c in chunks:
    if "ndma" in c["source"].lower() and c["page"] == 95:
        print(f"Source: {c['source']} | Physical Page Index: {c['page']}")
        print(f"Section: {c['section']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== 3. GOARN Page 16 Mismatch Verification ===")
for c in chunks:
    if "goarn" in c["source"].lower() and c["page"] == 16:
        print(f"Source: {c['source']} | Physical Page Index: {c['page']}")
        print(f"Section: {c['section']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== 4. GOARN 'Background' Survival (Real Content) ===")
background_chunks = [c for c in chunks if "goarn" in c["source"].lower() and c["section"] == "Background"]
for c in background_chunks:
    print(f"Source: {c['source']} | Physical Page Index: {c['page']}")
    print(f"Section: {c['section']}")
    print("-" * 40)
    print(c['content'])
    print("="*40)


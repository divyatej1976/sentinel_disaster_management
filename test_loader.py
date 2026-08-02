from server.rag.loader import load_disease_corpus

chunks = load_disease_corpus()

print("\n" + "="*80)
print("=== 1. Text-heavy page with 'Background' ===")
for c in chunks:
    # Match any page that has "Background" as its section or early in the content and is text-heavy
    if "Background" in c["section"] or "Background" in c["content"][:200]:
        if len(c["content"]) > 1000:
            print(f"Source: {c['source']}")
            print(f"Title: {c['title']}")
            print(f"Section: {c['section']}")
            print(f"Page: {c['page']}")
            print("-" * 40)
            print(c['content'])
            break

print("\n" + "="*80)
print("=== 2. 'Document at a glance' diagram page ===")
for c in chunks:
    if "goarn" in c["source"].lower() and "document at a glance" in c["content"].lower():
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

print("\n" + "="*80)
print("=== 3. Middle page with navigation strip ===")
for c in chunks:
    content_lower = c["content"].lower()
    if "goarn" in c["source"].lower() and "rcce" in content_lower and "ipc" in content_lower and "lab" in content_lower and c["page"] > 15:
        print(f"Source: {c['source']}")
        print(f"Title: {c['title']}")
        print(f"Section: {c['section']}")
        print(f"Page: {c['page']}")
        print("-" * 40)
        print(c['content'])
        break

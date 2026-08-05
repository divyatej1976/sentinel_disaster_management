import fitz
import os

filepath = "server/data/knowledge/disease/who_managing_epidemics.pdf"
doc = fitz.open(filepath)

# test_ask output gave ID who_managing_epidemics.pdf:223:0, which implies page_num+1 = 223 -> page_num = 222
page_num = 222 
page = doc.load_page(page_num)

blocks = page.get_text("dict").get("blocks", [])

print("--- Raw Spans containing 'dif' or 'cult' ---")
for b in blocks:
    if b.get("type") == 0:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                raw_text = s.get("text", "")
                if "dif" in raw_text or "cult" in raw_text or "\ufb01" in raw_text:
                    print(ascii(raw_text))

doc.close()

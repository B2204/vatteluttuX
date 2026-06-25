"""
Script to extract Vatteluttu to Modern Tamil character mappings from the PDF.
"""
import fitz
import json
import re

def extract_mappings():
    doc = fitz.open(r'F:\final mca project\VattalettuX\docs\247-vattelettukal.pdf')
    
    mappings = []
    
    for i, page in enumerate(doc):
        text = page.get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # Find the key mapping line - usually contains Brahmi + Tamil
        tamil_chars = []
        for line in lines:
            # Skip common header lines
            if line in ['தமிழ்', 'வட்டெழுத்து', 'எழுத்து', 'தமிழ் எழுத்து']:
                continue
            if ':' in line or line.replace('.', '').replace(' ', '').isdigit():
                continue
            # Check if line contains meaningful characters (not just spaces/numbers)
            meaningful = [c for c in line if ord(c) > 127]
            if meaningful:
                tamil_chars.append(line)
        
        if tamil_chars:
            mappings.append({
                'page': i + 1,
                'raw_content': tamil_chars
            })
    
    # Save all raw data for analysis
    with open(r'F:\final mca project\VattalettuX\docs\raw_mappings.json', 'w', encoding='utf-8') as f:
        json.dump(mappings, f, ensure_ascii=False, indent=2)
    
    # Also create a readable text file
    with open(r'F:\final mca project\VattalettuX\docs\mappings_readable.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total pages with content: {len(mappings)}\n\n")
        for m in mappings:
            f.write(f"Page {m['page']:3d}: {m['raw_content']}\n")
    
    print("Extraction complete! Check raw_mappings.json and mappings_readable.txt")

if __name__ == "__main__":
    extract_mappings()


import re

f = r'f:\final mca project\VattalettuX\docs\MCA_Project_Report_BHC_April2026.md'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Replace special Unicode with ASCII equivalents
replacements = {
    '\u2014': ' - ',    # em dash -> hyphen with spaces
    '\u2013': '-',      # en dash -> hyphen
    '\u2019': "'",      # right single quote -> apostrophe
    '\u2018': "'",      # left single quote -> apostrophe
    '\u201c': '"',      # left double quote
    '\u201d': '"',      # right double quote
    '\u00d7': 'x',      # multiplication sign
    '\u03b2': 'beta',   # beta symbol
    '\u03b5': 'epsilon', # epsilon
}

for old, new in replacements.items():
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"Replaced {count} instances of U+{ord(old):04X} with '{new}'")

# Write with UTF-8 BOM for proper editor detection
with open(f, 'w', encoding='utf-8-sig') as fh:
    fh.write(content)

print("Done! File saved with UTF-8 BOM encoding.")

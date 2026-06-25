"""Scan a Vatteluttu inscription image through the OCR API."""
import requests
import sys
import os

# Image path
image_path = r"C:\Users\Asus\Downloads\Vatteluttu (1).jpg"
if len(sys.argv) > 1:
    image_path = sys.argv[1]

if not os.path.exists(image_path):
    print(f"Image not found: {image_path}")
    sys.exit(1)

print(f"Scanning: {image_path}")
print("=" * 60)

# Send to API
with open(image_path, 'rb') as f:
    ext = os.path.splitext(image_path)[1].lower()
    mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
    r = requests.post(
        'http://127.0.0.1:8000/recognize',
        files={'image': (os.path.basename(image_path), f, mime)}
    )

if r.status_code != 200:
    print(f"Error: {r.status_code} - {r.text}")
    sys.exit(1)

d = r.json()

print(f"Characters detected: {len(d.get('characters', []))}")
print(f"Words detected: {len(d.get('words', []))}")
print()

# Character details
print("Character Predictions:")
print("-" * 60)
for i, c in enumerate(d.get('characters', [])):
    tamil = c.get('modern_tamil', '?')
    label = c.get('label', '?')
    conf = c.get('confidence', 0)
    pos = c.get('position', [0, 0])
    bbox = c.get('bounding_box', [0, 0, 0, 0])
    print(f"  #{i+1}: {label} -> conf={conf:.1%}  pos=({pos[0]},{pos[1]})  size={bbox[2]}x{bbox[3]}")

print()

# Word details
print("Word Predictions:")
print("-" * 60)
for i, w in enumerate(d.get('words', [])):
    text = w.get('text', '?')
    nc = w.get('num_chars', 0)
    conf = w.get('confidence', 0)
    labels = w.get('character_labels', [])
    print(f"  Word {i+1}: chars={nc}  conf={conf:.1%}  labels={labels}")

print()

# Full text
print("Recognized Text:")
print("-" * 60)
modern = d.get('modern_text', '')
print(f"  {repr(modern)}")

print()

# Warnings
warns = d.get('warnings', [])
if warns:
    print(f"Warnings ({len(warns)}):")
    for w in warns:
        print(f"  - {w}")

"""Quick test to verify database save works after the fix."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests

# Send a test image for OCR
print("1. Sending image for OCR recognition...")
with open("test_word_image.png", "rb") as f:
    r = requests.post(
        "http://localhost:8000/recognize",
        files={"image": ("test.png", f, "image/png")}
    )

print(f"   Status: {r.status_code}")
if r.ok:
    data = r.json()
    print(f"   Modern text: {data.get('modern_text', 'N/A')}")
    print(f"   Characters: {data.get('num_characters', 0)}")
else:
    print(f"   Error: {r.text}")

# Check history
print("\n2. Checking history from /history endpoint...")
r2 = requests.get("http://localhost:8000/history")
print(f"   Status: {r2.status_code}")
if r2.ok:
    history = r2.json()
    print(f"   Total records in DB: {len(history)}")
    for item in history:
        print(f"   - ID {item['id']}: {item['original_filename']} (conf: {item['avg_confidence']}, date: {item['created_at']})")
else:
    print(f"   Error: {r2.text}")

print("\nDone!")

"""Direct API test to check for errors"""
import requests
from pathlib import Path

# Test with existing image
image_path = Path("Vattaluttu (2).jpg")

if not image_path.exists():
    print(f"Image not found: {image_path}")
    print("Please ensure there's a test image in the directory")
else:
    print(f"Testing API with {image_path}...")
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post(
            "http://localhost:8000/recognize",
            files=files
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ API Response received")
        print(f"Modern text: '{data.get('modern_text', '')}'")
        print(f"Words detected: {data.get('num_words', 0)}")
        print(f"Characters detected: {data.get('num_characters', 0)}")
        
        warnings = data.get("warnings", [])
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for w in warnings:
                if "Sequence prediction failed" in w:
                    print(f"  ❌ ERROR STILL PRESENT: {w}")
                else:
                    print(f"  - {w}")
        else:
            print("\n✓ ✓ ✓ NO WARNINGS - ERROR IS GONE!")
    else:
        print(f"Error: {response.text}")

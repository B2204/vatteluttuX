"""
Process image and check if it matches va_037
"""
import requests
import json

# Image path
image_path = r"C:\Users\Asus\.gemini\antigravity\brain\020c1d6e-2a30-45aa-b5bc-e24cf834d439\uploaded_media_1770396039431.png"

# API endpoint
url = "http://localhost:8000/recognize"

# Send request
with open(image_path, 'rb') as image_file:
    files = {'image': ('image.png', image_file, 'image/png')}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    
    # Get recognized character
    if result.get('characters'):
        char = result['characters'][0]
        label = char.get('label')
        tamil = char.get('modern_tamil')
        conf = char.get('confidence', 0) * 100
        
        print(f"Recognized: {tamil}")
        print(f"Label: {label}")
        print(f"Confidence: {conf:.1f}%")
        
        # Check if it matches va_037
        if label == 'va_037':
            print("\n✓ MATCH! This is va_037 (ண)")
        else:
            print(f"\n✗ NO MATCH. This is {label}, not va_037")
            print(f"Expected: ண (va_037)")
            print(f"Got: {tamil} ({label})")
    else:
        print("No characters detected")
else:
    print(f"Error: {response.status_code}")

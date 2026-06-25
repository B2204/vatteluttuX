"""
Look up va_037 and process image
"""
import requests
import json

# First, look up va_037
with open(r'backend\app\core\character_map.json', 'r', encoding='utf-8') as f:
    char_map = json.load(f)
    va037_info = char_map['va_037']

print("va_037 Information:")
print(f"  Tamil: {va037_info['modern_tamil']}")
print(f"  Category: {va037_info['category']}")
print(f"  Transliteration: {va037_info['transliteration']}")
print(f"  Description: {va037_info['description']}")
print()

# Now process the image
image_path = r"C:\Users\Asus\.gemini\antigravity\brain\020c1d6e-2a30-45aa-b5bc-e24cf834d439\uploaded_media_1770396039431.png"
url = "http://localhost:8000/recognize"

with open(image_path, 'rb') as image_file:
    files = {'image': ('image.png', image_file, 'image/png')}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    
    # Save to file to avoid encoding issues
    with open('va037_check.txt', 'w', encoding='utf-8') as f:
        if result.get('characters'):
            char = result['characters'][0]
            label = char.get('label')
            tamil = char.get('modern_tamil')
            conf = char.get('confidence', 0) * 100
            
            f.write(f"Recognized Character: {tamil}\n")
            f.write(f"Label: {label}\n")
            f.write(f"Confidence: {conf:.1f}%\n\n")
            
            f.write(f"Expected (va_037): {va037_info['modern_tamil']}\n\n")
            
            if label == 'va_037':
                f.write("✓ MATCH! This is va_037\n")
                match_result = "MATCH"
            else:
                f.write(f"✗ NO MATCH\n")
                f.write(f"Expected: va_037 ({va037_info['modern_tamil']})\n")
                f.write(f"Got: {label} ({tamil})\n")
                match_result = "NO MATCH"
            
            print(f"Result: {match_result}")
            print(f"Detected: {label}")
            print(f"Confidence: {conf:.1f}%")
            print(f"\nDetails saved to va037_check.txt")

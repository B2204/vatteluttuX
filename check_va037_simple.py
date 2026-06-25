"""
Check va_037 match - save all output to file
"""
import requests
import json

# Process the image
image_path = r"C:\Users\Asus\.gemini\antigravity\brain\020c1d6e-2a30-45aa-b5bc-e24cf834d439\uploaded_media_1770396039431.png"
url = "http://localhost:8000/recognize"

with open(image_path, 'rb') as image_file:
    files = {'image': ('image.png', image_file, 'image/png')}
    response = requests.post(url, files=files)

# va_037 is ண
output = []
output.append("=" * 60)
output.append("va_037 Character Check")
output.append("=" * 60)
output.append("")
output.append("va_037 Information:")
output.append("  Tamil Character: ண")
output.append("  Category: Consonant")
output.append("  Transliteration: na")
output.append("")

if response.status_code == 200:
    result = response.json()
    
    if result.get('characters'):
        char = result['characters'][0]
        label = char.get('label')
        tamil = char.get('modern_tamil')
        conf = char.get('confidence', 0) * 100
        
        output.append("Image Recognition Result:")
        output.append(f"  Detected Character: {tamil}")
        output.append(f"  Label: {label}")
        output.append(f"  Confidence: {conf:.1f}%")
        output.append("")
        
        if label == 'va_037':
            output.append("✓✓✓ MATCH! This image is va_037 (ண)")
            result_msg = "MATCH"
        else:
            output.append("✗ NO MATCH")
            output.append(f"  Expected: va_037 (ண)")
            output.append(f"  Got: {label} ({tamil})")
            result_msg = f"NO MATCH - Got {label}"

# Write to file
with open('va037_comparison.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"[RESULT] {result_msg}")
print("Details saved to va037_comparison.txt")

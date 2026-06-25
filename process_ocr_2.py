"""
Process second OCR image
"""
import requests
import json

# New image path
image_path = r"C:\Users\Asus\.gemini\antigravity\brain\020c1d6e-2a30-45aa-b5bc-e24cf834d439\uploaded_media_1770395708475.png"

# API endpoint
url = "http://localhost:8000/recognize"

# Send request
with open(image_path, 'rb') as image_file:
    files = {'image': ('image.png', image_file, 'image/png')}
    response = requests.post(url, files=files)

# Save results
output_path = "ocr_result_2.txt"

with open(output_path, 'w', encoding='utf-8') as f:
    if response.status_code == 200:
        result = response.json()
        
        f.write("=" * 60 + "\n")
        f.write("OCR RECOGNITION RESULT - Image 2\n")
        f.write("=" * 60 + "\n\n")
        
        tamil_text = result.get('modern_text', result.get('recognized_text', 'N/A'))
        total_chars = result.get('total_characters', len(result.get('characters', [])))
        
        f.write(f"Recognized Tamil Text: {tamil_text}\n")
        f.write(f"Total Characters: {total_chars}\n\n")
        
        if 'characters' in result:
            f.write("=" * 60 + "\n")
            f.write("CHARACTER DETAILS:\n")
            f.write("=" * 60 + "\n\n")
            
            for i, char in enumerate(result['characters'], 1):
                tamil = char.get('modern_tamil', 'N/A')
                label = char.get('label', 'N/A')
                conf = char.get('confidence', 0) * 100
                translit = char.get('transliteration', 'N/A')
                
                f.write(f"{i}. Tamil: {tamil}\n")
                f.write(f"   Label: {label}\n")
                f.write(f"   Transliteration: {translit}\n")
                f.write(f"   Confidence: {conf:.1f}%\n\n")
        
        # Save JSON
        with open('ocr_result_2.json', 'w', encoding='utf-8') as jf:
            json.dump(result, jf, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Results saved to {output_path}")
        print(f"[SUCCESS] JSON saved to ocr_result_2.json")
        print(f"\nRecognized Text: {tamil_text}")
        print(f"Total Characters: {total_chars}")
        
    else:
        f.write(f"Error: {response.status_code}\n")
        f.write(response.text)
        print(f"[ERROR] Status code: {response.status_code}")

"""
Quick script to test OCR recognition on the uploaded image
"""
import requests
import json

# Image path
image_path = r"C:\Users\Asus\.gemini\antigravity\brain\020c1d6e-2a30-45aa-b5bc-e24cf834d439\uploaded_media_1770395248150.png"

# API endpoint
url = "http://localhost:8000/recognize"

# Send request with proper content type
with open(image_path, 'rb') as image_file:
    files = {'image': ('image.png', image_file, 'image/png')}
    response = requests.post(url, files=files)

# Print results
if response.status_code == 200:
    result = response.json()
    
    # Print formatted response
    print("=" * 60)
    print("OCR RECOGNITION RESULT")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Parse and display nicely
    if 'recognized_text' in result:
        print("\n" + "=" * 60)
        print(f"Recognized Text: {result['recognized_text']}")
        print(f"Total Characters: {result.get('total_characters', 'N/A')}")
    elif 'modern_tamil' in result:
        print("\n" + "=" * 60)
        print(f"Recognized Text: {result['modern_tamil']}")
        print(f"Total Characters: {result.get('total_characters', 'N/A')}")
        
else:
    print(f"Error: {response.status_code}")
    print(response.text)

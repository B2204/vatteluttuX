import sys
import os
import io

# Set stdout to UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ocr.pipeline import run_ocr_pipeline

def translate_image(image_path):
    print(f"Translating image: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Run pipeline
    result = run_ocr_pipeline(image_bytes, min_char_area=50)
    
    print("\n--- OCR Results ---")
    print(f"Modern Tamil text: {result.modern_text}")
    print(f"Recognized labels: {result.recognized_text}")
    
    for i, char in enumerate(result.characters):
        print(f"Char {i+1}: {char.label} -> {char.modern_tamil} ({char.transliteration})")

if __name__ == "__main__":
    img_path = r'C:\Users\Asus\.gemini\antigravity\brain\34c8d08f-580d-4cff-8221-eeecb069ba38\uploaded_image_1768029560319.png'
    translate_image(img_path)

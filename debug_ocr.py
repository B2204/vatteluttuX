import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ocr.pipeline import run_ocr_pipeline
from app.ml.preprocessing import load_image

def debug_image(image_path):
    # Set stdout to UTF-8 for Windows
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print(f"Debugging image: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Run pipeline
    result = run_ocr_pipeline(image_bytes, min_char_area=50)
    
    print("\n--- OCR Results ---")
    print(f"Recognized labels: {result.recognized_text}")
    print(f"Modern Tamil text: {result.modern_text}")
    print(f"Number of characters detected: {len(result.characters)}")

    
    for i, char in enumerate(result.characters):
        print(f"\nCharacter {i+1}:")
        print(f"  Label: {char.label}")
        print(f"  Tamil: {char.modern_tamil}")
        print(f"  Transliteration: {char.transliteration}")
        print(f"  Confidence: {char.confidence:.4f}")
        print(f"  Bounding Box: {char.bbox}")

    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"  - {w}")

if __name__ == "__main__":
    img_path = r'f:\final mca project\VattalettuX\data\val\sequences\seq_000003.png'
    debug_image(img_path)

"""Quick test to verify no errors and word grouping works."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.ocr.pipeline import run_ocr_pipeline
import cv2

# Test with an actual image
test_image_path = Path("Vattaluttu (2).jpg")

if test_image_path.exists():
    with open(test_image_path, "rb") as f:
        image_bytes = f.read()
    
    print("Testing OCR pipeline...")
    result = run_ocr_pipeline(image_bytes, min_char_area=50, confidence_threshold=0.3)
    
    print(f"\n✓ Success! No errors.")
    print(f"Characters detected: {len(result.characters)}")
    print(f"Words detected: {len(result.words)}")
    print(f"Modern text: '{result.modern_text}'")
    print(f"Warnings: {result.warnings}")
    
    if result.words:
        print("\nWords:")
        for i, word in enumerate(result.words):
            print(f"  {i+1}. '{word.text}' (confidence: {word.confidence:.2f}, chars: {len(word.characters)})")
else:
    print(f"Test image not found: {test_image_path}")

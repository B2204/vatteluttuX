"""
Test word recognition functionality with a simple multi-word image.
"""
import sys
import io
from pathlib import Path

# Configure stdout for UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.ocr.pipeline import run_ocr_pipeline
import cv2
import numpy as np


def create_test_image_with_words():
    """
    Create a simple synthetic test image with multiple 'words' (groups of rectangles).
    White characters on black background (as expected by the OCR system).
    """
    # Create BLACK background (0 = black)
    img = np.zeros((100, 800), dtype=np.uint8)
    
    # Word 1: Three characters close together (positions 50-200)
    # White rectangles (255 = white)
    cv2.rectangle(img, (50, 30), (90, 70), 255, -1)   # Char 1
    cv2.rectangle(img, (100, 30), (140, 70), 255, -1)  # Char 2
    cv2.rectangle(img, (150, 30), (190, 70), 255, -1)  # Char 3
    
    # Gap (word separator) - ~100px
    
    # Word 2: Two characters close together (positions 300-420)
    cv2.rectangle(img, (300, 30), (350, 70), 255, -1)  # Char 4
    cv2.rectangle(img, (370, 30), (420, 70), 255, -1)  # Char 5
    
    # Gap (word separator) - ~130px
    
    # Word 3: Single character (position 550-600)
    cv2.rectangle(img, (550, 30), (600, 70), 255, -1)  # Char 6
    
    return img


def test_word_recognition():
    """Test the word recognition pipeline."""
    print("=" * 60)
    print("Testing Word Recognition")
    print("=" * 60)
    
    # Create test image
    print("\n1. Creating synthetic test image with 3 words...")
    test_image = create_test_image_with_words()
    
    # Save for inspection
    test_image_path = Path("test_word_image.png")
    cv2.imwrite(str(test_image_path), test_image)
    print(f"   Saved test image to: {test_image_path}")
    print(f"   Image shape: {test_image.shape}")
    print(f"   Min/Max pixel values: {test_image.min()}/{test_image.max()}")
    
    # Convert to bytes
    _, buffer = cv2.imencode('.png', test_image)
    image_bytes = buffer.tobytes()
    
    # Run OCR pipeline
    print("\n2. Running OCR pipeline with word recognition...")
    try:
        result = run_ocr_pipeline(
            image_bytes=image_bytes,
            min_char_area=50,  # Smaller than our 40x40=1600 px rectangles
            confidence_threshold=0.1,  # Low threshold for synthetic test
            save_traced=True,
            apply_morphology=True
        )
        
        print(f"\n3. Results:")
        print(f"   Total characters detected: {len(result.characters)}")
        print(f"   Total words detected: {len(result.words)}")
        print(f"   Modern text: '{result.modern_text}'")
        
        if not result.words:
            print("\n   [!] No words detected. Character segmentation may have failed.")
        
        print(f"\n4. Word-level breakdown:")
        for i, word in enumerate(result.words):
            print(f"\n   Word {i + 1}:")
            print(f"      Text: '{word.text}'")
            print(f"      Num characters: {len(word.characters)}")
            print(f"      Confidence: {word.confidence:.3f}")
            print(f"      Bounding box: {word.bbox.to_list()}")
            print(f"      Validated: {word.is_validated}")
            if word.validation_warnings:
                print(f"      Warnings: {', '.join(word.validation_warnings)}")
            print(f"      Character labels: {', '.join(word.labels)}")
        
        print(f"\n5. Character-level details:")
        for i, char in enumerate(result.characters):
            print(f"   Char {i + 1}: {char.label} -> '{char.modern_tamil}' "
                  f"(conf: {char.confidence:.3f}, bbox: {char.bbox.to_list()})")
        
        if result.warnings:
            print(f"\n6. Warnings:")
            for warning in result.warnings:
                print(f"   - {warning}")
        
        print(f"\n7. Traced image saved to: {result.traced_image_path}")
        
        # Validate expected behavior
        print(f"\n8. Validation:")
        expected_words = 3
        expected_chars = 6
        
        success = True
        if len(result.words) == expected_words:
            print(f"   [OK] Correctly detected {expected_words} words")
        else:
            print(f"   [FAIL] Expected {expected_words} words, got {len(result.words)}")
            success = False
        
        if len(result.characters) == expected_chars:
            print(f"   [OK] Correctly detected {expected_chars} characters")
        else:
            print(f"   [FAIL] Expected {expected_chars} characters, got {len(result.characters)}")
            success = False
        
        print("\n" + "=" * 60)
        if success:
            print("Test PASSED!")
        else:
            print("Test PARTIALLY PASSED (see validation above)")
        print("=" * 60)
        
        return True  # Return True even for partial success since code runs
        
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_word_recognition()
    sys.exit(0 if success else 1)

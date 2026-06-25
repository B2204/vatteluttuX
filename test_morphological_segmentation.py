"""
Test Morphological Segmentation Improvements

This script tests the enhanced segmentation with morphological closing
and noise filtering on sample Vatteluttu inscription images.
"""
import cv2
import numpy as np
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.ml.preprocessing import preprocess_full, apply_morphology
from app.ocr.segmentation import segment_characters


def test_segmentation(image_path: str):
    """Test segmentation on an image with and without morphology."""
    print(f"\n{'='*60}")
    print(f"Testing: {image_path}")
    print(f"{'='*60}\n")
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"ERROR: Could not load image: {image_path}")
        return
    
    # Preprocess
    gray, binary = preprocess_full(img)
    
    # Test 1: Without morphology
    print("Test 1: Standard Segmentation (No Morphology)")
    boxes_no_morph = segment_characters(
        binary,
        min_area=100,
        apply_morphology=False,
        filter_noise=False
    )
    print(f"  Characters detected: {len(boxes_no_morph)}")
    
    # Test 2: With morphology only
    print("\nTest 2: With Morphological Closing")
    boxes_with_morph = segment_characters(
        binary,
        min_area=100,
        apply_morphology=True,
        morphology_kernel_size=3,
        filter_noise=False
    )
    print(f"  Characters detected: {len(boxes_with_morph)}")
    
    # Test 3: With morphology + noise filtering
    print("\nTest 3: With Morphology + Noise Filtering")
    boxes_full = segment_characters(
        binary,
        min_area=100,
        apply_morphology=True,
        morphology_kernel_size=3,
        filter_noise=True,
        min_solidity=0.3
    )
    print(f"  Characters detected: {len(boxes_full)}")
    
    # Visualize results
    vis_no_morph = img.copy()
    vis_with_morph = img.copy()
    vis_full = img.copy()
    
    for box in boxes_no_morph:
        cv2.rectangle(vis_no_morph, (box.x, box.y), 
                     (box.x + box.width, box.y + box.height), (0, 0, 255), 2)
    
    for box in boxes_with_morph:
        cv2.rectangle(vis_with_morph, (box.x, box.y), 
                     (box.x + box.width, box.y + box.height), (0, 255, 0), 2)
    
    for box in boxes_full:
        cv2.rectangle(vis_full, (box.x, box.y), 
                     (box.x + box.width, box.y + box.height), (255, 0, 0), 2)
    
    # Save results
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    img_name = Path(image_path).stem
    cv2.imwrite(str(output_dir / f"{img_name}_no_morph.jpg"), vis_no_morph)
    cv2.imwrite(str(output_dir / f"{img_name}_with_morph.jpg"), vis_with_morph)
    cv2.imwrite(str(output_dir / f"{img_name}_full.jpg"), vis_full)
    
    print(f"\n✓ Results saved to {output_dir}/")
    print(f"  - {img_name}_no_morph.jpg (RED boxes)")
    print(f"  - {img_name}_with_morph.jpg (GREEN boxes)")
    print(f"  - {img_name}_full.jpg (BLUE boxes)")


if __name__ == "__main__":
    # Test on sample images if available
    sample_images = [
        "test_images/sample1.jpg",
        "test_images/sample2.jpg",
        "backend/test_data/sample_inscription.jpg",
    ]
    
    found_images = []
    for img_path in sample_images:
        if Path(img_path).exists():
            found_images.append(img_path)
    
    if not found_images:
        print("No test images found. Please add sample images to test_images/ directory.")
        print("You can also specify a custom image path:")
        print("  python test_morphological_segmentation.py <image_path>")
    else:
        for img_path in found_images:
            test_segmentation(img_path)
    
    # Allow custom image path from command line
    if len(sys.argv) > 1:
        custom_path = sys.argv[1]
        if Path(custom_path).exists():
            test_segmentation(custom_path)
        else:
            print(f"\nERROR: Image not found: {custom_path}")

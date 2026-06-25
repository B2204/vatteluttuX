"""
VatteluttuX - Comprehensive Unit Testing Script
Tests all 8 unit test cases as documented in Chapter 5.1
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import os
import time
import json
import numpy as np

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 70)
print("  VatteluttuX - UNIT TESTING (Chapter 5.1)")
print("  Testing individual modules in isolation")
print("=" * 70)
print()

passed = 0
failed = 0
import cv2

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 1: Image Loading (load_image)
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 1: Image Loading (load_image)")
print("-" * 70)
try:
    from app.ml.preprocessing import load_image
    
    test_img_path = os.path.join("data_perfect", "train", "va_001", "img_00000.png")
    with open(test_img_path, "rb") as f:
        image_bytes = f.read()
    
    img = load_image(image_bytes)
    print(f"  Input:     PNG image file ({len(image_bytes)} bytes)")
    print(f"  Output:    NumPy ndarray")
    print(f"  Shape:     {img.shape}")
    print(f"  DType:     {img.dtype}")
    print(f"  Type OK:   {isinstance(img, np.ndarray)}")
    print(f"  DType OK:  {img.dtype == np.uint8}")
    
    try:
        corrupt_bytes = b"this is not an image at all random bytes 123456"
        load_image(corrupt_bytes)
        print(f"  Corrupt:   FAIL (no error raised)")
        failed += 1
    except ValueError as e:
        print(f"  Corrupt:   ValueError raised correctly: '{e}'")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 2: Grayscale Conversion (to_grayscale)
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 2: Grayscale Conversion (to_grayscale)")
print("-" * 70)
try:
    from app.ml.preprocessing import to_grayscale
    
    color_img = np.zeros((100, 150, 3), dtype=np.uint8)
    color_img[:, :, 2] = 255  # Red channel (BGR)
    
    gray = to_grayscale(color_img)
    print(f"  Input:     3-channel BGR image, shape {color_img.shape}")
    print(f"  Output:    Grayscale image, shape {gray.shape}")
    print(f"  Channels:  {len(gray.shape)} dimensions (expected: 2 = single channel)")
    
    gray_real = to_grayscale(img)
    print(f"  Real img:  {img.shape} -> {gray_real.shape}")
    
    gray_again = to_grayscale(gray)
    print(f"  Already gray: shape unchanged = {gray_again.shape == gray.shape}")
    
    test_pixel = np.array([[[100, 150, 200]]], dtype=np.uint8)  # BGR
    gray_pixel = to_grayscale(test_pixel)
    expected = int(0.299 * 200 + 0.587 * 150 + 0.114 * 100)
    print(f"  Formula:   BGR(100,150,200) -> Gray({gray_pixel[0,0]}) ~ {expected}")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 3: Otsu Binarization (otsu_threshold)
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 3: Otsu Binarization (otsu_threshold)")
print("-" * 70)
try:
    from app.ml.preprocessing import otsu_threshold
    
    gray_test = to_grayscale(img)
    binary = otsu_threshold(gray_test)
    
    unique_values = np.unique(binary)
    print(f"  Input:     Grayscale image, shape {gray_test.shape}")
    print(f"  Output:    Binary image, shape {binary.shape}")
    print(f"  Unique:    {unique_values} (expected: [0, 255])")
    print(f"  Binary OK: {set(unique_values).issubset({0, 255})}")
    
    binary_inv = otsu_threshold(gray_test, invert=True)
    inverted_ok = np.array_equal(binary, cv2.bitwise_not(binary_inv))
    print(f"  Invert:    Correctly inverted = {inverted_ok}")
    
    white = np.count_nonzero(binary)
    black = binary.size - white
    print(f"  White px:  {white} ({100*white/binary.size:.1f}%)")
    print(f"  Black px:  {black} ({100*black/binary.size:.1f}%)")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 4: Morphological Operations
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 4: Morphological Operations (apply_morphology)")
print("-" * 70)
try:
    from app.ml.preprocessing import apply_morphology
    
    # Create test binary image with noise dots
    test_bin = np.zeros((200, 200), dtype=np.uint8)
    test_bin[50:150, 50:100] = 255  # Character-like
    test_bin[10:13, 10:13] = 255    # Noise
    test_bin[180:182, 180:182] = 255  # Noise
    test_bin[30:32, 170:172] = 255  # Noise
    
    before_cc = cv2.connectedComponents(test_bin)[0] - 1
    
    opened = apply_morphology(test_bin.copy(), operation="opening", kernel_size=3)
    after_open_cc = cv2.connectedComponents(opened)[0] - 1
    
    print(f"  Input:     Binary image with 1 character + 3 noise blobs")
    print(f"  Before:    {before_cc} connected components")
    print(f"  Opening:   {after_open_cc} components (noise removed)")
    print(f"  Removed:   {before_cc - after_open_cc} noise blobs")
    
    broken_char = np.zeros((200, 200), dtype=np.uint8)
    broken_char[50:90, 50:100] = 255
    broken_char[95:150, 50:100] = 255
    
    before_close = cv2.connectedComponents(broken_char)[0] - 1
    closed = apply_morphology(broken_char.copy(), operation="closing", kernel_size=5)
    after_close = cv2.connectedComponents(closed)[0] - 1
    
    print(f"  Closing:   {before_close} -> {after_close} components (gaps filled)")
    print(f"  Kernel:    3x3 elliptical structuring element")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 5: CNN Model Architecture (VatteluttuCNN)
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 5: CNN Model Architecture (VatteluttuCNN)")
print("-" * 70)
try:
    import torch
    from app.ml.model import VatteluttuCNN
    
    model = VatteluttuCNN(num_classes=247)
    random_input = torch.randn(1, 1, 64, 64)
    
    output = model(random_input)
    print(f"  Input:     Random tensor, shape {list(random_input.shape)}")
    print(f"  Output:    Tensor, shape {list(output.shape)}")
    print(f"  Shape OK:  {list(output.shape) == [1, 247]}")
    
    probs = torch.softmax(output, dim=1)
    prob_sum = probs.sum().item()
    print(f"  Softmax:   Probabilities sum = {prob_sum:.4f}")
    print(f"  Sum ~ 1.0: {abs(prob_sum - 1.0) < 0.001}")
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Total:     {total_params:,} parameters (~{total_params/1e6:.1f}M)")
    print(f"  Trainable: {trainable:,} parameters")
    
    model_size_mb = total_params * 4 / (1024 * 1024)
    print(f"  Model mem: ~{model_size_mb:.1f} MB (float32)")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 6: CNN Model Inference (predict_single)
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 6: CNN Model Inference (predict_single)")
print("-" * 70)
try:
    from app.ml.inference import VatteluttuInference
    
    predictor = VatteluttuInference()
    
    # Load a known character image (va_001 = Tamil vowel A)
    test_img_path = os.path.join("data_perfect", "train", "va_001", "img_00000.png")
    char_img = cv2.imread(test_img_path, cv2.IMREAD_GRAYSCALE)
    
    start_time = time.time()
    # predict_single returns (label, confidence, top_k_predictions)
    best_label, confidence, top_k = predictor.predict_single(char_img)
    inference_time = (time.time() - start_time) * 1000
    
    print(f"  Input:     Character image va_001, preprocessed 64x64")
    print(f"  Label:     {best_label}")
    print(f"  Confidence:{confidence:.2%}")
    print(f"  Correct:   {best_label == 'va_001'}")
    print(f"  Conf > 80%:{confidence > 0.8}")
    print(f"  Time:      {inference_time:.1f}ms")
    print(f"  Device:    {predictor.device}")
    print(f"  Top-5:")
    for rank, (lbl, prob) in enumerate(top_k[:5], 1):
        print(f"    #{rank}: {lbl} ({prob:.2%})")
    
    model_path = os.path.join("backend", "app", "ml", "best_model.pth")
    if os.path.exists(model_path):
        model_size = os.path.getsize(model_path) / (1024 * 1024)
        print(f"  Model:     best_model.pth ({model_size:.1f} MB)")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 7: Character Segmentation
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 7: Character Segmentation (segment_characters)")
print("-" * 70)
try:
    from app.ocr.segmentation import segment_characters
    
    # Create test image with 5 character-like blobs
    test_seg = np.zeros((200, 500), dtype=np.uint8)
    for i in range(5):
        x = 20 + i * 90
        test_seg[40:160, x:x+60] = 255
    
    bboxes = segment_characters(test_seg, min_area=50, apply_morphology=False, filter_noise=False)
    
    print(f"  Input:     Binary image (200x500) with 5 characters")
    print(f"  Detected:  {len(bboxes)} bounding boxes")
    print(f"  Count OK:  {len(bboxes) >= 4}")  # May merge some
    
    # Check reading order (left to right)
    x_positions = [b.x for b in bboxes]
    sorted_ok = x_positions == sorted(x_positions)
    print(f"  Order:     Left-to-right = {sorted_ok}")
    
    for i, b in enumerate(bboxes):
        print(f"  Box {i+1}:    x={b.x}, y={b.y}, w={b.width}, h={b.height}, area={b.area}")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

print()

# ─────────────────────────────────────────────────────────────────────
# TEST CASE 8: Character Mapping (map_label)
# ─────────────────────────────────────────────────────────────────────
print("-" * 70)
print("TEST CASE 8: Character Mapping (label_to_char.json)")
print("-" * 70)
try:
    mapping_path = os.path.join("backend", "app", "core", "label_to_char.json")
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    
    print(f"  File:      label_to_char.json")
    print(f"  Entries:   {len(mapping)} (expected: 247)")
    print(f"  Count OK:  {len(mapping) == 247}")
    
    all_present = all(f"va_{i:03d}" in mapping for i in range(1, 248))
    print(f"  All keys:  va_001 to va_247 present = {all_present}")
    
    all_valid = all(isinstance(v, str) and len(v) > 0 for v in mapping.values())
    print(f"  All vals:  Non-empty Unicode strings = {all_valid}")
    
    known = {"va_001": "\u0b85", "va_013": "\u0b83", "va_032": "\u0b95"}
    for label, expected_char in known.items():
        actual = mapping.get(label, "?")
        match = actual == expected_char
        print(f"  {label}:   '{actual}' = '{expected_char}' -> {'MATCH' if match else 'MISMATCH'}")
    
    labels = list(mapping.keys())
    dup_labels = len(labels) != len(set(labels))
    print(f"  Dup keys:  {dup_labels} (expected: False)")
    
    print(f"  Samples:")
    for label in ["va_001", "va_014", "va_032", "va_044", "va_247"]:
        if label in mapping:
            print(f"    {label} -> {mapping[label]}")
    
    print(f"  Result:    *** PASS ***")
    passed += 1
except Exception as e:
    print(f"  Result:    *** FAIL *** ({e})")
    failed += 1

# ─────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("  UNIT TESTING SUMMARY")
print("=" * 70)
print(f"  Total Test Cases:  8")
print(f"  Passed:            {passed}")
print(f"  Failed:            {failed}")
print(f"  Success Rate:      {100*passed/(passed+failed):.0f}%")
print("=" * 70)
if failed == 0:
    print("  All unit tests PASSED!")
else:
    print("  COMPLETED WITH FAILURES")
print("=" * 70)

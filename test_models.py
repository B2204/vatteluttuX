"""
Test and compare different model files to identify the best performer.
"""
import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ml.inference import VatteluttuInference
from app.ml.preprocessing import load_image

def test_model(model_path, test_image_path):
    """Test a specific model on a test image."""
    print(f"\n{'='*60}")
    print(f"Testing model: {model_path.name}")
    print(f"{'='*60}")
    
    if not model_path.exists():
        print(f"❌ Model file not found!")
        return None
    
    # Create inference instance
    inference = VatteluttuInference(model_path=model_path, model_type="cnn")
    
    # Load model
    success = inference.load_model()
    if not success:
        print(f"❌ Failed to load model")
        return None
    
    # Load test image
    with open(test_image_path, 'rb') as f:
        img_bytes = f.read()
    
    img = load_image(img_bytes)
    
    # Make prediction
    try:
        label, confidence, top_5 = inference.predict_single(img)
        
        print(f"\n✓ Model loaded successfully")
        print(f"  Best prediction: {label}")
        print(f"  Confidence: {confidence:.4f}")
        print(f"\n  Top 5 predictions:")
        for i, (lbl, conf) in enumerate(top_5, 1):
            tamil = inference.mapper.map_label(lbl)
            print(f"    {i}. {lbl:8s} ({tamil}) - {conf:.4f}")
        
        return {
            'model': model_path.name,
            'label': label,
            'confidence': confidence,
            'top_5': top_5
        }
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Set stdout to UTF-8 for Windows
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # Test images
    test_images = [
        r'f:\final mca project\VattalettuX\data\val\sequences\seq_000003.png',
        r'f:\final mca project\VattalettuX\data\val\sequences\seq_000005.png',
        r'f:\final mca project\VattalettuX\data\val\sequences\seq_000007.png',
    ]
    
    # Models to test
    models_dir = Path(r'f:\final mca project\VattalettuX\backend\models')
    models_to_test = [
        models_dir / 'best_model.pth',
        models_dir / 'vatteluttu_cnn.pth',
    ]
    
    results = []
    
    for test_img in test_images:
        if not os.path.exists(test_img):
            print(f"Test image not found: {test_img}")
            continue
            
        print(f"\n\n{'#'*60}")
        print(f"# Testing image: {Path(test_img).name}")
        print(f"{'#'*60}")
        
        for model_path in models_to_test:
            result = test_model(model_path, test_img)
            if result:
                result['test_image'] = Path(test_img).name
                results.append(result)
    
    # Summary
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    if results:
        # Group by model
        by_model = {}
        for r in results:
            model = r['model']
            if model not in by_model:
                by_model[model] = []
            by_model[model].append(r['confidence'])
        
        print("\nAverage confidence by model:")
        for model, confidences in by_model.items():
            avg_conf = sum(confidences) / len(confidences)
            print(f"  {model:25s} - Avg: {avg_conf:.4f} ({len(confidences)} tests)")

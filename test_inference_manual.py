import torch
import sys
import os
import cv2
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ml.inference import VatteluttuInference

def test_inference():
    model_path = r'f:\final mca project\VattalettuX\backend\models\vatteluttu_crnn.pth'
    inference = VatteluttuInference(model_path=Path(model_path), model_type="crnn")
    
    # Create a dummy image (64x64)
    dummy_img = np.zeros((64, 64), dtype=np.uint8)
    cv2.putText(dummy_img, "A", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    
    print("Testing predict_single...")
    try:
        label, conf, top_k = inference.predict_single(dummy_img)
        print(f"Success! Label: {label}, Conf: {conf}")
    except Exception as e:
        print(f"FAILED predict_single: {e}")
        import traceback
        traceback.print_exc()

    print("\nTesting predict_sequence (height 64)...")
    try:
        seq_img = np.zeros((64, 200), dtype=np.uint8)
        text = inference.predict_sequence(seq_img)
        print(f"Success! Text: '{text}'")
    except Exception as e:
        print(f"FAILED predict_sequence: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_inference()

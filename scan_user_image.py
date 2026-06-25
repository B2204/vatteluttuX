import sys
import os
import cv2
import json
from pathlib import Path

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ml.inference import VatteluttuInference
from app.ml.preprocessing import load_image

def scan_image(image_path):
    print(f"Scanning image: {image_path}")
    
    if not os.path.exists(image_path):
        print("Error: Image file not found")
        return

    # Initialize inference for CRNN
    model_path = Path(r'f:\final mca project\VattalettuX\backend\models_tiny\last_model.pth')
    inference = VatteluttuInference(model_path=model_path, model_type="crnn")
    
    print("\nLoading CRNN model from models_tiny...")
    if not inference.load_model():
        print("Error: Failed to load CRNN model")
        return
    
    print("\nProcessing recognition using CRNN predict_sequence...")
    
    # Load image
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    img = load_image(img_bytes)
    
    # Run sequence prediction
    modern_text = inference.predict_sequence(img)
    
    print(f"\nRecognized Modern Tamil: {modern_text}")
    
    # Save result
    with open('scan_result.json', 'w', encoding='utf-8') as f:
        json.dump({
            "image": image_path,
            "recognized_text": modern_text,
            "model": "crnn_tiny"
        }, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Set stdout to UTF-8
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
    image_path = r"C:\Users\Asus\.gemini\antigravity\brain\f79769fb-0647-4fbd-ba20-9a29d4b2400c\media__1771479305341.png"
    scan_image(image_path)

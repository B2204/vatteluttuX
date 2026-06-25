import sys
import os
import io
from pathlib import Path
import torch

# Set stdout to UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ocr.pipeline import run_ocr_pipeline
from app.ml.inference import VatteluttuInference
import app.ml.inference as inference_module
from app.ml.mapping import TamilMapper

def translate_image_with_new_model(image_path, model_path):
    print(f"Translating image: {image_path}")
    print(f"Using targeted model: {model_path}")
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    # Target mapping for the 7 classes
    TARGET_IDX_TO_LABEL = {
        0: "va_001",
        1: "va_022",
        2: "va_023",
        3: "va_040",
        4: "va_041",
        5: "va_138",
        6: "va_149"
    }

    # Initialize targeted inference
    targeted_inference = VatteluttuInference(model_path=Path(model_path), model_type="cnn")
    
    # Manually load and setup the model with correct num_classes
    from app.ml.model import create_model
    targeted_inference.model = create_model(model_type="cnn", num_classes=7)
    state_dict = torch.load(model_path, map_location=targeted_inference.device)
    targeted_inference.model.load_state_dict(state_dict)
    targeted_inference.model.to(targeted_inference.device)
    targeted_inference.model.eval()
    targeted_inference.loaded = True
    
    # Monkey-patch the IDX_TO_LABEL and predict_single to use our targeted labels
    original_predict_single = targeted_inference.predict_single
    
    def patched_predict_single(image, top_k=5):
        # We need to manually do what predict_single does but with our IDX_TO_LABEL
        from app.ml.preprocessing import preprocess_character_crop
        processed = preprocess_character_crop(image)
        tensor = torch.from_numpy(processed).unsqueeze(0).to(targeted_inference.device)
        with torch.no_grad():
            outputs = targeted_inference.model(tensor)
            probs = torch.softmax(outputs, dim=1)[0]
            top_probs, top_indices = torch.topk(probs, min(top_k, 7))
            
            top_k_preds = []
            for prob, idx in zip(top_probs.cpu().numpy(), top_indices.cpu().numpy()):
                label = TARGET_IDX_TO_LABEL[idx]
                top_k_preds.append((label, float(prob)))
        
        best_label = top_k_preds[0][0]
        best_conf = top_k_preds[0][1]
        return best_label, best_conf, top_k_preds

    targeted_inference.predict_single = patched_predict_single
    
    # Also need to fix predict_sequence or it will call predict_single in a loop or use its own logic
    # The pipeline uses predict_single for individual boxes and predict_sequence for the whole line.
    
    def patched_predict_sequence(image):
        # Sequence logic for CNN-only would be character-by-character from segmentation (done in pipeline)
        # But predict_sequence in inference.py tries to run CRNN. We disable it for this test.
        return ""

    targeted_inference.predict_sequence = patched_predict_sequence
    
    # Inject into global module
    inference_module._inference = targeted_inference
    
    # Run pipeline
    result = run_ocr_pipeline(image_bytes, min_char_area=50)
    
    print("\n--- OCR Results ---")
    print(f"Recognized labels: {result.recognized_text}")
    print(f"Modern Tamil text: {result.modern_text}")
    
    # Note: Modern text might be empty because we disabled predict_sequence. 
    # Let's fallback to assembling from characters if needed.
    if not result.modern_text:
        assembled = "".join(c.modern_tamil for c in result.characters)
        print(f"Assembled Tamil text: {assembled}")
    
    for i, char in enumerate(result.characters):
        print(f"Char {i+1}: {char.label} -> {char.modern_tamil} ({char.transliteration}) | Conf: {char.confidence:.4f}")

if __name__ == "__main__":
    img_path = r'C:\Users\Asus\.gemini\antigravity\brain\34c8d08f-580d-4cff-8221-eeecb069ba38\uploaded_image_1768029560319.png'
    new_model_path = r'f:\final mca project\VattalettuX\backend\models_cnn_target\vatteluttu_cnn.pth'
    translate_image_with_new_model(img_path, new_model_path)

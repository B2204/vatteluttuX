import torch
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(os.path.abspath('f:/final mca project/VattalettuX/backend'))

from app.ml.model import create_model
from app.core.label_mappings import NUM_CLASSES

def inspect_model(model_path):
    print(f"Inspecting weights: {model_path}")
    if not os.path.exists(model_path):
        print("Model file not found!")
        return

    state_dict = torch.load(model_path, map_location='cpu')
    
    # Check classifier/fc layers
    for key in state_dict.keys():
        if 'fc.weight' in key or 'classifier' in key:
            print(f"Found weight layer: {key}, shape: {state_dict[key].shape}")
            if 'fc.weight' in key:
                out_features = state_dict[key].shape[0]
                print(f"Model out_features (classes+blank): {out_features}")
                print(f"Project NUM_CLASSES: {NUM_CLASSES}")
                print(f"Difference: {out_features - NUM_CLASSES}")

    # Try to load into a model
    try:
        # First guess: use project NUM_CLASSES
        model = create_model("crnn", num_classes=NUM_CLASSES)
        model.load_state_dict(state_dict)
        print("Successfully loaded state_dict with project NUM_CLASSES")
    except Exception as e:
        print(f"Failed to load with NUM_CLASSES={NUM_CLASSES}: {e}")
        
        # Try to infer num_classes from state_dict
        if 'fc.weight' in state_dict:
            inferred_num_classes = state_dict['fc.weight'].shape[0] - 1
            print(f"Retrying with inferred num_classes: {inferred_num_classes}")
            try:
                model = create_model("crnn", num_classes=inferred_num_classes)
                model.load_state_dict(state_dict)
                print(f"Successfully loaded with inferred num_classes={inferred_num_classes}")
            except Exception as e2:
                print(f"Failed again: {e2}")

if __name__ == "__main__":
    model_path = r'f:\final mca project\VattalettuX\backend\models\vatteluttu_crnn.pth'
    inspect_model(model_path)

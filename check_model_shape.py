import torch
import sys

def check_shape(path):
    sd = torch.load(path, map_location='cpu')
    print(f"File: {path}")
    if 'classifier.4.weight' in sd:
        print(f"classifier.4.weight shape: {sd['classifier.4.weight'].shape}")
    else:
        print("classifier.4.weight not found")
        for k in sd.keys():
            if 'fc' in k or 'classifier' in k:
                print(f"Found {k}: {sd[k].shape}")

if __name__ == "__main__":
    check_shape(r'f:\final mca project\VattalettuX\backend\models_tiny\last_model.pth')

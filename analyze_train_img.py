import cv2
import numpy as np

def analyze_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Failed to load image")
        return
    
    print(f"Image: {path}")
    print(f"Shape: {img.shape}")
    print(f"Min: {img.min()}, Max: {img.max()}, Mean: {img.mean():.2f}")
    
    # Check corners for background
    corners = [img[0,0], img[0,-1], img[-1,0], img[-1,-1]]
    print(f"Corners (probable background): {corners}")

if __name__ == "__main__":
    analyze_image(r'f:\final mca project\VattalettuX\data\train\sequences\seq_000000.png')

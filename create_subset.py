import os
import shutil
import random
from pathlib import Path

def create_subset(src_dir, dst_dir, samples_per_class=10):
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    
    for split in ['train', 'val']:
        src_split = src_dir / split
        dst_split = dst_dir / split
        dst_split.mkdir(parents=True, exist_ok=True)
        
        for class_dir in src_split.iterdir():
            if class_dir.is_dir() and class_dir.name.startswith("va_"):
                dst_class = dst_split / class_dir.name
                dst_class.mkdir(exist_ok=True)
                
                images = list(class_dir.glob("*.png"))
                selected = random.sample(images, min(len(images), samples_per_class))
                
                for img in selected:
                    shutil.copy(img, dst_class / img.name)
        
        print(f"Created subset for {split}")

if __name__ == "__main__":
    create_subset(
        r'f:\final mca project\VattalettuX\data_full',
        r'f:\final mca project\VattalettuX\data_subset',
        samples_per_class=15
    )

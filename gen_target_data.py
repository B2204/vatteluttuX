import subprocess
import os

classes = ["va_001", "va_022", "va_023", "va_040", "va_041", "va_138", "va_149"]
splits = [("train", 100), ("val", 25)]

for split_name, count in splits:
    print(f"Generating {split_name} data...")
    for cls in classes:
        print(f"  Generating {cls} ({count} samples)...")
        subprocess.run([
            "python", "training/generate_data.py",
            "--fonts-dir", "data/fonts",
            "--samples", str(count),
            "--output-dir", "data_target",
            "--label", cls,
            "--split", split_name
        ])
print("Done generating targeted data.")

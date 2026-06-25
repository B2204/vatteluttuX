"""
VatteluttuX - All-in-One Model Retraining Script

Generates fresh synthetic data for all 247 Tamil characters and trains
a TinyCNN model from scratch. Saves the best model to backend/models/.

Usage:
    python retrain_model.py
"""
import os
import sys
import io
import json
import time
import random
import shutil
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms

# ============================================================================
# CONFIGURATION
# ============================================================================
PROJECT_ROOT = Path(__file__).parent
FONT_PATH = PROJECT_ROOT / "data" / "fonts" / "e-VatteluttuOT.ttf"
LABEL_TO_CHAR_PATH = PROJECT_ROOT / "backend" / "app" / "core" / "label_to_char.json"
OUTPUT_DATA_DIR = PROJECT_ROOT / "data_retrain"
OUTPUT_MODEL_DIR = PROJECT_ROOT / "backend" / "models"

IMAGE_SIZE = 64
TRAIN_SAMPLES_PER_CLASS = 400   # 400 train + 100 val = 500 total
VAL_SAMPLES_PER_CLASS = 100
BATCH_SIZE = 64
EPOCHS = 50
LEARNING_RATE = 1e-3
NUM_WORKERS = 0  # Use 0 for Windows compatibility
EARLY_STOPPING = 12

# ============================================================================
# MODEL DEFINITION (TinyCNN - matches backend/app/ml/model.py)
# ============================================================================
class TinyCNN(nn.Module):
    """Small CNN for quick CPU training. Matches the one in model.py."""
    def __init__(self, num_classes=247, dropout=0.3):
        super().__init__()
        self.num_classes = num_classes
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.adaptive_pool = nn.AdaptiveAvgPool2d(4)
        self.fc1 = nn.Linear(64 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.relu(self.conv3(x))
        x = self.adaptive_pool(x)
        x = x.flatten(1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x


# ============================================================================
# DATA GENERATION
# ============================================================================
def load_fonts():
    """Load font at multiple sizes for variety."""
    fonts = []
    for size in [28, 32, 36, 40, 44, 48, 52, 56]:
        try:
            font = ImageFont.truetype(str(FONT_PATH), size)
            fonts.append(font)
        except Exception as e:
            print(f"  Warning: Could not load font at size {size}: {e}")
    return fonts


def create_base_image(char, font, img_size=IMAGE_SIZE):
    """Render a character centered on a white background."""
    img = Image.new('L', (img_size, img_size), 255)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), char, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (img_size - tw) // 2 - bbox[0]
    y = (img_size - th) // 2 - bbox[1]
    draw.text((x, y), char, font=font, fill=0)
    return img


def apply_augmentations(img):
    """Apply random augmentations to create training variety."""
    # Random rotation
    if random.random() > 0.3:
        angle = random.uniform(-15, 15)
        img = img.rotate(angle, fillcolor=255, expand=False)

    # Random brightness
    if random.random() > 0.3:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))

    # Random contrast
    if random.random() > 0.3:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))

    # Random blur
    if random.random() > 0.6:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3, 1.2)))

    # Random translation
    if random.random() > 0.3:
        dx = random.randint(-4, 4)
        dy = random.randint(-4, 4)
        img = img.transform(img.size, Image.AFFINE, (1, 0, dx, 0, 1, dy), fillcolor=255)

    # Noise
    if random.random() > 0.4:
        np_img = np.array(img).astype(np.float32)
        noise = np.random.normal(0, random.uniform(3, 15), np_img.shape)
        np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(np_img)

    # Thickness variation via resize
    if random.random() > 0.5:
        w, h = img.size
        scale = random.uniform(0.85, 1.15)
        temp = img.resize((int(w * scale), int(h * scale)), Image.BILINEAR)
        img = temp.resize((w, h), Image.BICUBIC)

    # Morphological-like effects (erosion/dilation via MinFilter/MaxFilter)
    if random.random() > 0.7:
        if random.random() > 0.5:
            img = img.filter(ImageFilter.MinFilter(3))  # Thicken strokes
        else:
            img = img.filter(ImageFilter.MaxFilter(3))  # Thin strokes

    return img


def generate_data(label_to_char, fonts):
    """Generate training and validation data for all characters."""
    print("\n" + "=" * 60)
    print("STEP 1: GENERATING TRAINING DATA")
    print("=" * 60)

    total_classes = len(label_to_char)
    print(f"  Classes: {total_classes}")
    print(f"  Train samples/class: {TRAIN_SAMPLES_PER_CLASS}")
    print(f"  Val samples/class: {VAL_SAMPLES_PER_CLASS}")
    print(f"  Total images: {total_classes * (TRAIN_SAMPLES_PER_CLASS + VAL_SAMPLES_PER_CLASS)}")
    print(f"  Output directory: {OUTPUT_DATA_DIR}")

    # Clean previous data
    if OUTPUT_DATA_DIR.exists():
        shutil.rmtree(OUTPUT_DATA_DIR)

    train_total = 0
    val_total = 0
    start_time = time.time()

    for ci, (label, char) in enumerate(sorted(label_to_char.items())):
        # Progress every 20 classes
        if ci % 20 == 0:
            elapsed = time.time() - start_time
            print(f"  [{ci+1}/{total_classes}] Generating {label} ({char})... ({elapsed:.0f}s elapsed)")

        # Generate training images
        train_dir = OUTPUT_DATA_DIR / "train" / label
        train_dir.mkdir(parents=True, exist_ok=True)
        for i in range(TRAIN_SAMPLES_PER_CLASS):
            font = random.choice(fonts)
            img = create_base_image(char, font)
            img = apply_augmentations(img)
            img.save(train_dir / f"img_{i:05d}.png")
            train_total += 1

        # Generate validation images (less augmentation)
        val_dir = OUTPUT_DATA_DIR / "val" / label
        val_dir.mkdir(parents=True, exist_ok=True)
        for i in range(VAL_SAMPLES_PER_CLASS):
            font = random.choice(fonts)
            img = create_base_image(char, font)
            # Lighter augmentation for val
            if random.random() > 0.5:
                angle = random.uniform(-5, 5)
                img = img.rotate(angle, fillcolor=255)
            img.save(val_dir / f"img_{i:05d}.png")
            val_total += 1

    elapsed = time.time() - start_time
    print(f"\n  Data generation complete in {elapsed:.0f}s")
    print(f"  Training images: {train_total}")
    print(f"  Validation images: {val_total}")
    return train_total, val_total


# ============================================================================
# DATASET
# ============================================================================
class CharDataset(Dataset):
    """Simple dataset for character images."""
    def __init__(self, root_dir, split, label_to_idx, transform=None):
        self.transform = transform
        self.samples = []
        split_dir = Path(root_dir) / split
        for label_dir in sorted(split_dir.iterdir()):
            if label_dir.is_dir() and label_dir.name in label_to_idx:
                idx = label_to_idx[label_dir.name]
                for img_path in label_dir.glob("*.png"):
                    self.samples.append((str(img_path), idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        path, label = self.samples[i]
        img = Image.open(path).convert('L')
        if self.transform:
            img = self.transform(img)
        else:
            img = transforms.ToTensor()(img)
        return img, label


# ============================================================================
# TRAINING
# ============================================================================
def train_model(label_to_idx):
    """Train TinyCNN on the generated data."""
    print("\n" + "=" * 60)
    print("STEP 2: TRAINING MODEL")
    print("=" * 60)

    num_classes = len(label_to_idx)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Device: {device}")
    print(f"  Classes: {num_classes}")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Learning rate: {LEARNING_RATE}")

    # Transforms
    train_transform = transforms.Compose([
        transforms.RandomRotation(10),
        transforms.RandomAffine(degrees=0, translate=(0.05, 0.05)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    val_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    # Datasets
    train_ds = CharDataset(OUTPUT_DATA_DIR, "train", label_to_idx, train_transform)
    val_ds = CharDataset(OUTPUT_DATA_DIR, "val", label_to_idx, val_transform)
    print(f"  Train samples: {len(train_ds)}")
    print(f"  Val samples: {len(val_ds)}")

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    # Model
    model = TinyCNN(num_classes=num_classes).to(device)
    params = sum(p.numel() for p in model.parameters())
    print(f"  Model parameters: {params:,}")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=5)

    best_val_acc = 0.0
    no_improve = 0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': [], 'lr': []}

    OUTPUT_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    for epoch in range(EPOCHS):
        # --- Train ---
        model.train()
        t_loss, t_correct, t_total = 0.0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            t_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            t_correct += predicted.eq(labels).sum().item()
            t_total += labels.size(0)

        train_loss = t_loss / t_total
        train_acc = t_correct / t_total

        # --- Validate ---
        model.eval()
        v_loss, v_correct, v_total = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                v_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                v_correct += predicted.eq(labels).sum().item()
                v_total += labels.size(0)

        val_loss = v_loss / v_total
        val_acc = v_correct / v_total

        lr = optimizer.param_groups[0]['lr']
        scheduler.step(val_acc)

        # Track
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['lr'].append(lr)

        marker = ""
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), OUTPUT_MODEL_DIR / "best_model.pth")
            no_improve = 0
            marker = " [*BEST*]"
        else:
            no_improve += 1

        torch.save(model.state_dict(), OUTPUT_MODEL_DIR / "last_model.pth")

        print(f"  Epoch {epoch+1:3d}/{EPOCHS} | "
              f"Train: {100*train_acc:.1f}% (loss={train_loss:.3f}) | "
              f"Val: {100*val_acc:.1f}% (loss={val_loss:.3f}) | "
              f"LR={lr:.6f}{marker}")

        if no_improve >= EARLY_STOPPING:
            print(f"\n  Early stopping at epoch {epoch+1}")
            break

    # Save artifacts
    shutil.copy(OUTPUT_MODEL_DIR / "best_model.pth", OUTPUT_MODEL_DIR / "vatteluttu_cnn.pth")

    label_to_idx_sorted = dict(sorted(label_to_idx.items()))
    with open(OUTPUT_MODEL_DIR / "label_to_idx.json", 'w', encoding='utf-8') as f:
        json.dump(label_to_idx_sorted, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_MODEL_DIR / "training_history.json", 'w') as f:
        json.dump(history, f, indent=2)

    print(f"\n  Training complete!")
    print(f"  Best validation accuracy: {100*best_val_acc:.1f}%")
    print(f"  Model saved to: {OUTPUT_MODEL_DIR / 'best_model.pth'}")
    print(f"  Also copied to: {OUTPUT_MODEL_DIR / 'vatteluttu_cnn.pth'}")

    return model, best_val_acc, history


# ============================================================================
# VERIFICATION
# ============================================================================
def verify_model(model, label_to_idx, label_to_char):
    """Quick sanity test: predict a few val images."""
    print("\n" + "=" * 60)
    print("STEP 3: VERIFICATION")
    print("=" * 60)

    idx_to_label = {v: k for k, v in label_to_idx.items()}
    device = next(model.parameters()).device
    model.eval()

    val_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    val_dir = OUTPUT_DATA_DIR / "val"
    label_dirs = sorted([d for d in val_dir.iterdir() if d.is_dir()])

    # Pick 10 random classes
    test_dirs = random.sample(label_dirs, min(10, len(label_dirs)))
    correct = 0
    total = 0

    for label_dir in test_dirs:
        label = label_dir.name
        expected_char = label_to_char.get(label, "?")
        imgs = list(label_dir.glob("*.png"))
        if not imgs:
            continue

        # Pick a random image
        img_path = random.choice(imgs)
        img = Image.open(img_path).convert('L')
        tensor = val_transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(tensor)
            probs = torch.softmax(output, dim=1)
            pred_idx = output.argmax(1).item()
            confidence = probs[0, pred_idx].item()

        pred_label = idx_to_label.get(pred_idx, "???")
        pred_char = label_to_char.get(pred_label, "?")
        match = "✓" if pred_label == label else "✗"
        if pred_label == label:
            correct += 1
        total += 1

        print(f"  {match} Expected: {label} ({expected_char}) | "
              f"Predicted: {pred_label} ({pred_char}) | "
              f"Confidence: {100*confidence:.1f}%")

    print(f"\n  Quick test accuracy: {correct}/{total} = {100*correct/total:.0f}%")


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("VatteluttuX - Model Retraining")
    print("=" * 60)

    # Load label mapping
    with open(LABEL_TO_CHAR_PATH, 'r', encoding='utf-8') as f:
        label_to_char = json.load(f)
    print(f"Loaded {len(label_to_char)} character mappings")

    # Check font
    if not FONT_PATH.exists():
        print(f"ERROR: Font not found at {FONT_PATH}")
        return
    print(f"Font: {FONT_PATH.name}")

    # Load fonts
    fonts = load_fonts()
    if not fonts:
        print("ERROR: No fonts could be loaded!")
        return
    print(f"Loaded {len(fonts)} font variations")

    # Build label_to_idx (sorted order, matching backend)
    label_to_idx = {label: idx for idx, label in enumerate(sorted(label_to_char.keys()))}

    # Step 1: Generate data
    generate_data(label_to_char, fonts)

    # Step 2: Train
    model, best_acc, history = train_model(label_to_idx)

    # Step 3: Verify
    verify_model(model, label_to_idx, label_to_char)

    print("\n" + "=" * 60)
    print("ALL DONE!")
    print(f"Best validation accuracy: {100*best_acc:.1f}%")
    print(f"Model saved to: {OUTPUT_MODEL_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

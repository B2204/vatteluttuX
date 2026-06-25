"""
VatteluttuX - Fast Model Retraining Script (v2)

Generates minimal synthetic data and trains TinyCNN quickly on CPU.
Uses 100 samples/class for fast training (~15-20 min on CPU).

Usage:
    python retrain_fast.py
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
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF

# ============================================================================
# CONFIGURATION
# ============================================================================
PROJECT_ROOT = Path(__file__).parent
FONT_PATH = PROJECT_ROOT / "data" / "fonts" / "e-VatteluttuOT.ttf"
LABEL_TO_CHAR_PATH = PROJECT_ROOT / "backend" / "app" / "core" / "label_to_char.json"
OUTPUT_MODEL_DIR = PROJECT_ROOT / "backend" / "models"

IMAGE_SIZE = 64
TRAIN_SAMPLES = 80       # per class
VAL_SAMPLES = 20          # per class
BATCH_SIZE = 128
EPOCHS = 60
LEARNING_RATE = 1e-3
EARLY_STOPPING = 15

print("=" * 60, flush=True)
print("VatteluttuX - Fast Model Retraining (v2)", flush=True)
print("=" * 60, flush=True)

# ============================================================================
# MODEL DEFINITION (TinyCNN - matches backend/app/ml/model.py exactly)
# ============================================================================
class TinyCNN(nn.Module):
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
# DATA GENERATION (in-memory for speed)
# ============================================================================
def load_fonts():
    fonts = []
    for size in [28, 32, 36, 40, 44, 48, 52, 56]:
        try:
            font = ImageFont.truetype(str(FONT_PATH), size)
            fonts.append(font)
        except:
            pass
    return fonts


def render_char(char, font, img_size=IMAGE_SIZE):
    img = Image.new('L', (img_size, img_size), 255)
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), char, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (img_size - tw) // 2 - bbox[0]
    y = (img_size - th) // 2 - bbox[1]
    draw.text((x, y), char, font=font, fill=0)
    return img


def augment(img):
    if random.random() > 0.3:
        img = img.rotate(random.uniform(-15, 15), fillcolor=255)
    if random.random() > 0.3:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.7, 1.3))
    if random.random() > 0.3:
        img = ImageEnhance.Contrast(img).enhance(random.uniform(0.7, 1.3))
    if random.random() > 0.6:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3, 1.0)))
    if random.random() > 0.3:
        dx, dy = random.randint(-4, 4), random.randint(-4, 4)
        img = img.transform(img.size, Image.AFFINE, (1, 0, dx, 0, 1, dy), fillcolor=255)
    if random.random() > 0.5:
        np_img = np.array(img).astype(np.float32)
        noise = np.random.normal(0, random.uniform(3, 12), np_img.shape)
        img = Image.fromarray(np.clip(np_img + noise, 0, 255).astype(np.uint8))
    if random.random() > 0.6:
        w, h = img.size
        s = random.uniform(0.85, 1.15)
        img = img.resize((int(w*s), int(h*s)), Image.BILINEAR).resize((w, h), Image.BICUBIC)
    if random.random() > 0.7:
        if random.random() > 0.5:
            img = img.filter(ImageFilter.MinFilter(3))
        else:
            img = img.filter(ImageFilter.MaxFilter(3))
    return img


def generate_tensor_dataset(label_to_char, fonts, num_samples, do_augment=True):
    """Generate entire dataset as tensors in memory."""
    labels_sorted = sorted(label_to_char.keys())
    num_classes = len(labels_sorted)
    total = num_classes * num_samples

    all_images = torch.zeros(total, 1, IMAGE_SIZE, IMAGE_SIZE)
    all_labels = torch.zeros(total, dtype=torch.long)

    normalize = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    idx = 0
    for ci, label in enumerate(labels_sorted):
        char = label_to_char[label]
        for j in range(num_samples):
            font = random.choice(fonts)
            img = render_char(char, font)
            if do_augment:
                img = augment(img)
            tensor = normalize(img)
            all_images[idx] = tensor
            all_labels[idx] = ci
            idx += 1

    return TensorDataset(all_images, all_labels)


# ============================================================================
# MAIN
# ============================================================================
def main():
    # Load mappings
    with open(LABEL_TO_CHAR_PATH, 'r', encoding='utf-8') as f:
        label_to_char = json.load(f)

    num_classes = len(label_to_char)
    print(f"Characters: {num_classes}", flush=True)

    # Check font
    if not FONT_PATH.exists():
        print(f"ERROR: Font not found at {FONT_PATH}", flush=True)
        return
    print(f"Font: {FONT_PATH.name}", flush=True)

    fonts = load_fonts()
    if not fonts:
        print("ERROR: No fonts loaded!", flush=True)
        return
    print(f"Font variations: {len(fonts)}", flush=True)

    label_to_idx = {label: i for i, label in enumerate(sorted(label_to_char.keys()))}
    idx_to_label = {i: label for label, i in label_to_idx.items()}

    # ---- Step 1: Generate data in memory ----
    print(f"\n--- STEP 1: Generating data in memory ---", flush=True)
    print(f"Train: {num_classes} x {TRAIN_SAMPLES} = {num_classes * TRAIN_SAMPLES} images", flush=True)
    print(f"Val:   {num_classes} x {VAL_SAMPLES} = {num_classes * VAL_SAMPLES} images", flush=True)

    t0 = time.time()
    train_ds = generate_tensor_dataset(label_to_char, fonts, TRAIN_SAMPLES, do_augment=True)
    print(f"  Train data generated in {time.time()-t0:.1f}s", flush=True)

    t0 = time.time()
    val_ds = generate_tensor_dataset(label_to_char, fonts, VAL_SAMPLES, do_augment=False)
    print(f"  Val data generated in {time.time()-t0:.1f}s", flush=True)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # ---- Step 2: Train ----
    print(f"\n--- STEP 2: Training TinyCNN ---", flush=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}", flush=True)
    print(f"Epochs: {EPOCHS}, Batch size: {BATCH_SIZE}, LR: {LEARNING_RATE}", flush=True)

    model = TinyCNN(num_classes=num_classes).to(device)
    params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {params:,}", flush=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=5)

    best_val_acc = 0.0
    no_improve = 0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': [], 'lr': []}

    OUTPUT_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    train_start = time.time()

    for epoch in range(EPOCHS):
        ep_start = time.time()

        # Train
        model.train()
        t_loss, t_correct, t_total = 0.0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            out = model(images)
            loss = criterion(out, labels)
            loss.backward()
            optimizer.step()
            t_loss += loss.item() * images.size(0)
            _, pred = out.max(1)
            t_correct += pred.eq(labels).sum().item()
            t_total += labels.size(0)

        train_loss = t_loss / t_total
        train_acc = t_correct / t_total

        # Validate
        model.eval()
        v_loss, v_correct, v_total = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                out = model(images)
                loss = criterion(out, labels)
                v_loss += loss.item() * images.size(0)
                _, pred = out.max(1)
                v_correct += pred.eq(labels).sum().item()
                v_total += labels.size(0)

        val_loss = v_loss / v_total
        val_acc = v_correct / v_total

        lr = optimizer.param_groups[0]['lr']
        scheduler.step(val_acc)

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
            marker = " *BEST*"
        else:
            no_improve += 1

        torch.save(model.state_dict(), OUTPUT_MODEL_DIR / "last_model.pth")

        ep_time = time.time() - ep_start
        print(f"  Ep {epoch+1:2d}/{EPOCHS} | "
              f"Train: {100*train_acc:.1f}% loss={train_loss:.3f} | "
              f"Val: {100*val_acc:.1f}% loss={val_loss:.3f} | "
              f"LR={lr:.6f} | {ep_time:.1f}s{marker}", flush=True)

        if no_improve >= EARLY_STOPPING:
            print(f"\n  Early stopping at epoch {epoch+1}", flush=True)
            break

    total_time = time.time() - train_start
    print(f"\nTraining complete in {total_time:.0f}s ({total_time/60:.1f} min)", flush=True)
    print(f"Best validation accuracy: {100*best_val_acc:.1f}%", flush=True)

    # Save final artifacts
    shutil.copy(OUTPUT_MODEL_DIR / "best_model.pth", OUTPUT_MODEL_DIR / "vatteluttu_cnn.pth")

    with open(OUTPUT_MODEL_DIR / "label_to_idx.json", 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(label_to_idx.items())), f, ensure_ascii=False, indent=2)

    with open(OUTPUT_MODEL_DIR / "training_history.json", 'w') as f:
        json.dump(history, f, indent=2)

    # ---- Step 3: Quick verification ----
    print(f"\n--- STEP 3: Verification ---", flush=True)
    model.load_state_dict(torch.load(OUTPUT_MODEL_DIR / "best_model.pth", map_location=device))
    model.eval()

    normalize = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    labels_sorted = sorted(label_to_char.keys())
    test_labels = random.sample(labels_sorted, min(15, len(labels_sorted)))
    correct, total = 0, 0

    for label in test_labels:
        ci = label_to_idx[label]
        char = label_to_char[label]
        font = random.choice(fonts)
        img = render_char(char, font)
        tensor = normalize(img).unsqueeze(0).to(device)

        with torch.no_grad():
            out = model(tensor)
            probs = torch.softmax(out, dim=1)
            pred_idx = out.argmax(1).item()
            conf = probs[0, pred_idx].item()

        pred_label = idx_to_label[pred_idx]
        pred_char = label_to_char.get(pred_label, "?")
        ok = pred_label == label
        if ok:
            correct += 1
        total += 1
        mark = "OK" if ok else "MISS"
        print(f"  [{mark}] Expected: {label} ({char}) -> Predicted: {pred_label} ({pred_char}) conf={100*conf:.0f}%", flush=True)

    print(f"\n  Verification: {correct}/{total} correct ({100*correct/total:.0f}%)", flush=True)

    print(f"\n{'='*60}", flush=True)
    print(f"DONE! Best val accuracy: {100*best_val_acc:.1f}%", flush=True)
    print(f"Model saved to: {OUTPUT_MODEL_DIR}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == "__main__":
    main()

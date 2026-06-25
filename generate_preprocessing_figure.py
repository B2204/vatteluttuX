"""
Generate Fig. 2: Preprocessing Pipeline figure for the VattalettuX research paper.
Uses the actual user-provided Vatteluttu script image.
Shows: (a) Original Image, (b) Grayscale, (c) Binarized, (d) Noise-Removed
"""
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# ─── Step 1: Load the real Vatteluttu script image ───────────────────────────

IMAGE_PATH = r"C:\Users\Asus\.gemini\antigravity\brain\tempmediaStorage\media__1771404092898.png"

original_bgr = cv2.imread(IMAGE_PATH)
if original_bgr is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

# ─── Step 2: Apply preprocessing stages ──────────────────────────────────────

# (b) Grayscale
gray = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2GRAY)

# (c) Binarized – Otsu's thresholding (after light denoising)
denoised_for_thresh = cv2.fastNlMeansDenoising(gray, h=10)
_, binary_otsu = cv2.threshold(denoised_for_thresh, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# (d) Noise-Removed – morphological opening to remove small speckles,
#     then closing to reconnect broken strokes
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
noise_removed = cv2.morphologyEx(binary_otsu, cv2.MORPH_OPEN,  kernel, iterations=1)
noise_removed = cv2.morphologyEx(noise_removed, cv2.MORPH_CLOSE, kernel, iterations=1)

# ─── Step 3: Compose the figure ──────────────────────────────────────────────

fig, axes = plt.subplots(1, 4, figsize=(16, 4.5))
fig.patch.set_facecolor('white')

panels = [
    (cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB), None,   '(a) Original Image'),
    (gray,                                           'gray', '(b) Grayscale'),
    (binary_otsu,                                    'gray', '(c) Binarized'),
    (noise_removed,                                  'gray', '(d) Noise-Removed'),
]

for ax, (img, cmap, label) in zip(axes, panels):
    ax.imshow(img, cmap=cmap, vmin=0, vmax=255)
    ax.set_title(label, fontsize=12, fontweight='bold', pad=9,
                 fontfamily='DejaVu Sans')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor('#444444')
        spine.set_linewidth(1.2)

plt.suptitle(
    'Fig. 2. Preprocessing Pipeline',
    fontsize=13, fontweight='bold', y=0.02,
    fontfamily='DejaVu Sans', color='#222222'
)

plt.tight_layout(rect=[0, 0.07, 1, 1])

# ─── Step 4: Save ────────────────────────────────────────────────────────────

out_path = os.path.join(
    r"f:\final mca project\VattalettuX\docs\assets",
    "fig2_preprocessing_pipeline.png"
)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
print(f"Saved: {out_path}")
plt.close()

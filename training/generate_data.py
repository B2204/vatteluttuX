"""
VatteluttuX - Synthetic Data Generator

Generate training images by rendering Tamil characters with various fonts.
"""
import os
import sys
import json
import random
import io
from pathlib import Path

# Set stdout to UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from typing import List, Tuple, Optional, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

# Try to import tqdm
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.core.label_mappings import LABEL_TO_CHAR, CHARACTER_MAP


class DataGenerator:
    """Generate synthetic training images for Vatteluttu OCR."""
    
    def __init__(
        self,
        fonts_dir: Path,
        output_dir: Path,
        image_size: int = 64,
        samples_per_class: int = 1000
    ):
        """
        Initialize the data generator.
        
        Args:
            fonts_dir: Directory containing .ttf/.otf font files
            output_dir: Directory to save generated images
            image_size: Size of output images (square)
            samples_per_class: Number of samples to generate per class
        """
        self.fonts_dir = Path(fonts_dir)
        self.output_dir = Path(output_dir)
        self.image_size = image_size
        self.samples_per_class = samples_per_class
        
        self.fonts: List[ImageFont.FreeTypeFont] = []
        self.font_sizes = [36, 40, 44, 48, 52, 56]
        
    def load_fonts(self) -> int:
        """
        Load all fonts from the fonts directory.
        
        Returns:
            Number of fonts loaded
        """
        self.fonts = []
        font_files = list(self.fonts_dir.glob("*.ttf")) + list(self.fonts_dir.glob("*.otf"))
        
        for font_path in font_files:
            for size in self.font_sizes:
                try:
                    font = ImageFont.truetype(str(font_path), size)
                    self.fonts.append(font)
                except Exception as e:
                    print(f"Could not load font {font_path}: {e}")
        
        print(f"Loaded {len(self.fonts)} font variations")
        return len(self.fonts)
    
    def create_base_image(self, char: str, font: ImageFont.FreeTypeFont) -> Image.Image:
        """
        Create a base image with a character.
        
        Args:
            char: Character to render
            font: Font to use
        
        Returns:
            PIL Image with character centered
        """
        # Create white background
        img = Image.new('L', (self.image_size, self.image_size), 255)
        draw = ImageDraw.Draw(img)
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the character
        x = (self.image_size - text_width) // 2 - bbox[0]
        y = (self.image_size - text_height) // 2 - bbox[1]
        
        # Draw black text
        draw.text((x, y), char, font=font, fill=0)
        
        return img
    
    def apply_augmentations(self, img: Image.Image) -> Image.Image:
        """
        Apply random augmentations to an image.
        
        Args:
            img: Input PIL Image
        
        Returns:
            Augmented PIL Image
        """
        # Random rotation (-15 to +15 degrees)
        if random.random() > 0.3:
            angle = random.uniform(-15, 15)
            img = img.rotate(angle, fillcolor=255, expand=False)
        
        # Random perspective transform
        if random.random() > 0.4:
            width, height = img.size
            # Four corners: [top-left, top-right, bottom-right, bottom-left]
            # Standard: [(0, 0), (W, 0), (W, H), (0, H)]
            shift = self.image_size * 0.1
            points = [
                (random.uniform(0, shift), random.uniform(0, shift)),
                (random.uniform(width - shift, width), random.uniform(0, shift)),
                (random.uniform(width - shift, width), random.uniform(height - shift, height)),
                (random.uniform(0, shift), random.uniform(height - shift, height))
            ]
            
            def find_coeffs(pa, pb):
                matrix = []
                for p1, p2 in zip(pa, pb):
                    matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
                    matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
                A = np.matrix(matrix, dtype=float)
                B = np.array(pb).reshape(8)
                res = np.linalg.solve(A, B)
                return np.array(res).reshape(8)

            coeffs = find_coeffs(
                [(0, 0), (width, 0), (width, height), (0, height)],
                points
            )
            img = img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC, fillcolor=255)

        # Random brightness adjustment
        if random.random() > 0.3:
            enhancer = ImageEnhance.Brightness(img)
            factor = random.uniform(0.7, 1.3)
            img = enhancer.enhance(factor)
        
        # Random contrast adjustment
        if random.random() > 0.3:
            enhancer = ImageEnhance.Contrast(img)
            factor = random.uniform(0.7, 1.3)
            img = enhancer.enhance(factor)
        
        # Random slight blur
        if random.random() > 0.7:
            img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.0)))
        
        # Add noise
        if random.random() > 0.5:
            img = self._add_noise(img)
        
        # Random translation
        if random.random() > 0.3:
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            img = img.transform(
                img.size, Image.AFFINE, (1, 0, dx, 0, 1, dy),
                fillcolor=255
            )

        # Randomly "thicken" or "thin" the stroke by resizing
        if random.random() > 0.5:
            w, h = img.size
            scale = random.uniform(0.9, 1.1)
            temp = img.resize((int(w * scale), int(h * scale)), Image.BILINEAR)
            img = temp.resize((w, h), Image.BICUBIC)
        
        return img
    
    def _add_noise(self, img: Image.Image) -> Image.Image:
        """Add random noise to an image with variable intensity."""
        noise_level = random.uniform(0.01, 0.08)
        np_img = np.array(img).astype(np.float32)
        noise = np.random.normal(0, noise_level * 255, np_img.shape)
        
        # Add salt and pepper noise occasionally
        if random.random() > 0.8:
            sp_noise = np.random.choice([0, 255, -1], size=np_img.shape, p=[0.01, 0.01, 0.98])
            np_img[sp_noise == 0] = 0
            np_img[sp_noise == 255] = 255
            
        np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(np_img)
    
    def create_sequence_image(self, characters: List[str], fonts: List[ImageFont.FreeTypeFont]) -> Tuple[Image.Image, List[str]]:
        """
        Create an image containing a sequence of characters.
        """
        # Target height is fixed, width is variable
        height = self.image_size
        
        # Draw each char to find total width
        temp_draw = ImageDraw.Draw(Image.new('L', (1, 1)))
        char_images = []
        total_width = 0
        
        for char in characters:
            font = random.choice(fonts)
            bbox = temp_draw.textbbox((0, 0), char, font=font)
            w = bbox[2] - bbox[0]
            # Add some random spacing
            spacing = random.randint(2, 10)
            
            char_img = Image.new('L', (w + spacing, height), 255)
            draw = ImageDraw.Draw(char_img)
            # Center vertically
            char_h = bbox[3] - bbox[1]
            y = (height - char_h) // 2 - bbox[1]
            draw.text((0, y), char, font=font, fill=0)
            
            char_images.append(char_img)
            total_width += char_img.width
        
        # Create full sequence image
        seq_img = Image.new('L', (total_width + 20, height), 255)
        curr_x = 10
        for char_img in char_images:
            seq_img.paste(char_img, (curr_x, 0))
            curr_x += char_img.width
            
        return seq_img, characters

    def generate_sequence_dataset(self, split: str = "train", num_sequences: int = 1000, min_len: int = 3, max_len: int = 10):
        """
        Generate a dataset of character sequences.
        """
        output_dir = self.output_dir / split / "sequences"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        all_labels = list(LABEL_TO_CHAR.keys())
        all_chars = list(LABEL_TO_CHAR.values())
        
        labels_file = self.output_dir / split / "sequence_labels.json"
        sequence_data = {}
        
        for i in tqdm(range(num_sequences), desc=f"Generating {split} sequences"):
            length = random.randint(min_len, max_len)
            seq_indices = [random.randint(0, len(all_chars) - 1) for _ in range(length)]
            chars = [all_chars[idx] for idx in seq_indices]
            labels = [all_labels[idx] for idx in seq_indices]
            
            img, _ = self.create_sequence_image(chars, self.fonts)
            img = self.apply_augmentations(img)
            
            filename = f"seq_{i:06d}.png"
            img.save(output_dir / filename)
            
            sequence_data[filename] = labels
            
        with open(labels_file, 'w', encoding='utf-8') as f:
            json.dump(sequence_data, f, ensure_ascii=False, indent=2)
            
        return num_sequences
    
    def generate_class(self, label: str, char: str, split: str = "train") -> int:
        """
        Generate all samples for a single class.
        
        Args:
            label: Class label (e.g., 'va_001')
            char: Tamil character to render
            split: 'train' or 'val'
        
        Returns:
            Number of images generated
        """
        if not self.fonts:
            raise RuntimeError("No fonts loaded. Call load_fonts() first.")
        
        # Create output directory
        class_dir = self.output_dir / split / label
        class_dir.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for i in range(self.samples_per_class):
            # Select random font
            font = random.choice(self.fonts)
            
            try:
                # Create base image
                img = self.create_base_image(char, font)
                
                # Apply augmentations
                img = self.apply_augmentations(img)
                
                # Save
                filename = f"img_{i:05d}.png"
                img.save(class_dir / filename)
                count += 1
                
            except Exception as e:
                print(f"Error generating {label} sample {i}: {e}")
                continue
        
        return count
    
    def generate_all(
        self,
        train_ratio: float = 0.8,
        max_classes: Optional[int] = None
    ) -> Tuple[int, int]:
        """
        Generate training and validation data for all classes.
        
        Args:
            train_ratio: Ratio of training samples
            max_classes: Maximum number of classes (for testing)
        
        Returns:
            Tuple of (train_count, val_count)
        """
        train_samples = int(self.samples_per_class * train_ratio)
        val_samples = self.samples_per_class - train_samples
        
        train_total = 0
        val_total = 0
        
        labels = list(LABEL_TO_CHAR.items())
        if max_classes:
            labels = labels[:max_classes]
        
        for i, (label, char) in enumerate(labels):
            print(f"Generating [{i+1}/{len(labels)}] {label} ({char})...")
            
            # Generate training samples
            self.samples_per_class = train_samples
            train_total += self.generate_class(label, char, "train")
            
            # Generate validation samples
            self.samples_per_class = val_samples
            val_total += self.generate_class(label, char, "val")
            
            # Reset
            self.samples_per_class = train_samples + val_samples
        
        print(f"\nGeneration complete!")
        print(f"Training samples: {train_total}")
        print(f"Validation samples: {val_total}")
        
        return train_total, val_total

    def generate_all_sequences(self, num_train: int = 5000, num_val: int = 500):
        """Generate sequence datasets for training and validation."""
        self.load_fonts()
        print(f"Generating {num_train} training sequences...")
        self.generate_sequence_dataset("train", num_train)
        print(f"Generating {num_val} validation sequences...")
        self.generate_sequence_dataset("val", num_val)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic training data")
    parser.add_argument("--fonts-dir", type=str, required=True,
                       help="Directory containing font files")
    parser.add_argument("--output-dir", type=str, default="./data",
                       help="Output directory for generated images")
    parser.add_argument("--samples", type=int, default=1000,
                       help="Samples per class")
    parser.add_argument("--size", type=int, default=64,
                       help="Image size")
    parser.add_argument("--sequences", action="store_true", help="Generate sequence dataset")
    parser.add_argument("--num-sequences", type=int, default=1000, help="Number of sequences to generate")
    parser.add_argument("--max-classes", type=int, default=None, help="Maximum number of classes to generate")
    parser.add_argument("--label", type=str, default=None, help="Generate only this label")
    parser.add_argument("--split", type=str, default="train", choices=["train", "val"], help="Split to generate data for")
    
    args = parser.parse_args()
    
    generator = DataGenerator(
        fonts_dir=Path(args.fonts_dir),
        output_dir=Path(args.output_dir),
        image_size=args.size,
        samples_per_class=args.samples
    )
    
    if generator.load_fonts() == 0:
        print("No fonts found! Please add .ttf or .otf files to the fonts directory.")
        return
    
    if args.sequences:
        generator.generate_all_sequences(num_train=args.num_sequences, num_val=int(args.num_sequences * 0.1))
    elif args.label:
        char = LABEL_TO_CHAR[args.label]
        generator.generate_class(args.label, char, split=args.split)
    else:
        generator.generate_all(max_classes=args.max_classes)


if __name__ == "__main__":
    main()

"""
VatteluttuX - PyTorch Dataset

Dataset class for loading generated training images.
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms


class VatteluttuDataset(Dataset):
    """PyTorch Dataset for Vatteluttu character images."""
    
    def __init__(
        self,
        root_dir: str,
        split: str = "train",
        transform: Optional[Callable] = None,
        label_to_idx: Optional[Dict[str, int]] = None
    ):
        """
        Initialize the dataset.
        
        Args:
            root_dir: Root directory containing train/val folders
            split: 'train' or 'val'
            transform: Optional transforms to apply
            label_to_idx: Optional label to index mapping
        """
        self.root_dir = Path(root_dir) / split
        self.split = split
        self.transform = transform
        
        # Collect all samples
        self.samples: List[Tuple[Path, str]] = []
        self.labels: List[str] = []
        
        # Build label mapping
        if label_to_idx is None:
            label_dirs = sorted([d for d in self.root_dir.iterdir() if d.is_dir() and d.name.startswith("va_")])
            self.label_to_idx = {d.name: i for i, d in enumerate(label_dirs)}
        else:
            self.label_to_idx = label_to_idx
        
        self.idx_to_label = {v: k for k, v in self.label_to_idx.items()}
        
        # Collect all image paths
        for label_dir in self.root_dir.iterdir():
            if label_dir.is_dir() and label_dir.name in self.label_to_idx:
                for img_path in label_dir.glob("*.png"):
                    self.samples.append((img_path, label_dir.name))
                    self.labels.append(label_dir.name)
        
        print(f"Loaded {len(self.samples)} samples from {len(self.label_to_idx)} classes ({split})")
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path, label = self.samples[idx]
        
        # Load image
        image = Image.open(img_path).convert('L')  # Grayscale
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        else:
            # Default transform
            image = transforms.ToTensor()(image)
        
        # Get label index
        label_idx = self.label_to_idx[label]
        
        return image, label_idx
    
    @property
    def num_classes(self) -> int:
        return len(self.label_to_idx)
    
    def save_label_mapping(self, path: str):
        """Save label to index mapping."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.label_to_idx, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def get_default_transforms(cls, split: str = "train", image_size: int = 64):
        """Get default transforms for training/validation."""
        if split == "train":
            return transforms.Compose([
                transforms.RandomRotation(10),
                transforms.RandomAffine(degrees=0, translate=(0.05, 0.05)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5], std=[0.5])
            ])
        else:
            return transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5], std=[0.5])
            ])


class VatteluttuSequenceDataset(Dataset):
    """Dataset for Vatteluttu character sequences."""
    
    def __init__(
        self,
        root_dir: str,
        split: str = "train",
        transform: Optional[Callable] = None,
        label_to_idx: Optional[Dict[str, int]] = None
    ):
        self.root_dir = Path(root_dir) / split
        self.split = split
        self.transform = transform
        
        # Load sequence labels
        labels_file = self.root_dir / "sequence_labels.json"
        with open(labels_file, 'r', encoding='utf-8') as f:
            self.sequence_data = json.load(f)
            
        self.image_paths = sorted(list(self.sequence_data.keys()))
        
        # Build label mapping
        if label_to_idx is None:
            # Fallback to core label mapping
            core_mapping = Path(__file__).parent.parent / "backend" / "app" / "core" / "label_to_char.json"
            with open(core_mapping, 'r', encoding='utf-8') as f:
                labels = sorted(json.load(f).keys())
                self.label_to_idx = {label: i for i, label in enumerate(labels)}
        else:
            self.label_to_idx = label_to_idx
            
    def __len__(self) -> int:
        return len(self.image_paths)
        
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        img_filename = self.image_paths[idx]
        img_path = self.root_dir / "sequences" / img_filename
        
        # Load image
        image = Image.open(img_path).convert('L')
        
        if self.transform:
            image = self.transform(image)
        else:
            image = transforms.ToTensor()(image)
            
        # Get sequence of label indices
        labels = self.sequence_data[img_filename]
        label_indices = [self.label_to_idx[l] for l in labels]
        
        return image, torch.LongTensor(label_indices)


def collate_fn(batch):
    """
    Collate function for variable length sequences.
    CTC loss requires:
    - images: (batch, channels, height, width) -> padded width
    - targets: (total_seq_len) -> flattened
    - target_lengths: (batch)
    """
    images, targets = zip(*batch)
    
    # Pad images to maximum width in batch
    max_width = max(img.shape[2] for img in images)
    height = images[0].shape[1]
    
    padded_images = []
    for img in images:
        padding = max_width - img.shape[2]
        if padding > 0:
            img = torch.nn.functional.pad(img, (0, padding), value=1.0) # Pad with white
        padded_images.append(img)
        
    images = torch.stack(padded_images)
    
    # Flatten targets and get lengths
    target_lengths = torch.LongTensor([len(t) for t in targets])
    targets = torch.cat(targets)
    
    return images, targets, target_lengths


def create_dataloaders(
    data_dir: str,
    batch_size: int = 32,
    num_workers: int = 4,
    image_size: int = 64
) -> Tuple[DataLoader, DataLoader, Dict[str, int]]:
    """
    Create training and validation dataloaders.
    
    Args:
        data_dir: Root data directory
        batch_size: Batch size
        num_workers: Number of data loading workers
        image_size: Image size
    
    Returns:
        Tuple of (train_loader, val_loader, label_to_idx)
    """
    # Create datasets
    train_transform = VatteluttuDataset.get_default_transforms("train", image_size)
    val_transform = VatteluttuDataset.get_default_transforms("val", image_size)
    
    train_dataset = VatteluttuDataset(data_dir, "train", train_transform)
    val_dataset = VatteluttuDataset(
        data_dir, "val", val_transform, 
        label_to_idx=train_dataset.label_to_idx  # Use same mapping
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, train_dataset.label_to_idx


if __name__ == "__main__":
    # Test dataset
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="./data")
    args = parser.parse_args()
    
    train_loader, val_loader, label_to_idx = create_dataloaders(args.data_dir)
    
    print(f"\nDataset statistics:")
    print(f"  Training batches: {len(train_loader)}")
    print(f"  Validation batches: {len(val_loader)}")
    print(f"  Classes: {len(label_to_idx)}")
    
    # Test a batch
    images, labels = next(iter(train_loader))
    print(f"\nSample batch:")
    print(f"  Images shape: {images.shape}")
    print(f"  Labels shape: {labels.shape}")

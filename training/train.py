"""
VatteluttuX - Model Training Script

Train the CNN model on generated synthetic data.
"""
import os
import sys
import json
import time
import io
from pathlib import Path

# Set stdout to UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from typing import Dict, Optional, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from training.dataset import create_dataloaders, VatteluttuDataset, VatteluttuSequenceDataset, collate_fn
from backend.app.ml.model import VatteluttuCNN, create_model, TamilCRNN


class Trainer:
    """Model trainer with validation and checkpointing."""
    
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        output_dir: Path,
        device: torch.device,
        learning_rate: float = 1e-3,
        weight_decay: float = 1e-4
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.output_dir = Path(output_dir)
        self.device = device
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Loss function
        if isinstance(model, TamilCRNN):
            self.criterion = nn.CTCLoss(blank=model.num_classes, zero_infinity=True)
            self.model_type = "crnn"
        else:
            self.criterion = nn.CrossEntropyLoss()
            self.model_type = "cnn"
        
        # Optimizer
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = ReduceLROnPlateau(
            self.optimizer, mode='max', factor=0.5, patience=5
        )
        
        # Tracking
        self.best_val_acc = 0.0
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'lr': []
        }
    
    def train_epoch(self) -> Tuple[float, float]:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc="Training")
        for batch in pbar:
            if self.model_type == "crnn":
                images, targets, target_lengths = batch
                images = images.to(self.device)
                targets = targets.to(self.device)
                
                # Forward pass
                self.optimizer.zero_grad()
                outputs = self.model(images) # (S, N, C)
                
                input_lengths = torch.full(size=(outputs.size(1),), fill_value=outputs.size(0), dtype=torch.long).to(self.device)
                loss = self.criterion(outputs.log_softmax(2), targets, input_lengths, target_lengths)
            else:
                images, labels = batch
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Track metrics
            total_loss += loss.item() * images.size(0)
            
            if self.model_type == "cnn":
                _, predicted = outputs.max(1)
                correct += predicted.eq(labels).sum().item()
                total += labels.size(0)
                
                # Update progress bar
                pbar.set_postfix({
                    'loss': f'{loss.item():.4f}',
                    'acc': f'{100.*correct/total:.2f}%'
                })
            else:
                total += images.size(0)
                # Update progress bar
                pbar.set_postfix({
                    'loss': f'{loss.item():.4f}'
                })
        
        avg_loss = total_loss / total
        accuracy = correct / total if total > 0 and self.model_type == "cnn" else -avg_loss
        return avg_loss, accuracy
    
    def validate(self) -> Tuple[float, float]:
        """Validate the model."""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc="Validation"):
                if self.model_type == "crnn":
                    images, targets, target_lengths = batch
                    images = images.to(self.device)
                    targets = targets.to(self.device)
                    
                    outputs = self.model(images)
                    input_lengths = torch.full(size=(outputs.size(1),), fill_value=outputs.size(0), dtype=torch.long).to(self.device)
                    loss = self.criterion(outputs.log_softmax(2), targets, input_lengths, target_lengths)
                    
                    # For accuracy in CRNN, we'd need to decode. For now, just use loss for best model selection.
                    # Or a simple greedy decode accuracy
                    total_loss += loss.item() * images.size(0)
                    total += images.size(0)
                    
                    # CRNN metrics: accuracy is complex, use negative loss for best model selection
                    # We can add CER calculation here if needed
                else:
                    images, labels = batch
                    images = images.to(self.device)
                    labels = labels.to(self.device)
                    
                    outputs = self.model(images)
                    loss = self.criterion(outputs, labels)
                    
                    total_loss += loss.item() * images.size(0)
                    _, predicted = outputs.max(1)
                    correct += predicted.eq(labels).sum().item()
                    total += labels.size(0)
        
        avg_loss = total_loss / total
        accuracy = correct / total if self.model_type == "cnn" else -avg_loss # Use negative loss as "accuracy" for CRNN for best model selection
        return avg_loss, accuracy
    
    def train(self, epochs: int = 100, early_stopping: int = 15) -> Dict:
        """
        Full training loop.
        
        Args:
            epochs: Number of epochs
            early_stopping: Stop if no improvement for this many epochs
        
        Returns:
            Training history
        """
        no_improve_count = 0
        
        print(f"\nStarting training for {epochs} epochs...")
        print(f"Device: {self.device}")
        print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
        
        for epoch in range(epochs):
            print(f"\n{'='*50}")
            print(f"Epoch {epoch + 1}/{epochs}")
            print(f"{'='*50}")
            
            # Train
            train_loss, train_acc = self.train_epoch()
            
            # Validate
            val_loss, val_acc = self.validate()
            
            # Get current learning rate
            current_lr = self.optimizer.param_groups[0]['lr']
            
            # Update scheduler
            self.scheduler.step(val_acc)
            
            # Track history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['lr'].append(current_lr)
            
            # Print metrics
            print(f"\nTrain Loss: {train_loss:.4f} | Train Acc: {100*train_acc:.2f}%")
            print(f"Val Loss:   {val_loss:.4f} | Val Acc:   {100*val_acc:.2f}%")
            print(f"LR: {current_lr:.6f}")
            
            # Save best model
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                self.save_checkpoint("best_model.pth")
                print(f"[*] New best model saved! (Val Acc: {100*val_acc:.2f}%)")
                no_improve_count = 0
            else:
                no_improve_count += 1
            
            # Save last model
            self.save_checkpoint("last_model.pth")
            
            # Early stopping
            if no_improve_count >= early_stopping:
                print(f"\nEarly stopping triggered after {epoch + 1} epochs")
                break
        
        # Save training history
        self.save_history()
        
        print(f"\nTraining complete!")
        print(f"Best validation accuracy: {100*self.best_val_acc:.2f}%")
        
        return self.history
    
    def save_checkpoint(self, filename: str):
        """Save model checkpoint."""
        path = self.output_dir / filename
        torch.save(self.model.state_dict(), path)
    
    def save_history(self):
        """Save training history."""
        path = self.output_dir / "training_history.json"
        with open(path, 'w') as f:
            json.dump(self.history, f, indent=2)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Train Vatteluttu CNN model")
    parser.add_argument("--data-dir", type=str, default="./data",
                       help="Data directory")
    parser.add_argument("--output-dir", type=str, default="./backend/models",
                       help="Output directory for model")
    parser.add_argument("--epochs", type=int, default=100,
                       help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32,
                       help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3,
                       help="Learning rate")
    parser.add_argument("--size", type=int, default=64,
                       help="Image size")
    parser.add_argument("--workers", type=int, default=4,
                       help="Data loading workers")
    parser.add_argument("--model-type", type=str, default="cnn", choices=["cnn", "crnn", "tiny_cnn"],
                       help="Model type to train")
    
    args = parser.parse_args()
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Create dataloaders
    if args.model_type == "crnn":
        train_transform = VatteluttuDataset.get_default_transforms("train", args.size)
        val_transform = VatteluttuDataset.get_default_transforms("val", args.size)
        
        train_dataset = VatteluttuSequenceDataset(args.data_dir, "train", train_transform)
        val_dataset = VatteluttuSequenceDataset(args.data_dir, "val", val_transform, label_to_idx=train_dataset.label_to_idx)
        
        train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.workers, collate_fn=collate_fn)
        val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.workers, collate_fn=collate_fn)
        label_to_idx = train_dataset.label_to_idx
    else:
        train_loader, val_loader, label_to_idx = create_dataloaders(
            args.data_dir,
            batch_size=args.batch_size,
            num_workers=args.workers,
            image_size=args.size
        )
    
    # Save label mapping
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "label_to_idx.json", 'w', encoding='utf-8') as f:
        json.dump(label_to_idx, f, ensure_ascii=False, indent=2)
    
    # Create model
    num_classes = len(label_to_idx)
    # Fix: use the model_type and pass to create_model
    model = create_model(model_type=args.model_type, num_classes=num_classes)
    
    # Create trainer
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        output_dir=output_dir,
        device=device,
        learning_rate=args.lr
    )
    
    # Train
    trainer.train(epochs=args.epochs)
    
    # Copy best model to expected location
    import shutil
    target_model_name = "vatteluttu_crnn.pth" if args.model_type == "crnn" else "vatteluttu_cnn.pth"
    shutil.copy(output_dir / "best_model.pth", output_dir / target_model_name)
    print(f"\nModel saved to: {output_dir / target_model_name}")


if __name__ == "__main__":
    main()

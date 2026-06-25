"""
VatteluttuX - Model Inference

Load model and perform inference on character images.
"""
import torch
import numpy as np
import cv2
from pathlib import Path
from typing import Tuple, List, Optional
import json

from app.ml.model import VatteluttuCNN, create_model, TamilCRNN
from app.ml.preprocessing import preprocess_character_crop, to_grayscale
from app.ml.mapping import TamilMapper
from app.core.label_mappings import IDX_TO_LABEL, LABEL_TO_CHAR, NUM_CLASSES
from app.core.config import settings


class VatteluttuInference:
    """Inference wrapper for the Vatteluttu CNN model."""
    
    def __init__(self, model_path: Optional[Path] = None, model_type: str = "cnn"):
        """
        Initialize the inference engine.
        
        Args:
            model_path: Path to pretrained model weights
            model_type: "cnn" or "crnn"
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path or (settings.MODEL_PATH if model_type == "cnn" else Path(str(settings.MODEL_PATH).replace("cnn", "crnn")))
        self.model_type = model_type
        self.model = None
        self.mapper = TamilMapper()
        self.loaded = False
        
    def load_model(self) -> bool:
        """
        Load the model weights.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            # Initialize the model first
            if self.model is None:
                # Create the model with default num_classes
                self.model = create_model(model_type=self.model_type, num_classes=NUM_CLASSES)
            
            # Load state dict to detect model type and class count automatically
            if self.model_path.exists():
                state_dict = torch.load(self.model_path, map_location=self.device, weights_only=False)
                
                # Detect num_classes from the output layer (supports both VatteluttuCNN and TinyCNN)
                detected_model_type = self.model_type
                if "classifier.4.weight" in state_dict:
                    weights_num_classes = state_dict["classifier.4.weight"].shape[0]
                    detected_model_type = "cnn"
                elif "fc2.weight" in state_dict:
                    weights_num_classes = state_dict["fc2.weight"].shape[0]
                    detected_model_type = "tiny_cnn"
                else:
                    weights_num_classes = self.model.num_classes
                
                if weights_num_classes != self.model.num_classes or detected_model_type != self.model_type:
                    print(f"Detected {weights_num_classes}-class {detected_model_type} model. Re-initializing...")
                    self.model = create_model(model_type=detected_model_type, num_classes=weights_num_classes)
                    self.model_type = detected_model_type
                    
                    # Load targeted mapping if available in same directory
                    target_map_path = self.model_path.parent / "label_to_idx.json"
                    if target_map_path.exists():
                        with open(target_map_path, 'r') as f:
                            t_map = json.load(f)
                            self.target_idx_to_label = {int(v): k for k, v in t_map.items()}
                            print(f"Loaded mapping for {weights_num_classes} classes from {target_map_path.name}")
                    else:
                        from app.core.label_mappings import get_all_labels
                        all_labs = get_all_labels()
                        self.target_idx_to_label = {i: label for i, label in enumerate(all_labs[:weights_num_classes])}
                        print(f"Warning: No label_to_idx.json found. Using first {weights_num_classes} labels as fallback.")
                
                self.model.load_state_dict(state_dict, strict=False)
                print(f"Loaded {self.model_type} model weights from {self.model_path}")
            else:
                print(f"No pretrained weights found at {self.model_path}, using random initialization")
                self.target_idx_to_label = None
            
            self.model.to(self.device)
            self.model.eval()
            self.loaded = True
            return True
            
        except Exception as e:
            import traceback
            print(f"Error loading model: {e}")
            traceback.print_exc()
            return False
    
    def predict_single(
        self,
        image: np.ndarray,
        top_k: int = 5
    ) -> Tuple[str, float, List[Tuple[str, float]]]:
        """
        Predict a single character image.
        
        Args:
            image: Character image (any size, will be preprocessed)
            top_k: Number of top predictions to return
        
        Returns:
            Tuple of (best_label, confidence, top_k_predictions)
        """
        if not self.loaded:
            if not self.load_model():
                raise RuntimeError("Model not loaded")
        
        # Preprocess image
        processed = preprocess_character_crop(image)
        
        # Convert to tensor
        tensor = torch.from_numpy(processed).unsqueeze(0).to(self.device)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(tensor)
            
            if self.model_type in ("cnn", "tiny_cnn"):
                probs = torch.softmax(outputs, dim=1)[0]
                # Get top-k predictions
                top_probs, top_indices = torch.topk(probs, min(top_k, NUM_CLASSES))
                
                top_k_preds = []
                for prob, idx in zip(top_probs.cpu().numpy(), top_indices.cpu().numpy()):
                    if getattr(self, 'target_idx_to_label', None):
                        label = self.target_idx_to_label.get(idx, "va_001")
                    else:
                        label = IDX_TO_LABEL[idx]
                    top_k_preds.append((label, float(prob)))
            else:
                # CRNN output: (seq_len, batch, num_classes + 1)
                try:
                    labels = self.decode_ctc(outputs)
                    if labels:
                        best_label = labels[0]
                        # Estimate confidence as mean of max probs
                        if outputs.dim() >= 3:
                            probs = torch.softmax(outputs, dim=2)
                            conf = float(torch.max(probs, dim=2)[0].mean())
                        else:
                            # Fallback for unexpected tensor shape
                            probs = torch.softmax(outputs, dim=1)[0]
                            conf = float(torch.max(probs))
                    else:
                        best_label = "va_001"
                        conf = 0.0
                except Exception as e:
                    print(f"CRNN prediction fallback error: {e}")
                    best_label = "va_001"
                    conf = 0.0
                
                return best_label, conf, [(best_label, conf)]
        
        best_label = top_k_preds[0][0]
        best_conf = top_k_preds[0][1]
        
        return best_label, best_conf, top_k_preds
    
    def predict_batch(
        self,
        images: List[np.ndarray]
    ) -> List[Tuple[str, float]]:
        """
        Predict a batch of character images.
        
        Args:
            images: List of character images
        
        Returns:
            List of (label, confidence) tuples
        """
        if not self.loaded:
            if not self.load_model():
                raise RuntimeError("Model not loaded")
        
        if not images:
            return []
        
        # Preprocess all images
        processed = np.stack([preprocess_character_crop(img) for img in images])
        
        # Convert to tensor
        tensor = torch.from_numpy(processed).to(self.device)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(tensor)
            
            if self.model_type in ("cnn", "tiny_cnn"):
                probs = torch.softmax(outputs, dim=1)
                best_probs, best_indices = torch.max(probs, dim=1)
                
                results = []
                for prob, idx in zip(best_probs.cpu().numpy(), best_indices.cpu().numpy()):
                    label = IDX_TO_LABEL[idx]
                    results.append((label, float(prob)))
            else:
                # For CRNN batch prediction on character crops
                results = []
                # Unfortunately decode_ctc is defined for single batch currently
                # Let's just process one by one for now or update decode_ctc
                for i in range(outputs.size(1)):
                    single_logits = outputs[:, i:i+1, :]
                    labels = self.decode_ctc(single_logits)
                    label = labels[0] if labels else "va_001"
                    results.append((label, 1.0)) # Placeholder confidence
                    
        return results

    def decode_ctc(self, logits: torch.Tensor) -> List[str]:
        """
        Greedy decoding for CTC outputs.
        """
        # logits shape: (seq_len, 1, num_classes + 1)
        probs = torch.softmax(logits, dim=2)
        indices = torch.argmax(probs, dim=2).squeeze(1) # (seq_len)
        
        # CTC Greedy Decoding
        labels = []
        prev_idx = -1
        blank_idx = NUM_CLASSES # According to model.py
        
        for idx in indices.cpu().numpy():
            if idx != blank_idx and idx != prev_idx:
                labels.append(IDX_TO_LABEL[idx])
            prev_idx = idx
            
        return labels

    def predict_sequence(self, image: np.ndarray) -> str:
        """
        Predict a sequence of characters from an image (line/word).
        """
        if not self.loaded:
            self.load_model()
            
        # Preprocess (height-fixed resize)
        # Standardize to height 64 as expected by the CRNN model
        image = to_grayscale(image)
        h, w = image.shape[:2]
        new_w = int(w * 64 / h)
        resized = cv2.resize(image, (new_w, 64), interpolation=cv2.INTER_AREA)
        
        # Normalize to [-1, 1] range (matches training)
        img_tensor = (torch.from_numpy(resized).float().unsqueeze(0).unsqueeze(0).to(self.device) / 127.5) - 1.0
        
        with torch.no_grad():
            logits = self.model(img_tensor)
            labels = self.decode_ctc(logits)
            
        # Map to modern Tamil
        modern_text = self.mapper.map_sequence(labels)
        return modern_text


# Global inference instance
_inference: Optional[VatteluttuInference] = None


def get_inference() -> VatteluttuInference:
    """Get or create the global inference instance."""
    global _inference
    if _inference is None:
        _inference = VatteluttuInference()
    return _inference


def predict_character(image: np.ndarray) -> Tuple[str, float]:
    """
    Convenience function to predict a single character.
    
    Args:
        image: Character image
    
    Returns:
        Tuple of (label, confidence)
    """
    inference = get_inference()
    label, conf, _ = inference.predict_single(image)
    return label, conf

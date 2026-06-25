"""
VatteluttuX - Traced Image Generation

Draw bounding boxes and annotations on images.
"""
import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
import uuid

from app.ocr.segmentation import BoundingBox
from app.core.config import settings


def draw_bounding_boxes(
    image: np.ndarray,
    boxes: List[BoundingBox],
    labels: Optional[List[str]] = None,
    confidences: Optional[List[float]] = None,
    box_color: Tuple[int, int, int] = (0, 255, 0),
    text_color: Tuple[int, int, int] = (255, 255, 255),
    thickness: int = 2,
    font_scale: float = 0.5
) -> np.ndarray:
    """
    Draw bounding boxes on an image.
    
    Args:
        image: Input image (will be copied)
        boxes: List of bounding boxes
        labels: Optional labels to display
        confidences: Optional confidence scores
        box_color: BGR color for boxes
        text_color: BGR color for text
        thickness: Box line thickness
        font_scale: Font scale for labels
    
    Returns:
        Annotated image
    """
    # Make a copy to avoid modifying original
    annotated = image.copy()
    
    # Convert to BGR if grayscale
    if len(annotated.shape) == 2:
        annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)
    
    for i, box in enumerate(boxes):
        # Draw rectangle
        pt1 = (box.x, box.y)
        pt2 = (box.x + box.width, box.y + box.height)
        cv2.rectangle(annotated, pt1, pt2, box_color, thickness)
        
        # Draw label if provided
        if labels and i < len(labels):
            label_text = labels[i]
            
            # Add confidence if available
            if confidences and i < len(confidences):
                label_text += f" ({confidences[i]:.2f})"
            
            # Draw text background
            text_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)[0]
            bg_pt1 = (box.x, box.y - text_size[1] - 4)
            bg_pt2 = (box.x + text_size[0] + 4, box.y)
            cv2.rectangle(annotated, bg_pt1, bg_pt2, box_color, -1)
            
            # Draw text
            text_pt = (box.x + 2, box.y - 4)
            cv2.putText(annotated, label_text, text_pt, cv2.FONT_HERSHEY_SIMPLEX,
                       font_scale, text_color, 1, cv2.LINE_AA)
    
    return annotated


def create_traced_image(
    original_image: np.ndarray,
    boxes: List[BoundingBox],
    labels: List[str],
    confidences: List[float],
    tamil_chars: List[str]
) -> np.ndarray:
    """
    Create a traced image with bounding boxes and Tamil character annotations.
    
    Args:
        original_image: Original input image
        boxes: Character bounding boxes
        labels: Predicted labels
        confidences: Prediction confidences
        tamil_chars: Modern Tamil characters
    
    Returns:
        Annotated image
    """
    # Use Tamil characters as labels if available
    display_labels = tamil_chars if tamil_chars else labels
    
    return draw_bounding_boxes(
        original_image,
        boxes,
        labels=display_labels,
        confidences=confidences,
        box_color=(0, 200, 0),
        text_color=(255, 255, 255),
        thickness=2
    )


def save_traced_image(
    image: np.ndarray,
    output_dir: Optional[Path] = None
) -> str:
    """
    Save a traced image and return its path.
    
    Args:
        image: Annotated image to save
        output_dir: Directory to save to (default: media/traced)
    
    Returns:
        Relative path to saved image
    """
    if output_dir is None:
        output_dir = settings.MEDIA_DIR / "traced"
    
    # Create directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    filename = f"{uuid.uuid4().hex[:12]}.png"
    filepath = output_dir / filename
    
    # Save image
    cv2.imwrite(str(filepath), image)
    
    # Return relative path for API
    return f"/media/traced/{filename}"

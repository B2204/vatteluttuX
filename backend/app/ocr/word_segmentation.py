"""
VatteluttuX - Word Segmentation

Group character bounding boxes into word clusters based on horizontal spacing.
Supports multi-line paragraphs by detecting lines first, then words within each line.
"""
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass

from app.ocr.segmentation import BoundingBox, detect_lines


@dataclass
class WordGroup:
    """A group of character bounding boxes forming a word."""
    boxes: List[BoundingBox]
    word_index: int
    line_index: int = 0  # Which line this word belongs to
    
    @property
    def bbox(self) -> BoundingBox:
        """Get the bounding box encompassing all characters in the word."""
        if not self.boxes:
            return BoundingBox(0, 0, 0, 0)
        
        min_x = min(b.x for b in self.boxes)
        min_y = min(b.y for b in self.boxes)
        max_x = max(b.x + b.width for b in self.boxes)
        max_y = max(b.y + b.height for b in self.boxes)
        
        return BoundingBox(min_x, min_y, max_x - min_x, max_y - min_y)
    
    @property
    def center_x(self) -> float:
        """Get the horizontal center of the word."""
        bbox = self.bbox
        return bbox.x + bbox.width / 2
    
    @property
    def center_y(self) -> float:
        """Get the vertical center of the word."""
        bbox = self.bbox
        return bbox.y + bbox.height / 2


def calculate_spacing_statistics(boxes: List[BoundingBox]) -> Tuple[float, float, float]:
    """
    Calculate spacing statistics from character bounding boxes.
    
    Args:
        boxes: List of character bounding boxes (assumed sorted left-to-right)
    
    Returns:
        Tuple of (avg_char_width, avg_gap, gap_std_dev)
    """
    if not boxes:
        return 0.0, 0.0, 0.0
    
    # Calculate average character width
    widths = [b.width for b in boxes]
    avg_width = np.mean(widths)
    
    # Calculate gaps between consecutive characters
    gaps = []
    for i in range(len(boxes) - 1):
        current_box = boxes[i]
        next_box = boxes[i + 1]
        gap = next_box.x - (current_box.x + current_box.width)
        gaps.append(gap)
    
    if not gaps:
        return avg_width, 0.0, 0.0
    
    avg_gap = np.mean(gaps)
    gap_std = np.std(gaps)
    
    return avg_width, avg_gap, gap_std


def detect_word_boundaries(
    boxes: List[BoundingBox],
    gap_threshold_multiplier: float = 2.0,
    min_word_gap_ratio: float = 1.2
) -> List[int]:
    """
    Detect word boundaries based on horizontal spacing analysis.
    
    Uses median-based gap analysis for robustness. A gap is considered
    a word boundary if it's significantly larger than the typical
    inter-character spacing within a word.
    
    Args:
        boxes: List of character bounding boxes (should be sorted left-to-right)
        gap_threshold_multiplier: Multiplier for median gap to detect word boundaries
        min_word_gap_ratio: Minimum ratio of word gap to median character width
    
    Returns:
        List of indices where word boundaries occur (indices point to the first
        character of the next word)
    """
    if len(boxes) <= 1:
        return []
    
    # Calculate all gaps
    gaps = []
    for i in range(len(boxes) - 1):
        current_box = boxes[i]
        next_box = boxes[i + 1]
        gap = next_box.x - (current_box.x + current_box.width)
        gaps.append(gap)
    
    if not gaps:
        return []
    
    # Use median-based statistics (robust to outliers)
    widths = sorted([b.width for b in boxes])
    median_width = widths[len(widths) // 2]
    
    sorted_gaps = sorted(gaps)
    median_gap = sorted_gaps[len(sorted_gaps) // 2]
    
    # Median absolute deviation (MAD) - robust alternative to std dev
    deviations = sorted([abs(g - median_gap) for g in gaps])
    mad = deviations[len(deviations) // 2] if deviations else 0
    
    # Method 1: Based on median gap + MAD (detects statistical outlier gaps)
    threshold_1 = median_gap + (mad * gap_threshold_multiplier)
    
    # Method 2: Based on character width (word gaps > 1.2x char width)
    threshold_2 = median_width * min_word_gap_ratio
    
    # Use the SMALLER threshold — if either method says it's a word boundary, honor it
    word_gap_threshold = min(threshold_1, threshold_2)
    
    # Ensure threshold is at least slightly larger than the median gap
    # to avoid splitting every character into its own word
    word_gap_threshold = max(word_gap_threshold, median_gap * 1.5)
    
    # Detect boundaries
    boundaries = []
    for i, gap in enumerate(gaps):
        if gap >= word_gap_threshold:
            boundaries.append(i + 1)
    
    return boundaries


def group_chars_into_words(
    boxes: List[BoundingBox],
    gap_threshold_multiplier: float = 1.5,
    min_word_gap_ratio: float = 1.2
) -> List[WordGroup]:
    """
    Group character bounding boxes into word clusters.
    
    Supports multi-line paragraphs: first groups boxes into lines,
    then detects word boundaries within each line independently.
    
    Args:
        boxes: List of character bounding boxes (assumed sorted in reading order)
        gap_threshold_multiplier: Multiplier for gap detection sensitivity
        min_word_gap_ratio: Minimum ratio for word gap detection
    
    Returns:
        List of WordGroup objects, each containing character boxes for one word
    """
    if not boxes:
        return []
    
    # Detect text lines first
    lines = detect_lines(boxes)
    
    words = []
    word_index = 0
    
    for line_idx, line_boxes in enumerate(lines):
        if not line_boxes:
            continue
        
        # Detect word boundaries within this line
        boundaries = detect_word_boundaries(
            line_boxes,
            gap_threshold_multiplier=gap_threshold_multiplier,
            min_word_gap_ratio=min_word_gap_ratio
        )
        
        # Group characters into words within this line
        current_word_boxes = []
        boundary_set = set(boundaries)
        
        for i, box in enumerate(line_boxes):
            if i in boundary_set and current_word_boxes:
                # Save current word and start new one
                words.append(WordGroup(
                    boxes=current_word_boxes,
                    word_index=word_index,
                    line_index=line_idx
                ))
                word_index += 1
                current_word_boxes = []
            
            current_word_boxes.append(box)
        
        # Add the last word of this line
        if current_word_boxes:
            words.append(WordGroup(
                boxes=current_word_boxes,
                word_index=word_index,
                line_index=line_idx
            ))
            word_index += 1
    
    return words


def analyze_word_spacing(boxes: List[BoundingBox], verbose: bool = False) -> dict:
    """
    Analyze spacing characteristics for debugging/tuning.
    
    Args:
        boxes: List of character bounding boxes
        verbose: Print detailed statistics
    
    Returns:
        Dictionary with spacing statistics
    """
    avg_width, avg_gap, gap_std = calculate_spacing_statistics(boxes)
    
    # Calculate all gaps
    gaps = []
    for i in range(len(boxes) - 1):
        current_box = boxes[i]
        next_box = boxes[i + 1]
        gap = next_box.x - (current_box.x + current_box.width)
        gaps.append(gap)
    
    # Detect lines
    lines = detect_lines(boxes)
    
    stats = {
        'avg_char_width': avg_width,
        'avg_gap': avg_gap,
        'gap_std_dev': gap_std,
        'min_gap': min(gaps) if gaps else 0,
        'max_gap': max(gaps) if gaps else 0,
        'num_chars': len(boxes),
        'num_lines': len(lines),
        'gaps': gaps
    }
    
    if verbose:
        print(f"=== Word Spacing Analysis ===")
        print(f"Characters: {stats['num_chars']}")
        print(f"Lines: {stats['num_lines']}")
        print(f"Avg Character Width: {avg_width:.2f}px")
        print(f"Avg Gap: {avg_gap:.2f}px")
        print(f"Gap Std Dev: {gap_std:.2f}px")
        print(f"Min Gap: {stats['min_gap']:.2f}px")
        print(f"Max Gap: {stats['max_gap']:.2f}px")
        print(f"Suggested Word Threshold: {avg_width * 1.2:.2f}px - {avg_width * 2.0:.2f}px")
    
    return stats

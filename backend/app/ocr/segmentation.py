"""
VatteluttuX - Character Segmentation

Segment characters from inscription images using connected components.
"""
import cv2
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class BoundingBox:
    """Bounding box for a detected character."""
    x: int
    y: int
    width: int
    height: int
    
    @property
    def area(self) -> int:
        return self.width * self.height
    
    @property
    def center_x(self) -> float:
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        return self.y + self.height / 2
    
    def to_list(self) -> List[int]:
        return [self.x, self.y, self.width, self.height]
    
    def crop(self, image: np.ndarray) -> np.ndarray:
        """Extract the region from an image."""
        return image[self.y:self.y + self.height, self.x:self.x + self.width]


def find_connected_components(
    binary_image: np.ndarray,
    min_area: int = 100,
    max_area: int = None,
    horizontal_merge_gap: int = 10
) -> List[BoundingBox]:
    """
    Find connected components and merge those within a horizontal gap.
    
    Args:
        binary_image: Binary image (white characters on black background)
        min_area: Minimum component area to consider
        max_area: Maximum component area
        horizontal_merge_gap: Max pixel distance to merge horizontally.
            If set to -1, an adaptive gap based on avg component width is used.
    
    Returns:
        List of bounding boxes for detected components
    """
    if max_area is None:
        max_area = binary_image.shape[0] * binary_image.shape[1] * 0.8
    
    # 1. Find initial connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary_image, connectivity=8
    )
    
    initial_boxes = []
    for i in range(1, num_labels):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        
        if area >= 3 and area <= max_area:
            initial_boxes.append(BoundingBox(x, y, w, h))
            
    if not initial_boxes:
        return []
    
    # Compute adaptive merge gap if requested
    if horizontal_merge_gap == -1:
        avg_width = sum(b.width for b in initial_boxes) / len(initial_boxes)
        # Only bridge tiny gaps (broken strokes), not inter-character spacing
        horizontal_merge_gap = max(2, min(5, int(avg_width * 0.1)))
        
    # 2. Merge boxes that are very close horizontally (for broken Vatteluttu strokes)
    # Sort by X
    initial_boxes.sort(key=lambda b: b.x)
    
    merged_boxes = []
    if initial_boxes:
        current = initial_boxes[0]
        for next_box in initial_boxes[1:]:
            # Check overlap or proximity
            vertical_overlap = max(0, min(current.y + current.height, next_box.y + next_box.height) - max(current.y, next_box.y))
            min_height = min(current.height, next_box.height)
            
            if (next_box.x <= current.x + current.width + horizontal_merge_gap) and (vertical_overlap > 0 or abs(current.center_y - next_box.center_y) < min_height * 0.3):
                # Merge
                x = min(current.x, next_box.x)
                y = min(current.y, next_box.y)
                w = max(current.x + current.width, next_box.x + next_box.width) - x
                h = max(current.y + current.height, next_box.y + next_box.height) - y
                current = BoundingBox(x, y, w, h)
            else:
                if current.area >= min_area:
                    merged_boxes.append(current)
                current = next_box
        
        if current.area >= min_area:
            merged_boxes.append(current)
            
    return merged_boxes


def filter_noise_components(
    binary_image: np.ndarray,
    boxes: List[BoundingBox],
    min_solidity: float = 0.3,
    min_aspect_ratio: float = 0.2,
    max_aspect_ratio: float = 5.0
) -> List[BoundingBox]:
    """
    Filter out noise components based on shape quality metrics.
    
    Inspired by research on Tamil inscription recognition, which emphasizes
    filtering components based on solidity (ratio of component area to convex hull area)
    and aspect ratio to distinguish real characters from cracks and deterioration.
    
    Args:
        binary_image: Binary image used for contour analysis
        boxes: List of bounding boxes
        min_solidity: Minimum solidity ratio (0-1)
        min_aspect_ratio: Minimum width/height ratio
        max_aspect_ratio: Maximum width/height ratio
    
    Returns:
        Filtered list of bounding boxes
    """
    if not boxes:
        return []
    
    filtered = []
    for box in boxes:
        # Calculate aspect ratio
        aspect_ratio = box.width / box.height if box.height > 0 else 0
        
        # Skip extremely elongated components (likely cracks/noise)
        if aspect_ratio < min_aspect_ratio or aspect_ratio > max_aspect_ratio:
            continue
        
        # Calculate solidity (component area / convex hull area)
        # Extract the component region
        crop = box.crop(binary_image)
        contours, _ = cv2.findContours(crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            continue
        
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        component_area = cv2.contourArea(largest_contour)
        
        if component_area == 0:
            continue
        
        # Get convex hull
        hull = cv2.convexHull(largest_contour)
        hull_area = cv2.contourArea(hull)
        
        # Calculate solidity
        solidity = component_area / hull_area if hull_area > 0 else 0
        
        # Filter by solidity (real characters typically have higher solidity)
        if solidity >= min_solidity:
            filtered.append(box)
    
    return filtered


def filter_by_median_size(
    boxes: List[BoundingBox],
    min_ratio: float = 0.3
) -> List[BoundingBox]:
    """
    Filter out boxes that are much smaller than the median size.
    Removes tiny noise artifacts while keeping real characters.
    
    Args:
        boxes: List of bounding boxes
        min_ratio: Minimum ratio of box height to median height (0-1)
    
    Returns:
        Filtered list of bounding boxes
    """
    if len(boxes) <= 1:
        return boxes
    
    heights = sorted(b.height for b in boxes)
    median_height = heights[len(heights) // 2]
    min_height = median_height * min_ratio
    
    widths = sorted(b.width for b in boxes)
    median_width = widths[len(widths) // 2]
    min_width = median_width * min_ratio
    
    filtered = [b for b in boxes if b.height >= min_height and b.width >= min_width]
    
    # Don't filter everything out
    return filtered if filtered else boxes


def split_merged_components(
    binary_image: np.ndarray,
    boxes: List[BoundingBox],
    width_ratio: float = 1.8
) -> List[BoundingBox]:
    """
    Split boxes that are much wider than the median (likely merged characters)
    or have complex overlapping shapes. Uses Watershed algorithm.
    
    Args:
        binary_image: Binary image for analysis
        boxes: List of bounding boxes
        width_ratio: Boxes wider than median_width * width_ratio are split
    
    Returns:
        List of bounding boxes with wide ones split
    """
    if len(boxes) <= 1:
        return boxes
    
    widths = sorted(b.width for b in boxes)
    median_width = widths[len(widths) // 2]
    max_width = median_width * width_ratio
    
    result = []
    for box in boxes:
        if box.width <= max_width:
            result.append(box)
            continue
            
        # This box is too wide, try to split using Watershed algorithm
        crop = box.crop(binary_image)
        
        # 1. Distance transform
        dist_transform = cv2.distanceTransform(crop, cv2.DIST_L2, 5)
        
        # 2. Threshold to get sure foreground (peaks)
        # Using 0.4 * max_val as threshold is a good starting point for text
        _, sure_fg = cv2.threshold(dist_transform, 0.4 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        
        # 3. Find sure background
        # Dilate the original crop to get sure background
        kernel = np.ones((3,3), np.uint8)
        sure_bg = cv2.dilate(crop, kernel, iterations=2)
        
        # 4. Find unknown region
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # 5. Marker labelling
        num_markers, markers = cv2.connectedComponents(sure_fg)
        
        if num_markers <= 2:  # 0 is bg, 1 is the whole object, meaning no split found
            result.append(box)
            continue
            
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1
        
        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        
        # 6. Apply watershed
        # Watershed requires 3 channel 8-bit image
        crop_color = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
        markers = cv2.watershed(crop_color, markers)
        
        # 7. Extract bounding boxes from markers
        sub_boxes = []
        for marker_id in range(2, num_markers + 1):
            # Create a mask for this marker
            mask = np.zeros_like(crop, dtype=np.uint8)
            mask[markers == marker_id] = 255
            
            # Find bounding box for this sub-component
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                c = max(contours, key=cv2.contourArea)
                if cv2.contourArea(c) > 10:  # Ignore tiny artifacts
                    x, y, w, h = cv2.boundingRect(c)
                    sub_boxes.append(BoundingBox(
                        box.x + x, box.y + y, w, h
                    ))
        
        if not sub_boxes:
            result.append(box)
        else:
            # Sort sub_boxes left-to-right
            sub_boxes.sort(key=lambda b: b.x)
            result.extend(sub_boxes)
            
    return result


def find_contours(
    binary_image: np.ndarray,
    min_area: int = 100,
    max_area: int = None
) -> List[BoundingBox]:
    """
    Find contours in a binary image.
    
    Args:
        binary_image: Binary image
        min_area: Minimum contour area
        max_area: Maximum contour area
    
    Returns:
        List of bounding boxes
    """
    if max_area is None:
        max_area = binary_image.shape[0] * binary_image.shape[1] * 0.5
    
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    
    boxes = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append(BoundingBox(x, y, w, h))
    
    return boxes


def sort_boxes_reading_order(
    boxes: List[BoundingBox],
    row_threshold: float = 0.5
) -> List[BoundingBox]:
    """
    Sort bounding boxes in reading order (left-to-right, top-to-bottom).
    
    Uses median-based row clustering: boxes are grouped into lines based
    on their vertical center. A box belongs to a row if its center_y is
    within row_threshold * median_height of the row's median center_y.
    
    Args:
        boxes: List of bounding boxes
        row_threshold: Fraction of median height to determine row grouping
    
    Returns:
        Sorted list of bounding boxes
    """
    if not boxes:
        return []
    
    if len(boxes) == 1:
        return list(boxes)
    
    # Use median height for more robust row grouping
    heights = sorted(b.height for b in boxes)
    median_height = heights[len(heights) // 2]
    row_gap = median_height * row_threshold
    
    # Sort by center_y first
    boxes_sorted = sorted(boxes, key=lambda b: b.center_y)
    
    # Group into rows using median center_y of the row (not pairwise comparison)
    rows = []
    current_row = [boxes_sorted[0]]
    
    for box in boxes_sorted[1:]:
        # Compare against the median center_y of the current row
        row_centers = [b.center_y for b in current_row]
        row_median_y = sorted(row_centers)[len(row_centers) // 2]
        
        if abs(box.center_y - row_median_y) < row_gap:
            current_row.append(box)
        else:
            rows.append(current_row)
            current_row = [box]
    
    rows.append(current_row)
    
    # Sort each row by x-coordinate (left to right)
    result = []
    for row in rows:
        row_sorted = sorted(row, key=lambda b: b.x)
        result.extend(row_sorted)
    
    return result


def detect_lines(
    boxes: List[BoundingBox],
    row_threshold: float = 0.5
) -> List[List[BoundingBox]]:
    """
    Detect text lines from bounding boxes.
    
    Groups boxes into line clusters based on vertical center proximity,
    then sorts each line left-to-right.
    
    Args:
        boxes: List of bounding boxes
        row_threshold: Fraction of median height to determine row grouping
    
    Returns:
        List of lines, where each line is a list of boxes sorted left-to-right.
        Lines are sorted top-to-bottom.
    """
    if not boxes:
        return []
    
    if len(boxes) == 1:
        return [list(boxes)]
    
    heights = sorted(b.height for b in boxes)
    median_height = heights[len(heights) // 2]
    row_gap = median_height * row_threshold
    
    # Sort by center_y
    boxes_sorted = sorted(boxes, key=lambda b: b.center_y)
    
    # Group into rows
    rows = []
    current_row = [boxes_sorted[0]]
    
    for box in boxes_sorted[1:]:
        row_centers = [b.center_y for b in current_row]
        row_median_y = sorted(row_centers)[len(row_centers) // 2]
        
        if abs(box.center_y - row_median_y) < row_gap:
            current_row.append(box)
        else:
            rows.append(current_row)
            current_row = [box]
    
    rows.append(current_row)
    
    # Sort each row left-to-right
    for i in range(len(rows)):
        rows[i] = sorted(rows[i], key=lambda b: b.x)
    
    return rows


def merge_overlapping_boxes(
    boxes: List[BoundingBox],
    overlap_threshold: float = 0.3
) -> List[BoundingBox]:
    """
    Merge overlapping bounding boxes.
    
    Args:
        boxes: List of bounding boxes
        overlap_threshold: IoU threshold for merging
    
    Returns:
        Merged bounding boxes
    """
    if not boxes:
        return []
    
    def iou(b1: BoundingBox, b2: BoundingBox) -> float:
        """Calculate Intersection over Union."""
        x1 = max(b1.x, b2.x)
        y1 = max(b1.y, b2.y)
        x2 = min(b1.x + b1.width, b2.x + b2.width)
        y2 = min(b1.y + b1.height, b2.y + b2.height)
        
        if x2 < x1 or y2 < y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        union = b1.area + b2.area - intersection
        return intersection / union if union > 0 else 0.0
    
    def merge(b1: BoundingBox, b2: BoundingBox) -> BoundingBox:
        """Merge two boxes."""
        x = min(b1.x, b2.x)
        y = min(b1.y, b2.y)
        x2 = max(b1.x + b1.width, b2.x + b2.width)
        y2 = max(b1.y + b1.height, b2.y + b2.height)
        return BoundingBox(x, y, x2 - x, y2 - y)
    
    merged = list(boxes)
    changed = True
    
    while changed:
        changed = False
        new_merged = []
        used = set()
        
        for i, b1 in enumerate(merged):
            if i in used:
                continue
            
            current = b1
            for j, b2 in enumerate(merged):
                if i != j and j not in used:
                    if iou(current, b2) > overlap_threshold:
                        current = merge(current, b2)
                        used.add(j)
                        changed = True
            
            new_merged.append(current)
            used.add(i)
        
        merged = new_merged
    
    return merged


def segment_characters(
    binary_image: np.ndarray,
    min_area: int = 100,
    use_contours: bool = False,
    horizontal_merge_gap: int = -1,
    apply_morphology: bool = True,
    morphology_kernel_size: int = 3,
    filter_noise: bool = True,
    min_solidity: float = 0.3
) -> List[BoundingBox]:
    """
    Segment characters from a binary image with enhanced morphological preprocessing.
    
    Args:
        binary_image: Binary image with white characters
        min_area: Minimum character area
        use_contours: Use contours instead of connected components
        horizontal_merge_gap: Gap to merge nearby components (-1 for adaptive)
        apply_morphology: Apply morphological closing to connect broken strokes
        morphology_kernel_size: Size of morphological kernel
        filter_noise: Apply noise filtering based on shape quality
        min_solidity: Minimum solidity for noise filtering
    
    Returns:
        List of bounding boxes in reading order
    """
    # Apply morphological closing to connect broken strokes
    processed_image = binary_image.copy()
    if apply_morphology:
        from app.ml.preprocessing import apply_morphology as morph_op
        processed_image = morph_op(
            processed_image, 
            operation="closing",
            kernel_size=morphology_kernel_size,
            kernel_shape="ellipse",
            iterations=1
        )
    
    # Find components
    if use_contours:
        boxes = find_contours(processed_image, min_area=min_area)
    else:
        boxes = find_connected_components(processed_image, min_area=min_area, horizontal_merge_gap=horizontal_merge_gap)
    
    # Filter noise based on component quality
    if filter_noise and boxes:
        boxes = filter_noise_components(
            processed_image,
            boxes,
            min_solidity=min_solidity
        )
    
    # Filter by median size (removes tiny noise relative to real characters)
    if len(boxes) > 2:
        boxes = filter_by_median_size(boxes, min_ratio=0.3)
    
    # Split over-merged boxes (wider than 1.8x median) using Watershed
    if len(boxes) > 1:
        boxes = split_merged_components(processed_image, boxes, width_ratio=1.8)
    
    # Merge overlapping boxes
    boxes = merge_overlapping_boxes(boxes)
    
    # Sort in reading order
    boxes = sort_boxes_reading_order(boxes)
    
    return boxes

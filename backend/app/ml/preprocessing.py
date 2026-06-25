"""
VatteluttuX - Image Preprocessing

Functions for preprocessing images before OCR.
"""
import cv2
import numpy as np
from typing import Tuple, Optional


def load_image(image_bytes: bytes) -> np.ndarray:
    """
    Load an image from bytes.
    
    Args:
        image_bytes: Raw image bytes
    
    Returns:
        OpenCV image (BGR format)
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    return img


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert image to grayscale."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def denoise(image: np.ndarray, strength: int = 10) -> np.ndarray:
    """
    Apply denoising to reduce noise in the image.
    
    Args:
        image: Grayscale image
        strength: Denoising strength (higher = more blur)
    
    Returns:
        Denoised image
    """
    return cv2.fastNlMeansDenoising(image, h=strength)


def adaptive_threshold(
    image: np.ndarray,
    block_size: int = 11,
    c: int = 2,
    invert: bool = False
) -> np.ndarray:
    """
    Apply adaptive thresholding for binarization.
    
    Args:
        image: Grayscale image
        block_size: Size of pixel neighborhood (must be odd)
        c: Constant subtracted from mean
        invert: If True, make characters white on black background
    
    Returns:
        Binary image
    """
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresh_type, block_size, c
    )


def otsu_threshold(image: np.ndarray, invert: bool = False) -> np.ndarray:
    """
    Apply Otsu's thresholding for automatic binarization.
    
    Args:
        image: Grayscale image
        invert: If True, make characters white on black background
    
    Returns:
        Binary image
    """
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    _, binary = cv2.threshold(image, 0, 255, thresh_type + cv2.THRESH_OTSU)
    return binary


def apply_morphology(
    image: np.ndarray,
    operation: str = "closing",
    kernel_size: int = 3,
    kernel_shape: str = "ellipse",
    iterations: int = 1
) -> np.ndarray:
    """
    Apply morphological operations to repair broken strokes or remove noise.
    
    Inspired by the DPB (Dynamic Profiling Bound) approach from research literature
    on Tamil inscription recognition, which uses morphological operations to handle
    broken and eroded character strokes.
    
    Args:
        image: Binary image
        operation: Type of operation ('closing', 'opening', 'dilation', 'erosion')
        kernel_size: Size of the structuring element
        kernel_shape: Shape of kernel ('rect', 'ellipse', 'cross')
        iterations: Number of times to apply the operation
    
    Returns:
        Processed binary image
    """
    # Create structuring element
    if kernel_shape == "rect":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    elif kernel_shape == "ellipse":
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    elif kernel_shape == "cross":
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernel_size, kernel_size))
    else:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    # Apply operation
    if operation == "closing":
        # Closing = Dilation followed by Erosion (fills small holes, connects broken strokes)
        result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    elif operation == "opening":
        # Opening = Erosion followed by Dilation (removes small noise)
        result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=iterations)
    elif operation == "dilation":
        result = cv2.dilate(image, kernel, iterations=iterations)
    elif operation == "erosion":
        result = cv2.erode(image, kernel, iterations=iterations)
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return result


def resize_for_model(image: np.ndarray, size: int = 64) -> np.ndarray:
    """
    Resize image for model input while maintaining aspect ratio.
    
    Args:
        image: Input image
        size: Target size (will be size x size)
    
    Returns:
        Resized image with padding to maintain aspect ratio
    """
    h, w = image.shape[:2]
    
    # Calculate scaling factor
    scale = size / max(h, w)
    new_h, new_w = int(h * scale), int(w * scale)
    
    # Resize
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Create padded image (center the character) - White background
    result = np.full((size, size), 255, dtype=np.uint8)
    y_offset = (size - new_h) // 2
    x_offset = (size - new_w) // 2
    result[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
    
    return result


def normalize_for_model(image: np.ndarray) -> np.ndarray:
    """
    Normalize image for model input to [-1, 1] range.
    Matches the normalization used during training.
    """
    return (image.astype(np.float32) / 127.5) - 1.0


def ensure_white_on_black(binary_image: np.ndarray) -> np.ndarray:
    """
    Ensure the binary image has white characters on a black background.
    
    Connected component segmentation expects white foreground (characters)
    on a black background. This function auto-detects the polarity and
    inverts if necessary.
    
    Args:
        binary_image: Binary image (0 and 255 values)
    
    Returns:
        Binary image with white characters on black background
    """
    # Count white and black pixels
    white_pixels = np.count_nonzero(binary_image)
    total_pixels = binary_image.size
    white_ratio = white_pixels / total_pixels
    
    # If more than 50% of pixels are white, the background is white
    # and characters are dark — need to invert
    if white_ratio > 0.5:
        return cv2.bitwise_not(binary_image)
    
    return binary_image


def preprocess_full(
    image: np.ndarray,
    denoise_strength: int = 10,
    use_otsu: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Full preprocessing pipeline.
    
    Args:
        image: Input image (BGR or grayscale)
        denoise_strength: Denoising strength
        use_otsu: Use Otsu's method (True) or adaptive threshold (False)
    
    Returns:
        Tuple of (grayscale_image, binary_image) where binary has
        white characters on black background
    """
    # Convert to grayscale
    gray = to_grayscale(image)
    
    # Denoise
    denoised = denoise(gray, denoise_strength)
    
    # Binarize
    if use_otsu:
        binary = otsu_threshold(denoised, invert=False)
    else:
        binary = adaptive_threshold(denoised, invert=False)
    
    # Auto-detect polarity and ensure white-on-black
    binary = ensure_white_on_black(binary)
    
    return gray, binary


def preprocess_character_crop(
    crop: np.ndarray,
    target_size: int = 64
) -> np.ndarray:
    """
    Preprocess a single character crop for model input.
    
    Args:
        crop: Character image crop (any size)
        target_size: Target size for model
    
    Returns:
        Preprocessed image ready for model (1, target_size, target_size)
    """
    # Convert to grayscale if needed
    if len(crop.shape) == 3:
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    
    # Resize with aspect ratio preservation
    resized = resize_for_model(crop, target_size)
    
    # Normalize
    normalized = normalize_for_model(resized)
    
    # Add channel dimension
    return normalized[np.newaxis, :, :]

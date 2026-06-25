"""
VatteluttuX - OCR Pipeline

Complete OCR pipeline: preprocess -> segment -> classify -> assemble.
"""
import cv2
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

from app.ml.preprocessing import load_image, preprocess_full, preprocess_character_crop
from app.ml.inference import get_inference, VatteluttuInference
from app.ocr.segmentation import segment_characters, BoundingBox
from app.ocr.traced_image import create_traced_image, save_traced_image
from app.ocr.word_segmentation import group_chars_into_words, WordGroup
from app.ocr.tamil_rules import validate_tamil_word, is_valid_tamil_text
from app.core.label_mappings import LABEL_TO_CHAR, labels_to_tamil, get_character_info
from app.core.config import settings


@dataclass
class CharacterResult:
    """Result for a single character prediction."""
    label: str
    modern_tamil: str
    confidence: float
    bbox: BoundingBox
    transliteration: str = ""


@dataclass
class WordResult:
    """Result for a single word."""
    text: str  # Modern Tamil text
    labels: List[str]  # Label sequence
    characters: List[CharacterResult]
    confidence: float  # Average of character confidences
    bbox: BoundingBox  # Bounding box encompassing entire word
    is_validated: bool  # Passed linguistic validation
    validation_warnings: List[str]  # Warnings from linguistic validation


@dataclass
class OCRResult:
    """Complete OCR result."""
    recognized_text: str  # Label sequence
    modern_text: str  # Tamil text
    characters: List[CharacterResult]
    words: List[WordResult]  # Word-level results
    traced_image_path: str
    image_width: int
    image_height: int
    warnings: List[str]


def run_ocr_pipeline(
    image_bytes: bytes,
    min_char_area: int = 100,
    confidence_threshold: float = 0.3,
    save_traced: bool = True,
    apply_morphology: bool = True,
    morphology_kernel_size: int = 3,
    filter_noise: bool = True,
    min_solidity: float = 0.3
) -> OCRResult:
    """
    Run the full OCR pipeline on an image.
    
    Args:
        image_bytes: Raw image bytes
        min_char_area: Minimum character area for segmentation
        confidence_threshold: Minimum confidence to include prediction
        save_traced: Whether to save the traced image
        apply_morphology: Apply morphological closing to connect broken strokes
        morphology_kernel_size: Size of morphological kernel (3-5 recommended)
        filter_noise: Filter components by quality metrics (solidity, aspect ratio)
        min_solidity: Minimum solidity ratio for noise filtering (0-1)
    
    Returns:
        OCRResult with predictions
    """
    warnings = []
    
    # Load image
    try:
        original_image = load_image(image_bytes)
    except Exception as e:
        raise ValueError(f"Could not load image: {e}")
    
    image_height, image_width = original_image.shape[:2]
    
    # Preprocess
    gray, binary = preprocess_full(original_image)
    
    # Segment characters - use adaptive strategy:
    # First try without morphology to preserve character separation
    # Only apply morphology if too few characters are detected (broken strokes)
    boxes = segment_characters(
        binary,
        min_area=min_char_area,
        apply_morphology=False,
        filter_noise=filter_noise,
        min_solidity=min_solidity
    )
    
    # If we got very few results, retry with morphological closing
    # (helps with broken/eroded strokes in stone inscriptions)
    if len(boxes) <= 1 and apply_morphology:
        boxes_morph = segment_characters(
            binary,
            min_area=min_char_area,
            apply_morphology=True,
            morphology_kernel_size=morphology_kernel_size,
            filter_noise=filter_noise,
            min_solidity=min_solidity
        )
        # Use morphology result only if it found more characters
        if len(boxes_morph) > len(boxes):
            boxes = boxes_morph
    
    if not boxes:
        warnings.append("No characters detected in image")
        return OCRResult(
            recognized_text="",
            modern_text="",
            characters=[],
            words=[],
            traced_image_path="",
            image_width=image_width,
            image_height=image_height,
            warnings=warnings
        )
    
    # Group characters into words based on spacing (line-aware)
    word_groups = group_chars_into_words(boxes)
    
    # Log segmentation results
    num_lines = max((wg.line_index for wg in word_groups), default=0) + 1 if word_groups else 0
    print(f"[OCR Pipeline] Segmented: {len(boxes)} characters, {num_lines} lines, {len(word_groups)} words")
    
    # Get inference engine
    inference = get_inference()
    if not inference.loaded:
        try:
            inference.load_model()
        except Exception as e:
            warnings.append(f"Model not loaded, using random predictions: {e}")
    
    # Classify characters and assemble text
    all_characters = []
    all_labels = []
    words = []
    
    # Process each word group
    for word_group in word_groups:
        word_chars = []
        word_labels = []
        
        # Classify each character in the word
        for box in word_group.boxes:
            crop = box.crop(gray)
            try:
                # Predict single character using the model
                label, confidence, _ = inference.predict_single(crop)
                modern_char = inference.mapper.map_label(label)
            except Exception as e:
                label = "va_001"
                confidence = 0.0
                modern_char = "?"
                warnings.append(f"Prediction error for box {box}: {e}")
                
            char_info = get_character_info(label) or {}
            
            char_result = CharacterResult(
                label=label,
                modern_tamil=modern_char,
                confidence=confidence,
                bbox=box,
                transliteration=char_info.get("transliteration", "")
            )
            
            word_chars.append(char_result)
            word_labels.append(label)
            all_characters.append(char_result)
            all_labels.append(label)
        
        # Assemble word text
        word_text = ''.join(char.modern_tamil for char in word_chars)
        
        # Calculate word-level confidence
        word_confidence = sum(char.confidence for char in word_chars) / len(word_chars) if word_chars else 0.0
        
        # Apply linguistic validation
        is_valid, adjusted_confidence, validation_warnings = validate_tamil_word(
            word_labels,
            word_text,
            word_confidence
        )
        
        # Create word result
        word_result = WordResult(
            text=word_text,
            labels=word_labels,
            characters=word_chars,
            confidence=adjusted_confidence,
            bbox=word_group.bbox,
            is_validated=is_valid,
            validation_warnings=validation_warnings
        )
        
        words.append(word_result)
        
        # Add validation warnings to global warnings
        if validation_warnings:
            warnings.extend([f"Word {word_group.word_index}: {w}" for w in validation_warnings])
    
    # Final recognized text sequence (label-based)
    recognized_text = " ".join(all_labels)
    
    # Assemble modern Tamil text with line-aware spacing
    if words:
        # Group words by line index
        lines_dict = {}
        for i, word in enumerate(words):
            line_idx = word_groups[i].line_index if i < len(word_groups) else 0
            if line_idx not in lines_dict:
                lines_dict[line_idx] = []
            lines_dict[line_idx].append(word.text)
        
        # Join words within each line with spaces, lines with newlines
        line_texts = []
        for line_idx in sorted(lines_dict.keys()):
            line_text = " ".join(lines_dict[line_idx])
            line_texts.append(line_text)
        
        modern_text = "\n".join(line_texts)
    elif all_characters:
        # Fallback: if no words detected, join characters without spaces
        modern_text = "".join(char.modern_tamil for char in all_characters)
    else:
        modern_text = ""

    
    # Create traced image
    traced_path = ""
    if save_traced:
        traced_image = create_traced_image(
            original_image, boxes, all_labels, [c.confidence for c in all_characters], 
            [c.modern_tamil for c in all_characters]
        )
        traced_path = save_traced_image(traced_image)
    
    return OCRResult(
        recognized_text=recognized_text,
        modern_text=modern_text,
        characters=all_characters,
        words=words,
        traced_image_path=traced_path,
        image_width=image_width,
        image_height=image_height,
        warnings=warnings
    )


def ocr_result_to_api_response(result: OCRResult) -> dict:
    """Convert OCRResult to API response format."""
    return {
        "recognized_text": result.recognized_text,
        "modern_text": result.modern_text,
        "words": [
            {
                "text": word.text,
                "labels": word.labels,
                "confidence": word.confidence,
                "bbox": word.bbox.to_list(),
                "is_validated": word.is_validated,
                "validation_warnings": word.validation_warnings,
                "num_characters": len(word.characters)
            }
            for word in result.words
        ],
        "characters": [
            {
                "label": char.label,
                "modern_tamil": char.modern_tamil,
                "confidence": char.confidence,
                "bbox": char.bbox.to_list(),
                "transliteration": char.transliteration
            }
            for char in result.characters
        ],
        "traced_image_path": result.traced_image_path,
        "image_width": result.image_width,
        "image_height": result.image_height,
        "warnings": result.warnings,
        "num_words": len(result.words),
        "num_characters": len(result.characters)
    }

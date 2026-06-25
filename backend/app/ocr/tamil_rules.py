"""
VatteluttuX - Tamil Linguistic Rules

Validate and correct character sequences using Tamil grammar rules.
"""
from typing import List, Tuple, Optional
from dataclasses import dataclass

from app.core.label_mappings import get_character_info, LABEL_TO_CHAR


@dataclass
class ValidationResult:
    """Result of linguistic validation."""
    is_valid: bool
    confidence_modifier: float  # Multiplier for confidence (0.8-1.2)
    warnings: List[str]
    suggested_corrections: List[str]


def get_character_category(label: str) -> Optional[str]:
    """
    Get the category of a character.
    
    Returns:
        'vowel', 'aytham', 'pure_consonant', 'consonant', 'uyirmei', or None
    """
    info = get_character_info(label)
    if info:
        return info.get('category')
    return None


def is_vowel(label: str) -> bool:
    """Check if a character is a vowel."""
    return get_character_category(label) == 'vowel'


def is_consonant(label: str) -> bool:
    """Check if a character is a pure consonant."""
    return get_character_category(label) in ['pure_consonant', 'consonant']


def is_uyirmei(label: str) -> bool:
    """Check if a character is uyirmei (consonant+vowel combination)."""
    return get_character_category(label) == 'uyirmei'


def validate_tamil_sequence(labels: List[str]) -> ValidationResult:
    """
    Validate a sequence of Tamil characters based on linguistic rules.
    
    Tamil word formation rules:
    1. Words can start with vowels or consonants
    2. Pure consonants (mei) typically followed by vowel signs or other consonants
    3. Uyirmei characters are standalone (consonant+vowel already combined)
    4. Certain sequences are grammatically invalid
    
    Args:
        labels: List of character labels in sequence
    
    Returns:
        ValidationResult with validation status and suggestions
    """
    if not labels:
        return ValidationResult(
            is_valid=True,
            confidence_modifier=1.0,
            warnings=[],
            suggested_corrections=[]
        )
    
    warnings = []
    confidence_modifier = 1.0
    
    # Rule 1: Check for invalid consecutive sequences
    for i in range(len(labels) - 1):
        current_label = labels[i]
        next_label = labels[i + 1]
        
        current_cat = get_character_category(current_label)
        next_cat = get_character_category(next_label)
        
        # Pure consonants followed by vowels is standard
        # Uyirmei can be followed by anything
        # Vowels followed by consonants/uyirmei is standard
        
        # Check for unusual patterns (not necessarily invalid, but lower confidence)
        if current_cat == 'pure_consonant' and next_cat == 'vowel':
            # This might indicate the characters should be merged into uyirmei
            warnings.append(f"Consecutive consonant-vowel at position {i}: might be uyirmei")
            confidence_modifier *= 0.95
    
    # Rule 2: Check sequence length (very short or very long words are unusual)
    if len(labels) == 1:
        # Single character words are valid (especially vowels)
        if not is_vowel(labels[0]):
            warnings.append("Single character word (non-vowel) is unusual")
            confidence_modifier *= 0.9
    
    if len(labels) > 15:
        warnings.append("Very long word (>15 characters) is unusual")
        confidence_modifier *= 0.85
    
    # Rule 3: First character validity
    first_cat = get_character_category(labels[0])
    if first_cat not in ['vowel', 'consonant', 'pure_consonant', 'uyirmei']:
        warnings.append(f"Unusual word starting character: {first_cat}")
        confidence_modifier *= 0.9
    
    # Determine if valid (we're lenient - mark as valid unless critical issues)
    is_valid = len(warnings) == 0 or confidence_modifier > 0.8
    
    return ValidationResult(
        is_valid=is_valid,
        confidence_modifier=max(0.7, min(1.2, confidence_modifier)),
        warnings=warnings,
        suggested_corrections=[]  # Can be enhanced later with dictionary lookup
    )


def validate_tamil_word(
    labels: List[str],
    modern_text: str,
    base_confidence: float
) -> Tuple[bool, float, List[str]]:
    """
    Validate a Tamil word and adjust confidence accordingly.
    
    Args:
        labels: List of character labels forming the word
        modern_text: Modern Tamil text of the word
        base_confidence: Average confidence from character predictions
    
    Returns:
        Tuple of (is_valid, adjusted_confidence, warnings)
    """
    result = validate_tamil_sequence(labels)
    
    # Adjust confidence based on linguistic validation
    adjusted_confidence = base_confidence * result.confidence_modifier
    
    return result.is_valid, adjusted_confidence, result.warnings


def get_common_tamil_patterns() -> List[str]:
    """
    Get common Tamil word patterns for validation.
    
    Returns:
        List of common patterns (can be expanded with actual dictionary)
    """
    # These could be expanded with actual Tamil word lists
    # For now, return empty list (future enhancement)
    return []


def suggest_word_corrections(
    labels: List[str],
    modern_text: str,
    confidence: float,
    max_suggestions: int = 3
) -> List[str]:
    """
    Suggest alternative word readings for low-confidence predictions.
    
    This is a placeholder for future enhancement with:
    - Tamil dictionary lookup
    - Edit distance calculations
    - Common confusion matrix corrections
    
    Args:
        labels: Character labels
        modern_text: Current modern Tamil text
        confidence: Word confidence score
        max_suggestions: Maximum number of suggestions
    
    Returns:
        List of suggested alternative words
    """
    suggestions = []
    
    # Future enhancements:
    # 1. Dictionary lookup for similar words
    # 2. Use character confusion matrix (e.g., va_037 often confused with va_149)
    # 3. Check for common OCR errors (merged/split characters)
    # 4. Use n-gram language models
    
    # For now, return empty list
    return suggestions


def is_valid_tamil_text(text: str) -> bool:
    """
    Quick validation that text contains valid Tamil characters.
    
    Args:
        text: Modern Tamil text string
    
    Returns:
        True if text appears to be valid Tamil
    """
    if not text:
        return False
    
    # Tamil Unicode range: U+0B80 to U+0BFF
    tamil_range_start = 0x0B80
    tamil_range_end = 0x0BFF
    
    for char in text:
        code_point = ord(char)
        if tamil_range_start <= code_point <= tamil_range_end:
            return True
    
    # Also accept '?' as placeholder for unknown characters
    return '?' in text

"""
VatteluttuX - Label Mappings
Single source of truth for Vatteluttu to Modern Tamil character mappings.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional

# Load character map from JSON
_CHARACTER_MAP_PATH = Path(__file__).parent / "character_map.json"
_LABEL_TO_CHAR_PATH = Path(__file__).parent / "label_to_char.json"

# Load mappings
with open(_LABEL_TO_CHAR_PATH, 'r', encoding='utf-8') as f:
    LABEL_TO_CHAR: Dict[str, str] = json.load(f)

with open(_CHARACTER_MAP_PATH, 'r', encoding='utf-8') as f:
    CHARACTER_MAP: Dict[str, dict] = json.load(f)

# Create reverse mapping
CHAR_TO_LABEL: Dict[str, str] = {v: k for k, v in LABEL_TO_CHAR.items()}

# Number of classes
NUM_CLASSES: int = len(LABEL_TO_CHAR)

# Create label to index mapping (for model training)
LABEL_TO_IDX: Dict[str, int] = {label: idx for idx, label in enumerate(sorted(LABEL_TO_CHAR.keys()))}
IDX_TO_LABEL: Dict[int, str] = {idx: label for label, idx in LABEL_TO_IDX.items()}


def labels_to_tamil(labels: List[str]) -> str:
    """
    Convert a list of labels to modern Tamil text.
    
    Args:
        labels: List of label strings like ['va_001', 'va_002', ...]
    
    Returns:
        Modern Tamil text string
    """
    return ''.join(LABEL_TO_CHAR.get(label, '?') for label in labels)


def get_character_info(label: str) -> Optional[dict]:
    """
    Get detailed information about a character label.
    
    Args:
        label: Label string like 'va_001'
    
    Returns:
        Dictionary with character information or None if not found
    """
    return CHARACTER_MAP.get(label)


def get_all_labels() -> List[str]:
    """Get all available labels sorted."""
    return sorted(LABEL_TO_CHAR.keys())


def get_category_labels(category: str) -> List[str]:
    """
    Get labels for a specific category.
    
    Args:
        category: One of 'vowel', 'aytham', 'pure_consonant', 'consonant', 'uyirmei'
    
    Returns:
        List of labels in that category
    """
    return [
        label for label, info in CHARACTER_MAP.items()
        if info.get('category') == category
    ]


# Export summary for debugging
if __name__ == "__main__":
    print(f"Total characters: {NUM_CLASSES}")
    print(f"Sample mappings:")
    for label in list(LABEL_TO_CHAR.keys())[:10]:
        print(f"  {label} -> {LABEL_TO_CHAR[label]}")

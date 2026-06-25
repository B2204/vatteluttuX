"""
VatteluttuX - Modern Tamil Mapping
"""
from typing import List, Dict, Optional
import json
from pathlib import Path

class TamilMapper:
    """
    Mapper to convert recognized Vatteluttu character labels to modern Tamil.
    """
    
    def __init__(self, mapping_path: Optional[Path] = None):
        """
        Initialize the mapper with label-to-character mappings.
        
        Args:
            mapping_path: Path to label_to_char.json
        """
        if mapping_path is None:
            # Default to the one in core
            mapping_path = Path(__file__).parent.parent / "core" / "label_to_char.json"
        
        self.mapping_path = mapping_path
        self._load_mapping()
        
    def _load_mapping(self):
        try:
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                self.label_to_char: Dict[str, str] = json.load(f)
        except Exception as e:
            print(f"Error loading mapping from {self.mapping_path}: {e}")
            self.label_to_char = {}
    
    def map_label(self, label: str) -> str:
        """Map a single label to its modern Tamil equivalent."""
        return self.label_to_char.get(label, "?")
    
    def map_sequence(self, labels: List[str]) -> str:
        """Map a sequence of labels to a modern Tamil string."""
        return "".join(self.map_label(label) for label in labels)
    
    def post_process(self, text: str) -> str:
        """
        Apply Tamil-specific post-processing rules.
        (e.g., handling combining characters, spellcheck placeholders)
        """
        # Placeholder for N-gram or Transformer-based correction
        return text

if __name__ == "__main__":
    # Test
    mapper = TamilMapper()
    test_labels = ["vatteluttu_86", "vatteluttu_102", "vatteluttu_99"]
    result = mapper.map_sequence(test_labels)
    print(f"Mapped {test_labels} to: {result}")

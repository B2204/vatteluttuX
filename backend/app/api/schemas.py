"""
VatteluttuX - Pydantic Schemas for API
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class CharacterPrediction(BaseModel):
    """A single character prediction with metadata."""
    label: str = Field(..., description="Character label (e.g., 'va_001')")
    modern_tamil: str = Field(..., description="Modern Tamil character")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence")
    bbox: List[int] = Field(..., description="Bounding box [x, y, width, height]")
    transliteration: Optional[str] = Field(None, description="Romanized transliteration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "label": "va_001",
                "modern_tamil": "அ",
                "confidence": 0.97,
                "bbox": [10, 20, 64, 64],
                "transliteration": "a"
            }
        }


class WordPrediction(BaseModel):
    """A single word prediction with metadata."""
    text: str = Field(..., description="Modern Tamil text for the word")
    labels: List[str] = Field(..., description="Character labels forming the word")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Word-level confidence")
    bbox: List[int] = Field(..., description="Bounding box encompassing the word")
    is_validated: bool = Field(..., description="Whether the word passed linguistic validation")
    validation_warnings: List[str] = Field(default_factory=list, description="Warnings from validation")
    num_characters: int = Field(..., description="Number of characters in the word")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "அம்மா",
                "labels": ["va_001", "va_022", "va_023"],
                "confidence": 0.94,
                "bbox": [10, 20, 150, 64],
                "is_validated": True,
                "validation_warnings": [],
                "num_characters": 3
            }
        }


class RecognitionResponse(BaseModel):
    """Response from the OCR recognition endpoint."""
    recognized_text: str = Field(..., description="Raw label sequence separated by spaces")
    modern_text: str = Field(..., description="Modern Tamil text (Unicode)")
    words: List[WordPrediction] = Field(default_factory=list, description="Word-level predictions")
    characters: List[CharacterPrediction] = Field(..., description="Per-character predictions")
    traced_image_path: str = Field(..., description="Path to traced image with bounding boxes")
    image_width: int = Field(..., description="Original image width")
    image_height: int = Field(..., description="Original image height")
    warnings: List[str] = Field(default_factory=list, description="Any warnings during processing")
    num_words: int = Field(default=0, description="Total number of words detected")
    num_characters: int = Field(default=0, description="Total number of characters detected")
    
    class Config:
        json_schema_extra = {
            "example": {
                "recognized_text": "va_001 va_014 va_047",
                "modern_text": "அகப",
                "words": [
                    {
                        "text": "அகப",
                        "labels": ["va_001", "va_014", "va_047"],
                        "confidence": 0.95,
                        "bbox": [10, 20, 200, 64],
                        "is_validated": True,
                        "validation_warnings": [],
                        "num_characters": 3
                    }
                ],
                "characters": [
                    {"label": "va_001", "modern_tamil": "அ", "confidence": 0.97, "bbox": [10, 20, 64, 64], "transliteration": "a"},
                    {"label": "va_014", "modern_tamil": "க்", "confidence": 0.94, "bbox": [80, 20, 64, 64], "transliteration": "k"},
                ],
                "traced_image_path": "/media/traced/abc123.png",
                "image_width": 800,
                "image_height": 200,
                "warnings": [],
                "num_words": 1,
                "num_characters": 3
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether the ML model is loaded")
    num_classes: int = Field(..., description="Number of character classes")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "num_classes": 247,
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for debugging")


class RecognitionHistoryResponse(BaseModel):
    """Response model for a recognition history record."""
    id: int = Field(..., description="Unique record ID")
    original_filename: str = Field(..., description="Uploaded image filename")
    recognized_text: str = Field(..., description="Raw label sequence")
    modern_text: str = Field(..., description="Modern Tamil text")
    num_characters: int = Field(0, description="Number of characters detected")
    num_words: int = Field(0, description="Number of words detected")
    avg_confidence: float = Field(0.0, description="Average confidence score")
    traced_image_path: Optional[str] = Field(None, description="Path to traced image")
    created_at: str = Field(..., description="Timestamp of recognition")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "original_filename": "inscription_01.png",
                "recognized_text": "va_001 va_014 va_047",
                "modern_text": "அகப",
                "num_characters": 3,
                "num_words": 1,
                "avg_confidence": 0.95,
                "traced_image_path": "/media/traced/abc123.png",
                "created_at": "2026-02-26T10:00:00"
            }
        }


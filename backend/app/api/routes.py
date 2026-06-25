"""
VatteluttuX - API Routes

Endpoints for OCR recognition, character info, and recognition history.
"""
import uuid
from typing import List

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.schemas import (
    HealthResponse,
    RecognitionResponse,
    CharacterPrediction,
    RecognitionHistoryResponse,
)
from app.core.config import settings
from app.core.label_mappings import (
    LABEL_TO_CHAR,
    NUM_CLASSES,
    labels_to_tamil,
    get_character_info,
    CHARACTER_MAP,
    get_category_labels,
    get_all_labels
)
from app.db.database import get_db
from app.db import crud


# Create router
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns the API status and model information.
    """
    from app.ml.inference import get_inference
    inference = get_inference()
    
    return HealthResponse(
        status="healthy",
        model_loaded=inference.loaded,
        num_classes=NUM_CLASSES,
        version=settings.API_VERSION
    )


@router.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "VatteluttuX OCR API",
        "version": settings.API_VERSION,
        "description": "API for recognizing Vatteluttu Tamil inscriptions",
        "docs": "/docs",
        "health": "/health"
    }


@router.post("/recognize", response_model=RecognitionResponse, tags=["OCR"])
async def recognize_image(
    image: UploadFile = File(..., description="Image file containing Vatteluttu inscription"),
    db: Session = Depends(get_db),
):
    """
    Recognize Vatteluttu characters in an uploaded image.
    
    Results are automatically saved to the database for history tracking.
    
    Returns:
    - Modern Tamil text
    - Per-character predictions with confidence and bounding boxes
    - Path to traced image with annotations
    """
    # Validate file type
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {image.content_type}. Please upload an image."
        )
    
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Run OCR pipeline
        from app.ocr.pipeline import run_ocr_pipeline, ocr_result_to_api_response
        
        result = run_ocr_pipeline(
            image_bytes=image_bytes,
            min_char_area=50,
            confidence_threshold=0.3
        )
        
        # Convert to API response
        response = ocr_result_to_api_response(result)
        
        # Save recognition result to database
        try:
            # Calculate average confidence from characters
            avg_conf = 0.0
            chars = response.get("characters", []) if isinstance(response, dict) else getattr(response, "characters", [])
            if chars:
                avg_conf = sum(c.get("confidence", 0) if isinstance(c, dict) else c.confidence for c in chars) / len(chars)
            
            # Get values using dict access (ocr_result_to_api_response returns a dict)
            rec_text = response.get("recognized_text", "") if isinstance(response, dict) else response.recognized_text
            mod_text = response.get("modern_text", "") if isinstance(response, dict) else response.modern_text
            n_chars = response.get("num_characters", 0) if isinstance(response, dict) else response.num_characters
            n_words = response.get("num_words", 0) if isinstance(response, dict) else response.num_words
            traced_path = response.get("traced_image_path", "") if isinstance(response, dict) else response.traced_image_path
            
            crud.save_recognition(
                db=db,
                original_filename=image.filename or "unknown",
                recognized_text=rec_text,
                modern_text=mod_text,
                num_characters=n_chars,
                num_words=n_words,
                avg_confidence=round(avg_conf, 4),
                traced_image_path=traced_path,
            )
        except Exception as db_err:
            # Don't fail the OCR request if DB save fails
            print(f"[WARNING] Failed to save recognition to DB: {db_err}")
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


# ==================== HISTORY ENDPOINTS ====================


@router.get("/history", response_model=List[RecognitionHistoryResponse], tags=["History"])
async def get_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """
    Get recognition history (newest first).
    
    This shows all past OCR recognitions saved in the MySQL database.
    You can also view these records in phpMyAdmin at http://localhost/phpmyadmin.
    """
    records = crud.get_recognition_history(db, skip=skip, limit=limit)
    total = crud.get_history_count(db)
    
    # Convert datetime to string for JSON serialization
    results = []
    for record in records:
        results.append(RecognitionHistoryResponse(
            id=record.id,
            original_filename=record.original_filename,
            recognized_text=record.recognized_text,
            modern_text=record.modern_text,
            num_characters=record.num_characters,
            num_words=record.num_words,
            avg_confidence=record.avg_confidence,
            traced_image_path=record.traced_image_path,
            created_at=record.created_at.isoformat() if record.created_at else "",
        ))
    
    return results


@router.get("/history/{record_id}", response_model=RecognitionHistoryResponse, tags=["History"])
async def get_history_record(record_id: int, db: Session = Depends(get_db)):
    """Get a single recognition history record by ID."""
    record = crud.get_recognition_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    
    return RecognitionHistoryResponse(
        id=record.id,
        original_filename=record.original_filename,
        recognized_text=record.recognized_text,
        modern_text=record.modern_text,
        num_characters=record.num_characters,
        num_words=record.num_words,
        avg_confidence=record.avg_confidence,
        traced_image_path=record.traced_image_path,
        created_at=record.created_at.isoformat() if record.created_at else "",
    )


@router.delete("/history/{record_id}", tags=["History"])
async def delete_history_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a recognition history record by ID."""
    deleted = crud.delete_recognition(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return {"message": f"Record {record_id} deleted successfully"}


# ==================== INFO ENDPOINTS ====================


@router.get("/labels", tags=["Info"])
async def get_labels():
    """Get all available character labels and their mappings."""
    return {
        "total": NUM_CLASSES,
        "labels": LABEL_TO_CHAR
    }


@router.get("/labels/{label}", tags=["Info"])
async def get_label_info(label: str):
    """Get detailed information about a specific label."""
    info = get_character_info(label)
    if not info:
        raise HTTPException(
            status_code=404,
            detail=f"Label '{label}' not found"
        )
    return {
        "label": label,
        **info
    }


@router.get("/characters", tags=["Info"])
async def get_all_characters(category: str = None):
    """
    Get all character mappings or filter by category.
    
    Args:
        category: Optional filter - 'vowel', 'aytham', 'pure_consonant', 'consonant', 'uyirmei'
    
    Returns:
        List of characters with their details
    """
    if category:
        # Get labels for specific category
        labels = get_category_labels(category)
        if not labels:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {category}. Valid categories: vowel, aytham, pure_consonant, consonant, uyirmei"
            )
    else:
        # Get all labels
        labels = get_all_labels()
    
    # Build response with character details
    characters = []
    for label in labels:
        char_info = get_character_info(label)
        if char_info:
            characters.append({
                "label": label,
                **char_info
            })
    
    return {
        "total": len(characters),
        "category": category if category else "all",
        "characters": characters
    }


@router.get("/character-map", tags=["Info"])
async def get_character_map():
    """
    Get the complete character mapping data.
    
    Returns:
        Full character map with all details and statistics
    """
    # Group by category
    categories = {
        "vowel": [],
        "aytham": [],
        "pure_consonant": [],
        "consonant": [],
        "uyirmei": []
    }
    
    for label in get_all_labels():
        char_info = get_character_info(label)
        if char_info and "category" in char_info:
            category = char_info["category"]
            if category in categories:
                categories[category].append({
                    "label": label,
                    **char_info
                })
    
    return {
        "total_characters": NUM_CLASSES,
        "categories": categories,
        "statistics": {
            "vowels": len(categories["vowel"]),
            "aytham": len(categories["aytham"]),
            "pure_consonants": len(categories["pure_consonant"]),
            "consonants": len(categories["consonant"]),
            "uyirmei": len(categories["uyirmei"])
        }
    }

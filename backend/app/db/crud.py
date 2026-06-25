"""
VatteluttuX - CRUD Operations

Create, Read, Update, Delete operations for the database.
These functions are called by the API routes.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models import RecognitionHistory


def save_recognition(
    db: Session,
    original_filename: str,
    recognized_text: str,
    modern_text: str,
    num_characters: int = 0,
    num_words: int = 0,
    avg_confidence: float = 0.0,
    traced_image_path: str = None,
) -> RecognitionHistory:
    """
    Save a new OCR recognition result to the database.
    
    Called automatically after every successful /recognize API call.
    """
    record = RecognitionHistory(
        original_filename=original_filename,
        recognized_text=recognized_text,
        modern_text=modern_text,
        num_characters=num_characters,
        num_words=num_words,
        avg_confidence=avg_confidence,
        traced_image_path=traced_image_path,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_recognition_history(
    db: Session,
    skip: int = 0,
    limit: int = 50,
) -> List[RecognitionHistory]:
    """
    Get all recognition history records, newest first.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
    """
    return (
        db.query(RecognitionHistory)
        .order_by(RecognitionHistory.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_recognition_by_id(db: Session, record_id: int) -> Optional[RecognitionHistory]:
    """Get a single recognition record by its ID."""
    return db.query(RecognitionHistory).filter(RecognitionHistory.id == record_id).first()


def delete_recognition(db: Session, record_id: int) -> bool:
    """
    Delete a recognition record by ID.
    Returns True if deleted, False if not found.
    """
    record = db.query(RecognitionHistory).filter(RecognitionHistory.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
        return True
    return False


def get_history_count(db: Session) -> int:
    """Get the total number of recognition records."""
    return db.query(RecognitionHistory).count()

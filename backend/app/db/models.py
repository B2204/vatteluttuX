"""
VatteluttuX - Database Models

SQLAlchemy models representing the database tables.
These map directly to MySQL tables visible in phpMyAdmin.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, DateTime

from app.db.database import Base


class RecognitionHistory(Base):
    """
    Stores the history of OCR recognition results.
    
    Each row represents one image that was scanned and recognized.
    Viewable in phpMyAdmin at: http://localhost/phpmyadmin → vattalettux → recognition_history
    """
    __tablename__ = "recognition_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_filename = Column(String(255), nullable=False, comment="Name of the uploaded image file")
    recognized_text = Column(Text, nullable=False, comment="Raw label sequence (e.g., va_001 va_014)")
    modern_text = Column(Text, nullable=False, comment="Modern Tamil Unicode text output")
    num_characters = Column(Integer, default=0, comment="Number of characters detected")
    num_words = Column(Integer, default=0, comment="Number of words detected")
    avg_confidence = Column(Float, default=0.0, comment="Average prediction confidence (0.0-1.0)")
    traced_image_path = Column(String(500), nullable=True, comment="Path to the annotated traced image")
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Timestamp when the recognition was performed"
    )

    def __repr__(self):
        return f"<RecognitionHistory(id={self.id}, file='{self.original_filename}', text='{self.modern_text[:20]}...')>"

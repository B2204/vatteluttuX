"""
VatteluttuX - Application Configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_TITLE: str = "VatteluttuX OCR API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5177",
    ]
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MEDIA_DIR: Path = BASE_DIR / "app" / "media"
    MODELS_DIR: Path = BASE_DIR / "models"
    MODEL_PATH: Path = MODELS_DIR / "best_model.pth"
    
    # Character Map
    CHARACTER_MAP_PATH: Path = Path(__file__).parent / "character_map.json"
    LABEL_TO_CHAR_PATH: Path = Path(__file__).parent / "label_to_char.json"
    
    # Database Settings
    DATABASE_URL: str = "mysql+pymysql://root@localhost/vattalettux"
    
    # OCR Settings
    IMAGE_SIZE: int = 64  # Size for character images
    CONFIDENCE_THRESHOLD: float = 0.5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

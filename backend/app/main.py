"""
VatteluttuX - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes import router
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="VatteluttuX OCR API",
    description="API for recognizing Vatteluttu Tamil inscriptions and converting to modern Tamil",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create media directory if it doesn't exist
media_path = Path(settings.MEDIA_DIR)
media_path.mkdir(parents=True, exist_ok=True)

# Mount static files for serving traced images
app.mount("/media", StaticFiles(directory=str(media_path)), name="media")

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    print("=" * 50)
    print("VatteluttuX OCR API Starting...")
    print(f"Media directory: {settings.MEDIA_DIR}")
    print(f"Model path: {settings.MODEL_PATH}")
    
    # Initialize database tables
    from app.db.database import init_db
    try:
        init_db()
        print(f"Database: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"[WARNING] Database initialization warning: {e}")
        print("  Make sure MySQL is running (XAMPP -> Start MySQL)")
    
    print("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("VatteluttuX OCR API Shutting down...")

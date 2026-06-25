"""
VatteluttuX - Database Connection & Session Management

Uses SQLAlchemy to connect to MySQL via PyMySQL.
Database: vattalettux (MySQL running via XAMPP)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before using them
)

# Session factory - each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session when the request is done.
    
    Usage in routes:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    Called once during application startup.
    """
    from app.db.models import RecognitionHistory  # noqa: F401
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created successfully")

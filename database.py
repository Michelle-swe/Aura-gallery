"""
Database configuration and session management module.
Handles SQLAlchemy setup, connection pooling, and session creation.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

from config import settings

# Create engine with appropriate configuration based on database type
if "sqlite" in settings.DATABASE_URL:
    # SQLite configuration (for development)
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use StaticPool for SQLite
        echo=settings.DATABASE_ECHO,
    )
else:
    # PostgreSQL/MySQL configuration (for production)
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,  # Verify connections before using them
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# Declarative base for all models
Base = declarative_base()


def get_db() -> Session:
    """
    Database session dependency for FastAPI.
    
    Yields:
        Session: SQLAlchemy session object
        
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def close_db() -> None:
    """Close all database connections."""
    engine.dispose()


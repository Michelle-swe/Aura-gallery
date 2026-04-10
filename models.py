"""
SQLAlchemy database models.
Defines all database table structures.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship

from database import Base


# =========================
# USER MODEL
# =========================

class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    photos = relationship("Photo", back_populates="owner", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_username", "username"),
        Index("idx_user_is_active", "is_active"),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


# =========================
# PHOTO MODEL
# =========================

class Photo(Base):
    """Photo model for storing gallery images."""
    
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    image_url = Column(String(500), nullable=False)
    public_id = Column(String(255), nullable=False, unique=True)  # Cloudinary public ID
    file_size = Column(Integer, nullable=True)  # In bytes
    
    is_public = Column(Boolean, default=True, index=True)
    is_favorite = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="photos")

    __table_args__ = (
        Index("idx_photo_user_id", "user_id"),
        Index("idx_photo_is_public", "is_public"),
        Index("idx_photo_created_at", "created_at"),
    )

    def __repr__(self):
        return f"<Photo(id={self.id}, title={self.title}, user_id={self.user_id})>"


# =========================
# REFRESH TOKEN MODEL
# =========================

class RefreshToken(Base):
    """Refresh token model for session management."""
    
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        Index("idx_refresh_token_user_id", "user_id"),
        Index("idx_refresh_token_expires_at", "expires_at"),
    )

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id})>"

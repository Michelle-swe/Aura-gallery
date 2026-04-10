"""
Pydantic schemas for request/response validation.
Defines data models for API endpoints.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# =========================
# USER SCHEMAS
# =========================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# =========================
# PHOTO SCHEMAS
# =========================

class PhotoBase(BaseModel):
    """Base photo schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class PhotoCreate(PhotoBase):
    """Schema for creating a new photo."""
    pass


class PhotoUpdate(BaseModel):
    """Schema for updating photo metadata."""
    title: Optional[str] = None
    description: Optional[str] = None


class PhotoResponse(PhotoBase):
    """Schema for photo response."""
    id: int
    user_id: int
    image_url: str
    public_id: str  # Cloudinary public ID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PhotoListResponse(PhotoResponse):
    """Schema for photo list items."""
    pass


# =========================
# TOKEN SCHEMAS
# =========================

class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[int] = None
    email: Optional[str] = None


# =========================
# ERROR SCHEMAS
# =========================

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None


# =========================
# PAGINATION SCHEMAS
# =========================

class PaginatedResponse(BaseModel):
    """Generic paginated response schema."""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list
    
    class Config:
        from_attributes = True

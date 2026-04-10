"""
Utility functions for the application.
Includes authentication, validation, and common helpers.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

from config import settings
from schemas import TokenData

# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# JWT TOKEN MANAGEMENT
# =========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in token
        expires_delta: Optional expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Data to encode in token
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM,
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        TokenData if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            return None
            
        return TokenData(user_id=user_id, email=email)
        
    except JWTError:
        return None


# =========================
# SECURITY DEPENDENCIES
# =========================

security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthCredentials = Depends(security)) -> int:
    """
    Extract and verify user ID from JWT token.
    
    Args:
        credentials: HTTP bearer credentials
        
    Returns:
        User ID from token
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data.user_id


# =========================
# PAGINATION HELPERS
# =========================

def paginate(query, page: int = 1, page_size: int = 10):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        dict with total, page, page_size, total_pages, and items
    """
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": items,
    }


# =========================
# VALIDATION HELPERS
# =========================

def validate_page_params(page: int = 1, page_size: int = 10) -> tuple[int, int]:
    """
    Validate and normalize pagination parameters.
    
    Args:
        page: Page number
        page_size: Items per page
        
    Returns:
        Tuple of (page, page_size) with valid values
    """
    page = max(1, page)
    page_size = max(1, min(page_size, 100))  # Cap at 100 items per page
    
    return page, page_size


# =========================
# ERROR HANDLERS
# =========================

def create_error_response(detail: str, error_code: Optional[str] = None) -> dict:
    """
    Create a standardized error response.
    
    Args:
        detail: Error message
        error_code: Optional error code
        
    Returns:
        Error response dictionary
    """
    return {
        "detail": detail,
        "error_code": error_code,
    }

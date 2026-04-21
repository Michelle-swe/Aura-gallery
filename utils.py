import jwt
import secrets
import requests
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """Decodes the JWT and returns the user_id."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.PyJWTError:
        raise credentials_exception

def enforce_storage_limit(user: models.User):
    """Checks if the user has reached their plan's photo limit."""
    # We count non-deleted photos
    active_photo_count = len([p for p in user.photos if not p.is_deleted])
    
    if active_photo_count >= user.total_limit:
        raise HTTPException(
            status_code=403, 
            detail=f"Storage limit reached for {user.plan} plan ({user.total_limit} photos). Please upgrade."
        )

def generate_share_hash():
    """Generates a secure random string for sharing collections."""
    return secrets.token_urlsafe(16)

def move_to_trash(photo: models.Photo):
    """Soft deletes a photo."""
    photo.is_deleted = True

def initialize_paystack_payment(email: str, amount: int):
    """Calls Paystack API to initialize a transaction."""
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    # Paystack expects amount in Kobo (Naira * 100)
    payload = {
        "email": email,
        "amount": amount * 100 
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Paystack initialization failed")
    return response.json()

def verify_paystack_payment(reference: str):
    """Verifies a Paystack transaction using the reference code."""
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not verify payment with Paystack")
    return response.json()
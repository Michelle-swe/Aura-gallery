import os
import uuid
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import settings

SECRET_KEY = str(settings.SECRET_KEY)
ALGORITHM = str(settings.ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

security = HTTPBearer()


# ==============================
# 🔐 JWT FUNCTIONS
# ==============================

def create_access_token(data: dict):
    """
    Generate JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str):
    """
    Verify and decode JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["user_id"]  # return just the user_id, not the whole payload


# ==============================
# 🚨 STORAGE LOGIC (CORE FEATURE)
# ==============================

def check_storage(user):
    return user.current_count < user.total_limit


def enforce_storage_limit(user):
    if user.current_count >= user.total_limit:
        raise HTTPException(
            status_code=403,
            detail="Storage full. Upgrade your plan."
        )


def increment_photo_count(user):
    user.current_count += 1


def decrement_photo_count(user):
    if user.current_count > 0:
        user.current_count -= 1


# ==============================
# 🔗 SHARE LINK
# ==============================

def generate_share_hash():
    return str(uuid.uuid4())[:8]


# ==============================
# 🗑️ TRASH SYSTEM
# ==============================

def move_to_trash(photo):
    photo.deleted_at = datetime.utcnow()


def is_in_trash(photo):
    return photo.deleted_at is not None


def should_delete_permanently(photo):
    if photo.deleted_at is None:
        return False

    return datetime.utcnow() > photo.deleted_at + timedelta(days=30)


# ==============================
# 💳 PLAN LIMITS
# ==============================

PLAN_LIMITS = {
    "Starter": 20,
    "Basic": 30,
    "Premium": 70,
    "Diamond": 120
}


def get_plan_limit(plan_name):
    return PLAN_LIMITS.get(plan_name, 20)


# ==============================
# 📅 OPTIONAL HELPERS
# ==============================

def format_date_group(date):
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    if date.date() == today:
        return "Today"
    elif date.date() == yesterday:
        return "Yesterday"
    else:
        return "Older"

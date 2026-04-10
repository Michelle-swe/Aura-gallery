"""
API route definitions.
Includes all endpoint routers for the application.
"""

from fastapi import APIRouter

# Create main router
router = APIRouter(prefix="/api", tags=["API"])


# =========================
# AUTH ROUTES
# =========================

@router.post("/auth/register", tags=["Authentication"])
async def register(username: str, email: str, password: str):
    """Register a new user."""
    pass


@router.post("/auth/login", tags=["Authentication"])
async def login(email: str, password: str):
    """Login user and return access token."""
    pass


@router.post("/auth/refresh", tags=["Authentication"])
async def refresh_token(refresh_token: str):
    """Refresh access token."""
    pass


@router.post("/auth/logout", tags=["Authentication"])
async def logout():
    """Logout user."""
    pass


# =========================
# USER ROUTES
# =========================

@router.get("/users/me", tags=["Users"])
async def get_current_user():
    """Get current user profile."""
    pass


@router.put("/users/me", tags=["Users"])
async def update_user():
    """Update current user profile."""
    pass


@router.delete("/users/me", tags=["Users"])
async def delete_account():
    """Delete user account."""
    pass


# =========================
# PHOTO ROUTES
# =========================

@router.get("/photos", tags=["Photos"])
async def list_photos(page: int = 1, page_size: int = 10):
    """List all photos with pagination."""
    pass


@router.post("/photos", tags=["Photos"])
async def upload_photo():
    """Upload a new photo."""
    pass


@router.get("/photos/{photo_id}", tags=["Photos"])
async def get_photo(photo_id: int):
    """Get a specific photo."""
    pass


@router.put("/photos/{photo_id}", tags=["Photos"])
async def update_photo(photo_id: int):
    """Update photo metadata."""
    pass


@router.delete("/photos/{photo_id}", tags=["Photos"])
async def delete_photo(photo_id: int):
    """Delete a photo."""
    pass


@router.post("/photos/{photo_id}/favorite", tags=["Photos"])
async def toggle_favorite(photo_id: int):
    """Toggle photo favorite status."""
    pass


# =========================
# HEALTH ROUTES
# =========================

# Note: Health check endpoints are in main.py


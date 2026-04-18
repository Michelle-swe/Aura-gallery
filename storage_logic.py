# -----------------------------
# 📦 PLAN LIMITS
# -----------------------------
PLAN_LIMITS = {
    "starter": 20,
    "basic": 30,
    "premium": 70,
    "diamond": 120
}


# -----------------------------
# ✅ CHECK IF USER CAN UPLOAD
# -----------------------------
def can_upload(plan: str, current_count: int) -> bool:
    """
    Returns True if user can upload more photos,
    False if storage is full.
    """
    limit = PLAN_LIMITS.get(plan.lower(), 20)  # default to starter

    return current_count < limit


# -----------------------------
# 📊 GET REMAINING STORAGE
# -----------------------------
def remaining_storage(plan: str, current_count: int) -> int:
    """
    Returns how many photos user can still upload.
    """
    limit = PLAN_LIMITS.get(plan.lower(), 20)

    return max(limit - current_count, 0)


# -----------------------------
# 🚫 CHECK IF STORAGE FULL
# -----------------------------
def is_storage_full(plan: str, current_count: int) -> bool:
    """
    Returns True if storage is full.
    """
    limit = PLAN_LIMITS.get(plan.lower(), 20)

    return current_count >= limit
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import uuid

from storage_logic import can_upload

router = APIRouter()

# 🧠 Temporary in-memory storage (replace with DB later)
fake_db = {
    "users": {
        "user1": {
            "plan": "starter",
            "photo_count": 0
        }
    },
    "photos": []
}


# -----------------------------
# 📤 UPLOAD PHOTO
# -----------------------------
@router.post("/photos/upload")
async def upload_photo(file: UploadFile = File(...)):
    user = fake_db["users"]["user1"]

    # 🔥 Check storage limit
    if not can_upload(user["plan"], user["photo_count"]):
        raise HTTPException(
            status_code=403,
            detail="🚫 Storage full. Upgrade your plan."
        )

    # 🧠 Simulate file upload (later use Cloudinary or S3)
    file_url = f"https://fake-storage.com/{uuid.uuid4()}_{file.filename}"

    # Save photo
    photo = {
        "id": str(uuid.uuid4()),
        "url": file_url,
        "created_at": datetime.utcnow(),
        "deleted": False
    }

    fake_db["photos"].append(photo)

    # Update user photo count
    user["photo_count"] += 1

    return {
        "message": "✅ Photo uploaded successfully",
        "photo": photo
    }


# -----------------------------
# 🖼️ GET ALL PHOTOS
# -----------------------------
@router.get("/photos")
def get_photos():
    return [p for p in fake_db["photos"] if not p["deleted"]]


# -----------------------------
# 🗑️ DELETE PHOTO (SOFT DELETE)
# -----------------------------
@router.delete("/photos/{photo_id}")
def delete_photo(photo_id: str):
    for photo in fake_db["photos"]:
        if photo["id"] == photo_id:
            photo["deleted"] = True
            photo["deleted_at"] = datetime.utcnow()
            return {"message": "🗑️ Photo moved to trash"}

    raise HTTPException(status_code=404, detail="Photo not found")
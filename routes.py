from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import bcrypt
import cloudinary
import cloudinary.uploader
from utils import (
    create_access_token,
    get_current_user,
    enforce_storage_limit,
    generate_share_hash,
    initialize_paystack_payment,
    move_to_trash,
    verify_paystack_payment
)

router = APIRouter()


# AUTH
@router.post("/register", response_model=schemas.UserResponse)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user_in.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = models.User(email=user_in.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if not user or not bcrypt.checkpw(user_in.password.encode("utf-8"), user.password_hash.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token}


# USER
@router.get("/me")
def get_me(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# PHOTOS
@router.post("/photos/upload")
async def upload_photo(file: UploadFile = File(...), user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    enforce_storage_limit(user)

    contents = await file.read()
    upload_result = cloudinary.uploader.upload(contents)
    image_url = upload_result["secure_url"]

    photo = models.Photo(image_url=image_url, user_id=user_id)
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {"message": "Photo uploaded successfully", "url": image_url}


@router.get("/photos")
def get_photos(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Photo).filter(
        models.Photo.user_id == user_id,
        models.Photo.is_deleted == False
    ).all()


@router.delete("/photos/{photo_id}")
def delete_photo(photo_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    photo = db.get(models.Photo, photo_id)
    if not photo or photo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Photo not found")

    move_to_trash(photo)
    db.commit()
    return {"message": "Moved to trash"}


# COLLECTIONS
@router.post("/collections")
def create_collection(name: str, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    collection = models.Collection(name=name, user_id=user_id)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return {"message": "Collection created"}


@router.get("/collections")
def get_collections(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Collection).filter(models.Collection.user_id == user_id).all()


@router.post("/collections/{collection_id}/photos/{photo_id}")
def add_photo_to_collection(collection_id: int, photo_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    collection = db.get(models.Collection, collection_id)
    if not collection or collection.user_id != user_id:
        raise HTTPException(status_code=404, detail="Collection not found")

    photo = db.get(models.Photo, photo_id)
    if not photo or photo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Photo not found")

    entry = models.CollectionPhoto(collection_id=collection_id, photo_id=photo_id)
    db.add(entry)
    db.commit()
    return {"message": "Photo added to collection"}


# SHARE
@router.post("/share/{collection_id}")
def share_collection(collection_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    collection = db.get(models.Collection, collection_id)
    if not collection or collection.user_id != user_id:
        raise HTTPException(status_code=404, detail="Collection not found")

    hash_code = generate_share_hash()
    share = models.ShareLink(collection_id=collection_id, share_hash=hash_code)
    db.add(share)
    db.commit()

    return {"link": f"/s/{hash_code}"}


@router.get("/s/{hash_code}")
def view_shared(hash_code: str, db: Session = Depends(get_db)):
    share = db.query(models.ShareLink).filter(models.ShareLink.share_hash == hash_code).first()
    if not share:
        raise HTTPException(status_code=404, detail="Not found")

    photos = db.query(models.CollectionPhoto).filter(
        models.CollectionPhoto.collection_id == share.collection_id
    ).all()
    return photos

@router.post("/paystack/init")
def init_payment(
    plan: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.get(models.User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prices = {
        "Basic": 0,
        "Premium": 12,
        "Diamond": 24
    }

    plan = plan.capitalize()

    if plan not in prices:
        raise HTTPException(status_code=400, detail="Invalid plan")

    amount = prices[plan]

    
    if amount <= 0:
        user.plan = "Basic"
        user.total_limit = 30
        db.commit()

        return {
            "message": "Basic plan activated successfully",
            "plan": "Basic"
        }

    
    response = initialize_paystack_payment(
        email=user.email,
        amount=amount
    )

    return {
        "message": f"{plan} payment initialized",
        "data": response
    }
@router.get("/paystack/verify/{reference}")
def verify_payment(reference: str, plan: str, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    result = verify_paystack_payment(reference)

    if result["data"]["status"] != "success":
        raise HTTPException(status_code=400, detail="Payment not successful")

    user = db.get(models.User, user_id)

    # update plan after payment
    if plan == "Basic":
        user.total_limit = 30
    elif plan == "Premium":
        user.total_limit = 70
    elif plan == "Diamond":
        user.total_limit = 120

    user.plan = plan
    db.commit()

    return {"message": f"Payment verified. Upgraded to {plan}"}
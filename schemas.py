from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime



class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password : str

class UserResponse(UserBase):
    id : int
    plan : str
    created_at : datetime

    class Config:
        from_attributes = True



class PhotoBase(BaseModel):
    image_url : str

class PhotoCreate(PhotoBase):
    pass

class PhotoResponse(PhotoBase):
    id : int
    user_id : int
    created_at : datetime
    is_deleted : bool

    class Config:
        from_attributes = True



class CollectionBase(BaseModel):
    name : str
    cover_image : Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionResponse(CollectionBase):
    id : int
    user_id : int
    created_at : datetime
    
    class Config:
        from_attributes = True



class CollectionPhotoBase(BaseModel):
    collection_id : int
    photo_id : int

class CollectionPhotoCreate(CollectionPhotoBase):
    pass

class CollectionPhotoResponse(CollectionPhotoBase):
    id : int
    created_at : datetime

    class Config:
        from_attributes = True





        
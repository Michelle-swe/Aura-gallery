from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    plan = Column(String, default="Starter")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    photos = relationship("Photo", back_populates="user", cascade="all, delete")
    collections = relationship("Collection", back_populates="user", cascade="all, delete")



class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="photos")
    collections = relationship("CollectionPhoto", back_populates="photo", cascade="all, delete")



class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cover_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="collections")
    photos = relationship("CollectionPhoto", back_populates="collection", cascade="all, delete")



class CollectionPhoto(Base):
    __tablename__ = "collection_photos"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)

    # Relationships
    collection = relationship("Collection", back_populates="photos")
    photo = relationship("Photo", back_populates="collections")






    
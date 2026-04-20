from ast import Import

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, init_db
import routes
import cloudinary
from config import settings



app = FastAPI(
    title="Aura Gallery API",
    description="Premium photo management platform — Digital Curator",
    version="1.0.0"
)


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

@app.on_event("startup")
def on_startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


@app.get("/")
def root():
    return {"message": "Aura Gallery API is live"}

@app.get("/health")
def health():
    return {"status": "ok"}





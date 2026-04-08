from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aura Gallery API",
    description="Premium photo management platform — Digital Curator",
    version="1.0.0"
)

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

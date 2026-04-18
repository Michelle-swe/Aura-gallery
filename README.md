# Aura Gallery — Backend

Premium photo management platform API built with FastAPI.

## Stack

- FastAPI + SQLAlchemy + PostgreSQL
- Cloudinary (photo storage)
- JWT Authentication + Google OAuth2

## Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your values
5. Run: `uvicorn main:app --reload`

## API Docs

Visit `http://localhost:8000/docs` after running the server.

## Structure

- `models/` → Database tables
- `schemas/` → Request/response validation
- `routes/` → API endpoints
- `utils/` → Shared helpers
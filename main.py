"""
FastAPI application entry point.
Initializes the Aura Gallery API with all configurations and middleware.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from database import init_db, close_db, Base, engine
from routes import router


# =========================
# LIFECYCLE EVENTS
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down application")
    close_db()
    print("✅ Database connections closed")


# =========================
# APPLICATION INITIALIZATION
# =========================

app = FastAPI(
    title=settings.APP_NAME,
    description="Premium photo management platform — Digital Curator",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


# =========================
# MIDDLEWARE CONFIGURATION
# =========================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# =========================
# ROUTES
# =========================

app.include_router(router)


# =========================
# ROOT ENDPOINTS
# =========================

@app.get("/", tags=["Health"])
def root():
    """Root endpoint for health check."""
    return {
        "message": f"{settings.APP_NAME} API is live",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }


# =========================
# ERROR HANDLERS
# =========================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR",
        },
    )


# =========================
# STARTUP INFO
# =========================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )

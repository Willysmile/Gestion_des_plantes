from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.config import settings
from app.utils.db import init_db, get_db
from app.models import Base
from app.routes.plants import router as plants_router
from app.routes.photos import router as photos_router, files_router
from app.routes.histories import watering_router, fertilizing_router, repotting_router, disease_router, notes_router
from app.routes.settings import router as settings_router
from app.routes.statistics import router as statistics_router
from app.routes.lookups import router as lookups_router
from app.scripts.seed_lookups import seed_all
import os

# Initialize database
init_db()

# Seed lookup tables at startup
db = next(get_db())
try:
    seed_all(db)
finally:
    db.close()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Desktop plant management application",
    version="2.0.0"
)

# CORS configuration for Tauri + React development
# ⚠️ CRITICAL: Both dev (Vite) and production (Tauri) origins needed
CORS_ORIGINS = [
    "http://localhost:5173",        # Vite dev server (React)
    "http://127.0.0.1:5173",        # Alternative localhost
    "https://tauri.localhost",      # Tauri production (correct format)
    "tauri://localhost",            # Legacy fallback (may not work)
]

# Add localhost backend variations for internal testing
if os.getenv("ENVIRONMENT", "development") != "production":
    CORS_ORIGINS.extend([
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(plants_router)
app.include_router(photos_router)
app.include_router(files_router)
app.include_router(watering_router)
app.include_router(fertilizing_router)
app.include_router(repotting_router)
app.include_router(disease_router)
app.include_router(notes_router)
app.include_router(settings_router)
app.include_router(statistics_router)
app.include_router(lookups_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "debug": settings.DEBUG
    }

# Test DB endpoint
@app.get("/api/db-status")
async def db_status(db: Session = Depends(get_db)):
    try:
        # Simple query to test DB connection
        result = db.execute("SELECT 1").fetchone()
        return {"status": "connected", "test": "ok"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

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
from app.routes.statistics import router as statistics_router  # Include activity endpoint
from app.routes.lookups import router as lookups_router
from app.routes.tags import router as tags_router
from app.routes.audit import router as audit_router
from app.routes.audit_stats import router as audit_stats_router
from app.routes.propagations import router as propagations_router
from app.scripts.seed_lookups import seed_all
# Importation de tous les modèles pour s'assurer qu'ils sont enregistrés
from app.models import (
    Plant, PhotoModel, Unit, Location, PurchasePlace, WateringFrequency,
    LightRequirement, FertilizerType, DiseaseType, TreatmentType,
    PlantHealthStatus, WateringHistory, FertilizingHistory, RepottingHistory,
    DiseaseHistory, PlantHistory, Tag, TagCategory, AuditLog,
    PlantPropagation, PropagationEvent
)
from app.scripts.seed_plants import seed_plants
# Audit listeners pour auto-logging
from app.listeners import AuditListeners
import os

# Create FastAPI app FIRST
app = FastAPI(
    title="Gestion des Plantes",
    description="Desktop plant management application",
    version="2.0.0"
)

# ADD CORS MIDDLEWARE IMMEDIATELY - MUST BE BEFORE ANY ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "https://tauri.localhost",
        "tauri://localhost",
        "*",  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# THEN initialize database and seed
init_db()

# Register audit event listeners ONLY IF NOT IN TESTING MODE
if not os.getenv('TESTING'):
    AuditListeners.register()

# Seed lookup tables and sample plants at startup
db = next(get_db())
try:
    seed_all(db)
    # seed_plants(db)  # Disabled - create plants manually with new fields
finally:
    db.close()

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
app.include_router(tags_router)
app.include_router(audit_router)
app.include_router(audit_stats_router)
app.include_router(propagations_router)

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

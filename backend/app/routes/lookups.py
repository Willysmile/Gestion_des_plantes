"""
Endpoints FastAPI pour les lookups
Alias pour /api/lookups/* pointant vers les services de settings
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.services.settings_service import SettingsService


router = APIRouter(
    prefix="/api/lookups",
    tags=["lookups"],
)


# ===== LOCATIONS =====

@router.get("/locations", response_model=List[dict])
async def list_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Récupère toutes les localisations"""
    locations = SettingsService.get_locations(db, skip=skip, limit=limit)
    return [{"id": l.id, "name": l.name} for l in locations]


# ===== WATERING FREQUENCIES =====

@router.get("/watering-frequencies", response_model=List[dict])
async def list_watering_frequencies(
    db: Session = Depends(get_db),
):
    """Récupère toutes les fréquences d'arrosage"""
    frequencies = SettingsService.get_watering_frequencies(db)
    return [{"id": f.id, "name": f.name, "days": f.days_interval} for f in frequencies]


# ===== LIGHT REQUIREMENTS =====

@router.get("/light-requirements", response_model=List[dict])
async def list_light_requirements(
    db: Session = Depends(get_db),
):
    """Récupère tous les besoins en lumière"""
    requirements = SettingsService.get_light_requirements(db)
    return [{"id": r.id, "name": r.name} for r in requirements]


# ===== FERTILIZER TYPES =====

@router.get("/fertilizer-types", response_model=List[dict])
async def list_fertilizer_types(
    db: Session = Depends(get_db),
):
    """Récupère tous les types d'engrais"""
    fertilizers = SettingsService.get_fertilizer_types(db)
    return [{"id": f.id, "name": f.name, "unit": f.unit, "description": f.description} for f in fertilizers]


# ===== DISEASE TYPES =====

@router.get("/disease-types", response_model=List[dict])
async def list_disease_types(
    db: Session = Depends(get_db),
):
    """Récupère tous les types de maladies"""
    disease_types = SettingsService.get_disease_types(db)
    return [{"id": dt.id, "name": dt.name, "description": dt.description} for dt in disease_types]


# ===== TREATMENT TYPES =====

@router.get("/treatment-types", response_model=List[dict])
async def list_treatment_types(
    db: Session = Depends(get_db),
):
    """Récupère tous les types de traitement"""
    treatment_types = SettingsService.get_treatment_types(db)
    return [{"id": tt.id, "name": tt.name, "description": tt.description} for tt in treatment_types]


# ===== PLANT HEALTH STATUSES =====

@router.get("/plant-health-statuses", response_model=List[dict])
async def list_plant_health_statuses(
    db: Session = Depends(get_db),
):
    """Récupère tous les états de santé des plantes"""
    statuses = SettingsService.get_plant_health_statuses(db)
    return [{"id": s.id, "name": s.name, "description": s.description} for s in statuses]

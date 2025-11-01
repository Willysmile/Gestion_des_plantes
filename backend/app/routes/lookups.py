"""
Endpoints FastAPI pour les lookups
Alias pour /api/lookups/* pointant vers les services de settings
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.services.settings_service import SettingsService
from app.services.lookup_service import UnitService, FertilizerTypeService
from app.schemas.lookup_schema import UnitCreate, UnitUpdate, UnitResponse, FertilizerTypeCreate, FertilizerTypeUpdate, FertilizerTypeResponse


router = APIRouter(
    prefix="/api/lookups",
    tags=["lookups"],
)


# ===== UNITS (NEW) =====

@router.get("/units", response_model=List[UnitResponse])
async def list_units(db: Session = Depends(get_db)):
    """Récupère toutes les unités"""
    return UnitService.get_all(db)


@router.get("/units/{unit_id}", response_model=UnitResponse)
async def get_unit(unit_id: int, db: Session = Depends(get_db)):
    """Récupère une unité par ID"""
    unit = UnitService.get_by_id(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.post("/units", response_model=UnitResponse)
async def create_unit(unit: UnitCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle unité"""
    return UnitService.create(db, unit)


@router.put("/units/{unit_id}", response_model=UnitResponse)
async def update_unit(unit_id: int, unit: UnitUpdate, db: Session = Depends(get_db)):
    """Modifie une unité"""
    db_unit = UnitService.update(db, unit_id, unit)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db_unit


@router.delete("/units/{unit_id}")
async def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    """Supprime une unité"""
    db_unit = UnitService.delete(db, unit_id)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"detail": "Unit deleted successfully"}


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


# ===== FERTILIZER FREQUENCIES =====

@router.get("/fertilizer-frequencies", response_model=List[dict])
async def list_fertilizer_frequencies(
    db: Session = Depends(get_db),
):
    """Récupère toutes les fréquences de fertilisation"""
    from app.models.lookup import FertilizerFrequency
    frequencies = db.query(FertilizerFrequency).all()
    return [{"id": f.id, "name": f.name, "weeks": f.weeks_interval} for f in frequencies]


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


@router.post("/fertilizer-types", response_model=FertilizerTypeResponse)
async def create_fertilizer_type(fertilizer: FertilizerTypeCreate, db: Session = Depends(get_db)):
    """Crée un nouveau type d'engrais"""
    return FertilizerTypeService.create(db, fertilizer)


@router.put("/fertilizer-types/{fert_id}", response_model=FertilizerTypeResponse)
async def update_fertilizer_type(fert_id: int, fertilizer: FertilizerTypeUpdate, db: Session = Depends(get_db)):
    """Modifie un type d'engrais"""
    db_fert = FertilizerTypeService.update(db, fert_id, fertilizer)
    if not db_fert:
        raise HTTPException(status_code=404, detail="Fertilizer type not found")
    return db_fert


@router.delete("/fertilizer-types/{fert_id}")
async def delete_fertilizer_type(fert_id: int, db: Session = Depends(get_db)):
    """Supprime un type d'engrais"""
    db_fert = FertilizerTypeService.delete(db, fert_id)
    if not db_fert:
        raise HTTPException(status_code=404, detail="Fertilizer type not found")
    return {"detail": "Fertilizer type deleted successfully"}


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


# ===== WATERING METHODS =====

@router.get("/watering-methods", response_model=List[dict])
async def list_watering_methods(
    db: Session = Depends(get_db),
):
    """Récupère toutes les méthodes d'arrosage"""
    methods = SettingsService.get_watering_methods(db)
    return [{"id": m.id, "name": m.name, "description": m.description} for m in methods]


# ===== WATER TYPES =====

@router.get("/water-types", response_model=List[dict])
async def list_water_types(
    db: Session = Depends(get_db),
):
    """Récupère tous les types d'eau"""
    types = SettingsService.get_water_types(db)
    return [{"id": t.id, "name": t.name, "description": t.description} for t in types]


# ===== SEASONS =====

@router.get("/seasons", response_model=List[dict])
async def list_seasons(
    db: Session = Depends(get_db),
):
    """Récupère toutes les saisons"""
    seasons = SettingsService.get_seasons(db)
    return [{"id": s.id, "name": s.name, "start_month": s.start_month, "end_month": s.end_month, "description": s.description} for s in seasons]


"""
Endpoints FastAPI pour les paramètres et lookups (Settings)
24 endpoints: GET/POST/PUT/DELETE pour 6 types de lookups
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.utils.db import get_db
from app.services.settings_service import SettingsService
from app.models.lookup import (
    Location, PurchasePlace, WateringFrequency,
    LightRequirement, FertilizerType
)
from app.models.tags import Tag, TagCategory


# Schemas simples
class NameSchema(BaseModel):
    name: str

class WateringFrequencySchema(BaseModel):
    name: str
    days: int

class TagSchema(BaseModel):
    category_id: int
    name: str

class FertilizerTypeSchema(BaseModel):
    name: str
    unit: str = "ml"
    description: Optional[str] = None


router = APIRouter(
    prefix="/api/settings",
    tags=["settings"],
)


# ===== LOCATIONS (4 endpoints) =====

@router.get("/locations", response_model=List[dict])
async def list_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Récupère toutes les localisations"""
    locations = SettingsService.get_locations(db, skip=skip, limit=limit)
    return [{"id": l.id, "name": l.name} for l in locations]


@router.post("/locations", status_code=201)
async def create_location(
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Crée une nouvelle localisation"""
    location = SettingsService.create_location(db, data.name)
    return {"id": location.id, "name": location.name}


@router.put("/locations/{location_id}")
async def update_location(
    location_id: int,
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Met à jour une localisation"""
    location = SettingsService.update_location(db, location_id, data.name)
    if not location:
        raise HTTPException(status_code=404, detail="Localisation non trouvée")
    return {"id": location.id, "name": location.name}


@router.delete("/locations/{location_id}", status_code=204)
async def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    """Supprime une localisation"""
    success = SettingsService.delete_location(db, location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Localisation non trouvée")


# ===== PURCHASE PLACES (4 endpoints) =====

@router.get("/purchase-places", response_model=List[dict])
async def list_purchase_places(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Récupère tous les lieux d'achat"""
    places = SettingsService.get_purchase_places(db, skip=skip, limit=limit)
    return [{"id": p.id, "name": p.name} for p in places]


@router.post("/purchase-places", status_code=201)
async def create_purchase_place(
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Crée un nouveau lieu d'achat"""
    place = SettingsService.create_purchase_place(db, data.name)
    return {"id": place.id, "name": place.name}


@router.put("/purchase-places/{place_id}")
async def update_purchase_place(
    place_id: int,
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Met à jour un lieu d'achat"""
    place = SettingsService.update_purchase_place(db, place_id, data.name)
    if not place:
        raise HTTPException(status_code=404, detail="Lieu d'achat non trouvé")
    return {"id": place.id, "name": place.name}


@router.delete("/purchase-places/{place_id}", status_code=204)
async def delete_purchase_place(
    place_id: int,
    db: Session = Depends(get_db),
):
    """Supprime un lieu d'achat"""
    success = SettingsService.delete_purchase_place(db, place_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lieu d'achat non trouvé")


# ===== WATERING FREQUENCIES (4 endpoints) =====

@router.get("/watering-frequencies", response_model=List[dict])
async def list_watering_frequencies(
    db: Session = Depends(get_db),
):
    """Récupère toutes les fréquences d'arrosage"""
    frequencies = SettingsService.get_watering_frequencies(db)
    return [{"id": f.id, "name": f.name, "days": f.days_interval} for f in frequencies]


@router.post("/watering-frequencies", status_code=201)
async def create_watering_frequency(
    data: WateringFrequencySchema,
    db: Session = Depends(get_db),
):
    """Crée une nouvelle fréquence d'arrosage"""
    frequency = SettingsService.create_watering_frequency(db, data.name, data.days)
    return {"id": frequency.id, "name": frequency.name, "days": frequency.days_interval}


@router.put("/watering-frequencies/{frequency_id}")
async def update_watering_frequency(
    frequency_id: int,
    data: WateringFrequencySchema,
    db: Session = Depends(get_db),
):
    """Met à jour une fréquence d'arrosage"""
    frequency = SettingsService.update_watering_frequency(db, frequency_id, data.name, data.days)
    if not frequency:
        raise HTTPException(status_code=404, detail="Fréquence d'arrosage non trouvée")
    return {"id": frequency.id, "name": frequency.name, "days": frequency.days_interval}


@router.delete("/watering-frequencies/{frequency_id}", status_code=204)
async def delete_watering_frequency(
    frequency_id: int,
    db: Session = Depends(get_db),
):
    """Supprime une fréquence d'arrosage"""
    success = SettingsService.delete_watering_frequency(db, frequency_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fréquence d'arrosage non trouvée")


# ===== LIGHT REQUIREMENTS (4 endpoints) =====

@router.get("/light-requirements", response_model=List[dict])
async def list_light_requirements(
    db: Session = Depends(get_db),
):
    """Récupère toutes les exigences lumineuses"""
    requirements = SettingsService.get_light_requirements(db)
    return [{"id": r.id, "name": r.name} for r in requirements]


@router.post("/light-requirements", status_code=201)
async def create_light_requirement(
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Crée une nouvelle exigence lumineuse"""
    requirement = SettingsService.create_light_requirement(db, data.name)
    return {"id": requirement.id, "name": requirement.name}


@router.put("/light-requirements/{requirement_id}")
async def update_light_requirement(
    requirement_id: int,
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Met à jour une exigence lumineuse"""
    requirement = SettingsService.update_light_requirement(db, requirement_id, data.name)
    if not requirement:
        raise HTTPException(status_code=404, detail="Exigence lumineuse non trouvée")
    return {"id": requirement.id, "name": requirement.name}


@router.delete("/light-requirements/{requirement_id}", status_code=204)
async def delete_light_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
):
    """Supprime une exigence lumineuse"""
    success = SettingsService.delete_light_requirement(db, requirement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exigence lumineuse non trouvée")


# ===== FERTILIZER TYPES (4 endpoints) =====

@router.get("/fertilizer-types", response_model=List[dict])
async def list_fertilizer_types(
    db: Session = Depends(get_db),
):
    """Récupère tous les types d'engrais"""
    types = SettingsService.get_fertilizer_types(db)
    return [{"id": t.id, "name": t.name, "unit": t.unit, "description": t.description} for t in types]


@router.post("/fertilizer-types", status_code=201)
async def create_fertilizer_type(
    data: FertilizerTypeSchema,
    db: Session = Depends(get_db),
):
    """Crée un nouveau type d'engrais"""
    fert_type = SettingsService.create_fertilizer_type(db, data.name, data.unit, data.description)
    return {"id": fert_type.id, "name": fert_type.name, "unit": fert_type.unit, "description": fert_type.description}


@router.put("/fertilizer-types/{fert_type_id}")
async def update_fertilizer_type(
    fert_type_id: int,
    data: FertilizerTypeSchema,
    db: Session = Depends(get_db),
):
    """Met à jour un type d'engrais"""
    fert_type = SettingsService.update_fertilizer_type(db, fert_type_id, data.name, data.unit, data.description)
    if not fert_type:
        raise HTTPException(status_code=404, detail="Type d'engrais non trouvé")
    return {"id": fert_type.id, "name": fert_type.name, "unit": fert_type.unit, "description": fert_type.description}


@router.delete("/fertilizer-types/{fert_type_id}", status_code=204)
async def delete_fertilizer_type(
    fert_type_id: int,
    db: Session = Depends(get_db),
):
    """Supprime un type d'engrais"""
    success = SettingsService.delete_fertilizer_type(db, fert_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Type d'engrais non trouvé")


# ===== TAGS & CATEGORIES (4 endpoints) =====

@router.get("/tag-categories", response_model=List[dict])
async def list_tag_categories(
    db: Session = Depends(get_db),
):
    """Récupère toutes les catégories de tags"""
    categories = SettingsService.get_tag_categories(db)
    return [{"id": c.id, "name": c.name} for c in categories]


@router.get("/tags", response_model=List[dict])
async def list_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_id: int = Query(None),
    db: Session = Depends(get_db),
):
    """Récupère tous les tags"""
    tags = SettingsService.get_tags(db, skip=skip, limit=limit, category_id=category_id)
    return [{"id": t.id, "category_id": t.tag_category_id, "name": t.name} for t in tags]


@router.post("/tags", status_code=201)
async def create_tag(
    data: TagSchema,
    db: Session = Depends(get_db),
):
    """Crée un nouveau tag"""
    tag = SettingsService.create_tag(db, data.category_id, data.name)
    if not tag:
        raise HTTPException(status_code=404, detail="Catégorie de tag non trouvée")
    return {"id": tag.id, "category_id": tag.tag_category_id, "name": tag.name}


@router.put("/tags/{tag_id}")
async def update_tag(
    tag_id: int,
    data: NameSchema,
    db: Session = Depends(get_db),
):
    """Met à jour un tag"""
    tag = SettingsService.update_tag(db, tag_id, data.name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    return {"id": tag.id, "category_id": tag.tag_category_id, "name": tag.name}


@router.delete("/tags/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
):
    """Supprime un tag"""
    success = SettingsService.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

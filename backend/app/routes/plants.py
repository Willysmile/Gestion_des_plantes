"""
Endpoints FastAPI pour les plantes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.schemas.plant_schema import PlantCreate, PlantUpdate, PlantResponse, PlantListResponse
from app.services import PlantService


router = APIRouter(
    prefix="/api/plants",
    tags=["plants"],
)


# ===== ROUTES SANS PARAMÈTRES D'ID (à placer AVANT /{plant_id}) =====

@router.get("", response_model=List[PlantListResponse])
async def list_plants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    archived: bool = Query(False, description="Inclure les plantes archivées"),
    db: Session = Depends(get_db),
):
    """Récupère la liste des plantes avec pagination"""
    plants = PlantService.get_all(
        db,
        skip=skip,
        limit=limit,
        include_archived=archived,
        include_deleted=False,
    )
    return plants


@router.post("", response_model=PlantResponse, status_code=201)
async def create_plant(
    plant_data: PlantCreate,
    db: Session = Depends(get_db),
):
    """Crée une nouvelle plante"""
    try:
        plant = PlantService.create(db, plant_data)
        return plant
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.post("/generate-reference")
async def generate_reference(
    family: str = Query(..., min_length=1, description="Famille botanique"),
    db: Session = Depends(get_db),
):
    """
    Génère une référence unique au format FAMILY-NNN
    
    Exemples:
    - Araceae → ARA-001, ARA-002, ...
    - Phalaenopsidaceae → PHA-001, ...
    
    Args:
        family: Famille botanique (ex: "Araceae")
    
    Returns:
        {reference: "ARA-001"}
    """
    try:
        from app.services.plant_service import PlantService
        reference = PlantService.generate_reference(db, family)
        return {"reference": reference, "status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération référence: {str(e)}")


@router.get("/archived", response_model=List[PlantListResponse])
async def get_archived_plants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Récupère les plantes archivées"""
    plants = PlantService.get_archived(db, skip=skip, limit=limit)
    return plants


@router.get("/search", response_model=List[PlantListResponse])
async def search_plants_endpoint(
    q: str = Query(..., min_length=1, description="Terme de recherche"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Recherche full-text dans name, scientific_name, description"""
    plants = PlantService.search(db, q, skip=skip, limit=limit)
    return plants


@router.get("/filter", response_model=List[PlantListResponse])
async def filter_plants_endpoint(
    location_id: int = Query(None),
    difficulty: str = Query(None),
    health_status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Filtre avancé: localisation, difficulté, santé"""
    plants = PlantService.filter_plants(
        db,
        location_id=location_id,
        difficulty=difficulty,
        health_status=health_status,
        skip=skip,
        limit=limit
    )
    return plants


@router.get("/to-water", response_model=List[dict])
async def plants_to_water_endpoint(
    days_ago: int = Query(0, ge=0, description="Jours depuis dernier arrosage"),
    db: Session = Depends(get_db),
):
    """Plantes à arroser: jamais arrosées ou arrosées il y a N jours"""
    plants = PlantService.get_plants_to_water(db, days_ago=days_ago)
    return plants


@router.get("/to-fertilize", response_model=List[dict])
async def plants_to_fertilize_endpoint(
    days_ago: int = Query(0, ge=0, description="Jours depuis dernière fertilisation"),
    db: Session = Depends(get_db),
):
    """Plantes à fertiliser: jamais fertilisées ou fertilisées il y a N jours"""
    plants = PlantService.get_plants_to_fertilize(db, days_ago=days_ago)
    return plants


@router.get("/favorites", response_model=List[PlantListResponse])
async def get_favorite_plants(
    db: Session = Depends(get_db),
):
    """Récupère les plantes favorites"""
    plants = PlantService.get_favorites(db)
    return plants


# ===== ROUTES AVEC PARAMÈTRES D'ID (à placer APRÈS les routes sans params) =====

@router.get("/{plant_id}", response_model=PlantResponse)
async def get_plant(
    plant_id: int,
    db: Session = Depends(get_db),
):
    """Récupère les détails d'une plante"""
    plant = PlantService.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    return plant


@router.put("/{plant_id}", response_model=PlantResponse)
async def update_plant(
    plant_id: int,
    plant_data: PlantUpdate,
    db: Session = Depends(get_db),
):
    """Met à jour une plante"""
    plant = PlantService.update(db, plant_id, plant_data)
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    return plant


@router.delete("/{plant_id}", status_code=204)
async def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
):
    """Supprime une plante (soft delete)"""
    success = PlantService.delete(db, plant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    return None


@router.post("/{plant_id}/regenerate-reference", response_model=PlantResponse)
async def regenerate_reference(
    plant_id: int,
    db: Session = Depends(get_db),
):
    """
    Régénère la référence d'une plante existante
    
    Utilise la famille actuelle pour générer une nouvelle référence unique.
    Remplace l'ancienne référence.
    
    Args:
        plant_id: ID de la plante
    
    Returns:
        Plant: Plante avec nouvelle référence
    """
    try:
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            raise HTTPException(status_code=404, detail="Plante non trouvée")
        
        if not plant.family:
            raise HTTPException(
                status_code=400, 
                detail="La plante doit avoir une famille pour régénérer la référence"
            )
        
        # Générer nouvelle référence
        new_reference = PlantService.generate_reference(db, plant.family)
        
        # Mettre à jour la plante
        plant.reference = new_reference
        db.commit()
        db.refresh(plant)
        
        return plant
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.post("/{plant_id}/archive", response_model=PlantResponse)
async def archive_plant(
    plant_id: int,
    db: Session = Depends(get_db),
):
    """Archive une plante"""
    plant = PlantService.archive(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    return plant


@router.post("/{plant_id}/restore", response_model=PlantResponse)
async def restore_plant(
    plant_id: int,
    db: Session = Depends(get_db),
):
    """Restaure une plante archivée"""
    plant = PlantService.restore(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    return plant


@router.get("/{plant_id}/seasonal-watering/{season_id}")
async def get_seasonal_watering(
    plant_id: int,
    season_id: int,
    db: Session = Depends(get_db),
):
    """Récupère la fréquence d'arrosage pour une saison donnée"""
    from app.models.lookup import PlantSeasonalWatering, WateringFrequency
    
    seasonal = db.query(PlantSeasonalWatering).filter(
        PlantSeasonalWatering.plant_id == plant_id,
        PlantSeasonalWatering.season_id == season_id
    ).first()
    
    if not seasonal or not seasonal.watering_frequency_id:
        raise HTTPException(status_code=404, detail="Fréquence saisonnière non trouvée")
    
    freq = db.query(WateringFrequency).filter_by(id=seasonal.watering_frequency_id).first()
    if not freq:
        raise HTTPException(status_code=404, detail="Fréquence non trouvée")
    
    return {"id": freq.id, "name": freq.name, "days_interval": freq.days_interval}


@router.put("/{plant_id}/seasonal-watering/{season_id}")
async def update_seasonal_watering(
    plant_id: int,
    season_id: int,
    data: dict,
    db: Session = Depends(get_db),
):
    """Met à jour la fréquence d'arrosage pour une saison donnée"""
    from app.models.lookup import PlantSeasonalWatering, WateringFrequency
    
    seasonal = db.query(PlantSeasonalWatering).filter(
        PlantSeasonalWatering.plant_id == plant_id,
        PlantSeasonalWatering.season_id == season_id
    ).first()
    
    if not seasonal:
        # Créer un nouveau si n'existe pas
        seasonal = PlantSeasonalWatering(
            plant_id=plant_id,
            season_id=season_id,
            watering_frequency_id=data.get("watering_frequency_id")
        )
        db.add(seasonal)
    else:
        # Mettre à jour
        seasonal.watering_frequency_id = data.get("watering_frequency_id")
    
    db.commit()
    db.refresh(seasonal)
    
    if seasonal.watering_frequency_id:
        freq = db.query(WateringFrequency).filter_by(id=seasonal.watering_frequency_id).first()
        return {"id": freq.id, "name": freq.name, "days_interval": freq.days_interval}
    
    return {"id": seasonal.id, "message": "Fréquence mise à jour"}


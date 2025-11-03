"""
Endpoints FastAPI pour les plantes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.schemas.plant_schema import PlantCreate, PlantUpdate, PlantResponse, PlantListResponse
from app.services import PlantService
from app.models.lookup import Location
from app.utils.sync_health import sync_plant_health_status, sync_all_plants_health
from app.utils.season_helper import get_current_season_id


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
    
    # Enrichir avec le nom de l'emplacement
    if plant.location_id:
        location = db.query(Location).filter(Location.id == plant.location_id).first()
        if location:
            plant.location_name = location.name
    
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
    
    # Retourner vide si pas de données ou pas de fréquence définie
    if not seasonal or not seasonal.watering_frequency_id:
        return None
    
    freq = db.query(WateringFrequency).filter_by(id=seasonal.watering_frequency_id).first()
    if not freq:
        return None
    
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


@router.get("/{plant_id}/seasonal-fertilizing/{season_id}")
async def get_seasonal_fertilizing(
    plant_id: int,
    season_id: int,
    db: Session = Depends(get_db),
):
    """Récupère la fréquence de fertilisation pour une saison donnée"""
    from app.models.lookup import PlantSeasonalFertilizing, FertilizerFrequency
    
    seasonal = db.query(PlantSeasonalFertilizing).filter(
        PlantSeasonalFertilizing.plant_id == plant_id,
        PlantSeasonalFertilizing.season_id == season_id
    ).first()
    
    # Retourner vide si pas de données ou pas de fréquence définie
    if not seasonal or not seasonal.fertilizer_frequency_id:
        return None
    
    freq = db.query(FertilizerFrequency).filter_by(id=seasonal.fertilizer_frequency_id).first()
    if not freq:
        return None
    
    return {"id": freq.id, "name": freq.name, "weeks_interval": freq.weeks_interval}


@router.put("/{plant_id}/seasonal-fertilizing/{season_id}")
async def update_seasonal_fertilizing(
    plant_id: int,
    season_id: int,
    data: dict,
    db: Session = Depends(get_db),
):
    """Met à jour la fréquence de fertilisation pour une saison donnée"""
    from app.models.lookup import PlantSeasonalFertilizing, FertilizerFrequency
    
    seasonal = db.query(PlantSeasonalFertilizing).filter(
        PlantSeasonalFertilizing.plant_id == plant_id,
        PlantSeasonalFertilizing.season_id == season_id
    ).first()
    
    if not seasonal:
        # Créer un nouveau si n'existe pas
        seasonal = PlantSeasonalFertilizing(
            plant_id=plant_id,
            season_id=season_id,
            fertilizer_frequency_id=data.get("fertilizer_frequency_id")
        )
        db.add(seasonal)
    else:
        # Mettre à jour
        seasonal.fertilizer_frequency_id = data.get("fertilizer_frequency_id")
    
    db.commit()
    db.refresh(seasonal)
    
    if seasonal.fertilizer_frequency_id:
        freq = db.query(FertilizerFrequency).filter_by(id=seasonal.fertilizer_frequency_id).first()
        return {"id": freq.id, "name": freq.name, "weeks_interval": freq.weeks_interval}
    
    return {"id": seasonal.id, "message": "Fréquence mise à jour"}


# ===== SYNCHRONISATION DE LA SANTÉ =====

@router.post("/admin/sync-health/{plant_id}")
async def sync_single_plant_health(plant_id: int, db: Session = Depends(get_db)):
    """
    Synchronise l'état de santé d'une plante unique avec son dernier historique de maladie
    """
    plant = sync_plant_health_status(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    return {
        "id": plant.id,
        "name": plant.name,
        "health_status": plant.health_status,
        "message": "État de santé synchronisé"
    }


@router.post("/admin/sync-health-all")
async def sync_all_plants_health_endpoint(db: Session = Depends(get_db)):
    """
    Synchronise l'état de santé de TOUTES les plantes avec leurs historiques
    """
    count = sync_all_plants_health(db)
    
    return {
        "count": count,
        "message": f"État de santé de {count} plantes synchronisés"
    }


@router.get("/{plant_id}/current-season-watering")
async def get_current_season_watering(plant_id: int, db: Session = Depends(get_db)):
    """
    Récupère la fréquence d'arrosage pour la saison actuelle
    """
    from datetime import datetime
    from app.models.lookup import Season, PlantSeasonalWatering, WateringFrequency
    
    # Obtenir le mois courant
    current_month = datetime.now().month
    
    # Obtenir toutes les saisons
    seasons = db.query(Season).all()
    if not seasons:
        return {"frequency_name": None, "message": "Pas de saisons définies"}
    
    # Trouver la saison courante
    current_season_id = get_current_season_id(current_month, seasons)
    if not current_season_id:
        return {"frequency_name": None, "message": "Saison non trouvée"}
    
    current_season = db.query(Season).filter(Season.id == current_season_id).first()
    
    # Trouver la fréquence d'arrosage pour cette plante et cette saison
    seasonal_watering = db.query(PlantSeasonalWatering).filter(
        PlantSeasonalWatering.plant_id == plant_id,
        PlantSeasonalWatering.season_id == current_season.id
    ).first()
    
    if not seasonal_watering or not seasonal_watering.watering_frequency_id:
        return {"frequency_name": None, "season": current_season.name, "message": "Pas de fréquence définie"}
    
    # Obtenir le nom de la fréquence
    frequency = db.query(WateringFrequency).filter(
        WateringFrequency.id == seasonal_watering.watering_frequency_id
    ).first()
    
    if not frequency:
        return {"frequency_name": None, "season": current_season.name, "message": "Fréquence non trouvée"}
    
    # Extraire les 2 premiers mots (ignoring contenu entre parenthèses)
    freq_name = frequency.name
    # Enlever ce qui est entre parenthèses
    freq_name_clean = freq_name.split('(')[0].strip()
    # Prendre les 2 premiers mots
    freq_name_parts = freq_name_clean.split()
    short_name = ' '.join(freq_name_parts[:2]) if len(freq_name_parts) > 0 else freq_name_clean
    
    return {
        "frequency_name": short_name,
        "full_frequency_name": frequency.name,
        "season": current_season.name,
        "season_id": current_season.id
    }


"""
Endpoints FastAPI pour les historiques (5 types)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.schemas.history_schema import (
    WateringHistoryCreate, WateringHistoryUpdate, WateringHistoryResponse,
    FertilizingHistoryCreate, FertilizingHistoryUpdate, FertilizingHistoryResponse,
    RepottingHistoryCreate, RepottingHistoryUpdate, RepottingHistoryResponse,
    DiseaseHistoryCreate, DiseaseHistoryUpdate, DiseaseHistoryResponse,
    PlantHistoryCreate, PlantHistoryUpdate, PlantHistoryResponse,
)
from app.services.history_service import HistoryService
from app.models.plant import Plant
from app.utils.sync_health import sync_plant_health_status

# Créer 5 routers pour chaque type d'historique
watering_router = APIRouter(prefix="/api/plants", tags=["watering-history"])
fertilizing_router = APIRouter(prefix="/api/plants", tags=["fertilizing-history"])
repotting_router = APIRouter(prefix="/api/plants", tags=["repotting-history"])
disease_router = APIRouter(prefix="/api/plants", tags=["disease-history"])
notes_router = APIRouter(prefix="/api/plants", tags=["plant-notes"])


# ===== WATERING HISTORY =====

@watering_router.post("/{plant_id}/watering-history", response_model=WateringHistoryResponse, status_code=201)
async def create_watering(plant_id: int, data: WateringHistoryCreate, db: Session = Depends(get_db)):
    """Créer une entrée d'arrosage"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    history = HistoryService.create_watering(db, plant_id, data)
    return history


@watering_router.get("/{plant_id}/watering-history", response_model=List[WateringHistoryResponse])
async def get_watering_list(plant_id: int, db: Session = Depends(get_db)):
    """Lister les arrosages"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    return HistoryService.get_all_watering(db, plant_id)


@watering_router.get("/{plant_id}/watering-history/{history_id}", response_model=WateringHistoryResponse)
async def get_watering(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Récupérer une entrée d'arrosage"""
    history = HistoryService.get_watering(db, plant_id, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@watering_router.put("/{plant_id}/watering-history/{history_id}", response_model=WateringHistoryResponse)
async def update_watering(plant_id: int, history_id: int, data: WateringHistoryUpdate, db: Session = Depends(get_db)):
    """Mettre à jour une entrée d'arrosage"""
    history = HistoryService.update_watering(db, plant_id, history_id, data)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@watering_router.delete("/{plant_id}/watering-history/{history_id}", status_code=204)
async def delete_watering(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Supprimer une entrée d'arrosage"""
    success = HistoryService.delete_watering(db, plant_id, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return None


# ===== FERTILIZING HISTORY =====

@fertilizing_router.post("/{plant_id}/fertilizing-history", response_model=FertilizingHistoryResponse, status_code=201)
async def create_fertilizing(plant_id: int, data: FertilizingHistoryCreate, db: Session = Depends(get_db)):
    """Créer une entrée de fertilisation"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    history = HistoryService.create_fertilizing(db, plant_id, data)
    return history


@fertilizing_router.get("/{plant_id}/fertilizing-history", response_model=List[FertilizingHistoryResponse])
async def get_fertilizing_list(plant_id: int, db: Session = Depends(get_db)):
    """Lister les fertilisations"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    return HistoryService.get_all_fertilizing(db, plant_id)


@fertilizing_router.get("/{plant_id}/fertilizing-history/{history_id}", response_model=FertilizingHistoryResponse)
async def get_fertilizing(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Récupérer une fertilisation"""
    history = HistoryService.get_fertilizing(db, plant_id, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@fertilizing_router.put("/{plant_id}/fertilizing-history/{history_id}", response_model=FertilizingHistoryResponse)
async def update_fertilizing(plant_id: int, history_id: int, data: FertilizingHistoryUpdate, db: Session = Depends(get_db)):
    """Mettre à jour une fertilisation"""
    history = HistoryService.update_fertilizing(db, plant_id, history_id, data)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@fertilizing_router.delete("/{plant_id}/fertilizing-history/{history_id}", status_code=204)
async def delete_fertilizing(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Supprimer une fertilisation"""
    success = HistoryService.delete_fertilizing(db, plant_id, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return None


# ===== REPOTTING HISTORY =====

@repotting_router.post("/{plant_id}/repotting-history", response_model=RepottingHistoryResponse, status_code=201)
async def create_repotting(plant_id: int, data: RepottingHistoryCreate, db: Session = Depends(get_db)):
    """Créer une entrée de rempotage"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    history = HistoryService.create_repotting(db, plant_id, data)
    return history


@repotting_router.get("/{plant_id}/repotting-history", response_model=List[RepottingHistoryResponse])
async def get_repotting_list(plant_id: int, db: Session = Depends(get_db)):
    """Lister les rempotages"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    return HistoryService.get_all_repotting(db, plant_id)


@repotting_router.get("/{plant_id}/repotting-history/{history_id}", response_model=RepottingHistoryResponse)
async def get_repotting(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Récupérer un rempotage"""
    history = HistoryService.get_repotting(db, plant_id, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@repotting_router.put("/{plant_id}/repotting-history/{history_id}", response_model=RepottingHistoryResponse)
async def update_repotting(plant_id: int, history_id: int, data: RepottingHistoryUpdate, db: Session = Depends(get_db)):
    """Mettre à jour un rempotage"""
    history = HistoryService.update_repotting(db, plant_id, history_id, data)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@repotting_router.delete("/{plant_id}/repotting-history/{history_id}", status_code=204)
async def delete_repotting(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Supprimer un rempotage"""
    success = HistoryService.delete_repotting(db, plant_id, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return None


# ===== DISEASE HISTORY =====

@disease_router.post("/{plant_id}/disease-history", response_model=DiseaseHistoryResponse, status_code=201)
async def create_disease(plant_id: int, data: DiseaseHistoryCreate, db: Session = Depends(get_db)):
    """Créer une entrée de maladie"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    history = HistoryService.create_disease(db, plant_id, data)
    
    # Synchroniser l'état de santé de la plante
    sync_plant_health_status(db, plant_id)
    
    return history


@disease_router.get("/{plant_id}/disease-history", response_model=List[DiseaseHistoryResponse])
async def get_disease_list(plant_id: int, db: Session = Depends(get_db)):
    """Lister les maladies"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    return HistoryService.get_all_disease(db, plant_id)


@disease_router.get("/{plant_id}/disease-history/{history_id}", response_model=DiseaseHistoryResponse)
async def get_disease(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Récupérer une maladie"""
    history = HistoryService.get_disease(db, plant_id, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@disease_router.put("/{plant_id}/disease-history/{history_id}", response_model=DiseaseHistoryResponse)
async def update_disease(plant_id: int, history_id: int, data: DiseaseHistoryUpdate, db: Session = Depends(get_db)):
    """Mettre à jour une maladie"""
    history = HistoryService.update_disease(db, plant_id, history_id, data)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    
    # Synchroniser l'état de santé de la plante
    sync_plant_health_status(db, plant_id)
    
    return history


@disease_router.delete("/{plant_id}/disease-history/{history_id}", status_code=204)
async def delete_disease(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Supprimer une maladie"""
    success = HistoryService.delete_disease(db, plant_id, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    
    # Synchroniser l'état de santé de la plante après suppression
    sync_plant_health_status(db, plant_id)
    
    return None


# ===== PLANT HISTORY (NOTES) =====

@notes_router.post("/{plant_id}/plant-history", response_model=PlantHistoryResponse, status_code=201)
async def create_plant_note(plant_id: int, data: PlantHistoryCreate, db: Session = Depends(get_db)):
    """Créer une note"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    history = HistoryService.create_plant_note(db, plant_id, data)
    return history


@notes_router.get("/{plant_id}/plant-history", response_model=List[PlantHistoryResponse])
async def get_plant_notes_list(plant_id: int, db: Session = Depends(get_db)):
    """Lister les notes"""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    return HistoryService.get_all_plant_notes(db, plant_id)


@notes_router.get("/{plant_id}/plant-history/{history_id}", response_model=PlantHistoryResponse)
async def get_plant_note(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Récupérer une note"""
    history = HistoryService.get_plant_note(db, plant_id, history_id)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@notes_router.put("/{plant_id}/plant-history/{history_id}", response_model=PlantHistoryResponse)
async def update_plant_note(plant_id: int, history_id: int, data: PlantHistoryUpdate, db: Session = Depends(get_db)):
    """Mettre à jour une note"""
    history = HistoryService.update_plant_note(db, plant_id, history_id, data)
    if not history:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return history


@notes_router.delete("/{plant_id}/plant-history/{history_id}", status_code=204)
async def delete_plant_note(plant_id: int, history_id: int, db: Session = Depends(get_db)):
    """Supprimer une note"""
    success = HistoryService.delete_plant_note(db, plant_id, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    return None

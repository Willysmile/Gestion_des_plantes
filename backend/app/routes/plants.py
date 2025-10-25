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
async def search_plants(
    q: str = Query(..., min_length=1, description="Terme de recherche"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Recherche les plantes par nom"""
    plants = PlantService.search(db, q, skip=skip, limit=limit)
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

"""
Endpoints FastAPI pour les photos
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.schemas.photo_schema import PhotoResponse, PhotoUploadResponse
from app.services.photo_service import PhotoService
from app.models.plant import Plant, Photo

router = APIRouter(
    prefix="/api/plants",
    tags=["photos"],
)

# Routeur séparé pour serveur les fichiers (sans prefix)
files_router = APIRouter(
    tags=["files"],
)


@router.post("/{plant_id}/photos", response_model=PhotoUploadResponse, status_code=201)
async def upload_photo(
    plant_id: int,
    file: UploadFile = File(...),
    description: str = Query(None),
    db: Session = Depends(get_db),
):
    """Upload une photo pour une plante"""
    
    # Vérifier que la plante existe
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    # Lire le fichier
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lecture fichier: {str(e)}")
    
    # Traiter l'upload
    success, photo, msg = PhotoService.process_upload(
        plant_id=plant_id,
        file_content=file_content,
        filename=file.filename,
        db=db,
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    
    # Ajouter description si fournie
    if description:
        photo.description = description
        db.commit()
        db.refresh(photo)
    
    return PhotoUploadResponse(
        **photo.__dict__,
        thumbnail_url=f"/api/photos/{plant_id}/{photo.filename}/thumb",
        photo_url=f"/api/photos/{plant_id}/{photo.filename}",
    )


@router.get("/{plant_id}/photos", response_model=List[PhotoResponse])
async def list_photos(
    plant_id: int,
    db: Session = Depends(get_db),
):
    """Récupère les photos d'une plante"""
    
    # Vérifier que la plante existe
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.deleted_at == None).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    photos = PhotoService.get_photos(db, plant_id)
    return photos


@router.get("/{plant_id}/photos/{photo_id}", response_model=PhotoResponse)
async def get_photo_info(
    plant_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
):
    """Récupère les infos d'une photo"""
    
    photo = PhotoService.get_photo(db, photo_id, plant_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    return photo


@router.delete("/{plant_id}/photos/{photo_id}", status_code=204)
async def delete_photo(
    plant_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
):
    """Supprime une photo (soft delete)"""
    
    success = PhotoService.delete_photo(db, photo_id, plant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    return None


@router.patch("/{plant_id}/photos/{photo_id}/set-main", response_model=PhotoResponse)
async def set_main_photo(
    plant_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
):
    """Désigne une photo comme main photo"""
    
    photo = PhotoService.set_main_photo(db, photo_id, plant_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    return photo


# ===== ROUTES DE SERVEUR DE FICHIERS =====

@files_router.get("/api/photos/{plant_id}/{filename}")
async def get_photo_file(
    plant_id: int,
    filename: str,
    thumb: bool = Query(False, description="Retourner le thumbnail"),
    db: Session = Depends(get_db),
):
    """Servir le fichier photo (full resolution ou thumbnail)"""
    
    # Récupérer la photo de la DB pour vérifier qu'elle existe et n'est pas supprimée
    photo = db.query(Photo).filter(
        Photo.plant_id == plant_id,
        Photo.filename == filename,
        Photo.deleted_at == None
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    # Récupérer le chemin du fichier
    if thumb:
        file_path = PhotoService.get_thumbnail_path(photo)
    else:
        file_path = PhotoService.get_file_path(photo)
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        path=file_path,
        media_type="image/webp",
        filename=f"{filename}",
    )

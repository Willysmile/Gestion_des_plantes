"""
Routes pour la gestion des photos
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Path as PathParam, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pathlib import Path
import logging

from app.utils.db import get_db
from app.models.plant import Plant
from app.models.photo import Photo as PhotoModel
from app.schemas.photo_schema import PhotoResponse, PhotoUploadResponse
from app.services.photo_service import PhotoService
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/plants", tags=["photos"])
files_router = APIRouter(tags=["files"])


@router.post("/{plant_id}/photos", response_model=PhotoUploadResponse, status_code=201)
async def upload_photo(
    plant_id: int = PathParam(..., gt=0),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Télécharge une photo pour une plante avec UUID
    - Convertit en WebP
    - Génère versions (large, medium, thumbnail)
    - Stocke les métadonnées en DB
    """
    # Vérifier que la plante existe
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    # Lire le fichier
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lecture fichier: {str(e)}")
    
    # Traiter l'upload avec PhotoService (utilise UUID)
    success, photo, msg = PhotoService.process_upload(
        plant_id=plant_id,
        file_content=file_content,
        filename=file.filename or "photo.jpg",
        db=db,
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    
    # Construire la réponse avec URLs
    response_data = {
        'id': photo.id,
        'plant_id': photo.plant_id,
        'filename': photo.filename,
        'file_size': photo.file_size,
        'is_primary': photo.is_primary,
        'created_at': photo.created_at,
        'updated_at': photo.updated_at,
        'urls': {
            'large': f'/api/photos/{plant_id}/{photo.filename}',
            'medium': f'/api/photos/{plant_id}/{photo.filename}?size=medium',
            'thumbnail': f'/api/photos/{plant_id}/{photo.filename}?size=thumb'
        }
    }
    
    return response_data


@router.get("/{plant_id}/photos", response_model=list[PhotoResponse])
async def get_photos(
    plant_id: int = PathParam(..., gt=0),
    db: Session = Depends(get_db)
):
    """Récupère toutes les photos d'une plante"""
    # Vérifier que la plante existe
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    photos = db.query(PhotoModel).filter(
        PhotoModel.plant_id == plant_id
    ).order_by(desc(PhotoModel.created_at)).all()
    
    return photos


@router.delete("/{plant_id}/photos/{photo_id}", status_code=204)
async def delete_photo(
    plant_id: int = PathParam(..., gt=0),
    photo_id: int = PathParam(..., gt=0),
    db: Session = Depends(get_db)
):
    """Supprime une photo et ses fichiers"""
    # Utiliser PhotoService pour suppression complète
    success = PhotoService.delete_photo(db, photo_id, plant_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    logger.info(f"Photo {photo_id} supprimée de la plante {plant_id}")


@router.put("/{plant_id}/photos/{photo_id}/set-primary", response_model=PhotoResponse)
async def set_primary_photo(
    plant_id: int = PathParam(..., gt=0),
    photo_id: int = PathParam(..., gt=0),
    db: Session = Depends(get_db)
):
    """Désigne une photo comme la principale"""
    # Vérifier que la photo existe
    photo = db.query(PhotoModel).filter(
        PhotoModel.id == photo_id,
        PhotoModel.plant_id == plant_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    # Retirer le flag principal de toutes les photos de cette plante
    db.query(PhotoModel).filter(
        PhotoModel.plant_id == plant_id
    ).update({'is_primary': False})
    
    # Désigner celle-ci comme principale
    photo.is_primary = True
    db.add(photo)
    db.commit()
    db.refresh(photo)
    
    logger.info(f"Photo {photo_id} désignée comme principale pour la plante {plant_id}")
    
    return photo


# ===== ROUTES DE SERVEUR DE FICHIERS =====

@files_router.get("/api/photos/{plant_id}/{filename}")
async def get_photo_file(
    plant_id: int,
    filename: str,
    thumb: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Servir le fichier photo JPG"""
    # Vérifier que la photo existe en DB
    photo = db.query(PhotoModel).filter(
        PhotoModel.plant_id == plant_id,
        PhotoModel.filename == filename
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    # Construire le chemin du fichier - les photos sont directement dans /data/photos/
    file_path = settings.PHOTOS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    # Détecter le type MIME selon l'extension
    media_type = "image/jpeg"
    if filename.lower().endswith(".png"):
        media_type = "image/png"
    elif filename.lower().endswith(".webp"):
        media_type = "image/webp"
    elif filename.lower().endswith(".gif"):
        media_type = "image/gif"
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )

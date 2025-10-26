"""
Routes pour la gestion des photos
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Path as PathParam
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pathlib import Path
import logging

from app.utils.db import get_db
from app.models.plant import Plant
from app.models.photo import Photo as PhotoModel
from app.schemas.photo_schema import PhotoResponse, PhotoUploadResponse
from app.utils.image_processor import validate_image_upload, process_image_to_webp, delete_photo_files

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
    Télécharge une photo pour une plante
    - Convertit en WebP
    - Génère 3 versions (large, medium, thumbnail)
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
    
    # Valider l'image
    validation = validate_image_upload(file_content, file.filename or "unknown")
    if not validation['valid']:
        raise HTTPException(status_code=400, detail=validation['error'])
    
    # Obtenir le prochain ID photo pour cette plante
    last_photo = db.query(PhotoModel).filter(
        PhotoModel.plant_id == plant_id
    ).order_by(desc(PhotoModel.id)).first()
    
    photo_id = (last_photo.id + 1) if last_photo else 1
    
    # Traiter l'image en WebP
    result = process_image_to_webp(file_content, plant_id, photo_id)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    
    # Déterminer si c'est la première/principale photo
    is_primary = not bool(last_photo)
    
    # Créer l'enregistrement en DB (utiliser la version large comme fichier principal)
    large_info = result['files']['large']
    
    photo = PhotoModel(
        plant_id=plant_id,
        filename=large_info['filename'],
        file_size=large_info['file_size'],
        width=result['original_width'],
        height=result['original_height'],
        is_primary=is_primary
    )
    
    db.add(photo)
    db.commit()
    db.refresh(photo)
    
    logger.info(f"Photo {photo.id} créée pour la plante {plant_id}")
    
    # Construire la réponse avec URLs - utiliser model_dump et ajouter urls
    response_data = {
        'id': photo.id,
        'plant_id': photo.plant_id,
        'filename': large_info['filename'],
        'file_size': large_info['file_size'],
        'width': result['original_width'],
        'height': result['original_height'],
        'is_primary': photo.is_primary,
        'created_at': photo.created_at,
        'updated_at': photo.updated_at,
        'urls': {
            'large': f'/api/photos/{plant_id}/{large_info["filename"]}',
            'medium': f'/api/photos/{plant_id}/{result["files"]["medium"]["filename"]}',
            'thumbnail': f'/api/photos/{plant_id}/{result["files"]["thumbnail"]["filename"]}'
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
    """Supprime une photo"""
    # Vérifier que la photo existe
    photo = db.query(PhotoModel).filter(
        PhotoModel.id == photo_id,
        PhotoModel.plant_id == plant_id
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    # Supprimer les fichiers physiques
    delete_photo_files(plant_id, photo_id)
    
    # Si c'était la principale, en désigner une autre
    if photo.is_primary:
        other_photo = db.query(PhotoModel).filter(
            PhotoModel.plant_id == plant_id,
            PhotoModel.id != photo_id
        ).order_by(PhotoModel.created_at).first()
        
        if other_photo:
            other_photo.is_primary = True
            db.add(other_photo)
    
    # Supprimer de la DB
    db.delete(photo)
    db.commit()
    
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
    plant_id: int = PathParam(..., gt=0),
    filename: str = PathParam(...),
    db: Session = Depends(get_db)
):
    """Servir le fichier photo WebP"""
    # Vérifier que la photo existe en DB
    photo = db.query(PhotoModel).filter(
        PhotoModel.plant_id == plant_id,
        PhotoModel.filename == filename
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo non trouvée")
    
    # Construire le chemin du fichier
    file_path = Path(f'data/photos/{plant_id}/{filename}')
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        path=file_path,
        media_type="image/webp",
        filename=filename
    )

"""
Service pour gérer les photos de plantes
Upload, conversion WebP, compression, stockage
"""

import os
import uuid
import logging
from pathlib import Path
from io import BytesIO
from PIL import Image
from sqlalchemy.orm import Session
from typing import Optional, Tuple
from datetime import datetime

from app.models.photo import Photo
from app.config import settings

logger = logging.getLogger(__name__)


class PhotoService:
    """Service pour gérer les photos"""
    
    # Constantes
    MAX_FILE_SIZE = 500 * 1024  # 500KB
    MAX_TOTAL_PER_PLANT = 5 * 1024 * 1024  # 5MB
    ALLOWED_FORMATS = {"JPEG", "PNG", "GIF", "BMP", "TIFF", "WEBP"}
    THUMBNAIL_SIZE = (300, 300)
    WEBP_QUALITY = 85
    MAX_IMAGE_SIZE = (2000, 2000)
    
    @staticmethod
    def _get_plant_photos_path(plant_id: int) -> Path:
        """Retourne le chemin du dossier photos pour une plante"""
        path = settings.PHOTOS_DIR / str(plant_id)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def _get_plant_thumbs_path(plant_id: int) -> Path:
        """Retourne le chemin du dossier thumbnails pour une plante"""
        path = settings.PHOTOS_DIR / str(plant_id) / "thumbs"
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def _validate_file(file_content: bytes) -> Tuple[bool, str]:
        """Valide le fichier avant traitement"""
        # Vérifier la taille
        if len(file_content) > PhotoService.MAX_FILE_SIZE * 2:  # 2x car non compressé
            return False, f"Fichier trop volumineux (max 500KB après compression)"
        
        # Vérifier que c'est une image
        try:
            img = Image.open(BytesIO(file_content))
            if img.format and img.format.upper() not in PhotoService.ALLOWED_FORMATS:
                return False, f"Format non accepté. Acceptés: {', '.join(PhotoService.ALLOWED_FORMATS)}"
            return True, "OK"
        except Exception as e:
            return False, f"Fichier invalide: {str(e)}"
    
    @staticmethod
    def _convert_to_webp(image: Image.Image, quality: int = 85) -> bytes:
        """Convertit une image en WebP"""
        output = BytesIO()
        
        # Convertir en RGB si nécessaire (pour support WebP)
        if image.mode in ("RGBA", "LA", "P"):
            # Créer un fond blanc pour les images avec transparence
            background = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        
        image.save(output, format="WEBP", quality=quality, method=6)
        return output.getvalue()
    
    @staticmethod
    def _compress_to_target(image_bytes: bytes, target_size: int = MAX_FILE_SIZE) -> bytes:
        """Compresse l'image jusqu'à atteindre la taille cible"""
        img = Image.open(BytesIO(image_bytes))
        
        quality = PhotoService.WEBP_QUALITY
        while quality > 50:
            webp_data = PhotoService._convert_to_webp(img, quality)
            if len(webp_data) <= target_size:
                return webp_data
            quality -= 5
        
        # Si encore trop volumineux, redimensionner
        if len(webp_data) > target_size:
            img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
            quality = PhotoService.WEBP_QUALITY
            while quality > 50:
                webp_data = PhotoService._convert_to_webp(img, quality)
                if len(webp_data) <= target_size:
                    return webp_data
                quality -= 5
        
        return webp_data
    
    @staticmethod
    def process_upload(
        plant_id: int,
        file_content: bytes,
        filename: str,
        db: Session,
    ) -> Tuple[bool, Optional[Photo], str]:
        """
        Traite l'upload d'une photo:
        1. Valide le fichier
        2. Redimensionne si besoin
        3. Convertit en WebP + compression
        4. Génère thumbnail
        5. Sauvegarde fichiers et metadata
        """
        
        # 1. Valider
        valid, msg = PhotoService._validate_file(file_content)
        if not valid:
            return False, None, msg
        
        # 2. Vérifier quota total de la plante
        plant_photos_dir = PhotoService._get_plant_photos_path(plant_id)
        total_size = sum(
            f.stat().st_size for f in plant_photos_dir.rglob("*.webp")
            if "thumbs" not in str(f)
        )
        
        if total_size > PhotoService.MAX_TOTAL_PER_PLANT:
            return False, None, f"Quota de 5MB atteint pour cette plante"
        
        # 3. Ouvrir et redimensionner
        img = Image.open(BytesIO(file_content))
        img.thumbnail(PhotoService.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        # 4. Convertir en WebP + compression
        webp_data = PhotoService._compress_to_target(file_content)
        
        if len(webp_data) > PhotoService.MAX_FILE_SIZE:
            return False, None, "Impossible de compresser le fichier assez (>500KB)"
        
        # 5. Générer thumbnail
        img.thumbnail(PhotoService.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        thumb_data = PhotoService._convert_to_webp(img, PhotoService.WEBP_QUALITY)
        
        # 6. Générer UUID et sauver fichiers
        file_uuid = str(uuid.uuid4())
        file_path = PhotoService._get_plant_photos_path(plant_id) / f"{file_uuid}.webp"
        thumb_path = PhotoService._get_plant_thumbs_path(plant_id) / f"{file_uuid}.webp"
        
        try:
            with open(file_path, "wb") as f:
                f.write(webp_data)
            with open(thumb_path, "wb") as f:
                f.write(thumb_data)
        except Exception as e:
            return False, None, f"Erreur lors de la sauvegarde: {str(e)}"
        
        # 7. Sauver metadata en DB
        try:
            # Si c'est la première photo, la marquer comme primary
            existing_photos = db.query(Photo).filter(
                Photo.plant_id == plant_id
            ).count()
            
            photo = Photo(
                plant_id=plant_id,
                filename=f"{file_uuid}.webp",
                file_size=len(webp_data),
                is_primary=(existing_photos == 0),  # Première photo = primary
            )
            db.add(photo)
            db.commit()
            db.refresh(photo)
            
            return True, photo, "Photo uploadée avec succès"
        except Exception as e:
            # Nettoyer les fichiers si DB échoue
            file_path.unlink(missing_ok=True)
            thumb_path.unlink(missing_ok=True)
            return False, None, f"Erreur DB: {str(e)}"
    
    @staticmethod
    def get_photos(db: Session, plant_id: int) -> list:
        """Récupère toutes les photos d'une plante"""
        return db.query(Photo).filter(
            Photo.plant_id == plant_id
        ).order_by(Photo.is_primary.desc(), Photo.created_at.asc()).all()
    
    @staticmethod
    def get_photo(db: Session, photo_id: int, plant_id: int) -> Optional[Photo]:
        """Récupère une photo spécifique"""
        return db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.plant_id == plant_id
        ).first()
    
    @staticmethod
    def delete_photo(db: Session, photo_id: int, plant_id: int) -> bool:
        """Supprime une photo (fichiers + base de données)"""
        photo = PhotoService.get_photo(db, photo_id, plant_id)
        if not photo:
            return False
        
        # 1. Supprimer les fichiers physiques
        try:
            # Supprimer la photo principale
            photo_path = PhotoService.get_file_path(photo)
            if photo_path.exists():
                photo_path.unlink()
            
            # Supprimer la thumbnail
            thumb_path = PhotoService.get_thumbnail_path(photo)
            if thumb_path.exists():
                thumb_path.unlink()
        except Exception as e:
            # Log l'erreur mais continue la suppression en DB
            logger.error(f"Erreur suppression fichiers photo {photo_id}: {str(e)}")
        
        # 2. Supprimer de la base de données
        try:
            # Si c'était la photo primary, désigner une autre
            if photo.is_primary:
                next_photo = db.query(Photo).filter(
                    Photo.plant_id == plant_id,
                    Photo.id != photo_id
                ).first()
                
                if next_photo:
                    next_photo.is_primary = True
                    db.add(next_photo)
            
            db.delete(photo)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Erreur suppression photo en DB {photo_id}: {str(e)}")
            return False
    
    @staticmethod
    def set_main_photo(db: Session, photo_id: int, plant_id: int) -> Optional[Photo]:
        """Désigne une photo comme primary"""
        photo = PhotoService.get_photo(db, photo_id, plant_id)
        if not photo:
            return None
        
        # Désélectionner l'ancienne primary
        db.query(Photo).filter(
            Photo.plant_id == plant_id,
            Photo.is_primary == True,
            Photo.id != photo_id
        ).update({"is_primary": False})
        
        # Sélectionner la nouvelle
        photo.is_primary = True
        db.commit()
        db.refresh(photo)
        return photo
    
    @staticmethod
    def get_file_path(photo: Photo) -> Path:
        """Retourne le chemin complet du fichier photo"""
        return settings.PHOTOS_DIR / str(photo.plant_id) / photo.filename
    
    @staticmethod
    def get_thumbnail_path(photo: Photo) -> Path:
        """Retourne le chemin complet du thumbnail"""
        return settings.PHOTOS_DIR / str(photo.plant_id) / "thumbs" / photo.filename

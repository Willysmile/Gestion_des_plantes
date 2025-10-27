"""
Image processing utilities for WebP conversion and optimization
"""

import io
import os
from pathlib import Path
from PIL import Image, ImageOps
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# Configuration
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
MAX_STORED_SIZE = 800 * 1024        # 800KB
WEBP_QUALITY = 80

# Image versions to generate
VERSIONS = {
    'large': {'size': (1200, 1200), 'max_size': 800 * 1024},
    'medium': {'size': (400, 400), 'max_size': 300 * 1024},
    'thumbnail': {'size': (150, 150), 'max_size': 100 * 1024},
}


def validate_image_upload(file_content: bytes, filename: str) -> dict:
    """
    Validate uploaded image
    
    Returns: {'valid': bool, 'error': str or None, 'mime_type': str}
    """
    # Check size
    if len(file_content) > MAX_UPLOAD_SIZE:
        return {
            'valid': False,
            'error': f'File size exceeds 5MB limit',
            'mime_type': None
        }
    
    # Check if it's a valid image
    try:
        image = Image.open(io.BytesIO(file_content))
        mime_type = image.format.lower()
        
        # Check supported formats
        if mime_type not in ['jpeg', 'jpg', 'png', 'gif', 'webp']:
            return {
                'valid': False,
                'error': f'Unsupported format: {mime_type}. Allowed: JPG, PNG, GIF, WebP',
                'mime_type': None
            }
        
        return {
            'valid': True,
            'error': None,
            'mime_type': f'image/{mime_type.lower()}'
        }
    except Exception as e:
        return {
            'valid': False,
            'error': f'Invalid image file: {str(e)}',
            'mime_type': None
        }


def process_image_to_webp(
    file_content: bytes,
    plant_id: int,
    photo_id: int
) -> dict:
    """
    Process uploaded image to WebP format in multiple sizes
    
    Args:
        file_content: Raw image bytes
        plant_id: Plant ID for directory structure
        photo_id: Photo ID for filename
    
    Returns: {
        'success': bool,
        'error': str or None,
        'files': {
            'large': {'filename': str, 'file_size': int},
            'medium': {...},
            'thumbnail': {...}
        },
        'original_width': int,
        'original_height': int
    }
    """
    try:
        # Open and validate image
        image = Image.open(io.BytesIO(file_content))
        original_width = image.width
        original_height = image.height
        
        # Convert to RGB if needed (remove alpha channel for JPEG/WebP)
        if image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create photos directory using settings
        photos_dir = settings.PHOTOS_DIR / str(plant_id)
        photos_dir.mkdir(parents=True, exist_ok=True)
        
        files = {}
        
        # Generate each version
        for version_name, version_config in VERSIONS.items():
            target_size = version_config['size']
            max_size = version_config['max_size']
            
            # Resize WITHOUT crop (keep aspect ratio)
            resized = image.copy()
            resized.thumbnail(target_size, Image.LANCZOS)
            
            # Determine filename
            if version_name == 'large':
                filename = f'photo_{photo_id}.webp'
            else:
                filename = f'photo_{photo_id}_{version_name}.webp'
            
            filepath = photos_dir / filename
            
            # Save as WebP with quality adjustment
            quality = WEBP_QUALITY
            
            # Iterative quality reduction if file too large
            for _ in range(5):  # Try up to 5 times
                buffer = io.BytesIO()
                resized.save(buffer, format='WebP', quality=quality, method=6)
                buffer.seek(0)
                file_bytes = buffer.read()
                
                if len(file_bytes) <= max_size:
                    break
                
                # Reduce quality and try again
                quality -= 10
                if quality < 30:
                    logger.warning(
                        f'Could not compress {version_name} to {max_size} bytes, '
                        f'using quality {quality} (size: {len(file_bytes)} bytes)'
                    )
                    break
            
            # Write file
            with open(filepath, 'wb') as f:
                f.write(file_bytes)
            
            files[version_name] = {
                'filename': filename,
                'file_size': len(file_bytes)
            }
            
            logger.info(f'Generated {version_name} for photo {photo_id}: {len(file_bytes)} bytes')
        
        return {
            'success': True,
            'error': None,
            'files': files,
            'original_width': original_width,
            'original_height': original_height
        }
    
    except Exception as e:
        logger.error(f'Error processing image: {str(e)}')
        return {
            'success': False,
            'error': f'Image processing failed: {str(e)}',
            'files': None,
            'original_width': None,
            'original_height': None
        }


def delete_photo_files(plant_id: int, photo_id: int, filename: str = None) -> bool:
    """
    Delete all versions of a photo (large, medium, thumbnail)
    Uses filename if provided (from DB), otherwise falls back to photo_id pattern
    
    Returns: True if successful
    """
    try:
        photos_dir = settings.PHOTOS_DIR / str(plant_id)
        
        # If filename provided (from DB), use it
        if filename:
            # Remove extension for base name
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            
            # Delete main photo
            main_photo = photos_dir / f'{base_name}.webp'
            if main_photo.exists():
                main_photo.unlink()
                logger.info(f'Deleted {main_photo}')
            
            # Delete thumbnail
            thumb_dir = photos_dir / 'thumbs'
            thumb_photo = thumb_dir / f'{base_name}.webp'
            if thumb_photo.exists():
                thumb_photo.unlink()
                logger.info(f'Deleted {thumb_photo}')
        else:
            # Fallback: try the old naming pattern photo_{photo_id}
            for version_name in VERSIONS.keys():
                if version_name == 'large':
                    filename_pattern = f'photo_{photo_id}.webp'
                else:
                    filename_pattern = f'photo_{photo_id}_{version_name}.webp'
                
                filepath = photos_dir / filename_pattern
                
                if filepath.exists():
                    filepath.unlink()
                    logger.info(f'Deleted {filepath}')
        
        # Remove directory if empty
        if photos_dir.exists() and not any(photos_dir.iterdir()):
            photos_dir.rmdir()
            logger.info(f'Removed empty directory {photos_dir}')
        
        return True
    
    except Exception as e:
        logger.error(f'Error deleting photo files: {str(e)}')
        return False

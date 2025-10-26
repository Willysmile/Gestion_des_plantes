"""
Pydantic schemas pour Photo CRUD
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class PhotoResponse(BaseModel):
    """Schéma pour les réponses photo"""
    
    id: int
    plant_id: int
    filename: str
    file_size: int
    width: Optional[int] = None
    height: Optional[int] = None
    is_primary: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PhotoUploadResponse(PhotoResponse):
    """Schéma pour la réponse d'upload"""
    
    urls: dict = Field(..., description="URLs pour les différentes versions WebP")
    
    model_config = ConfigDict(from_attributes=True)


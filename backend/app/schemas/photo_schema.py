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
    description: Optional[str] = None
    is_main: bool
    deleted_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PhotoUploadResponse(BaseModel):
    """Schéma pour la réponse d'upload"""
    
    id: int
    plant_id: int
    filename: str
    file_size: int
    description: Optional[str] = None
    is_main: bool
    thumbnail_url: str
    photo_url: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

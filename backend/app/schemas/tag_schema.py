"""
Pydantic schemas pour Tag/TagCategory CRUD
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class TagCategoryResponse(BaseModel):
    """Réponse pour une catégorie de tags"""
    
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TagResponse(BaseModel):
    """Réponse pour un tag"""
    
    id: int
    name: str
    tag_category_id: Optional[int] = None
    category: Optional[TagCategoryResponse] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TagCreate(BaseModel):
    """Schéma pour créer un tag"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Nom du tag")
    tag_category_id: int = Field(..., description="ID de la catégorie")
    
    model_config = ConfigDict(from_attributes=True)


class TagUpdate(BaseModel):
    """Schéma pour mettre à jour un tag"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    tag_category_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class TagCategoryCreate(BaseModel):
    """Schéma pour créer une catégorie de tags"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Nom de la catégorie")
    
    model_config = ConfigDict(from_attributes=True)


class TagCategoryWithTags(BaseModel):
    """Catégorie avec ses tags"""
    
    id: int
    name: str
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

"""
Pydantic schemas pour Plant CRUD (Pydantic v2 with model_validator)
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List
from datetime import datetime


class PlantCreate(BaseModel):
    """Schéma pour créer une plante"""
    
    # Obligatoires
    name: str = Field(..., min_length=1, max_length=100, description="Nom commun de la plante")
    
    # Optionnels - Info botanique
    scientific_name: Optional[str] = Field(None, max_length=150)
    family: Optional[str] = Field(None, max_length=100)
    subfamily: Optional[str] = Field(None, max_length=100)
    genus: Optional[str] = Field(None, max_length=100)
    species: Optional[str] = Field(None, max_length=100)
    subspecies: Optional[str] = Field(None, max_length=100)
    variety: Optional[str] = Field(None, max_length=100)
    cultivar: Optional[str] = Field(None, max_length=100)
    reference: Optional[str] = Field(None, max_length=100, description="Identifiant unique pour l'utilisateur")
    
    # Description
    description: Optional[str] = None
    health_status: Optional[str] = Field("healthy", description="healthy, sick, recovering, dead")
    difficulty_level: Optional[str] = Field(None, description="easy, medium, hard")
    growth_speed: Optional[str] = Field(None, description="slow, medium, fast")
    flowering_season: Optional[str] = Field(None, max_length=100)
    
    # Location & Purchase
    location_id: Optional[int] = None
    purchase_date: Optional[str] = Field(None, description="Format: dd/mm/yyyy ou mm/yyyy")
    purchase_place_id: Optional[int] = None
    purchase_price: Optional[float] = None
    
    # Environment
    watering_frequency_id: Optional[int] = None
    light_requirement_id: Optional[int] = None
    preferred_watering_method_id: Optional[int] = None
    preferred_water_type_id: Optional[int] = None
    temperature_min: Optional[int] = None
    temperature_max: Optional[int] = None
    humidity_level: Optional[int] = None
    soil_humidity: Optional[str] = None
    soil_type: Optional[str] = None
    pot_size: Optional[str] = None
    
    # Flags
    is_indoor: bool = False
    is_outdoor: bool = False
    is_favorite: bool = False
    is_toxic: bool = False
    
    # Tags (IDs des tags manuels, les tags auto sont générés)
    tag_ids: Optional[List[int]] = Field(None, description="IDs des tags à associer (tags manuels)")
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Valide que le nom n'est pas vide"""
        if not v or not v.strip():
            raise ValueError("Le nom ne peut pas être vide")
        return v.strip()
    
    @field_validator("temperature_min", "temperature_max")
    @classmethod
    def validate_temps(cls, v):
        """Valide que les températures sont raisonnables"""
        if v is not None and (v < -50 or v > 60):
            raise ValueError("Température invalide (doit être entre -50 et 60°C)")
        return v
    
    @field_validator("humidity_level")
    @classmethod
    def validate_humidity(cls, v):
        """Valide que l'humidité est entre 0 et 100"""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("L'humidité doit être entre 0 et 100%")
        return v
    
    @field_validator("purchase_price")
    @classmethod
    def validate_price(cls, v):
        """Valide que le prix est positif"""
        if v is not None and v < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        return v
    
    @model_validator(mode='after')
    def validate_temperature_range(self):
        """Valide que temperature_min < temperature_max (cross-field validation)"""
        if self.temperature_min is not None and self.temperature_max is not None:
            if self.temperature_min >= self.temperature_max:
                raise ValueError("temperature_min doit être < temperature_max")
        return self
    
    model_config = ConfigDict(from_attributes=True)


class SimpleTagResponse(BaseModel):
    """Réponse simple pour un tag (pour éviter les imports circulaires)"""
    
    id: int
    name: str
    tag_category_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class PlantUpdate(PlantCreate):
    """Schéma pour mettre à jour une plante (tous les champs optionnels)"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class PlantResponse(BaseModel):
    """Schéma pour les réponses GET"""
    
    id: int
    name: str
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    subfamily: Optional[str] = None
    genus: Optional[str] = None
    species: Optional[str] = None
    subspecies: Optional[str] = None
    variety: Optional[str] = None
    cultivar: Optional[str] = None
    reference: Optional[str] = None
    description: Optional[str] = None
    health_status: Optional[str] = None
    difficulty_level: Optional[str] = None
    growth_speed: Optional[str] = None
    flowering_season: Optional[str] = None
    location_id: Optional[int] = None
    purchase_date: Optional[str] = None
    purchase_place_id: Optional[int] = None
    purchase_price: Optional[float] = None
    watering_frequency_id: Optional[int] = None
    light_requirement_id: Optional[int] = None
    preferred_watering_method_id: Optional[int] = None
    preferred_water_type_id: Optional[int] = None
    temperature_min: Optional[int] = None
    temperature_max: Optional[int] = None
    humidity_level: Optional[int] = None
    soil_humidity: Optional[str] = None
    soil_type: Optional[str] = None
    pot_size: Optional[str] = None
    is_indoor: bool
    is_outdoor: bool
    is_favorite: bool
    is_toxic: bool
    is_archived: bool
    archived_date: Optional[datetime] = None
    archived_reason: Optional[str] = None
    deleted_at: Optional[datetime] = None
    tags: List[SimpleTagResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PlantListResponse(BaseModel):
    """Schéma pour les réponses de liste (sans toutes les infos)"""
    
    id: int
    name: str
    reference: Optional[str] = None
    scientific_name: Optional[str] = None
    health_status: Optional[str] = None
    location_id: Optional[int] = None
    is_favorite: bool
    is_archived: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

from sqlalchemy import Column, String, Integer
from app.models.base import BaseModel

class Location(BaseModel):
    __tablename__ = "locations"
    name = Column(String(100), unique=True, nullable=False)

class PurchasePlace(BaseModel):
    __tablename__ = "purchase_places"
    name = Column(String(100), unique=True, nullable=False)

class WateringFrequency(BaseModel):
    __tablename__ = "watering_frequencies"
    name = Column(String(100), unique=True, nullable=False)

class LightRequirement(BaseModel):
    __tablename__ = "light_requirements"
    name = Column(String(100), unique=True, nullable=False)

class FertilizerType(BaseModel):
    __tablename__ = "fertilizer_types"
    name = Column(String(100), unique=True, nullable=False)

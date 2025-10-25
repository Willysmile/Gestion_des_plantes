from sqlalchemy import Column, String, Integer, Text
from app.models.base import BaseModel

class Location(BaseModel):
    __tablename__ = "locations"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class PurchasePlace(BaseModel):
    __tablename__ = "purchase_places"
    name = Column(String(100), unique=True, nullable=False)
    url = Column(String(255), nullable=True)

class WateringFrequency(BaseModel):
    __tablename__ = "watering_frequencies"
    name = Column(String(100), unique=True, nullable=False)
    days_interval = Column(Integer, nullable=True)

class LightRequirement(BaseModel):
    __tablename__ = "light_requirements"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class FertilizerType(BaseModel):
    __tablename__ = "fertilizer_types"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

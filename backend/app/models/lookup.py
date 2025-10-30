from sqlalchemy import Column, String, Integer, Text
from app.models.base import BaseModel

class Unit(BaseModel):
    __tablename__ = "units"
    name = Column(String(50), unique=True, nullable=False)
    symbol = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)

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
    unit = Column(String(50), nullable=False, default="ml")  # ml, g, cuillère, etc.

class DiseaseType(BaseModel):
    __tablename__ = "disease_types"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class TreatmentType(BaseModel):
    __tablename__ = "treatment_types"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class PlantHealthStatus(BaseModel):
    __tablename__ = "plant_health_statuses"
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class WateringMethod(BaseModel):
    __tablename__ = "watering_methods"
    name = Column(String(100), unique=True, nullable=False)  # par le dessus, par le dessous, etc.
    description = Column(Text, nullable=True)

class WaterType(BaseModel):
    __tablename__ = "water_types"
    name = Column(String(50), unique=True, nullable=False)  # pluie, robinet_reposee, filtree, distillee
    description = Column(Text, nullable=True)

class Season(BaseModel):
    __tablename__ = "seasons"
    name = Column(String(50), unique=True, nullable=False)  # printemps, été, automne, hiver
    start_month = Column(Integer, nullable=False)  # 1-12
    end_month = Column(Integer, nullable=False)  # 1-12
    description = Column(Text, nullable=True)


from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Plant(BaseModel):
    __tablename__ = "plants"
    
    # Basic info
    name = Column(String(100), nullable=False, index=True)
    scientific_name = Column(String(150))
    family = Column(String(100))
    subfamily = Column(String(100))
    genus = Column(String(100))
    species = Column(String(100))
    subspecies = Column(String(100))
    variety = Column(String(100))
    cultivar = Column(String(100))
    reference = Column(String(100), unique=True, index=True)
    
    # Description
    description = Column(Text)
    health_status = Column(String(50))  # healthy, sick, recovering, dead
    difficulty_level = Column(String(50))  # easy, medium, hard
    growth_speed = Column(String(50))  # slow, medium, fast
    flowering_season = Column(String(100))
    
    # Location & Purchase
    location_id = Column(Integer, ForeignKey("locations.id"))
    purchase_date = Column(String(20))
    purchase_place_id = Column(Integer, ForeignKey("purchase_places.id"))
    purchase_price = Column(DECIMAL(10, 2))
    
    # Environment
    watering_frequency_id = Column(Integer, ForeignKey("watering_frequencies.id"))
    light_requirement_id = Column(Integer, ForeignKey("light_requirements.id"))
    temperature_min = Column(Integer)
    temperature_max = Column(Integer)
    humidity_level = Column(Integer)
    soil_humidity = Column(String(50))
    soil_type = Column(String(100))
    pot_size = Column(String(50))
    
    # Flags
    is_indoor = Column(Boolean, default=False)
    is_outdoor = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    is_toxic = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    photos = relationship("Photo", back_populates="plant", cascade="all, delete-orphan")
    watering_histories = relationship("WateringHistory", back_populates="plant")
    fertilizing_histories = relationship("FertilizingHistory", back_populates="plant")
    repotting_histories = relationship("RepottingHistory", back_populates="plant")
    disease_histories = relationship("DiseaseHistory", back_populates="plant")
    plant_histories = relationship("PlantHistory", back_populates="plant")

class Photo(BaseModel):
    __tablename__ = "photos"
    
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=True)  # Size of the file in bytes
    description = Column(Text)
    is_main = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    plant = relationship("Plant", back_populates="photos")

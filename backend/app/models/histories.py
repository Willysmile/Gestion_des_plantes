from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class WateringHistory(BaseModel):
    __tablename__ = "watering_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    watering_date = Column(DateTime, nullable=False)
    amount = Column(String(100))
    notes = Column(Text)
    plant = relationship("Plant", back_populates="watering_histories")

class FertilizingHistory(BaseModel):
    __tablename__ = "fertilizing_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    fertilizing_date = Column(DateTime, nullable=False)
    fertilizer_type = Column(String(100))
    amount = Column(String(100))
    notes = Column(Text)
    plant = relationship("Plant", back_populates="fertilizing_histories")

class RepottingHistory(BaseModel):
    __tablename__ = "repotting_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    repotting_date = Column(DateTime, nullable=False)
    old_pot_size = Column(String(50))
    new_pot_size = Column(String(50))
    soil_type = Column(String(100))
    notes = Column(Text)
    plant = relationship("Plant", back_populates="repotting_histories")

class DiseaseHistory(BaseModel):
    __tablename__ = "disease_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    disease_date = Column(DateTime, nullable=False)
    disease_name = Column(String(100))
    treatment = Column(String(255))
    status = Column(String(50))
    notes = Column(Text)
    plant = relationship("Plant", back_populates="disease_histories")

class PlantHistory(BaseModel):
    __tablename__ = "plant_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    history_date = Column(DateTime, nullable=False)
    event_type = Column(String(100))
    notes = Column(Text, nullable=False)
    plant = relationship("Plant", back_populates="plant_histories")

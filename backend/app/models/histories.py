from sqlalchemy import Column, String, Integer, DateTime, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class WateringHistory(BaseModel):
    __tablename__ = "watering_histories"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    date = Column(Date, nullable=False)
    amount_ml = Column(Integer)
    notes = Column(Text)
    deleted_at = Column(DateTime, nullable=True)
    plant = relationship("Plant", back_populates="watering_histories")

class FertilizingHistory(BaseModel):
    __tablename__ = "fertilizing_histories"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    date = Column(Date, nullable=False)
    fertilizer_type_id = Column(Integer, ForeignKey("fertilizer_types.id"))
    amount = Column(String(100))
    notes = Column(Text)
    deleted_at = Column(DateTime, nullable=True)
    plant = relationship("Plant", back_populates="fertilizing_histories")

class RepottingHistory(BaseModel):
    __tablename__ = "repotting_histories"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    date = Column(Date, nullable=False)
    soil_type = Column(String(100))
    pot_size = Column(String(50))
    notes = Column(Text)
    deleted_at = Column(DateTime, nullable=True)
    plant = relationship("Plant", back_populates="repotting_histories")

class DiseaseHistory(BaseModel):
    __tablename__ = "disease_histories"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    date = Column(Date, nullable=False)
    disease_name = Column(String(100), nullable=False)
    treatment = Column(String(255))
    treated_date = Column(Date)
    recovered = Column(Boolean, default=False)
    notes = Column(Text)
    deleted_at = Column(DateTime, nullable=True)
    plant = relationship("Plant", back_populates="disease_histories")

class PlantHistory(BaseModel):
    __tablename__ = "plant_histories"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    date = Column(Date, nullable=False)
    title = Column(String(100))
    note = Column(Text, nullable=False)
    category = Column(String(50))
    deleted_at = Column(DateTime, nullable=True)
    plant = relationship("Plant", back_populates="plant_histories")

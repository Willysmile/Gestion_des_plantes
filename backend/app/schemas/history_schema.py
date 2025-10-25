from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class WateringHistoryCreate(BaseModel):
    date: date
    amount_ml: Optional[int] = None
    notes: Optional[str] = None


class WateringHistoryUpdate(BaseModel):
    date: Optional[date] = None
    amount_ml: Optional[int] = None
    notes: Optional[str] = None


class WateringHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: date
    amount_ml: Optional[int]
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class FertilizingHistoryCreate(BaseModel):
    date: date
    fertilizer_type_id: Optional[int] = None
    amount: Optional[str] = None
    notes: Optional[str] = None


class FertilizingHistoryUpdate(BaseModel):
    date: Optional[date] = None
    fertilizer_type_id: Optional[int] = None
    amount: Optional[str] = None
    notes: Optional[str] = None


class FertilizingHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: date
    fertilizer_type_id: Optional[int]
    amount: Optional[str]
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class RepottingHistoryCreate(BaseModel):
    date: date
    soil_type: Optional[str] = None
    pot_size: Optional[str] = None
    notes: Optional[str] = None


class RepottingHistoryUpdate(BaseModel):
    date: Optional[date] = None
    soil_type: Optional[str] = None
    pot_size: Optional[str] = None
    notes: Optional[str] = None


class RepottingHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: date
    soil_type: Optional[str]
    pot_size: Optional[str]
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class DiseaseHistoryCreate(BaseModel):
    date: date
    disease_name: str
    treatment: Optional[str] = None
    treated_date: Optional[date] = None
    recovered: bool = False
    notes: Optional[str] = None


class DiseaseHistoryUpdate(BaseModel):
    date: Optional[date] = None
    disease_name: Optional[str] = None
    treatment: Optional[str] = None
    treated_date: Optional[date] = None
    recovered: Optional[bool] = None
    notes: Optional[str] = None


class DiseaseHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: date
    disease_name: str
    treatment: Optional[str]
    treated_date: Optional[date]
    recovered: bool
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class PlantHistoryCreate(BaseModel):
    date: date
    title: Optional[str] = None
    note: str
    category: Optional[str] = None


class PlantHistoryUpdate(BaseModel):
    date: Optional[date] = None
    title: Optional[str] = None
    note: Optional[str] = None
    category: Optional[str] = None


class PlantHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: date
    title: Optional[str]
    note: str
    category: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None

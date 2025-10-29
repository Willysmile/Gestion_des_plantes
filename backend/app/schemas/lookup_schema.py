from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Disease Type schemas
class DiseaseTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None


class DiseaseTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DiseaseTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Treatment Type schemas
class TreatmentTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TreatmentTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TreatmentTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Plant Health Status schemas
class PlantHealthStatusCreate(BaseModel):
    name: str
    description: Optional[str] = None


class PlantHealthStatusUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PlantHealthStatusResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Fertilizer Type schemas (already exists, but adding for consistency)
class FertilizerTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    unit: str = "ml"


class FertilizerTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None


class FertilizerTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    unit: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

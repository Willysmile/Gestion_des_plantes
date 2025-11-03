from pydantic import BaseModel, field_validator, ConfigDict, Field
from typing import Optional
from datetime import datetime
from datetime import date as DateType
from app.utils.validators import validate_not_future_date


class WateringHistoryCreate(BaseModel):
    date: DateType
    amount_ml: Optional[int] = None
    notes: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        return validate_not_future_date(v)


class WateringHistoryUpdate(BaseModel):
    date: Optional[DateType] = Field(default=None)
    amount_ml: Optional[int] = Field(default=None)
    notes: Optional[str] = Field(default=None)

    @field_validator('date', mode='before')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            if isinstance(v, str):
                from datetime import datetime as dt
                v = dt.strptime(v, '%Y-%m-%d').date()
            return validate_not_future_date(v)
        return v


class WateringHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: DateType
    amount_ml: Optional[int]
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class FertilizingHistoryCreate(BaseModel):
    date: DateType
    fertilizer_type_id: Optional[int] = None
    amount: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        return validate_not_future_date(v)


class FertilizingHistoryUpdate(BaseModel):
    date: Optional[DateType] = None
    fertilizer_type_id: Optional[int] = None
    amount: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            return validate_not_future_date(v)
        return v


class FertilizingHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: DateType
    fertilizer_type_id: Optional[int]
    amount: Optional[str]
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class RepottingHistoryCreate(BaseModel):
    date: DateType
    soil_type: Optional[str] = None
    pot_size_before: Optional[int] = None
    pot_size_after: Optional[int] = None
    notes: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        return validate_not_future_date(v)


class RepottingHistoryUpdate(BaseModel):
    date: Optional[DateType] = None
    soil_type: Optional[str] = None
    pot_size_before: Optional[int] = None
    pot_size_after: Optional[int] = None
    notes: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            return validate_not_future_date(v)
        return v


class RepottingHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: DateType
    soil_type: Optional[str]
    pot_size_before: Optional[int]
    pot_size_after: Optional[int]
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class DiseaseHistoryCreate(BaseModel):
    date: DateType
    disease_type_id: Optional[int] = None
    treatment_type_id: Optional[int] = None
    health_status_id: Optional[int] = None
    treated_date: Optional[DateType] = None
    recovered: bool = False
    notes: Optional[str] = None

    @field_validator('date', 'treated_date')
    @classmethod
    def validate_dates(cls, v):
        if v is not None:
            return validate_not_future_date(v)
        return v


class DiseaseHistoryUpdate(BaseModel):
    disease_type_id: Optional[int] = None
    treatment_type_id: Optional[int] = None
    health_status_id: Optional[int] = None
    treated_date: Optional[DateType] = None
    recovered: Optional[bool] = None
    notes: Optional[str] = None

    @field_validator('treated_date')
    @classmethod
    def validate_treated_date(cls, v):
        if v is not None:
            return validate_not_future_date(v)
        return v


class DiseaseHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: DateType
    disease_type_id: Optional[int]
    treatment_type_id: Optional[int]
    health_status_id: Optional[int]
    treated_date: Optional[DateType]
    recovered: bool
    notes: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None


class PlantHistoryCreate(BaseModel):
    date: DateType
    title: Optional[str] = None
    note: str
    category: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        return validate_not_future_date(v)


class PlantHistoryUpdate(BaseModel):
    date: Optional[DateType] = None
    title: Optional[str] = None
    note: Optional[str] = None
    category: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            return validate_not_future_date(v)
        return v


class PlantHistoryResponse(BaseModel):
    id: int
    plant_id: int
    date: DateType
    title: Optional[str]
    note: str
    category: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime] = None

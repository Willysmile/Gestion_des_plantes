from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime


class PropagationEventBase(BaseModel):
    """Base schema for propagation events."""
    event_type: str
    event_date: datetime
    measurement: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None


class PropagationEventCreate(PropagationEventBase):
    """Schema for creating propagation events."""
    pass


class PropagationEventUpdate(BaseModel):
    """Schema for updating propagation events."""
    event_type: Optional[str] = None
    event_date: Optional[datetime] = None
    measurement: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None


class PropagationEventResponse(PropagationEventBase):
    """Schema for propagation event responses."""
    id: int
    propagation_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PlantPropagationBase(BaseModel):
    """Base schema for plant propagations."""
    parent_plant_id: int
    child_plant_id: Optional[int] = None
    source_type: str = Field(..., description="cutting, seeds, division, offset")
    method: str = Field(..., description="water, soil, air-layer, substrate")
    propagation_date: date
    date_harvested: date
    expected_ready: Optional[date] = None
    notes: Optional[str] = None
    success_rate_estimate: Optional[float] = 0.85


class PlantPropagationCreate(PlantPropagationBase):
    """Schema for creating plant propagations."""
    pass


class PlantPropagationUpdate(BaseModel):
    """Schema for updating plant propagations."""
    status: Optional[str] = None
    current_root_length_cm: Optional[float] = None
    current_leaves_count: Optional[int] = None
    current_roots_count: Optional[int] = None
    notes: Optional[str] = None
    expected_ready: Optional[date] = None
    success_rate_estimate: Optional[float] = None
    is_active: Optional[bool] = None


class PlantPropagationResponse(PlantPropagationBase):
    """Schema for plant propagation responses."""
    id: int
    status: str
    current_root_length_cm: Optional[float]
    current_leaves_count: Optional[int]
    current_roots_count: Optional[int]
    success_date: Optional[date]
    success_rate_estimate: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    events: List[PropagationEventResponse] = []

    class Config:
        from_attributes = True


class PropagationTimelineResponse(BaseModel):
    """Schema for propagation timeline (with calculated fields)."""
    id: int
    parent_plant_id: int
    child_plant_id: Optional[int]
    source_type: str
    method: str
    status: str
    propagation_date: date
    date_harvested: date
    expected_ready: Optional[date]
    success_date: Optional[date]
    days_since_propagation: int
    expected_duration_days: int
    is_overdue: bool
    success_rate_estimate: float
    notes: Optional[str]


class PropagationConversionRequest(BaseModel):
    """Schema for converting a propagation to an established plant."""
    child_plant_id: int = Field(..., description="ID of the plant to link as child")
    success_date: Optional[date] = None
    inherit_parent_settings: bool = Field(default=True, description="Copy parent plant settings to child")


class PropagationStatsResponse(BaseModel):
    """Schema for propagation statistics."""
    total: int
    by_status: Dict[str, int]
    by_source_type: Dict[str, int]
    by_method: Dict[str, int]
    success_rate: float
    average_duration_days: float


class GenealogyCellResponse(BaseModel):
    """Schema for a single plant in genealogy tree."""
    plant_id: int
    propagation_id: int
    source_type: str
    method: str
    propagation_date: Optional[str]
    status: str


class GenealogyTreeResponse(BaseModel):
    """Schema for plant genealogy tree."""
    id: int
    parents: List[GenealogyCellResponse]
    children: List[GenealogyCellResponse]


class PropagationCalendarEvent(BaseModel):
    """Schema for a propagation event in calendar view."""
    id: int
    parent_plant_id: int
    child_plant_id: Optional[int]
    source_type: str
    method: str
    status: str
    propagation_date: date
    expected_ready: Optional[date]
    success_date: Optional[date]
    is_overdue: bool

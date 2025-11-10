"""
Pydantic schemas pour AuditLog
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class AuditLogResponse(BaseModel):
    """Réponse pour un log d'audit"""
    
    id: int
    action: str  # INSERT, UPDATE, DELETE
    entity_type: str  # Plant, Photo, etc.
    entity_id: int
    field_name: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    description: Optional[str] = None
    raw_changes: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(BaseModel):
    """Réponse pour une liste de logs d'audit"""
    
    id: int
    action: str
    entity_type: str
    entity_id: int
    description: Optional[str] = None
    user_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

"""
Routes pour récupérer les logs d'audit
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.services.audit_service import AuditLogService
from app.schemas.audit_schema import AuditLogResponse, AuditLogListResponse
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/logs", response_model=List[AuditLogListResponse])
def get_all_logs(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Récupère tous les logs d'audit"""
    logs = AuditLogService.get_all_logs(db, limit=limit)
    return logs


@router.get("/logs/entity/{entity_type}/{entity_id}", response_model=List[AuditLogResponse])
def get_entity_logs(
    entity_type: str,
    entity_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Récupère tous les logs pour une entité spécifique"""
    logs = AuditLogService.get_logs_for_entity(db, entity_type, entity_id, limit=limit)
    return logs


@router.get("/logs/action/{action}", response_model=List[AuditLogListResponse])
def get_action_logs(
    action: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Récupère tous les logs d'une action spécifique (INSERT, UPDATE, DELETE)"""
    logs = AuditLogService.get_logs_by_action(db, action, limit=limit)
    return logs


@router.get("/logs/user/{user_id}", response_model=List[AuditLogListResponse])
def get_user_logs(
    user_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Récupère tous les logs d'un utilisateur"""
    logs = AuditLogService.get_logs_by_user(db, user_id, limit=limit)
    return logs


@router.get("/logs/recent", response_model=List[AuditLogListResponse])
def get_recent_logs(
    days: int = Query(7, ge=1, le=365),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Récupère les logs récents (derniers N jours)"""
    logs = AuditLogService.get_recent_logs(db, days=days, limit=limit)
    return logs




@router.delete("/logs/cleanup")
def cleanup_old_logs(
    days: Optional[int] = Query(None, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Supprime les logs de plus de N jours (nettoyage). Si days=None, supprime TOUS les logs"""
    count = AuditLogService.delete_old_logs(db, days=days)
    return {"deleted_count": count, "message": f"{count} logs supprimés"}


@router.post("/logs/create-test")
def create_test_log(db: Session = Depends(get_db)):
    """Crée un log de test pour la démo (développement uniquement)"""
    from datetime import datetime
    from app.models import AuditLog
    
    test_log = AuditLog(
        action="UPDATE",
        entity_type="Plant",
        entity_id=1,
        field_name="description",
        old_value="Ancienne description",
        new_value="Nouvelle description mise à jour",
        user_id=None,
        description="Log de test pour la démo",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(test_log)
    db.commit()
    db.refresh(test_log)
    return {"id": test_log.id, "message": "Log de test créé"}


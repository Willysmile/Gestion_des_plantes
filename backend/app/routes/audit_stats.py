"""
Routes pour les statistiques d'audit
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.services.audit_stats_service import AuditStatsService

router = APIRouter(prefix="/api/audit/stats", tags=["audit-stats"])


@router.get("/summary")
def get_audit_summary(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """
    Résumé complet des statistiques d'audit
    
    Retourne:
    - action_counts: {INSERT, UPDATE, DELETE}
    - entity_breakdown: Comptage par type d'entité
    - daily_activity: Activité par jour
    - top_entities: Entités les plus modifiées
    - user_activity: Activité par utilisateur
    - action_by_entity: Distribution actions/entité
    """
    return AuditStatsService.get_dashboard_summary(db, days)


@router.get("/actions")
def get_action_counts(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """
    Comptage des logs par action (INSERT, UPDATE, DELETE)
    
    Retourne: {'INSERT': 45, 'UPDATE': 120, 'DELETE': 8}
    """
    return AuditStatsService.get_action_counts(db, days)


@router.get("/entity-breakdown")
def get_entity_breakdown(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """
    Répartition des logs par type d'entité
    
    Retourne: {'Plant': 150, 'Photo': 45, 'WateringHistory': 89}
    """
    return AuditStatsService.get_entity_type_breakdown(db, days)


@router.get("/daily-activity")
def get_daily_activity(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """
    Activité quotidienne détaillée
    
    Retourne: [
        {'date': '2025-11-10', 'INSERT': 5, 'UPDATE': 12, 'DELETE': 2, 'total': 19},
        ...
    ]
    """
    return AuditStatsService.get_daily_activity(db, days)


@router.get("/top-entities")
def get_top_entities(
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Entités les plus modifiées
    
    Retourne: [
        {'entity_type': 'Plant', 'entity_id': 42, 'count': 15, 'last_modified': '2025-11-10T...'},
        ...
    ]
    """
    return AuditStatsService.get_top_entities(db, limit, days)


@router.get("/user-activity")
def get_user_activity(
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Activité par utilisateur
    
    Retourne: [
        {'user_id': 1, 'action_count': 45, 'last_action': '2025-11-10T...'},
        ...
    ]
    """
    return AuditStatsService.get_user_activity(db, limit, days)


@router.get("/action-by-entity")
def get_action_by_entity(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """
    Distribution des actions par type d'entité
    
    Retourne: {
        'Plant': {'INSERT': 10, 'UPDATE': 25, 'DELETE': 5},
        'Photo': {'INSERT': 8, 'UPDATE': 12, 'DELETE': 2},
        ...
    }
    """
    return AuditStatsService.get_action_by_entity(db, days)


@router.get("/change-frequency/{entity_type}")
def get_change_frequency(
    entity_type: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Champs les plus souvent modifiés pour un type d'entité
    
    Retourne: [
        {'field_name': 'health_status', 'change_count': 12},
        {'field_name': 'soil_humidity', 'change_count': 8},
        ...
    ]
    """
    return AuditStatsService.get_change_frequency(db, entity_type, days)

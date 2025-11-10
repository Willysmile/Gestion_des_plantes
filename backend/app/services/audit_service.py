"""
Service pour gérer les logs d'audit
"""

from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from datetime import datetime, timedelta
from typing import List, Optional
import json


class AuditLogService:
    """Service pour créer et récupérer les logs d'audit"""
    
    @staticmethod
    def log_change(db: Session, action: str, entity_type: str, entity_id: int,
                   field_name: Optional[str] = None, old_value: Optional[any] = None,
                   new_value: Optional[any] = None, user_id: Optional[int] = None,
                   description: Optional[str] = None, ip_address: Optional[str] = None,
                   user_agent: Optional[str] = None, raw_changes: Optional[dict] = None):
        """Créer un log d'audit"""
        
        log = AuditLog.create_from_change(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            user_id=user_id,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            raw_changes=raw_changes or {},
        )
        
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_logs_for_entity(db: Session, entity_type: str, entity_id: int,
                           limit: int = 100) -> List[AuditLog]:
        """Récupérer tous les logs pour une entité"""
        return db.query(AuditLog)\
            .filter(AuditLog.entity_type == entity_type, AuditLog.entity_id == entity_id)\
            .order_by(AuditLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_logs_by_action(db: Session, action: str, limit: int = 100) -> List[AuditLog]:
        """Récupérer tous les logs d'un type d'action"""
        return db.query(AuditLog)\
            .filter(AuditLog.action == action)\
            .order_by(AuditLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_logs_by_user(db: Session, user_id: int, limit: int = 100) -> List[AuditLog]:
        """Récupérer tous les logs d'un utilisateur"""
        return db.query(AuditLog)\
            .filter(AuditLog.user_id == user_id)\
            .order_by(AuditLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_logs_by_date_range(db: Session, start_date: datetime, end_date: datetime,
                               limit: int = 100) -> List[AuditLog]:
        """Récupérer les logs dans une plage de dates"""
        return db.query(AuditLog)\
            .filter(AuditLog.created_at >= start_date, AuditLog.created_at <= end_date)\
            .order_by(AuditLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_recent_logs(db: Session, days: int = 7, limit: int = 100) -> List[AuditLog]:
        """Récupérer les logs récents (derniers N jours)"""
        start_date = datetime.utcnow() - timedelta(days=days)
        return AuditLogService.get_logs_by_date_range(db, start_date, datetime.utcnow(), limit)
    
    @staticmethod
    def get_all_logs(db: Session, limit: int = 100) -> List[AuditLog]:
        """Récupérer tous les logs"""
        return db.query(AuditLog)\
            .order_by(AuditLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def delete_old_logs(db: Session, days: int = 90) -> int:
        """Supprimer les logs de plus de N jours (nettoyage)"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        count = db.query(AuditLog)\
            .filter(AuditLog.created_at < cutoff_date)\
            .delete()
        db.commit()
        return count

"""
Service pour calculer les statistiques d'audit
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.audit import AuditLog
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class AuditStatsService:
    """Service pour les statistiques d'audit"""
    
    @staticmethod
    def get_action_counts(db: Session, days: int = 30) -> Dict[str, int]:
        """
        Compter les logs par action sur les N derniers jours
        Retourne: {'INSERT': 45, 'UPDATE': 120, 'DELETE': 8}
        """
        start_date = datetime.now() - timedelta(days=days)
        
        counts = db.query(
            AuditLog.action,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(
            AuditLog.action
        ).all()
        
        return {action: count for action, count in counts}
    
    @staticmethod
    def get_entity_type_breakdown(db: Session, days: int = 30) -> Dict[str, int]:
        """
        Compter les logs par type d'entité
        Retourne: {'Plant': 150, 'Photo': 45, 'WateringHistory': 89, ...}
        """
        start_date = datetime.now() - timedelta(days=days)
        
        counts = db.query(
            AuditLog.entity_type,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(
            AuditLog.entity_type
        ).all()
        
        return {entity_type: count for entity_type, count in counts}
    
    @staticmethod
    def get_daily_activity(db: Session, days: int = 30) -> List[Dict]:
        """
        Activité quotidienne (INSERT, UPDATE, DELETE par jour)
        Retourne:
        [
            {
                'date': '2025-11-10',
                'INSERT': 5,
                'UPDATE': 12,
                'DELETE': 2,
                'total': 19
            },
            ...
        ]
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Requête pour chaque jour et action
        raw_data = db.query(
            func.date(AuditLog.created_at).label('date'),
            AuditLog.action,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(
            func.date(AuditLog.created_at),
            AuditLog.action
        ).order_by(
            func.date(AuditLog.created_at)
        ).all()
        
        # Restructurer les données
        daily_data = {}
        for date, action, count in raw_data:
            date_str = date.isoformat() if hasattr(date, 'isoformat') else str(date)
            if date_str not in daily_data:
                daily_data[date_str] = {'date': date_str, 'INSERT': 0, 'UPDATE': 0, 'DELETE': 0}
            daily_data[date_str][action] = count
        
        # Calculer totaux
        result = []
        for date_str, data in sorted(daily_data.items()):
            data['total'] = data['INSERT'] + data['UPDATE'] + data['DELETE']
            result.append(data)
        
        return result
    
    @staticmethod
    def get_top_entities(db: Session, limit: int = 10, days: int = 30) -> List[Dict]:
        """
        Entités les plus modifiées
        Retourne:
        [
            {'entity_type': 'Plant', 'entity_id': 42, 'count': 15, 'last_modified': '2025-11-10T...'},
            ...
        ]
        """
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            AuditLog.entity_type,
            AuditLog.entity_id,
            func.count(AuditLog.id).label('count'),
            func.max(AuditLog.created_at).label('last_modified')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(
            AuditLog.entity_type,
            AuditLog.entity_id
        ).order_by(
            desc(func.count(AuditLog.id))
        ).limit(limit).all()
        
        return [
            {
                'entity_type': entity_type,
                'entity_id': entity_id,
                'count': count,
                'last_modified': last_modified.isoformat() if last_modified else None
            }
            for entity_type, entity_id, count, last_modified in results
        ]
    
    @staticmethod
    def get_user_activity(db: Session, limit: int = 10, days: int = 30) -> List[Dict]:
        """
        Activité par utilisateur
        Retourne:
        [
            {'user_id': 1, 'action_count': 45, 'last_action': '2025-11-10T...'},
            ...
        ]
        """
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            AuditLog.user_id,
            func.count(AuditLog.id).label('action_count'),
            func.max(AuditLog.created_at).label('last_action')
        ).filter(
            AuditLog.created_at >= start_date,
            AuditLog.user_id.isnot(None)
        ).group_by(
            AuditLog.user_id
        ).order_by(
            desc(func.count(AuditLog.id))
        ).limit(limit).all()
        
        return [
            {
                'user_id': user_id,
                'action_count': action_count,
                'last_action': last_action.isoformat() if last_action else None
            }
            for user_id, action_count, last_action in results
        ]
    
    @staticmethod
    def get_action_by_entity(db: Session, days: int = 30) -> Dict[str, Dict[str, int]]:
        """
        Distribution des actions par type d'entité
        Retourne:
        {
            'Plant': {'INSERT': 10, 'UPDATE': 25, 'DELETE': 5},
            'Photo': {'INSERT': 8, 'UPDATE': 12, 'DELETE': 2},
            ...
        }
        """
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            AuditLog.entity_type,
            AuditLog.action,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= start_date
        ).group_by(
            AuditLog.entity_type,
            AuditLog.action
        ).all()
        
        # Restructurer
        data = {}
        for entity_type, action, count in results:
            if entity_type not in data:
                data[entity_type] = {'INSERT': 0, 'UPDATE': 0, 'DELETE': 0}
            data[entity_type][action] = count
        
        return data
    
    @staticmethod
    def get_change_frequency(db: Session, entity_type: str, days: int = 30) -> List[Dict]:
        """
        Fréquence de changements pour un type d'entité spécifique
        Retourne les champs les plus souvent modifiés
        [
            {'field_name': 'health_status', 'change_count': 12},
            {'field_name': 'soil_humidity', 'change_count': 8},
            ...
        ]
        """
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            AuditLog.field_name,
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.action == 'UPDATE',
            AuditLog.field_name.isnot(None),
            AuditLog.created_at >= start_date
        ).group_by(
            AuditLog.field_name
        ).order_by(
            desc(func.count(AuditLog.id))
        ).all()
        
        return [
            {'field_name': field_name, 'change_count': count}
            for field_name, count in results
        ]
    
    @staticmethod
    def get_dashboard_summary(db: Session, days: int = 30) -> Dict:
        """
        Résumé complet pour le dashboard
        """
        return {
            'action_counts': AuditStatsService.get_action_counts(db, days),
            'entity_breakdown': AuditStatsService.get_entity_type_breakdown(db, days),
            'daily_activity': AuditStatsService.get_daily_activity(db, days),
            'top_entities': AuditStatsService.get_top_entities(db, days=days),
            'user_activity': AuditStatsService.get_user_activity(db, days=days),
            'action_by_entity': AuditStatsService.get_action_by_entity(db, days),
            'period_days': days
        }

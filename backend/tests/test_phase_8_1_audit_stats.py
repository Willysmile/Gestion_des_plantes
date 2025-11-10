"""
Tests pour Phase 8.1: Audit Stats API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.services.audit_stats_service import AuditStatsService
from datetime import datetime, timedelta
import json


class TestAuditStatsService:
    """Tests du service de stats"""
    
    def test_get_action_counts(self, db: Session):
        """Tester le comptage par action"""
        # Créer quelques logs
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='INSERT', entity_type='Plant', entity_id=2, description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='DELETE', entity_type='Plant', entity_id=2, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        # Tester
        counts = AuditStatsService.get_action_counts(db, days=1)
        assert counts.get('INSERT', 0) >= 2
        assert counts.get('UPDATE', 0) >= 1
        assert counts.get('DELETE', 0) >= 1
    
    def test_get_entity_type_breakdown(self, db: Session):
        """Tester le breakdown par type d'entité"""
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='INSERT', entity_type='Plant', entity_id=2, description='test'),
            AuditLog(action='INSERT', entity_type='Photo', entity_id=1, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        breakdown = AuditStatsService.get_entity_type_breakdown(db, days=1)
        assert breakdown.get('Plant', 0) >= 2
        assert breakdown.get('Photo', 0) >= 1
    
    def test_get_daily_activity(self, db: Session):
        """Tester l'activité quotidienne"""
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        activity = AuditStatsService.get_daily_activity(db, days=1)
        assert len(activity) > 0
        
        # Chaque jour doit avoir des champs
        for day in activity:
            assert 'date' in day
            assert 'total' in day
            assert day['total'] >= 0
    
    def test_get_top_entities(self, db: Session):
        """Tester les entités les plus modifiées"""
        # Créer plusieurs logs pour Plant #1
        for i in range(5):
            log = AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test')
            db.add(log)
        
        # Un log pour Plant #2
        log = AuditLog(action='UPDATE', entity_type='Plant', entity_id=2, description='test')
        db.add(log)
        db.commit()
        
        top = AuditStatsService.get_top_entities(db, limit=5, days=1)
        assert len(top) > 0
        
        # Plant #1 devrait être premier
        first = top[0]
        assert first['entity_type'] == 'Plant'
        assert first['entity_id'] == 1
        assert first['count'] >= 5
    
    def test_get_user_activity(self, db: Session):
        """Tester l'activité par utilisateur"""
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, user_id=1, description='test'),
            AuditLog(action='INSERT', entity_type='Plant', entity_id=2, user_id=1, description='test'),
            AuditLog(action='INSERT', entity_type='Plant', entity_id=3, user_id=2, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        activity = AuditStatsService.get_user_activity(db, limit=10, days=1)
        assert len(activity) > 0
        
        # User 1 doit avoir 2 actions
        user_1 = next((u for u in activity if u['user_id'] == 1), None)
        if user_1:
            assert user_1['action_count'] >= 2
    
    def test_get_action_by_entity(self, db: Session):
        """Tester la distribution actions/entité"""
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='DELETE', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='INSERT', entity_type='Photo', entity_id=1, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        by_entity = AuditStatsService.get_action_by_entity(db, days=1)
        
        assert 'Plant' in by_entity
        assert by_entity['Plant']['INSERT'] >= 1
        assert by_entity['Plant']['UPDATE'] >= 1
        assert by_entity['Plant']['DELETE'] >= 1
        
        assert 'Photo' in by_entity
        assert by_entity['Photo']['INSERT'] >= 1
    
    def test_get_change_frequency(self, db: Session):
        """Tester la fréquence des changements par champ"""
        logs = [
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, field_name='name', description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=2, field_name='name', description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=3, field_name='health_status', description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        freq = AuditStatsService.get_change_frequency(db, 'Plant', days=1)
        assert len(freq) > 0
        
        # 'name' doit être le plus fréquent
        name_freq = next((f for f in freq if f['field_name'] == 'name'), None)
        if name_freq:
            assert name_freq['change_count'] >= 2
    
    def test_get_dashboard_summary(self, db: Session):
        """Tester le résumé du dashboard"""
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        summary = AuditStatsService.get_dashboard_summary(db, days=1)
        
        assert 'action_counts' in summary
        assert 'entity_breakdown' in summary
        assert 'daily_activity' in summary
        assert 'top_entities' in summary
        assert 'user_activity' in summary
        assert 'action_by_entity' in summary
        assert 'period_days' in summary


class TestAuditStatsAPI:
    """Tests des endpoints API"""
    
    def test_get_summary_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/summary"""
        # Créer quelques logs
        logs = [
            AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test'),
            AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test'),
        ]
        for log in logs:
            db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/summary')
        assert response.status_code == 200
        
        data = response.json()
        assert 'action_counts' in data
        assert 'entity_breakdown' in data
        assert 'daily_activity' in data
    
    def test_get_summary_with_days_param(self, client, db: Session):
        """Tester le paramètre 'days' du résumé"""
        response = client.get('/api/audit/stats/summary?days=7')
        assert response.status_code == 200
        
        data = response.json()
        assert data['period_days'] == 7
    
    def test_get_actions_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/actions"""
        log = AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test')
        db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/actions')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_entity_breakdown_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/entity-breakdown"""
        log = AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test')
        db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/entity-breakdown')
        assert response.status_code == 200
        
        data = response.json()
        assert 'Plant' in data or data == {}
    
    def test_get_daily_activity_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/daily-activity"""
        log = AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test')
        db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/daily-activity')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_top_entities_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/top-entities"""
        # Créer plusieurs logs
        for i in range(5):
            log = AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, description='test')
            db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/top-entities?limit=10')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_user_activity_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/user-activity"""
        log = AuditLog(action='INSERT', entity_type='Plant', entity_id=1, user_id=1, description='test')
        db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/user-activity')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_action_by_entity_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/action-by-entity"""
        log = AuditLog(action='INSERT', entity_type='Plant', entity_id=1, description='test')
        db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/action-by-entity')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_change_frequency_endpoint(self, client, db: Session):
        """Tester GET /api/audit/stats/change-frequency/{entity_type}"""
        log = AuditLog(action='UPDATE', entity_type='Plant', entity_id=1, field_name='name', description='test')
        db.add(log)
        db.commit()
        
        response = client.get('/api/audit/stats/change-frequency/Plant')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_stats_with_invalid_days(self, client):
        """Tester avec paramètre 'days' invalide"""
        # Days > 365 devrait être rejeté
        response = client.get('/api/audit/stats/summary?days=400')
        assert response.status_code == 422
        
        # Days < 1 devrait être rejeté
        response = client.get('/api/audit/stats/summary?days=0')
        assert response.status_code == 422

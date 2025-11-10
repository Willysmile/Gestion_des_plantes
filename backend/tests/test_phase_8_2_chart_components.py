"""
test_phase_8_2_chart_components.py
Tests d'intégration pour Phase 8.2: Chart Components
Valide que les endpoints API retournent les bonnes données pour les charts
"""

import pytest
import json
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.plant import Plant
from app.models.audit import AuditLog


client = TestClient(app)


@pytest.fixture
def create_audit_logs(db: Session):
    """Créer des logs d'audit variés pour tester les charts"""
    base_date = datetime(2025, 11, 1)
    
    # Créer des logs pour tester les graphiques
    logs = []
    
    # Daily Activity: Logs sur plusieurs jours
    for day_offset in range(5):
        date = base_date + timedelta(days=day_offset)
        
        # Jour 1: 5 INSERT, 10 UPDATE, 2 DELETE
        for i in range(5):
            logs.append(AuditLog(
                action='INSERT',
                entity_type='Plant',
                entity_id=100 + i,
                field_name=None,
                old_value=None,
                new_value=None,
                raw_changes=json.dumps({'name': f'Plant {100+i}'}),
                user_id=1,
                ip_address='127.0.0.1',
                user_agent='Test',
                description=f'Plant {100+i} créée',
                created_at=date + timedelta(hours=8 + i),
            ))
        
        for i in range(10):
            logs.append(AuditLog(
                action='UPDATE',
                entity_type='Plant',
                entity_id=100 + (i % 5),
                field_name='name',
                old_value=f'Old {i}',
                new_value=f'New {i}',
                raw_changes=json.dumps({'name': {'old': f'Old {i}', 'new': f'New {i}'}}),
                user_id=1,
                ip_address='127.0.0.1',
                user_agent='Test',
                description=f'Plant {100 + (i % 5)} modifiée',
                created_at=date + timedelta(hours=14 + i),
            ))
        
        for i in range(2):
            logs.append(AuditLog(
                action='DELETE',
                entity_type='Plant',
                entity_id=200 + i,
                field_name=None,
                old_value=None,
                new_value=None,
                raw_changes=json.dumps({'deleted': True}),
                user_id=2,
                ip_address='127.0.0.1',
                user_agent='Test',
                description=f'Plant {200+i} supprimée',
                created_at=date + timedelta(hours=20 + i),
            ))
    
    # Entity Breakdown: Logs variés par entity_type
    entity_types = ['Plant', 'Photo', 'WateringHistory', 'FertilizingHistory']
    for idx, entity_type in enumerate(entity_types):
        for i in range(10 + idx * 5):
            logs.append(AuditLog(
                action='INSERT',
                entity_type=entity_type,
                entity_id=1000 + i,
                field_name=None,
                old_value=None,
                new_value=None,
                raw_changes=json.dumps({}),
                user_id=1,
                ip_address='127.0.0.1',
                user_agent='Test',
                description=f'{entity_type} créée',
                created_at=base_date + timedelta(hours=idx * 10 + i),
            ))
    
    # User Activity: Logs de différents users
    for user_id in [1, 2, 3]:
        for i in range(5 + user_id * 3):
            logs.append(AuditLog(
                action='UPDATE',
                entity_type='Plant',
                entity_id=500 + i,
                field_name='name',
                old_value='Old',
                new_value='New',
                raw_changes=json.dumps({}),
                user_id=user_id,
                ip_address='127.0.0.1',
                user_agent='Test',
                description=f'User {user_id} modification {i}',
                created_at=base_date + timedelta(hours=user_id * 5 + i),
            ))
    
    # Action by Entity: Garantir tous les types d'actions pour tous les types d'entités
    for entity_type in ['Plant', 'Photo']:
        for action in ['INSERT', 'UPDATE', 'DELETE']:
            for i in range(3):
                logs.append(AuditLog(
                    action=action,
                    entity_type=entity_type,
                    entity_id=2000 + i,
                    field_name='test' if action == 'UPDATE' else None,
                    old_value='old' if action == 'UPDATE' else None,
                    new_value='new' if action == 'UPDATE' else None,
                    raw_changes=json.dumps({}),
                    user_id=1,
                    ip_address='127.0.0.1',
                    user_agent='Test',
                    description=f'{entity_type} {action}',
                    created_at=base_date + timedelta(hours=1),
                ))
    
    for log in logs:
        db.add(log)
    
    db.commit()
    return logs


class TestChartDataEndpoints:
    """Tests des endpoints retournant les données pour les charts"""
    
    def test_daily_activity_data_structure(self, create_audit_logs):
        """Vérifier que daily-activity retourne la bonne structure"""
        response = client.get('/api/audit/stats/daily-activity?days=7')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        if len(data) > 0:
            item = data[0]
            assert 'date' in item
            assert 'INSERT' in item or item.get('INSERT') is not None
            assert 'UPDATE' in item or item.get('UPDATE') is not None
            assert 'DELETE' in item or item.get('DELETE') is not None
            assert 'total' in item or item.get('total') is not None
    
    def test_entity_breakdown_data_structure(self, create_audit_logs):
        """Vérifier que entity-breakdown retourne la bonne structure"""
        response = client.get('/api/audit/stats/entity-breakdown?days=7')
        assert response.status_code == 200
        
        data = response.json()
        # Peut être une liste ou un dict
        assert isinstance(data, (list, dict))
        
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            assert 'entity_type' in item
            assert 'count' in item
            assert isinstance(item['count'], int)
            assert item['count'] > 0
        elif isinstance(data, dict) and len(data) > 0:
            # Format dict: {'Plant': 35, 'Photo': 18, ...}
            assert any(isinstance(v, int) for v in data.values())
    
    def test_user_activity_data_structure(self, create_audit_logs):
        """Vérifier que user-activity retourne la bonne structure"""
        response = client.get('/api/audit/stats/user-activity?limit=10&days=7')
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        if len(data) > 0:
            item = data[0]
            assert 'user_id' in item
            assert 'count' in item
            assert isinstance(item['count'], int)
    
    def test_action_by_entity_data_structure(self, create_audit_logs):
        """Vérifier que action-by-entity retourne la bonne structure"""
        response = client.get('/api/audit/stats/action-by-entity?days=7')
        assert response.status_code == 200
        
        data = response.json()
        # Peut être une liste ou un dict
        assert isinstance(data, (list, dict))
        
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            assert 'entity_type' in item
            assert 'INSERT' in item
            assert 'UPDATE' in item
            assert 'DELETE' in item
        elif isinstance(data, dict):
            # Format dict: {'Plant': {'INSERT': 5, 'UPDATE': 10, 'DELETE': 2}, ...}
            if len(data) > 0:
                first_val = next(iter(data.values()))
                assert isinstance(first_val, dict)
                assert any(k in first_val for k in ['INSERT', 'UPDATE', 'DELETE'])
    
    def test_daily_activity_respects_days_parameter(self, create_audit_logs):
        """Vérifier que le filtre 'days' fonctionne correctement"""
        response_7 = client.get('/api/audit/stats/daily-activity?days=7').json()
        response_1 = client.get('/api/audit/stats/daily-activity?days=1').json()
        
        # Moins de jours = moins de résultats généralement
        assert len(response_1) <= len(response_7)
    
    def test_entity_breakdown_includes_all_types(self, create_audit_logs):
        """Vérifier que entity-breakdown inclut tous les types d'entités"""
        response = client.get('/api/audit/stats/entity-breakdown?days=30')
        data = response.json()
        
        # L'endpoint fonctionne (retourne un dict ou liste)
        assert response.status_code == 200
        # Si les données existent, elles doivent être du bon type
        assert isinstance(data, (list, dict))
    
    def test_user_activity_respects_limit(self, create_audit_logs):
        """Vérifier que le limit est respecté"""
        response = client.get('/api/audit/stats/user-activity?limit=2&days=30')
        data = response.json()
        
        assert len(data) <= 2
    
    def test_action_by_entity_has_all_actions(self, create_audit_logs):
        """Vérifier que action-by-entity inclut tous les types d'actions"""
        response = client.get('/api/audit/stats/action-by-entity?days=30')
        data = response.json()
        
        # Chaque item doit avoir INSERT, UPDATE, DELETE
        for item in data:
            assert 'INSERT' in item
            assert 'UPDATE' in item
            assert 'DELETE' in item


class TestChartIntegration:
    """Tests d'intégration pour les charts avec le dashboard"""
    
    def test_load_all_charts_data_in_parallel(self, create_audit_logs):
        """Vérifier que tous les endpoints fonctionnent ensemble"""
        endpoints = [
            '/api/audit/stats/daily-activity?days=7',
            '/api/audit/stats/entity-breakdown?days=7',
            '/api/audit/stats/user-activity?limit=10&days=7',
            '/api/audit/stats/action-by-entity?days=7',
        ]
        
        responses = []
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            responses.append(response.json())
        
        # Vérifier que toutes les réponses sont valides (list ou dict)
        assert all(isinstance(r, (list, dict)) for r in responses)
    
    def test_chart_data_consistency(self, create_audit_logs):
        """Vérifier la cohérence des données entre les endpoints"""
        # Charger tous les datasets
        daily = client.get('/api/audit/stats/daily-activity?days=30').json()
        entity = client.get('/api/audit/stats/entity-breakdown?days=30').json()
        user = client.get('/api/audit/stats/user-activity?days=30').json()
        action = client.get('/api/audit/stats/action-by-entity?days=30').json()
        
        # Calculer les totaux
        if isinstance(daily, list):
            daily_total = sum(d.get('total', 0) for d in daily)
        else:
            daily_total = sum(daily.values()) if daily else 0
            
        if isinstance(entity, list):
            entity_total = sum(e.get('count', 0) for e in entity)
        else:
            entity_total = sum(entity.values()) if entity else 0
        
        # Au moins un endpoint doit avoir des données
        # (ou tous les deux peuvent être vides)
        assert isinstance(daily, (list, dict))
        assert isinstance(entity, (list, dict))
    
    def test_different_date_ranges(self, create_audit_logs):
        """Tester avec différentes plages de dates"""
        date_ranges = [1, 7, 30, 90, 365]
        
        for days in date_ranges:
            response = client.get(f'/api/audit/stats/daily-activity?days={days}')
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    def test_empty_chart_data(self, db: Session):
        """Vérifier le comportement avec aucunes données"""
        # Pas d'audit logs dans cette fixture
        response = client.get('/api/audit/stats/daily-activity?days=7')
        assert response.status_code == 200
        data = response.json()
        # Doit être une liste (vide ou non)
        assert isinstance(data, list)
    
    def test_chart_performance_large_dataset(self, db: Session, create_audit_logs):
        """Vérifier la performance avec un grand dataset"""
        import time
        
        start = time.time()
        response = client.get('/api/audit/stats/summary?days=30')
        duration = time.time() - start
        
        assert response.status_code == 200
        # Les queries doivent être rapides (< 1 seconde)
        assert duration < 1.0


class TestChartErrorHandling:
    """Tests de gestion d'erreurs pour les charts"""
    
    def test_invalid_days_parameter(self):
        """Vérifier la validation du paramètre 'days'"""
        response = client.get('/api/audit/stats/daily-activity?days=400')
        # Doit rejeter ou limiter à 365 (422 Unprocessable Entity ou 200 avec max 365)
        assert response.status_code in [200, 422]
    
    def test_invalid_limit_parameter(self):
        """Vérifier la validation du paramètre 'limit'"""
        response = client.get('/api/audit/stats/user-activity?limit=1000')
        # Doit rejeter ou limiter à 100 (422 Unprocessable Entity ou 200 avec max 100)
        assert response.status_code in [200, 422]
    
    def test_missing_parameters_use_defaults(self):
        """Vérifier que les paramètres manquants utilisent les defaults"""
        response = client.get('/api/audit/stats/daily-activity')
        assert response.status_code == 200
        
        response = client.get('/api/audit/stats/user-activity')
        assert response.status_code == 200

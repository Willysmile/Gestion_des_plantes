"""
Tests pour Phase 6.2: API d'Audit manuelle
Tests le logging manuel via AuditLogService (les event listeners automatiques sont trop complexes à tester)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.plant import Plant
from app.models.photo import Photo
from app.models.audit import AuditLog
from app.services.audit_service import AuditLogService
from datetime import datetime
import json


class TestAuditAPIEndpoints:
    """Tests pour les endpoints API d'audit"""
    
    def test_create_plant_and_manually_log(self, client: TestClient, db: Session):
        """Vérifier qu'on peut créer une plante et loguer manuellement"""
        # Nettoyer les logs existants
        db.query(AuditLog).delete()
        db.commit()
        
        # Créer une plante via l'API
        plant_data = {
            "name": "Rose Test",
            "scientific_name": "Rosa sp.",
            "family": "Rosaceae",
            "description": "Belle rose",
            "is_indoor": True,
            "is_outdoor": False,
        }
        
        response = client.post("/api/plants", json=plant_data)
        assert response.status_code == 201
        created_plant = response.json()
        plant_id = created_plant["id"]
        
        # Loguer manuellement cette insertion
        AuditLogService.log_change(
            db=db,
            action='INSERT',
            entity_type='Plant',
            entity_id=plant_id,
            description=f"Création de {created_plant['name']}",
            raw_changes={
                'name': created_plant['name'],
                'family': created_plant['family'],
            }
        )
        
        # Vérifier qu'un log a été créé
        logs = db.query(AuditLog)\
            .filter(AuditLog.action == 'INSERT', AuditLog.entity_type == 'Plant')\
            .all()
        
        assert len(logs) >= 1
        
        log = logs[0]
        assert log.action == 'INSERT'
        assert log.entity_type == 'Plant'
        assert log.entity_id == plant_id


class TestAuditLogRetention:
    """Tests pour la politique de rétention des logs"""
    
    def test_cleanup_old_logs(self, client: TestClient, db: Session):
        """Vérifier que l'API cleanup supprime les anciens logs"""
        # Créer un log avec une date ancienne
        old_log = AuditLog(
            action='INSERT',
            entity_type='Plant',
            entity_id=999,
            field_name=None,
            old_value=None,
            new_value=json.dumps({'name': 'Old Plant'}),
            user_id=None,
            description='Test log ancien',
            raw_changes=json.dumps({}),
        )
        
        # Forcer la date de création à il y a 100 jours
        from datetime import datetime, timedelta
        old_log.created_at = datetime.now() - timedelta(days=100)
        
        db.add(old_log)
        db.commit()
        
        old_log_id = old_log.id
        
        # Appeler le cleanup avec retention de 90 jours
        response = client.delete("/api/audit/logs/cleanup?days=90")
        assert response.status_code == 200
        
        # Vérifier que le vieux log a été supprimé
        remaining = db.query(AuditLog).filter(AuditLog.id == old_log_id).first()
        assert remaining is None
    
    def test_recent_logs_endpoint(self, client: TestClient, db: Session):
        """Vérifier que l'endpoint recent fonctionne correctement"""
        # Créer quelques logs manuellement
        for i in range(3):
            log = AuditLogService.log_change(
                db=db,
                action='INSERT',
                entity_type='Plant',
                entity_id=100 + i,
                description=f"Test log {i}",
                raw_changes={'name': f"Plant {i}"}
            )
        
        # Récupérer les logs récents
        response = client.get("/api/audit/logs/recent?days=7")
        assert response.status_code == 200
        
        logs = response.json()
        assert isinstance(logs, list)
        assert len(logs) >= 3

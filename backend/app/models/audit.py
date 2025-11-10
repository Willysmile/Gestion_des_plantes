"""
AuditLog model pour tracer tous les changements dans la base de données
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Index
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.base import BaseModel
import json
from datetime import datetime


class AuditLog(BaseModel):
    """Modèle pour enregistrer l'audit des changements"""
    
    __tablename__ = "audit_logs"
    
    # Clés pour identifier ce qui a changé
    action = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    entity_type = Column(String(100), nullable=False)  # Plant, Photo, etc.
    entity_id = Column(Integer, nullable=False)  # ID de l'entité modifiée
    
    # Détails des changements
    field_name = Column(String(100))  # Champ modifié (pour UPDATE)
    old_value = Column(Text)  # Ancienne valeur (JSON)
    new_value = Column(Text)  # Nouvelle valeur (JSON)
    
    # Contexte
    user_id = Column(Integer)  # ID de l'utilisateur qui a fait le changement
    ip_address = Column(String(45))  # IP address (IPv4 ou IPv6)
    user_agent = Column(String(255))  # User-Agent du navigateur
    
    # Métadonnées
    description = Column(String(255))  # Description textuelle du changement
    raw_changes = Column(Text)  # JSON de tous les changements
    
    def to_dict(self):
        """Convertir en dictionnaire avec parsing JSON"""
        return {
            'id': self.id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'field_name': self.field_name,
            'old_value': json.loads(self.old_value) if self.old_value else None,
            'new_value': json.loads(self.new_value) if self.new_value else None,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'description': self.description,
            'raw_changes': json.loads(self.raw_changes) if self.raw_changes else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @staticmethod
    def create_from_change(action, entity_type, entity_id, field_name=None, 
                          old_value=None, new_value=None, user_id=None, 
                          description=None, **kwargs):
        """Factory method pour créer un log d'audit"""
        return AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            field_name=field_name,
            old_value=json.dumps(old_value) if old_value is not None else None,
            new_value=json.dumps(new_value) if new_value is not None else None,
            user_id=user_id,
            description=description,
            raw_changes=json.dumps(kwargs.get('raw_changes', {})),
            ip_address=kwargs.get('ip_address'),
            user_agent=kwargs.get('user_agent'),
        )

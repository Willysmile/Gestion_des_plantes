"""
Event listeners SQLAlchemy pour auto-logger les changements aux modèles
Enregistre automatiquement INSERT, UPDATE, DELETE dans la table audit_logs
"""

from sqlalchemy import event
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.models.plant import Plant
from app.models.photo import Photo
from app.models.histories import WateringHistory, FertilizingHistory, RepottingHistory, DiseaseHistory
import json
from datetime import datetime


class AuditListeners:
    """Gestionnaire des event listeners pour l'audit automatique"""
    
    # Modèles à auditer automatiquement
    AUDITED_MODELS = [Plant, Photo, WateringHistory, FertilizingHistory]
    
    # Champs à ignorer (techniques, timestamps, etc.)
    IGNORED_FIELDS = {'id', 'created_at', 'updated_at'}
    
    @staticmethod
    def get_entity_name(mapper):
        """Extraire le nom de l'entité du mapper SQLAlchemy"""
        return mapper.class_.__name__
    
    @staticmethod
    def get_model_changes(mapper, instance):
        """
        Extraire les changements d'une instance SQLAlchemy
        Retourne {field_name: {'old': value, 'new': value}, ...}
        """
        changes = {}
        state = instance.__dict__
        
        for column in mapper.columns:
            if column.name in AuditListeners.IGNORED_FIELDS:
                continue
                
            # Récupérer la valeur actuelle
            value = getattr(instance, column.name, None)
            
            # Pour les Decimal et autres types, convertir en format sérialisable
            if value is not None and not isinstance(value, (str, int, float, bool, type(None))):
                value = str(value)
            
            changes[column.name] = value
        
        return changes
    
    @staticmethod
    def get_previous_values(mapper, instance):
        """
        Récupérer les valeurs précédentes d'une instance avant modification
        """
        from sqlalchemy.orm import attributes
        
        previous = {}
        
        for column in mapper.columns:
            if column.name in AuditListeners.IGNORED_FIELDS:
                continue
            
            # Utiliser attributes pour obtenir l'historique
            hist = attributes.get_history(instance, column.name)
            
            if hist and hist.unchanged:
                value = hist.unchanged[0] if hist.unchanged else None
            elif hist and hist.deleted:
                value = hist.deleted[0] if hist.deleted else None
            else:
                value = getattr(instance, column.name, None)
            
            # Convertir les types non-sérialisables
            if value is not None and not isinstance(value, (str, int, float, bool, type(None))):
                value = str(value)
            
            previous[column.name] = value
        
        return previous
    
    @staticmethod
    def before_insert(mapper, connection, target):
        """
        Callback avant INSERT - enregistrer la création
        """
        try:
            # Accéder à la session via la connexion
            from sqlalchemy.orm import Session
            session = Session.registry.sessions.get(id(connection))
            
            if not session:
                # Pas de session disponible (ex: en test)
                return
            
            if not hasattr(session, 'info'):
                session.info = {}
            
            entity_type = AuditListeners.get_entity_name(mapper)
            entity_id = getattr(target, 'id', None)
            
            # Enregistrer un log d'INSERT
            changes = AuditListeners.get_model_changes(mapper, target)
            
            log = AuditLog(
                action='INSERT',
                entity_type=entity_type,
                entity_id=entity_id,
                field_name=None,
                old_value=None,
                new_value=json.dumps(changes),
                user_id=session.info.get('user_id'),
                ip_address=session.info.get('ip_address'),
                user_agent=session.info.get('user_agent'),
                description=f"Création de {entity_type} #{entity_id}",
                raw_changes=json.dumps(changes),
            )
            
            session.add(log)
        except Exception as e:
            # Silencieusement ignorer les erreurs (ex: session non disponible)
            print(f"⚠️ Audit log error in before_insert: {e}")
            pass
    
    @staticmethod
    def before_update(mapper, connection, target):
        """
        Callback avant UPDATE - enregistrer les modifications
        """
        try:
            from sqlalchemy.orm import Session, attributes
            
            session = Session.registry.sessions.get(id(connection))
            if not session:
                return
            
            if not hasattr(session, 'info'):
                session.info = {}
            
            entity_type = AuditListeners.get_entity_name(mapper)
            entity_id = getattr(target, 'id', None)
            
            # Récupérer les changements
            changes = {}
            for column in mapper.columns:
                if column.name in AuditListeners.IGNORED_FIELDS:
                    continue
                
                hist = attributes.get_history(target, column.name)
                
                # Si la valeur a changé
                if hist.has_changes():
                    old_value = hist.deleted[0] if hist.deleted else None
                    new_value = hist.added[0] if hist.added else None
                    
                    # Convertir les types non-sérialisables
                    if old_value is not None and not isinstance(old_value, (str, int, float, bool, type(None))):
                        old_value = str(old_value)
                    if new_value is not None and not isinstance(new_value, (str, int, float, bool, type(None))):
                        new_value = str(new_value)
                    
                    changes[column.name] = {'old': old_value, 'new': new_value}
            
            # Créer un log pour chaque champ modifié
            for field_name, values in changes.items():
                log = AuditLog(
                    action='UPDATE',
                    entity_type=entity_type,
                    entity_id=entity_id,
                    field_name=field_name,
                    old_value=json.dumps(values['old']),
                    new_value=json.dumps(values['new']),
                    user_id=session.info.get('user_id'),
                    ip_address=session.info.get('ip_address'),
                    user_agent=session.info.get('user_agent'),
                    description=f"Modification {field_name}: {values['old']} → {values['new']}",
                    raw_changes=json.dumps(changes),
                )
                
                session.add(log)
        except Exception as e:
            print(f"⚠️ Audit log error in before_update: {e}")
            pass
    
    @staticmethod
    def before_delete(mapper, connection, target):
        """
        Callback avant DELETE - enregistrer la suppression
        """
        try:
            from sqlalchemy.orm import Session
            
            session = Session.registry.sessions.get(id(connection))
            if not session:
                return
            
            if not hasattr(session, 'info'):
                session.info = {}
            
            entity_type = AuditListeners.get_entity_name(mapper)
            entity_id = getattr(target, 'id', None)
            
            # Récupérer l'état actuel avant suppression
            changes = AuditListeners.get_model_changes(mapper, target)
            
            log = AuditLog(
                action='DELETE',
                entity_type=entity_type,
                entity_id=entity_id,
                field_name=None,
                old_value=json.dumps(changes),
                new_value=None,
                user_id=session.info.get('user_id'),
                ip_address=session.info.get('ip_address'),
                user_agent=session.info.get('user_agent'),
                description=f"Suppression de {entity_type} #{entity_id}",
                raw_changes=json.dumps(changes),
            )
            
            session.add(log)
        except Exception as e:
            print(f"⚠️ Audit log error in before_delete: {e}")
            pass
    
    @staticmethod
    def register():
        """
        Enregistrer tous les event listeners
        À appeler une fois au démarrage de l'application
        """
        for model in AuditListeners.AUDITED_MODELS:
            # Enregistrer les callbacks
            event.listen(model, 'before_insert', AuditListeners.before_insert, propagate=True)
            event.listen(model, 'before_update', AuditListeners.before_update, propagate=True)
            event.listen(model, 'before_delete', AuditListeners.before_delete, propagate=True)
        
        print("✅ Audit event listeners enregistrés pour:", 
              [m.__name__ for m in AuditListeners.AUDITED_MODELS])

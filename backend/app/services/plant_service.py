"""
Service métier pour les plantes
Gestion CRUD + logique métier (référence generation, etc)
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional
from datetime import datetime
import re

from app.models.plant import Plant
from app.models.tags import Tag, TagCategory
from app.schemas.plant_schema import PlantCreate, PlantUpdate
from app.services.tag_service import get_auto_tags_for_plant


class PlantService:
    """Service pour gérer les plantes et leur logique métier"""
    
    # ===== RÉFÉRENCE GENERATION =====
    
    @staticmethod
    def generate_reference(db: Session, family: str) -> str:
        """
        Génère une référence unique au format FAMILY-NNN
        
        Règles:
        - Préfixe: 5 premières lettres de la famille (MAJUSCULES)
        - Numéro: compteur séquentiel (3 chiffres padded avec zéros)
        - Exemples: "ARACA-001", "ARACA-042", "PHALA-001"
        - Unicité: garantie par unique constraint en BD
        
        Args:
            db: Session SQLAlchemy
            family: Famille botanique (ex: "Araceae")
        
        Returns:
            str: Référence au format "{PREFIX}-{NUMBER}" ex: "ARACA-001"
        
        Raises:
            ValueError: Si family est vide
        """
        if not family or not family.strip():
            raise ValueError("La famille est requise pour générer une référence")
        
        # 1. Extraire les 5 premières lettres en MAJUSCULES
        prefix = family.strip()[:5].upper()
        
        # 2. Chercher toutes les références avec ce préfixe
        #    Pattern: "{PREFIX}-NNN"
        pattern = f"{prefix}-%"
        
        last_plant = db.query(Plant).filter(
            Plant.reference.ilike(pattern)
        ).order_by(desc(Plant.reference)).first()
        
        # 3. Extraire le numéro courant
        current_number = 0
        if last_plant and last_plant.reference:
            try:
                # Format: "ARACA-001" → extraire 001
                parts = last_plant.reference.split('-')
                if len(parts) == 2:
                    current_number = int(parts[1])
            except (ValueError, IndexError):
                # Si format invalide, commencer à 0
                current_number = 0
        
        # 4. Incrémenter et formater
        next_number = current_number + 1
        reference = f"{prefix}-{str(next_number).zfill(3)}"
        
        return reference
    
    # ===== CRUD OPERATIONS =====
    
    @staticmethod
    def create(db: Session, plant_data: PlantCreate) -> Plant:
        """
        Crée une nouvelle plante
        
        Logique:
        - Auto-génère scientific_name si genus + species fournis
        - Auto-génère reference si famille fournie
        - Auto-génère et ajoute les tags pré-remplis (location, health_status, light)
        - Ajoute les tags manuels fournis
        
        Args:
            db: Session SQLAlchemy
            plant_data: Données PlantCreate
        
        Returns:
            Plant: Plante créée avec ID
        """
        try:
            # Convertir Pydantic v2 model en dict
            plant_dict = plant_data.model_dump(exclude_unset=True)
            
            # Extraire tag_ids avant de passer au Plant
            tag_ids = plant_dict.pop('tag_ids', None)
            
            # 1. Générer scientific_name si absent mais genus + species présents
            if (not plant_dict.get('scientific_name') and 
                plant_dict.get('genus') and plant_dict.get('species')):
                genus = plant_dict['genus'].strip().capitalize()
                species = plant_dict['species'].strip().lower()
                plant_dict['scientific_name'] = f"{genus} {species}"
            
            # 2. Générer reference si absent mais family présente
            if (not plant_dict.get('reference') and plant_dict.get('family')):
                try:
                    plant_dict['reference'] = PlantService.generate_reference(
                        db, 
                        plant_dict['family']
                    )
                except ValueError:
                    # Si génération échoue, laisser vide (sera geré par UI)
                    pass
            
            # 3. Créer la plante
            plant = Plant(**plant_dict)
            db.add(plant)
            db.flush()  # Flush pour obtenir l'ID
            
            # 4. Ajouter tags auto-générés
            auto_tags = get_auto_tags_for_plant(plant, db)
            for tag in auto_tags:
                if tag not in plant.tags:
                    plant.tags.append(tag)
            
            # 5. Ajouter tags manuels fournis
            if tag_ids:
                for tag_id in tag_ids:
                    tag = db.query(Tag).filter(Tag.id == tag_id).first()
                    if tag and tag not in plant.tags:
                        plant.tags.append(tag)
            
            db.commit()
            db.refresh(plant)
            return plant
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Erreur création plante: {str(e)}")
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        include_archived: bool = False,
        include_deleted: bool = False,
    ) -> List[Plant]:
        """
        Récupère toutes les plantes avec filtres
        
        Args:
            db: Session SQLAlchemy
            skip: Nombre de plantes à sauter (pagination)
            limit: Nombre max de plantes à retourner
            include_archived: Inclure les plantes archivées
            include_deleted: Inclure les plantes supprimées (soft delete)
        
        Returns:
            List[Plant]: Liste des plantes
        """
        query = db.query(Plant)
        
        # Filtrer soft deleted
        if not include_deleted:
            query = query.filter(Plant.deleted_at.is_(None))
        
        # Filtrer archived
        if not include_archived:
            query = query.filter(Plant.is_archived == False)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    @staticmethod
    def get_by_id(db: Session, plant_id: int, include_deleted: bool = False) -> Optional[Plant]:
        """
        Récupère une plante par ID
        
        Args:
            db: Session SQLAlchemy
            plant_id: ID de la plante
            include_deleted: Inclure les plantes soft-deleted
        
        Returns:
            Optional[Plant]: Plante ou None
        """
        from sqlalchemy.orm import joinedload
        
        query = db.query(Plant).options(joinedload(Plant.tags)).filter(Plant.id == plant_id)
        
        if not include_deleted:
            query = query.filter(Plant.deleted_at.is_(None))
        
        return query.first()
    
    @staticmethod
    def update(db: Session, plant_id: int, plant_data: PlantUpdate) -> Optional[Plant]:
        """
        Met à jour une plante
        
        Immuabilité:
        - reference: ne peut pas être changée après création
        - created_at: ne peut pas être changée
        - archived_date: ne peut pas être changée manuellement
        - Tags auto: sont recalculés automatiquement basés sur location/health_status/light
        
        Args:
            db: Session SQLAlchemy
            plant_id: ID de la plante à mettre à jour
            plant_data: Données PlantUpdate
        
        Returns:
            Optional[Plant]: Plante mise à jour ou None
        """
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return None
        
        try:
            # Préparer les données (Pydantic v2)
            update_data = plant_data.model_dump(exclude_unset=True)
            
            # Extraire tag_ids avant de passer au Plant
            tag_ids = update_data.pop('tag_ids', None)
            
            # Empêcher modification de reference (immutable)
            if 'reference' in update_data:
                if plant.reference and update_data['reference'] != plant.reference:
                    raise ValueError("La référence ne peut pas être modifiée après création")
            
            # Empêcher modification de created_at (immutable)
            if 'created_at' in update_data:
                raise ValueError("La date de création ne peut pas être modifiée")
            
            # Empêcher modification directe de archived_date (immuable)
            if 'archived_date' in update_data:
                raise ValueError("Use archive/restore endpoints to manage archived_date")
            
            # Mettre à jour les champs autorisés
            for field, value in update_data.items():
                if hasattr(plant, field):
                    setattr(plant, field, value)
            
            # Mettre à jour updated_at
            plant.updated_at = datetime.utcnow()
            
            # Recalculer et synchroniser les tags auto
            auto_categories = ["Emplacement", "État de la plante", "Luminosité"]
            auto_tags_ids = db.query(Tag.id).filter(
                Tag.category.has(TagCategory.name.in_(auto_categories))
            ).all()
            auto_tags_ids = [t[0] for t in auto_tags_ids]
            
            # Supprimer les anciens tags auto
            current_auto_tags = [t for t in plant.tags if t.id in auto_tags_ids]
            for tag in current_auto_tags:
                plant.tags.remove(tag)
            
            # Ajouter les nouveaux tags auto
            new_auto_tags = get_auto_tags_for_plant(plant, db)
            for tag in new_auto_tags:
                if tag not in plant.tags:
                    plant.tags.append(tag)
            
            # Gérer les tags manuels fournis (remplacer les non-auto)
            if tag_ids is not None:
                # Supprimer tous les tags non-auto actuels
                non_auto_tags = [t for t in plant.tags if t.id not in auto_tags_ids]
                for tag in non_auto_tags:
                    plant.tags.remove(tag)
                
                # Ajouter les nouveaux tags manuels
                for tag_id in tag_ids:
                    tag = db.query(Tag).filter(Tag.id == tag_id).first()
                    if tag and tag not in plant.tags:
                        plant.tags.append(tag)
            
            db.commit()
            db.refresh(plant)
            return plant
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Erreur mise à jour plante: {str(e)}")
    
    @staticmethod
    def delete(db: Session, plant_id: int, soft: bool = True) -> bool:
        """
        Supprime une plante (soft delete par défaut)
        
        Args:
            db: Session SQLAlchemy
            plant_id: ID de la plante
            soft: Si True, soft delete (deleted_at). Si False, hard delete.
        
        Returns:
            bool: True si succès, False si plante non trouvée
        """
        plant = PlantService.get_by_id(db, plant_id, include_deleted=False)
        if not plant:
            return False
        
        try:
            if soft:
                # Soft delete: marquer deleted_at
                plant.deleted_at = datetime.utcnow()
                db.commit()
            else:
                # Hard delete: supprimer complètement
                db.delete(plant)
                db.commit()
            
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"Erreur suppression plante: {str(e)}")
    
    @staticmethod
    def archive(db: Session, plant_id: int, reason: str = None) -> Optional[Plant]:
        """
        Archive une plante
        
        Définit:
        - is_archived = True
        - archived_date = now()
        - archived_reason = reason (optionnel)
        
        Args:
            db: Session SQLAlchemy
            plant_id: ID de la plante
            reason: Raison de l'archivage (optionnelle)
        
        Returns:
            Optional[Plant]: Plante archivée ou None
        """
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return None
        
        try:
            plant.is_archived = True
            plant.archived_date = datetime.utcnow()
            if reason:
                plant.archived_reason = reason[:255]  # Limiter à 255 chars
            
            db.commit()
            db.refresh(plant)
            return plant
        except Exception as e:
            db.rollback()
            raise Exception(f"Erreur archivage plante: {str(e)}")
    
    @staticmethod
    def restore(db: Session, plant_id: int) -> Optional[Plant]:
        """
        Restaure une plante archivée
        
        Définit:
        - is_archived = False
        - archived_date = NULL
        - archived_reason = NULL
        
        Args:
            db: Session SQLAlchemy
            plant_id: ID de la plante
        
        Returns:
            Optional[Plant]: Plante restaurée ou None
        """
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return None
        
        if not plant.is_archived:
            return plant  # Déjà active
        
        try:
            plant.is_archived = False
            plant.archived_date = None
            plant.archived_reason = None
            
            db.commit()
            db.refresh(plant)
            return plant
        except Exception as e:
            db.rollback()
            raise Exception(f"Erreur restauration plante: {str(e)}")
    
    @staticmethod
    def get_plants_to_water(db: Session, days_ago: int = 0) -> list:
        """Retourne TOUTES les plantes avec info arrosage + warning si fréquence saisonnière manque"""
        from app.models.lookup import Season, PlantSeasonalWatering, WateringFrequency
        from app.models.histories import WateringHistory
        from app.utils.season_helper import get_current_season_id
        from datetime import datetime, timedelta
        
        try:
            today = datetime.utcnow().date()
            seasons = db.query(Season).all()
            current_season_id = get_current_season_id(today.month, seasons)
            
            plants = db.query(Plant).filter(Plant.deleted_at == None).all()
            plants_to_water = []
            
            for plant in plants:
                # Historique d'arrosage
                last_watering = db.query(WateringHistory).filter(
                    WateringHistory.plant_id == plant.id
                ).order_by(WateringHistory.date.desc()).first()
                
                days_since = (today - last_watering.date).days if last_watering else 999999
                
                # Fréquence saisonnière
                seasonal = db.query(PlantSeasonalWatering).filter(
                    PlantSeasonalWatering.plant_id == plant.id,
                    PlantSeasonalWatering.season_id == current_season_id
                ).first()
                
                warning = None
                needs_watering = False
                
                if not seasonal or not seasonal.watering_frequency_id:
                    # ⚠️ Pas de fréquence définie pour cette saison
                    warning = "Fréquence d'arrosage non définie pour cette saison"
                    needs_watering = days_since >= 7  # Heuristique: 7+ jours
                else:
                    frequency = db.query(WateringFrequency).filter(
                        WateringFrequency.id == seasonal.watering_frequency_id
                    ).first()
                    
                    if not frequency or not frequency.days_interval:
                        warning = "Fréquence invalide en base"
                        needs_watering = days_since >= 7
                    else:
                        # Calcul basé sur fréquence
                        if last_watering:
                            next_date = last_watering.date + timedelta(days=frequency.days_interval)
                        else:
                            next_date = today
                        
                        needs_watering = next_date <= today + timedelta(days=days_ago)
                
                plants_to_water.append({
                    'id': plant.id,
                    'name': plant.name,
                    'scientific_name': plant.scientific_name,
                    'days_since_watering': days_since,
                    'last_watering': last_watering.date.isoformat() if last_watering else None,
                    'needs_watering': needs_watering,
                    'warning': warning,
                })
            
            # Trier: besoin d'eau d'abord, puis par urgence
            plants_to_water.sort(key=lambda p: (-p['needs_watering'], -p['days_since_watering']))
            return plants_to_water
        except Exception as e:
            print(f"Error in get_plants_to_water: {e}")
            return []
    
    @staticmethod
    def get_plants_to_fertilize(db: Session, days_ago: int = 0) -> list:
        """Retourne TOUTES les plantes avec info fertilisation + warning si fréquence saisonnière manque"""
        from app.models.lookup import Season, PlantSeasonalFertilizing, FertilizerFrequency
        from app.models.histories import FertilizingHistory
        from app.utils.season_helper import get_current_season_id
        from datetime import datetime, timedelta
        
        try:
            today = datetime.utcnow().date()
            seasons = db.query(Season).all()
            current_season_id = get_current_season_id(today.month, seasons)
            
            plants = db.query(Plant).filter(Plant.deleted_at == None).all()
            plants_to_fertilize = []
            
            for plant in plants:
                # Historique de fertilisation
                last_fertilizing = db.query(FertilizingHistory).filter(
                    FertilizingHistory.plant_id == plant.id
                ).order_by(FertilizingHistory.date.desc()).first()
                
                days_since = (today - last_fertilizing.date).days if last_fertilizing else 999999
                
                # Fréquence saisonnière
                seasonal = db.query(PlantSeasonalFertilizing).filter(
                    PlantSeasonalFertilizing.plant_id == plant.id,
                    PlantSeasonalFertilizing.season_id == current_season_id
                ).first()
                
                warning = None
                needs_fertilizing = False
                
                if not seasonal or not seasonal.fertilizer_frequency_id:
                    # ⚠️ Pas de fréquence définie pour cette saison
                    warning = "Fréquence de fertilisation non définie pour cette saison"
                    needs_fertilizing = days_since >= 30  # Heuristique: 30+ jours
                else:
                    frequency = db.query(FertilizerFrequency).filter(
                        FertilizerFrequency.id == seasonal.fertilizer_frequency_id
                    ).first()
                    
                    if not frequency or not frequency.weeks_interval:
                        warning = "Fréquence invalide en base"
                        needs_fertilizing = days_since >= 30
                    else:
                        # Calcul basé sur fréquence (semaines → jours)
                        frequency_days = frequency.weeks_interval * 7
                        
                        if last_fertilizing:
                            next_date = last_fertilizing.date + timedelta(days=frequency_days)
                        else:
                            next_date = today
                        
                        needs_fertilizing = next_date <= today + timedelta(days=days_ago)
                
                plants_to_fertilize.append({
                    'id': plant.id,
                    'name': plant.name,
                    'scientific_name': plant.scientific_name,
                    'days_since_fertilizing': days_since,
                    'last_fertilizing': last_fertilizing.date.isoformat() if last_fertilizing else None,
                    'needs_fertilizing': needs_fertilizing,
                    'warning': warning,
                })
            
            # Trier: besoin d'engrais d'abord, puis par urgence
            plants_to_fertilize.sort(key=lambda p: (-p['needs_fertilizing'], -p['days_since_fertilizing']))
            return plants_to_fertilize
        except Exception as e:
            print(f"Error in get_plants_to_fertilize: {e}")
            return []

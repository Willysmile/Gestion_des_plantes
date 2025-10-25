"""
Service métier pour les plantes
Contient la logique CRUD et les fonctions utilitaires
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from app.models.plant import Plant
from app.schemas.plant_schema import PlantCreate, PlantUpdate


class PlantService:
    """Service pour gérer les plantes"""
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        include_archived: bool = False,
        include_deleted: bool = False,
    ) -> List[Plant]:
        """Récupère toutes les plantes avec pagination et filtres"""
        query = db.query(Plant)
        
        # Exclure les archives si demandé
        if not include_archived:
            query = query.filter(Plant.is_archived == False)
        
        # Exclure les supprimées si demandé
        if not include_deleted:
            query = query.filter(Plant.deleted_at == None)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, plant_id: int) -> Optional[Plant]:
        """Récupère une plante par ID (excluant les supprimées)"""
        return db.query(Plant).filter(
            and_(
                Plant.id == plant_id,
                Plant.deleted_at == None
            )
        ).first()
    
    @staticmethod
    def search(
        db: Session,
        query_str: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Plant]:
        """Recherche les plantes par nom ou nom scientifique"""
        search_term = f"%{query_str}%"
        
        return db.query(Plant).filter(
            and_(
                Plant.deleted_at == None,
                Plant.is_archived == False,
                or_(
                    Plant.name.ilike(search_term),
                    Plant.scientific_name.ilike(search_term),
                    Plant.reference.ilike(search_term),
                )
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, data: PlantCreate) -> Plant:
        """Crée une nouvelle plante"""
        plant = Plant(**data.model_dump())
        db.add(plant)
        db.commit()
        db.refresh(plant)
        return plant
    
    @staticmethod
    def update(db: Session, plant_id: int, data: PlantUpdate) -> Optional[Plant]:
        """Met à jour une plante"""
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return None
        
        # Mettre à jour uniquement les champs fournis (non-None)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(plant, key, value)
        
        plant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(plant)
        return plant
    
    @staticmethod
    def delete(db: Session, plant_id: int) -> bool:
        """Soft delete : marque une plante comme supprimée"""
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return False
        
        plant.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def archive(db: Session, plant_id: int) -> Optional[Plant]:
        """Archive une plante"""
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return None
        
        plant.is_archived = True
        db.commit()
        db.refresh(plant)
        return plant
    
    @staticmethod
    def restore(db: Session, plant_id: int) -> Optional[Plant]:
        """Restaure une plante archivée"""
        plant = PlantService.get_by_id(db, plant_id)
        if not plant:
            return None
        
        plant.is_archived = False
        db.commit()
        db.refresh(plant)
        return plant
    
    @staticmethod
    def get_archived(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Plant]:
        """Récupère les plantes archivées"""
        return db.query(Plant).filter(
            and_(
                Plant.is_archived == True,
                Plant.deleted_at == None
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_favorites(db: Session) -> List[Plant]:
        """Récupère les plantes favorites"""
        return db.query(Plant).filter(
            and_(
                Plant.is_favorite == True,
                Plant.deleted_at == None,
                Plant.is_archived == False
            )
        ).all()
    
    @staticmethod
    def get_by_location(db: Session, location_id: int) -> List[Plant]:
        """Récupère les plantes par emplacement"""
        return db.query(Plant).filter(
            and_(
                Plant.location_id == location_id,
                Plant.deleted_at == None,
                Plant.is_archived == False
            )
        ).all()
    
    @staticmethod
    def get_count(db: Session, include_archived: bool = False) -> int:
        """Compte le nombre de plantes"""
        query = db.query(Plant).filter(Plant.deleted_at == None)
        
        if not include_archived:
            query = query.filter(Plant.is_archived == False)
        
        return query.count()

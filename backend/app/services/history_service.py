"""
Service pour gérer les historiques
Contient CRUD pour tous les types d'historique
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.histories import (
    WateringHistory,
    FertilizingHistory,
    RepottingHistory,
    DiseaseHistory,
    PlantHistory,
)
from app.schemas.history_schema import (
    WateringHistoryCreate, WateringHistoryUpdate,
    FertilizingHistoryCreate, FertilizingHistoryUpdate,
    RepottingHistoryCreate, RepottingHistoryUpdate,
    DiseaseHistoryCreate, DiseaseHistoryUpdate,
    PlantHistoryCreate, PlantHistoryUpdate,
)


class HistoryService:
    """Service pour gérer tous les historiques"""
    
    # ===== WATERING HISTORY =====
    
    @staticmethod
    def create_watering(db: Session, plant_id: int, data: WateringHistoryCreate) -> WateringHistory:
        """Créer une entrée d'arrosage"""
        history = WateringHistory(
            plant_id=plant_id,
            **data.model_dump()
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def get_watering(db: Session, plant_id: int, history_id: int) -> Optional[WateringHistory]:
        """Récupérer une entrée d'arrosage"""
        return db.query(WateringHistory).filter(
            WateringHistory.id == history_id,
            WateringHistory.plant_id == plant_id,
            WateringHistory.deleted_at == None
        ).first()
    
    @staticmethod
    def get_all_watering(db: Session, plant_id: int) -> List[WateringHistory]:
        """Lister tous les arrosages d'une plante"""
        return db.query(WateringHistory).filter(
            WateringHistory.plant_id == plant_id,
            WateringHistory.deleted_at == None
        ).order_by(WateringHistory.date.desc()).all()
    
    @staticmethod
    def update_watering(db: Session, plant_id: int, history_id: int, data: WateringHistoryUpdate) -> Optional[WateringHistory]:
        """Mettre à jour une entrée d'arrosage"""
        history = HistoryService.get_watering(db, plant_id, history_id)
        if not history:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(history, key, value)
        
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def delete_watering(db: Session, plant_id: int, history_id: int) -> bool:
        """Soft delete une entrée d'arrosage"""
        history = HistoryService.get_watering(db, plant_id, history_id)
        if not history:
            return False
        
        history.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    # ===== FERTILIZING HISTORY =====
    
    @staticmethod
    def create_fertilizing(db: Session, plant_id: int, data: FertilizingHistoryCreate) -> FertilizingHistory:
        """Créer une entrée de fertilisation"""
        history = FertilizingHistory(
            plant_id=plant_id,
            **data.model_dump()
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def get_fertilizing(db: Session, plant_id: int, history_id: int) -> Optional[FertilizingHistory]:
        """Récupérer une entrée de fertilisation"""
        return db.query(FertilizingHistory).filter(
            FertilizingHistory.id == history_id,
            FertilizingHistory.plant_id == plant_id,
            FertilizingHistory.deleted_at == None
        ).first()
    
    @staticmethod
    def get_all_fertilizing(db: Session, plant_id: int) -> List[FertilizingHistory]:
        """Lister toutes les fertilisations"""
        return db.query(FertilizingHistory).filter(
            FertilizingHistory.plant_id == plant_id,
            FertilizingHistory.deleted_at == None
        ).order_by(FertilizingHistory.date.desc()).all()
    
    @staticmethod
    def update_fertilizing(db: Session, plant_id: int, history_id: int, data: FertilizingHistoryUpdate) -> Optional[FertilizingHistory]:
        """Mettre à jour une fertilisation"""
        history = HistoryService.get_fertilizing(db, plant_id, history_id)
        if not history:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(history, key, value)
        
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def delete_fertilizing(db: Session, plant_id: int, history_id: int) -> bool:
        """Soft delete une fertilisation"""
        history = HistoryService.get_fertilizing(db, plant_id, history_id)
        if not history:
            return False
        
        history.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    # ===== REPOTTING HISTORY =====
    
    @staticmethod
    def create_repotting(db: Session, plant_id: int, data: RepottingHistoryCreate) -> RepottingHistory:
        """Créer une entrée de rempotage"""
        history = RepottingHistory(
            plant_id=plant_id,
            **data.model_dump()
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def get_repotting(db: Session, plant_id: int, history_id: int) -> Optional[RepottingHistory]:
        """Récupérer un rempotage"""
        return db.query(RepottingHistory).filter(
            RepottingHistory.id == history_id,
            RepottingHistory.plant_id == plant_id,
            RepottingHistory.deleted_at == None
        ).first()
    
    @staticmethod
    def get_all_repotting(db: Session, plant_id: int) -> List[RepottingHistory]:
        """Lister tous les rempotages"""
        return db.query(RepottingHistory).filter(
            RepottingHistory.plant_id == plant_id,
            RepottingHistory.deleted_at == None
        ).order_by(RepottingHistory.date.desc()).all()
    
    @staticmethod
    def update_repotting(db: Session, plant_id: int, history_id: int, data: RepottingHistoryUpdate) -> Optional[RepottingHistory]:
        """Mettre à jour un rempotage"""
        history = HistoryService.get_repotting(db, plant_id, history_id)
        if not history:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(history, key, value)
        
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def delete_repotting(db: Session, plant_id: int, history_id: int) -> bool:
        """Soft delete un rempotage"""
        history = HistoryService.get_repotting(db, plant_id, history_id)
        if not history:
            return False
        
        history.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    # ===== DISEASE HISTORY =====
    
    @staticmethod
    def create_disease(db: Session, plant_id: int, data: DiseaseHistoryCreate) -> DiseaseHistory:
        """Créer une entrée de maladie"""
        history = DiseaseHistory(
            plant_id=plant_id,
            **data.model_dump()
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def get_disease(db: Session, plant_id: int, history_id: int) -> Optional[DiseaseHistory]:
        """Récupérer une maladie"""
        return db.query(DiseaseHistory).filter(
            DiseaseHistory.id == history_id,
            DiseaseHistory.plant_id == plant_id,
            DiseaseHistory.deleted_at == None
        ).first()
    
    @staticmethod
    def get_all_disease(db: Session, plant_id: int) -> List[DiseaseHistory]:
        """Lister toutes les maladies"""
        return db.query(DiseaseHistory).filter(
            DiseaseHistory.plant_id == plant_id,
            DiseaseHistory.deleted_at == None
        ).order_by(DiseaseHistory.date.desc(), DiseaseHistory.id.desc()).all()
    
    @staticmethod
    def update_disease(db: Session, plant_id: int, history_id: int, data: DiseaseHistoryUpdate) -> Optional[DiseaseHistory]:
        """Mettre à jour une maladie"""
        history = HistoryService.get_disease(db, plant_id, history_id)
        if not history:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(history, key, value)
        
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def delete_disease(db: Session, plant_id: int, history_id: int) -> bool:
        """Soft delete une maladie"""
        history = HistoryService.get_disease(db, plant_id, history_id)
        if not history:
            return False
        
        history.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    # ===== PLANT HISTORY (NOTES) =====
    
    @staticmethod
    def create_plant_note(db: Session, plant_id: int, data: PlantHistoryCreate) -> PlantHistory:
        """Créer une note"""
        history = PlantHistory(
            plant_id=plant_id,
            **data.model_dump()
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def get_plant_note(db: Session, plant_id: int, history_id: int) -> Optional[PlantHistory]:
        """Récupérer une note"""
        return db.query(PlantHistory).filter(
            PlantHistory.id == history_id,
            PlantHistory.plant_id == plant_id,
            PlantHistory.deleted_at == None
        ).first()
    
    @staticmethod
    def get_all_plant_notes(db: Session, plant_id: int) -> List[PlantHistory]:
        """Lister toutes les notes"""
        return db.query(PlantHistory).filter(
            PlantHistory.plant_id == plant_id,
            PlantHistory.deleted_at == None
        ).order_by(PlantHistory.date.desc()).all()
    
    @staticmethod
    def update_plant_note(db: Session, plant_id: int, history_id: int, data: PlantHistoryUpdate) -> Optional[PlantHistory]:
        """Mettre à jour une note"""
        history = HistoryService.get_plant_note(db, plant_id, history_id)
        if not history:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(history, key, value)
        
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def delete_plant_note(db: Session, plant_id: int, history_id: int) -> bool:
        """Soft delete une note"""
        history = HistoryService.get_plant_note(db, plant_id, history_id)
        if not history:
            return False
        
        history.deleted_at = datetime.utcnow()
        db.commit()
        return True

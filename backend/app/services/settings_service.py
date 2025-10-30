"""
Service métier pour les paramètres et lookups
Gestion CRUD pour: Locations, PurchasePlaces, WateringFrequencies, 
LightRequirements, FertilizerTypes, Tags
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime

from app.models.lookup import (
    Location, PurchasePlace, WateringFrequency, 
    LightRequirement, FertilizerType, DiseaseType, TreatmentType, PlantHealthStatus
)
from app.models.tags import Tag, TagCategory


class SettingsService:
    """Service pour gérer les paramètres et lookups"""
    
    # ===== LOCATIONS =====
    
    @staticmethod
    def create_location(db: Session, name: str) -> Location:
        """Crée une nouvelle localisation"""
        location = Location(name=name)
        db.add(location)
        db.commit()
        db.refresh(location)
        return location
    
    @staticmethod
    def get_locations(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Location]:
        """Récupère toutes les localisations"""
        return db.query(Location).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_location(db: Session, location_id: int) -> Optional[Location]:
        """Récupère une localisation par ID"""
        return db.query(Location).filter(Location.id == location_id).first()
    
    @staticmethod
    def update_location(db: Session, location_id: int, name: str) -> Optional[Location]:
        """Met à jour une localisation"""
        location = SettingsService.get_location(db, location_id)
        if not location:
            return None
        location.name = name
        db.commit()
        db.refresh(location)
        return location
    
    @staticmethod
    def delete_location(db: Session, location_id: int) -> bool:
        """Supprime une localisation"""
        location = SettingsService.get_location(db, location_id)
        if not location:
            return False
        db.delete(location)
        db.commit()
        return True
    
    # ===== PURCHASE PLACES =====
    
    @staticmethod
    def create_purchase_place(db: Session, name: str) -> PurchasePlace:
        """Crée un nouveau lieu d'achat"""
        place = PurchasePlace(name=name)
        db.add(place)
        db.commit()
        db.refresh(place)
        return place
    
    @staticmethod
    def get_purchase_places(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[PurchasePlace]:
        """Récupère tous les lieux d'achat"""
        return db.query(PurchasePlace).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_purchase_place(db: Session, place_id: int) -> Optional[PurchasePlace]:
        """Récupère un lieu d'achat par ID"""
        return db.query(PurchasePlace).filter(PurchasePlace.id == place_id).first()
    
    @staticmethod
    def update_purchase_place(db: Session, place_id: int, name: str) -> Optional[PurchasePlace]:
        """Met à jour un lieu d'achat"""
        place = SettingsService.get_purchase_place(db, place_id)
        if not place:
            return None
        place.name = name
        db.commit()
        db.refresh(place)
        return place
    
    @staticmethod
    def delete_purchase_place(db: Session, place_id: int) -> bool:
        """Supprime un lieu d'achat"""
        place = SettingsService.get_purchase_place(db, place_id)
        if not place:
            return False
        db.delete(place)
        db.commit()
        return True
    
    # ===== WATERING FREQUENCIES =====
    
    @staticmethod
    def create_watering_frequency(
        db: Session, 
        name: str, 
        days: int
    ) -> WateringFrequency:
        """Crée une nouvelle fréquence d'arrosage"""
        frequency = WateringFrequency(name=name, days_interval=days)
        db.add(frequency)
        db.commit()
        db.refresh(frequency)
        return frequency
    
    @staticmethod
    def get_watering_frequencies(db: Session) -> List[WateringFrequency]:
        """Récupère toutes les fréquences d'arrosage"""
        return db.query(WateringFrequency).all()
    
    @staticmethod
    def get_watering_frequency(
        db: Session, 
        frequency_id: int
    ) -> Optional[WateringFrequency]:
        """Récupère une fréquence d'arrosage par ID"""
        return db.query(WateringFrequency).filter(
            WateringFrequency.id == frequency_id
        ).first()
    
    @staticmethod
    def update_watering_frequency(
        db: Session, 
        frequency_id: int, 
        name: str, 
        days: int
    ) -> Optional[WateringFrequency]:
        """Met à jour une fréquence d'arrosage"""
        frequency = SettingsService.get_watering_frequency(db, frequency_id)
        if not frequency:
            return None
        frequency.name = name
        frequency.days_interval = days
        db.commit()
        db.refresh(frequency)
        return frequency
    
    @staticmethod
    def delete_watering_frequency(db: Session, frequency_id: int) -> bool:
        """Supprime une fréquence d'arrosage"""
        frequency = SettingsService.get_watering_frequency(db, frequency_id)
        if not frequency:
            return False
        db.delete(frequency)
        db.commit()
        return True
    
    # ===== LIGHT REQUIREMENTS =====
    
    @staticmethod
    def create_light_requirement(db: Session, name: str) -> LightRequirement:
        """Crée une nouvelle exigence lumineuse"""
        requirement = LightRequirement(name=name)
        db.add(requirement)
        db.commit()
        db.refresh(requirement)
        return requirement
    
    @staticmethod
    def get_light_requirements(db: Session) -> List[LightRequirement]:
        """Récupère toutes les exigences lumineuses"""
        return db.query(LightRequirement).all()
    
    @staticmethod
    def get_light_requirement(
        db: Session, 
        requirement_id: int
    ) -> Optional[LightRequirement]:
        """Récupère une exigence lumineuse par ID"""
        return db.query(LightRequirement).filter(
            LightRequirement.id == requirement_id
        ).first()
    
    @staticmethod
    def update_light_requirement(
        db: Session, 
        requirement_id: int, 
        name: str
    ) -> Optional[LightRequirement]:
        """Met à jour une exigence lumineuse"""
        requirement = SettingsService.get_light_requirement(db, requirement_id)
        if not requirement:
            return None
        requirement.name = name
        db.commit()
        db.refresh(requirement)
        return requirement
    
    @staticmethod
    def delete_light_requirement(db: Session, requirement_id: int) -> bool:
        """Supprime une exigence lumineuse"""
        requirement = SettingsService.get_light_requirement(db, requirement_id)
        if not requirement:
            return False
        db.delete(requirement)
        db.commit()
        return True
    
    # ===== FERTILIZER TYPES =====
    
    @staticmethod
    def create_fertilizer_type(db: Session, name: str, unit: str = "ml", description: str = None) -> FertilizerType:
        """Crée un nouveau type d'engrais"""
        fert_type = FertilizerType(name=name, unit=unit, description=description)
        db.add(fert_type)
        db.commit()
        db.refresh(fert_type)
        return fert_type
    
    @staticmethod
    def get_fertilizer_types(db: Session) -> List[FertilizerType]:
        """Récupère tous les types d'engrais"""
        return db.query(FertilizerType).all()
    
    @staticmethod
    def get_fertilizer_type(
        db: Session, 
        fert_type_id: int
    ) -> Optional[FertilizerType]:
        """Récupère un type d'engrais par ID"""
        return db.query(FertilizerType).filter(
            FertilizerType.id == fert_type_id
        ).first()
    
    @staticmethod
    def update_fertilizer_type(
        db: Session, 
        fert_type_id: int, 
        name: str,
        unit: str = "ml",
        description: str = None
    ) -> Optional[FertilizerType]:
        """Met à jour un type d'engrais"""
        fert_type = SettingsService.get_fertilizer_type(db, fert_type_id)
        if not fert_type:
            return None
        fert_type.name = name
        fert_type.unit = unit
        fert_type.description = description
        db.commit()
        db.refresh(fert_type)
        return fert_type
    
    @staticmethod
    def delete_fertilizer_type(db: Session, fert_type_id: int) -> bool:
        """Supprime un type d'engrais"""
        fert_type = SettingsService.get_fertilizer_type(db, fert_type_id)
        if not fert_type:
            return False
        db.delete(fert_type)
        db.commit()
        return True
    
    # ===== TAG CATEGORIES =====
    
    @staticmethod
    def create_tag_category(db: Session, name: str) -> TagCategory:
        """Crée une nouvelle catégorie de tags"""
        category = TagCategory(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def get_tag_categories(db: Session) -> List[TagCategory]:
        """Récupère toutes les catégories de tags"""
        return db.query(TagCategory).all()
    
    @staticmethod
    def get_tag_category(
        db: Session, 
        category_id: int
    ) -> Optional[TagCategory]:
        """Récupère une catégorie de tags par ID"""
        return db.query(TagCategory).filter(TagCategory.id == category_id).first()
    
    @staticmethod
    def update_tag_category(
        db: Session, 
        category_id: int, 
        name: str
    ) -> Optional[TagCategory]:
        """Met à jour une catégorie de tags"""
        category = SettingsService.get_tag_category(db, category_id)
        if not category:
            return None
        category.name = name
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def delete_tag_category(db: Session, category_id: int) -> bool:
        """Supprime une catégorie de tags"""
        category = SettingsService.get_tag_category(db, category_id)
        if not category:
            return False
        db.delete(category)
        db.commit()
        return True
    
    # ===== TAGS =====
    
    @staticmethod
    def create_tag(
        db: Session, 
        category_id: int, 
        name: str
    ) -> Optional[Tag]:
        """Crée un nouveau tag"""
        # Vérifier que la catégorie existe
        category = SettingsService.get_tag_category(db, category_id)
        if not category:
            return None
        
        # Tag model uses 'tag_category_id' as the FK column name
        tag = Tag(tag_category_id=category_id, name=name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    
    @staticmethod
    def get_tags(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category_id: Optional[int] = None
    ) -> List[Tag]:
        """Récupère tous les tags, optionnellement filtrés par catégorie"""
        query = db.query(Tag)
        if category_id:
            # Tag model uses 'tag_category_id' as the FK column
            query = query.filter(Tag.tag_category_id == category_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
        """Récupère un tag par ID"""
        return db.query(Tag).filter(Tag.id == tag_id).first()
    
    @staticmethod
    def update_tag(
        db: Session, 
        tag_id: int, 
        name: str
    ) -> Optional[Tag]:
        """Met à jour un tag"""
        tag = SettingsService.get_tag(db, tag_id)
        if not tag:
            return None
        tag.name = name
        db.commit()
        db.refresh(tag)
        return tag
    
    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> bool:
        """Supprime un tag"""
        tag = SettingsService.get_tag(db, tag_id)
        if not tag:
            return False
        db.delete(tag)
        db.commit()
        return True

    # ===== DISEASE TYPES =====

    @staticmethod
    def get_disease_types(db: Session) -> List[DiseaseType]:
        """Récupère tous les types de maladies"""
        return db.query(DiseaseType).all()

    @staticmethod
    def get_disease_type(db: Session, disease_type_id: int) -> Optional[DiseaseType]:
        """Récupère un type de maladie par ID"""
        return db.query(DiseaseType).filter(DiseaseType.id == disease_type_id).first()

    # ===== TREATMENT TYPES =====

    @staticmethod
    def get_treatment_types(db: Session) -> List[TreatmentType]:
        """Récupère tous les types de traitement"""
        return db.query(TreatmentType).all()

    @staticmethod
    def get_treatment_type(db: Session, treatment_type_id: int) -> Optional[TreatmentType]:
        """Récupère un type de traitement par ID"""
        return db.query(TreatmentType).filter(TreatmentType.id == treatment_type_id).first()

    # ===== PLANT HEALTH STATUSES =====

    @staticmethod
    def get_plant_health_statuses(db: Session) -> List[PlantHealthStatus]:
        """Récupère tous les états de santé des plantes"""
        return db.query(PlantHealthStatus).all()

    @staticmethod
    def get_plant_health_status(db: Session, status_id: int) -> Optional[PlantHealthStatus]:
        """Récupère un état de santé par ID"""
        return db.query(PlantHealthStatus).filter(PlantHealthStatus.id == status_id).first()

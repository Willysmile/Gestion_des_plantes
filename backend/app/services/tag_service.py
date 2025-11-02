"""
Service pour gérer les tags automatiques des plantes
Auto-génère les tags pré-remplis basés sur les données existantes
"""

from sqlalchemy.orm import Session
from app.models.tags import Tag
from app.models.plant import Plant
from app.models.lookup import Location, PlantHealthStatus, LightRequirement


def get_auto_tags_for_plant(plant: Plant, db: Session) -> list:
    """
    Récupère les tags auto-générés pour une plante basés sur :
    - Location (location_id + is_indoor/is_outdoor)
    - Health Status (health_status)
    - Light Requirement (light_requirement_id)
    
    Retourne une liste de Tag objects
    """
    auto_tags = []
    
    # 1. Tags d'emplacement
    if plant.location_id:
        location = db.query(Location).filter(Location.id == plant.location_id).first()
        if location:
            # Chercher ou créer un tag pour cet emplacement
            tag = db.query(Tag).filter(
                Tag.name == location.name,
                Tag.category.has(name="Emplacement")
            ).first()
            if tag:
                auto_tags.append(tag)
    
    # Ajouter tags indoor/outdoor
    if plant.is_indoor:
        tag = db.query(Tag).filter(
            Tag.name == "Intérieur",
            Tag.category.has(name="Emplacement")
        ).first()
        if tag:
            auto_tags.append(tag)
    
    if plant.is_outdoor:
        tag = db.query(Tag).filter(
            Tag.name == "Extérieur",
            Tag.category.has(name="Emplacement")
        ).first()
        if tag:
            auto_tags.append(tag)
    
    # 2. Tags d'état de la plante
    if plant.health_status:
        tag = db.query(Tag).filter(
            Tag.name == plant.health_status,
            Tag.category.has(name="État de la plante")
        ).first()
        if tag:
            auto_tags.append(tag)
    
    # 3. Tags de luminosité
    if plant.light_requirement_id:
        light_req = db.query(LightRequirement).filter(
            LightRequirement.id == plant.light_requirement_id
        ).first()
        if light_req:
            # Mapper le light_requirement au bon tag de luminosité
            light_name = light_req.name  # ex: "Plein soleil", "Ombre", etc.
            tag = db.query(Tag).filter(
                Tag.name == light_name,
                Tag.category.has(name="Luminosité")
            ).first()
            if tag:
                auto_tags.append(tag)
    
    return auto_tags


def sync_auto_tags_for_plant(plant: Plant, db: Session):
    """
    Synchronise les tags auto-générés pour une plante.
    Supprime les anciens tags auto et en ajoute de nouveaux.
    """
    # Récupérer les catégories auto
    auto_categories = ["Emplacement", "État de la plante", "Luminosité"]
    
    # Supprimer les tags auto existants
    auto_tags_ids = db.query(Tag.id).filter(
        Tag.category.has(name__in=auto_categories)
    ).all()
    auto_tags_ids = [t[0] for t in auto_tags_ids]
    
    current_auto_tags = [t.id for t in plant.tags if t.id in auto_tags_ids]
    for tag_id in current_auto_tags:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag and tag in plant.tags:
            plant.tags.remove(tag)
    
    # Ajouter les nouveaux tags auto
    new_auto_tags = get_auto_tags_for_plant(plant, db)
    for tag in new_auto_tags:
        if tag not in plant.tags:
            plant.tags.append(tag)
    
    db.commit()

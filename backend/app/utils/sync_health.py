"""
Utilitaires pour synchroniser l'état de santé des plantes avec l'historique des maladies
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.plant import Plant
from app.models.histories import DiseaseHistory
from app.models.lookup import PlantHealthStatus


def sync_plant_health_status(db: Session, plant_id: int):
    """
    Synchronise l'état de santé d'une plante avec son dernier enregistrement de maladie
    
    Cherche le dernier historique de maladie et met à jour health_status en conséquence
    """
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        return None
    
    # Chercher le dernier historique de maladie
    latest_disease = db.query(DiseaseHistory).filter(
        DiseaseHistory.plant_id == plant_id
    ).order_by(desc(DiseaseHistory.date)).first()
    
    if not latest_disease or not latest_disease.health_status_id:
        # Pas d'historique, la plante est saine
        plant.health_status = 'healthy'
        db.commit()
        return plant
    
    # Récupérer le statut de santé et le mapper à la valeur anglaise
    health_status = db.query(PlantHealthStatus).filter(
        PlantHealthStatus.id == latest_disease.health_status_id
    ).first()
    
    if not health_status:
        plant.health_status = 'healthy'
        db.commit()
        return plant
    
    # Mapper les noms français aux valeurs anglaises
    status_map = {
        'Sain': 'healthy',
        'Malade': 'sick',
        'Rétablie': 'recovering',
        'Morte': 'dead',
        'Critique': 'critical',
        'En traitement': 'treating',
        'En convalescence': 'convalescent'
    }
    
    plant.health_status = status_map.get(health_status.name, 'healthy')
    db.commit()
    
    return plant


def sync_all_plants_health(db: Session):
    """
    Synchronise l'état de santé de TOUTES les plantes avec leur historique
    """
    plants = db.query(Plant).all()
    count = 0
    
    for plant in plants:
        sync_plant_health_status(db, plant.id)
        count += 1
    
    print(f"✅ Synchronisé l'état de santé de {count} plantes")
    return count

"""
Service de statistiques pour le dashboard
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.plant import Plant
from app.models.histories import WateringHistory, FertilizingHistory


class StatsService:
    """Service pour calculer les statistiques du dashboard"""

    @staticmethod
    def get_dashboard_stats(db: Session) -> dict:
        """
        Récupère les 7 KPI du dashboard:
        - total_plants: Nombre total de plantes
        - active_plants: Plantes non archivées
        - archived_plants: Plantes archivées
        - health_excellent: Plantes en excellente santé
        - health_good: Plantes en bonne santé
        - health_poor: Plantes en mauvaise santé
        - total_photos: Nombre total de photos
        """
        try:
            total_plants = db.query(Plant).count()
            active_plants = db.query(Plant).filter(Plant.is_archived == False).count()
            archived_plants = db.query(Plant).filter(Plant.is_archived == True).count()
            
            health_excellent = db.query(Plant).filter(
                Plant.is_archived == False,
                Plant.health_status == "excellent"
            ).count()
            health_good = db.query(Plant).filter(
                Plant.is_archived == False,
                Plant.health_status == "good"
            ).count()
            health_poor = db.query(Plant).filter(
                Plant.is_archived == False,
                Plant.health_status == "poor"
            ).count()
            
            # Compter les photos via la relation
            total_photos = db.query(func.count(Plant.id)).filter(
                Plant.photos != None
            ).scalar() or 0
            
            return {
                "total_plants": total_plants,
                "active_plants": active_plants,
                "archived_plants": archived_plants,
                "health_excellent": health_excellent,
                "health_good": health_good,
                "health_poor": health_poor,
                "total_photos": total_photos
            }
        except Exception as e:
            print(f"Erreur StatsService.get_dashboard_stats: {e}")
            return {
                "total_plants": 0,
                "active_plants": 0,
                "archived_plants": 0,
                "health_excellent": 0,
                "health_good": 0,
                "health_poor": 0,
                "total_photos": 0
            }

    @staticmethod
    def get_upcoming_waterings(db: Session, days: int = 7) -> list:
        """
        Récupère les plantes à arroser dans N jours
        Retourne: [{id, name, last_watered, days_since}]
        """
        try:
            today = datetime.now().date()
            cutoff_date = today - timedelta(days=days)
            
            # Plantes jamais arrosées ou arrosées avant la cutoff_date
            result = []
            
            # 1. Plantes jamais arrosées
            never_watered = db.query(Plant).filter(
                Plant.is_archived == False,
                ~Plant.waterings.any()
            ).all()
            
            for plant in never_watered:
                result.append({
                    "id": plant.id,
                    "name": plant.name,
                    "last_watered": None,
                    "days_since": None,
                    "reason": "Jamais arrosée"
                })
            
            # 2. Plantes arrosées avant cutoff_date
            recent_waterings = db.query(
                WateringHistory.plant_id,
                func.max(WateringHistory.watering_date).label("last_date")
            ).group_by(WateringHistory.plant_id).subquery()
            
            plants_to_water = db.query(Plant).join(
                recent_waterings,
                Plant.id == recent_waterings.c.plant_id
            ).filter(
                Plant.is_archived == False,
                recent_waterings.c.last_date <= cutoff_date
            ).all()
            
            for plant in plants_to_water:
                last_watering = db.query(
                    func.max(WateringHistory.watering_date)
                ).filter(WateringHistory.plant_id == plant.id).scalar()
                
                days_since = (today - last_watering.date()).days if last_watering else None
                
                result.append({
                    "id": plant.id,
                    "name": plant.name,
                    "last_watered": last_watering.isoformat() if last_watering else None,
                    "days_since": days_since,
                    "reason": f"Arrosée il y a {days_since} jours" if days_since else None
                })
            
            return sorted(result, key=lambda x: (x["days_since"] is None, x.get("days_since", 0)))
        except Exception as e:
            print(f"Erreur StatsService.get_upcoming_waterings: {e}")
            return []

    @staticmethod
    def get_upcoming_fertilizing(db: Session, days: int = 7) -> list:
        """
        Récupère les plantes à fertiliser dans N jours
        Retourne: [{id, name, last_fertilized, days_since}]
        """
        try:
            today = datetime.now().date()
            cutoff_date = today - timedelta(days=days)
            
            result = []
            
            # 1. Plantes jamais fertilisées
            never_fertilized = db.query(Plant).filter(
                Plant.is_archived == False,
                ~Plant.fertilizings.any()
            ).all()
            
            for plant in never_fertilized:
                result.append({
                    "id": plant.id,
                    "name": plant.name,
                    "last_fertilized": None,
                    "days_since": None,
                    "reason": "Jamais fertilisée"
                })
            
            # 2. Plantes fertilisées avant cutoff_date
            recent_fertilizings = db.query(
                FertilizingHistory.plant_id,
                func.max(FertilizingHistory.fertilizing_date).label("last_date")
            ).group_by(FertilizingHistory.plant_id).subquery()
            
            plants_to_fertilize = db.query(Plant).join(
                recent_fertilizings,
                Plant.id == recent_fertilizings.c.plant_id
            ).filter(
                Plant.is_archived == False,
                recent_fertilizings.c.last_date <= cutoff_date
            ).all()
            
            for plant in plants_to_fertilize:
                last_fertilizing = db.query(
                    func.max(FertilizingHistory.fertilizing_date)
                ).filter(FertilizingHistory.plant_id == plant.id).scalar()
                
                days_since = (today - last_fertilizing.date()).days if last_fertilizing else None
                
                result.append({
                    "id": plant.id,
                    "name": plant.name,
                    "last_fertilized": last_fertilizing.isoformat() if last_fertilizing else None,
                    "days_since": days_since,
                    "reason": f"Fertilisée il y a {days_since} jours" if days_since else None
                })
            
            return sorted(result, key=lambda x: (x["days_since"] is None, x.get("days_since", 0)))
        except Exception as e:
            print(f"Erreur StatsService.get_upcoming_fertilizing: {e}")
            return []

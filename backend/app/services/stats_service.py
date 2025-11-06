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
            # Plants without any watering history are considered 'never watered'
            never_watered = db.query(Plant).filter(
                Plant.is_archived == False,
                ~Plant.watering_histories.any()
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
                func.max(WateringHistory.date).label("last_date")
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
                    func.max(WateringHistory.date)
                ).filter(WateringHistory.plant_id == plant.id).scalar()

                days_since = (today - last_watering).days if last_watering else None

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
            # Plants without any fertilizing history
            never_fertilized = db.query(Plant).filter(
                Plant.is_archived == False,
                ~Plant.fertilizing_histories.any()
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
                func.max(FertilizingHistory.date).label("last_date")
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
                    func.max(FertilizingHistory.date)
                ).filter(FertilizingHistory.plant_id == plant.id).scalar()

                days_since = (today - last_fertilizing).days if last_fertilizing else None

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

    @staticmethod
    def get_activity(db: Session, days: int = 30) -> dict:
        """
        Récupère l'activité des derniers N jours (arrosages et fertilisations)
        Retourne: {
            "watering_count": int,
            "fertilizing_count": int,
            "daily_activity": [
                {"date": "2025-11-06", "watering": 5, "fertilizing": 2},
                ...
            ]
        }
        """
        try:
            today = datetime.now().date()
            cutoff_date = today - timedelta(days=days)
            
            # Activité d'arrosage par jour
            watering_activity = db.query(
                func.date(WateringHistory.date).label("activity_date"),
                func.count(WateringHistory.id).label("count")
            ).filter(
                WateringHistory.date >= cutoff_date,
                WateringHistory.deleted_at == None
            ).group_by(func.date(WateringHistory.date)).all()
            
            # Activité de fertilisation par jour
            fertilizing_activity = db.query(
                func.date(FertilizingHistory.date).label("activity_date"),
                func.count(FertilizingHistory.id).label("count")
            ).filter(
                FertilizingHistory.date >= cutoff_date,
                FertilizingHistory.deleted_at == None
            ).group_by(func.date(FertilizingHistory.date)).all()
            
            # Organiser les données par date
            activity_dict = {}
            for item in watering_activity:
                date_str = item.activity_date.isoformat()
                if date_str not in activity_dict:
                    activity_dict[date_str] = {"date": date_str, "watering": 0, "fertilizing": 0}
                activity_dict[date_str]["watering"] = item.count
            
            for item in fertilizing_activity:
                date_str = item.activity_date.isoformat()
                if date_str not in activity_dict:
                    activity_dict[date_str] = {"date": date_str, "watering": 0, "fertilizing": 0}
                activity_dict[date_str]["fertilizing"] = item.count
            
            # Trier par date
            daily_activity = sorted(activity_dict.values(), key=lambda x: x["date"])
            
            total_watering = sum(item["watering"] for item in daily_activity)
            total_fertilizing = sum(item["fertilizing"] for item in daily_activity)
            
            return {
                "watering_count": total_watering,
                "fertilizing_count": total_fertilizing,
                "daily_activity": daily_activity
            }
        except Exception as e:
            print(f"Erreur StatsService.get_activity: {e}")
            return {
                "watering_count": 0,
                "fertilizing_count": 0,
                "daily_activity": []
            }


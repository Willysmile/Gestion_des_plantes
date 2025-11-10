"""
Service de statistiques pour le dashboard
"""

from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date

from app.models.plant import Plant
from app.models.histories import WateringHistory, FertilizingHistory
from app.models.lookup import WateringFrequency, PlantSeasonalWatering, PlantSeasonalFertilizing, FertilizerFrequency, Season


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
            
            # Mapper les vraies valeurs de health_status
            # Excellente = healthy
            health_excellent = db.query(Plant).filter(
                Plant.is_archived == False,
                Plant.health_status == "healthy"
            ).count()
            # Bonne = recovering
            health_good = db.query(Plant).filter(
                Plant.is_archived == False,
                Plant.health_status == "recovering"
            ).count()
            # Mauvaise = sick ou dead
            health_poor = db.query(Plant).filter(
                Plant.is_archived == False,
                Plant.health_status.in_(["sick", "dead"])
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
            import traceback
            traceback.print_exc()
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

    @staticmethod
    def get_calendar_events(db: Session, year: int, month: int) -> dict:
        """
        Récupère tous les événements pour un mois donné
        Retourne les arrosages et fertilisations par date (passés ET prédits)
        """
        try:
            from calendar import monthrange
            from sqlalchemy.orm import joinedload
            
            # Vérifier la validité du mois
            if month < 1 or month > 12:
                return {"events": [], "summary": {}}
            
            # Obtenir le nombre de jours dans le mois
            days_in_month = monthrange(year, month)[1]
            
            # Dates limites du mois
            first_day = datetime(year, month, 1).date()
            last_day = datetime(year, month, days_in_month).date()
            
            events = []
            dates_used = set()  # Pour éviter les doublons
            
            # 1. Récupérer tous les arrosages HISTORIQUES du mois
            waterings = db.query(
                func.date(WateringHistory.date).label("event_date"),
                WateringHistory.plant_id,
                func.count(WateringHistory.id).label("count")
            ).filter(
                func.date(WateringHistory.date) >= first_day.isoformat(),
                func.date(WateringHistory.date) <= last_day.isoformat(),
                WateringHistory.deleted_at == None
            ).group_by(func.date(WateringHistory.date), WateringHistory.plant_id).all()
            
            for watering in waterings:
                plant = db.query(Plant).filter(Plant.id == watering.plant_id).first()
                if plant:
                    event_date = watering.event_date if isinstance(watering.event_date, str) else watering.event_date.isoformat()
                    
                    # Déterminer la saison à la date de l'arrosage
                    watering_date = datetime.fromisoformat(event_date).date() if isinstance(event_date, str) else watering.event_date
                    month = watering_date.month
                    
                    # Trouver la saison correspondante
                    season = db.query(Season).filter(
                        ((Season.start_month <= Season.end_month) & (Season.start_month <= month) & (month <= Season.end_month)) |
                        ((Season.start_month > Season.end_month) & ((month >= Season.start_month) | (month <= Season.end_month)))
                    ).first()
                    
                    # Récupérer la fréquence saisonnière
                    seasonal_watering = None
                    seasonal_freq_days = None
                    next_watering_date = None
                    season_name = None
                    
                    if season:
                        season_name = season.name
                        seasonal_watering = db.query(PlantSeasonalWatering).filter(
                            PlantSeasonalWatering.plant_id == plant.id,
                            PlantSeasonalWatering.season_id == season.id
                        ).first()
                        
                        if seasonal_watering and seasonal_watering.watering_frequency_id:
                            freq_obj = db.query(WateringFrequency).filter(
                                WateringFrequency.id == seasonal_watering.watering_frequency_id
                            ).first()
                            if freq_obj and freq_obj.days_interval:
                                seasonal_freq_days = freq_obj.days_interval
                                next_watering_date = (watering_date + timedelta(days=seasonal_freq_days)).isoformat()
                    
                    event_key = f"{event_date}-watering-{watering.plant_id}"
                    event_obj = {
                        "date": event_date,
                        "type": "watering",
                        "plant_id": watering.plant_id,
                        "plant_name": plant.name,
                        "count": watering.count,
                        "is_predicted": False
                    }
                    
                    # Ajouter les infos saisonnières pour les arrosages réels
                    if seasonal_freq_days:
                        event_obj["seasonal_frequency_days"] = seasonal_freq_days
                        event_obj["seasonal_name"] = season_name
                        event_obj["next_watering_estimated"] = next_watering_date
                    
                    events.append(event_obj)
                    dates_used.add(event_key)
            
            # 2. Récupérer toutes les fertilisations HISTORIQUES du mois
            fertilizings = db.query(
                func.date(FertilizingHistory.date).label("event_date"),
                FertilizingHistory.plant_id,
                func.count(FertilizingHistory.id).label("count")
            ).filter(
                func.date(FertilizingHistory.date) >= first_day.isoformat(),
                func.date(FertilizingHistory.date) <= last_day.isoformat(),
                FertilizingHistory.deleted_at == None
            ).group_by(func.date(FertilizingHistory.date), FertilizingHistory.plant_id).all()
            
            for fertilizing in fertilizings:
                plant = db.query(Plant).filter(Plant.id == fertilizing.plant_id).first()
                if plant:
                    event_key = f"{fertilizing.event_date}-fertilizing-{fertilizing.plant_id}"
                    events.append({
                        "date": fertilizing.event_date if isinstance(fertilizing.event_date, str) else fertilizing.event_date.isoformat(),
                        "type": "fertilizing",
                        "plant_id": fertilizing.plant_id,
                        "plant_name": plant.name,
                        "count": fertilizing.count,
                        "is_predicted": False
                    })
                    dates_used.add(event_key)
            
            # 3. AJOUTER LES PRÉDICTIONS D'ARROSAGES FUTURS basées sur la fréquence SAISONNIÈRE
            plants = db.query(Plant).filter(
                Plant.is_archived == False
            ).all()
            
            for plant in plants:
                # Trouver le dernier arrosage
                last_watering = db.query(WateringHistory).filter(
                    WateringHistory.plant_id == plant.id,
                    WateringHistory.deleted_at == None
                ).order_by(WateringHistory.date.desc()).first()
                
                if last_watering:
                    # Calculer le PROCHAIN arrosage à partir du dernier
                    current_date = last_watering.date
                    if isinstance(current_date, str):
                        current_date = datetime.fromisoformat(current_date).date()
                    
                    last_watering_date_str = current_date.isoformat() if isinstance(current_date, date) else current_date
                    
                    # Déterminer la saison du mois actuel
                    current_month = month
                    current_season = db.query(Season).filter(
                        ((Season.start_month <= Season.end_month) & (Season.start_month <= current_month) & (current_month <= Season.end_month)) |
                        ((Season.start_month > Season.end_month) & ((current_month >= Season.start_month) | (current_month <= Season.end_month)))
                    ).first()
                    
                    # Récupérer la fréquence saisonnière, sinon la fréquence par défaut
                    seasonal_freq_days = None
                    if current_season:
                        seasonal_watering = db.query(PlantSeasonalWatering).filter(
                            PlantSeasonalWatering.plant_id == plant.id,
                            PlantSeasonalWatering.season_id == current_season.id
                        ).first()
                        if seasonal_watering and seasonal_watering.watering_frequency_id:
                            freq_obj = db.query(WateringFrequency).filter(
                                WateringFrequency.id == seasonal_watering.watering_frequency_id
                            ).first()
                            if freq_obj:
                                seasonal_freq_days = freq_obj.days_interval
                    
                    # Si pas de fréquence saisonnière, utiliser la fréquence par défaut
                    if seasonal_freq_days is None and plant.watering_frequency_id:
                        freq_obj = db.query(WateringFrequency).filter(
                            WateringFrequency.id == plant.watering_frequency_id
                        ).first()
                        if freq_obj:
                            seasonal_freq_days = freq_obj.days_interval
                    
                    # Générer UNE SEULE prédiction (le prochain arrosage)
                    if seasonal_freq_days:
                        next_date = current_date + timedelta(days=seasonal_freq_days)
                        if next_date <= last_day and next_date >= first_day:  # Dans le mois courant
                            event_key = f"{next_date.isoformat()}-watering-{plant.id}"
                            if event_key not in dates_used:
                                events.append({
                                    "date": next_date.isoformat(),
                                    "type": "watering",
                                    "plant_id": plant.id,
                                    "plant_name": plant.name,
                                    "count": 1,
                                    "is_predicted": True,
                                    "last_watering_date": last_watering_date_str
                                })
                                dates_used.add(event_key)
            
            # 4. AJOUTER LES PRÉDICTIONS DE FERTILISATIONS FUTURES basées sur la fréquence SAISONNIÈRE
            for plant in plants:
                # Trouver la dernière fertilisation
                last_fertilizing = db.query(FertilizingHistory).filter(
                    FertilizingHistory.plant_id == plant.id,
                    FertilizingHistory.deleted_at == None
                ).order_by(FertilizingHistory.date.desc()).first()
                
                if last_fertilizing:
                    # Calculer la PROCHAINE fertilisation à partir de la dernière
                    current_date = last_fertilizing.date
                    if isinstance(current_date, str):
                        current_date = datetime.fromisoformat(current_date).date()
                    
                    last_fertilizing_date_str = current_date.isoformat() if isinstance(current_date, date) else current_date
                    
                    # Déterminer la saison du mois actuel
                    current_month = month
                    current_season = db.query(Season).filter(
                        ((Season.start_month <= Season.end_month) & (Season.start_month <= current_month) & (current_month <= Season.end_month)) |
                        ((Season.start_month > Season.end_month) & ((current_month >= Season.start_month) | (current_month <= Season.end_month)))
                    ).first()
                    
                    # Récupérer la fréquence saisonnière, sinon utiliser une fréquence par défaut
                    seasonal_freq_days = None
                    if current_season:
                        seasonal_fertilizing = db.query(PlantSeasonalFertilizing).filter(
                            PlantSeasonalFertilizing.plant_id == plant.id,
                            PlantSeasonalFertilizing.season_id == current_season.id
                        ).first()
                        if seasonal_fertilizing and seasonal_fertilizing.fertilizer_frequency_id:
                            freq_obj = db.query(FertilizerFrequency).filter(
                                FertilizerFrequency.id == seasonal_fertilizing.fertilizer_frequency_id
                            ).first()
                            if freq_obj and freq_obj.weeks_interval:
                                # Convertir les semaines en jours
                                seasonal_freq_days = freq_obj.weeks_interval * 7
                    
                    # Générer UNE SEULE prédiction (la prochaine fertilisation)
                    if seasonal_freq_days:
                        next_date = current_date + timedelta(days=seasonal_freq_days)
                        if next_date <= last_day and next_date >= first_day:  # Dans le mois courant
                            event_key = f"{next_date.isoformat()}-fertilizing-{plant.id}"
                            if event_key not in dates_used:
                                events.append({
                                    "date": next_date.isoformat(),
                                    "type": "fertilizing",
                                    "plant_id": plant.id,
                                    "plant_name": plant.name,
                                    "count": 1,
                                    "is_predicted": True,
                                    "last_fertilizing_date": last_fertilizing_date_str
                                })
                                dates_used.add(event_key)
            
            # Compter les événements par type
            watering_count = len([e for e in events if e["type"] == "watering" and not e.get("is_predicted", False)])
            watering_predicted = len([e for e in events if e["type"] == "watering" and e.get("is_predicted", False)])
            fertilizing_count = len([e for e in events if e["type"] == "fertilizing" and not e.get("is_predicted", False)])
            fertilizing_predicted = len([e for e in events if e["type"] == "fertilizing" and e.get("is_predicted", False)])
            
            # Résumé
            summary = {
                "year": year,
                "month": month,
                "total_days": days_in_month,
                "active_days": len(set(e["date"] for e in events)),
                "water_events": watering_count,
                "water_events_predicted": watering_predicted,
                "fertilize_events": fertilizing_count,
                "fertilize_events_predicted": fertilizing_predicted,
                "total_events": len(events)
            }
            
            return {
                "events": sorted(events, key=lambda x: x["date"]),
                "summary": summary
            }
        except Exception as e:
            print(f"Erreur StatsService.get_calendar_events: {e}")
            return {"events": [], "summary": {}}

    @staticmethod
    def get_advanced_alerts(db: Session) -> dict:
        """
        Génère des alertes avancées par sévérité
        Sévérité: critical > high > medium > low
        """
        try:
            today = datetime.now().date()
            alerts = []
            
            # Plantes à arroser (jamais arrosées ou > 7 jours)
            never_watered = db.query(Plant).filter(
                Plant.is_archived == False,
                ~Plant.watering_histories.any()
            ).all()
            
            for plant in never_watered:
                alerts.append({
                    "id": f"water_{plant.id}_never",
                    "type": "watering",
                    "plant_id": plant.id,
                    "plant_name": plant.name,
                    "message": f"{plant.name} n'a jamais été arrosée",
                    "severity": "high",
                    "action": "water",
                    "date": None
                })
            
            # Plantes critiquement sèches (> 14 jours)
            recent_waterings = db.query(
                WateringHistory.plant_id,
                func.max(WateringHistory.date).label("last_date")
            ).group_by(WateringHistory.plant_id).subquery()
            
            critical_dry = db.query(Plant).join(
                recent_waterings,
                Plant.id == recent_waterings.c.plant_id
            ).filter(
                Plant.is_archived == False,
                recent_waterings.c.last_date <= today - timedelta(days=14)
            ).all()
            
            for plant in critical_dry:
                last_watering = db.query(
                    func.max(WateringHistory.date)
                ).filter(WateringHistory.plant_id == plant.id).scalar()
                days_since = (today - last_watering).days if last_watering else 0
                
                alerts.append({
                    "id": f"water_{plant.id}_critical",
                    "type": "watering",
                    "plant_id": plant.id,
                    "plant_name": plant.name,
                    "message": f"{plant.name} - URGENT: Non arrosée depuis {days_since} jours",
                    "severity": "critical",
                    "action": "water",
                    "date": last_watering.isoformat() if last_watering else None
                })
            
            # Plantes à arroser bientôt (7-14 jours)
            soon_to_water = db.query(Plant).join(
                recent_waterings,
                Plant.id == recent_waterings.c.plant_id
            ).filter(
                Plant.is_archived == False,
                recent_waterings.c.last_date > today - timedelta(days=14),
                recent_waterings.c.last_date <= today - timedelta(days=7)
            ).all()
            
            for plant in soon_to_water:
                last_watering = db.query(
                    func.max(WateringHistory.date)
                ).filter(WateringHistory.plant_id == plant.id).scalar()
                days_since = (today - last_watering).days if last_watering else 0
                
                alerts.append({
                    "id": f"water_{plant.id}_medium",
                    "type": "watering",
                    "plant_id": plant.id,
                    "plant_name": plant.name,
                    "message": f"{plant.name} - À arroser dans {14 - days_since} jours",
                    "severity": "medium",
                    "action": "water",
                    "date": last_watering.isoformat() if last_watering else None
                })
            
            # Plantes saines - aucune alerte
            healthy = db.query(Plant).join(
                recent_waterings,
                Plant.id == recent_waterings.c.plant_id
            ).filter(
                Plant.is_archived == False,
                recent_waterings.c.last_date > today - timedelta(days=7)
            ).all()
            
            for plant in healthy:
                alerts.append({
                    "id": f"water_{plant.id}_ok",
                    "type": "watering",
                    "plant_id": plant.id,
                    "plant_name": plant.name,
                    "message": f"{plant.name} - Bien hydratée ✓",
                    "severity": "low",
                    "action": "none",
                    "date": None
                })
            
            # Regrouper par sévérité
            by_severity = {
                "critical": [a for a in alerts if a["severity"] == "critical"],
                "high": [a for a in alerts if a["severity"] == "high"],
                "medium": [a for a in alerts if a["severity"] == "medium"],
                "low": [a for a in alerts if a["severity"] == "low"]
            }
            
            return {
                "alerts": sorted(alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x['severity']]),
                "by_severity": by_severity,
                "summary": {
                    "critical_count": len(by_severity["critical"]),
                    "high_count": len(by_severity["high"]),
                    "medium_count": len(by_severity["medium"]),
                    "low_count": len(by_severity["low"]),
                    "total_count": len(alerts)
                }
            }
        except Exception as e:
            print(f"Erreur StatsService.get_advanced_alerts: {e}")
            import traceback
            traceback.print_exc()
            return {
                "alerts": [],
                "by_severity": {"critical": [], "high": [], "medium": [], "low": []},
                "summary": {"critical_count": 0, "high_count": 0, "medium_count": 0, "low_count": 0, "total_count": 0}
            }
            }


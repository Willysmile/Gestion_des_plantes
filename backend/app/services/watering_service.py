"""
Service pour gérer les notifications d'arrosage
"""
from datetime import datetime, timedelta
from app.models.plant import Plant
from app.models.histories import WateringHistory

def get_plants_to_water(session, lookups_service=None):
    """
    Retourne les plantes qui ont besoin d'être arrosées
    basé sur la fréquence d'arrosage et le dernier arrosage
    
    Args:
        session: SQLAlchemy session
        lookups_service: Service pour récupérer les lookups
        
    Returns:
        list[dict]: Liste des plantes à arroser avec infos
    """
    try:
        # Récupérer toutes les plantes actives avec leur fréquence d'arrosage
        plants = session.query(Plant).filter(
            Plant.is_deleted == False
        ).all()
        
        plants_to_water = []
        
        for plant in plants:
            if not plant.watering_frequency_id:
                continue
                
            # Récupérer le dernier arrosage
            last_watering = session.query(WateringHistory).filter(
                WateringHistory.plant_id == plant.id
            ).order_by(WateringHistory.date.desc()).first()
            
            # Calculer les jours écoulés depuis dernier arrosage
            if last_watering:
                days_since = (datetime.utcnow() - last_watering.watering_date).days
            else:
                # Si jamais arrosée, considérer comme très longtemps
                days_since = 999
            
            # Déterminer l'intervalle recommandé (en jours)
            # Cela dépend de la fréquence d'arrosage
            interval_days = get_watering_interval_days(plant.watering_frequency_id)
            
            # Si jours écoulés >= intervalle, plante à arroser
            if days_since >= interval_days:
                urgency = calculate_urgency(days_since, interval_days)
                
                plants_to_water.append({
                    'id': plant.id,
                    'name': plant.name,
                    'scientific_name': plant.scientific_name,
                    'days_since_watering': days_since,
                    'recommended_interval_days': interval_days,
                    'urgency': urgency,  # 'normal', 'high', 'critical'
                    'last_watering': last_watering.date.isoformat() if last_watering else None,
                })
        
        # Trier par urgence (critical > high > normal) puis par days_since
        plants_to_water.sort(key=lambda p: (
            {'critical': 0, 'high': 1, 'normal': 2}[p['urgency']],
            -p['days_since_watering']
        ))
        
        return plants_to_water
        
    except Exception as e:
        print(f"Error in get_plants_to_water: {e}")
        return []


def get_watering_interval_days(frequency_id):
    """
    Retourne l'intervalle d'arrosage en jours basé sur l'ID de fréquence
    
    Args:
        frequency_id: ID de la fréquence d'arrosage
        
    Returns:
        int: Nombre de jours entre arrosages
    """
    # Mapping des fréquences standard
    frequency_map = {
        1: 30,   # Rare: tous les 30 jours
        2: 14,   # Normal: tous les 14 jours
        3: 7,    # Régulier: tous les 7 jours
        4: 3,    # Fréquent: tous les 3 jours
        5: 1,    # Très fréquent: quotidien
    }
    
    return frequency_map.get(frequency_id, 7)  # Default 7 jours


def calculate_urgency(days_since, interval_days):
    """
    Calcule le niveau d'urgence basé sur combien de temps s'est écoulé
    
    Args:
        days_since: Jours écoulés depuis dernier arrosage
        interval_days: Intervalle recommandé en jours
        
    Returns:
        str: 'normal', 'high', 'critical'
    """
    ratio = days_since / interval_days
    
    if ratio >= 2.0:  # Double du temps recommandé
        return 'critical'
    elif ratio >= 1.5:  # 50% plus long que recommandé
        return 'high'
    else:
        return 'normal'


def get_watering_summary(session):
    """
    Retourne un résumé des arrosages pour le dashboard
    
    Args:
        session: SQLAlchemy session
        
    Returns:
        dict: Stats d'arrosage
    """
    try:
        plants_to_water = get_plants_to_water(session)
        
        critical_count = len([p for p in plants_to_water if p['urgency'] == 'critical'])
        high_count = len([p for p in plants_to_water if p['urgency'] == 'high'])
        normal_count = len([p for p in plants_to_water if p['urgency'] == 'normal'])
        
        total_count = len(session.query(Plant).filter(Plant.is_deleted == False).all())
        watered_count = total_count - len(plants_to_water)
        
        return {
            'total_plants': total_count,
            'plants_watered': watered_count,
            'plants_to_water': len(plants_to_water),
            'critical': critical_count,
            'high': high_count,
            'normal': normal_count,
            'plants': plants_to_water,
        }
        
    except Exception as e:
        print(f"Error in get_watering_summary: {e}")
        return {
            'total_plants': 0,
            'plants_watered': 0,
            'plants_to_water': 0,
            'critical': 0,
            'high': 0,
            'normal': 0,
            'plants': [],
        }

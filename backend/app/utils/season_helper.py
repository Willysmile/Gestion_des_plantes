"""
Utilitaires pour déterminer la saison actuelle
"""

def get_current_season_id(month, seasons):
    """
    Détermine la saison courante basée sur le mois (1-12)
    
    Args:
        month: Le mois courant (1-12)
        seasons: Liste des objets Season
        
    Returns:
        L'ID de la saison ou None
    """
    for season in seasons:
        # Cas normal: start_month < end_month (ex: 3-5 pour printemps)
        if season.start_month <= season.end_month:
            if season.start_month <= month <= season.end_month:
                return season.id
        # Cas spécial: start_month > end_month (ex: 12-2 pour hiver)
        else:
            if month >= season.start_month or month <= season.end_month:
                return season.id
    
    return None

"""
Seed data for disease-related lookup tables
"""

DISEASE_TYPES = [
    {"name": "Oïdium", "description": "Maladie fongique blanche poudreuse"},
    {"name": "Mildiou", "description": "Maladie fongique due à l'humidité"},
    {"name": "Rouille", "description": "Maladie fongique avec taches rouilles"},
    {"name": "Pourriture", "description": "Décomposition des tissus"},
    {"name": "Pourriture racinaire", "description": "Pourritures des racines par excès d'eau"},
    {"name": "Tétranyque", "description": "Acarien nuisible"},
    {"name": "Cochenille", "description": "Insecte parasite"},
    {"name": "Mouche blanche", "description": "Petit insecte blanc"},
    {"name": "Pucerons", "description": "Petits insectes suceurs de sève"},
]

TREATMENT_TYPES = [
    {"name": "Fongicide", "description": "Traitement contre les maladies fongiques"},
    {"name": "Insecticide", "description": "Traitement contre les insectes"},
    {"name": "Nettoyage", "description": "Nettoyage manuel des zones affectées"},
    {"name": "Isolation", "description": "Isoler la plante pour éviter la contamination"},
    {"name": "Eau savonneuse", "description": "Solution d'eau et savon"},
    {"name": "Huile de neem", "description": "Traitement naturel à base d'huile de neem"},
    {"name": "Sulfate de cuivre", "description": "Fongicide à base de cuivre"},
    {"name": "Extraction", "description": "Supprimer les parties affectées"},
]

PLANT_HEALTH_STATUSES = [
    {"name": "Sain", "description": "Plante en bonne santé"},
    {"name": "Malade", "description": "Plante atteinte d'une maladie"},
    {"name": "Rétablie", "description": "Plante ayant récupéré"},
    {"name": "Critique", "description": "État critique, intervention urgente requise"},
    {"name": "En traitement", "description": "Plante en cours de traitement"},
    {"name": "En convalescence", "description": "Plante en période de récupération"},
]

"""
Seed data for watering configuration lookup tables
"""

WATERING_METHODS = [
    {"name": "Par le dessus", "description": "Verser directement sur le sol"},
    {"name": "Par le dessous", "description": "Tremper le pot dans un bac d'eau"},
    {"name": "Par brumisation", "description": "Vaporiser sur les feuilles"},
    {"name": "Goutte à goutte", "description": "Arrosage automatique lent et régulier"},
    {"name": "Immersion", "description": "Immerger le pot quelques minutes"},
]

WATER_TYPES = [
    {"name": "Pluie", "description": "Eau de pluie (idéale)"},
    {"name": "Robinet reposée", "description": "Eau du robinet reposée 24h minimum"},
    {"name": "Filtrée", "description": "Eau filtrée (meilleure qualité)"},
    {"name": "Distillée", "description": "Eau distillée (pour plantes sensibles)"},
]

SEASONS = [
    {"name": "Printemps", "start_month": 3, "end_month": 5, "description": "Croissance active, plus d'eau"},
    {"name": "Été", "start_month": 6, "end_month": 8, "description": "Croissance active, maximum d'eau"},
    {"name": "Automne", "start_month": 9, "end_month": 11, "description": "Repos végétatif, moins d'eau"},
    {"name": "Hiver", "start_month": 12, "end_month": 2, "description": "Repos végétatif, minimum d'eau"},
]

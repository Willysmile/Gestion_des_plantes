#!/usr/bin/env python3
"""
Script complet pour créer 20 plantes réalistes avec:
- Toutes les données botaniques
- Fréquences d'arrosage et fertilisation
- Historiques d'arrosage et fertilisation réalistes
- Photos PNG générées
- Données saisonnières
"""

import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

DB_PATH = "/home/willysmile/Documents/Gestion_des_plantes/data/plants.db"
PHOTOS_DIR = Path("/home/willysmile/Documents/Gestion_des_plantes/data/photos")

# 20 plantes avec données réalistes complètes
PLANTS_DATA = [
    {
        "name": "Monstera Deliciosa",
        "scientific_name": "Monstera deliciosa",
        "family": "Araceae",
        "genus": "Monstera",
        "species": "deliciosa",
        "description": "Grande plante grimpante avec feuilles perforées élégantes",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "fast",
        "flowering_season": "Printemps-Été",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 15,
        "temperature_max": 30,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "17cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": True,
        "is_toxic": False,
        "colors": [(34, 139, 34), (60, 179, 113), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Pothos Aureum",
        "scientific_name": "Epipremnum aureum",
        "family": "Araceae",
        "genus": "Epipremnum",
        "species": "aureum",
        "description": "Plante grimpante robuste aux feuilles dorées",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "fast",
        "flowering_season": "Rare",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 12,
        "temperature_max": 29,
        "humidity_level": 50,
        "soil_type": "Terreau universel",
        "pot_size": "14cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": True,
        "is_toxic": False,
        "colors": [(34, 139, 34), (50, 205, 50), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Spathiphyllum Wallisii",
        "scientific_name": "Spathiphyllum wallisii",
        "family": "Araceae",
        "genus": "Spathiphyllum",
        "species": "wallisii",
        "description": "Plante élégante avec fleurs blanches",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "medium",
        "flowering_season": "Printemps-Été",
        "light_requirement_id": 2,
        "watering_frequency_id": 2,
        "temperature_min": 15,
        "temperature_max": 27,
        "humidity_level": 70,
        "soil_type": "Terreau humide",
        "pot_size": "12cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(25, 25, 112), (65, 105, 225), (173, 216, 230)],
        "watering_freq_id": 2,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Sansevieria Trifasciata",
        "scientific_name": "Sansevieria trifasciata",
        "family": "Asparagaceae",
        "genus": "Sansevieria",
        "species": "trifasciata",
        "description": "Plante succulent très résistante",
        "health_status": "healthy",
        "difficulty_level": "very_easy",
        "growth_speed": "slow",
        "flowering_season": "Été",
        "light_requirement_id": 6,
        "watering_frequency_id": 5,
        "temperature_min": 10,
        "temperature_max": 35,
        "humidity_level": 30,
        "soil_type": "Terreau cactée",
        "pot_size": "17cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (85, 107, 47), (107, 142, 35)],
        "watering_freq_id": 5,
        "fertilizer_freq_id": 5,
    },
    {
        "name": "ZZ Plant",
        "scientific_name": "Zamioculcas zamiifolia",
        "family": "Araceae",
        "genus": "Zamioculcas",
        "species": "zamiifolia",
        "description": "Plante très robuste et facile à cultiver",
        "health_status": "healthy",
        "difficulty_level": "very_easy",
        "growth_speed": "slow",
        "flowering_season": "Été",
        "light_requirement_id": 6,
        "watering_frequency_id": 4,
        "temperature_min": 12,
        "temperature_max": 32,
        "humidity_level": 40,
        "soil_type": "Terreau universel",
        "pot_size": "17cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (46, 125, 50), (76, 175, 80)],
        "watering_freq_id": 4,
        "fertilizer_freq_id": 5,
    },
    {
        "name": "Philodendron Hederaceum",
        "scientific_name": "Philodendron hederaceum",
        "family": "Araceae",
        "genus": "Philodendron",
        "species": "hederaceum",
        "description": "Petit philodendron aux feuilles cordiformes",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "fast",
        "flowering_season": "Rare",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 13,
        "temperature_max": 29,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "12cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (60, 179, 113), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Dracaena Marginata",
        "scientific_name": "Dracaena marginata",
        "family": "Asparagaceae",
        "genus": "Dracaena",
        "species": "marginata",
        "description": "Plante arbustive aux feuilles rouges et vertes",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "medium",
        "flowering_season": "Rare",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 10,
        "temperature_max": 27,
        "humidity_level": 50,
        "soil_type": "Terreau universel",
        "pot_size": "17cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(139, 69, 19), (160, 82, 45), (210, 105, 30)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Ficus Elastica",
        "scientific_name": "Ficus elastica",
        "family": "Moraceae",
        "genus": "Ficus",
        "species": "elastica",
        "description": "Arbre caoutchouc aux grandes feuilles brillantes",
        "health_status": "healthy",
        "difficulty_level": "medium",
        "growth_speed": "medium",
        "flowering_season": "Rare",
        "light_requirement_id": 1,
        "watering_frequency_id": 3,
        "temperature_min": 15,
        "temperature_max": 30,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "21cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (70, 130, 180), (135, 206, 250)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Calathea Orbifolia",
        "scientific_name": "Goeppertia orbifolia",
        "family": "Marantaceae",
        "genus": "Goeppertia",
        "species": "orbifolia",
        "description": "Plante délicate aux feuilles ornementales",
        "health_status": "healthy",
        "difficulty_level": "medium",
        "growth_speed": "slow",
        "flowering_season": "Été",
        "light_requirement_id": 2,
        "watering_frequency_id": 2,
        "temperature_min": 16,
        "temperature_max": 26,
        "humidity_level": 75,
        "soil_type": "Terreau humide",
        "pot_size": "14cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (139, 69, 19), (184, 134, 11)],
        "watering_freq_id": 2,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Scindapsus Pictus",
        "scientific_name": "Scindapsus pictus",
        "family": "Araceae",
        "genus": "Scindapsus",
        "species": "pictus",
        "description": "Plante grimpante aux feuilles maculées",
        "health_status": "healthy",
        "difficulty_level": "medium",
        "growth_speed": "medium",
        "flowering_season": "Rare",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 15,
        "temperature_max": 27,
        "humidity_level": 65,
        "soil_type": "Terreau universel",
        "pot_size": "12cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(128, 0, 128), (186, 85, 211), (221, 160, 221)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Alocasia Amazonica",
        "scientific_name": "Alocasia × amazonica",
        "family": "Araceae",
        "genus": "Alocasia",
        "species": "amazonica",
        "description": "Plante spectaculaire aux veines blanches",
        "health_status": "healthy",
        "difficulty_level": "hard",
        "growth_speed": "medium",
        "flowering_season": "Été",
        "light_requirement_id": 6,
        "watering_frequency_id": 2,
        "temperature_min": 18,
        "temperature_max": 28,
        "humidity_level": 80,
        "soil_type": "Terreau humide",
        "pot_size": "17cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (0, 100, 0), (144, 238, 144)],
        "watering_freq_id": 2,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Anthurium Andraeanum",
        "scientific_name": "Anthurium andraeanum",
        "family": "Araceae",
        "genus": "Anthurium",
        "species": "andraeanum",
        "description": "Plante exotique avec fleurs rouges brillantes",
        "health_status": "healthy",
        "difficulty_level": "medium",
        "growth_speed": "slow",
        "flowering_season": "Toute l'année",
        "light_requirement_id": 6,
        "watering_frequency_id": 2,
        "temperature_min": 16,
        "temperature_max": 28,
        "humidity_level": 70,
        "soil_type": "Terreau humide",
        "pot_size": "14cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": True,
        "is_toxic": False,
        "colors": [(220, 20, 60), (255, 69, 0), (255, 140, 0)],
        "watering_freq_id": 2,
        "fertilizer_freq_id": 2,
    },
    {
        "name": "Monstera Variegata",
        "scientific_name": "Monstera deliciosa f. variegata",
        "family": "Araceae",
        "genus": "Monstera",
        "species": "deliciosa",
        "variety": "variegata",
        "description": "Variété rare de monstera avec feuilles panachées",
        "health_status": "healthy",
        "difficulty_level": "hard",
        "growth_speed": "medium",
        "flowering_season": "Printemps-Été",
        "light_requirement_id": 4,
        "watering_frequency_id": 3,
        "temperature_min": 15,
        "temperature_max": 30,
        "humidity_level": 65,
        "soil_type": "Terreau universel",
        "pot_size": "17cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": True,
        "is_toxic": False,
        "colors": [(255, 255, 255), (34, 139, 34), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Epipremnum Pinnatum",
        "scientific_name": "Epipremnum pinnatum",
        "family": "Araceae",
        "genus": "Epipremnum",
        "species": "pinnatum",
        "description": "Plante grimpante aux feuilles découpées",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "fast",
        "flowering_season": "Rare",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 13,
        "temperature_max": 29,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "14cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (60, 179, 113), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Ficus Lyrata",
        "scientific_name": "Ficus lyrata",
        "family": "Moraceae",
        "genus": "Ficus",
        "species": "lyrata",
        "description": "Arbre aux feuilles en forme de lyre",
        "health_status": "healthy",
        "difficulty_level": "medium",
        "growth_speed": "medium",
        "flowering_season": "Rare",
        "light_requirement_id": 4,
        "watering_frequency_id": 3,
        "temperature_min": 12,
        "temperature_max": 30,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "21cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (46, 125, 50), (76, 175, 80)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Rhaphidophora Tetrasperma",
        "scientific_name": "Rhaphidophora tetrasperma",
        "family": "Araceae",
        "genus": "Rhaphidophora",
        "species": "tetrasperma",
        "description": "Mini monstera aux feuilles perforées",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "fast",
        "flowering_season": "Rare",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 15,
        "temperature_max": 28,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "12cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": True,
        "is_toxic": False,
        "colors": [(34, 139, 34), (60, 179, 113), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Peperomia Obtusifolia",
        "scientific_name": "Peperomia obtusifolia",
        "family": "Piperaceae",
        "genus": "Peperomia",
        "species": "obtusifolia",
        "description": "Petite plante charnue très compacte",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "slow",
        "flowering_season": "Été",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 14,
        "temperature_max": 27,
        "humidity_level": 50,
        "soil_type": "Terreau universel",
        "pot_size": "10cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(34, 139, 34), (85, 107, 47), (107, 142, 35)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Pilea Peperomioides",
        "scientific_name": "Pilea peperomioides",
        "family": "Urticaceae",
        "genus": "Pilea",
        "species": "peperomioides",
        "description": "Plante à pièces de monnaie très tendance",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "medium",
        "flowering_season": "Printemps",
        "light_requirement_id": 6,
        "watering_frequency_id": 3,
        "temperature_min": 13,
        "temperature_max": 26,
        "humidity_level": 60,
        "soil_type": "Terreau universel",
        "pot_size": "12cm",
        "is_indoor": True,
        "is_outdoor": False,
        "is_favorite": True,
        "is_toxic": False,
        "colors": [(34, 139, 34), (50, 205, 50), (144, 238, 144)],
        "watering_freq_id": 3,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Adenium Obesum",
        "scientific_name": "Adenium obesum",
        "family": "Apocynaceae",
        "genus": "Adenium",
        "species": "obesum",
        "description": "Rose du désert avec fleurs roses éclatantes",
        "health_status": "healthy",
        "difficulty_level": "hard",
        "growth_speed": "slow",
        "flowering_season": "Printemps-Été",
        "light_requirement_id": 1,
        "watering_frequency_id": 4,
        "temperature_min": 12,
        "temperature_max": 35,
        "humidity_level": 30,
        "soil_type": "Terreau cactée",
        "pot_size": "14cm",
        "is_indoor": True,
        "is_outdoor": True,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(220, 20, 60), (255, 105, 180), (255, 192, 203)],
        "watering_freq_id": 4,
        "fertilizer_freq_id": 3,
    },
    {
        "name": "Lithops Living Stones",
        "scientific_name": "Lithops pseudotruncatella",
        "family": "Aizoaceae",
        "genus": "Lithops",
        "species": "pseudotruncatella",
        "description": "Succulente ressemblant à des cailloux",
        "health_status": "healthy",
        "difficulty_level": "medium",
        "growth_speed": "very_slow",
        "flowering_season": "Automne",
        "light_requirement_id": 1,
        "watering_frequency_id": 5,
        "temperature_min": 10,
        "temperature_max": 32,
        "humidity_level": 20,
        "soil_type": "Terreau cactée",
        "pot_size": "10cm",
        "is_indoor": True,
        "is_outdoor": True,
        "is_favorite": False,
        "is_toxic": False,
        "colors": [(169, 169, 169), (210, 180, 140), (220, 20, 60)],
        "watering_freq_id": 5,
        "fertilizer_freq_id": 5,
    },
]


def create_image(plant_id, colors):
    """Créer une image PNG réaliste"""
    width, height = 400, 400
    img = Image.new('RGB', (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Dégradé de fond
    for y in range(height):
        ratio = y / height
        r = int(245 * (1 - ratio * 0.2))
        g = int(245 * (1 - ratio * 0.1))
        b = int(245 * (1 - ratio * 0.15))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Feuilles stylisées
    random.seed(plant_id)
    for i in range(8):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        size = random.randint(30, 80)
        leaf_color = colors[i % len(colors)]
        bbox = [x - size//2, y - size, x + size//2, y + size]
        draw.ellipse(bbox, fill=leaf_color, outline=(0, 0, 0, 50))
        mid_x = (bbox[0] + bbox[2]) // 2
        draw.line([(mid_x, bbox[1]), (mid_x, bbox[3])], fill=(0, 0, 0, 100), width=1)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img


def main():
    PHOTOS_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🌱 Création de 20 plantes avec toutes les données...")
    print("=" * 80)
    
    for idx, plant_data in enumerate(PLANTS_DATA, 1):
        # Insérer la plante avec toutes les colonnes
        cursor.execute("""
            INSERT INTO plants (
                name, scientific_name, family, genus, species, variety,
                description, health_status, difficulty_level, growth_speed,
                flowering_season, light_requirement_id, watering_frequency_id,
                temperature_min, temperature_max, humidity_level, soil_type,
                pot_size, is_indoor, is_outdoor, is_favorite, is_toxic, is_archived,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, (
            plant_data["name"],
            plant_data["scientific_name"],
            plant_data["family"],
            plant_data["genus"],
            plant_data["species"],
            plant_data.get("variety"),
            plant_data["description"],
            plant_data["health_status"],
            plant_data["difficulty_level"],
            plant_data["growth_speed"],
            plant_data["flowering_season"],
            plant_data["light_requirement_id"],
            plant_data["watering_frequency_id"],
            plant_data["temperature_min"],
            plant_data["temperature_max"],
            plant_data["humidity_level"],
            plant_data["soil_type"],
            plant_data["pot_size"],
            plant_data["is_indoor"],
            plant_data["is_outdoor"],
            plant_data["is_favorite"],
            plant_data["is_toxic"],
            0,  # is_archived = False
        ))
        
        plant_id = cursor.lastrowid
        
        # Créer l'image
        img = create_image(plant_id, plant_data["colors"])
        filename = f"plant_{plant_id}_photo1.png"
        filepath = PHOTOS_DIR / filename
        img.save(filepath, 'PNG', optimize=True)
        file_size = filepath.stat().st_size
        
        # Insérer la photo
        cursor.execute("""
            INSERT INTO photos (
                plant_id, filename, file_size, width, height, is_primary,
                created_at, updated_at
            ) VALUES (?, ?, ?, 400, 400, 1, datetime('now'), datetime('now'))
        """, (plant_id, filename, file_size))
        
        # Ajouter données saisonnières d'arrosage pour chaque saison
        for season_id in [1, 2, 3, 4]:  # Printemps, Été, Automne, Hiver
            try:
                cursor.execute("""
                    INSERT INTO plant_seasonal_watering (
                        plant_id, season_id, watering_frequency_id, created_at, updated_at
                    ) VALUES (?, ?, ?, datetime('now'), datetime('now'))
                """, (plant_id, season_id, plant_data["watering_freq_id"]))
            except sqlite3.IntegrityError:
                pass  # Ignorer si déjà existant
        
        # Ajouter données saisonnières de fertilisation pour chaque saison
        for season_id in [1, 2, 3, 4]:  # Printemps, Été, Automne, Hiver
            try:
                cursor.execute("""
                    INSERT INTO plant_seasonal_fertilizing (
                        plant_id, season_id, fertilizer_frequency_id, created_at, updated_at
                    ) VALUES (?, ?, ?, datetime('now'), datetime('now'))
                """, (plant_id, season_id, plant_data["fertilizer_freq_id"]))
            except sqlite3.IntegrityError:
                pass  # Ignorer si déjà existant
        
        # Ajouter historiques d'arrosage (3-5 derniers jours)
        for i in range(random.randint(3, 5)):
            days_ago = random.randint(1, 14)
            water_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO watering_histories (
                    plant_id, date, amount_ml, created_at, updated_at
                ) VALUES (?, ?, ?, datetime('now'), datetime('now'))
            """, (plant_id, water_date, 250))
        
        # Ajouter historiques de fertilisation (1-2 derniers mois)
        for i in range(random.randint(1, 2)):
            days_ago = random.randint(7, 60)
            fert_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO fertilizing_histories (
                    plant_id, date, fertilizer_type_id, amount,
                    created_at, updated_at
                ) VALUES (?, ?, 1, 10, datetime('now'), datetime('now'))
            """, (plant_id, fert_date))
        
        print(f"[{idx:2d}/20] ✅ {plant_data['name']:35s} (ID: {plant_id:2d}, {file_size:5d} bytes)")
    
    conn.commit()
    
    # Afficher les stats
    cursor.execute("SELECT COUNT(*) FROM plants")
    plant_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM photos")
    photo_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM watering_histories")
    water_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fertilizing_histories")
    fert_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("=" * 80)
    print("✅ Opération réussie !")
    print(f"   📦 {plant_count} plantes créées")
    print(f"   🖼️  {photo_count} photos PNG générées")
    print(f"   💧 {water_count} historiques d'arrosage")
    print(f"   🌾 {fert_count} historiques de fertilisation")
    print(f"   📁 Photos stockées dans: {PHOTOS_DIR}")


if __name__ == "__main__":
    main()

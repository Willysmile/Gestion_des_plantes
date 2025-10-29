"""Seed sample plants for testing photo gallery"""
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.plant import Plant
from app.models.histories import WateringHistory, FertilizingHistory, RepottingHistory, DiseaseHistory

SAMPLE_PLANTS = [
    {
        "name": "Monstera Deliciosa",
        "scientific_name": "Monstera deliciosa",
        "family": "Araceae",
        "light_requirement_id": 2,
        "watering_frequency_id": 2,
        "temperature_min": 18,
        "temperature_max": 27,
        "humidity_level": 65,
        "soil_type": "Well-draining potting mix",
        "location_id": 1,
        "purchase_place_id": 1,
        "purchase_price": 45.99,
        "is_indoor": True,
        "difficulty_level": "easy",
    },
    {
        "name": "Sansevieria trifasciata",
        "scientific_name": "Sansevieria trifasciata",
        "family": "Asparagaceae",
        "light_requirement_id": 3,
        "watering_frequency_id": 4,
        "temperature_min": 16,
        "temperature_max": 27,
        "humidity_level": 45,
        "soil_type": "Cactus/succulent mix",
        "location_id": 2,
        "purchase_place_id": 2,
        "purchase_price": 22.50,
        "is_indoor": True,
        "difficulty_level": "easy",
    },
    {
        "name": "Pothos (Devil's Ivy)",
        "scientific_name": "Epipremnum aureum",
        "family": "Araceae",
        "light_requirement_id": 2,
        "watering_frequency_id": 2,
        "temperature_min": 16,
        "temperature_max": 27,
        "humidity_level": 55,
        "soil_type": "General-purpose potting mix",
        "location_id": 3,
        "purchase_place_id": 1,
        "purchase_price": 15.00,
        "is_indoor": True,
        "difficulty_level": "easy",
    },
    {
        "name": "Fiddle Leaf Fig",
        "scientific_name": "Ficus lyrata",
        "family": "Moraceae",
        "light_requirement_id": 1,
        "watering_frequency_id": 2,
        "temperature_min": 16,
        "temperature_max": 27,
        "humidity_level": 60,
        "soil_type": "Well-draining potting mix",
        "location_id": 1,
        "purchase_place_id": 2,
        "purchase_price": 60.00,
        "is_indoor": True,
        "difficulty_level": "medium",
    },
    {
        "name": "Calathea Orbifolia",
        "scientific_name": "Goeppertia orbifolia",
        "family": "Marantaceae",
        "light_requirement_id": 2,
        "watering_frequency_id": 2,
        "temperature_min": 18,
        "temperature_max": 27,
        "humidity_level": 70,
        "soil_type": "Well-draining potting mix",
        "location_id": 2,
        "purchase_place_id": 1,
        "purchase_price": 35.99,
        "is_indoor": True,
        "difficulty_level": "medium",
    },
]


def seed_plants(db: Session):
    """Seed sample plants if they don't exist"""
    try:
        existing_count = db.query(Plant).count()
        if existing_count > 0:
            print(f"✅ Plants already seeded ({existing_count} plants found)")
            return

        print("🌱 Seeding sample plants...")
        plants = []
        for plant_data in SAMPLE_PLANTS:
            plant = Plant(**plant_data)
            db.add(plant)
            plants.append(plant)
            print(f"  ✓ {plant.name}")

        db.commit()
        print(f"✅ {len(SAMPLE_PLANTS)} plants seeded successfully!")
        
        # Ajouter des enregistrements historiques
        seed_plant_histories(db, plants)

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding plants: {e}")
        raise


def seed_plant_histories(db: Session, plants: list):
    """Ajouter des historiques pour les plantes seeded"""
    if not plants:
        return
    
    print("\n🌿 Seeding plant histories...")
    today = date.today()
    
    # Historique d'arrosage pour la première plante
    if len(plants) > 0:
        plant = plants[0]
        watering_records = [
            WateringHistory(plant_id=plant.id, date=today - timedelta(days=7), amount_ml=250, notes="Arrosage régulier"),
            WateringHistory(plant_id=plant.id, date=today - timedelta(days=4), amount_ml=300, notes="Feuilles asséchées"),
            WateringHistory(plant_id=plant.id, date=today - timedelta(days=1), amount_ml=250, notes="Eau tiède"),
        ]
        for record in watering_records:
            db.add(record)
        print(f"  ✓ Arrosage x{len(watering_records)} pour {plant.name}")
    
    # Historique de fertilisation pour la deuxième plante
    if len(plants) > 1:
        plant = plants[1]
        fertilizing_records = [
            FertilizingHistory(plant_id=plant.id, date=today - timedelta(days=30), fertilizer_type_id=1, amount=20, notes="NPK équilibré"),
            FertilizingHistory(plant_id=plant.id, date=today - timedelta(days=15), fertilizer_type_id=2, amount=15, notes="Riche en azote pour feuillage"),
        ]
        for record in fertilizing_records:
            db.add(record)
        print(f"  ✓ Fertilisation x{len(fertilizing_records)} pour {plant.name}")
    
    # Historique de rempotage pour la troisième plante
    if len(plants) > 2:
        plant = plants[2]
        repotting_records = [
            RepottingHistory(plant_id=plant.id, date=today - timedelta(days=60), soil_type="Terreau universel", pot_size_before=15, pot_size_after=20, notes="Rempotage printemps"),
        ]
        for record in repotting_records:
            db.add(record)
        print(f"  ✓ Rempotage x{len(repotting_records)} pour {plant.name}")
    
    # Historique de maladie pour la quatrième plante
    if len(plants) > 3:
        plant = plants[3]
        disease_records = [
            DiseaseHistory(plant_id=plant.id, date=today - timedelta(days=45), disease_type_id=1, treatment_type_id=1, health_status_id=3, notes="Araignées rouges détectées"),
            DiseaseHistory(plant_id=plant.id, date=today - timedelta(days=30), disease_type_id=1, health_status_id=2, notes="Traitement en cours"),
            DiseaseHistory(plant_id=plant.id, date=today - timedelta(days=15), disease_type_id=1, health_status_id=1, treated_date=today - timedelta(days=20), recovered=True, notes="Plante rétablie"),
        ]
        for record in disease_records:
            db.add(record)
        print(f"  ✓ Maladie x{len(disease_records)} pour {plant.name}")
    
    db.commit()
    print("✅ Plant histories seeded successfully!\n")

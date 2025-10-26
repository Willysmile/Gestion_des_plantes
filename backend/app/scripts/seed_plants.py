"""Seed sample plants for testing photo gallery"""
from sqlalchemy.orm import Session
from app.models.plant import Plant

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
        for plant_data in SAMPLE_PLANTS:
            plant = Plant(**plant_data)
            db.add(plant)
            print(f"  ✓ {plant.name}")

        db.commit()
        print(f"✅ {len(SAMPLE_PLANTS)} plants seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding plants: {e}")
        raise

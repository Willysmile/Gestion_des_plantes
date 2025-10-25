"""
Seed script pour pré-remplir les lookup tables au démarrage
Exécuté une seule fois lors de l'init DB
"""

from sqlalchemy.orm import Session
from app.models.lookup import (
    Location,
    PurchasePlace,
    WateringFrequency,
    LightRequirement,
    FertilizerType,
)


def seed_locations(db: Session) -> None:
    """Pré-remplit les emplacements"""
    locations = [
        Location(name="Salon", description="Pièce principale"),
        Location(name="Chambre", description="Chambre à coucher"),
        Location(name="Cuisine", description="Cuisine"),
        Location(name="Bureau", description="Bureau/Workspace"),
        Location(name="Terrasse", description="Balcon/Terrasse extérieure"),
        Location(name="Serre", description="Serre intérieure"),
        Location(name="Véranda", description="Véranda"),
    ]
    
    for loc in locations:
        if not db.query(Location).filter(Location.name == loc.name).first():
            db.add(loc)
    
    db.commit()


def seed_purchase_places(db: Session) -> None:
    """Pré-remplit les lieux d'achat"""
    places = [
        PurchasePlace(name="Jardinerie locale", url=None),
        PurchasePlace(name="Pépinière", url=None),
        PurchasePlace(name="Marché", url=None),
        PurchasePlace(name="Amazon", url="https://www.amazon.fr"),
        PurchasePlace(name="Etsy", url="https://www.etsy.com"),
        PurchasePlace(name="Truffaut", url="https://www.truffaut.com"),
        PurchasePlace(name="Botanic", url="https://www.botanic.com"),
        PurchasePlace(name="Échange/Ami", url=None),
    ]
    
    for place in places:
        if not db.query(PurchasePlace).filter(PurchasePlace.name == place.name).first():
            db.add(place)
    
    db.commit()


def seed_watering_frequencies(db: Session) -> None:
    """Pré-remplit les fréquences d'arrosage"""
    frequencies = [
        WateringFrequency(name="Très rare (1x/mois)", days_interval=30),
        WateringFrequency(name="Rare (2x/mois)", days_interval=15),
        WateringFrequency(name="Normal (1x/semaine)", days_interval=7),
        WateringFrequency(name="Régulier (2-3x/semaine)", days_interval=3),
        WateringFrequency(name="Fréquent (tous les jours)", days_interval=1),
        WateringFrequency(name="Laisser sécher entre arrosages", days_interval=14),
        WateringFrequency(name="Garder humide", days_interval=2),
    ]
    
    for freq in frequencies:
        if not db.query(WateringFrequency).filter(WateringFrequency.name == freq.name).first():
            db.add(freq)
    
    db.commit()


def seed_light_requirements(db: Session) -> None:
    """Pré-remplit les exigences lumineuses"""
    requirements = [
        LightRequirement(name="Lumière directe", description="Besoin de lumière directe du soleil"),
        LightRequirement(name="Mi-ombre", description="Lumière indirecte, mi-ombre"),
        LightRequirement(name="Ombre", description="Ombre, peu de lumière"),
        LightRequirement(name="Ombre profonde", description="Peut survivre en ombre profonde"),
        LightRequirement(name="Lumière indirecte", description="Lumière indirecte vive"),
        LightRequirement(name="Variable", description="Flexible, s'adapte à la lumière"),
    ]
    
    for req in requirements:
        if not db.query(LightRequirement).filter(LightRequirement.name == req.name).first():
            db.add(req)
    
    db.commit()


def seed_fertilizer_types(db: Session) -> None:
    """Pré-remplit les types d'engrais"""
    types = [
        FertilizerType(name="NPK équilibré (10-10-10)", description="Engrais équilibré pour usage général"),
        FertilizerType(name="NPK riche en Azote (20-5-5)", description="Pour feuillage luxuriant"),
        FertilizerType(name="NPK riche en Potassium (5-10-20)", description="Pour fleurs et fruits"),
        FertilizerType(name="Engrais bio", description="Engrais organique naturel"),
        FertilizerType(name="Engrais liquide", description="Engrais dilué à l'eau"),
        FertilizerType(name="Bâtons d'engrais", description="Engrais à libération lente"),
        FertilizerType(name="Compost", description="Compost maison ou acheté"),
        FertilizerType(name="Engrais foliaire", description="À pulvériser sur les feuilles"),
    ]
    
    for fert in types:
        if not db.query(FertilizerType).filter(FertilizerType.name == fert.name).first():
            db.add(fert)
    
    db.commit()


def seed_all(db: Session) -> None:
    """Exécute tous les seeds"""
    print("🌱 Seeding lookup tables...")
    
    seed_locations(db)
    print("✅ Locations seeded")
    
    seed_purchase_places(db)
    print("✅ Purchase places seeded")
    
    seed_watering_frequencies(db)
    print("✅ Watering frequencies seeded")
    
    seed_light_requirements(db)
    print("✅ Light requirements seeded")
    
    seed_fertilizer_types(db)
    print("✅ Fertilizer types seeded")
    
    print("✅ All lookups seeded successfully!")

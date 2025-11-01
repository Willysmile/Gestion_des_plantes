"""
Seed script pour pré-remplir les lookup tables au démarrage
Exécuté une seule fois lors de l'init DB
"""

from sqlalchemy.orm import Session
from app.models.lookup import (
    Location,
    PurchasePlace,
    WateringFrequency,
    FertilizerFrequency,
    LightRequirement,
    Unit,
    FertilizerType,
    DiseaseType,
    TreatmentType,
    PlantHealthStatus,
    WateringMethod,
    WaterType,
    Season,
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


def seed_fertilizer_frequencies(db: Session) -> None:
    """Pré-remplit les fréquences de fertilisation"""
    frequencies = [
        FertilizerFrequency(name="Hebdomadaire", weeks_interval=1),
        FertilizerFrequency(name="Bi-hebdomadaire", weeks_interval=2),
        FertilizerFrequency(name="Mensuel", weeks_interval=4),
        FertilizerFrequency(name="Tous les 6 semaines", weeks_interval=6),
        FertilizerFrequency(name="Trimestriel", weeks_interval=12),
    ]
    
    for freq in frequencies:
        if not db.query(FertilizerFrequency).filter(FertilizerFrequency.name == freq.name).first():
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


def seed_units(db: Session) -> None:
    """Pré-remplit les unités"""
    units = [
        Unit(name="millilitre", symbol="ml", description="Unité de volume"),
        Unit(name="litre", symbol="L", description="Unité de volume"),
        Unit(name="centimètre cube", symbol="cm³", description="Unité de volume"),
        Unit(name="gramme", symbol="g", description="Unité de poids"),
        Unit(name="kilogramme", symbol="kg", description="Unité de poids"),
        Unit(name="cuillère", symbol="c.", description="Mesure à la cuillère"),
        Unit(name="bâton", symbol="bâton", description="Engrais en forme de bâton"),
        Unit(name="pastille", symbol="pastille", description="Engrais en forme de pastille"),
        Unit(name="dose", symbol="dose", description="Une dose"),
        Unit(name="unité", symbol="unité", description="Unité générique"),
    ]
    
    for unit in units:
        if not db.query(Unit).filter(Unit.name == unit.name).first():
            db.add(unit)
    
    db.commit()


def seed_fertilizer_types(db: Session) -> None:
    """Pré-remplit les types d'engrais"""
    types = [
        FertilizerType(name="NPK équilibré (10-10-10)", description="Engrais équilibré pour usage général", unit="ml"),
        FertilizerType(name="NPK riche en Azote (20-5-5)", description="Pour feuillage luxuriant", unit="ml"),
        FertilizerType(name="NPK riche en Potassium (5-10-20)", description="Pour fleurs et fruits", unit="ml"),
        FertilizerType(name="Engrais bio", description="Engrais organique naturel", unit="g"),
        FertilizerType(name="Engrais liquide", description="Engrais dilué à l'eau", unit="ml"),
        FertilizerType(name="Bâtons d'engrais", description="Engrais à libération lente", unit="unité"),
        FertilizerType(name="Compost", description="Compost maison ou acheté", unit="L"),
        FertilizerType(name="Engrais foliaire", description="À pulvériser sur les feuilles", unit="ml"),
    ]
    
    for fert in types:
        if not db.query(FertilizerType).filter(FertilizerType.name == fert.name).first():
            db.add(fert)
    
    db.commit()



def seed_disease_types(db: Session) -> None:
    """Pré-remplit les types de maladies"""
    disease_types = [
        DiseaseType(name="Oïdium", description="Maladie fongique blanche poudreuse"),
        DiseaseType(name="Mildiou", description="Maladie fongique due à l'humidité"),
        DiseaseType(name="Rouille", description="Maladie fongique avec taches rouilles"),
        DiseaseType(name="Pourriture", description="Décomposition des tissus"),
        DiseaseType(name="Pourriture racinaire", description="Pourritures des racines par excès d'eau"),
        DiseaseType(name="Tétranyque", description="Acarien nuisible"),
        DiseaseType(name="Cochenille", description="Insecte parasite"),
        DiseaseType(name="Mouche blanche", description="Petit insecte blanc"),
        DiseaseType(name="Pucerons", description="Petits insectes suceurs de sève"),
    ]
    
    for dt in disease_types:
        if not db.query(DiseaseType).filter(DiseaseType.name == dt.name).first():
            db.add(dt)
    
    db.commit()


def seed_treatment_types(db: Session) -> None:
    """Pré-remplit les types de traitement"""
    treatment_types = [
        TreatmentType(name="Fongicide", description="Traitement contre les maladies fongiques"),
        TreatmentType(name="Insecticide", description="Traitement contre les insectes"),
        TreatmentType(name="Nettoyage", description="Nettoyage manuel des zones affectées"),
        TreatmentType(name="Isolation", description="Isoler la plante pour éviter la contamination"),
        TreatmentType(name="Eau savonneuse", description="Solution d'eau et savon"),
        TreatmentType(name="Huile de neem", description="Traitement naturel à base d'huile de neem"),
        TreatmentType(name="Sulfate de cuivre", description="Fongicide à base de cuivre"),
        TreatmentType(name="Extraction", description="Supprimer les parties affectées"),
    ]
    
    for tt in treatment_types:
        if not db.query(TreatmentType).filter(TreatmentType.name == tt.name).first():
            db.add(tt)
    
    db.commit()


def seed_plant_health_statuses(db: Session) -> None:
    """Pré-remplit les états de santé des plantes"""
    statuses = [
        PlantHealthStatus(name="Sain", description="Plante en bonne santé"),
        PlantHealthStatus(name="Malade", description="Plante atteinte d'une maladie"),
        PlantHealthStatus(name="Rétablie", description="Plante ayant récupéré"),
        PlantHealthStatus(name="Critique", description="État critique, intervention urgente requise"),
        PlantHealthStatus(name="En traitement", description="Plante en cours de traitement"),
        PlantHealthStatus(name="En convalescence", description="Plante en période de récupération"),
    ]
    
    for status in statuses:
        if not db.query(PlantHealthStatus).filter(PlantHealthStatus.name == status.name).first():
            db.add(status)
    
    db.commit()


def seed_watering_methods(db: Session) -> None:
    """Pré-remplit les méthodes d'arrosage"""
    from app.scripts.seed_watering_lookups import WATERING_METHODS
    
    for data in WATERING_METHODS:
        if not db.query(WateringMethod).filter(WateringMethod.name == data["name"]).first():
            db.add(WateringMethod(**data))
    
    db.commit()


def seed_water_types(db: Session) -> None:
    """Pré-remplit les types d'eau"""
    from app.scripts.seed_watering_lookups import WATER_TYPES
    
    for data in WATER_TYPES:
        if not db.query(WaterType).filter(WaterType.name == data["name"]).first():
            db.add(WaterType(**data))
    
    db.commit()


def seed_seasons(db: Session) -> None:
    """Pré-remplit les saisons"""
    from app.scripts.seed_watering_lookups import SEASONS
    
    for data in SEASONS:
        if not db.query(Season).filter(Season.name == data["name"]).first():
            db.add(Season(**data))
    
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
    
    seed_fertilizer_frequencies(db)
    print("✅ Fertilizer frequencies seeded")

    seed_light_requirements(db)
    print("✅ Light requirements seeded")
    
    seed_units(db)
    print("✅ Units seeded")

    seed_fertilizer_types(db)
    print("✅ Fertilizer types seeded")

    seed_disease_types(db)
    print("✅ Disease types seeded")

    seed_treatment_types(db)
    print("✅ Treatment types seeded")

    seed_plant_health_statuses(db)
    print("✅ Plant health statuses seeded")

    seed_watering_methods(db)
    print("✅ Watering methods seeded")

    seed_water_types(db)
    print("✅ Water types seeded")

    seed_seasons(db)
    print("✅ Seasons seeded")
    
    print("✅ All lookups seeded successfully!")


"""
Script pour peupler les catégories et tags dans la base de données
"""

from sqlalchemy.orm import Session
from app.models.tags import TagCategory, Tag
from app.models.lookup import Location, LightRequirement

def seed_tag_categories_and_tags(db: Session):
    """
    Peuuple les catégories et tags pré-remplis
    """
    
    # Vérifier si les catégories existent déjà
    categories_count = db.query(TagCategory).count()
    if categories_count > 0:
        print(f"✅ Catégories de tags déjà présentes ({categories_count})")
        # Mais on doit quand même vérifier les tags manquants
        sync_location_tags(db)
        sync_light_requirement_tags(db)
        return
    
    print("🌱 Création des catégories et tags...")
    
    # Récupérer toutes les locations et light requirements pour créer les tags correspondants
    locations = db.query(Location).all()
    location_names = [loc.name for loc in locations]
    
    light_reqs = db.query(LightRequirement).all()
    light_req_names = [lr.name for lr in light_reqs]
    
    # Données des catégories et tags
    tags_data = {
        # AUTO-GÉNÉRÉS (3 catégories)
        "Emplacement": location_names,  # Dynamique basé sur les locations
        
        "État de la plante": [
            "En bonne santé", "Malade", "En rétablissement", "Morte", "En traitement", "En convalescence"
        ],
        
        "Luminosité": light_req_names,  # Dynamique basé sur les light requirements
        
        # MANUELS (6 catégories)
        "Type de plante": [
            "Succulente", "Cactus", "Plante verte", "Plante à fleurs",
            "Plante retombante", "Orchidée", "Fougère", "Herbe aromatique"
        ],
        
        "Besoins en eau": [
            "Très peu d'eau", "Peu d'eau", "Arrosage modéré",
            "Arrosage régulier", "Très humide"
        ],
        
        "Difficulté": [
            "Débutant", "Facile", "Intermédiaire", "Avancé", "Expert"
        ],
        
        "Taille": [
            "Mini (<15cm)", "Petit (15-30cm)", "Moyen (30-60cm)",
            "Grand (60-120cm)", "Très grand (>120cm)"
        ],
        
        "Toxicité": [
            "Sans danger", "Toxique", "Très toxique"
        ],
        
        "Particularités": [
            "Purifiante", "Parfumée", "Croissance rapide",
            "Plante rare", "Fragile"
        ]
    }
    
    # Créer les catégories et tags
    for category_name, tag_names in tags_data.items():
        # Créer la catégorie
        category = TagCategory(name=category_name)
        db.add(category)
        db.flush()  # Flush pour obtenir l'ID
        
        # Créer les tags
        for tag_name in tag_names:
            tag = Tag(name=tag_name, tag_category_id=category.id)
            db.add(tag)
        
        print(f"✅ {category_name}: {len(tag_names)} tags créés")
    
    db.commit()


def sync_location_tags(db: Session):
    """
    Synchronise les tags Emplacement avec les locations existantes
    Crée les tags manquants
    """
    # Récupérer la catégorie Emplacement
    location_category = db.query(TagCategory).filter(TagCategory.name == "Emplacement").first()
    if not location_category:
        return  # Catégorie n'existe pas encore
    
    # Récupérer les locations et les tags Emplacement existants
    locations = db.query(Location).all()
    existing_tags = db.query(Tag).filter(Tag.tag_category_id == location_category.id).all()
    existing_tag_names = {tag.name for tag in existing_tags}
    
    # Créer les tags manquants
    new_tags_count = 0
    for location in locations:
        if location.name not in existing_tag_names:
            tag = Tag(name=location.name, tag_category_id=location_category.id)
            db.add(tag)
            new_tags_count += 1
            print(f"  ➕ Tag Emplacement créé: {location.name}")
    
    if new_tags_count > 0:
        db.commit()
        print(f"✅ {new_tags_count} tags Emplacement synchronisés")


def sync_light_requirement_tags(db: Session):
    """
    Synchronise les tags Luminosité avec les light requirements existantes
    Crée les tags manquants
    """
    # Récupérer la catégorie Luminosité
    light_category = db.query(TagCategory).filter(TagCategory.name == "Luminosité").first()
    if not light_category:
        return  # Catégorie n'existe pas encore
    
    # Récupérer les light requirements et les tags Luminosité existants
    light_reqs = db.query(LightRequirement).all()
    existing_tags = db.query(Tag).filter(Tag.tag_category_id == light_category.id).all()
    existing_tag_names = {tag.name for tag in existing_tags}
    
    # Créer les tags manquants
    new_tags_count = 0
    for light_req in light_reqs:
        if light_req.name not in existing_tag_names:
            tag = Tag(name=light_req.name, tag_category_id=light_category.id)
            db.add(tag)
            new_tags_count += 1
            print(f"  ➕ Tag Luminosité créé: {light_req.name}")
    
    if new_tags_count > 0:
        db.commit()
        print(f"✅ {new_tags_count} tags Luminosité synchronisés")
    
    # Vérification
    total_categories = db.query(TagCategory).count()
    total_tags = db.query(Tag).count()
    
    print(f"\n✨ Seed terminé!")
    print(f"   • {total_categories} catégories créées (3 auto + 6 manuelles)")
    print(f"   • {total_tags} tags créés")

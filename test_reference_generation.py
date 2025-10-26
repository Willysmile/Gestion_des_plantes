#!/usr/bin/env python3
"""
Test pour Reference Generation
Vérifie la génération de références au format FAMILY-NNN
"""

import sys
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.plant import Plant
from app.models.base import BaseModel
from app.services.plant_service import PlantService

# Créer une DB de test en mémoire
engine = create_engine('sqlite:///:memory:')
BaseModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

print("=" * 60)
print("TEST: Reference Generation")
print("=" * 60)

# Test 1: Générer une référence pour la première plante
try:
    ref1 = PlantService.generate_reference(db, "Araceae")
    print(f"✅ Test 1 - Première référence: {ref1}")
    assert ref1 == "ARACE-001", f"Expected ARACE-001, got {ref1}"
except Exception as e:
    print(f"❌ Test 1 FAILED: {e}")
    sys.exit(1)

# Test 2: Créer une plante avec la référence générée
try:
    from app.schemas.plant_schema import PlantCreate
    plant_data = PlantCreate(
        name="Test Plant 1",
        genus="Test",
        species="test",
        family="Araceae",
        reference=ref1
    )
    plant1 = PlantService.create(db, plant_data)
    print(f"✅ Test 2 - Plante créée avec référence: {plant1.reference}")
    assert plant1.reference == "ARACE-001"
except Exception as e:
    print(f"❌ Test 2 FAILED: {e}")
    sys.exit(1)

# Test 3: Générer une deuxième référence pour la même famille
try:
    ref2 = PlantService.generate_reference(db, "Araceae")
    print(f"✅ Test 3 - Deuxième référence (même famille): {ref2}")
    assert ref2 == "ARACE-002", f"Expected ARACE-002, got {ref2}"
except Exception as e:
    print(f"❌ Test 3 FAILED: {e}")
    sys.exit(1)

# Test 4: Créer une plante avec la nouvelle référence
try:
    plant_data2 = PlantCreate(
        name="Test Plant 2",
        genus="Test",
        species="test2",
        family="Araceae",
        reference=ref2
    )
    plant2 = PlantService.create(db, plant_data2)
    print(f"✅ Test 4 - Deuxième plante créée: {plant2.reference}")
    assert plant2.reference == "ARACE-002"
except Exception as e:
    print(f"❌ Test 4 FAILED: {e}")
    sys.exit(1)

# Test 5: Tester avec une autre famille
try:
    ref3 = PlantService.generate_reference(db, "Phalaenopsidaceae")
    print(f"✅ Test 5 - Référence nouvelle famille: {ref3}")
    assert ref3 == "PHALA-001", f"Expected PHALA-001, got {ref3}"
except Exception as e:
    print(f"❌ Test 5 FAILED: {e}")
    sys.exit(1)

# Test 6: Auto-génération de nom scientifique
try:
    plant_data3 = PlantCreate(
        name="Orchidée",
        genus="Phalaenopsis",
        species="amabilis",
        family="Orchidaceae"
    )
    plant3 = PlantService.create(db, plant_data3)
    print(f"✅ Test 6 - Auto-génération scientific_name: {plant3.scientific_name}")
    assert plant3.scientific_name == "Phalaenopsis amabilis"
    print(f"   Auto-génération reference: {plant3.reference}")
    assert plant3.reference == "ORCHI-001"
except Exception as e:
    print(f"❌ Test 6 FAILED: {e}")
    sys.exit(1)

# Test 7: Vérifier l'immuabilité de la référence
try:
    from app.schemas.plant_schema import PlantUpdate
    update_data = PlantUpdate(name="Updated Name", reference="ARA-999")
    updated = PlantService.update(db, plant1.id, update_data)
    print(f"❌ Test 7 FAILED: Reference devrait être immuable!")
    sys.exit(1)
except Exception as e:
    if "ne peut pas être modifiée" in str(e):
        print(f"✅ Test 7 - Immuabilité référence validée: {str(e)}")
    else:
        print(f"❌ Test 7 FAILED: Erreur inattendue: {e}")
        sys.exit(1)

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS RÉUSSIS!")
print("=" * 60)

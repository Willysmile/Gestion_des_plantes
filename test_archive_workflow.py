#!/usr/bin/env python3
"""
Test pour Archive/Restore workflow
Vérifie l'archivage complet avec timestamps et raison
"""

import sys
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models.plant import Plant
from app.models.base import BaseModel
from app.services.plant_service import PlantService
from app.schemas.plant_schema import PlantCreate

# Créer une DB de test en mémoire
engine = create_engine('sqlite:///:memory:')
BaseModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

print("=" * 60)
print("TEST: Archive/Restore Workflow")
print("=" * 60)

# Créer une plante de test
try:
    plant_data = PlantCreate(
        name="Test Plant",
        genus="Test",
        species="test",
        family="Testaceae"
    )
    plant = PlantService.create(db, plant_data)
    print(f"✅ Test 1 - Plante créée: {plant.name} (ID: {plant.id})")
    assert plant.is_archived == False
    assert plant.archived_date is None
    assert plant.archived_reason is None
except Exception as e:
    print(f"❌ Test 1 FAILED: {e}")
    sys.exit(1)

# Test 2: Archiver la plante avec raison
try:
    archived_plant = PlantService.archive(db, plant.id, reason="Plante morte")
    print(f"✅ Test 2 - Plante archivée")
    assert archived_plant.is_archived == True
    assert archived_plant.archived_date is not None
    assert archived_plant.archived_reason == "Plante morte"
    archived_date = archived_plant.archived_date
    print(f"   - archived_date: {archived_date}")
    print(f"   - archived_reason: {archived_plant.archived_reason}")
except Exception as e:
    print(f"❌ Test 2 FAILED: {e}")
    sys.exit(1)

# Test 3: Vérifier que la date n'est pas modifiée
try:
    plant_reloaded = PlantService.get_by_id(db, plant.id)
    print(f"✅ Test 3 - Plante rechargée de la BD")
    assert plant_reloaded.is_archived == True
    assert plant_reloaded.archived_date == archived_date
    assert plant_reloaded.archived_reason == "Plante morte"
except Exception as e:
    print(f"❌ Test 3 FAILED: {e}")
    sys.exit(1)

# Test 4: Restaurer la plante
try:
    restored_plant = PlantService.restore(db, plant.id)
    print(f"✅ Test 4 - Plante restaurée")
    assert restored_plant.is_archived == False
    assert restored_plant.archived_date is None
    assert restored_plant.archived_reason is None
    print(f"   - is_archived: {restored_plant.is_archived}")
    print(f"   - archived_date: {restored_plant.archived_date}")
    print(f"   - archived_reason: {restored_plant.archived_reason}")
except Exception as e:
    print(f"❌ Test 4 FAILED: {e}")
    sys.exit(1)

# Test 5: Vérifier l'immuabilité de archived_date
try:
    from app.schemas.plant_schema import PlantUpdate
    # Essayer d'archiver à nouveau, puis modifier archived_date
    archived_plant2 = PlantService.archive(db, plant.id, reason="Raison 2")
    date_before = archived_plant2.archived_date
    
    # Essayer de mettre à jour (devrait échouer si archived_date dans update_data)
    update_data = PlantUpdate(name="New Name")
    updated = PlantService.update(db, plant.id, update_data)
    
    print(f"✅ Test 5 - Immuabilité archived_date respectée")
    assert updated.archived_date == date_before
    print(f"   - archived_date inchangée: {updated.archived_date}")
except Exception as e:
    print(f"❌ Test 5 FAILED: {e}")
    sys.exit(1)

# Test 6: Archivage sans raison
try:
    plant2_data = PlantCreate(
        name="Test Plant 2",
        family="TestFamily"
    )
    plant2 = PlantService.create(db, plant2_data)
    archived_plant3 = PlantService.archive(db, plant2.id)  # Sans raison
    
    print(f"✅ Test 6 - Archivage sans raison")
    assert archived_plant3.is_archived == True
    assert archived_plant3.archived_date is not None
    assert archived_plant3.archived_reason is None
    print(f"   - archived_reason: {archived_plant3.archived_reason}")
except Exception as e:
    print(f"❌ Test 6 FAILED: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS D'ARCHIVAGE RÉUSSIS!")
print("=" * 60)

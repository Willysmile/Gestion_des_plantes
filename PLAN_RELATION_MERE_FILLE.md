# 📋 Plan: Relation Mère/Fille pour Boutures

## 🎯 Objectif Simple

**Permettre de tracker les générations de plantes:**
```
Monstera (original #1) ← mère
├─ Bouture #2 (2024-10) ← fille
├─ Bouture #3 (2024-12) ← fille
└─ Bouture #4 (2025-01) ← fille
```

---

## � Types de Propagation Supportés

### **4 Méthodes Principales**

```python
source_type: "cutting"      # Bouture (tige + feuilles)
             "seeds"        # Graines (reproduction sexuée)
             "division"     # Division (séparer plant multi-tiges)
             "offset"       # Rejeton (petite plante détachée)

method:      "water"        # Eau (bouteille verre)
             "soil"         # Terreau
             "air-layer"    # Marcottage aérien
             "substrate"    # Substrat spécialisé
             "tissue"       # Culture de tissus (avancé)
```

### **Exemples par Plante**

| Plante | Type | Méthode | Durée |
|--------|------|---------|-------|
| **Monstera** | cutting | water | 2-3 semaines |
| **Pothos** | cutting | water | 1-2 semaines |
| **Snake Plant** | division | soil | immédiat |
| **Peperomia** | offset | soil | 1-2 semaines |
| **Calathea** | division | soil | 1-2 semaines |
| **Hoya** | cutting + air-layer | soil | 4-6 semaines |
| **Succulente** | leaf cutting | soil | 3-4 semaines |
| **Orchidée** | tissue | substrate | 2-3 mois |

---

## 🌱 Cycle de Vie d'une Bouture

```
1. SOURCE (Mère)
   └─ Monstera #1 (originale)
   
2. HARVEST (Prélèvement)
   └─ Date: 1er Nov 2025
   └─ Type: cutting (tige)
   └─ Size: 3 feuilles, 4 pouces
   
3. PROPAGATION (En cours)
   └─ Method: water
   └─ Status: rooting
   └─ Days passed: 2
   
4. TIMELINE
   Day 0:   "Prélevée, mise en eau"
   Day 3:   "Roots apparentes (3mm)"
   Day 7:   "Roots bien formées (1cm)"
   Day 10:  "Nouvelle feuille"
   Day 14:  "Ready-to-pot (roots 2cm)"
   
5. CONVERSION
   └─ Plant #2 créée
   └─ Rempoté en substrat
   └─ Status: "Plante indépendante"
   
6. RESULT
   └─ Success: ✅ (potted)
   ou
   └─ Failed: ❌ (no roots, rot)
```

---

## 🏗️ Architecture (2 Options)

### **Option A: Minimal (1 colonne)**

Ajouter `parent_plant_id` à PLANTS table.

**Pros:** Simple (1-2h), relation directe
**Cons:** Pas de métadonnées

---

### **Option B: Complète (2 tables)** ⭐ RECOMMANDÉ

**Table 1: PlantCutting**
```sql
CREATE TABLE plant_cuttings (
    id INTEGER PRIMARY KEY,
    parent_plant_id INTEGER NOT NULL,
    source_type VARCHAR(50),      -- "cutting", "seeds", "division", "offset"
    method VARCHAR(50),            -- "water", "soil", "air-layer", "substrate"
    date_harvested DATETIME,
    expected_ready DATETIME,
    status VARCHAR(50),            -- "rooting", "growing", "ready-to-pot", "potted"
    notes TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (parent_plant_id) REFERENCES plants(id)
);
```

**Table 2: CuttingHistory**
```sql
CREATE TABLE cutting_history (
    id INTEGER PRIMARY KEY,
    cutting_id INTEGER NOT NULL,
    date DATETIME,
    event VARCHAR(50),             -- "rooted", "leaves-grown", "ready-to-pot"
    measurement JSON,              -- {root_length_cm: 1.5, leaves: 3}
    notes TEXT,
    created_at DATETIME,
    FOREIGN KEY (cutting_id) REFERENCES plant_cuttings(id)
);
```

**Pros:** 
- ✅ Support 4 types propagation + 4 méthodes
- ✅ Timeline complète (rooting → potted)
- ✅ Success rate tracking
- ✅ Estimateur de date prête

**Cons:** 3.5-4 heures

---

## 💾 Plan d'Implémentation

### **Phase 1: Database (30 min)**

**Créer migration 010:**
```bash
cd backend
alembic revision --autogenerate -m "Add plant propagation tracking"
# Edit: migration file pour ajouter colonnes/tables
alembic upgrade head
```

**Schéma:**
```sql
-- Option B: Complet (Recommandé)
CREATE TABLE plant_cuttings (
    id INTEGER PRIMARY KEY,
    parent_plant_id INTEGER NOT NULL,
    source_type VARCHAR(50),
    method VARCHAR(50),
    date_harvested DATETIME,
    status VARCHAR(50),
    notes TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (parent_plant_id) REFERENCES plants(id)
);

CREATE TABLE cutting_history (
    id INTEGER PRIMARY KEY,
    cutting_id INTEGER NOT NULL,
    date DATETIME,
    event VARCHAR(50),
    measurement JSON,
    notes TEXT,
    created_at DATETIME,
    FOREIGN KEY (cutting_id) REFERENCES plant_cuttings(id)
);
```

---

### **Phase 2: Models (30 min)**

**File: `backend/app/models/propagation.py` (nouveau)**

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class PlantCutting(BaseModel):
    __tablename__ = "plant_cuttings"
    
    parent_plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    source_type = Column(String(50))      # "cutting", "seeds", "division", "offset"
    method = Column(String(50))           # "water", "soil", "air-layer", "substrate"
    date_harvested = Column(DateTime)
    expected_ready = Column(DateTime)     # Estimé: quand sera prête
    status = Column(String(50))           # "rooting", "growing", "ready-to-pot", "potted", "failed"
    notes = Column(Text)
    
    # Relationships
    parent_plant = relationship("Plant", backref="cuttings")
    history = relationship("CuttingHistory", cascade="all, delete-orphan")

class CuttingHistory(BaseModel):
    __tablename__ = "cutting_history"
    
    cutting_id = Column(Integer, ForeignKey('plant_cuttings.id'), nullable=False)
    date = Column(DateTime)
    event = Column(String(50))            # "rooted", "leaves-grown", "ready-to-pot"
    measurement = Column(JSON)            # {root_length_cm: 1.5, leaves: 3}
    notes = Column(Text)
    
    # Relationships
    cutting = relationship("PlantCutting", backref="events")
```

---

### **Phase 3: API Endpoints (1 heure)**

**File: `backend/app/routes/propagation.py` (nouveau)**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix="/api/plants", tags=["propagation"])

# Get all cuttings from a parent plant
@router.get("/{plant_id}/cuttings")
async def get_cuttings(plant_id: int, db: Session = Depends(get_db)):
    """Récupère toutes les boutures d'une plante mère"""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    cuttings = db.query(PlantCutting).filter(PlantCutting.parent_plant_id == plant_id).all()
    return cuttings

# Create a cutting
@router.post("/{plant_id}/cuttings")
async def create_cutting(plant_id: int, data: dict, db: Session = Depends(get_db)):
    """Crée une nouvelle bouture de la plante"""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    cutting = PlantCutting(
        parent_plant_id=plant_id,
        source_type=data.get("source_type", "cutting"),
        method=data.get("method", "water"),
        date_harvested=datetime.now(),
        status="rooting",
        notes=data.get("notes", "")
    )
    db.add(cutting)
    db.commit()
    return cutting

# Log cutting progress
@router.post("/cuttings/{cutting_id}/progress")
async def log_progress(cutting_id: int, data: dict, db: Session = Depends(get_db)):
    """Enregistre la progression d'une bouture"""
    cutting = db.query(PlantCutting).filter(PlantCutting.id == cutting_id).first()
    if not cutting:
        raise HTTPException(status_code=404, detail="Bouture non trouvée")
    
    history = CuttingHistory(
        cutting_id=cutting_id,
        date=datetime.now(),
        event=data.get("event"),
        measurement=data.get("measurement"),
        notes=data.get("notes", "")
    )
    db.add(history)
    
    # Update cutting status
    cutting.status = data.get("status", cutting.status)
    
    db.commit()
    return history

# Get family tree
@router.get("/{plant_id}/family-tree")
async def get_family_tree(plant_id: int, db: Session = Depends(get_db)):
    """Récupère l'arbre généalogique d'une plante"""
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plante non trouvée")
    
    # Find all ancestors
    ancestors = []
    current = plant
    while current.parent_plant_id:  # Si Option A
        parent = db.query(Plant).filter(Plant.id == current.parent_plant_id).first()
        if parent:
            ancestors.append(parent)
            current = parent
    
    # Find all descendants
    def get_descendants(plant_id):
        children = db.query(Plant).filter(Plant.parent_plant_id == plant_id).all()
        result = list(children)
        for child in children:
            result.extend(get_descendants(child.id))
        return result
    
    descendants = get_descendants(plant_id)
    
    return {
        "plant": plant,
        "ancestors": ancestors,
        "descendants": descendants,
        "cuttings": [{"id": c.id, "status": c.status, "date": c.date_harvested} for c in plant.cuttings]
    }
```

---

### **Phase 4: Services (30 min)**

**File: `backend/app/services/propagation_service.py` (nouveau)**

```python
class PropagationService:
    """Service pour gérer la propagation des plantes"""
    
    @staticmethod
    def get_success_rate(plant_id: int, db: Session) -> dict:
        """Calcule le taux de succès des boutures"""
        cuttings = db.query(PlantCutting).filter(
            PlantCutting.parent_plant_id == plant_id
        ).all()
        
        if not cuttings:
            return {"total": 0, "success_rate": 0, "details": {}}
        
        total = len(cuttings)
        potted = len([c for c in cuttings if c.status == "potted"])
        failed = len([c for c in cuttings if c.status == "failed"])
        
        success_rate = (potted / total * 100) if total > 0 else 0
        
        return {
            "total_cuttings": total,
            "success_rate": f"{success_rate:.1f}%",
            "potted": potted,
            "failed": failed,
            "in_progress": total - potted - failed
        }
    
    @staticmethod
    def convert_cutting_to_plant(cutting_id: int, plant_name: str, db: Session):
        """Convertit une bouture en plante indépendante"""
        cutting = db.query(PlantCutting).filter(PlantCutting.id == cutting_id).first()
        if not cutting:
            return False, "Bouture non trouvée"
        
        if cutting.status != "potted":
            return False, "Bouture doit être 'potted' avant conversion"
        
        parent = db.query(Plant).filter(Plant.id == cutting.parent_plant_id).first()
        
        # Créer une nouvelle plante
        new_plant = Plant(
            name=plant_name,
            parent_plant_id=cutting.parent_plant_id,  # Link genealogy
            # Copy parent's settings
            is_indoor=parent.is_indoor,
            is_outdoor=parent.is_outdoor,
            location_id=parent.location_id,
            # ... other fields
        )
        db.add(new_plant)
        db.commit()
        
        cutting.status = "converted"
        db.commit()
        
        return True, new_plant.id
```

---

### **Phase 5: Tests (1 heure)**

**File: `backend/tests/test_propagation.py` (nouveau)**

```python
import pytest
from app.models.propagation import PlantCutting, CuttingHistory
from app.models.plant import Plant

def test_create_cutting(client, db):
    # Create parent plant
    plant = Plant(name="Monstera", is_indoor=True)
    db.add(plant)
    db.commit()
    
    # Create cutting
    response = client.post(f"/api/plants/{plant.id}/cuttings", json={
        "source_type": "cutting",
        "method": "water",
        "notes": "3 leaves"
    })
    assert response.status_code == 201
    cutting = response.json()
    assert cutting["parent_plant_id"] == plant.id

def test_log_progress(client, db, cutting):
    response = client.post(f"/api/cuttings/{cutting.id}/progress", json={
        "event": "rooted",
        "measurement": {"root_length_cm": 1.5},
        "status": "growing"
    })
    assert response.status_code == 201

def test_family_tree(client, db):
    # Create family
    parent = Plant(name="Monstera")
    child1 = Plant(name="Monstera-1", parent_plant_id=parent.id)
    child2 = Plant(name="Monstera-2", parent_plant_id=parent.id)
    
    response = client.get(f"/api/plants/{parent.id}/family-tree")
    assert response.status_code == 200
    family = response.json()
    assert len(family["descendants"]) == 2

def test_success_rate(client, db):
    response = client.get(f"/api/plants/{plant.id}/success-rate")
    assert response.status_code == 200
    stats = response.json()
    assert "success_rate" in stats
```

---

## 📅 Timeline

```
Phase 1 (Database):         30 min
Phase 2 (Models):           30 min
Phase 3 (API):              1 heure
Phase 4 (Services):         30 min
Phase 5 (Tests):            1 heure
────────────────────────────────
TOTAL:                       3.5 heures
```

---

## 🎯 Étapes à Faire (dans l'ordre)

### **Step 1: Choose Architecture**
- [ ] Décider entre Option A (simple) vs Option B (complète)
- [ ] ➡️ **Je recommande Option B** (juste 1h de plus, beaucoup mieux)

### **Step 2: Create Migration**
```bash
# Générer migration
alembic revision --autogenerate -m "Add plant propagation"

# Éditer le fichier migration pour ajouter tables/colonnes
# Appliquer
alembic upgrade head
```

### **Step 3: Add Models**
- [ ] Créer `backend/app/models/propagation.py`
- [ ] Ajouter `PlantCutting` et `CuttingHistory` classes
- [ ] Ajouter relation dans `Plant` model

### **Step 4: Add API Routes**
- [ ] Créer `backend/app/routes/propagation.py`
- [ ] Implémenter 5 endpoints (GET cuttings, POST cutting, LOG progress, GET family-tree, GET success-rate)
- [ ] Ajouter router à `main.py`

### **Step 5: Add Service Logic**
- [ ] Créer `backend/app/services/propagation_service.py`
- [ ] Implémenter `success_rate()` et `convert_cutting_to_plant()`

### **Step 6: Add Tests**
- [ ] Créer `backend/tests/test_propagation.py`
- [ ] 5+ tests cases

### **Step 7: Update Frontend** (optionnel maintenant)
- [ ] Ajouter UI pour voir cuttings
- [ ] Timeline visuelle
- [ ] Bouton "Convert to plant"

---

## 🚀 Endpoints Finaux

```
GET    /api/plants/{id}/cuttings              → Liste boutures
POST   /api/plants/{id}/cuttings              → Créer bouture
POST   /api/cuttings/{id}/progress            → Logger progression
GET    /api/plants/{id}/family-tree           → Arbre généalogique
GET    /api/plants/{id}/success-rate          → Taux de succès
DELETE /api/cuttings/{id}                     → Supprimer bouture
```

---

## ✅ Résultat Final

```python
# Après implémentation:

# 1. Créer une bouture
POST /api/plants/1/cuttings
{
  "source_type": "cutting",
  "method": "water",
  "notes": "Prélevée le 1er nov"
}
# → Created cutting #42

# 2. Logger progression
POST /api/cuttings/42/progress
{
  "event": "rooted",
  "measurement": {"root_length_cm": 1.5},
  "status": "growing"
}

# 3. Voir l'arbre
GET /api/plants/1/family-tree
# → {
#     "plant": {...},
#     "ancestors": [],
#     "descendants": [Cutting #42 details],
#     "cuttings": [...]
#   }

# 4. Stats
GET /api/plants/1/success-rate
# → {"total_cuttings": 3, "success_rate": "66.7%", "potted": 2, "failed": 1}
```

---

## 🎓 Questions Avant de Coder?

1. **Option A ou B?** → Je recommande **Option B** (plus complet)
2. **Veux-tu faire le frontend aussi?** → Peux attendre après
3. **Veux-tu des notifications?** → Optionnel pour Phase 2
4. **Veux-tu des migrations reversible?** → Oui (Alembic)

**Ready to code? 🚀**


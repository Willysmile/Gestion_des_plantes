# 📋 Plan: Relation Mère/Fille/Soeur pour Propagation

**📖 Voir aussi:** [`RECAP_FEATURE_PROPAGATION.md`](RECAP_FEATURE_PROPAGATION.md) pour le recap complet

## 🎯 Objectif Simple

**Permettre de tracker les générations de plantes avec source & méthode:**
```
Monstera (original #1) ← MÈRE
│
├─ Bouture #2 (Oct 2024) ← FILLE 1 (cutting + water, 2-3 sem)
│  └─ Soeur: Bouture #3
│
└─ Bouture #3 (Oct 2024) ← FILLE 2 (cutting + water, 2-3 sem)
   └─ Soeur: Bouture #2
   
Relations:
✅ #2 et #3 = SOEURS (même mère, même jour)
✅ #1 = MÈRE de #2 et #3
✅ #2/#3 peuvent devenir MÈRES à leur tour
```

---

## 🔗 Types de Propagation Supportés

### **4 Types de Relations**

```
MÈRE:   Plante source originale
        ├─ Peut générer N enfants (filles)
        ├─ Peut devenir fille d'une autre (si elle-même issue de bouture)
        └─ Exemple: Monstera achetée en 2020

FILLE:  Issue directe d'une mère
        ├─ Via: cutting, seeds, division, offset
        ├─ Via: water, soil, air-layer, substrate
        ├─ Peut devenir mère à son tour
        └─ Exemple: Bouture prélevée Oct 2024

SOEUR:  Partage la même mère
        ├─ Peut être du même jour (lancée ensemble)
        ├─ Peut être de jours différents (même source, jours différents)
        ├─ Même ou différentes méthodes
        └─ Exemple: 3 boutures du Monstera en même temps

PETITE-FILLE: Enfant d'une fille
        ├─ Exemple: Bouture d'une bouture
        └─ Arbre généalogique sur 3+ générations
```

### **4 Sources de Propagation**

```python
source_type: "cutting"      # Bouture (tige + feuilles) - PLUS COURANT
             "seeds"        # Graines (reproduction sexuée)
             "division"     # Division (séparer plant multi-tiges)
             "offset"       # Rejeton (petite plante détachée)
```

### **4 Méthodes de Culture**

```python
method:      "water"        # Eau (bouteille verre) - PLUS RAPIDE
             "soil"         # Terreau
             "air-layer"    # Marcottage aérien
             "substrate"    # Substrat spécialisé
```

### **Matrice: Source × Méthode (Optimale)**

| Source | Water | Soil | Air-layer | Substrate |
|--------|-------|------|-----------|-----------|
| **cutting** | ✅✅ 2-3 sem | ✅ 3-4 sem | ✅ 4-6 sem | ✅ 2-4 sem |
| **seeds** | ❌ rare | ✅ 1-2 mois | ❌ non | ✅ 1-2 mois |
| **division** | ⚠️ possible | ✅✅ immédiat | ❌ non | ⚠️ possible |
| **offset** | ⚠️ possible | ✅✅ 1-2 sem | ❌ non | ✅ 1-2 sem |

✅✅ = Optimal | ✅ = Bon | ⚠️ = Possible | ❌ = Rare

### **Exemples Réels par Plante**

| Plante | Type | Méthode | Durée |
|--------|------|---------|-------|
| **Monstera** | cutting | water | ✅✅ 2-3 sem | Ultra rapide |
| **Pothos** | cutting | water | ✅✅ 1-2 sem | Le plus rapide |
| **Snake Plant** | division | soil | ✅✅ immédiat | Instant |
| **Peperomia** | offset | soil | ✅✅ 1-2 sem | Rejets naturels |
| **Calathea** | division | soil | ✅ 1-2 sem | Séparer tiges |
| **Hoya** | cutting | air-layer | ✅ 4-6 sem | Pour branches épaisses |
| **Succulente** | leaf cutting | soil | ✅ 3-4 sem | Feuille seule |
| **Orchidée** | tissue | substrate | ⚠️ 2-3 mois | Avancé |

---

## 🌱 3 Niveaux de Données pour Tracker Propagation

### **Niveau 1: Relation Simple (Parent-Child)**
```
Colonne ajoutée à PLANTS:
├─ parent_plant_id ← FK vers plants(id)
├─ Permet: "Voir la mère", "Voir les enfants", "Arbre complet"
└─ Exemple: Monstera #2.parent_plant_id = 1 (mère)

Accès rapide:
- Voir tous les enfants d'une mère
- Voir la mère d'une plante
- Générer l'arbre généalogique
```

### **Niveau 2: Métadonnées de Bouture (PlantCuttings table)**
```
Nouvelle table PLANT_CUTTINGS:
├─ id
├─ parent_plant_id ← FK plants(id) [LA MÈRE]
├─ source_type ← "cutting", "seeds", "division", "offset"
├─ method ← "water", "soil", "air-layer", "substrate"
├─ date_harvested ← Quand prélevée (1er Nov 2025)
├─ expected_ready ← Quand prête (auto-calculé: date_harvested + durée)
├─ status ← "rooting", "growing", "ready-to-pot", "potted", "failed"
├─ notes ← Texte libre
└─ success_rate_estimate ← % selon type + méthode

Accès:
- Quelle source et méthode utilisées?
- Quand sera-t-elle prête? (estimateur)
- Quel est le statut actuel?
- Quel taux de succès pour ce type/méthode?
```

### **Niveau 3: Timeline Complète (CuttingHistory table)**
```
Nouvelle table CUTTING_HISTORY:
├─ id
├─ cutting_id ← FK plant_cuttings(id) [QUE TRACKER]
├─ date ← Quand cet événement?
├─ event ← "rooted", "leaves-grown", "ready-to-pot", "potted", "failed"
├─ measurement ← JSON: {root_length_cm: 1.5, leaves: 3, roots: 4}
├─ notes ← "Première racine visible!"
└─ [photos] ← Intégrées à chaque étape

Timeline exemple:
Day 0 (Nov 1):   "Bouture prélevée"
Day 3 (Nov 4):   "Racines apparentes (3mm)"
Day 7 (Nov 8):   "Racines bien formées (1.2cm)"
Day 10 (Nov 11): "Nouvelle feuille!"
Day 14 (Nov 15): "READY-TO-POT (roots 2cm)"
Day 21 (Nov 22): "Rempoté en substrat"

Accès:
- Voir chaque étape jour par jour
- Photos de chaque étape
- Mesures précises (root_length, leaves, roots)
- Notes et observations
- Détecter problèmes (pas de racines après 10j?)
- Apprendre des patterns
```

---

## 🏗️ Architecture Complète (Option B Recommandée)

### **Changement à PLANTS Table**
```sql
ALTER TABLE plants ADD COLUMN parent_plant_id INTEGER;
ALTER TABLE plants ADD FOREIGN KEY (parent_plant_id) REFERENCES plants(id);

-- nullable: une plante peut être une mère originale (pas de parent)
```

### **Nouvelle Table 1: PLANT_CUTTINGS**
```sql
CREATE TABLE plant_cuttings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_plant_id INTEGER NOT NULL,          -- FK vers plants(id) [LA MÈRE]
    source_type VARCHAR(50) NOT NULL,          -- "cutting", "seeds", "division", "offset"
    method VARCHAR(50) NOT NULL,               -- "water", "soil", "air-layer", "substrate"
    date_harvested DATETIME NOT NULL,          -- Quand prélevée
    expected_ready DATETIME,                   -- Quand prête (auto-calculé)
    status VARCHAR(50) DEFAULT 'rooting',      -- rooting, growing, ready-to-pot, potted, failed
    success_rate_estimate FLOAT DEFAULT 0.85,  -- % estimé selon type+method
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_plant_id) REFERENCES plants(id) ON DELETE CASCADE
);
```

### **Nouvelle Table 2: CUTTING_HISTORY**
```sql
CREATE TABLE cutting_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cutting_id INTEGER NOT NULL,               -- FK vers plant_cuttings(id)
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event VARCHAR(50) NOT NULL,                -- "rooted", "leaves-grown", "ready-to-pot", "potted", "failed"
    measurement JSON,                          -- {root_length_cm: 1.5, leaves: 3, roots: 4, health: "good"}
    notes TEXT,                                -- Observation libre
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cutting_id) REFERENCES plant_cuttings(id) ON DELETE CASCADE
);
```

**Exemple de données:**
```sql
-- Monstera originale (mère)
INSERT INTO plants (name, scientific_name, parent_plant_id, ...) 
VALUES ('Monstera Deliciosa', 'Monstera deliciosa', NULL, ...);  -- id = 1

-- Bouture #1 lancée 1er Nov
INSERT INTO plant_cuttings (parent_plant_id, source_type, method, date_harvested, expected_ready, status, notes)
VALUES (1, 'cutting', 'water', '2025-11-01', '2025-11-18', 'rooting', 'Tige 3 feuilles');  -- id = 100

-- Timeline de la bouture
INSERT INTO cutting_history (cutting_id, date, event, measurement, notes)
VALUES (100, '2025-11-01', 'rooted', '{}', 'Mise en eau');
VALUES (100, '2025-11-04', 'rooted', '{"root_length_cm": 0.3}', 'Première racine!');
VALUES (100, '2025-11-08', 'rooted', '{"root_length_cm": 1.2, "roots": 4}', 'Racines bien formées');
VALUES (100, '2025-11-15', 'ready-to-pot', '{"root_length_cm": 2.0, "roots": 5}', 'PRÊTE!');
```

---

## 💾 Plan d'Implémentation Détaillé

### **Phase 1: Database (30-45 min)**

**Créer migration 010:**
```bash
cd backend
alembic revision --autogenerate -m "Add plant propagation tracking (parent_plant_id + cuttings + history)"
```

**À éditer dans le fichier migration:**
- Ajouter colonne parent_plant_id à plants
- Créer table plant_cuttings (12 colonnes)
- Créer table cutting_history (7 colonnes)
- Ajouter indices sur parent_plant_id, cutting_id, status

**Vérifier:**
```bash
alembic upgrade head  # Appliquer migration
```

---

### **Phase 2: Models (30-45 min)**

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


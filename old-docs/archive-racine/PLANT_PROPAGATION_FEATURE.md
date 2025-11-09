# 🌱 Gestion Mère/Fille - Division & Propagation

## 📋 Contexte

La table `plant_propagations` existait dans le cahier des charges Laravel original mais n'a pas été implémentée dans la version Python/FastAPI actuelle.

Cette feature permettrait de **tracker les relations parent-enfant** entre plantes (divisions, boutures, propagations).

---

## 🎯 Cas d'Usage

### Exemple 1: Division d'une Monstera
```
Plant Mère: Monstera #1 (ID: 5)
  ├─ Créée le 15/10/2023
  ├─ Arrosée régulièrement
  └─ Divisée le 01/11/2025

Plant Enfant 1: Monstera #1-A (ID: 15)
  ├─ Créée par division
  ├─ Parent: Monstera #1
  ├─ Date division: 01/11/2025
  └─ Nombre pousses: 2

Plant Enfant 2: Monstera #1-B (ID: 16)
  ├─ Créée par division
  ├─ Parent: Monstera #1
  ├─ Date division: 01/11/2025
  └─ Nombre pousses: 1
```

### Exemple 2: Bouture d'une Chaîne des Cœurs
```
Plant Mère: String of Hearts (ID: 3)
  └─ Boutures prélevées: 3 (01/11/2025)

Plant Enfant 1: String of Hearts (Bouture 1) (ID: 12)
  ├─ Créée par bouture
  ├─ Parent: String of Hearts
  ├─ Date bouture: 01/11/2025
  └─ État: En enracinement (eau)
```

### Exemple 3: Tracking Généalogique
```
Monstera deliciosa (Grand-mère)
  ├─ Enfant 1 (Mère): Division 2020
  │   ├─ Petit-enfant 1A: Division 2023
  │   ├─ Petit-enfant 1B: Division 2023
  │   └─ Petit-enfant 1C: Bouture 2024
  └─ Enfant 2 (Mère): Bouture 2021
      ├─ Petit-enfant 2A: Division 2024
      └─ Petit-enfant 2B: Division 2024
```

---

## 🏗️ Architecture Base de Données

### Nouvelle Table: `plant_propagations`

```sql
CREATE TABLE plant_propagations (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Relation parent-enfant
  parent_plant_id     INTEGER NOT NULL,        -- Plante mère
  child_plant_id      INTEGER NOT NULL,        -- Plante enfant
  
  -- Type de propagation
  propagation_type    VARCHAR(50) NOT NULL,    -- 'division', 'bouture', 'semis', 'marcottage', 'autre'
  
  -- Dates
  propagation_date    DATE NOT NULL,           -- Date de la division/bouture
  success_date        DATE,                    -- Date enracinement/succès (NULL si en cours)
  
  -- Détails
  notes               TEXT,                    -- Notes libres
  quantity            INTEGER DEFAULT 1,       -- Nombre de plantes créées
  propagation_method  VARCHAR(255),            -- Ex: "Division", "Bouture air", "Bouture eau"
  
  -- Status
  status              VARCHAR(50),             -- 'pending', 'success', 'failed'
  is_active           BOOLEAN DEFAULT TRUE,    -- Suivi actif ou archivé?
  
  -- Audit
  created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY(parent_plant_id) REFERENCES plants(id) ON DELETE CASCADE,
  FOREIGN KEY(child_plant_id) REFERENCES plants(id) ON DELETE CASCADE,
  
  UNIQUE(parent_plant_id, child_plant_id),  -- Une enfant ne peut venir qu'une fois d'une mère
  CHECK(parent_plant_id != child_plant_id)  -- Pas de self-reference
);

CREATE INDEX idx_parent_plant_id ON plant_propagations(parent_plant_id);
CREATE INDEX idx_child_plant_id ON plant_propagations(child_plant_id);
CREATE INDEX idx_propagation_date ON plant_propagations(propagation_date);
```

### Colonne Supplémentaire: `plants` Table

```sql
ALTER TABLE plants ADD COLUMN parent_plant_id INTEGER REFERENCES plants(id);
ALTER TABLE plants ADD COLUMN propagation_type VARCHAR(50);  -- Type si enfant
ALTER TABLE plants ADD COLUMN propagation_date DATE;         -- Date si enfant
```

---

## 🔄 Flux de Données

### 1. **Créer une Propagation**

**Endpoint:** `POST /api/plants/{parent_id}/propagate`

**Payload:**
```json
{
  "child_plant_id": 15,
  "propagation_type": "division",
  "propagation_date": "2025-11-01",
  "quantity": 2,
  "notes": "Divisée en 2 parties égales",
  "status": "pending"
}
```

**Response:**
```json
{
  "id": 1,
  "parent_plant_id": 5,
  "child_plant_id": 15,
  "propagation_type": "division",
  "propagation_date": "2025-11-01",
  "status": "pending",
  "created_at": "2025-11-06T10:30:00"
}
```

### 2. **Récupérer les Enfants d'une Plante**

**Endpoint:** `GET /api/plants/{id}/children`

**Response:**
```json
[
  {
    "id": 15,
    "name": "Monstera #1-A",
    "parent_plant_id": 5,
    "propagation_type": "division",
    "propagation_date": "2025-11-01",
    "status": "pending",
    "notes": "Partie 1"
  },
  {
    "id": 16,
    "name": "Monstera #1-B",
    "parent_plant_id": 5,
    "propagation_type": "division",
    "propagation_date": "2025-11-01",
    "status": "pending",
    "notes": "Partie 2"
  }
]
```

### 3. **Récupérer la Généalogie Complète**

**Endpoint:** `GET /api/plants/{id}/genealogy`

**Response:**
```json
{
  "plant": { "id": 5, "name": "Monstera #1", "parent_plant_id": null },
  "children": [
    {
      "id": 15,
      "name": "Monstera #1-A",
      "propagation_type": "division",
      "propagation_date": "2025-11-01"
    }
  ],
  "grandchildren": [
    {
      "id": 20,
      "name": "Monstera #1-A-I",
      "parent_plant_id": 15
    }
  ]
}
```

### 4. **Mettre à Jour le Statut d'une Propagation**

**Endpoint:** `PUT /api/plants/{parent_id}/propagations/{child_id}`

**Payload:**
```json
{
  "status": "success",
  "success_date": "2025-11-15",
  "notes": "Enracinement complet, en terre maintenant"
}
```

---

## 💻 Implémentation Backend

### 1. Modèle SQLAlchemy

```python
# app/models/propagation.py

from sqlalchemy import Column, Integer, String, DateTime, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class PlantPropagation(BaseModel):
    __tablename__ = "plant_propagations"
    
    parent_plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    child_plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    
    propagation_type = Column(String(50), nullable=False)  # division, bouture, semis, etc.
    propagation_date = Column(Date, nullable=False)
    success_date = Column(Date)
    
    notes = Column(Text)
    quantity = Column(Integer, default=1)
    propagation_method = Column(String(255))
    
    status = Column(String(50), default="pending")  # pending, success, failed
    is_active = Column(Boolean, default=True)
    
    # Relations
    parent_plant = relationship("Plant", foreign_keys=[parent_plant_id], backref="children_propagations")
    child_plant = relationship("Plant", foreign_keys=[child_plant_id], backref="parent_propagation")
```

### 2. Service Backend

```python
# app/services/propagation_service.py

class PropagationService:
    @staticmethod
    def create_propagation(db: Session, parent_id: int, child_id: int, data: dict):
        """Créer une relation mère-enfant"""
        propagation = PlantPropagation(
            parent_plant_id=parent_id,
            child_plant_id=child_id,
            **data
        )
        db.add(propagation)
        db.commit()
        return propagation
    
    @staticmethod
    def get_children(db: Session, plant_id: int):
        """Récupérer tous les enfants d'une plante"""
        return db.query(PlantPropagation).filter(
            PlantPropagation.parent_plant_id == plant_id,
            PlantPropagation.is_active == True
        ).all()
    
    @staticmethod
    def get_genealogy(db: Session, plant_id: int, depth: int = 3):
        """Récupérer la généalogie (parents + enfants + petit-enfants)"""
        # Implémentation recursive pour tracker toute la ligne
        pass
```

### 3. Routes FastAPI

```python
# app/routes/propagations.py

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/plants", tags=["propagations"])

@router.post("/{parent_id}/propagate")
async def create_propagation(parent_id: int, data: PropagationCreate, db: Session = Depends(get_db)):
    """Créer une propagation (division, bouture, etc.)"""
    return PropagationService.create_propagation(db, parent_id, data)

@router.get("/{plant_id}/children")
async def get_children(plant_id: int, db: Session = Depends(get_db)):
    """Récupérer tous les enfants d'une plante"""
    return PropagationService.get_children(db, plant_id)

@router.get("/{plant_id}/genealogy")
async def get_genealogy(plant_id: int, db: Session = Depends(get_db)):
    """Récupérer la généalogie complète"""
    return PropagationService.get_genealogy(db, plant_id)

@router.put("/{parent_id}/propagations/{child_id}")
async def update_propagation(parent_id: int, child_id: int, data: PropagationUpdate, db: Session = Depends(get_db)):
    """Mettre à jour le statut d'une propagation"""
    pass
```

---

## 🎨 Interface Frontend

### Vue: Page Détail Plante - Onglet "Généalogie"

```
┌─────────────────────────────────────────────────────┐
│ Monstera deliciosa (Mère)                           │
├─────────────────────────────────────────────────────┤
│ 📊 GÉNÉALOGIE                                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  👨‍👩‍👧‍👦 Parents                                         │
│  ├─ Aucun (plante originelle)                       │
│                                                     │
│  👶 Enfants (2)                                     │
│  ├─ 🌿 Monstera #1-A (ID: 15)                       │
│  │   ├─ Type: Division                              │
│  │   ├─ Date: 01/11/2025                            │
│  │   ├─ Status: ✅ Succès                            │
│  │   └─ [Voir généalogie]                           │
│  │                                                  │
│  └─ 🌿 Monstera #1-B (ID: 16)                       │
│      ├─ Type: Division                              │
│      ├─ Date: 01/11/2025                            │
│      ├─ Status: ⏳ En attente                        │
│      └─ [Voir généalogie]                           │
│                                                     │
│  👶👶 Petit-enfants (3)                              │
│  ├─ 🌿 Monstera #1-A-I                              │
│  ├─ 🌿 Monstera #1-A-II                             │
│  └─ 🌿 Monstera #1-B-I                              │
│                                                     │
│  [+ Créer une nouvelle division]                    │
│  [+ Créer une nouvelle bouture]                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Modal: Créer une Propagation

```
┌──────────────────────────────────────────┐
│ 🌱 Nouvelle Propagation                  │
├──────────────────────────────────────────┤
│                                          │
│ Mère: Monstera deliciosa                 │
│                                          │
│ Type de propagation:                     │
│ ⚪ Division                               │
│ ⚪ Bouture                                │
│ ⚪ Semis                                  │
│ ⚪ Marcottage                             │
│ ⚪ Autre                                  │
│                                          │
│ Enfant (nouvelle plante):                │
│ [📝 Sélectionner une plante existante]   │
│ OU                                       │
│ [➕ Créer une nouvelle plante]            │
│                                          │
│ Date de la propagation:                  │
│ [📅 06/11/2025]                          │
│                                          │
│ Nombre de plantes créées:                │
│ [2]                                      │
│                                          │
│ Notes:                                   │
│ [Divisée en 2 parties, enracinement OK]  │
│                                          │
│ [Annuler] [Créer propagation]            │
│                                          │
└──────────────────────────────────────────┘
```

---

## 📊 Statistiques Possibles

Une fois implémenté, on pourrait tracker:

- **Nombre total de propagations:** 15
- **Taux de succès:** 87% (13/15 réussies)
- **Types de propagation populaires:** 60% divisions, 35% boutures, 5% semis
- **Temps moyen d'enracinement:** 21 jours
- **Plante la plus propagée:** Monstera deliciosa (5 fois)
- **Clones les plus anciens:** String of Hearts (2020)

---

## ⏳ Estimation

| Phase | Temps | Notes |
|-------|-------|-------|
| Migration DB | 1-2h | Créer table, migration Alembic |
| Backend (API) | 2-3h | Models + Services + Routes |
| Frontend (UI) | 3-4h | Modal + Vue généalogie + Intégration |
| Tests | 1-2h | API tests + E2E tests |
| **Total** | **7-11h** | ~2 jours de travail |

---

## 🔄 Phase Future

### Phase 1: Implémentation MVP
- ✅ Créer relation parent-enfant simple
- ✅ Afficher enfants d'une plante
- ✅ Vue généalogie 2 niveaux

### Phase 2: Avancé
- 📊 Statistiques de propagation
- 📈 Graphiques généalogie (tree view)
- 📝 Historique modifications
- 🔔 Rappels "enracinement prévu"

### Phase 3: Intégration
- 🗓️ Calendrier avec dates de propagation
- 📤 Export généalogie (PDF/PNG)
- 🔗 Liens entre plantes (variantes, hybrides)

---

## 🎯 Priorité

**BASSE-MOYENNE** - Fonctionnalité avancée mais utile pour collectionneurs.

À implémenter **après** les futures features hautes priorités (Calendrier, Alertes, Search).

---

**Créé:** 9 Nov 2025  
**Statut:** Non implémenté  
**Type:** Feature Request

# 🔄 Comparaison: Plan Original vs Recommandations d'Amélioration

**Date:** 11 Novembre 2025  
**Documents analysés:**
- 📄 Plan original: `PLAN_FEATURE_PROPAGATION.md`
- 📊 Recommandations: `RECAP_FEATURE_PROPAGATION.md`

---

## 📊 Vue d'Ensemble

### Points de Convergence ✅
- Architecture 3 tables (plants + propagations + history)
- Support multi-générations
- Tracking temporel détaillé
- API RESTful

### Différences Majeures ⚠️
| Aspect | Plan Original | Mes Recommandations |
|--------|---------------|---------------------|
| **Focus** | Boutures/cuttings spécifique | Propagations génériques |
| **Table principale** | `plant_cuttings` | `plant_propagations` |
| **Relation parent** | `parent_plant_id` dans plants | Uniquement dans table dédiée |
| **Types supportés** | 4 types détaillés | Types + méthodes séparés |
| **Timeline** | Table `cutting_history` | États granulaires |

---

## 🔍 Analyse Détaillée par Composant

### 1. **Architecture Base de Données**

#### Plan Original (Option B)
```sql
-- Colonne dans PLANTS
ALTER TABLE plants ADD COLUMN parent_plant_id INTEGER;

-- Table PLANT_CUTTINGS
CREATE TABLE plant_cuttings (
    parent_plant_id INTEGER,
    source_type VARCHAR(50),  -- cutting/seeds/division/offset
    method VARCHAR(50),       -- water/soil/air-layer/substrate
    date_harvested DATETIME,
    status VARCHAR(50),       -- rooting/growing/ready-to-pot/potted/failed
    ...
);

-- Table CUTTING_HISTORY
CREATE TABLE cutting_history (
    cutting_id INTEGER,
    event VARCHAR(50),        -- rooted/leaves-grown/ready-to-pot
    measurement JSON,
    ...
);
```

#### Mes Recommandations
```sql
-- ❌ PAS de colonne dans plants (duplication)
-- Table plants reste pure

-- Table PLANT_PROPAGATIONS (plus générique)
CREATE TABLE plant_propagations (
    parent_plant_id INTEGER,
    child_plant_id INTEGER,  -- ← Différence clé!
    propagation_type VARCHAR(50),
    propagation_method VARCHAR(255),
    propagation_date DATE,
    status VARCHAR(50),      -- pending/rooting/rooted/transplanted/established/failed
    ...
);
```

#### 🎯 Recommandation Hybride

**Fusion des deux approches pour le meilleur des deux mondes :**

```sql
-- ✅ PAS de parent_plant_id dans plants (éviter duplication)

-- ✅ Table unifiée PLANT_PROPAGATIONS
CREATE TABLE plant_propagations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Relations (comme mes recommandations)
    parent_plant_id INTEGER NOT NULL,
    child_plant_id INTEGER,              -- NULL si bouture pas encore convertie
    
    -- Détails propagation (du plan original - EXCELLENT)
    source_type VARCHAR(50) NOT NULL,    -- cutting/seeds/division/offset
    method VARCHAR(50) NOT NULL,         -- water/soil/air-layer/substrate
    propagation_date DATE NOT NULL,
    
    -- États enrichis (mes recommandations)
    status VARCHAR(50) DEFAULT 'pending',
    -- pending → rooting → rooted → ready-to-pot → potted → established
    
    -- Tracking détaillé (plan original)
    date_harvested DATE NOT NULL,
    expected_ready DATE,                 -- Auto-calculé
    success_date DATE,
    
    -- Mesures (plan original - TRÈS BON)
    current_root_length_cm FLOAT,
    current_leaves_count INTEGER,
    current_roots_count INTEGER,
    
    -- Métadonnées
    notes TEXT,
    success_rate_estimate FLOAT DEFAULT 0.85,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(parent_plant_id) REFERENCES plants(id) ON DELETE CASCADE,
    FOREIGN KEY(child_plant_id) REFERENCES plants(id) ON DELETE SET NULL,
    
    CHECK(parent_plant_id != child_plant_id)
);

-- ✅ Table PROPAGATION_EVENTS (renommé de cutting_history)
CREATE TABLE propagation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    propagation_id INTEGER NOT NULL,
    event_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50) NOT NULL,     -- rooted/leaves-grown/transplanted/failed
    measurement JSON,                     -- {root_length_cm: 1.5, leaves: 3, roots: 4}
    notes TEXT,
    photo_url VARCHAR(255),              -- URL photo de progression
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(propagation_id) REFERENCES plant_propagations(id) ON DELETE CASCADE
);

-- Index
CREATE INDEX idx_parent_plant ON plant_propagations(parent_plant_id);
CREATE INDEX idx_child_plant ON plant_propagations(child_plant_id);
CREATE INDEX idx_status ON plant_propagations(status);
CREATE INDEX idx_source_method ON plant_propagations(source_type, method);
CREATE INDEX idx_propagation_events ON propagation_events(propagation_id, event_date);
```

**Avantages de cette fusion :**
- ✅ Pas de duplication (pas de parent_plant_id dans plants)
- ✅ Support boutures EN COURS (child_plant_id = NULL)
- ✅ Support boutures CONVERTIES (child_plant_id = plant_id)
- ✅ Détails source/method du plan original
- ✅ États granulaires de mes recommandations
- ✅ Timeline complète avec events
- ✅ Mesures progressives (root_length, leaves, roots)

---

### 2. **Workflow de Création**

#### Plan Original
```python
# Étape 1: Créer bouture (pas encore plante)
POST /api/plants/1/cuttings
{
    "source_type": "cutting",
    "method": "water",
    "notes": "3 feuilles"
}
# → Crée entry dans plant_cuttings (id=42)
# → PAS ENCORE une plante!

# Étape 2: Logger progression
POST /api/cuttings/42/progress
{
    "event": "rooted",
    "measurement": {"root_length_cm": 1.5}
}

# Étape 3: Convertir en plante (quand prête)
POST /api/cuttings/42/convert-to-plant
{
    "plant_name": "Monstera #2"
}
# → Crée entry dans plants
# → Link: plants.parent_plant_id = 1
```

#### Mes Recommandations
```python
# Créer plante + propagation en une fois
POST /api/plants/1/propagate-complete
{
    "child_plant_name": "Monstera #2",
    "propagation_type": "division",
    "propagation_date": "2025-11-01"
}
# → Crée plants entry ET plant_propagations entry
# → Transaction atomique
```

#### 🎯 Recommandation Hybride

**Combiner les deux approches selon le cas d'usage :**

```python
# CAS 1: Bouture en cours (pas encore plante)
POST /api/plants/{parent_id}/propagations/start
{
    "source_type": "cutting",
    "method": "water",
    "notes": "3 feuilles prélevées"
}
# → Crée plant_propagations (child_plant_id = NULL)
# → Status: "pending"

# CAS 2: Logger progression
POST /api/propagations/{id}/events
{
    "event_type": "rooted",
    "measurement": {"root_length_cm": 1.5, "roots": 4},
    "notes": "Premières racines!"
}
# → Crée propagation_events entry
# → Update plant_propagations.status si applicable

# CAS 3A: Conversion manuelle en plante
POST /api/propagations/{id}/convert-to-plant
{
    "plant_name": "Monstera #2",
    "location_id": 5
}
# → Crée plants entry
# → Update plant_propagations.child_plant_id
# → Update status: "potted" → "established"

# CAS 3B: Création directe (ex: division)
POST /api/plants/{parent_id}/propagations/immediate
{
    "child_plant_name": "Snake Plant Division",
    "source_type": "division",
    "method": "soil",
    "notes": "Séparation immédiate"
}
# → Crée plants entry ET plant_propagations entry
# → child_plant_id défini immédiatement
# → Status: "established" (pas de phase rooting)
```

**Règle métier :**
```python
def should_create_plant_immediately(source_type: str, method: str) -> bool:
    """Détermine si la plante doit être créée immédiatement"""
    # Division en terre = plante immédiate
    if source_type == "division" and method == "soil":
        return True
    
    # Offset déjà enraciné = plante immédiate
    if source_type == "offset":
        return True
    
    # Bouture = attendre enracinement
    if source_type == "cutting":
        return False
    
    # Graines = attendre germination
    if source_type == "seeds":
        return False
    
    return False
```

---

### 3. **États et Transitions**

#### Plan Original
```
rooting → growing → ready-to-pot → potted → failed
```

#### Mes Recommandations
```
pending → rooting → rooted → transplanted → established → failed/abandoned
```

#### 🎯 Recommandation Hybride

**États unifiés avec logique métier :**

```python
class PropagationStatus(str, Enum):
    # Phase 1: Démarrage
    PENDING = "pending"              # Juste créée, pas encore en rooting
    
    # Phase 2: Enracinement (pour cuttings/seeds)
    ROOTING = "rooting"              # En cours d'enracinement (eau/terre)
    ROOTED = "rooted"                # Racines formées (>1cm)
    
    # Phase 3: Croissance
    GROWING = "growing"              # Nouvelle croissance visible (feuilles)
    READY_TO_POT = "ready-to-pot"    # Prête à être mise en pot (racines >2cm)
    
    # Phase 4: Établissement
    POTTED = "potted"                # Mise en pot/terre
    TRANSPLANTED = "transplanted"    # Transplantée (synonyme de potted)
    ESTABLISHED = "established"      # Bien établie, croissance stable
    
    # Phase 5: Terminale
    FAILED = "failed"                # Échec (mort, pourriture)
    ABANDONED = "abandoned"          # Projet abandonné

# Transitions valides (machine à états)
STATUS_TRANSITIONS = {
    'pending': ['rooting', 'growing', 'potted', 'failed', 'abandoned'],
    'rooting': ['rooted', 'growing', 'failed', 'abandoned'],
    'rooted': ['growing', 'ready-to-pot', 'failed'],
    'growing': ['ready-to-pot', 'potted', 'established', 'failed'],
    'ready-to-pot': ['potted', 'transplanted', 'failed'],
    'potted': ['established', 'failed'],
    'transplanted': ['established', 'failed'],
    'established': [],  # État terminal positif
    'failed': [],       # État terminal négatif
    'abandoned': []     # État terminal neutre
}

# Durées estimées par état (jours)
STATUS_DURATION_ESTIMATES = {
    ('cutting', 'water'): {
        'rooting': 7,      # 1 semaine en eau
        'rooted': 3,       # 3 jours croissance racines
        'growing': 7,      # 1 semaine nouvelles feuilles
        'ready-to-pot': 0  # Prêt immédiatement
    },
    ('cutting', 'soil'): {
        'rooting': 14,     # 2 semaines en terre
        'rooted': 7,
        'growing': 7,
        'ready-to-pot': 0
    },
    ('division', 'soil'): {
        'potted': 0,       # Immédiat
        'established': 14  # 2 semaines adaptation
    }
}

def calculate_expected_ready_date(
    source_type: str,
    method: str,
    start_date: date
) -> date:
    """Calcule la date prévue de succès"""
    durations = STATUS_DURATION_ESTIMATES.get((source_type, method), {})
    total_days = sum(durations.values())
    return start_date + timedelta(days=total_days)
```

---

### 4. **API Endpoints**

#### Comparaison

| Endpoint | Plan Original | Mes Recommandations | Hybride Recommandé |
|----------|---------------|---------------------|---------------------|
| **Liste enfants** | `GET /plants/{id}/cuttings` | `GET /plants/{id}/children` | `GET /plants/{id}/propagations` ✅ |
| **Créer propagation** | `POST /plants/{id}/cuttings` | `POST /plants/{id}/propagate` | `POST /plants/{id}/propagations` ✅ |
| **Logger progression** | `POST /cuttings/{id}/progress` | - | `POST /propagations/{id}/events` ✅ |
| **Généalogie** | `GET /plants/{id}/family-tree` | `GET /plants/{id}/genealogy` | `GET /plants/{id}/genealogy` ✅ |
| **Convertir** | `POST /cuttings/{id}/convert` | - | `POST /propagations/{id}/convert-to-plant` ✅ |
| **Statistiques** | `GET /plants/{id}/success-rate` | - | `GET /plants/{id}/propagations/stats` ✅ |

#### 🎯 API Finale Recommandée

```python
# ==========================================
# CRUD Propagations
# ==========================================

# 1. Lister toutes les propagations d'une plante
GET /api/plants/{plant_id}/propagations
Query params: ?status=rooting&source_type=cutting
Response: [
    {
        "id": 1,
        "parent_plant_id": 5,
        "child_plant_id": null,  # Pas encore convertie
        "source_type": "cutting",
        "method": "water",
        "status": "rooting",
        "date_harvested": "2025-11-01",
        "expected_ready": "2025-11-18",
        "current_root_length_cm": 1.2,
        "events_count": 3
    }
]

# 2. Créer une propagation (bouture en cours)
POST /api/plants/{plant_id}/propagations
Body: {
    "source_type": "cutting",
    "method": "water",
    "notes": "3 feuilles, tige 15cm"
}
Response: 201 Created

# 3. Créer propagation + plante immédiatement (division/offset)
POST /api/plants/{plant_id}/propagations/immediate
Body: {
    "child_plant_name": "Snake Plant Division A",
    "source_type": "division",
    "method": "soil",
    "location_id": 3
}
Response: 201 Created (avec child_plant_id rempli)

# 4. Détails d'une propagation
GET /api/propagations/{propagation_id}
Response: {
    "id": 1,
    "parent_plant": {...},
    "child_plant": null,
    "status": "rooting",
    "events": [
        {
            "id": 1,
            "event_type": "rooted",
            "event_date": "2025-11-04",
            "measurement": {"root_length_cm": 0.3},
            "notes": "Première racine visible!"
        }
    ],
    "success_rate_estimate": 0.85
}

# 5. Mettre à jour une propagation
PATCH /api/propagations/{propagation_id}
Body: {
    "status": "rooted",
    "current_root_length_cm": 1.5,
    "notes": "Racines bien développées"
}

# 6. Supprimer une propagation
DELETE /api/propagations/{propagation_id}

# ==========================================
# Events Timeline
# ==========================================

# 7. Logger un événement de progression
POST /api/propagations/{propagation_id}/events
Body: {
    "event_type": "rooted",
    "measurement": {
        "root_length_cm": 1.5,
        "roots_count": 4,
        "leaves_count": 3
    },
    "notes": "Premières racines visibles",
    "photo_url": "/uploads/cutting_day7.jpg"
}
Response: 201 Created

# 8. Lister les événements
GET /api/propagations/{propagation_id}/events
Response: [
    {
        "id": 1,
        "event_date": "2025-11-04",
        "event_type": "rooted",
        "measurement": {...},
        "notes": "...",
        "days_since_start": 3
    }
]

# ==========================================
# Conversion & Genealogy
# ==========================================

# 9. Convertir bouture en plante
POST /api/propagations/{propagation_id}/convert-to-plant
Body: {
    "plant_name": "Monstera #2",
    "location_id": 5,
    "inherit_parent_settings": true
}
Response: {
    "plant_id": 15,
    "propagation_id": 1,
    "message": "Bouture convertie en plante avec succès"
}

# 10. Arbre généalogique complet
GET /api/plants/{plant_id}/genealogy
Query params: ?max_depth=3
Response: {
    "plant": {...},
    "ancestors": [...],
    "descendants": [...],
    "propagations": [
        {
            "id": 1,
            "status": "rooting",
            "child_plant": null
        }
    ]
}

# ==========================================
# Statistiques & Analytics
# ==========================================

# 11. Statistiques de propagation
GET /api/plants/{plant_id}/propagations/stats
Response: {
    "total_propagations": 10,
    "by_status": {
        "rooting": 2,
        "rooted": 1,
        "potted": 4,
        "established": 2,
        "failed": 1
    },
    "success_rate": 0.70,
    "avg_rooting_days": 12.5,
    "by_method": {
        "water": {"count": 6, "success_rate": 0.83},
        "soil": {"count": 4, "success_rate": 0.50}
    }
}

# 12. Suggestions optimales
GET /api/plants/{plant_id}/propagation-recommendations
Response: {
    "recommended_source": "cutting",
    "recommended_method": "water",
    "best_season": "spring",
    "estimated_success_rate": 0.90,
    "reasoning": "Basé sur historique (6/6 réussies en eau)"
}

# ==========================================
# Batch Operations
# ==========================================

# 13. Créer plusieurs propagations en une fois
POST /api/plants/{plant_id}/propagations/batch
Body: {
    "quantity": 3,
    "base_name": "Monstera Bouture",
    "source_type": "cutting",
    "method": "water",
    "notes": "Prélevées le même jour"
}
Response: {
    "created": 3,
    "propagation_ids": [10, 11, 12]
}

# ==========================================
# Alertes & Notifications
# ==========================================

# 14. Propagations nécessitant attention
GET /api/propagations/alerts
Response: [
    {
        "propagation_id": 5,
        "alert_type": "stuck_rooting",
        "message": "En enracinement depuis 30 jours",
        "action": "Vérifier l'état, envisager échec?"
    },
    {
        "propagation_id": 8,
        "alert_type": "ready_to_pot",
        "message": "Racines >2cm, prête à être mise en pot",
        "action": "Rempoter maintenant"
    }
]
```

---

### 5. **Détection Cycles & Validations**

#### Plan Original
```python
# ❌ Pas de validation anti-cycle mentionnée
```

#### Mes Recommandations
```python
# ✅ Validation anti-cycle stricte
def check_circular_dependency(db, parent_id, child_id):
    # Vérifier qu'on ne crée pas de cycle
    pass
```

#### 🎯 Implémentation Recommandée

```python
# backend/app/services/validation_service.py

class PropagationValidationService:
    """Service de validation pour propagations"""
    
    @staticmethod
    def validate_propagation_creation(
        db: Session,
        parent_id: int,
        child_id: Optional[int] = None,
        source_type: str = None,
        method: str = None
    ) -> tuple[bool, Optional[str]]:
        """
        Valide la création d'une propagation.
        
        Returns: (is_valid, error_message)
        """
        # 1. Vérifier que le parent existe
        parent = db.query(Plant).filter(Plant.id == parent_id).first()
        if not parent:
            return False, "Plante mère introuvable"
        
        # 2. Si child_id fourni, vérifier cycles
        if child_id:
            if parent_id == child_id:
                return False, "Une plante ne peut être son propre parent"
            
            if PropagationValidationService._has_circular_dependency(
                db, parent_id, child_id
            ):
                return False, "Cycle détecté dans la généalogie"
        
        # 3. Valider combinaison source/method
        if source_type and method:
            if not PropagationValidationService._is_valid_combination(
                source_type, method
            ):
                return False, f"Combinaison invalide: {source_type} + {method}"
        
        return True, None
    
    @staticmethod
    def _has_circular_dependency(
        db: Session,
        parent_id: int,
        child_id: int,
        max_depth: int = 50
    ) -> bool:
        """Vérifie si ajouter child comme enfant de parent crée un cycle"""
        visited = set()
        current = parent_id
        depth = 0
        
        while current and depth < max_depth:
            if current == child_id:
                return True  # Cycle détecté!
            
            if current in visited:
                break  # Cycle dans les ancêtres (déjà invalide)
            
            visited.add(current)
            
            # Chercher le parent de current via propagations
            parent_prop = db.query(PlantPropagation).filter(
                PlantPropagation.child_plant_id == current
            ).first()
            
            current = parent_prop.parent_plant_id if parent_prop else None
            depth += 1
        
        return False
    
    @staticmethod
    def _is_valid_combination(source_type: str, method: str) -> bool:
        """Vérifie si la combinaison source/method est valide"""
        VALID_COMBINATIONS = {
            'cutting': ['water', 'soil', 'air-layer', 'substrate'],
            'seeds': ['soil', 'substrate'],
            'division': ['soil', 'substrate'],
            'offset': ['soil', 'substrate', 'water']
        }
        
        allowed_methods = VALID_COMBINATIONS.get(source_type, [])
        return method in allowed_methods
    
    @staticmethod
    def validate_status_transition(
        current_status: str,
        new_status: str
    ) -> tuple[bool, Optional[str]]:
        """Valide une transition de statut"""
        allowed = STATUS_TRANSITIONS.get(current_status, [])
        
        if new_status not in allowed:
            return False, (
                f"Transition invalide: {current_status} → {new_status}. "
                f"Transitions autorisées: {', '.join(allowed)}"
            )
        
        return True, None


# Utilisation dans les endpoints
@router.post("/{plant_id}/propagations")
async def create_propagation(
    plant_id: int,
    data: PropagationCreate,
    db: Session = Depends(get_db)
):
    # Validation
    is_valid, error = PropagationValidationService.validate_propagation_creation(
        db, plant_id, None, data.source_type, data.method
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Créer propagation...
```

---

### 6. **Modèles SQLAlchemy**

#### 🎯 Modèles Finaux Recommandés

```python
# backend/app/models/propagation.py

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON, Boolean, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class PlantPropagation(BaseModel):
    """
    Représente une propagation (bouture, division, etc.)
    Peut exister SANS plante enfant (bouture en cours)
    Peut être liée à une plante enfant (bouture convertie)
    """
    __tablename__ = "plant_propagations"
    
    # Relations
    parent_plant_id = Column(Integer, ForeignKey('plants.id', ondelete='CASCADE'), nullable=False, index=True)
    child_plant_id = Column(Integer, ForeignKey('plants.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Type de propagation (du plan original)
    source_type = Column(String(50), nullable=False, index=True)
    # Valeurs: cutting, seeds, division, offset
    
    method = Column(String(50), nullable=False)
    # Valeurs: water, soil, air-layer, substrate
    
    # Dates
    propagation_date = Column(Date, nullable=False, index=True)  # Date création/prélèvement
    date_harvested = Column(Date, nullable=False)  # Synonyme (compatibilité)
    expected_ready = Column(Date)  # Date prévue de succès (auto-calculé)
    success_date = Column(Date)  # Date effective de succès
    
    # État (mes recommandations)
    status = Column(String(50), default='pending', nullable=False, index=True)
    # Valeurs: pending, rooting, rooted, growing, ready-to-pot, potted, transplanted, established, failed, abandoned
    
    # Mesures actuelles (du plan original)
    current_root_length_cm = Column(Float)
    current_leaves_count = Column(Integer)
    current_roots_count = Column(Integer)
    
    # Métadonnées
    notes = Column(Text)
    success_rate_estimate = Column(Float, default=0.85)
    is_active = Column(Boolean, default=True)
    
    # Audit
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    
    # Relationships
    parent_plant = relationship(
        "Plant",
        foreign_keys=[parent_plant_id],
        backref="propagations_as_parent"
    )
    child_plant = relationship(
        "Plant",
        foreign_keys=[child_plant_id],
        backref="propagation_source",
        uselist=False
    )
    events = relationship(
        "PropagationEvent",
        back_populates="propagation",
        cascade="all, delete-orphan",
        order_by="PropagationEvent.event_date"
    )
    
    # Contraintes
    __table_args__ = (
        CheckConstraint('parent_plant_id != child_plant_id', name='no_self_parent'),
        CheckConstraint("source_type IN ('cutting', 'seeds', 'division', 'offset')", name='valid_source'),
        CheckConstraint("method IN ('water', 'soil', 'air-layer', 'substrate')", name='valid_method'),
        CheckConstraint('current_root_length_cm >= 0', name='positive_root_length'),
        CheckConstraint('current_leaves_count >= 0', name='positive_leaves'),
        CheckConstraint('current_roots_count >= 0', name='positive_roots'),
    )
    
    def __repr__(self):
        return f"<PlantPropagation(id={self.id}, parent={self.parent_plant_id}, status={self.status})>"
    
    @property
    def days_since_harvest(self) -> int:
        """Nombre de jours depuis le prélèvement"""
        if self.date_harvested:
            return (datetime.now().date() - self.date_harvested).days
        return 0
    
    @property
    def is_overdue(self) -> bool:
        """Vérifie si la propagation est en retard"""
        if self.expected_ready and self.status not in ['established', 'failed', 'abandoned']:
            return datetime.now().date() > self.expected_ready
        return False
    
    @property
    def progress_percentage(self) -> float:
        """Calcule le pourcentage de progression estimé"""
        status_weights = {
            'pending': 0,
            'rooting': 20,
            'rooted': 40,
            'growing': 60,
            'ready-to-pot': 80,
            'potted': 90,
            'transplanted': 90,
            'established': 100,
            'failed': 0,
            'abandoned': 0
        }
        return status_weights.get(self.status, 0)


class PropagationEvent(BaseModel):
    """
    Timeline détaillée de la progression d'une propagation.
    Chaque événement = snapshot d'un moment (mesures, observations, photos)
    """
    __tablename__ = "propagation_events"
    
    propagation_id = Column(Integer, ForeignKey('plant_propagations.id', ondelete='CASCADE'), nullable=False, index=True)
    event_date = Column(DateTime, server_default='CURRENT_TIMESTAMP', nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    # Valeurs: rooted, leaves-grown, ready-to-pot, potted, transplanted, failed, measurement
    
    # Mesures snapshot (JSON pour flexibilité)
    measurement = Column(JSON)
    # Exemple: {"root_length_cm": 1.5, "leaves_count": 3, "roots_count": 4, "health": "good"}
    
    notes = Column(Text)
    photo_url = Column(String(255))  # URL vers photo de progression
    
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    propagation = relationship("PlantPropagation", back_populates="events")
    
    def __repr__(self):
        return f"<PropagationEvent(id={self.id}, type={self.event_type}, date={self.event_date})>"
    
    @property
    def days_since_propagation_start(self) -> int:
        """Jours depuis le début de la propagation"""
        if self.propagation and self.propagation.date_harvested:
            return (self.event_date.date() - self.propagation.date_harvested).days
        return 0
```

---

## 📋 Checklist de Migration

### Avant de Commencer
- [ ] **Backup de la base de données** (CRITIQUE!)
- [ ] Lire ce document en entier
- [ ] Décider quelle approche adopter (voir recommandations ci-dessous)
- [ ] Préparer environnement de test
# 🌳 FEATURE PROPAGATION - ARCHITECTE FINALE
**11 Novembre 2025** | Améliorations intégrées | Sans code

---

## 🎯 VISION GLOBALE

Tracker les relations généalogiques entre plantes avec:
- **3 types de relations:** mère/fille/soeur (+ petite-fille, cousine...)
- **4 sources de propagation:** cutting, seeds, division, offset
- **4 méthodes de culture:** water, soil, air-layer, substrate
- **Calendrier dédié:** chronologie jour-par-jour avec photos
- **Statistiques intelligentes:** taux succès par source × méthode
- **Arbre familial:** visualisation graphique des générations

---

## 🏗️ ARCHITECTURE RECOMMANDÉE (Fusion Optimale)

### **Principes Clés**
```
✅ Pas de parent_plant_id dans plants (éviter duplication)
✅ Une table unifiée pour TOUS les types propagation
✅ Support boutures EN COURS (sans plante enfant)
✅ Support boutures CONVERTIES (avec plante enfant)
✅ États granulaires (pending → rooting → potted → established)
✅ Timeline complète avec mesures progressives
```

### **3 Tables Principales**

#### **TABLE 1: PLANT_PROPAGATIONS** (Unifiée)
```
Remplace: plant_cuttings + cutting_history

Colonnes principales:
├─ id
├─ parent_plant_id (FK) ← LA MÈRE
├─ child_plant_id (FK) ← LA FILLE (NULL = pas encore convertie)
├─ source_type: "cutting" | "seeds" | "division" | "offset"
├─ method: "water" | "soil" | "air-layer" | "substrate"
├─ propagation_date: DATE (création/prélèvement)
├─ expected_ready: DATE (auto-calculé)
├─ success_date: DATE (effective)
├─ status: "pending" | "rooting" | "rooted" | "growing" | 
│          "ready-to-pot" | "potted" | "established" | "failed" | "abandoned"
├─ current_root_length_cm: FLOAT
├─ current_leaves_count: INT
├─ current_roots_count: INT
├─ success_rate_estimate: FLOAT (0.85 = 85%)
├─ notes: TEXT
├─ is_active: BOOLEAN
├─ created_at, updated_at: TIMESTAMPS
└─ Contraintes: 
   ├─ parent_plant_id != child_plant_id
   ├─ source_type IN (cutting, seeds, division, offset)
   ├─ method IN (water, soil, air-layer, substrate)

Indices:
├─ parent_plant_id
├─ child_plant_id
├─ status
└─ source_type + method (composite)

Cas d'Usage:
✅ Bouture en eau depuis 10 jours (child_plant_id = NULL)
✅ Bouture convertie en plant #5 (child_plant_id = 5)
✅ Division immédiate avec plant créé (status = "established" jour 0)
✅ Graines en germinateur (source_type = "seeds")
```

#### **TABLE 2: PROPAGATION_EVENTS** (Timeline)
```
Remplace: cutting_history

Colonnes:
├─ id
├─ propagation_id (FK) → plant_propagations
├─ event_date: DATETIME (auto = CURRENT_TIMESTAMP)
├─ event_type: "rooted" | "leaves-grown" | "ready-to-pot" | "potted" | "failed"
├─ measurement: JSON
│  └─ Exemple: {"root_length_cm": 1.5, "leaves_count": 3, "roots_count": 4, "health": "good"}
├─ notes: TEXT (observation libre)
├─ photo_url: VARCHAR(255) (lien photo progression)
└─ created_at: TIMESTAMP

Indices:
├─ propagation_id + event_date (composite, ordered)

Cas d'Usage:
✅ Day 0: "Bouture prélevée et mise en eau"
✅ Day 3: "Première racine visible (0.3cm)"
✅ Day 7: "Racines bien formées (1.2cm, 4 racines)"
✅ Day 14: "Nouvelle feuille + prête à rempoter"
✅ Day 21: "Rempoté en terre"
```

#### **TABLE 3: PLANTS** (Inchangée)
```
⚠️ IMPORTANT: PAS de parent_plant_id ici!

Raison:
- Évite duplication (relation existe dans plant_propagations)
- Plants peut être créé sans propagation (achats)
- Recherche parent passe par plant_propagations

Si besoin de requête rapide (rare):
- Créer VIEW: SELECT parent_plant_id FROM plant_propagations WHERE child_plant_id = ?
```

---

## 📊 ÉTATS & TRANSITIONS (Machine à États)

### **États Définis**

```python
States = {
    # Phase 1: Initiale
    'pending': {
        'meaning': 'Juste créée, attente démarrage',
        'next': ['rooting', 'growing', 'potted', 'failed', 'abandoned'],
        'use_case': 'Bouture prête mais pas encore en eau'
    },
    
    # Phase 2: Enracinement (cutting/seeds)
    'rooting': {
        'meaning': 'Développement des racines',
        'next': ['rooted', 'growing', 'failed', 'abandoned'],
        'use_case': 'Bouture en eau depuis 3 jours, pas encore racines'
    },
    'rooted': {
        'meaning': 'Racines visibles formées',
        'next': ['growing', 'ready-to-pot', 'failed'],
        'use_case': 'Racines > 1cm, structure établie'
    },
    
    # Phase 3: Croissance
    'growing': {
        'meaning': 'Nouvelle croissance visible',
        'next': ['ready-to-pot', 'potted', 'established', 'failed'],
        'use_case': 'Nouvelle feuille, tige allonge'
    },
    'ready-to-pot': {
        'meaning': 'Prête à être rempoté',
        'next': ['potted', 'transplanted', 'failed'],
        'use_case': 'Racines > 2cm, suffisant pour terre'
    },
    
    # Phase 4: Établissement
    'potted': {
        'meaning': 'Rempoté en terre',
        'next': ['established', 'failed'],
        'use_case': 'Première semaine après rempotage'
    },
    'transplanted': {
        'meaning': 'Transplantée (synonyme potted)',
        'next': ['established', 'failed'],
        'use_case': 'Déplacée vers meilleur emplacement'
    },
    'established': {
        'meaning': '✅ SUCCÈS - plante stable',
        'next': [],
        'use_case': 'Croissance normale depuis 2+ semaines'
    },
    
    # Phase 5: Terminales
    'failed': {
        'meaning': '❌ ÉCHEC - morte',
        'next': [],
        'use_case': 'Pourriture, pas de racines, moisissure'
    },
    'abandoned': {
        'meaning': '⚠️ ABANDON - projet arrêté',
        'next': [],
        'use_case': 'Arrêt volontaire du tracking'
    }
}
```

### **Règles de Transition par Type × Méthode**

```python
# Division/Offset = pas d'enracinement
Division (soil):
  pending → potted → established (immédiat, juste adaptation)
  
# Cutting water = rapide
Cutting (water):
  pending → rooting (3j) → rooted (7j) → growing (10j) → ready-to-pot (14j) → potted (21j) → established

# Cutting soil = plus lent
Cutting (soil):
  pending → rooting (7j) → rooted (14j) → growing (20j) → ready-to-pot (28j) → potted → established

# Seeds = très long
Seeds (soil):
  pending → rooting (14j) → rooted (30j) → growing (60j) → established
```

---

## 🔗 RELATIONS & CYCLES

### **3 Types de Relations**

```
MÈRE (Plante source originale)
├─ parent_plant_id = NULL (elle-même n'a pas de parent)
├─ Peut générer N enfants
├─ Exemple: Monstera achetée en 2020

FILLE (Issue directe d'une mère)
├─ child_plant_id = plant_id de la fille
├─ parent_plant_id = plant_id de la mère
├─ Peut devenir mère à son tour
├─ Exemple: Bouture prélevée Oct 2024

SOEUR (Partage la même mère)
├─ Même parent_plant_id
├─ Peut être même jour ou jours différents
├─ Peut être même méthode ou méthodes différentes
└─ Exemple: 3 boutures du Monstera prélevées ensemble

PETITE-FILLE (Enfant d'une fille)
├─ Générations sur 3+ niveaux
├─ Arbre généalogique complet
└─ Exemple: Bouture de bouture de bouture
```

### **Validation Anti-Cycle**

```python
# ⚠️ CRITIQUE: Vérifier avant de créer propagation

def has_circular_dependency(db, parent_id, child_id, max_depth=50):
    """
    Parcourt les ancêtres de parent_id.
    Si on trouve child_id, c'est un cycle!
    
    Exemple problème:
    Plant #1 → #2 (parent) → #3 (parent)
    Créer #3 → #1 serait un cycle!
    """
    visited = set()
    current = parent_id
    depth = 0
    
    while current and depth < max_depth:
        if current == child_id:
            return True  # CYCLE DÉTECTÉ!
        
        if current in visited:
            break  # Cycle dans les ancêtres (déjà invalide)
        
        visited.add(current)
        
        # Chercher parent via propagations
        parent_prop = db.query(PlantPropagation).filter(
            PlantPropagation.child_plant_id == current
        ).first()
        
        current = parent_prop.parent_plant_id if parent_prop else None
        depth += 1
    
    return False  # Pas de cycle

# Avant de créer propagation:
if has_circular_dependency(db, parent_id, child_id):
    raise ValueError("Cycle généalogique détecté!")
```

---

## 🔌 API ENDPOINTS (Complets)

### **CRUD Propagations**

```
# 1. LISTER propagations d'une plante
GET /api/plants/{plant_id}/propagations
Query params:
  ?status=rooting              # Filter par statut
  ?source_type=cutting         # Filter par source
  ?method=water                # Filter par méthode
  ?include_archived=false      # Inclure échouées/abandonnées?

Response: [
  {
    "id": 1,
    "parent_plant_id": 5,
    "child_plant_id": null,
    "source_type": "cutting",
    "method": "water",
    "status": "rooting",
    "date_harvested": "2025-11-01",
    "expected_ready": "2025-11-18",
    "current_root_length_cm": 1.2,
    "current_leaves_count": 3,
    "current_roots_count": 4,
    "notes": "3 feuilles, bonne tige",
    "success_rate_estimate": 0.85,
    "days_since_harvest": 14,
    "progress_percentage": 40,
    "is_overdue": false,
    "events_count": 5
  }
]

# 2. CRÉER propagation (bouture en cours)
POST /api/plants/{plant_id}/propagations
Body: {
  "source_type": "cutting",
  "method": "water",
  "notes": "3 feuilles, 15cm"
}
Response: 201 Created { "id": 42, ... }

# 3. CRÉER propagation + plante immédiate (division/offset)
POST /api/plants/{plant_id}/propagations/immediate
Body: {
  "child_plant_name": "Monstera Division A",
  "source_type": "division",
  "method": "soil",
  "location_id": 3
}
Response: 201 Created {
  "propagation_id": 42,
  "plant_id": 15,
  "status": "established"
}

# 4. DÉTAILS une propagation
GET /api/propagations/{propagation_id}
Response: {
  "id": 42,
  "parent_plant": { id: 5, name: "Monstera Original", ... },
  "child_plant": null,
  "status": "rooting",
  "source_type": "cutting",
  "method": "water",
  "events": [
    {
      "id": 100,
      "event_date": "2025-11-04",
      "event_type": "rooted",
      "measurement": {"root_length_cm": 0.3, "roots_count": 1},
      "notes": "Première racine!",
      "photo_url": "/uploads/cutting_day4.webp",
      "days_since_start": 3
    }
  ],
  "timeline_summary": "Jour 14/17 avant prête"
}

# 5. METTRE À JOUR propagation
PATCH /api/propagations/{propagation_id}
Body: {
  "status": "rooted",
  "current_root_length_cm": 1.5,
  "current_roots_count": 4,
  "notes": "Racines bien développées"
}

# 6. SUPPRIMER propagation
DELETE /api/propagations/{propagation_id}
```

### **Timeline Events**

```
# 7. LOGGER événement de progression
POST /api/propagations/{propagation_id}/events
Body: {
  "event_type": "rooted",
  "measurement": {
    "root_length_cm": 1.5,
    "leaves_count": 3,
    "roots_count": 4,
    "health": "good"
  },
  "notes": "Premières racines bien formées!",
  "photo_url": "/uploads/cutting_day7.webp"
}
Response: 201 Created { "id": 101, ... }

# 8. LISTER events
GET /api/propagations/{propagation_id}/events
Response: [{...}, {...}]

# 9. DÉTAILS un event
GET /api/propagations/{propagation_id}/events/{event_id}

# 10. SUPPRIMER event
DELETE /api/propagations/{propagation_id}/events/{event_id}
```

### **Conversion & Genealogy**

```
# 11. CONVERTIR bouture en plante
POST /api/propagations/{propagation_id}/convert-to-plant
Body: {
  "plant_name": "Monstera #2",
  "location_id": 5,
  "inherit_parent_settings": true
}
Response: 201 Created {
  "plant_id": 15,
  "propagation_id": 42,
  "message": "Bouture #42 convertie en plant #15"
}

# 12. ARBRE GÉNÉALOGIQUE complet
GET /api/plants/{plant_id}/genealogy
Query params:
  ?max_depth=3              # Limiter profondeur
  ?include_failed=false     # Inclure échouées?
  
Response: {
  "plant": { id: 1, name: "Monstera Original", ... },
  "ancestors": [
    { id: 0, relation: "MÈRE d'achat (aucune)" }
  ],
  "descendants": [
    {
      "id": 2,
      "name": "Monstera Cutting #1",
      "relation": "FILLE",
      "propagation_id": 1,
      "source_type": "cutting",
      "method": "water",
      "status": "established",
      "propagation_date": "2025-11-01",
      "children": [
        {
          "id": 4,
          "relation": "PETITE-FILLE",
          "status": "rooting",
          ...
        }
      ]
    }
  ],
  "siblings": [
    {
      "id": 3,
      "name": "Monstera Cutting #2",
      "propagation_date": "2025-11-01",
      "status": "rooting"
    }
  ]
}

# 13. GRAPHE pour visualisation
GET /api/plants/{plant_id}/genealogy/graph
Response: {
  "nodes": [
    {"id": 1, "label": "Monstera Original", "type": "mère"},
    {"id": 2, "label": "Cutting #1", "type": "fille"}
  ],
  "edges": [
    {"source": 1, "target": 2, "label": "cutting/water"}
  ]
}
```

### **Statistiques & Analytics**

```
# 14. STATS de propagation
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
    "water": { "count": 6, "success_rate": 0.83, "avg_days": 14 },
    "soil": { "count": 4, "success_rate": 0.50, "avg_days": 21 }
  }
}

# 15. RECOMMANDATIONS
GET /api/plants/{plant_id}/propagation-recommendations
Response: {
  "recommended_source": "cutting",
  "recommended_method": "water",
  "best_season": "spring",
  "estimated_success_rate": 0.90,
  "reasoning": "Basé sur 6 tentatives: 6/6 réussies en eau"
}

# 16. ALERTES & SUIVI
GET /api/propagations/alerts
Response: [
  {
    "propagation_id": 5,
    "alert_type": "stuck_rooting",
    "message": "En rooting depuis 30 jours (estimé: 14)",
    "action": "Vérifier: eau claire? Tige pourrie?"
  },
  {
    "propagation_id": 8,
    "alert_type": "ready_to_pot",
    "message": "Racines >2cm, prête à rempoter",
    "action": "Rempoter aujourd'hui!"
  }
]

# 17. BATCH créer propagations
POST /api/plants/{plant_id}/propagations/batch
Body: {
  "quantity": 3,
  "base_name": "Monstera Bouture",
  "source_type": "cutting",
  "method": "water",
  "notes": "Prélevées ensemble"
}
Response: {
  "created": 3,
  "propagation_ids": [10, 11, 12]
}

# 18. CALENDRIER mensuel
GET /api/propagations/calendar/{year}/{month}
Response: {
  "month": "2025-11",
  "propagations": [
    {
      "id": 1,
      "date": "2025-11-01",
      "event": "Cutting prélevée",
      "parent_plant": "Monstera #1"
    },
    {
      "id": 1,
      "date": "2025-11-04",
      "event": "Première racine",
      "status": "rooting"
    }
  ]
}

# 19. EXPORT CSV
GET /api/propagations/export?format=csv&include_timeline=true
Response: CSV file
```

---

## 📅 CALENDRIER DÉDIÉ AUX BOUTURES

### **Vue Mensuelle**

```
NOVEMBRE 2025 - Propagations

  1  2  3  4  5  6  7
              |------ Monstera Cutting #1 (water) [🌱 rooting]
     |------- Pothos Cutting (soil) [🌱 rooting]

  8  9 10 11 12 13 14
     |-------- Hoya Cutting (air-layer) [🌿 growing]
                          |--- Peperomia Offset (soil) [🌱 rooting]

 15 16 17 18 19 20 21
                   ✅ Monstera ready-to-pot! (rooté)

 22 23 24 25 26 27 28
  ✅ Pothos prêt aussi!

 29 30
  
RÉSUMÉ:
- Total en cours: 7 propagations
- Prêtes à rempoter: 2
- Échouées: 1
- Taux succès: 85%
- Prochaine prête: 28 Nov
```

### **Indicateurs par Bouture**

```
Monstera Cutting #1
├─ Source: cutting (tige 3 feuilles)
├─ Method: water (dans verre)
├─ Lancée: 1er Nov 2025
├─ Estimée prête: 18 Nov (17 jours)
├─ Status: rooting (jour 14)
├─ Progression: 40% [████░░░░░░]
├─ Alerte: ⚠️ Légèrement retardée (30j vs 14j estimé)
└─ Prochaine action: Vérifier eau, chercher racines

Pothos Cutting
├─ Source: cutting
├─ Method: soil
├─ Lancée: 5 Nov
├─ Estimée prête: 25 Nov (20 jours)
├─ Status: rooting (jour 10)
├─ Progression: 50% [█████░░░░░]
├─ Alerte: ✅ Pas d'alerte
└─ Prochaine action: Attendre 10 jours, vérifier humidité
```

---

## 💾 MODÈLES SQLAlchemy (Recommandés)

### **PlantPropagation**
```python
class PlantPropagation(BaseModel):
    __tablename__ = "plant_propagations"
    
    id = Column(Integer, primary_key=True)
    
    # Relations
    parent_plant_id = Column(Integer, ForeignKey('plants.id', ondelete='CASCADE'), nullable=False, index=True)
    child_plant_id = Column(Integer, ForeignKey('plants.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Détails propagation
    source_type = Column(String(50), nullable=False, index=True)  # cutting/seeds/division/offset
    method = Column(String(50), nullable=False)  # water/soil/air-layer/substrate
    
    # Dates
    propagation_date = Column(Date, nullable=False, index=True)
    date_harvested = Column(Date, nullable=False)  # Synonyme
    expected_ready = Column(Date)  # Auto-calculé
    success_date = Column(Date)
    
    # État
    status = Column(String(50), default='pending', nullable=False, index=True)
    
    # Mesures
    current_root_length_cm = Column(Float)
    current_leaves_count = Column(Integer)
    current_roots_count = Column(Integer)
    
    # Métadonnées
    notes = Column(Text)
    success_rate_estimate = Column(Float, default=0.85)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    
    # Relationships
    parent_plant = relationship("Plant", foreign_keys=[parent_plant_id], backref="propagations_as_parent")
    child_plant = relationship("Plant", foreign_keys=[child_plant_id], backref="propagation_source", uselist=False)
    events = relationship("PropagationEvent", back_populates="propagation", cascade="all, delete-orphan")
    
    # Properties utiles
    @property
    def days_since_harvest(self) -> int:
        """Nombre de jours depuis prélèvement"""
        if self.date_harvested:
            return (datetime.now().date() - self.date_harvested).days
        return 0
    
    @property
    def is_overdue(self) -> bool:
        """Vérifie si en retard"""
        if self.expected_ready and self.status not in ['established', 'failed', 'abandoned']:
            return datetime.now().date() > self.expected_ready
        return False
    
    @property
    def progress_percentage(self) -> float:
        """% de progression estimé"""
        weights = {
            'pending': 0, 'rooting': 20, 'rooted': 40, 'growing': 60,
            'ready-to-pot': 80, 'potted': 90, 'established': 100,
            'failed': 0, 'abandoned': 0
        }
        return weights.get(self.status, 0)
```

### **PropagationEvent**
```python
class PropagationEvent(BaseModel):
    __tablename__ = "propagation_events"
    
    id = Column(Integer, primary_key=True)
    propagation_id = Column(Integer, ForeignKey('plant_propagations.id', ondelete='CASCADE'), nullable=False, index=True)
    
    event_date = Column(DateTime, server_default='CURRENT_TIMESTAMP', nullable=False, index=True)
    event_type = Column(String(50), nullable=False)  # rooted/leaves-grown/potted/failed
    
    measurement = Column(JSON)  # {root_length_cm: 1.5, leaves_count: 3, roots_count: 4, health: "good"}
    notes = Column(Text)
    photo_url = Column(String(255))
    
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    propagation = relationship("PlantPropagation", back_populates="events")
    
    @property
    def days_since_start(self) -> int:
        """Jours depuis le début de la propagation"""
        if self.propagation and self.propagation.date_harvested:
            return (self.event_date.date() - self.propagation.date_harvested).days
        return 0
```

---

## ⚠️ RÈGLES MÉTIER CRITIQUES

```python
# 1. VALIDATION SOURCE × MÉTHODE
VALID_COMBINATIONS = {
    'cutting': ['water', 'soil', 'air-layer', 'substrate'],
    'seeds': ['soil', 'substrate'],
    'division': ['soil', 'substrate'],
    'offset': ['soil', 'substrate', 'water']
}

# 2. CRÉATION IMMÉDIATE vs ATTENTE
def should_create_plant_immediately(source_type, method):
    # Immédiate: division soil, tous offset
    if (source_type == 'division' and method == 'soil') or source_type == 'offset':
        return True
    # Attendre: cutting, seeds
    return False

# 3. ESTIMATEUR DE DURÉE
DURATION_ESTIMATES = {
    ('cutting', 'water'): 14,      # 2 semaines
    ('cutting', 'soil'): 21,       # 3 semaines
    ('cutting', 'air-layer'): 35,  # 5 semaines
    ('seeds', 'soil'): 30,         # 1 mois
    ('division', 'soil'): 0,       # Immédiat
    ('offset', 'soil'): 7,         # 1 semaine
}

# 4. TAUX DE SUCCÈS ESTIMÉS
SUCCESS_RATES = {
    ('cutting', 'water'): 0.85,      # 85%
    ('cutting', 'soil'): 0.70,       # 70%
    ('cutting', 'air-layer'): 0.90,  # 90% (mais compliqué)
    ('seeds', 'soil'): 0.60,         # 60%
    ('division', 'soil'): 0.95,      # 95% (quasi garanti)
    ('offset', 'soil'): 0.80,        # 80%
}

# 5. ANTI-CYCLE
def prevent_circular_genealogy(db, parent_id, child_id):
    if has_circular_dependency(db, parent_id, child_id):
        raise ValueError("Cycle généalogique détecté!")

# 6. ALERTE SURCHARGE (rooting)
def check_rooting_alert(propagation):
    if propagation.status == 'rooting':
        days_rooting = propagation.days_since_harvest
        expected_days = DURATION_ESTIMATES[(propagation.source_type, propagation.method)]
        
        if days_rooting > expected_days + 10:  # Plus de 10 jours en retard
            return f"Alerte: {days_rooting}j en rooting (estimé: {expected_days}j)"
    
    return None
```

---

## 📋 FONCTIONNALITÉS CLÉS

### **Pour l'Utilisateur**

| Feature | Utilité |
|---------|---------|
| **Arbre Familial** | Visualiser générations d'un coup |
| **Filtre Filles** | "Combien de boutures du Monstera?" |
| **Filtre Soeurs** | "Lesquelles nées ensemble?" |
| **Timeline Photo** | Documenter chaque étape |
| **Estimateur** | "Prête le 18 Nov?" |
| **Success Rate** | "Water vs Soil - meilleur?" |
| **Alertes** | "Pas de racines depuis 30j?" |
| **Calendrier** | "Beaucoup de travail ce mois?" |
| **Statistiques** | Taux succès par method |
| **Recommandations** | "Comment réussir?" |

---

## ⏱️ EFFORT ESTIMÉ (Implementation)

| Phase | Effort | Notes |
|-------|--------|-------|
| Database (Migration) | 45 min | Créer 2 tables, indices |
| Models (SQLAlchemy) | 45 min | PlantPropagation, PropagationEvent |
| Services (Business Logic) | 1h | Validations, estimateurs, alerts |
| API Endpoints | 1h 30 | 18+ endpoints CRUD |
| Tests (Backend) | 1h 30 | Models, API, edge cases |
| Frontend Dashboard | 1h 30 | Résumé, stats, listes |
| Frontend Détails | 1h | Bouture, timeline |
| Frontend Calendrier | 1h 30 | Vue mensuelle avec gantt |
| Frontend Arbre | 1h 30 | Graphe généalogique (D3/Cytoscape) |
| Frontend Photos | 1h | Intégration images |
| Tests Frontend | 1h | Components, intégrations |
| Polish & QA | 1h | Edge cases, erreurs |

**TOTAL: 14-15 heures**
- **MVP (Backend seul):** 4-5 heures
- **MVP + Dashboard simple:** 6-7 heures
- **Complet (arbre + calendrier):** 14-15 heures

---

## ✅ STATUT: ARCHITECTURE FINALE, PRÊT À CODER

**Résumé des améliorations apportées:**
- ✅ Table unifiée (plant_propagations) au lieu de plant_cuttings
- ✅ Support boutures EN COURS + CONVERTIES
- ✅ États granulaires avec transitions validées
- ✅ Validation anti-cycle
- ✅ Estimateurs de durée et taux succès
- ✅ 18+ endpoints API spécifiés
- ✅ 10+ pages frontend
- ✅ Modèles SQLAlchemy complets
- ✅ Règles métier documentées
- ✅ Timeline jour-par-jour avec mesures

**Document complet, aucun code - prêt pour implementation!** 🚀

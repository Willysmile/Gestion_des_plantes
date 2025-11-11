# ⚡ QUICK START: IMPLÉMENTER LA FEATURE PROPAGATION

**11 Novembre 2025** | Guide étape-par-étape sans bullshit

---

## 🎯 En 30 Secondes

**Quoi:** Tracker générations de plantes (mère/fille/soeur) avec timeline photo
**Pourquoi:** Documenter comment propager + apprendre meilleure méthode
**Effort:** 14-15 heures
**Prêt:** Oui, architecture finalisée, code 0%

---

## 📚 DOCUMENTATION REQUISE

### **Avant de Coder (lisez absolument)**
1. `INDEX_PROPAGATION_DOCS.md` - Navigation (5 min)
2. `SYNTHESE_AMELIORATIONS_PROPAGATION.md` - Pourquoi ce design (10 min)
3. `FEATURE_PROPAGATION_FINAL.md` - Technique (30 min)

**Temps total: 45 minutes**

---

## 🗓️ PLAN D'IMPLÉMENTATION

### **Phase 1: Database (45 minutes)**

#### Étape 1.1: Créer Migration Alembic
```bash
cd backend
alembic revision --autogenerate -m "Add propagation tracking (plant_propagations + propagation_events)"
# Éditer le fichier généré
```

#### Étape 1.2: Ajouter à la migration
```python
# Dans le fichier migration (Voir FEATURE_PROPAGATION_FINAL.md pour schéma SQL complet)

op.create_table(
    'plant_propagations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_plant_id', sa.Integer(), nullable=False),
    sa.Column('child_plant_id', sa.Integer(), nullable=True),
    sa.Column('source_type', sa.String(50), nullable=False),  # cutting/seeds/division/offset
    sa.Column('method', sa.String(50), nullable=False),       # water/soil/air-layer/substrate
    sa.Column('propagation_date', sa.Date(), nullable=False),
    sa.Column('date_harvested', sa.Date(), nullable=False),
    sa.Column('expected_ready', sa.Date(), nullable=True),
    sa.Column('success_date', sa.Date(), nullable=True),
    sa.Column('status', sa.String(50), default='pending'),
    sa.Column('current_root_length_cm', sa.Float(), nullable=True),
    sa.Column('current_leaves_count', sa.Integer(), nullable=True),
    sa.Column('current_roots_count', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('success_rate_estimate', sa.Float(), default=0.85),
    sa.Column('is_active', sa.Boolean(), default=True),
    sa.Column('created_at', sa.DateTime(), server_default='CURRENT_TIMESTAMP'),
    sa.Column('updated_at', sa.DateTime(), server_default='CURRENT_TIMESTAMP'),
    sa.ForeignKeyConstraint(['parent_plant_id'], ['plants.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['child_plant_id'], ['plants.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.CheckConstraint('parent_plant_id != child_plant_id')
)

op.create_table(
    'propagation_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('propagation_id', sa.Integer(), nullable=False),
    sa.Column('event_date', sa.DateTime(), server_default='CURRENT_TIMESTAMP'),
    sa.Column('event_type', sa.String(50), nullable=False),
    sa.Column('measurement', sa.JSON(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('photo_url', sa.String(255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default='CURRENT_TIMESTAMP'),
    sa.ForeignKeyConstraint(['propagation_id'], ['plant_propagations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
)

# Indices
op.create_index('idx_parent_plant', 'plant_propagations', ['parent_plant_id'])
op.create_index('idx_child_plant', 'plant_propagations', ['child_plant_id'])
op.create_index('idx_status', 'plant_propagations', ['status'])
op.create_index('idx_source_method', 'plant_propagations', ['source_type', 'method'])
op.create_index('idx_propagation_events', 'propagation_events', ['propagation_id', 'event_date'])
```

#### Étape 1.3: Appliquer migration
```bash
alembic upgrade head
```

---

### **Phase 2: Modèles (45 minutes)**

#### Étape 2.1: Créer `backend/app/models/propagation.py`
```python
# Copier-coller depuis FEATURE_PROPAGATION_FINAL.md
# Section "Modèles SQLAlchemy (Recommandés)"

# Classes à créer:
- PlantPropagation (avec properties utiles)
- PropagationEvent
```

#### Étape 2.2: Mettre à jour `backend/app/models/__init__.py`
```python
from app.models.propagation import PlantPropagation, PropagationEvent
```

---

### **Phase 3: Services (1 heure)**

#### Étape 3.1: Créer `backend/app/services/propagation_service.py`
```python
# Implémenter les services:

class PropagationValidationService:
    # validate_propagation_creation()
    # validate_status_transition()
    # _has_circular_dependency()
    # _is_valid_combination()

class PropagationEstimatorService:
    # estimate_ready_date()
    # estimate_success_rate()
    # calculate_progress_percentage()
    # get_rooting_alert()

class PropagationAnalyticsService:
    # get_stats_for_plant()
    # get_recommendations()
    # get_success_rate_by_method()
```

#### Étape 3.2: Copier code depuis FEATURE_PROPAGATION_FINAL.md
- Section "Règles Métier Critiques"
- Utiliser les dictionnaires STATUS_TRANSITIONS, VALID_COMBINATIONS, etc.

---

### **Phase 4: API Endpoints (1 heure 30)**

#### Étape 4.1: Créer `backend/app/routes/propagations.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.propagation_service import *

router = APIRouter(prefix="/propagations", tags=["propagations"])

# Implémenter endpoints (voir FEATURE_PROPAGATION_FINAL.md):

# 1. GET /plants/{plant_id}/propagations
# 2. POST /plants/{plant_id}/propagations
# 3. POST /plants/{plant_id}/propagations/immediate
# 4. GET /propagations/{id}
# 5. PATCH /propagations/{id}
# 6. DELETE /propagations/{id}
# 7. POST /propagations/{id}/events
# 8. GET /propagations/{id}/events
# 9. POST /propagations/{id}/convert-to-plant
# 10. GET /plants/{id}/genealogy
# ... (19 endpoints totaux)
```

#### Étape 4.2: Créer schemas dans `backend/app/schemas/propagation.py`
```python
class PropagationCreate(BaseModel):
    source_type: str  # cutting, seeds, division, offset
    method: str       # water, soil, air-layer, substrate
    notes: Optional[str]

class PropagationUpdate(BaseModel):
    status: Optional[str]
    current_root_length_cm: Optional[float]
    notes: Optional[str]

class PropagationEventCreate(BaseModel):
    event_type: str
    measurement: Optional[dict]
    notes: Optional[str]
    photo_url: Optional[str]

class PropagationResponse(BaseModel):
    id: int
    parent_plant_id: int
    child_plant_id: Optional[int]
    source_type: str
    method: str
    status: str
    days_since_harvest: int
    progress_percentage: float
    is_overdue: bool
    
    class Config:
        from_attributes = True
```

#### Étape 4.3: Ajouter routes à `backend/app/main.py`
```python
from app.routes import propagations

app.include_router(propagations.router, prefix="/api")
```

---

### **Phase 5: Tests Backend (1 heure 30)**

#### Étape 5.1: Créer `backend/tests/test_propagations.py`
```python
import pytest
from sqlalchemy.orm import Session
from app.models import Plant, PlantPropagation
from app.services.propagation_service import PropagationValidationService

class TestPropagationValidation:
    def test_create_propagation_valid(self, db: Session):
        # Test case 1: Valid propagation
        pass
    
    def test_create_propagation_circular_dependency(self, db: Session):
        # Test case 2: Cycle detection
        pass
    
    def test_convert_to_plant(self, db: Session):
        # Test case 3: Convert cutting to plant
        pass
    
    # ... Plus de tests pour:
    # - Status transitions
    # - Rooting alerts
    # - Success rate calculation
    # - Timeline events
    # - Genealogy queries
```

#### Étape 5.2: Lancer tests
```bash
cd backend
pytest tests/test_propagations.py -v
```

---

### **Phase 6: Frontend Dashboard (1 heure 30)**

#### Étape 6.1: Créer page `frontend/src/pages/Propagations.jsx`
```jsx
import { useEffect, useState } from 'react'
import axios from 'axios'

export function PropagationsDashboard() {
  const [propagations, setPropagations] = useState([])
  const [stats, setStats] = useState(null)
  
  useEffect(() => {
    // Fetch /api/propagations/summary
    // Fetch /api/propagations/stats
    // Fetch /api/propagations/alerts
  }, [])
  
  return (
    <div>
      <h1>Propagations</h1>
      
      {/* Résumé: en_rooting, growing, ready, potted, established */}
      <StatsSummary stats={stats} />
      
      {/* Liste propagations avec filtres */}
      <PropagationsList propagations={propagations} />
      
      {/* Alertes */}
      <AlertsPanel />
    </div>
  )
}
```

#### Étape 6.2: Pages additionnelles (à faire après dashboard)
- `/propagations/:id` - Détails propagation
- `/plants/:id/genealogy` - Arbre généalogique
- `/propagations/calendar` - Vue mensuelle
- `/propagations/stats` - Statistiques

---

### **Phase 7: Frontend Calendrier (1 heure 30)**

#### Étape 7.1: Composant Calendrier
```jsx
// Utiliser library comme:
// - react-big-calendar
// - fullcalendar
// - ou custom Gantt

// Afficher:
// - Chaque bouture = une ligne
// - Timeline: jour 0 → established
// - Couleurs par statut (rooting, ready, potted, etc)
```

---

### **Phase 8: Frontend Arbre Généalogique (1 heure 30)**

#### Étape 8.1: Composant Graphe
```jsx
// Utiliser D3.js ou Cytoscape.js

// Afficher:
// - Parent au centre
// - Enfants autour (soeurs au même niveau)
// - Petites-filles en dessous
// - Clic = voir détails/ouvrir photo
```

---

### **Phase 9: Tests Frontend (1 heure)**

#### Étape 9.1: Tester composants
```bash
# Utiliser React Testing Library
npm test -- propagations
```

---

### **Phase 10: Polish & QA (1 heure)**

#### Étape 10.1: Tester scénarios
- [ ] Créer bouture
- [ ] Logger progression (5+ événements)
- [ ] Convertir en plante
- [ ] Voir arbre généalogique
- [ ] Voir alertes (overdue, ready)
- [ ] Export CSV
- [ ] Statistiques correctes

---

## 📋 CHECKLIST COMPLÈTE

### **Avant de Commencer**
- [ ] Lire FEATURE_PROPAGATION_FINAL.md (30 min)
- [ ] Comprendre 9 états (pending → established)
- [ ] Comprendre validation anti-cycle
- [ ] Backup DB (CRITIQUE!)

### **Database**
- [ ] Migration créée
- [ ] 2 tables ajoutées
- [ ] Indices créés
- [ ] Migration testée (alembic upgrade head)

### **Backend Code**
- [ ] Modèles SQLAlchemy (PlantPropagation, PropagationEvent)
- [ ] Services (validation, estimateurs, analytics)
- [ ] Routes (19 endpoints)
- [ ] Schemas Pydantic
- [ ] Tests (100% des endpoints)
- [ ] Aucune erreur de code

### **Frontend Code**
- [ ] Dashboard (résumé + listes)
- [ ] Détails propagation (timeline)
- [ ] Calendrier (vue mensuelle)
- [ ] Arbre généalogique (graphe)
- [ ] Composants testés
- [ ] Aucune erreur console

### **QA**
- [ ] Tous les endpoints testés
- [ ] Timeline jour-par-jour fonctionne
- [ ] Photos intégrées
- [ ] Arbre généalogique affiche bien
- [ ] Alertes correctes
- [ ] Pas d'erreurs
- [ ] Production-ready

---

## 🚀 COMMANDES RAPIDES

### **Start Database**
```bash
cd backend
alembic revision --autogenerate -m "Add propagation"
# Edit file
alembic upgrade head
```

### **Start Models**
```bash
# Créer backend/app/models/propagation.py
# Copier depuis FEATURE_PROPAGATION_FINAL.md
```

### **Start Services**
```bash
# Créer backend/app/services/propagation_service.py
# Implémenter validation + estimateurs
```

### **Start API**
```bash
# Créer backend/app/routes/propagations.py
# Implémenter 19 endpoints
# pytest tests/test_propagations.py
```

### **Start Frontend**
```bash
cd frontend
npm run dev
# Ajouter routes et pages
```

---

## ⚡ TIPS & TRICKS

### **Pour Aller Plus Vite**

1. **Copier-Coller Modèles**
   - FEATURE_PROPAGATION_FINAL.md section "Modèles"
   - Juste adapter noms/types

2. **Copier-Coller Endpoints**
   - Section "API ENDPOINTS"
   - Adapter pour votre setup

3. **Utiliser Templates Tests**
   - Copier structure tests existants
   - Adapter pour propagations

4. **Réutiliser Composants**
   - Existing plants list = template
   - Existing timeline UI = template

### **Pour Éviter Bugs**

1. **Validation Anti-Cycle**
   - Tester avec 3+ générations
   - Tester cas problématiques (cycle)

2. **États Transitions**
   - Vérifier machine à états
   - Pas de transition invalide

3. **Estimateurs**
   - Vérifier durées estimées
   - Vérifier taux succès par type/method

4. **Timeline Photos**
   - Vérifier photos sauvegardées
   - Vérifier URLs correctes

---

## 🎯 OBJECTIFS PAR JOUR

### **Jour 1 (4 heures)**
- [ ] Migration DB créée & testée
- [ ] Modèles SQLAlchemy complétés
- [ ] Services > validations

### **Jour 2 (4 heures)**
- [ ] Services > estimateurs
- [ ] 10 premiers endpoints
- [ ] Tests de base

### **Jour 3 (4 heures)**
- [ ] 9 endpoints restants
- [ ] Tests complètement
- [ ] Backend done

### **Jour 4 (4 heures)**
- [ ] Dashboard frontend
- [ ] Détails propagation
- [ ] Composants de base

### **Jour 5 (3 heures)**
- [ ] Calendrier
- [ ] Arbre généalogique
- [ ] Tests frontend

### **Total: ~19 heures** (proche du 14-15h estimé)

---

## 📞 QUESTIONS?

**Q: Par où commencer si nouveau?**
A: Phase 1 → Phase 2 → Phase 3. Ordre critique.

**Q: Comment tester ma migration?**
A: `alembic upgrade head` puis vérifier tables existent

**Q: Quels endpoints prioritaires?**
A: Lister, créer, détails, convertir. Puis ajouter alertes/stats

**Q: Comment faire l'arbre généalogique?**
A: Utiliser D3.js ou Cytoscape. API retourne nodes + edges.

**Q: Tout bon pour production?**
A: Oui si 100% tests + aucune erreur + alertes working

---

**Créé:** 11 Novembre 2025  
**Prêt:** OUI ✅  
**Bon courage!** 🚀

# 📋 CAHIER DES CHARGES & LOGIQUE MÉTIER - RECAP COMPLET

**Date:** 30 Octobre 2025  
**Phase:** 5A - Coverage Optimization (52% atteint)  
**Basé sur:** README.md, PLAN_ACTION_COMPLET.md, documentation métier

---

## 🎯 VISION PROJET

**Application web intuitive pour gérer ses plantes d'intérieur et extérieur :**
- 📱 Cataloguer plantes avec fiches détaillées (35+ champs)
- 💧 Suivi d'arrosage automatique et historique complet
- 📷 Galerie photos avec thumbnails (suivi croissance)
- 📊 Historique d'actions (arrosage, engrais, rempotage, maladies, notes)
- 💾 Export/Import données (CSV/JSON)
- 🗂️ Archivage & restauration de plantes
- 🔐 Soft delete (suppression logique, pas physique)
- ✨ Interface responsive (desktop/mobile/tablette)

**Target:** Utilisateurs passionnés par les plantes qui veulent tracker leur collection

---

## 🏗️ ARCHITECTURE MÉTIER

### **Entités Principales & Champs**

#### 1. **Plant** (Plante) - Entité Racine
```python
Plant:
  # Identités
  ├─ id: int (PK)
  ├─ name: str (obligatoire) - "Monstera Deliciosa"
  ├─ reference: str (unique, auto-générée) - "ARAC-001"
  ├─ scientific_name: str - "Rhaphidophora tetrasperma"
  ├─ family: str - "Araceae"
  ├─ genus: str
  ├─ species: str
  │
  # Propriétés physiques
  ├─ age_months: int - Durée depuis l'achat
  ├─ description: str - Notes générales
  ├─ purchase_date: date - Date d'achat
  ├─ purchase_place_id: int FK → PurchasePlaces
  │
  # Localisation
  ├─ location_id: int FK → Locations - Pièce (séjour, chambre, etc)
  │
  # État & Santé
  ├─ is_active: bool - True par défaut
  ├─ is_archived: bool - Soft delete marker
  ├─ archived_date: datetime - Quand archivée
  ├─ archived_reason: str - Pourquoi archivée
  ├─ last_watering_date: date - Dernière date d'arrosage (calculée)
  ├─ health_status: str - "HEALTHY", "SICK", "RECOVERING"
  │
  # Besoins environnementaux
  ├─ light_requirement: str - "LOW", "MEDIUM", "HIGH", "INDIRECT", "DIRECT"
  ├─ humidity_requirement: str - "LOW", "MEDIUM", "HIGH", "HUMID"
  ├─ temperature_min: int - ex: 15°C
  ├─ temperature_max: int - ex: 28°C
  ├─ difficulty_level: str - "EASY", "MEDIUM", "HARD"
  │
  # Métadonnées
  ├─ created_at: datetime
  ├─ updated_at: datetime
  ├─ deleted_at: datetime (soft delete)
  │
  # Relations
  ├─ photos: List[Photo] - Photos de la plante
  ├─ watering_histories: List[WateringHistory]
  ├─ fertilizing_histories: List[FertilizingHistory]
  ├─ repotting_histories: List[RepottingHistory]
  ├─ disease_histories: List[DiseaseHistory]
  ├─ plant_histories: List[PlantHistory] - Notes générales
  ├─ seasonal_waterings: List[SeasonalWatering] - Fréquence arrosage x 4 saisons
  ├─ seasonal_fertilizings: List[SeasonalFertilizing]
  ├─ tags: List[Tag] - Organisation
  └─ diseases: List[Disease] - Problèmes actuels
```

#### 2. **Photo** (Galerie)
```python
Photo:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant (obligatoire)
  ├─ url: str - Chemin local ou URL
  ├─ thumbnail_url: str - Version réduite
  ├─ is_primary: bool - Photo principale
  ├─ description: str - "Jour 45 - nouvelles feuilles"
  ├─ upload_date: datetime
  ├─ file_size: int
  ├─ image_format: str - "WEBP", "JPEG", "PNG"
  ├─ created_at: datetime
  └─ deleted_at: datetime (soft delete)
```

#### 3. **SeasonalWatering** (Fréquence Arrosage)
```python
SeasonalWatering:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant
  ├─ season: int - 1=Printemps, 2=Été, 3=Automne, 4=Hiver
  ├─ frequency_id: int FK → WateringFrequencies
  │  └─ Lookup table: [1=Quotidienne, 3=3 jours, 7=Hebdo, 14=Bi-hebdo, 30=Mensuelle, 60=2 mois]
  ├─ notes: str - "Moins d'eau en été"
  ├─ created_at: datetime
  └─ updated_at: datetime
```

#### 4. **WateringHistory** (Enregistrement Arrosage)
```python
WateringHistory:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant
  ├─ date: date - Quand arrosée
  ├─ amount_ml: int - Quantité en ml (ex: 250)
  ├─ notes: str - "Eau tiède", "Feuilles asséchées"
  ├─ created_at: datetime
  ├─ updated_at: datetime
  └─ deleted_at: datetime (soft delete)
```

#### 5. **FertilizingHistory** (Enregistrement Fertilisation)
```python
FertilizingHistory:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant
  ├─ date: date
  ├─ fertilizer_type_id: int FK → FertilizerTypes
  ├─ amount: str - "1/2 dose", "1 dose"
  ├─ notes: str
  ├─ created_at: datetime
  ├─ updated_at: datetime
  └─ deleted_at: datetime
```

#### 6. **RepottingHistory** (Changement de Pot)
```python
RepottingHistory:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant
  ├─ date: date
  ├─ old_pot_size: str - "10cm", "15cm"
  ├─ new_pot_size: str - "20cm"
  ├─ soil_type_id: int FK → SoilTypes
  ├─ notes: str
  ├─ created_at: datetime
  └─ deleted_at: datetime
```

#### 7. **DiseaseHistory** (Maladie/Problème)
```python
DiseaseHistory:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant
  ├─ disease_id: int FK → Disease
  ├─ date_detected: date - Quand découverte
  ├─ treatment: str - "Traitement appliqué"
  ├─ recovery_status: str - "INFECTED", "RECOVERING", "RECOVERED"
  ├─ recovery_date: date - Quand guérie
  ├─ notes: str
  ├─ created_at: datetime
  └─ deleted_at: datetime
```

#### 8. **PlantHistory** (Notes Générales)
```python
PlantHistory:
  ├─ id: int (PK)
  ├─ plant_id: int FK → Plant
  ├─ body: str - Note libre (ex: "A bien grandi ce mois-ci")
  ├─ created_at: datetime
  └─ deleted_at: datetime
```

#### **Lookup Tables** (Références)
```python
Locations:
  ├─ Salon, Chambre, Cuisine, Bureau, Balcon, Jardin, etc.

PurchasePlaces:
  ├─ Jardinerie, IKEA, Pépinière, Marché, Ligne, etc.

Tags:
  ├─ Succulent, Tropical, Facile, Fleuri, Toxique, etc.

Diseases:
  ├─ Pourriture racines, Araignée rouge, Mites, Chlorose, etc.

FertilizerTypes:
  ├─ Engrais liquide, Bâton, Poudre, Organique, NPK, etc.

SoilTypes:
  ├─ Terreau universel, Cactus/Succulentes, Orchidées, Acidophile, etc.

WateringFrequencies:
  ├─ Quotidienne (1j), 3 jours, Hebdomadaire (7j), Bi-hebdo (14j), Mensuelle (30j), Bimensuelle (60j)

Treatments:
  ├─ Spray insecticide, Fongicide, Isolation, etc.
```

---

## 📊 LOGIQUE MÉTIER CLÉS

### 1️⃣ **Gestion Saisonnière**
```
Chaque plante a DIFFÉRENTS besoins par saison:

SeasonalWatering(plant_id=5, season=1[printemps], frequency=7[hebdo])
SeasonalWatering(plant_id=5, season=2[été], frequency=3[3j])
SeasonalWatering(plant_id=5, season=3[automne], frequency=7[hebdo])
SeasonalWatering(plant_id=5, season=4[hiver], frequency=30[mensuelle])

→ Permet: "En hiver, arroser chaque 30 jours. En été, tous les 3 jours"
```

### 2️⃣ **Soft Delete (Archive)**
```
Pas de suppression physique → Archive logique:

DELETE /api/plants/{id}
  ↓ Ne supprime PAS la ligne
  ↓ Set is_archived = True, archived_date = NOW(), archived_reason = "..."

Récupérable:
PUT /api/plants/{id}/restore
  ↓ Set is_archived = False, archived_date = NULL
```

### 3️⃣ **Historique Complet**
```
Tracer TOUS les soins apportés:
- Arrosages (date, quantité, notes)
- Fertilisations (date, type, dose)
- Rempotages (date, ancien→nouveau pot)
- Maladies (date, traitement, récupération)
- Notes générales (observations libres)

→ Timeline complète de vie de la plante
```

### 4️⃣ **Calcul Dates Arrosage**
```
Business Logic:

last_watering_date = Date de dernier arrosage enregistré
today_date = Date du jour
frequency_jours = Fréquence saison actuelle (30, 7, 3, 1, etc.)

next_watering_date = last_watering_date + frequency_jours

Status:
- Si next_watering_date ≤ today_date  → "À ARROSER" (OVERDUE)
- Si next_watering_date = today_date  → "À ARROSER AUJOURD'HUI" (TODAY)
- Si next_watering_date ≤ today + 3j  → "À ARROSER BIENTÔT" (SOON)
- Si next_watering_date > today + 3j  → "Aucun arrosage urgent" (OK)

API endpoint: GET /api/statistics/upcoming-waterings
```

### 5️⃣ **Auto-calcul Référence**
```
Lors création plante:
  name = "Monstera Deliciosa"
  family = "Araceae"

→ Auto-generate reference = "ARAC-001" (Premier 4 lettres famille + compteur)

Counter global par famille:
  ARAC-001, ARAC-002, ARAC-003...
  FABACEAE-001, FABACEAE-002...
```

### 6️⃣ **Validation Métier**
```
Règles strictes:

Plant:
  - name: obligatoire, max 255 chars
  - location_id: optionnel, FK valide si présent
  - purchase_date: ≤ today()
  - temperature_min < temperature_max

WateringHistory:
  - date: ≤ today() (pas de dates futures)
  - amount_ml: positif ou NULL
  - plant_id: FK valide

SeasonalWatering:
  - season: 1-4 (4 saisons)
  - frequency_id: FK valide dans WateringFrequencies
  - Clé unique: (plant_id, season) - Une seule freq par saison
```

---

## ✨ FONCTIONNALITÉS IMPLÉMENTÉES vs À FAIRE

### ✅ **PRIORITÉ 1 - CORE FONCTIONNALITÉS (98% COMPLÈTES)**

#### 1.1 CRUD Plantes
- [x] **POST /api/plants** - Créer plante
- [x] **GET /api/plants** - Lister plantes (avec pagination, filtres, recherche)
- [x] **GET /api/plants/{id}** - Détails plante
- [x] **PUT /api/plants/{id}** - Mettre à jour plante
- [x] **DELETE /api/plants/{id}** - Archiver plante (soft delete)
- [x] **GET /api/plants?is_archived=false** - Lister actives
- [x] **GET /api/plants?is_archived=true** - Lister archivées
- [x] **POST /api/plants/{id}/restore** - Restaurer plante

#### 1.2 Historiques Complets
- [x] **POST /api/plants/{id}/watering-history** - Enregistrer arrosage
- [x] **GET /api/plants/{id}/watering-history** - Lister arrosages
- [x] **POST /api/plants/{id}/fertilizing-history** - Enregistrer fertilisation
- [x] **GET /api/plants/{id}/fertilizing-history** - Lister fertilisations
- [x] **POST /api/plants/{id}/repotting-history** - Enregistrer rempotage
- [x] **GET /api/plants/{id}/repotting-history** - Lister rempotages
- [x] **POST /api/plants/{id}/disease-history** - Enregistrer maladie
- [x] **GET /api/plants/{id}/disease-history** - Lister maladies
- [x] **POST /api/plants/{id}/plant-history** - Ajouter note générale
- [x] **GET /api/plants/{id}/plant-history** - Lister notes

#### 1.3 Gestion Saisonnière
- [x] **GET /api/plants/{id}/seasonal-watering** - Fréquences saison
- [x] **PUT /api/plants/{id}/seasonal-watering** - Mettre à jour fréquences
- [x] **GET /api/plants/{id}/seasonal-fertilizing** - Fréquences fertilisation
- [x] **PUT /api/plants/{id}/seasonal-fertilizing** - Mettre à jour fréquences

#### 1.4 Photos
- [x] **POST /api/plants/{id}/photos** - Upload photo
- [x] **GET /api/plants/{id}/photos** - Lister photos
- [x] **PUT /api/photos/{id}/set-primary** - Définir photo principale
- [x] **DELETE /api/plants/{id}/photos/{photo_id}** - Supprimer photo
- [x] Auto-conversion WebP (quality=85)
- [x] Génération thumbnails

#### 1.5 Statistiques & Dashboard
- [x] **GET /api/statistics/upcoming-waterings** - Plantes à arroser
- [x] **GET /api/statistics/plants-by-location** - Grouper par pièce
- [x] **GET /api/statistics/health-status** - Distribution santé

#### 1.6 Lookups (Paramètres)
- [x] **GET /api/locations** - Lister pièces
- [x] **POST /api/locations** - Ajouter pièce
- [x] **GET /api/purchase-places** - Lister sources
- [x] **POST /api/purchase-places** - Ajouter source
- [x] **GET /api/fertilizer-types** - Types engrais
- [x] **GET /api/soil-types** - Types terreau
- [x] **GET /api/diseases** - Maladies
- [x] **GET /api/treatments** - Traitements
- [x] **GET /api/tags** - Tags

#### 1.7 Recherche & Filtres
- [x] **GET /api/plants?search=monstera** - Recherche par nom
- [x] **GET /api/plants?location_id=5** - Filtrer par pièce
- [x] **GET /api/plants?is_archived=false** - Filtrer archivées
- [x] **GET /api/plants?difficulty_level=EASY** - Filtrer par niveau
- [x] **GET /api/plants?page=1&limit=10** - Pagination

### 🟡 **PRIORITÉ 2 - AMÉLIORATIONS (50-80% COMPLÈTES)**

#### 2.1 Export/Import
- [ ] **GET /api/export/csv** - Exporter plantes en CSV
- [ ] **GET /api/export/json** - Exporter plantes en JSON
- [ ] **POST /api/import** - Importer plantes (JSON/CSV)
- [ ] ZIP avec photos + métadonnées
- [ ] Checksum SHA256 pour intégrité

#### 2.2 Validation Côté Frontend
- [ ] **Zod Schema** - Validation formules
- [ ] Messages d'erreur détaillés (inline)
- [ ] Validation temps-réel
- [ ] Indicateurs obligatoire/optionnel

#### 2.3 Components Frontend Avancés
- [ ] **HistoryTimeline** - Timeline visuelle historiques
  - Timeline verticale
  - Cards par type (couleurs)
  - Filtres par type d'événement
- [ ] **PhotoGallery Amélioré**
  - Drag-drop upload
  - Lazy loading images
  - Lightbox/modal
  - Rotation images
- [ ] **Dashboard KPIs**
  - Graphiques arrosages
  - Statistiques santé
  - Prévisions

#### 2.4 Tests E2E (Cypress/Playwright)
- [ ] CRUD plantes complètes
- [ ] Upload photos
- [ ] Formulaires validation
- [ ] Navigation pages
- [ ] Responsive design

### ❌ **PRIORITÉ 3 - FUTUR (À PLANIFIER)**

- [ ] Notifications/rappels (email, SMS, web push)
- [ ] Synchronisation cloud
- [ ] Mode hors-ligne (offline-first)
- [ ] API GraphQL
- [ ] Mobile app native (React Native)
- [ ] Partage de collections (collaboration)
- [ ] IA identification plantes (photos)

---

## 📈 PLAN D'ACTION IMMÉDIATES (SEMAINE 1)

### **ÉTAPE 1: Fixer 7 tests échoués** (2-3h) 🔴 URGENT
**Fichier:** `backend/tests/test_settings_routes_integration.py`

**Problème:** 7 tests en erreur  
**Résultat attendu:** 186 tests passants (au lieu de 179)  
**Coverage impact:** 81% → 82%+

**À faire:**
1. Vérifier endpoints `GET /api/settings/{type}/{id}` (locations, purchase-places)
2. Vérifier format réponses `POST /api/settings/*` (tags, diseases)
3. Vérifier seed données (diseases, treatments en BD)
4. Corriger format réponses JSON (structure attendue)

```bash
# Test et voir erreurs
cd backend && pytest tests/test_settings_routes_integration.py -v

# Lancer seed pour avoir données
python app/scripts/seed_plants.py
```

---

### **ÉTAPE 2: Intégrer lookup_routes.py** (1-2h) 🟡 IMPORTANT
**Fichier:** `backend/app/routes/lookup_routes.py`

**Problème:** 
- Route file existe mais jamais enregistré dans `main.py`
- 126 lignes de code sans couverture (0%)
- Endpoints lookup pas testés

**À faire:**
1. Vérifier si route file doit être utilisé (check commits history)
2. Importer et enregistrer dans `main.py`:
```python
from app.routes import lookup_routes
app.include_router(lookup_routes.router, prefix="/api")
```
3. Créer tests d'intégration pour endpoints lookup
4. Vérifier endpoints fonctionnent (GET /api/locations, /api/tags, etc.)

**Coverage impact:** 82% → 85%+

---

### **ÉTAPE 3: Compléter tests histories.py** (2-3h) 🟡 IMPORTANT
**Fichier:** `backend/app/services/history_service.py`

**Problème:** Couverture 55% (beaucoup de branches non testées)

**À faire:**
1. Tests chaque type historique:
   - WateringHistory: create, read, update, delete, list
   - FertilizingHistory: même pattern
   - RepottingHistory: même pattern
   - DiseaseHistory: même pattern
   - PlantHistory: même pattern
2. Tester cas d'erreur:
   - Plant not found
   - Invalid dates (future dates)
   - Invalid data (amount < 0, etc.)
3. Tester edge cases:
   - Soft delete (deleted_at not null)
   - Query ordering

**Coverage impact:** 85% → 88%+

```bash
cd backend
# Générer rapport coverage
pytest tests/test_history_service.py --cov=app.services.history_service --cov-report=html
```

---

### **ÉTAPE 4: Phase 5B - Tests Frontend** (4-5h) 🟢 NEXT WEEK
**Fichier:** `frontend/src/__tests__/unit/HomePage.test.jsx`

**28 tests prêts**, exécuter avec:
```bash
cd frontend
npm test -- HomePage.test.jsx --coverage
```

**Coverage impact:** 52% → 58%+

---

## 🎯 ÉTAT ACTUEL (Phase 5A)

| Métrique | Valeur | Status |
|----------|--------|--------|
| **Couverture tests** | 52% | 🟢 Phase 5A terminée |
| **Tests backend** | 28/32 (87.5%) | ✅ 4 skipped (DB fixtures) |
| **Tests frontend** | 28 prêts | 📋 À exécuter |
| **Phase 4 baseline** | 51% | ✅ Référence |
| **Cible Phase 5B** | 58% (+6%) | 🎯 Next |
| **Cible Phase 5C** | 95% (+37%) | 🎯 Final |

---

## 🔧 COMMANDES UTILES

```bash
# 🏃 Lancer l'app complète
cd backend && python -m uvicorn app.main:app --reload &
cd frontend && npm run dev

# 🧪 Tests backend
cd backend
pytest                                          # Tous les tests
pytest tests/test_coverage_gaps.py -v           # Gap tests
pytest tests/test_settings_routes_integration.py -v  # Settings tests
pytest --cov=app --cov-report=html              # Avec couverture

# 🎨 Tests frontend
cd frontend
npm test                                        # Tous les tests
npm test -- HomePage.test.jsx                   # Composant spécifique
npm test -- --coverage                          # Avec couverture
npm run build                                   # Build Vite

# 🗄️ Base de données
cd backend
alembic upgrade head                            # Migrer BD
python app/scripts/seed_plants.py               # Seeder données
```

---

## 📚 DOCUMENTS DE RÉFÉRENCE

- **README.md** - Overview projet & setup
- **DEMARRER_ICI.md** - Guide de démarrage complet
- **docs/INDEX.md** - Index documentation
- **PHASE_5_ROADMAP.md** - Stratégie coverage (51% → 95%)
- **PHASE_5B_QUICK_START.md** - Prochaines étapes détaillées
- **FIN_DE_CHANTIER_PHASE_5A.md** - Session closure report

---

## ✅ CHECKLIST DÉVELOPPEUR

Avant de commencer une tâche:

- [ ] Lire le cahier des charges (ce doc)
- [ ] Comprendre la logique métier associée
- [ ] Consulter modèles (`app/models/`)
- [ ] Vérifier endpoints existants (`app/routes/`)
- [ ] Écrire tests AVANT code
- [ ] Valider en local (`pytest`)
- [ ] Committer avec message clair

---

**💡 Questions? Consulte les docs ou lance l'app et teste!**

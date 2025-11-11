# 🔍 Audit Complet: Tables & Logique Métier

## 📊 État Actuel de la Base de Données

### ✅ Tables Existantes (18 tables)

```
1. PLANTS (41 colonnes)
   ├─ Basic: name, scientific_name, family, genus, species
   ├─ Description: description, health_status, difficulty_level
   ├─ Location: location_id, purchase_date, purchase_place_id
   ├─ Environment: temperature, humidity, soil_type, pot_size
   ├─ Flags: is_indoor, is_outdoor, is_favorite, is_toxic, is_archived
   └─ NO: parent_plant_id ❌ (manque pour relation mère/fille)

2. WATERING_HISTORIES (8 colonnes)
   ├─ plant_id (FK)
   ├─ date, notes, water_type_id, watering_method_id
   └─ Tracks: quand on a arrosé

3. FERTILIZING_HISTORIES (9 colonnes)
   ├─ plant_id (FK)
   ├─ date, fertilizer_type_id, amount, notes
   └─ Tracks: quand on a fertilisé

4. REPOTTING_HISTORIES (10 colonnes)
   ├─ plant_id (FK)
   ├─ date, soil_type, pot_size_before/after, notes
   └─ Tracks: quand on a rempoté

5. DISEASE_HISTORIES (12 colonnes)
   ├─ plant_id (FK)
   ├─ date, disease_type_id, treatment_type_id, notes
   └─ Tracks: maladies et traitements

6. PLANT_HISTORIES (9 colonnes)
   ├─ plant_id (FK)
   ├─ date, title, note, category
   └─ Tracks: événements généraux (notes libres)

7. PHOTOS (9 colonnes)
   ├─ plant_id (FK), filename, file_size, width, height
   ├─ is_primary, created_at, updated_at
   └─ Stores: metadata de photos (fichiers dans /data/photos/{plant_id}/)

8. PLANT_TAG (2 colonnes)
   ├─ plant_id (FK), tag_id (FK)
   └─ M2M: relation plante ↔ tags

9. PLANT_SEASONAL_WATERING (6 colonnes)
   ├─ plant_id (FK), season_id (FK), watering_frequency_id (FK)
   └─ Stores: fréquence d'arrosage par saison

10. PLANT_SEASONAL_FERTILIZING (6 colonnes)
    ├─ plant_id (FK), season_id (FK), fertilizer_frequency_id (FK)
    └─ Stores: fréquence de fertilisation par saison

11-20. LOOKUP TABLES (8 tables)
    ├─ LOCATIONS (où sont les plantes)
    ├─ PURCHASE_PLACES (où acheter)
    ├─ WATERING_FREQUENCIES (fréquences)
    ├─ FERTILIZER_FREQUENCIES (fréquences)
    ├─ WATERING_METHODS (spray, soil, etc)
    ├─ WATER_TYPES (tap, distilled, rainwater)
    ├─ LIGHT_REQUIREMENTS (full sun, partial shade, etc)
    ├─ DISEASE_TYPES (list des maladies)
    ├─ TREATMENT_TYPES (treatments possibles)
    ├─ FERTILIZER_TYPES (engrais)
    ├─ SEASONS (été, hiver, etc)
    └─ TAG_CATEGORIES + TAGS (25+ catégories, 67+ tags)

21. AUDIT_LOGS (14 colonnes)
    ├─ action (create/update/delete)
    ├─ entity_type, entity_id, field_name
    ├─ old_value, new_value, user_id, timestamp
    └─ Tracks: TOUTES les modifications
```

---

## ❌ RELATION PARENT/CHILD: ABSENTE

### Le Problème

**Actuellement:**
```sql
Plants table:
├─ Plant #1 (Monstera - mère)
├─ Plant #2 (Mondi - fille de #1)
└─ Plant #3 (Mondi #2 - fille de #1)

Mais AUCUN lien entre eux! ❌
```

**Cas d'usage manquant:**
```
1. Je prends une bouture de ma Monstera (Plant #1)
   → Crée Plant #2
   → Devrait tracker: "Plant #2 vient de Plant #1"

2. Je peux voir l'historique familial:
   Plant #1 (original)
   ├─ Plant #2 (bouture 2024)
   ├─ Plant #3 (bouture 2024)
   └─ Plant #4 (bouture 2025)

3. Si Monstera #1 meurt:
   → Je vois que Plant #2-4 sont toujours vivantes
   → Statistique: "85% de survie avec cette méthode"
```

---

## 🔧 Ce Qui Existe pour Suivre la Propagation

### 1. ❌ Pas de Table CUTTINGS ou PROPAGATIONS
```
Manque:
- PlantCutting (source_plant, date, method)
- CuttingHistory (timeline: rooted, ready-to-pot, etc)
```

### 2. ✅ PLANT_HISTORIES (peut servir partiellement)
```
Table existante:
- plant_id (FK)
- date
- title (ex: "Bouture de Monstera")
- note (ex: "Petites racines apparues")
- category (ex: "propagation")

Limitation: C'est juste des notes, pas de vraies tracking
- Pas de "plant_source_id"
- Pas de statut standardisé (rooting/ready-to-pot/etc)
- Pas d'estimateur de prêt
```

### 3. ✅ PHOTOS avec relationship
```
Peut documenter:
- Photo avant prélèvement
- Photo du bouturage en cours
- Photo des racines qui apparaissent
- Photo dans le nouveau pot

Limitation: Juste visuel, pas de logique
```

### 4. ✅ AUDIT_LOGS (peut tracer origine)
```
Quand on crée Plant #2 depuis Plant #1:
- AUDIT_LOGS enregistrerait la création
- Mais PAS le lien parent/child

Limitation: Pas de relation structurée
```

---

## 📈 Logique Métier Existante vs Manquante

### ✅ CE QUI FONCTIONNE BIEN

```
1. ARROSAGE/FERTILISATION
   ├─ Historique complet par plante
   ├─ Fréquences saisonnières
   ├─ Alertes quand arroser
   ├─ Calendrier mensuel
   └─ Stats par plante (OK ✓)

2. SANTÉ DES PLANTES
   ├─ Health status (healthy/sick/recovering/dead)
   ├─ Maladies + traitement tracking
   ├─ Historique des modifications
   └─ Stats globales (OK ✓)

3. PHOTOS
   ├─ Upload avec compression WebP
   ├─ Multi-versions (full/medium/thumb)
   ├─ Primary photo flag
   ├─ Galerie par plante
   └─ Serving optimisé (OK ✓)

4. CONFIGURATION
   ├─ 25+ catégories de tags
   ├─ 67+ tags spécifiques
   ├─ Lookup tables (lieux, fréquences, etc)
   ├─ Saisonnalité (été/hiver/printemps/automne)
   └─ Tous les paramètres (OK ✓)

5. AUDIT
   ├─ Traçage de TOUTES les modifications
   ├─ Qui a changé quoi et quand
   ├─ Historique complet
   └─ Dashboard audit (OK ✓)
```

### ❌ CE QUI MANQUE

```
1. RELATION PARENT/CHILD
   ├─ NO parent_plant_id column
   ├─ NO propagation table
   ├─ NO genealogy tracking
   ├─ NO "family tree"
   └─ NEED: Database schema update

2. CUTTINGS/PROPAGATION WORKFLOW
   ├─ NO cutting creation
   ├─ NO progress tracking (rooting → ready-to-pot)
   ├─ NO timeline of events
   ├─ NO conversion logic (cutting → plant)
   └─ NEED: New table + service logic

3. ENCYCLOPEDIA
   ├─ NO 1000+ plant database
   ├─ NO search API
   ├─ NO plant matching
   ├─ NO care instructions
   └─ NEED: New table + data seeding

4. NOTIFICATIONS
   ├─ NO email sending
   ├─ NO push notifications
   ├─ NO scheduled alerts
   ├─ NO reminder system
   └─ NEED: Integration (Mailgun, Firebase, etc)

5. ADVANCED ANALYTICS
   ├─ NO ML predictions
   ├─ NO pattern detection
   ├─ NO health forecasting
   ├─ NO success rate tracking
   └─ NEED: ML service integration
```

---

## 🗂️ Structure Complète des Données

### Diagramme des Relations (simplifié)

```
PLANTS (mère)
  ├─ WATERING_HISTORIES
  ├─ FERTILIZING_HISTORIES
  ├─ REPOTTING_HISTORIES
  ├─ DISEASE_HISTORIES
  ├─ PLANT_HISTORIES
  ├─ PHOTOS
  ├─ PLANT_TAG → TAGS
  ├─ PLANT_SEASONAL_WATERING → SEASONS + WATERING_FREQUENCIES
  ├─ PLANT_SEASONAL_FERTILIZING → SEASONS + FERTILIZER_FREQUENCIES
  └─ AUDIT_LOGS (traces toutes les modifications)

LOOKUP TABLES (référentiels)
  ├─ LOCATIONS
  ├─ PURCHASE_PLACES
  ├─ WATERING_METHODS
  ├─ WATER_TYPES
  ├─ LIGHT_REQUIREMENTS
  ├─ DISEASE_TYPES
  ├─ TREATMENT_TYPES
  ├─ FERTILIZER_TYPES
  ├─ WATERING_FREQUENCIES
  ├─ FERTILIZER_FREQUENCIES
  ├─ SEASONS
  ├─ PLANT_HEALTH_STATUSES
  ├─ TAG_CATEGORIES → TAGS
  └─ FERTILIZER_TYPES
```

---

## 🚨 Ce Qu'il Faut Ajouter pour Parent/Child

### Option 1: Simple (1 colonne)

```sql
ALTER TABLE plants ADD COLUMN parent_plant_id INTEGER;
ALTER TABLE plants ADD FOREIGN KEY (parent_plant_id) REFERENCES plants(id);

-- Puis créer une relation auto-référencée:
class Plant(Base):
    parent_id = Column(Integer, ForeignKey('plants.id'))
    children = relationship("Plant", backref="parent", remote_side=[id])
```

**Avantage:** Simple, rapide (1 colonne)
**Limitation:** Pas de métadonnées (date, méthode, statut)

---

### Option 2: Complète (1 nouvelle table) ⭐ RECOMMANDÉ

```sql
CREATE TABLE plant_cuttings (
    id INTEGER PRIMARY KEY,
    parent_plant_id INTEGER NOT NULL (FK),
    child_plant_id INTEGER (FK),  -- NULL until converted
    source_type VARCHAR(50),      -- cutting/seeds/division/offset
    propagation_method VARCHAR(50), -- water/soil/air-layer
    date_harvested DATE,
    status VARCHAR(50),           -- rooting/growing/ready-to-pot/potted/failed
    days_until_ready INTEGER,
    success_rate FLOAT,           -- % of similar cuttings that survived
    notes TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE cutting_history (
    id INTEGER PRIMARY KEY,
    cutting_id INTEGER NOT NULL (FK),
    date DATE,
    event_type VARCHAR(50),  -- rooted/leaves-grown/ready-to-pot/potted
    measurement JSON,         -- {root_length_cm: 1.5, leaves_count: 3}
    notes TEXT,
    created_at DATETIME
);
```

**Avantage:** Complet, trackable, statistiques possibles
**Structure:** Permet timeline complète + success rates

---

## 📋 Checklist d'Implémentation

**Pour relation simple parent/child:**
```
[ ] 1. Migration: Ajouter parent_plant_id à PLANTS
[ ] 2. Model: Auto-relationship avec backref
[ ] 3. API: GET /api/plants/{id}/descendants
[ ] 4. API: GET /api/plants/{id}/ancestors
[ ] 5. UI: Afficher "Family tree" d'une plante
```

**Pour cutting/propagation complet:**
```
[ ] 1. Migration 010: CREATE TABLE plant_cuttings
[ ] 2. Migration 011: CREATE TABLE cutting_history
[ ] 3. Model: PlantCutting + CuttingHistory
[ ] 4. Service: CuttingService (create/update/convert)
[ ] 5. API: CRUD endpoints
[ ] 6. API: Convert cutting → plant
[ ] 7. API: Get timeline + success rate
[ ] 8. UI: Propagation dashboard
[ ] 9. Tests: 20+ test cases
```

---

## 💡 Verdict

### Tables & Logique Métier: 90% Complète ✅

**Bon:**
- 18 tables bien structurées
- Tous les lookups en place
- Historique complet pour chaque domaine
- Audit logging fonctionne
- Fréquences saisonnières fonctionnent
- Photos bien gérées

**À améliorer:**
- ❌ Relation parent/child absente (mais facile à ajouter)
- ❌ Cuttings/propagation pas d'historique structuré
- ❌ Pas d'encyclopédie 
- ❌ Pas de notification système
- ❌ Pas d'IA/ML intégration

### Effort pour Compléter

```
Parent/Child simple:      1-2 jours
Cuttings complet:         4-5 jours
Encyclopedia:             7-10 jours
Notifications:            2-3 jours
────────────────────────────────
Total pour 100% complet:  14-21 jours
```

**Conclusion:** L'app est **solide**, pas besoin de refactoriser, juste ajouter les features manquantes! 🎯


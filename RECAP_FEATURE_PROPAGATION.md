# 🌳 FEATURE PROPAGATION - Recap Complet
**11 Novembre 2025** | Sans code (Planning seulement)

---

## 📌 Vue d'Ensemble

### **Objectif Principal**
Tracker les générations de plantes via **relations mère/fille/soeur** + **source & méthode de propagation** + **calendrier dédié aux boutures**.

### **Cas d'Usage Type**
```
1. J'ai un Monstera original (mère)
2. J'ai prélevé une bouture en eau (source: cutting, method: water)
3. Elle fait 2 semaines, attend les racines (status: rooting)
4. Je veux voir l'arbre familial complet
5. Je veux estimer quand elle sera prête à rempoter
6. Je veux tracker la progression jour par jour (photos + notes)
```

---

## 🔗 LES 3 TYPES DE RELATIONS

### **1️⃣ MÈRE**
- Plante source originale
- Peut générer N enfants (filles)
- Exemple: Monstera achetée en 2020

### **2️⃣ FILLE** 
- Issue directe d'une mère (par bouturage, semis, etc.)
- Peut devenir mère à son tour
- Exemple: Bouture prélevée en Oct 2024

### **3️⃣ SOEUR**
- Partage la même mère
- Même source, possiblement même méthode
- Exemple: 3 boutures prélevées le même jour de la même mère

### **Arbre Exemple**
```
Monstera Originale (2020) = MÈRE
│
├─ Bouture #1 (Oct 2024) = FILLE 1
│  │
│  └─ Sous-bouture (Fév 2025) = PETITE-FILLE
│
└─ Bouture #2 (Dec 2024) = FILLE 2 (SOEUR de FILLE 1)
```

---

## 📦 SOURCE & MÉTHODE (4 + 4 Combinaisons)

### **4 SOURCES DE PROPAGATION**

| Source | Description | Plantes Courantes |
|--------|-------------|-------------------|
| **cutting** | Tige + feuilles prélevées | Monstera, Pothos, Hoya |
| **seeds** | Reproduction sexuée (graine) | Succulentes, Cactus |
| **division** | Séparer une plante multi-tiges | Snake Plant, Calathea |
| **offset** | Petit rejet détaché | Peperomia, Begonia |

### **4 MÉTHODES DE CULTURE**

| Méthode | Description | Durée Moyenne | Talon d'Achille |
|---------|-------------|----------------|-----------------|
| **water** | Bouteille/verre d'eau | 2-3 semaines | Pourriture, algues |
| **soil** | Terreau humidifié | 3-4 semaines | Assèchement |
| **air-layer** | Marcottage aérien | 4-6 semaines | Complexe à faire |
| **substrate** | Substrat spécialisé | 2-4 semaines | Coûteux |

### **Matrice Source × Méthode**
```
         water    soil    air-layer  substrate
cutting   ✅      ✅      ✅         ✅
seeds     ❌      ✅      ❌         ✅
division  ⚠️      ✅      ❌         ⚠️
offset    ⚠️      ✅      ❌         ✅

✅ = Optimal
⚠️ = Possible mais moins courant
❌ = Rare/inefficace
```

### **Exemples Réels par Plante**

```
MONSTERA
├─ cutting + water (2-3 sem) → Super rapide, mes favoris
├─ cutting + soil (3-4 sem) → Plus lent mais terre
└─ air-layer (4-6 sem) → Pour branches épaisses

POTHOS
├─ cutting + water (1-2 sem) → Ultra rapide
└─ cutting + soil (2-3 sem) → Plus stable

SNAKE PLANT
├─ division + soil (immédiat) → La plus rapide
└─ leaf cutting + soil (4-6 sem) → Feuille seule

PEPEROMIA
├─ offset + soil (1-2 sem) → Rejets naturels
└─ cutting + soil (2-3 sem) → Sinon bouture classique

SUCCULENTE
├─ leaf cutting + soil (3-4 sem) → Feuille seule
└─ offset + soil (2-3 sem) → Rejets prélevés
```

---

## 📅 CALENDRIER DÉDIÉ AUX BOUTURES

### **3 Niveaux de Tracking**

#### **NIVEAU 1: Relation Simple (Parent-Child)**
```
Plante: Monstera #1
├─ Enfants: [Plant #2, Plant #3, Plant #4]
└─ Arbre complet visible en 1 clic

Données stockées:
✅ parent_plant_id dans la table plants
✅ Relation 1-vers-N (1 mère → N filles)
```

#### **NIVEAU 2: Métadonnées de Bouture (What & How)**
```
Bouture: #2 (10 Oct 2024)
├─ Parent: Monstera #1
├─ Source: cutting (tige 3 feuilles)
├─ Method: water (dans verre)
├─ Date harvested: 10 Oct 2024
├─ Expected ready: 27 Oct 2024 (estimé)
├─ Status: rooting
├─ Notes: "Bonne tige, conservé 2 feuilles"
└─ Success rate: 85% (données statistiques)

Données stockées:
✅ Table PlantCutting (1 ligne = 1 bouture)
✅ Métadonnées source + méthode
✅ Estimateur de date prête
✅ Suivi du statut (rooting → growing → ready-to-pot → potted)
```

#### **NIVEAU 3: Timeline Jour par Jour (When & How Did It Go)**
```
Bouture #2 - Timeline Complète:
├─ Day 0 (10 Oct): "Prélevée et mise en eau"
│  └─ Notes: "Tige bien formée, 3 feuilles"
│
├─ Day 3 (13 Oct): "Premiers signes de roots"
│  └─ Measurement: {root_length_cm: 0.3, leaves: 3}
│  └─ Photos: [photo1.webp, photo2.webp]
│
├─ Day 7 (17 Oct): "Roots bien formées"
│  └─ Measurement: {root_length_cm: 1.2, leaves: 3, root_count: 4}
│  └─ Photo: evidence du progrès
│
├─ Day 10 (20 Oct): "Nouvelle feuille!"
│  └─ Event: "leaves-grown"
│  └─ Measurement: {root_length_cm: 1.5, leaves: 4}
│
├─ Day 14 (24 Oct): "READY-TO-POT"
│  └─ Event: "ready-to-pot"
│  └─ Status: "Transition vers terre"
│
└─ Day 20 (30 Oct): "Rempoté en substrat"
   └─ Event: "potted"
   └─ Status: "Plante indépendante"
   └─ Result: ✅ SUCCESS

Données stockées:
✅ Table CuttingHistory (N lignes = N étapes)
✅ Date, événement, mesures (JSON)
✅ Notes et photos pour chaque étape
✅ Détection automatique des problèmes (pourriture, stagnation)
```

---

## 🎯 FONCTIONNALITÉS CLÉS

### **Pour l'Utilisateur**

| Feature | Description | Utilité |
|---------|-------------|---------|
| **Arbre Familial** | Vue graphique des générations | Visualiser tout en 1 clic |
| **Filtre Filles** | Voir tous les enfants d'une mère | "Combien de boutures du Monstera?" |
| **Filtre Soeurs** | Voir les boutures même-jour | "Lesquelles sont nées ensemble?" |
| **Statut Bouture** | rooting → growing → ready-to-pot → potted | Savoir où on en est |
| **Estimateur** | "Prête le 27 Oct" (basé sur source + méthode) | Planifier le rempotage |
| **Timeline** | Voir toutes les étapes jour par jour | Apprendre des patterns |
| **Success Rate** | % de réussite par source + méthode | "water ou soil? Meilleur taux?" |
| **Calendrier** | Vue mensuelle de toutes les boutures | "Beaucoup de travail ce mois?" |
| **Statistiques** | Combien en rooting? Combien prêtes? | Résumé rapide |

### **Vue Calendrier Spécifique**

```
NOVEMBRE 2025
Boutures en cours:

  1  2  3  4  5  6  7
              |------ Monstera (water) day 2 [🌱 rooting]
     |------- Pothos (soil) day 8 [🌿 growing]

  8  9 10 11 12 13 14
     |-------- Hoya (air-layer) day 15 [🌿 growing]
                          |--- Peperomia (soil) day 1 [🌱 rooting]

 15 16 17 18 19 20 21
                   ✅ Monstera ready-to-pot!

 22 23 24 25 26 27 28
  ✅ Pothos ready!

 29 30
  
STATUT: 7 boutures actives | 2 prêtes | 0 échouées | 85% succès
```

---

## 💾 ARCHITECTURE DE BASE DE DONNÉES

### **Table Existante: PLANTS (Légère Extension)**
```sql
plants table (AVANT):
├─ id
├─ name
├─ scientific_name
├─ ... (41 colonnes)
└─ created_at

plants table (APRÈS):
├─ id
├─ name
├─ scientific_name
├─ ... (41 colonnes)
├─ parent_plant_id ← NEW (FK vers plants.id)
└─ created_at

Impact: 1 colonne ajoutée (nullable)
Compatibilité: 100% backward compatible
```

### **Nouvelle Table 1: PLANT_CUTTINGS**
```sql
CREATE TABLE plant_cuttings (
    id INTEGER PRIMARY KEY,
    parent_plant_id INTEGER NOT NULL,           -- FK plants(id)
    source_type VARCHAR(50) NOT NULL,           -- "cutting", "seeds", "division", "offset"
    method VARCHAR(50) NOT NULL,                -- "water", "soil", "air-layer", "substrate"
    date_harvested DATETIME NOT NULL,           -- Quand prélevée
    expected_ready DATETIME,                    -- Estimation prête (basée sur source+method)
    status VARCHAR(50) DEFAULT 'rooting',       -- rooting, growing, ready-to-pot, potted, failed
    success_rate_estimate FLOAT DEFAULT 0.85,   -- % estimé de succès pour ce type/method
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

Exemple:
┌─────┬──────────────────┬────────┬─────────┬───────────────┬────────────────┬──────────────────┐
│ id  │ parent_plant_id  │ source │ method  │ date_harvested│ expected_ready │ status           │
├─────┼──────────────────┼────────┼─────────┼───────────────┼────────────────┼──────────────────┤
│ 1   │ 5 (Monstera)     │ cutting│ water   │ 2025-11-01    │ 2025-11-18     │ rooting          │
│ 2   │ 5 (Monstera)     │ cutting│ water   │ 2025-11-01    │ 2025-11-18     │ rooting          │
│ 3   │ 12 (Pothos)      │ cutting│ soil    │ 2025-11-05    │ 2025-11-28     │ growing          │
└─────┴──────────────────┴────────┴─────────┴───────────────┴────────────────┴──────────────────┘

Colonnes clés:
✅ Lien parent: parent_plant_id (FK)
✅ Source: "cutting", "seeds", "division", "offset"
✅ Méthode: "water", "soil", "air-layer", "substrate"
✅ Timeline: date_harvested + expected_ready
✅ État: status (4 étapes)
✅ Estimateur: expected_ready (calculé auto)
✅ Taux: success_rate_estimate (pour stats)
```

### **Nouvelle Table 2: CUTTING_HISTORY**
```sql
CREATE TABLE cutting_history (
    id INTEGER PRIMARY KEY,
    cutting_id INTEGER NOT NULL,                -- FK plant_cuttings(id)
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event VARCHAR(50) NOT NULL,                 -- "rooted", "leaves-grown", "ready-to-pot", "potted", "failed"
    measurement JSON,                           -- {root_length_cm: 1.5, leaves: 3, root_count: 4, health: "good"}
    notes TEXT,                                 -- "Première racine visible!"
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cutting_id) REFERENCES plant_cuttings(id) ON DELETE CASCADE
);

Exemple:
┌─────┬────────────┬─────────────────┬──────────────┬──────────────────────────────────────┬──────────────┐
│ id  │ cutting_id │ date            │ event        │ measurement                          │ notes        │
├─────┼────────────┼─────────────────┼──────────────┼──────────────────────────────────────┼──────────────┤
│ 1   │ 1          │ 2025-11-01      │ rooted       │ {root_length: 0}                     │ Prélevée     │
│ 2   │ 1          │ 2025-11-04      │ rooted       │ {root_length: 0.3, roots: 1}        │ Première!    │
│ 3   │ 1          │ 2025-11-07      │ rooted       │ {root_length: 1.2, roots: 4}        │ Racines OK   │
│ 4   │ 1          │ 2025-11-10      │ leaves-grown │ {root_length: 1.5, roots: 4, leaves:4}│ Feuille+    │
│ 5   │ 1          │ 2025-11-14      │ ready-to-pot │ {root_length: 2.0, roots: 5, leaves:4}│ PRÊTE!       │
└─────┴────────────┴─────────────────┴──────────────┴──────────────────────────────────────┴──────────────┘

Colonnes clés:
✅ Lien cutting: cutting_id (FK)
✅ Date: tracke automatiquement chaque étape
✅ Événement: "rooted", "leaves-grown", "ready-to-pot", "potted", "failed"
✅ Mesures: JSON avec root_length, leaves, roots, health
✅ Notes: observation libre de l'utilisateur
✅ Photos: rattachées via photo_id (ou table de liaison)
```

### **Relation aux Photos**
```
Photos existantes:
├─ plant_id → Photos de la plante finale

Photos de progression:
├─ cutting_id → Photos de chaque étape de la bouture
└─ cutting_history_id → Rattachées à une étape spécifique

Exemple:
Plant #2 (bouture prête-à-pot)
├─ Photos finales: [photo1.webp, photo2.webp]
└─ Timeline avec photos:
   ├─ Day 0: [bouture_initiale.webp]
   ├─ Day 3: [premières_racines.webp]
   ├─ Day 7: [racines_formées.webp]
   ├─ Day 10: [nouvelle_feuille.webp]
   └─ Day 14: [prête_à_rempoter.webp]
```

---

## 🔌 ENDPOINTS API (Propulsés par le Calendar)

### **Relations Parent-Child (Arbre Familial)**
```
GET    /api/plants/{id}/children              → Voir tous les enfants
GET    /api/plants/{id}/siblings              → Voir les soeurs
GET    /api/plants/{id}/genealogy             → Arbre complet (ancestors + descendants)
GET    /api/plants/{id}/family-tree           → Visualisation (JSON pour graphe)
```

### **Cuttings Management (Métadonnées)**
```
POST   /api/plants/{id}/cuttings              → Créer bouture (source, method, date)
GET    /api/cuttings                          → Toutes les boutures
GET    /api/cuttings/{id}                     → Détails 1 bouture
PATCH  /api/cuttings/{id}                     → Update status, notes
DELETE /api/cuttings/{id}                     → Supprimer
```

### **Timeline Tracking (Progression)**
```
POST   /api/cuttings/{id}/timeline            → Ajouter étape (event, mesures, notes)
GET    /api/cuttings/{id}/timeline            → Toute la timeline
GET    /api/cuttings/{id}/timeline/{step_id}  → 1 étape spécifique
```

### **Calendar & Statistics (Vue Calendrier)**
```
GET    /api/cuttings/calendar/{year}/{month}  → Boutures du mois (pour affichage)
GET    /api/cuttings/summary                  → Résumé: en_rooting, growing, ready, potted, failed
GET    /api/cuttings/stats                    → Taux de succès, durée moyenne, par source+method
GET    /api/cuttings/readiness                → "Prêtes à rempoter cette semaine?" 
```

### **Photos intégrées**
```
POST   /api/cuttings/{id}/timeline/{step}/photo  → Ajouter photo à une étape
GET    /api/cuttings/{id}/timeline/{step}/photo  → Photos de cette étape
```

---

## 🖼️ INTERFACE UTILISATEUR

### **Écrans Principaux (10+ pages)**

1. **Dashboard Propagation**
   - Résumé: N en rooting, N growing, N prêtes
   - Prochaines prêtes: "Monstera prête le 27 Nov"
   - Dernier ajout: "Hoya ajoutée hier"

2. **Arbre Familial (Graphique)**
   - Vue visuelle: Parent au centre, enfants autour
   - Clic = voir détails
   - Filtre par année, par succès

3. **Liste des Boutures**
   - Tableau avec colonnes: Parent, Source, Method, Status, Date, %
   - Filtre: source, method, status
   - Sort: par date, par durée restante

4. **Détail Bouture**
   - Metadata: parent, source, method, dates
   - Timeline: chaque étape avec dates
   - Photos: progressivité jour par jour
   - Notes: libre

5. **Calendrier Mensuel**
   - Vue Monsanto: chaque bouture = barre
   - Cliquer = voir détails
   - Colorer par statut (rooting=bleu, ready=vert)

6. **Statistiques**
   - Taux réussite par source (cutting/seeds/etc)
   - Taux réussite par méthode (water/soil/etc)
   - Durée moyenne avant "ready-to-pot"
   - Graphiques temporels

7. **Paramètres & Estimateurs**
   - Durée estimée par (source, method)
   - Taux de succès par (source, method)
   - Éditables si l'utilisateur veut correction

8. **Timeline Détaillée**
   - Vue scrollable: jour par jour
   - Photos intégrées
   - Notes et mesures
   - Événements clés colorés

9. **Export & Analytics**
   - CSV des boutures
   - Statistiques printables
   - Partage arbre familial

10. **Notifications**
    - "Bouture prête à rempoter demain"
    - "Pas de roots après 10 jours - problème?"

---

## ⏱️ EFFORT ESTIMÉ

### **Répartition par Phase**

| Phase | Composant | Effort | Notes |
|-------|-----------|--------|-------|
| **1** | Database (Migration Alembic) | 30 min | Ajouter parent_plant_id + 2 tables |
| **2** | Models (SQLAlchemy) | 30 min | PlantCutting + CuttingHistory |
| **3** | Services | 45 min | Logique estimateur, success rates |
| **4** | API Endpoints | 1h | 15-20 endpoints CRUD |
| **5** | Tests (Backend) | 1h | API tests, timeline tests |
| **6** | Frontend Dashboard | 1h 30 | Résumé, stats, listes |
| **7** | Frontend Détails | 1h | Bouture individual, timeline |
| **8** | Frontend Calendrier | 1h | Vue Gantt-like |
| **9** | Frontend Arbre Familial | 1h 30 | Graphe visuel (D3 ou Cytoscape) |
| **10** | Frontend Photos Timeline | 1h | Intégration images |
| **11** | Tests (Frontend) | 1h | Components, intégrations |
| **12** | Polishing | 1h | Edge cases, error handling |

### **Total Estimé: 12 heures**
- **MVP (Backend seul):** 3.5 heures
- **MVP + Dashboard simple:** 5-6 heures  
- **Complet (avec arbre + calendrier):** 12-14 heures

---

## 🎓 Exemple Concret: Monstera Deliciosa

### **Scénario Réel**
```
11 NOV 2025: J'achète un Monstera (Plant #1 - MÈRE)

15 NOV 2025: Je prélève 3 boutures
└─ Bouture #1: tige 3 feuilles + eau (expected: 2 Nov)
└─ Bouture #2: tige 2 feuilles + eau (expected: 2 Nov)
└─ Bouture #3: tige 3 feuilles + sol (expected: 3 Nov)

TIMELINE BOUTURE #1:
├─ 15 Nov: "Mise en eau"                   [Photo 1]
├─ 18 Nov: "Petites racines (3mm)"         [Photo 2]
├─ 22 Nov: "Racines formées (1cm)"         [Photo 3]
├─ 25 Nov: "Nouvelle feuille! 🎉"          [Photo 4]
├─ 29 Nov: "READY-TO-POT"                   [Photo 5]
└─ 02 Déc: "Rempoté en substrat (Plant #2)" [Photo 6]

RÉSULTAT:
✅ Monstera #2 créée
   ├─ parent_plant_id = 1
   ├─ status = "independent"
   └─ durée réelle = 17 jours (estimé: 15)

CALENDRIER NOV 2025:
┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│  │  │  │  │  │B1◄─┬─┐ ├──┤B1 ready│  │  │  │
│  │  │  │  │  │    │ └──B2◄─┬──┤  B2 │  │  │
│  │  │  │  │  │B3◄──────────┬──┤  │  │  │  │
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

STATS:
- 3 boutures lancées
- 2 réussies, 1 en attente
- Durée moyenne: 18 jours
- Taux succès (water): 100%
- Taux succès (soil): 0% (1 seule, à confirmer)
```

---

## ✅ Points Clés à Retenir

### **Techniquement**
- ✅ 3 niveaux de données (relation simple → metadata → timeline)
- ✅ 2 nouvelles tables (PlantCuttings + CuttingHistory)
- ✅ 1 colonne parent_plant_id dans plants
- ✅ 15-20 endpoints API
- ✅ 10+ pages frontend

### **Fonctionnellement**
- ✅ 4 types propagation (cutting, seeds, division, offset)
- ✅ 4 méthodes culture (water, soil, air-layer, substrate)
- ✅ 3 types relations (mère, fille, soeur)
- ✅ Timeline jour-par-jour avec photos
- ✅ Estimateur date prête (auto)
- ✅ Taux succès par source × méthode
- ✅ Calendrier dédié (vue mensuelle)
- ✅ Arbre familial (graphe visuel)

### **Pour l'Utilisateur**
- ✅ Tracker 1 ou 100 boutures en parallèle
- ✅ Voir l'arbre familial complet
- ✅ Documenter chaque étape (photo + notes)
- ✅ Apprendre des patterns (meilleure méthode?)
- ✅ Planifier (quand prête à rempoter?)
- ✅ Analyser (succès par source/méthode)

---

## 📋 Statut: PLANNING COMPLET, PRÊT À CODER

**Documenté:**
- ✅ Architecture de base de données (2 tables)
- ✅ Endpoints API (15-20)
- ✅ Pages Frontend (10+)
- ✅ Effort estimé (12 heures)
- ✅ Exemples concrets
- ✅ Cas d'usage

**Pas de code:**
- ❌ Aucune ligne implémentée
- ❌ Aucun test écrit
- ❌ Aucun composant frontend

**Prêt à démarrer** dès que "go!" 🚀

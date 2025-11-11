# 📝 RECAP SIMPLE: À IMPLÉMENTER PROPAGATION

**11 Novembre 2025** | Version ultra-synthétique (2 minutes de lecture)

---

## 🎯 RÉSUMÉ EN UNE PHRASE

Tracker les générations de plantes (mère→fille→petite-fille) avec timeline photo jour-par-jour, estimateurs automatiques et arbre généalogique visuel.

---

## 🗄️ DATABASE: 2 TABLES À CRÉER

### **Table 1: plant_propagations** (métadonnées)
```
parent_plant_id  ← La mère
child_plant_id   ← La fille (NULL si pas encore convertie)
source_type      ← "cutting" | "seeds" | "division" | "offset"
method           ← "water" | "soil" | "air-layer" | "substrate"
status           ← 9 états: pending → rooting → rooted → growing → ready-to-pot → potted → established
date_harvested   ← Quand prélevée
expected_ready   ← Auto-calculé (ex: 14 jours pour cutting+water)
current_root_length_cm, current_leaves_count, current_roots_count ← Mesures progressives
notes            ← Libre
success_rate_estimate ← 85% (auto basé sur type+method)
```

### **Table 2: propagation_events** (timeline jour-par-jour)
```
propagation_id
event_date       ← Date de l'événement
event_type       ← "rooted" | "leaves-grown" | "potted" | "failed"
measurement      ← JSON: {root_length_cm: 1.5, leaves: 3, roots: 4}
notes            ← "Première racine!" 
photo_url        ← Lien image
```

---

## 🔌 API: 19 ENDPOINTS

### **Basiques (CRUD)**
```
POST   /api/plants/{id}/propagations              → Créer bouture
GET    /api/plants/{id}/propagations              → Lister boutures mère
GET    /api/propagations/{id}                     → Détails 1 bouture
PATCH  /api/propagations/{id}                     → Modifier status/notes
DELETE /api/propagations/{id}                     → Supprimer
```

### **Timeline**
```
POST   /api/propagations/{id}/events              → Logger étape (rooted, leaves-grown, potted)
GET    /api/propagations/{id}/events              → Voir timeline complète
```

### **Conversion**
```
POST   /api/propagations/{id}/convert-to-plant    → Bouture → Plant #5
POST   /api/plants/{id}/propagations/immediate    → Division (plante créée immédiatement)
```

### **Généalogie**
```
GET    /api/plants/{id}/genealogy                 → Arbre complet (ancêtres + descendants)
GET    /api/plants/{id}/genealogy/graph           → JSON pour D3.js (nodes + edges)
```

### **Statistiques & Alertes**
```
GET    /api/plants/{id}/propagations/stats        → Taux succès, durée moyenne, par method
GET    /api/propagations/alerts                   → "Prête demain?", "Pas de racines depuis 30j?"
GET    /api/plants/{id}/propagation-recommendations → "Meilleure méthode pour cette plante?"
```

### **Calendrier & Export**
```
GET    /api/propagations/calendar/{year}/{month}  → Vue mensuelle
GET    /api/propagations/export?format=csv        → Exporter données
```

### **Batch**
```
POST   /api/plants/{id}/propagations/batch        → Créer 5 boutures en une fois
```

---

## 🐍 MODELS: 2 CLASSES

### **PlantPropagation**
```python
class PlantPropagation:
    parent_plant_id
    child_plant_id
    source_type
    method
    status
    date_harvested
    expected_ready
    current_root_length_cm
    current_leaves_count
    current_roots_count
    notes
    success_rate_estimate
    
    # Properties utiles
    @property days_since_harvest() → int
    @property is_overdue() → bool
    @property progress_percentage() → float
    
    # Relations
    parent_plant → Plant
    child_plant → Plant
    events → [PropagationEvent]
```

### **PropagationEvent**
```python
class PropagationEvent:
    propagation_id
    event_date
    event_type
    measurement (JSON)
    notes
    photo_url
    
    @property days_since_start() → int
```

---

## ⚙️ SERVICES: 3 VALIDATIONS CLÉS

### **1. Anti-Cycle (CRITIQUE)**
```
Avant de créer propagation:
  ✅ Vérifier que parent_id n'a pas child_id en ancêtres
  ✅ Empêcher: Plant #1 → #2 → #3 → #1 (CYCLE!)
```

### **2. States Valides**
```
pending → rooting → rooted → growing → ready-to-pot → potted → established
❌ Pas de saut (pending → potted interdit)
❌ Pas de retour en arrière
```

### **3. Source × Méthode Valides**
```
✅ Cutting: water, soil, air-layer, substrate
✅ Seeds: soil, substrate
✅ Division: soil (uniquement)
✅ Offset: soil, water
```

---

## 💡 ESTIMATEURS (Auto-Calculés)

### **Durée Avant "Ready-to-Pot"**
```
Cutting water    → 14 jours
Cutting soil     → 21 jours
Cutting air-layer → 35 jours
Seeds soil       → 30 jours
Division soil    → 0 jours (immédiat)
Offset soil      → 7 jours
```

### **Taux Succès Estimé**
```
Division soil    → 95% (quasi garanti)
Cutting air-layer → 90%
Cutting water    → 85%
Offset soil      → 80%
Cutting soil     → 70%
Seeds soil       → 60%
```

---

## 🖥️ FRONTEND: 5 PAGES PRINCIPALES

### **1. Dashboard**
```
- Résumé: N en rooting, N prêtes, N réussies
- Prochaines prêtes: "Monstera prête le 28 Nov"
- Alertes: "Pas de racines depuis 30j!"
- Boutons: Créer, Voir arbre, Voir calendrier
```

### **2. Détails Bouture**
```
- Metadata: parent, source, method, dates estimées
- Timeline: jour 0 → jour 21 (chaque étape)
- Photos intégrées à chaque étape
- Mesures: root_length, leaves, roots
- Bouton: Convertir en plante
```

### **3. Calendrier**
```
Vue mensuelle Gantt:
├─ Chaque bouture = une ligne
├─ Timeline: de jour 0 à established
└─ Coleurs par statut (bleu rooting, vert ready, etc)
```

### **4. Arbre Généalogique**
```
D3.js ou Cytoscape:
- Parent au centre
- Filles autour
- Petites-filles en dessous
- Clic = voir détails/photos
```

### **5. Statistiques**
```
- Taux succès par source (cutting/seeds/etc)
- Taux succès par méthode (water/soil/etc)
- Durée moyenne avant "ready-to-pot"
- Graphiques temporels
```

---

## 🧪 TESTS: CAS CLÉS À COUVRIR

```
✅ Créer bouture
✅ Logger progression (5+ événements)
✅ Convertir en plante
✅ Voir arbre généalogique
✅ Détecter cycle (empêcher Plant #1 → #2 → #1)
✅ Transitions d'état valides
✅ Estimateurs corrects
✅ Alertes correctes (overdue, ready-to-pot)
✅ Export CSV
✅ Timeline photos
```

---

## 📊 3 CONCEPTS CLÉS À RETENIR

### **1. Boutures EN COURS vs CONVERTIES**
```
EN COURS (child_plant_id = NULL):
├─ Bouture en eau depuis 10 jours
├─ Pas encore une plante indépendante
├─ Status: rooting

CONVERTIE (child_plant_id = 5):
├─ Bouture devenue plant #5
├─ Status: potted → established
```

### **2. Machine à États Stricte**
```
pending ↓ (pré-prélèvement)
rooting ↓ (enracinement en cours)
rooted ↓ (racines visibles)
growing ↓ (nouvelle croissance)
ready-to-pot ↓ (prête à rempoter)
potted ↓ (rempoté)
established ✅ (succès final)
```

### **3. 3 Types de Relations**
```
MÈRE: parent_plant_id = NULL
FILLE: parent_plant_id = 1 (la mère)
SOEUR: même parent_plant_id
```

---

## ⏱️ EFFORT & TIMELINE

```
Phase 1: Database (45 min)
  └─ Alembic migration + 2 tables + indices

Phase 2: Models (45 min)
  └─ PlantPropagation + PropagationEvent

Phase 3: Services (1h)
  └─ Validations (anti-cycle, states)
  └─ Estimateurs (durée, taux)

Phase 4: API (1.5h)
  └─ 19 endpoints

Phase 5: Tests (1.5h)
  └─ Backend tests 100%

Phase 6: Frontend (5h)
  └─ Dashboard (1h)
  └─ Détails + Timeline (1h)
  └─ Calendrier (1.5h)
  └─ Arbre généalogique (1.5h)

Total: 14-15 heures

MVP (backend seul): 4-5 heures
```

---

## ✅ CHECKLIST AVANT DE CODER

- [ ] Lire `FEATURE_PROPAGATION_FINAL.md` (30 min)
- [ ] Comprendre anti-cycle validation
- [ ] Comprendre 9 états
- [ ] Backup DB (TRÈS IMPORTANT!)
- [ ] Prêt à commencer

---

## 🚀 POUR LANCER

**1. Créer migration Alembic**
```bash
cd backend
alembic revision --autogenerate -m "Add propagation tracking"
```

**2. Éditer le fichier (copier SQL depuis FEATURE_PROPAGATION_FINAL.md)**

**3. Appliquer**
```bash
alembic upgrade head
```

**4. Créer modèles (copier depuis FEATURE_PROPAGATION_FINAL.md)**

**5. Créer services (copier validations depuis FEATURE_PROPAGATION_FINAL.md)**

**6. Créer endpoints (copier spécifications depuis FEATURE_PROPAGATION_FINAL.md)**

**7. Tester**

**8. Frontend**

---

## 📚 DOCUMENTS DE RÉFÉRENCE

| Doc | Usage |
|-----|-------|
| `FEATURE_PROPAGATION_FINAL.md` | ⭐ Source de vérité technique |
| `QUICKSTART_PROPAGATION.md` | Guide étape-par-étape |
| `SYNTHESE_AMELIORATIONS_PROPAGATION.md` | Comprendre pourquoi ce design |

---

## 🎯 EN RÉSUMÉ

**À Implémenter:**
- ✅ 2 tables (plant_propagations + propagation_events)
- ✅ 2 modèles SQLAlchemy
- ✅ 3 services (validations, estimateurs, analytics)
- ✅ 19 endpoints API
- ✅ 5 pages frontend
- ✅ Tests complets

**Effort:** 14-15 heures (2-3 semaines part-time)

**État:** 100% planifiée, 0% code

**Prêt à démarrer:** OUI ✅

---

**Créé:** 11 Novembre 2025  
**Lecture:** 2 minutes  
**Lien vers détails:** `FEATURE_PROPAGATION_FINAL.md`

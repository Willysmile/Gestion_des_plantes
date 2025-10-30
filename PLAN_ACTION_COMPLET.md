# 📋 PLAN D'ACTION - Prochaines Semaines

**Date:** 30 Octobre 2025  
**Branche actuelle:** v2.10  
**État projet:** 81% couverture, 179/186 tests passants

---

## 🎯 OBJECTIFS FINAUX

| Objectif | Cible | Effort |
|----------|-------|--------|
| **Couverture tests** | 90%+ | 15-20h |
| **Tests passants** | 100% (186/186) | 2-3h |
| **Frontend features** | 100% (validation + timeline) | 8-10h |
| **Bugs fixés** | 0 critiques | Var. |
| **Documentation** | À jour | 5h |
| **Performance** | <2s avg response | 3-5h |

**Total estimé:** 30-40 heures

---

## 🔴 PRIORITÉ 1 - URGENT (Cette semaine)

### 1.1 Fixer 7 tests échoués (2-3h)
**Fichier:** `backend/tests/test_settings_routes_integration.py`  
**Détail:** Voir `ANALYSE_7_TESTS_ECHOUES.md`

**À faire:**
- [ ] Ajouter endpoints GET /api/settings/{type}/{id} (locations, purchase-places)
- [ ] Vérifier format réponses POST (tags, diseases)
- [ ] Vérifier seed données (diseases, treatments)
- [ ] Rerun tests → 186/186 passants ✅

**Commandes:**
```bash
cd backend
venv/bin/pytest tests/test_settings_routes_integration.py -v
```

**Impact:** Tests 179→186, Couverture 81%→82%+

---

### 1.2 Intégrer lookup_routes.py (1-2h)
**Fichier:** `backend/app/routes/lookup_routes.py` (0% couverture, 126 lignes)  
**Problème:** Route file non enregistré dans main.py

**À faire:**
- [ ] Vérifier que lookup_routes doit être utilisé (ou le supprimer?)
- [ ] Si oui: l'importer et l'enregistrer dans main.py
- [ ] Créer tests d'intégration pour tous les endpoints
- [ ] Atteindre 90%+ couverture

**Commandes:**
```bash
# Vérifier que le route est importé
grep -n "lookup_routes" backend/app/main.py

# Ajouter si nécessaire:
# from app.routes import lookup_routes
# app.include_router(lookup_routes.router)
```

**Impact:** Couverture 82%→85%+

---

### 1.3 Compléter histories.py (2-3h)
**Fichier:** `backend/app/routes/histories.py` (55% couverture, 75 lignes)  
**Problème:** Beaucoup de branches non testées (creates, updates, deletes, erreurs)

**À faire:**
- [ ] Analyser lignes manquantes (voir BILAN_COMPLET.md)
- [ ] Créer tests pour chaque type historique (watering, fertilizing, repotting, disease, notes)
- [ ] Tester cas d'erreur (plant not found, invalid data, validation errors)
- [ ] Atteindre 90%+ couverture

**Commandes:**
```bash
cd backend
venv/bin/pytest --cov=app.routes.histories --cov-report=term-missing -v
```

**Impact:** Couverture 85%→88%+

---

## 🟠 PRIORITÉ 2 - IMPORTANT (La semaine suivante)

### 2.1 Augmenter couverture routes (1-2h)
- [ ] settings.py: 79% → 90% (30 lignes)
- [ ] plants.py: 79% → 90% (21 lignes)
- [ ] photos.py: 86% → 95% (9 lignes)

**Chacun:** Ajouter 3-5 tests pour branches manquantes

**Impact:** Couverture 88%→90%+

---

### 2.2 Compléter services tests (1h)
- [ ] plant_service.py: 85% → 95% (20 lignes)
- [ ] stats_service.py: 84% → 95% (9 lignes)

**Chacun:** Ajouter 2-3 tests pour branches manquantes

**Impact:** Couverture 90%→92%+

---

### 2.3 image_processor.py tests (1-2h)
**Fichier:** `backend/app/utils/image_processor.py` (71% couverture)  
**À faire:**
- [ ] Tester compression d'images
- [ ] Tester resize / thumbnail generation
- [ ] Tester erreurs (invalid image, size limits, etc.)

**Impact:** Couverture 92%→94%+

---

## 🟡 PRIORITÉ 3 - Frontend Features (Semaine 2-3)

### 3.1 Validation Zod (2h)
**Phase:** Phase 3.1 (voir docs/PHASE_3_PLAN.md)  
**À faire:**
- [ ] `npm install zod`
- [ ] Créer `src/lib/schemas.js` avec validation plante
- [ ] Modifier `PlantForm.jsx` pour valider avant submit
- [ ] Afficher messages d'erreur en français
- [ ] Tester: required fields, email format, etc.

**Fichiers à créer/modifier:**
- Créer: `frontend/src/lib/schemas.js`
- Modifier: `frontend/src/components/PlantForm.jsx`
- Modifier: `frontend/src/lib/api.js`

---

### 3.2 HistoryTimeline Component (3h)
**Phase:** Phase 3.3 (voir docs/PHASE_3_PLAN.md)  
**À faire:**
- [ ] Créer `src/components/HistoryTimeline.jsx`
  - Timeline visuelle (vertical line + events)
  - Event cards par type (couleurs)
  - Date/time, description, icons
- [ ] Modifier `PlantDetailPage.jsx` pour intégrer
- [ ] Ajouter filtres par type d'événement
- [ ] Tester: chronologie, filtrage

**Fichiers à créer/modifier:**
- Créer: `frontend/src/components/HistoryTimeline.jsx`
- Créer: `frontend/src/hooks/useHistory.js`
- Modifier: `frontend/src/pages/PlantDetailPage.jsx`

---

### 3.3 Améliorer PhotoGallery (1-2h)
**À faire:**
- [ ] Vérifier upload/delete/list fonctionnent
- [ ] Ajouter tests E2E pour galerie
- [ ] Améliorer UX (drag-drop, lazy loading, lightbox)

**Fichiers à vérifier/modifier:**
- `frontend/src/components/PhotoGallery.jsx`
- `frontend/src/hooks/usePhotos.js`

---

## 🟣 PRIORITÉ 4 - Tests E2E & Polish (Semaine 3-4)

### 4.1 Tests E2E (2-3h)
**À faire:**
- [ ] Setup Cypress ou Playwright
- [ ] Tests CRUD plantes complets
- [ ] Tests upload photo
- [ ] Tests historique
- [ ] Tests validation formulaire

---

### 4.2 Performance & Optimisation (2h)
- [ ] Vérifier lazy loading images
- [ ] Optimiser requêtes API (caching)
- [ ] Bundle size avec Vite
- [ ] Mesurer response times

---

### 4.3 Documentation & Polish (2h)
- [ ] Mettre à jour README
- [ ] Documenter endpoints API
- [ ] Guide utilisateur final
- [ ] Optimiser UI/UX Tauri

---

## 📊 ROADMAP TEMPORELLE

```
Semaine 1 (30 Oct - 3 Nov):
├─ Fixer 7 tests échoués (Lun-Mar) ← URGENT
├─ Intégrer lookup_routes (Mar) ← URGENT
├─ Compléter histories.py (Mar-Mer) ← URGENT
├─ Remonter couverture 81% → 90% (Jeu-Ven)
└─ OBJECTIF: Tests 186/186 ✅, Couverture 90%+ ✅

Semaine 2 (6 Nov - 10 Nov):
├─ Validation Zod frontend (Lun-Mar)
├─ HistoryTimeline component (Mar-Jeu)
├─ PhotoGallery improvements (Ven)
└─ OBJECTIF: Frontend features 80% ✅

Semaine 3 (13 Nov - 17 Nov):
├─ Tests E2E setup & écriture (Lun-Mer)
├─ Performance optimisation (Jeu)
├─ Documentation (Ven)
└─ OBJECTIF: E2E 90%+, Docs à jour ✅

Semaine 4 (20 Nov - 24 Nov):
├─ Bugfixes et refinements
├─ User testing & feedback
├─ Final polish & release prep
└─ OBJECTIF: Ready for production ✅
```

---

## 🛠️ COMMANDES RAPIDES

### Backend
```bash
cd backend
source venv/bin/activate

# Voir tous les tests
pytest -v

# Voir couverture
pytest --cov=app --cov-report=term-missing

# Un test spécifique
pytest tests/test_settings_routes_integration.py::test_create_tag -v

# Avec log
pytest -v -s
```

### Frontend
```bash
cd frontend
npm install       # Si new dependencies
npm run dev       # Development
npm run build     # Production
npm run tauri dev # Desktop Tauri
```

### Git
```bash
# Sur v2.10 branch
git status
git add .
git commit -m "fix: Description"
git push origin v2.10

# Créer feature branch
git checkout -b feature/nom-du-feature
# ... faire du code ...
git add .
git commit -m "feat: Description"
git push origin feature/nom-du-feature

# Merger back to v2.10
git checkout v2.10
git pull origin v2.10
git merge feature/nom-du-feature
git push origin v2.10
```

---

## 📋 CHECKLIST COMPLÈTE

### Backend Tests (Cette semaine)
- [ ] 7 tests échoués fixés → 186/186 ✅
- [ ] lookup_routes.py intégré → 0% → 90%+ ✅
- [ ] histories.py complété → 55% → 90%+ ✅
- [ ] Couverture globale: 81% → 90%+ ✅
- [ ] Tous warnings supprimés ✅
- [ ] Code committé & pushé ✅

### Frontend Features (Semaines 2-3)
- [ ] Zod validation créée
- [ ] HistoryTimeline créée
- [ ] PhotoGallery améliorée
- [ ] Tests E2E crées
- [ ] Documentation à jour

### Quality Assurance (Semaines 3-4)
- [ ] Performance testée
- [ ] UI/UX polished
- [ ] Tous bugs corrigés
- [ ] Ready for production

---

## 📞 Questions Clés à Répondre

1. **lookup_routes.py est-il utilisé?** Vérifier si endpoint déjà utilisé par frontend avant de l'ajouter
2. **Format des réponses POST correct?** Vérifier si response a "name" field pour tests
3. **Seed données complètes?** Vérifier que diseases et treatments sont seedés
4. **Photo upload fonctionne?** Tester manuellement avant de polir UX
5. **Performance acceptée?** Mesurer temps réponse API sous charge

---

## ✅ DÉFINITION "DONE"

Le projet est considéré "DONE" quand:
- ✅ 90%+ test coverage
- ✅ 186/186 tests passing
- ✅ 0 warnings in test output
- ✅ All 5 frontend features implemented
- ✅ Performance: <2s avg response
- ✅ Documentation: 100% up-to-date
- ✅ Code: Clean, well-structured
- ✅ Tauri app: Runs smoothly, no crashes
- ✅ UX: Polished, user-friendly
- ✅ Security: No vulnerabilities

---

**Prêt à commencer? Commencez par la Priorité 1.1 (7 tests échoués).**  
**Branche:** v2.10  
**Dernier commit:** 85e6bac

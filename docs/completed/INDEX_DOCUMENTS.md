# 📑 INDEX DES DOCUMENTS - Gestion des Plantes v2

**Date:** 30 Octobre 2025  
**Branche:** v2.10  
**Version:** 2.0 (Tauri + React + FastAPI)

---

## 🚀 COMMENCER ICI

**Nouveau dans le projet?** Lire dans cet ordre:

1. **[README.md](./README.md)** — Vue d'ensemble du projet (5 min)
2. **[BILAN_COMPLET.md](./BILAN_COMPLET.md)** — État actuel détaillé (10 min)
3. **[PLAN_ACTION_COMPLET.md](./PLAN_ACTION_COMPLET.md)** — Ce qu'il faut faire (15 min)
4. **[ANALYSE_7_TESTS_ECHOUES.md](./ANALYSE_7_TESTS_ECHOUES.md)** — Premiers bugs à fixer (5 min)

**Total:** 35 minutes pour avoir une vue complète ✅

---

## 📋 DOCUMENTS PAR CATÉGORIE

### 🔴 URGENT (Lire immédiatement)

| Document | Sujet | Urgence | Durée |
|----------|-------|---------|-------|
| **[BILAN_COMPLET.md](./BILAN_COMPLET.md)** | État projet 81% couverture | 🔴 URGENT | 10 min |
| **[PLAN_ACTION_COMPLET.md](./PLAN_ACTION_COMPLET.md)** | Roadmap 4 semaines | 🔴 URGENT | 15 min |
| **[ANALYSE_7_TESTS_ECHOUES.md](./ANALYSE_7_TESTS_ECHOUES.md)** | 7 tests échoués + solutions | 🔴 URGENT | 5 min |

### 📖 ARCHITECTURE & DESIGN

| Document | Sujet | Détail |
|----------|-------|--------|
| **docs/INDEX.md** | Hub principal docs v2 | Navigation, phases |
| **docs/DECISION_LOG_V2.md** | Décisions architecturales | Pourquoi FastAPI? Pourquoi Tauri? |
| **docs/PHASE_1_V2_PLAN.md** | Détails backend (1h40) | Architecture, endpoints, models |
| **docs/PHASE_2_V2_PLAN.md** | Détails frontend (1h20) | React structure, components |
| **docs/PHASE_3_PLAN.md** | Features finales | Validation, photos, timeline |

### ✅ STATUS PHASES

| Document | Phase | Status | Complétude |
|----------|-------|--------|-----------|
| **docs/PHASE_3_1_COMPLETE.md** | 3.1 Validation | ✅ DONE | 100% |
| **PHASE_3_2_COMPLETE.md** | 3.2 Photos | ✅ DONE | 95% |
| **[BILAN_COMPLET.md](./BILAN_COMPLET.md)** | 3.3-3.4 Pending | 🟡 In Progress | 0% |

### 🧪 TESTS & COUVERTURE

| Document | Sujet | État |
|----------|-------|------|
| **[ANALYSE_7_TESTS_ECHOUES.md](./ANALYSE_7_TESTS_ECHOUES.md)** | 7 tests échoués + fixes | 🔴 À fixer |
| **COVERAGE_REPORT_30OCT.md** | Rapport couverture détaillé | 81% couverture |
| **TEST_README.md** | Guide tests | Comment run pytest |
| **TEST_RESULTS_EXECUTED.md** | Résultats tests exécutés | 179/186 passants |

### 🐛 BUGS & FIXES

| Document | Sujet | Priorité |
|----------|-------|----------|
| **WATERING_DEBUG_FIXES.md** | Fixes arrosage historique | ✅ DONE |
| **[ANALYSE_7_TESTS_ECHOUES.md](./ANALYSE_7_TESTS_ECHOUES.md)** | 7 bugs tests | 🔴 P1 |

### 📚 SESSIONS PRÉCÉDENTES

| Document | Date | Sujet |
|----------|------|-------|
| **SESSION_26_OCT_SUMMARY.md** | 26 Oct | Résumé dernière session |
| **LIVE_TEST_SESSION.md** | ?? | Test en direct |
| **LIVE_TEST_GUIDE.md** | ?? | Guide pour tester live |
| **TEST_PLAN_PHASE_3_1.md** | ?? | Plan tests phase 3.1 |

### 🔧 OUTILS & SCRIPTS

| Fichier | Sujet | Usage |
|---------|-------|-------|
| **test_watering_api.mjs** | Test API arrosage (Node.js) | `node test_watering_api.mjs` |
| **test-live.sh** | Script test live | `bash test-live.sh` |
| **test_live.sh** | Variante shell | `bash test_live.sh` |
| **test-photos.sh** | Tests photos | `bash test-photos.sh` |
| **test-api.sh** | Tests API généraux | `bash test-api.sh` |
| **test_delete_photo.sh** | Test suppression photo | `bash test_delete_photo.sh` |

---

## 🏗️ STRUCTURE PROJET

```
Gestion_des_plantes/
├── README.md                           ← Main overview
├── BILAN_COMPLET.md                   ← État détaillé + problèmes
├── PLAN_ACTION_COMPLET.md             ← Roadmap 4 semaines
├── ANALYSE_7_TESTS_ECHOUES.md         ← Solutions bugs tests
├── INDEX_DOCUMENTS.md                 ← Ce fichier
│
├── docs/                              ← Documentation v2
│   ├── INDEX.md                       ← Nav hub docs
│   ├── PHASE_1_READY.md               ← Checklist green light
│   ├── PHASE_1_V2_PLAN.md             ← Backend design
│   ├── PHASE_2_V2_PLAN.md             ← Frontend design
│   ├── PHASE_3_PLAN.md                ← Validation + Photos + Timeline
│   ├── PHASE_3_1_COMPLETE.md          ← Validation ✅
│   ├── DECISION_LOG_V2.md             ← Décisions arch
│   └── RECAP_PHASE_1_V2.md            ← Résumé phase 1
│
├── old-docs/                          ← Archive docs v1 (legacy)
│   ├── README-v1.md
│   ├── PHASE_1_COMPLETE.md
│   ├── PHASE_2_COMPLETE.md
│   └── ... (autres phases v1)
│
├── backend/                           ← FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── main.py                    # 86% - FastAPI app
│   │   ├── models/                    # 95-100% - SQLAlchemy
│   │   ├── routes/                    # 55-86% ← À compléter
│   │   ├── services/                  # 85-96% - Business logic
│   │   └── utils/                     # 71-100% - Helpers
│   ├── tests/                         # 179/186 passing ← À fixer
│   ├── migrations/                    # Alembic
│   ├── pytest.ini                     # Config tests
│   ├── requirements.txt               # Dependencies
│   └── venv/                          # Python 3.11 venv
│
├── frontend/                          ← React + Vite + Tauri
│   ├── src/
│   │   ├── components/                # React components
│   │   ├── pages/                     # Pages principales
│   │   ├── hooks/                     # Custom React hooks
│   │   ├── contexts/                  # React contexts
│   │   ├── lib/                       # API client, schemas
│   │   └── utils/                     # Formatters, helpers
│   ├── package.json                   # npm dependencies
│   ├── vite.config.js                 # Vite config
│   └── tailwind.config.js             # Tailwind CSS
│
├── data/                              ← Database & exports
│   ├── plants.db                      # SQLite database
│   ├── exports/                       # CSV/JSON exports
│   └── photos/                        # Plant images
│
└── tools/                             ← Utilitaires externes
```

---

## 🎯 OBJECTIFS RÉSUMÉS

### Court Terme (Cette semaine)
- ✅ Fixer 7 tests échoués
- ✅ Atteindre 90%+ couverture tests
- ✅ Tous 186 tests passants
- **Durée:** 3-4 jours

### Moyen Terme (Semaines 2-3)
- ✅ Validation Zod frontend
- ✅ HistoryTimeline component
- ✅ Galerie photos améliorée
- **Durée:** 5-8 jours

### Long Terme (Semaine 4+)
- ✅ Tests E2E complets
- ✅ Performance optimisée
- ✅ Documentation à jour
- ✅ Tauri app polished
- **Durée:** 5+ jours

---

## 🔍 TROUVER RAPIDEMENT

### Je veux...
| Besoin | Aller à |
|--------|---------|
| Voir l'état du projet | [BILAN_COMPLET.md](./BILAN_COMPLET.md) |
| Savoir ce faire | [PLAN_ACTION_COMPLET.md](./PLAN_ACTION_COMPLET.md) |
| Fixer les bugs | [ANALYSE_7_TESTS_ECHOUES.md](./ANALYSE_7_TESTS_ECHOUES.md) |
| Architecture backend | docs/PHASE_1_V2_PLAN.md |
| Architecture frontend | docs/PHASE_2_V2_PLAN.md |
| Features manquantes | docs/PHASE_3_PLAN.md |
| Décisions design | docs/DECISION_LOG_V2.md |
| Comment lancer tests | TEST_README.md |
| Rapport couverture | COVERAGE_REPORT_30OCT.md |
| Lancer le serveur | backend/README.md ou `uvicorn app.main:app --reload` |
| Lancer le frontend | frontend/README.md ou `npm run dev` |

---

## 📊 STATISTIQUES

| Métrique | Valeur |
|----------|--------|
| **Lignes code** | ~5000 |
| **Tests** | 186 (179 ✅, 7 ❌) |
| **Couverture** | 81% |
| **Endpoints API** | 40+ |
| **Models** | 7 |
| **Frontend components** | 15+ |
| **Git branches** | 9 |
| **Commits** | 50+ |

---

## 🔗 LIENS RAPIDES

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload     # http://localhost:8000/docs
pytest -v                         # Run all tests
pytest --cov=app                  # Coverage report
```

### Frontend
```bash
cd frontend
npm install                       # Install deps
npm run dev                       # Development
npm run tauri dev                 # Tauri desktop app
```

### Git
```bash
git branch                        # Current branch: v2.10
git log --oneline -10             # Last 10 commits
git status                        # Changes
git diff                          # What changed
```

---

## 📞 SUPPORT

### Questions Fréquentes

**Q: Comment run les tests?**  
A: `cd backend && venv/bin/pytest -v`

**Q: Comment voir la couverture?**  
A: `venv/bin/pytest --cov=app --cov-report=term-missing`

**Q: Comment ajouter une dépendance?**  
A: Backend: `pip install <pkg> && pip freeze > requirements.txt`  
Frontend: `npm install <pkg>`

**Q: Comment merger une feature branch?**  
A: 
```bash
git checkout feature-branch
git push origin feature-branch
# Create PR on GitHub (or merge locally)
git checkout v2.10
git merge feature-branch
git push origin v2.10
```

**Q: Quel est l'état de la DB?**  
A: SQLite at `data/plants.db`. Migrations: `backend/migrations/`

---

## 📝 CONVENTIONS

### Git Commits
```
fix: Description courte du bug fixé
feat: Description de la nouvelle feature
test: Amélioration des tests
docs: Mise à jour documentation
refactor: Refactoring sans nouvelle feature
```

### Branches
- `v2.10` — Main branche de développement (ACTUELLE)
- `v2-tauri-react` — Source branche (stable)
- `master` — Production (à définir)
- `feature/*` — Feature branches (temporaires)

### Code Style
- Python: PEP 8 (black formatted)
- JavaScript: ESLint standard
- Comments: English or French OK
- Docstrings: Obligatoires pour functions

---

## ✅ PRÊT À DÉMARRER?

**Suivez ce plan:**

1. Lire [BILAN_COMPLET.md](./BILAN_COMPLET.md) (10 min)
2. Lire [PLAN_ACTION_COMPLET.md](./PLAN_ACTION_COMPLET.md) (15 min)
3. Lire [ANALYSE_7_TESTS_ECHOUES.md](./ANALYSE_7_TESTS_ECHOUES.md) (5 min)
4. Commencer par Priorité 1.1 (Fixer 7 tests)
5. Commit & push quand terminé
6. Créer PR pour review

**Branche active:** `v2.10`  
**Derniers commits:** 85e6bac  
**État:** Prêt pour développement ✅

---

**Dernier mis à jour:** 30 Octobre 2025  
**Prochain bilan:** Après P1 (7 tests fixés)

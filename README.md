# 🌱 Gestion des Plantes - Plant Manager v2 (Python)

**Application desktop de gestion de collection de plantes.**

**Status:** 📝 Préparation en cours (Phase 0 - Documentation complète)

---

## 📚 Documentation

**Commencez par lire ces fichiers (dans `docs/preparation_projet/`):**

### 🔴 Essentiels (15 min)
1. **`docs/preparation_projet/QUICK_REFERENCE.md`** - Vue d'ensemble en 1 page (5 min)
2. **`docs/preparation_projet/CAHIER_DES_CHARGES_PYTHON.md`** - Specifications complètes (10 min)

### 🟡 Importantes (30 min)
3. **`docs/preparation_projet/PLAN_ACTION_PHASES.md`** - Roadmap 6 phases de développement (30 min)
4. **`docs/preparation_projet/DECISIONS_LOG.md`** - Choix architecturaux & justifications (20 min)

### 🟢 Référence
- `docs/preparation_projet/RESUME_TECHNIQUE_MIGRATION.md` - Comment on passe de Laravel à Python
- `docs/preparation_projet/INDEX_DOCUMENTATION.md` - Index complet des docs
- `docs/preparation_projet/CONFIRMATION_FINALE.md` - Validations finales

---

## 🛠️ Tech Stack

```
Backend:   FastAPI (Python 3.10+) + SQLAlchemy ORM + Pydantic
Frontend:  PySimpleGUI (Python desktop UI)
Database:  SQLite local (zero configuration, ~10k plants max)
Storage:   Local filesystem (photos/webp + exports/zip)
Deploy:    PyInstaller → Single .exe file (Windows/Mac/Linux)
ORM:       SQLAlchemy + Alembic (migrations)
Validation: Pydantic schemas (45+ REST endpoints)
```

---

## 🎯 Fonctionnalités Clés

✅ **CRUD plantes** - Création/édition/suppression/archivage  
✅ **Gestion photos** - Upload, WebP conversion (quality=85), main photo  
✅ **5 historiques** - Arrosage, fertilisation, rempotage, maladies, notes générales  
✅ **Tags & catégories** - Organisation flexible  
✅ **Recherche & filtres** - Par localisation, status, difficultés, etc.  
✅ **Export/Import** - ZIP avec JSON + photos + metadata + checksum SHA256  
✅ **Statistiques** - Plantes par localisation, arrosages prévus, KPIs  
✅ **Audit logging** - Traçabilité CREATE/UPDATE/DELETE  
✅ **Soft delete** - Suppression logique avec recovery possible  
✅ **Offline-first** - Zéro connexion internet requise  

---

## 📅 Phases de développement (6 semaines)

| Phase | Durée | Focus | Status |
|-------|-------|-------|--------|
| 0 | Done | Documentation complète + decisions | ✅ DONE |
| 1 | Week 1 | Infrastructure (FastAPI + SQLite + 15 models) | 🚀 NEXT |
| 2 | Week 2-3 | CRUD Plantes + Pydantic schemas |  |
| 3 | Week 4 | Photos + 5 historiques |  |
| 4 | Week 5 | Settings + Statistiques |  |
| 5 | Week 6 | Export/Import + Polish |  |
| 6 | Week 7 | Déploiement (PyInstaller) |  |
| **TOTAL** | **~6-7 semaines** | **5000+ LOC** |  |

---

## 🚀 Installation (Phase 1 en cours)

### Development Setup

```bash
# Backend (Terminal 1)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# → http://localhost:8000/docs (Swagger API)

# Frontend (Terminal 2)
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

### Production Deployment (Phase 6)

```bash
# PyInstaller packaging
pyinstaller --onefile --windowed app/main.py
# → dist/plant_manager.exe (Windows)
# → dist/plant_manager (Linux/Mac)
```

---

## 📂 Structure du Projet

```
Gestion_des_plantes/
├── docs/
│   └── preparation_projet/          ← Phase 0: Documentation
│       ├── QUICK_REFERENCE.md       (Vue 1-page)
│       ├── CAHIER_DES_CHARGES_PYTHON.md
│       ├── PLAN_ACTION_PHASES.md
│       ├── DECISIONS_LOG.md
│       ├── RESUME_TECHNIQUE_MIGRATION.md
│       └── ...
│
├── backend/                         ← Phase 1+: FastAPI
│   ├── app/
│   │   ├── main.py                  (FastAPI app + routes)
│   │   ├── config.py                (settings, DB URL)
│   │   ├── models/
│   │   │   ├── plant.py             (Plant, Photo)
│   │   │   ├── histories.py         (5 history models)
│   │   │   ├── tags.py              (Tag, TagCategory)
│   │   │   └── lookup.py            (Location, PurchasePlace, etc)
│   │   ├── schemas/                 (Pydantic validation)
│   │   ├── routes/                  (45+ endpoints)
│   │   ├── services/                (Business logic)
│   │   └── utils/
│   ├── migrations/                  (Alembic)
│   ├── tests/
│   ├── requirements.txt
│   └── venv/
│
├── frontend/                        ← Phase 1+: PySimpleGUI
│   ├── app/
│   │   ├── main.py                  (Entry point)
│   │   ├── api_client.py            (HTTP wrapper)
│   │   ├── config.py                (API base URL, etc)
│   │   ├── windows/
│   │   │   ├── main_window.py       (Plant list)
│   │   │   ├── plant_form.py        (Create/edit)
│   │   │   ├── plant_detail.py      (View + histories)
│   │   │   ├── settings_window.py
│   │   │   └── ...
│   │   └── utils/
│   ├── requirements.txt
│   └── venv/
│
├── data/                            ← Created automatically
│   ├── plants.db                    (SQLite database)
│   ├── photos/                      (WebP images)
│   └── exports/                     (ZIP backups)
│
├── .gitignore
├── README.md
├── DEVELOPMENT.md                   (Setup guide for devs)
└── .github/workflows/               (CI/CD future)
│   │   ├── routes/
│   │   └── utils/
│   └── requirements.txt
├── frontend/                ← PySimpleGUI UI (Phase 1+)
│   ├── app/
│   │   ├── main.py
│   │   ├── windows/
│   │   ├── api_client.py
│   │   └── config.py
│   └── requirements.txt
└── data/                    ← Local storage (created at runtime)
    ├── plants.db
    ├── photos/
    └── exports/
```

---

## 📖 Prochaines étapes

1. ✅ Documentation complète (Phase 0) **← FAIT**
2. ⬜ Lire la documentation (`docs/preparation_projet/`)
3. ⬜ Phase 1: Setup infrastructure
4. ⬜ Phase 2-6: Développement itératif

**Voir `docs/preparation_projet/PLAN_ACTION_PHASES.md` pour les détails.**

---

## 📝 Cahier des charges

**Voir `docs/preparation_projet/CAHIER_DES_CHARGES_PYTHON.md` pour:**
- Modèles de données (15 models)
- API endpoints (45+)
- UI windows (10)
- Features détaillées

---

## 🤔 Questions?

**Comment j'utilise ça?**
→ Lire `docs/preparation_projet/INDEX_DOCUMENTATION.md`

**Pourquoi FastAPI et pas Django?**
→ Lire `docs/preparation_projet/DECISIONS_LOG.md`

**Combien de temps pour coder?**
→ Lire `docs/preparation_projet/PLAN_ACTION_PHASES.md` (5-8 semaines)

**Ça vient d'où?**
→ Lire `docs/preparation_projet/RESUME_TECHNIQUE_MIGRATION.md` (extraction du Laravel)

---

**Status:** Documentation complète ✅  
**Date:** 25 Octobre 2025  
**Prêt à coder:** OUI 🚀

---

*Application Python desktop de gestion de plantes.*  
*Basée sur les specs du projet Laravel Plant Manager original.*

---

**Créé par:** Willysmile  
**Codé avec et par:** GitHub Copilot et Claude Haiku 4.5 (et autres suivant disponibilité des serveurs)

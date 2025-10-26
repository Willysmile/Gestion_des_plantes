# 🌿 Gestion des Plantes - v2 (Tauri + React + FastAPI)# 🌱 Gestion des Plantes - Plant Manager v2 (Python)



Plant management application rebuilt from scratch with modern tech stack.**Application desktop de gestion de collection de plantes.**



## 📁 Project Structure**Status:** 📝 Préparation en cours (Phase 0 - Documentation complète)



```---

gestion-plantes/

├── backend/                  # FastAPI + SQLAlchemy## 📚 Documentation

│   ├── app/

│   │   ├── main.py          # FastAPI app**Commencez par lire ces fichiers (dans `docs/preparation_projet/`):**

│   │   ├── models/          # SQLAlchemy models

│   │   ├── schemas/         # Pydantic schemas### 🔴 Essentiels (15 min)

│   │   ├── routes/          # API endpoints1. **`docs/preparation_projet/QUICK_REFERENCE.md`** - Vue d'ensemble en 1 page (5 min)

│   │   └── services/        # Business logic2. **`docs/preparation_projet/CAHIER_DES_CHARGES_PYTHON.md`** - Specifications complètes (10 min)

│   ├── requirements.txt

│   └── alembic/             # Database migrations### 🟡 Importantes (30 min)

│3. **`docs/preparation_projet/PLAN_ACTION_PHASES.md`** - Roadmap 6 phases de développement (30 min)

├── frontend/                # Tauri + React + TypeScript4. **`docs/preparation_projet/DECISIONS_LOG.md`** - Choix architecturaux & justifications (20 min)

│   ├── src/

│   │   ├── components/      # React components### 🟢 Référence

│   │   ├── pages/           # Page components- `docs/preparation_projet/RESUME_TECHNIQUE_MIGRATION.md` - Comment on passe de Laravel à Python

│   │   ├── hooks/           # Custom hooks- `docs/preparation_projet/INDEX_DOCUMENTATION.md` - Index complet des docs

│   │   └── App.tsx- `docs/preparation_projet/CONFIRMATION_FINALE.md` - Validations finales

│   ├── src-tauri/           # Tauri config

│   └── package.json---

│

├── data/                    # SQLite database## 🛠️ Tech Stack

│   └── plants.db

│```

├── docs-v1/                 # Archived v1 documentationBackend:   FastAPI (Python 3.10+) + SQLAlchemy ORM + Pydantic

│   ├── README-v1.mdFrontend:  PySimpleGUI (Python desktop UI)

│   ├── tests-v1/            # Old test filesDatabase:  SQLite local (zero configuration, ~10k plants max)

│   ├── phases/              # Phase 1-6 reportsStorage:   Local filesystem (photos/webp + exports/zip)

│   └── docs-preparation/    # Project prep docsDev Mode:  python app/main.py (simple, with auto-reload)

│Phase 6:   PyInstaller → Single .exe file (Windows/Mac/Linux)

└── README.mdORM:       SQLAlchemy + Alembic (migrations)

```Validation: Pydantic schemas (45+ REST endpoints)

```

## 🚀 Quick Start

---

### Backend Setup

## 🎯 Fonctionnalités Clés

```bash

cd backend✅ **CRUD plantes** - Création/édition/suppression/archivage  

python -m venv venv✅ **Gestion photos** - Upload, WebP conversion (quality=85), main photo  

source venv/bin/activate  # or: venv\Scripts\activate on Windows✅ **5 historiques** - Arrosage, fertilisation, rempotage, maladies, notes générales  

pip install -r requirements.txt✅ **Tags & catégories** - Organisation flexible  

```✅ **Recherche & filtres** - Par localisation, status, difficultés, etc.  

✅ **Export/Import** - ZIP avec JSON + photos + metadata + checksum SHA256  

### Frontend Setup✅ **Statistiques** - Plantes par localisation, arrosages prévus, KPIs  

✅ **Audit logging** - Traçabilité CREATE/UPDATE/DELETE  

```bash✅ **Soft delete** - Suppression logique avec recovery possible  

cd frontend✅ **Offline-first** - Zéro connexion internet requise  

npm install

npm run tauri dev  # Development with hot reload---

npm run tauri build  # Build desktop app

```## 📅 Phases de développement (6 semaines)



## 📚 Previous Version (v1)| Phase | Durée | Focus | Status |

|-------|-------|-------|--------|

All Phase 1-6 documentation, tests, and PySimpleGUI implementation archived in `docs-v1/`:| 0 | Done | Documentation complète + decisions | ✅ DONE |

- See `docs-v1/README-v1.md` for v1 overview| 1 | Week 1 | Infrastructure (FastAPI + SQLite + 15 models) | 🚀 NEXT |

- See `docs-v1/phases/` for phase-by-phase reports| 2 | Week 2-3 | CRUD Plantes + Pydantic schemas |  |

- See `docs-v1/tests-v1/` for all test files| 3 | Week 4 | Photos + 5 historiques |  |

| 4 | Week 5 | Settings + Statistiques |  |

## 🔄 Git Branches| 5 | Week 6 | Export/Import + Polish |  |

| 6 | Week 7 | Déploiement (PyInstaller) |  |

- **master**: Stable production-ready code (squashed Phase 1-6)| **TOTAL** | **~6-7 semaines** | **5000+ LOC** |  |

- **v2-tauri-react**: Current development branch

---

## 📋 Tech Stack

## 🚀 Quick Start (Développement)

- **Backend**: FastAPI, SQLAlchemy, Pydantic, Alembic

- **Frontend**: Tauri, React, TypeScript, Tailwind CSS, shadcn/ui### Backend (Terminal 1)

- **Database**: SQLite```bash

- **API Client**: TanStack Query (React Query)cd backend

- **Validation**: Zod (client-side)python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

## ✨ Featurespip install -r requirements.txt

python -m uvicorn app.main:app --reload

- ✅ Plant CRUD operations# → http://localhost:8000/docs (Swagger API docs)

- ✅ Reference generation (auto-format: FAMILY-NNN)```

- ✅ Archive/restore workflow with timestamps

- ✅ Dashboard with statistics### Frontend (Terminal 2)

- ✅ Search and filtering```bash

- ✅ Theme systemcd frontend

- ✅ Responsive UIpython -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

## 📝 Licensepip install -r requirements.txt

python app/main.py

Private project - 2025```


**Note:** Pendant le développement (Phase 1-5), on utilise simplement `python app/main.py`. PyInstaller (exe packaging) est réservé à la Phase 6 (déploiement final).

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

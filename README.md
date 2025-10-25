# 🌱 Gestion des Plantes - Plant Manager v2 (Python)

**Application desktop de gestion de collection de plantes.**

**Status:** 📝 Préparation en cours (Phase 0 - Documentation complète)

---

## 📚 Documentation

**Commencez par lire ces fichiers (dans `docs/preparation_projet/`):**

### 🔴 Essentiels (15 min)
1. **`docs/preparation_projet/QUICK_REFERENCE.md`** - Vue d'ensemble en 1 page (5 min)
2. **`docs/preparation_projet/CAHIER_DES_CHARGES_PYTHON.md`** - Specifications complètes (10 min)

### 🟡 Importants (30 min)
3. **`docs/preparation_projet/PLAN_ACTION_PHASES.md`** - Roadmap 6 phases de développement (30 min)

### 🟢 Référence
- `docs/preparation_projet/RESUME_TECHNIQUE_MIGRATION.md` - Comment on passe de Laravel à Python
- `docs/preparation_projet/DECISIONS_LOG.md` - Pourquoi ces choix technologiques?
- `docs/preparation_projet/INDEX_DOCUMENTATION.md` - Index complet des docs

---

## 🛠️ Tech Stack

```
Backend:   FastAPI (Python) + SQLAlchemy ORM
Frontend:  PySimpleGUI (Python desktop UI)
Database:  SQLite local (zero configuration)
Storage:   Local filesystem (photos + exports)
Deploy:    PyInstaller → Single .exe file
```

---

## 🎯 Fonctionnalités

✅ CRUD complet pour plantes  
✅ Gestion des photos (WebP conversion)  
✅ 5 types d'historiques (arrosage, fertilisation, rempotage, maladies, notes)  
✅ Tags & catégories  
✅ Recherche & filtres avancés  
✅ Export/Import en ZIP  
✅ Statistiques & dashboard  
✅ Audit logging  

---

## 📅 Phases de développement

| Phase | Durée | Focus |
|-------|-------|-------|
| 1 | Week 1 | Infrastructure (FastAPI + SQLite) |
| 2 | Week 2-3 | CRUD Plantes |
| 3 | Week 4 | Photos + Historiques |
| 4 | Week 5 | Settings + Statistiques |
| 5 | Week 6-7 | Export/Import + Polish |
| 6 | Week 8 | Déploiement |
| **TOTAL** | **5-8 semaines** | |

---

## 🚀 Installation (à venir)

```bash
# Phase 1: Setup
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Terminal 2:
cd frontend
pip install -r requirements.txt
python app/main.py
```

---

## 📂 Structure (à venir)

```
Gestion_des_plantes/
├── docs/
│   └── preparation_projet/     ← Cahier des charges & planning (Phase 0)
│       ├── CAHIER_DES_CHARGES_PYTHON.md
│       ├── PLAN_ACTION_PHASES.md
│       ├── QUICK_REFERENCE.md
│       ├── DECISIONS_LOG.md
│       ├── RESUME_TECHNIQUE_MIGRATION.md
│       ├── INDEX_DOCUMENTATION.md
│       └── ...
├── backend/                 ← FastAPI backend (Phase 1+)
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
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

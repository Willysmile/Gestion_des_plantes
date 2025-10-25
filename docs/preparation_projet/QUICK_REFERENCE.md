# 🚀 QUICK REFERENCE - PLANT MANAGER v2 PYTHON

**Imprimable en 1 page** ✅

---

## 📱 TECH STACK

```
Backend:  FastAPI + SQLAlchemy + SQLite + Pydantic
Frontend: PySimpleGUI + Requests + Pillow
Storage:  /data/plants.db + /data/photos/ + /data/exports/
Deployment: PyInstaller → Single .exe
```

---

## 🗂️ STRUCTURE PROJECT

```
plant_manager_python/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/ (15 modèles)
│   │   ├── schemas/ (Pydantic)
│   │   ├── services/ (business logic)
│   │   ├── routes/ (12 groupes d'endpoints)
│   │   └── utils/
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── main.py
│   │   ├── windows/ (10 windows)
│   │   ├── api_client.py
│   │   └── config.py
│   └── requirements.txt
└── data/ (créé automatiquement)
    ├── plants.db
    ├── photos/
    └── exports/
```

---

## 🛢️ MODELS (15)

```
Core:        Plant, Photo
Histories:   WateringHistory, FertilizingHistory, RepottingHistory, 
             DiseaseHistory, PlantHistory
Tags:        Tag, TagCategory
Lookup:      Location, PurchasePlace, WateringFrequency, LightRequirement, 
             FertilizerType
Tracking:    AuditLog
```

---

## 🔌 API ENDPOINTS (45+)

```
PLANTS:        GET/POST /api/plants, PUT/DELETE /api/plants/{id}
               + archive, restore, archived, search, generate-reference
PHOTOS:        POST/GET/PATCH/DELETE /api/plants/{id}/photos
HISTORIES:     GET/POST/PUT/DELETE /api/plants/{id}/*-history (5 types)
SETTINGS:      CRUD for locations, purchase-places, frequencies, 
               light-requirements, fertilizer-types, tags
EXPORT/IMPORT: POST export, preview, import, GET exports, DELETE export/{file}
STATISTICS:    GET /api/statistics, /plants-by-location, /upcoming-waterings
AUDIT:         GET /api/audit-logs
```

---

## 🖥️ WINDOWS UI (10)

```
1. MainWindow          - Plant list + search + filters
2. PlantForm           - Create/edit (4 tabs)
3. PlantDetail         - View detail + histories (6 tabs)
4. SettingsWindow      - Manage lookups (6 tabs)
5. TagsWindow          - Manage tags + categories
6. StatisticsWindow    - Charts + KPIs + upcoming
7. ExportDialog        - Export ZIP + list existing
8. ImportDialog        - Import ZIP + preview + mode select
9. AuditWindow         - Audit logs viewer
10. RecoveryWindow     - Soft deleted items
```

---

## 📊 DATA MODEL (KEY FIELDS)

### Plant
```
name, scientific_name, family, subfamily, genus, species, subspecies, 
variety, cultivar, reference, description, health_status, difficulty_level,
location_id, purchase_date, watering_frequency_id, light_requirement_id,
temperature_min/max, humidity, soil_type, pot_size, is_indoor/outdoor,
is_favorite, is_toxic, is_archived, deleted_at (soft delete)
```

### Others
```
Photo:           filename (WebP), is_main, description
History:         *_date, amount/name/status, notes
Tag:             name, tag_category_id
Lookup:          name (simple)
```

---

## 🎯 FEATURES CHECKLIST

✅ CRUD plantes (create, read, update, delete, archive)
✅ Photos + WebP conversion
✅ 5 types historiques (arrosage, fertilisation, rempotage, maladie, notes)
✅ Tags & catégories
✅ Search & advanced filters
✅ Export/Import ZIP (checksum SHA256)
✅ Statistics & charts
✅ Audit logging
✅ Soft delete + recovery
✅ Settings management

---

## 🚀 QUICK START (DEV)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# → http://localhost:8000/docs (Swagger)
```

### Frontend
```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

---

## 📋 PHASE OVERVIEW

| Phase | Focus | Duration |
|-------|-------|----------|
| 1 | Setup + Backend infra + DB | 3-4j |
| 2 | CRUD plantes + basic UI | 4-5j |
| 3 | Photos + historiques | 5-6j |
| 4 | Settings + stats + search | 4-5j |
| 5 | Export/import + polish | 5-6j |
| 6 | Deploy + PyInstaller | 1-2j |
| **TOTAL** | | **5-8w** |

---

## 🔑 KEY DECISIONS

✅ Single user (no auth)
✅ SQLite local (no server)
✅ PySimpleGUI (easy packaging)
✅ Repartir from zero (not migrate Laravel data)
✅ Same features as Laravel v1.12
✅ Export/import for backup & sharing

---

## 🧪 TESTING STRATEGY

```
Unit:        Model + Service tests (70% coverage target)
Integration: Full CRUD roundtrip (create → update → export → delete)
E2E:         Manual UI testing
Edge cases:  Large exports, special chars, soft delete, recovery
```

---

## 📦 DEPENDENCIES

### Backend (minimal)
```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
pillow==10.1.0
python-multipart==0.0.6
```

### Frontend (minimal)
```
PySimpleGUI==4.60.5
requests==2.31.0
Pillow==10.1.0
matplotlib==3.8.2
```

---

## 🐛 DEBUGGING

```bash
# Backend logs
tail -f data/logs/app.log

# Database
sqlite3 data/plants.db ".schema"
sqlite3 data/plants.db "SELECT COUNT(*) FROM plants;"

# Frontend console
python app/main.py  # shows errors/exceptions
```

---

## 🔒 SECURITY

✅ No auth needed (single user)
✅ Soft delete for recovery
✅ SHA256 checksum on exports
✅ Audit logging all operations
✅ WebP conversion reduces file sizes

---

## 📝 NEXT STEPS

1. ✅ Read all 4 cahiers des charges files
2. ✅ Understand architecture
3. ⬜ Start Phase 1: Setup
4. ⬜ Build Phase 2: CRUD
5. ⬜ Continue phases 3-6
6. ⬜ Deploy & share

---

**Questions? Check:**
- `CAHIER_DES_CHARGES_PYTHON.md` - full specs
- `RESUME_TECHNIQUE_MIGRATION.md` - Laravel → Python mapping
- `PLAN_ACTION_PHASES.md` - detailed tasklist
- This file - quick reference

**Ready to code! 🚀**

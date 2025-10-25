# 🚀 PHASE 2 - CRUD PLANTES ✅

**Date:** 25 Octobre 2025  
**Status:** ✅ COMPLETE & TESTED  
**Branch:** 2.02 (local)  
**Tests:** 10/10 PASS ✅

---

## 📊 Résumé Phase 2

### ✅ Architecture créée

**Backend - Plant Service**
```
backend/app/
├── schemas/
│   └── plant_schema.py          ← Pydantic models (CRUD validation)
│       ├── PlantCreate          (obligation: name)
│       ├── PlantUpdate          (tous les champs optionnels)
│       ├── PlantResponse        (full plant details)
│       └── PlantListResponse    (lite version for lists)
├── services/
│   └── __init__.py              ← PlantService class
│       ├── get_all()            (list with pagination)
│       ├── get_by_id()          (get single plant)
│       ├── create()             (create with validation)
│       ├── update()             (update specific fields)
│       ├── delete()             (soft delete)
│       ├── archive()            (archive plant)
│       ├── restore()            (restore from archive)
│       ├── search()             (search by name/scientific)
│       ├── get_archived()       (list archived)
│       ├── get_favorites()      (list favorites)
│       ├── get_by_location()    (filter by location)
│       └── get_count()          (count total)
├── routes/
│   └── plants.py                ← FastAPI endpoints (10 routes)
└── scripts/
    └── seed_lookups.py          ← Pre-populate lookup tables
        ├── seed_locations()     (7 locations)
        ├── seed_purchase_places() (8 places)
        ├── seed_watering_frequencies() (7 frequencies)
        ├── seed_light_requirements() (6 requirements)
        └── seed_fertilizer_types() (8 types)
```

**Database Updates**
```
app/models/lookup.py
├── Location (added: description)
├── PurchasePlace (added: url)
├── WateringFrequency (added: days_interval)
├── LightRequirement (added: description)
└── FertilizerType (added: description)
```

---

## 🔌 Endpoints Implémentés (10 routes)

### Plant CRUD

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/plants` | List all plants (paginated) | ✅ 200 |
| POST | `/api/plants` | Create new plant | ✅ 201 |
| GET | `/api/plants/{id}` | Get plant details | ✅ 200 |
| PUT | `/api/plants/{id}` | Update plant | ✅ 200 |
| DELETE | `/api/plants/{id}` | Soft delete plant | ✅ 204 |

### Plant Actions

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/plants/{id}/archive` | Archive plant | ✅ 200 |
| POST | `/api/plants/{id}/restore` | Restore from archive | ✅ 200 |

### Plant Search & Filters

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/plants/archived` | List archived plants | ✅ 200 |
| GET | `/api/plants/search?q=...` | Search by name | ✅ 200 |
| GET | `/api/plants/favorites` | List favorites only | ✅ 200 |

---

## ✅ Validation Rules (Pydantic)

### Obligatoires
- `name` (1-100 chars, required)

### Optionnels (avec validation)
- `temperature_min`, `temperature_max` : -50 à 60°C
- `humidity_level` : 0 à 100%
- `purchase_price` : > 0
- `scientific_name`, `family`, `genus`, `species`, etc (max 150 chars)
- FK: `location_id`, `purchase_place_id`, `watering_frequency_id`, `light_requirement_id`
- Flags: `is_indoor`, `is_outdoor`, `is_favorite`, `is_toxic` (defaults False)
- Health: `health_status` (default: "healthy")

### Soft Delete Features
- `DELETE /api/plants/{id}` → sets `deleted_at = now()` (not removed from DB)
- `POST /api/plants/{id}/restore` → sets `deleted_at = NULL`
- `POST /api/plants/{id}/archive` → sets `is_archived = True`
- Archived/deleted plants excluded from normal queries

---

## 🌱 Seed Data

Pre-populated at startup (if missing):

**Locations** (7)
- Salon, Chambre, Cuisine, Bureau, Terrasse, Serre, Véranda

**Purchase Places** (8)
- Jardinerie locale, Pépinière, Marché, Amazon, Etsy, Truffaut, Botanic, Échange/Ami

**Watering Frequencies** (7)
- Très rare (30j), Rare (15j), Normal (7j), Régulier (3j), Fréquent (1j), Laisser sécher (14j), Garder humide (2j)

**Light Requirements** (6)
- Lumière directe, Mi-ombre, Ombre, Ombre profonde, Lumière indirecte, Variable

**Fertilizer Types** (8)
- NPK équilibré, NPK riche N, NPK riche K, Bio, Liquide, Bâtons, Compost, Foliaire

---

## 🧪 Tests Phase 2

### Test Suite (10/10 PASS ✅)

```
✅ Test 1: GET /api/plants (liste)
   Status: 200, Count: 1

✅ Test 2: POST /api/plants (create)
   Status: 201, ID: 2, Name: Pothos

✅ Test 3: GET /api/plants/2 (get one)
   Status: 200, Name: Pothos, Favorite: True

✅ Test 4: PUT /api/plants/2 (update)
   Status: 200, Health: sick, Desc: Un peu jaune

✅ Test 5: POST /api/plants/2/archive (archive)
   Status: 200, Archived: True

✅ Test 6: POST /api/plants/2/restore (restore)
   Status: 200, Archived: False

✅ Test 7: GET /api/plants?archived=true (list archived)
   Status: 200, Count: 2

✅ Test 8: GET /api/plants/favorites (favorites)
   Status: 200, Favorites: 1

✅ Test 9: DELETE /api/plants/2 (soft delete)
   Status: 204, Verify 404 after delete ✓

✅ Test 10: GET /api/plants/search?q=Monstera (search)
   Status: 200, Results: 1
```

### API Response Examples

**Create Plant (POST /api/plants)**
```json
{
  "id": 1,
  "name": "Monstera Deliciosa",
  "scientific_name": "Monstera deliciosa",
  "health_status": "healthy",
  "difficulty_level": "easy",
  "is_indoor": true,
  "is_favorite": false,
  "is_archived": false,
  "created_at": "2025-10-25T17:42:19.591207",
  "updated_at": "2025-10-25T17:42:19.591211"
}
```

**Update Plant (PUT /api/plants/{id})**
```json
{
  "id": 2,
  "health_status": "sick",
  "description": "Un peu jaune",
  ...
}
```

---

## 📁 Files Created/Modified

**Created:**
- ✅ `backend/app/schemas/plant_schema.py` (146 lines)
- ✅ `backend/app/services/__init__.py` (151 lines - PlantService)
- ✅ `backend/app/routes/plants.py` (161 lines - 10 endpoints)
- ✅ `backend/app/scripts/seed_lookups.py` (113 lines)
- ✅ `backend/app/scripts/__init__.py`

**Modified:**
- ✅ `backend/app/models/lookup.py` (added fields to 5 models)
- ✅ `backend/app/main.py` (added routes + seed at startup)

---

## 📈 Statistics Phase 2

| Metric | Count |
|--------|-------|
| Endpoints | 10 |
| Routes | 10 (all working ✅) |
| Pydantic schemas | 4 |
| Service methods | 11 |
| Seed functions | 5 |
| Pre-populated records | 36 (7+8+7+6+8) |
| Lines of code (new) | 571 |
| Test cases | 10 |
| Test pass rate | 100% ✅ |

---

## 🔄 Flow

### Create Plant Flow
```
POST /api/plants
  ↓ PlantCreate (validation)
  ↓ PlantService.create()
  ↓ SQLAlchemy INSERT
  ↓ DB commit
  ↓ PlantResponse (full details)
  ↓ 201 Created
```

### Update Plant Flow
```
PUT /api/plants/{id}
  ↓ PlantUpdate (partial validation)
  ↓ PlantService.update()
  ↓ Fetch plant, update fields
  ↓ DB commit
  ↓ PlantResponse
  ↓ 200 OK
```

### Soft Delete Flow
```
DELETE /api/plants/{id}
  ↓ PlantService.delete()
  ↓ Set deleted_at = now()
  ↓ DB commit
  ↓ 204 No Content
```

### Search Flow
```
GET /api/plants/search?q=Monstera
  ↓ PlantService.search(q)
  ↓ Query: name LIKE or scientific_name LIKE
  ↓ Exclude deleted_at != NULL
  ↓ PlantListResponse[]
  ↓ 200 OK
```

---

## 🚀 Next: Phase 3

### Prochaine étape : PHOTOS & HISTORIQUES

- [ ] Photo upload & storage (WebP conversion)
- [ ] Photo display & gallery
- [ ] Watering History CRUD
- [ ] Fertilizing History CRUD
- [ ] Repotting History CRUD
- [ ] Disease History CRUD
- [ ] Plant Notes (PlantHistory) CRUD
- [ ] History display in plant detail

---

## 📊 Database State

**Plants table:** 3 rows (1 Monstera + 2 Pothos)
**Locations:** 7 records (seeded)
**Purchase places:** 8 records (seeded)
**Watering frequencies:** 7 records (seeded)
**Light requirements:** 6 records (seeded)
**Fertilizer types:** 8 records (seeded)

---

**Phase 2 = Foundation Ready for Photos & History** 🎯

Next: Phase 3 in `2.02` branch 🚀

---

*Last updated: 25 Octobre 2025*
*Status: ✅ COMPLETE & SHIPPED*

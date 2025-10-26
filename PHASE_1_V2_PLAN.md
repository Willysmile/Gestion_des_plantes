# 🚀 PHASE 1 - Backend Setup v2 (FastAPI Modernisé)

**Date**: 26 Oct 2025  
**Branche**: `v2-tauri-react`  
**Objectif**: Préparer backend FastAPI solide, moderne, réutilisable pour v2

---

## 📋 Checklist Phase 1

- [ ] 1.1 - Moderniser `backend/app/main.py` (FastAPI setup)
- [ ] 1.2 - Vérifier + nettoyer models (Plant, Photo, relationships)
- [ ] 1.3 - Vérifier + nettoyer schemas Pydantic (PlantCreate, PlantUpdate)
- [ ] 1.4 - Copier PlantService (generate_reference, archive, restore)
- [ ] 1.5 - Vérifier routes CRUD (GET all, GET by id, POST, PUT, DELETE, PATCH)
- [ ] 1.6 - Setup Alembic migrations
- [ ] 1.7 - Setup pytest + tests unitaires backend
- [ ] 1.8 - Requirements.txt à jour + documentation
- [ ] 1.9 - Test local: `uvicorn app.main:app --reload`
- [ ] 1.10 - Commit: "feat: Modernize backend FastAPI for v2"

---

## 🎯 Détails Phase 1

### 1.1 - Moderniser `backend/app/main.py`

**Checklist:**
- [x] FastAPI app initialized
- [x] CORS enabled (pour Tauri frontend)
- [x] Database session dependency
- [x] Health check endpoint `/health` ou `/api/health`
- [x] Root endpoint `/`
- [x] Error handlers
- [x] Startup + shutdown events

**Exemple minimal:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models.base import BaseModel
import os

# Create tables
BaseModel.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion des Plantes API", version="2.0.0")

# CORS for Tauri (development + production)
CORS_ORIGINS = [
    "http://localhost:5173",        # Vite dev server (React)
    "http://127.0.0.1:5173",        # Alternative localhost
    "https://tauri.localhost",      # Tauri production (correct format)
    "tauri://localhost",            # Legacy (fallback)
]

# Add localhost variations if in development
if os.getenv("ENVIRONMENT") != "production":
    CORS_ORIGINS.extend([
        "http://localhost:8000",    # Backend health checks
        "http://127.0.0.1:8000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "🌿 Gestion des Plantes API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "gestion-plantes-api",
        "version": "2.0.0"
    }
```

**⚠️ CORS Clarification:**
- `http://localhost:5173` ✅ Vite dev server (React development)
- `https://tauri.localhost` ✅ Tauri production (correct format)
- `tauri://localhost` ⚠️ Might not work in production (keep for compatibility)
- Verify in Tauri config: `tauri.conf.json` → `build.withGlobalTauri`
- Test in dev: `npm run tauri dev` will show actual origin in browser console

### 1.2 - Vérifier Models

**À vérifier:**
- [x] Plant model: tous les 35 champs présents
- [x] Photo model: relationship vers Plant
- [x] Relationships: photos, histories (watering, fertilizing, etc.)
- [x] Soft delete: `deleted_at`, `is_archived`
- [x] Timestamps: `created_at`, `updated_at`
- [x] Unique constraints: `reference` unique
- [x] Indexes: `name`, `reference`, `is_archived`

**À vérifier aussi:**
- Location model (foreignkey)
- WateringFrequency, LightRequirement models
- History models (WateringHistory, FertilizingHistory, etc.)

### 1.3 - Vérifier Schemas Pydantic

**PlantCreate schema:**
```python
class PlantCreate(BaseModel):
    name: str
    family: Optional[str] = None
    scientific_name: Optional[str] = None
    # ... tous les 35 champs
    
    # Validations
    @model_validator(mode='after')
    def validate_temperatures(self):
        if self.temperature_min and self.temperature_max:
            if self.temperature_min >= self.temperature_max:
                raise ValueError("temperature_min must be < temperature_max")
        return self
```

**PlantUpdate schema:**
- Tous les champs Optional
- Mêmes validations

**PlantResponse schema:**
- Include tous les champs
- Include relationships (photos, etc.)
- Include IDs, timestamps

### 1.4 - Copier PlantService

**Méthodes essentielles:**
```python
class PlantService:
    # Reference generation
    @staticmethod
    def generate_reference(db, family: str) -> str:
        """Generate FAMILY-NNN format reference"""
    
    # Archive/Restore
    @staticmethod
    def archive(db, plant_id: int, reason: str):
        """Archive plant with timestamp + reason"""
    
    @staticmethod
    def restore(db, plant_id: int):
        """Restore plant (clear archive fields)"""
    
    # CRUD
    @staticmethod
    def create(db, plant_data: PlantCreate) -> Plant:
        """Create plant + auto-generate reference + scientific_name"""
    
    @staticmethod
    def get_by_id(db, plant_id: int) -> Optional[Plant]:
        """Get plant by ID (exclude soft-deleted)"""
    
    @staticmethod
    def get_all(db, skip: int = 0, limit: int = 100) -> List[Plant]:
        """Get all active plants (exclude archived + deleted)"""
    
    @staticmethod
    def update(db, plant_id: int, plant_data: PlantUpdate) -> Plant:
        """Update plant fields"""
    
    @staticmethod
    def delete(db, plant_id: int):
        """Soft delete plant"""
```

### 1.5 - Routes CRUD

**Endpoints à avoir:**

```
GET    /api/plants                    - List all plants (paginated)
GET    /api/plants/{id}               - Get plant details
POST   /api/plants                    - Create new plant
PUT    /api/plants/{id}               - Update plant
DELETE /api/plants/{id}               - Delete plant
PATCH  /api/plants/{id}/archive       - Archive plant
PATCH  /api/plants/{id}/restore       - Restore plant
GET    /api/plants/search?q=...       - Search plants
GET    /api/stats                     - KPI stats
```

### 1.6 - Alembic Migrations

**Setup:**
```bash
cd backend
alembic init migrations
```

**Check migrations are there:**
- `migrations/env.py`
- `migrations/script.py.mako`
- `migrations/versions/001_initial.py`

**Run migrations:**
```bash
alembic upgrade head
```

### 1.7 - Pytest Tests

**Structure:**
```
backend/tests/
├── conftest.py                  # Fixtures (db, client, etc.)
├── test_models.py               # Model tests
├── test_plant_service.py        # Service tests
├── test_routes.py               # API endpoint tests
└── __init__.py
```

**Coverage Target:** 80%+

**What to test (priority):**
```
CRITICAL (must have):
✅ PlantService.generate_reference() - all cases
   - Format: FAMILY-NNN
   - Uniqueness
   - Error handling (empty family)
   
✅ PlantService.archive()/restore()
   - Archive sets: is_archived, archived_date, archived_reason
   - Restore clears: is_archived, archived_date, archived_reason
   - Timestamps work correctly
   
✅ Plant model validation
   - temperature_min < temperature_max
   - soil_ph ∈ [0, 14]
   - Cross-field validators work

✅ CRUD routes (happy path + errors)
   - GET /api/plants (list, pagination)
   - GET /api/plants/{id} (found, not found)
   - POST /api/plants (create with validation)
   - PUT /api/plants/{id} (update)
   - DELETE /api/plants/{id} (soft delete)
   - PATCH /api/plants/{id}/archive
   - PATCH /api/plants/{id}/restore

✅ Auto-generated fields
   - reference auto-generated on create
   - scientific_name auto-generated if genus+species

NICE-TO-HAVE:
⚠️ Database transactions
⚠️ Search/filter endpoints
⚠️ Stats/KPI endpoints
⚠️ Error messages clarity
```

**Test command:**
```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_plant_service.py -v

# Run with markers
pytest -m "not slow" -v
```

### 1.8 - Requirements.txt

**Essential (minimalist):**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
alembic==1.12.1
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
```

**Optional (if using env management):**
```
pydantic-settings==2.1.0  # Only if .env config is complex
```

**Why removed:**
- ❌ `pydantic-settings` - Not needed if config in code or simple .env
- ✅ Keep minimal: focus on core dependencies
- ✅ Add later only if needed (YAGNI principle)

### 1.9 - Test Local

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
# Test: http://localhost:8000/api/health
```

### 1.10 - Commit

```bash
git add -A
git commit -m "feat: Modernize backend FastAPI for v2

- Update FastAPI main.py with CORS for Tauri
- Verify all 35 Plant fields present in model
- Update Pydantic v2 schemas with cross-field validators
- Copy PlantService (generate_reference, archive, restore)
- Add CRUD routes (GET, POST, PUT, DELETE, PATCH)
- Setup Alembic migrations
- Add pytest tests (80%+ coverage)
- Update requirements.txt with modern versions
- Ready for Tauri frontend integration"
```

---

## 📊 Logique Métier à Préserver

| Élément | Description |
|---------|-------------|
| **Reference** | Auto-generated FAMILY-NNN format (unique) |
| **Scientific Name** | Auto-generated from Genus + Species |
| **Archive** | Soft delete avec timestamp + raison + restored flag |
| **Validations** | temp_min < max, soil_ph [0-14], archived_reason if archiving |
| **KPIs** | total, active, archived, healthy counts |
| **Soft Delete** | `is_archived` + `deleted_at` flags |

---

## 🔗 Integration Points (Phase 2)

- ✅ Tauri frontend will call these endpoints via HTTP
- ✅ TanStack Query (React Query) for caching
- ✅ Zod for client-side validation

---

## ⏱️ Estimation

- **Setup main.py**: 10 min
- **Verify models/schemas**: 15 min
- **Copy PlantService**: 5 min
- **Add routes**: 20 min
- **Setup Alembic**: 10 min
- **Write tests**: 30 min
- **Documentation**: 10 min
- **Total**: ~100 min (1h 40min)

---

## 🎯 Key Implementation Notes

### Architecture Decisions
- **Database**: Keep SQLite (portable, no server needed for desktop app)
- **ORM**: SQLAlchemy 2.0+ (modern, async-ready)
- **Validation**: Pydantic v2 at routes + model_validator for cross-field
- **Testing**: pytest + fixtures (standard Python testing)
- **Migrations**: Alembic for schema versioning

### Best Practices to Follow
- ✅ Keep business logic in Service layer (easy to test)
- ✅ Keep HTTP handling in routes layer (separation of concerns)
- ✅ Use dependency injection (FastAPI get_db pattern)
- ✅ Soft delete with `is_archived` flag (preserve data history)
- ✅ Auto-generate immutable fields (reference, scientific_name) on create
- ✅ Error handling with proper HTTP status codes
- ✅ OpenAPI documentation (FastAPI auto-docs at /docs)

### CORS Configuration
**Critical for Tauri:**
- ✅ `http://localhost:5173` - Vite dev server
- ✅ `https://tauri.localhost` - Tauri production window
- ❌ `tauri://` protocol may not work consistently
- **Action**: Test both dev + production builds, add origin logging

### Testing Coverage (80%+)
**Must cover:**
1. Reference generation (all edge cases)
2. Archive/Restore workflow (state transitions)
3. Validations (cross-field, boundaries)
4. CRUD operations (happy path + errors)
5. Auto-generated fields (immutability)

**Run before commit:**
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
# Expect: 80%+ coverage (show missing lines)
```

---

## 📝 Known Issues & Decisions

### Issue 1: Pydantic v2 Migration
- **Problem**: v1 used `@field_validator`, now requires `@model_validator` for cross-field
- **Decision**: Use `@model_validator(mode='after')` for temperature_min < max validation
- **Status**: ✅ Already tested in v1, working

### Issue 2: Database Soft Delete
- **Problem**: How to handle archived plants in queries?
- **Decision**: Filter by `is_archived=False` by default in get_all()
- **Alternative**: Could use SQLAlchemy hybrid properties (more advanced)
- **Current**: Keep simple with explicit filtering

### Issue 3: Reference Generation Uniqueness
- **Problem**: FAMILY-NNN format, need to ensure uniqueness
- **Decision**: Unique constraint in DB + index on reference column
- **Testing**: Must test concurrent creation (edge case)
- **Status**: ✅ Already implemented in v1

### Issue 4: Scientific Name Auto-Generation
- **Problem**: Should auto-generate from Genus + Species
- **Decision**: Generate on Plant.__init__ if both present
- **Edge case**: What if genus/species updated later? (accept as is for v2)
- **Status**: ✅ Works in v1, copy as-is

### Issue 5: Photo Relationships
- **Problem**: Plant → Photos (one-to-many)
- **Decision**: Keep relationships intact, add tests for cascade delete
- **Cleanup**: If plant deleted, photos deleted too
- **Status**: ✅ Configured in models

---

## ✅ Pre-Commit Checklist

Before `git commit`:

- [ ] All tests passing: `pytest tests/ -v`
- [ ] Coverage 80%+: `pytest --cov`
- [ ] Code formatted: `black app/` (if using)
- [ ] API docs work: `http://localhost:8000/docs`
- [ ] Health check works: `http://localhost:8000/api/health`
- [ ] CORS tested (check browser console for errors)
- [ ] Alembic migrations applied: `alembic upgrade head`
- [ ] No import errors: `python -c "from app.main import app"`
- [ ] Requirements.txt clean: only what's used

**Status**: 🔄 Ready to start  
**Next Phase**: Phase 2 - Frontend Tauri + React setup

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
from app.config import settings
from app.database import engine
from app.models.base import BaseModel

# Create tables
BaseModel.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion des Plantes API")

# CORS for Tauri
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "tauri://localhost"],  # Tauri dev + prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🌿 Gestion des Plantes API"}

@app.get("/api/health")
def health():
    return {"status": "ok"}
```

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
├── conftest.py           # Fixtures (db, client, etc.)
├── test_models.py        # Model tests
├── test_plant_service.py # Service tests (reference generation, archive, etc.)
└── test_routes.py        # API endpoint tests
```

**Coverage target:** 80%+

### 1.8 - Requirements.txt

**Essential:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
alembic==1.12.1
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
```

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

## 📝 Notes

- Keep existing database structure
- Migrate from PySimpleGUI API to REST API best practices
- Add proper error handling + logging
- Add request validation at routes level
- Add response documentation (OpenAPI schema)

**Status**: 🔄 Ready to start  
**Next Phase**: Phase 2 - Frontend Tauri + React setup

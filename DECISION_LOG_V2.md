# 📋 DECISION LOG - v2 Reboot Decisions (26 Oct 2025)

**Purpose**: Track architectural decisions, rationale, and alternatives for Phase 1-2

---

## 🔀 CORS Configuration

**Decision**: Allow both `http://localhost:5173` (Vite dev) and `https://tauri.localhost` (Tauri production)

**Rationale**:
- Vite dev server runs on port 5173 by default
- Tauri production needs `tauri.localhost` (not `tauri://` protocol)
- Testing requires both environments

**Alternative Rejected**:
- ❌ `tauri://localhost` protocol (may not work in production)
- ❌ Wildcard `*` (security risk, open to all origins)

**Implementation**:
```python
CORS_ORIGINS = [
    "http://localhost:5173",        # Vite dev
    "https://tauri.localhost",      # Tauri production
]
```

**Testing**: 
- [ ] Verify in browser console (Origin header)
- [ ] Test in `npm run tauri dev`
- [ ] Test in `npm run tauri build`

---

## 📦 Requirements.txt Strategy

**Decision**: Keep minimal dependencies (only what's essential)

**Removed**:
- ❌ `pydantic-settings` - Not needed if config in code
- ❌ Extra logging libraries - Use Python built-in logging

**Kept**:
- ✅ `fastapi` - API framework
- ✅ `uvicorn` - ASGI server
- ✅ `sqlalchemy` - ORM
- ✅ `pydantic` - Validation
- ✅ `alembic` - Migrations
- ✅ `pytest` - Testing
- ✅ `python-dotenv` - .env support

**Rationale**:
- YAGNI principle (You Ain't Gonna Need It)
- Add dependencies only when needed
- Easier to maintain, fewer conflicts
- Faster installation for developers

**Future**: Add `pydantic-settings` only if config becomes complex

---

## 🧪 Testing Coverage Strategy

**Decision**: 80%+ coverage focusing on critical paths

**Coverage Breakdown**:
```
CRITICAL (MUST TEST):
  - Reference generation (format, uniqueness, errors)
  - Archive/restore workflow (state transitions)
  - Plant validations (temperature, soil_ph, cross-field)
  - CRUD routes (happy path + errors)
  - Auto-generated fields (immutability)

IMPORTANT:
  - Search/filter functionality
  - Soft delete behavior
  - Relationship cascades

NICE-TO-HAVE:
  - Edge cases (concurrent creation)
  - Performance (slow queries)
  - Error message clarity
```

**Why 80% not 100%?**
- 100% often means testing trivial code (diminishing returns)
- 80% covers critical business logic + happy paths
- Focus on value, not vanity metrics

**Test Structure**:
```
backend/tests/
├── conftest.py              # Shared fixtures
├── test_models.py           # Model validation tests
├── test_plant_service.py    # Business logic tests
├── test_routes.py           # API endpoint tests
└── test_fixtures.py         # Sample data generators
```

---

## 🎯 Service Layer Pattern

**Decision**: Keep business logic in PlantService (separate from routes)

**Rationale**:
- Easy to test (no HTTP dependencies)
- Reusable across multiple endpoints
- Clear separation of concerns
- Can be used by CLI, scripts, etc.

**Pattern**:
```python
# routes/plants.py
@app.post("/api/plants")
def create_plant(plant_data: PlantCreate):
    return PlantService.create(db, plant_data)

# services/plant_service.py
class PlantService:
    @staticmethod
    def create(db, plant_data: PlantCreate) -> Plant:
        # Business logic here
        ref = PlantService.generate_reference(db, plant_data.family)
        plant = Plant(**plant_data.dict(), reference=ref)
        db.add(plant)
        db.commit()
        return plant
```

---

## 🔐 Database Soft Delete Strategy

**Decision**: Use `is_archived` flag + `deleted_at` timestamp (soft delete)

**Why Soft Delete?**
- ✅ Preserve data history (audit trail)
- ✅ Enable archive/restore workflow
- ✅ Easy to undelete accidentally deleted records
- ✅ No CASCADE DELETE issues

**Implementation**:
```python
# In models
class Plant(BaseModel):
    is_archived = Column(Boolean, default=False, index=True)
    archived_date = Column(DateTime, nullable=True)
    archived_reason = Column(String(255), nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # For hard delete later

# In queries
def get_all(db):
    return db.query(Plant).filter(Plant.is_archived == False).all()
```

**Alternative Rejected**:
- ❌ Hard delete (lose data)
- ❌ Complete soft delete (no historical tracking)

---

## 🏗️ Auto-Generated Fields (Reference + Scientific Name)

**Decision**: Auto-generate on Plant creation, never update

**Reference Generation**:
```python
# Auto-generate FAMILY-NNN format
def generate_reference(db, family):
    prefix = family[:5].upper()
    existing = db.query(Plant).filter(
        Plant.reference.like(f"{prefix}-%")
    ).count()
    return f"{prefix}-{existing+1:03d}"
```

**Scientific Name Generation**:
```python
# Auto-generate from Genus + Species
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if self.genus and self.species and not self.scientific_name:
        self.scientific_name = f"{self.genus.capitalize()} {self.species.lower()}"
```

**Why Immutable?**
- ✅ Reference is unique identifier (database integrity)
- ✅ Scientific name follows Linnaean nomenclature (standardized)
- ✅ Both are auto-generated (no manual entry, no conflicts)

**Note**: If genus/species updated later, scientific_name NOT re-generated (by design)

---

## 🔗 Tauri ↔ Backend Communication

**Decision**: Simple HTTP requests (no Tauri invoke/commands)

**Rationale**:
- ✅ Standard REST API (works with any client)
- ✅ Same backend usable for web app later
- ✅ TanStack Query handles caching/retries
- ✅ Browser dev tools (network tab debugging)

**Alternative Considered**:
- ⚠️ Tauri invoke (backend Rust commands) - Rejected because:
  - Backend written in Python (not Rust)
  - Would require Tauri backend layer
  - Less portable

**Implementation**:
```typescript
// Frontend (React + TanStack Query)
const { data } = useQuery({
  queryKey: ['plants'],
  queryFn: () => fetch('http://localhost:8000/api/plants')
                  .then(r => r.json())
});
```

---

## 📊 Database Choice: SQLite

**Decision**: Keep SQLite for v2 (no PostgreSQL migration)

**Rationale**:
- ✅ Desktop app (no server needed)
- ✅ Single file database (portable)
- ✅ Good performance for CRUD operations
- ✅ Full transactions support
- ✅ Already working in v1

**Scalability Note**:
- SQLite is suitable for < 100k records
- For larger data: consider migration to PostgreSQL later
- Alembic migrations make switching easier

---

## 🚀 Frontend Framework: Tauri + React

**Decision**: Tauri (not Electron) + React (not Vue)

**Rationale - Tauri**:
- ✅ Smaller binary (~3MB vs Electron 200MB+)
- ✅ Faster startup
- ✅ Native performance
- ✅ Security-focused
- ✅ Web-based UI + Rust backend capable

**Rationale - React**:
- ✅ Largest ecosystem
- ✅ TanStack Query (best data fetching)
- ✅ shadcn/ui (component library)
- ✅ Job market friendly

**Why Not Vue/Svelte?**:
- Vue: Smaller ecosystem, fewer libraries
- Svelte: Smaller community for Tauri integration

---

## 🛠️ Tooling: Vite + pnpm

**Decision**: Use Vite (not webpack/CRA) + pnpm (not npm)

**Rationale - Vite**:
- ✅ Fast development (HMR in milliseconds)
- ✅ Small build size
- ✅ Native ES modules
- ✅ Tailwind CSS first-class support

**Rationale - pnpm**:
- ✅ Faster than npm
- ✅ Stricter dependency management
- ✅ Less disk space

**Alternative**: npm works fine too (stick with npm if team preference)

---

## 📝 Validation Strategy

**Decision**: Pydantic v2 (backend) + Zod (frontend)

**Backend (Pydantic)**:
```python
class PlantCreate(BaseModel):
    temperature_min: Optional[int] = None
    temperature_max: Optional[int] = None
    
    @model_validator(mode='after')
    def validate_temp(self):
        if self.temperature_min and self.temperature_max:
            if self.temperature_min >= self.temperature_max:
                raise ValueError("...")
        return self
```

**Frontend (Zod)**:
```typescript
const PlantSchema = z.object({
  temperature_min: z.number().optional(),
  temperature_max: z.number().optional(),
}).refine(
  (data) => !data.temp_min || !data.temp_max || temp_min < temp_max,
  { message: "..." }
);
```

**Why Both?**
- Pydantic: Protects backend (never trust client)
- Zod: Provides instant feedback in UI (better UX)

---

---

## ⚠️ Potential Issues & Monitoring (Watch List)

### Issue 1: CORS with Tauri Production Build

**Risk Level**: 🔴 **HIGH** (blocking)

**Problem**:
- `https://tauri.localhost` works in theory
- Actual Tauri build may use different origin
- CORS failures = app can't communicate with backend

**Monitoring**:
- [ ] Test immediately after `npm run tauri build`
- [ ] Check browser console for CORS errors
- [ ] Log actual Origin header from request

**Troubleshooting Checklist**:
```bash
# 1. Build Tauri app
npm run tauri build

# 2. Run backend
uvicorn app.main:app --reload

# 3. Check console for actual origin being sent
# Expected: "https://tauri.localhost" or similar

# 4. If CORS error, add to CORS_ORIGINS:
CORS_ORIGINS = [
    "http://localhost:5173",           # Vite dev
    "https://tauri.localhost",         # Theory
    "https://localhost:1430",          # Possible fallback
    "app://localhost",                 # Alternative
]

# 5. Test with curl to verify backend
curl -H "Origin: https://tauri.localhost" http://localhost:8000/api/health
```

**Resolution Path**:
1. Launch production build + monitor
2. If CORS fails, check actual origin in browser
3. Add discovered origin to CORS_ORIGINS
4. Document actual origin used by Tauri

**Status**: ⏳ TO TEST (Phase 2)

---

### Issue 2: Reference Generation - Family Prefix Collision

**Risk Level**: 🟡 **MEDIUM** (data integrity)

**Problem**:
```
Current implementation:
  prefix = family[:5].upper()
  
Examples:
  "Araceae" → "ARACA"
  "Arachnida" → "ARACH"  ← Different family, same prefix!
  "Aralia" → "ARALI"
```

**Collision Scenarios**:
- ARACA-001 (Araceae family)
- ARACH-001 (Arachnida family)  ← OK, different
- But what if both families start with ARACAE...?

**Current Implementation** (v1):
```python
prefix = family[:5].upper()  # Takes first 5 letters
count = db.query(Plant).filter(
    Plant.reference.like(f"{prefix}-%")
).count()
return f"{prefix}-{count+1:03d}"
```

**Potential Fix**:
```python
# Option A: Use full family name (safer)
prefix = family.upper()[:5]  # Still first 5, but clearer

# Option B: Use full family name hash (unique)
import hashlib
prefix = hashlib.md5(family.encode()).hexdigest()[:5].upper()

# Option C: Document and accept (current approach)
# With full family stored, collisions rare in practice
```

**Current Assessment**:
- ✅ Collision unlikely in practice (35 common plant families)
- ✅ Family name stored separately (can disambiguate)
- ⚠️ But should document this decision

**Action**:
- [ ] Add comment in code explaining prefix strategy
- [ ] Monitor for actual collisions (unlikely before 10k plants)
- [ ] If collision happens, implement Option B

**Documentation to Add**:
```python
"""
Reference Generation Strategy:
  Format: FAMILY-NNN (5-letter family prefix + counter)
  
  Example:
    Family: "Araceae" → Prefix: "ARACA"
    First plant: ARACA-001
    Second plant: ARACA-002
  
  Note on collisions:
    - Prefix is first 5 letters of family name
    - Same prefix ≠ same family (rare but possible)
    - Full family name stored in DB for disambiguation
    - If collision detected, consider hash-based prefix
"""
```

**Status**: ⏳ MONITOR (Phase 1 implementation)

---

### Issue 3: SQLite Scalability Beyond 100k Records

**Risk Level**: 🟢 **LOW** (future concern)

**Problem**:
- SQLite good for < 100k records
- Beyond that: slower queries, larger file size
- No built-in clustering/replication

**Current Assessment**:
```
📊 Typical usage:
  - Casual user: 50-200 plants
  - Dedicated user: 500-2k plants
  - Power user: 5k-50k plants
  - Large collection: 50k+ (rare for one person)
  
Estimate: Most users stay < 10k plants
Timeline: Years before hitting 100k (if ever)
```

**Monitoring Strategy**:
- [ ] Track database file size in deployment
- [ ] Monitor query performance (create index if slow)
- [ ] Log slow queries (> 500ms)

**When to Migrate** (if needed):
- Database file > 500MB
- Query response time > 1 second
- More than 1 user with shared database

**Migration Path to PostgreSQL**:
```bash
# If migration needed:
1. Alembic already in place (easy to migrate schemas)
2. SQLAlchemy DB-agnostic (code stays same)
3. Just change connection string
4. Run migrations on new database

# Code stays same, only connection changes:
# OLD: sqlite:///./data/plants.db
# NEW: postgresql://user:pass@localhost/plants
```

**Current Decision**: 
- ✅ Keep SQLite for v2 (MVP focus)
- ✅ Document migration path
- ⏳ Revisit if user base grows

**Status**: ✅ ACCEPTABLE (Phase 1, revisit later)

---

### Issue 4: Concurrent Access (Multiple Users)

**Risk Level**: 🟡 **MEDIUM** (if shared database later)

**Current Assumption**: Single-user desktop app (one person, one database)

**Scenario If Multi-User Later**:
- SQLite has row-level locking (not optimal for concurrency)
- Race conditions possible (especially reference generation)

**Current Protection**:
```python
# Database transaction ensures atomicity
def generate_reference(db, family):
    db.begin()  # Start transaction
    # Get count + increment atomically
    db.commit()  # Commit transaction
```

**If Multi-User Becomes Requirement**:
- Migrate to PostgreSQL (full ACID compliance)
- Use connection pooling (PgBouncer)
- Implement row-level versioning (optimistic locking)

**Current Status**: 
- ✅ Not a problem (single-user desktop app)
- ⏳ Revisit if web version planned

**Status**: ✅ ACCEPTABLE (Phase 1)

---

## 🎯 Summary: Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Desktop Framework** | Tauri | Small, fast, modern |
| **Frontend Framework** | React | Ecosystem, libraries |
| **Database** | SQLite | Portable, no server |
| **API Pattern** | REST HTTP | Standard, portable |
| **Validation** | Pydantic + Zod | Backend security + UX |
| **Testing** | pytest | Python standard |
| **Coverage** | 80%+ | Practical, valuable |
| **Requirements** | Minimal | YAGNI principle |
| **Soft Delete** | is_archived flag | Preserve history |
| **Service Layer** | Separate | Testability, reuse |

---

## 📋 Watch List (Before Production)

| Issue | Risk | Status | Action |
|-------|------|--------|--------|
| CORS with Tauri build | 🔴 HIGH | ⏳ TO TEST | Test immediately after build |
| Reference prefix collision | 🟡 MEDIUM | ⏳ MONITOR | Add code comment, check if collision occurs |
| SQLite 100k+ records | 🟢 LOW | ✅ OK | Document migration path, revisit if needed |
| Multi-user access | 🟡 MEDIUM | ✅ OK | Single-user for now, migrate if needed |

---

**Next Review**: After Phase 1 completion  
**Last Updated**: 26 Oct 2025  
**Status**: ✅ Consensus reached + Watch List defined

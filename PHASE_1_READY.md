# ✅ PRE-PHASE 1 CHECKLIST - Ready to Code

**Date**: 26 Oct 2025  
**Status**: 🟢 **READY TO LAUNCH**  
**Branch**: `v2-tauri-react`

---

## 📋 Documentation Complete

- ✅ README.md - Project overview
- ✅ PHASE_1_V2_PLAN.md - Backend detailed checklist (1h 40min work)
- ✅ PHASE_2_V2_PLAN.md - Frontend detailed checklist (1h 20min work)
- ✅ RECAP_PHASE_1_V2.md - Comprehensive summary
- ✅ DECISION_LOG_V2.md - Architecture decisions + watch list

**Total Documentation**: 65 KB of detailed plans + rationale

---

## 🗂️ Repository Structure Verified

```
✅ backend/              (FastAPI ready to modernize)
✅ data/                 (SQLite database intact)
✅ docs-v1/              (v1 archived - 76 files)
✅ README.md             (v2 intro)
✅ PHASE_*.md            (detailed plans)
✅ DECISION_LOG_V2.md    (decisions + watch list)
✅ .gitignore            (proper)
✅ .git/                 (clean history)
```

---

## 🔑 Key Points Before Starting Phase 1

### Business Logic ✅ Preserved
- [x] Reference Generation (FAMILY-NNN format)
- [x] Archive/Restore workflow (timestamps + reason)
- [x] Scientific Name auto-generation (Genus + Species)
- [x] 35 Plant fields intact
- [x] Cross-field validations
- [x] KPI metrics structure

### Tech Stack Decided ✅
- [x] Backend: FastAPI + SQLAlchemy 2.0 + Pydantic v2
- [x] Database: SQLite (portable, no server)
- [x] Testing: pytest (80%+ coverage)
- [x] Migrations: Alembic
- [x] Frontend: Tauri + React + TypeScript (Phase 2)

### Watch List Identified ✅
- [x] CORS with Tauri build (must test immediately)
- [x] Reference prefix collision (document, monitor)
- [x] SQLite scalability (OK for MVP, revisit at 100k)

---

## 🚀 Phase 1 Work (Ready to Start)

**Estimated Time**: 1 hour 40 minutes

**10-Item Checklist**:
```
[ ] 1.1 - Modernise backend/app/main.py
    - FastAPI app with CORS for Tauri
    - Health check endpoint
    - Error handlers

[ ] 1.2 - Verify + clean models
    - All 35 Plant fields present
    - Relationships configured
    - Soft delete setup
    - Indexes on important columns

[ ] 1.3 - Verify + clean Pydantic schemas
    - PlantCreate with validations
    - PlantUpdate with optional fields
    - PlantResponse with all details
    - Cross-field validators (temperature, soil_ph)

[ ] 1.4 - Copy PlantService
    - generate_reference() method
    - archive() and restore() methods
    - Full CRUD methods
    - Keep business logic here

[ ] 1.5 - Add CRUD routes
    - GET /api/plants (list)
    - GET /api/plants/{id} (detail)
    - POST /api/plants (create)
    - PUT /api/plants/{id} (update)
    - DELETE /api/plants/{id} (delete)
    - PATCH /api/plants/{id}/archive
    - PATCH /api/plants/{id}/restore

[ ] 1.6 - Setup Alembic migrations
    - alembic init migrations
    - Configure sqlalchemy.url in alembic.ini
    - Create initial migration
    - Run: alembic upgrade head

[ ] 1.7 - Setup pytest + tests
    - Create tests/ directory
    - Write conftest.py (fixtures)
    - Test reference generation
    - Test archive/restore
    - Test CRUD routes
    - Target: 80%+ coverage

[ ] 1.8 - Update requirements.txt
    - fastapi==0.104.1
    - uvicorn==0.24.0
    - sqlalchemy==2.0.23
    - pydantic==2.5.0
    - alembic==1.12.1
    - pytest==7.4.3
    - pytest-cov==4.1.0
    - python-dotenv==1.0.0

[ ] 1.9 - Test local backend
    - pytest tests/ -v --cov (expect 80%+)
    - uvicorn app.main:app --reload
    - Visit http://localhost:8000/docs (FastAPI UI)
    - Test GET /api/health → {"status": "ok"}

[ ] 1.10 - Commit + push
    - Message: "feat: Modernize backend FastAPI for v2"
    - Include all updates
```

---

## 🎯 Success Criteria (Phase 1 Complete)

**All of these must be true**:

- ✅ All tests passing: `pytest tests/ -v`
- ✅ Coverage 80%+: `pytest --cov=app`
- ✅ No import errors: Backend starts cleanly
- ✅ Health check works: `curl http://localhost:8000/api/health`
- ✅ FastAPI docs available: `http://localhost:8000/docs`
- ✅ CORS configured: Origins list ready for Tauri
- ✅ Alembic migrations: `alembic upgrade head` works
- ✅ Requirements.txt: Only essential packages, minimal
- ✅ Git history: Clean commit with descriptive message
- ✅ No broken references: All services + routes working

---

## 🔐 Watch List During Phase 1

**Keep Eye On**:

1. **Pydantic v2 Migration**
   - Cross-field validators must use `@model_validator(mode='after')`
   - Not `@field_validator` (that's v1)

2. **Reference Generation**
   - Test uniqueness constraint works
   - Test collision handling (rare but possible)
   - Document in code comments

3. **Test Coverage**
   - Aim for 80%+
   - Focus on critical paths (reference, archive, CRUD)
   - Don't chase 100% (diminishing returns)

4. **SQLite Performance**
   - Monitor query times (shouldn't exceed 100ms for CRUD)
   - Index on `name`, `reference`, `is_archived` present

---

## 📦 Environment Setup

**Before Starting**:

```bash
# 1. Verify Python version
python --version  # Should be 3.8+

# 2. Navigate to project
cd /home/willysmile/Documents/Gestion_des_plantes

# 3. Switch to correct branch
git checkout v2-tauri-react

# 4. Create backend venv
cd backend
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# 5. Install dependencies
pip install -r requirements.txt  # (to be updated in step 1.8)

# 6. Run initial test
pytest tests/ -v  # (will fail initially, that's ok)
```

---

## 🎬 First 5 Minutes (Kickoff)

```bash
# 1. Activate environment
cd backend
source venv/bin/activate

# 2. Check current state
ls -la app/
# Should see: main.py, models/, schemas/, services/, routes/

# 3. Open main.py
code app/main.py  # or your editor

# 4. Start with 1.1 checklist item
# Update FastAPI app, add CORS for Tauri

# 5. Test
uvicorn app.main:app --reload
# Visit: http://localhost:8000/api/health
```

---

## 📞 If Stuck

**Common Issues**:

| Issue | Solution |
|-------|----------|
| Import errors | Check venv is activated |
| `ModuleNotFoundError: No module named 'fastapi'` | `pip install -r requirements.txt` |
| Tests don't run | `pytest tests/` (need conftest.py) |
| CORS errors (later in Phase 2) | Add origin to CORS_ORIGINS list |
| Alembic connection error | Check `sqlalchemy.url` in alembic.ini |

**Documentation Links**:
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic v2: https://docs.pydantic.dev/latest/
- Alembic: https://alembic.sqlalchemy.org/
- pytest: https://docs.pytest.org/

---

## ✨ Final Checklist (Ready to Code?)

- [x] Documentation complete (5 files, 65 KB)
- [x] Business logic understood (preserved from v1)
- [x] Tech stack decided (FastAPI + React + Tauri)
- [x] Architecture decisions logged (with rationale)
- [x] Watch list identified (CORS, collision, scalability)
- [x] Repository clean (branch ready, v1 archived)
- [x] Phase 1 detailed (10-item checklist)
- [x] Success criteria defined
- [x] Environment setup documented
- [x] This checklist completed!

---

## 🚀 **Status: 🟢 READY TO LAUNCH PHASE 1**

**Next Step**: Open `backend/app/main.py` and start with checklist item 1.1

**Estimated Completion**: ~1 hour 40 minutes

**When Done**: Commit and push to `v2-tauri-react` branch

---

**Created**: 26 Oct 2025  
**By**: GitHub Copilot  
**Status**: ✅ Ready to code

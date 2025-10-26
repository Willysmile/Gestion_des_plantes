# 🌿 Gestion des Plantes - v2 (Tauri + React + FastAPI)

Plant management application rebuilt from scratch with modern tech stack.

---

## 📁 Project Structure

```
gestion-plantes/
├── docs/                    # v2 Documentation (Phase 1-2 planning)
│   ├── INDEX.md             ← Start here (navigation hub)
│   ├── PHASE_1_READY.md     ← Green light to code
│   ├── PHASE_1_V2_PLAN.md   ← Backend detailed plan (1h 40min)
│   ├── PHASE_2_V2_PLAN.md   ← Frontend detailed plan (1h 20min)
│   ├── DECISION_LOG_V2.md   ← Architecture decisions + watch list
│   └── RECAP_PHASE_1_V2.md  ← Summary of today's work
│
├── old-docs/                # Archived v1 documentation
│   ├── README-v1.md         ← v1 overview
│   ├── tests-v1/            ← Old test files (15 tests)
│   ├── phases/              ← Phase 1-6 reports
│   └── docs-preparation/    ← Project preparation
│
├── backend/                 # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── models/          # SQLAlchemy models (35 plant fields)
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routes/          # API endpoints (CRUD + archive)
│   │   └── services/        # Business logic (PlantService)
│   ├── migrations/          # Alembic migrations
│   ├── tests/               # pytest tests (80%+ coverage)
│   ├── requirements.txt
│   └── alembic.ini
│
├── data/                    # Database
│   ├── plants.db            # SQLite database
│   ├── exports/             # Export files
│   └── photos/              # Plant photos
│
├── .gitignore
└── README.md                # This file
```

---

## 🚀 Quick Start

### Documentation First

```bash
# 1. Read the index
cat docs/INDEX.md

# 2. Read Phase 1 ready checklist
cat docs/PHASE_1_READY.md

# 3. Read Phase 1 detailed plan
cat docs/PHASE_1_V2_PLAN.md
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload
# Visit: http://localhost:8000/docs (FastAPI UI)
```

### Frontend Setup (Phase 2)

```bash
# (After Phase 1 complete)
cd frontend
npm install
npm run tauri dev
```

---

## 📚 Documentation Files

| File | Purpose | Read When |
|------|---------|-----------|
| **docs/INDEX.md** | Navigation hub + quick links | First thing |
| **docs/PHASE_1_READY.md** | Ready to code checklist | Before Phase 1 |
| **docs/PHASE_1_V2_PLAN.md** | Backend: 10 detailed items | Doing Phase 1 |
| **docs/PHASE_2_V2_PLAN.md** | Frontend: 10 detailed items | After Phase 1 |
| **docs/DECISION_LOG_V2.md** | Architecture decisions + watch list | Understanding why |
| **docs/RECAP_PHASE_1_V2.md** | Today's summary (26 Oct 2025) | Project overview |
| **old-docs/README-v1.md** | v1 overview | Learning from v1 |

---

## 🎯 Quick Start for Phase 1

```bash
# 1. Read docs
cat docs/INDEX.md
cat docs/PHASE_1_READY.md

# 2. Navigate
cd backend

# 3. Create venv (if first time)
python -m venv venv
source venv/bin/activate

# 4. Install deps
pip install -r requirements.txt

# 5. Open editor
code app/main.py

# 6. Start Phase 1 checklist item 1.1
# (Modernize FastAPI main.py)
```

**Estimated Time**: 1h 40min

---

## 🔑 Key Points

### Business Logic ✅ Preserved from v1
- **Reference Generation**: Auto-format FAMILY-NNN (unique)
- **Archive/Restore**: With timestamps + reason
- **Scientific Name**: Auto-generated from Genus + Species
- **35 Plant Fields**: All present in models
- **Cross-Field Validations**: temperature_min < max, soil_ph [0-14]
- **KPI Metrics**: total, active, archived, healthy counts
- **Soft Delete**: Preserve data history with `is_archived` flag

### Tech Stack ✨ Modern & Professional
- **Backend**: FastAPI + SQLAlchemy 2.0 + Pydantic v2
- **Database**: SQLite (portable, no server needed)
- **Testing**: pytest (80%+ coverage target)
- **Frontend**: Tauri + React + TypeScript (Phase 2)
- **Styling**: Tailwind CSS + shadcn/ui (Phase 2)

### Architecture 🏗️ Clean & Maintainable
- Service layer pattern (business logic separated)
- REST API (standard HTTP, no Tauri invoke)
- Dependency injection (FastAPI get_db pattern)
- Alembic migrations (schema versioning)
- TanStack Query (React data fetching + caching)

---

## 📊 Development Timeline

| Phase | Task | Time | Status |
|-------|------|------|--------|
| 0 | Planning | 3h | ✅ DONE |
| 1 | Backend FastAPI | 1h 40min | 🔄 READY |
| 2 | Frontend Tauri | 1h 20min | ⏳ NEXT |
| 3 | Plants UI | 2h | ⏳ P3 |
| 4 | Dashboard | 1h | ⏳ P4 |
| 5 | Settings | 1h 30min | ⏳ P5 |
| 6 | Testing | 2h | ⏳ P6 |
| 7 | Build | 1h | ⏳ P7 |
| **TOTAL** | | **~11h** | |

---

## ⚠️ Watch List

Before going to production, monitor these issues:

| Issue | Risk | Action |
|-------|------|--------|
| CORS Tauri build | 🔴 HIGH | Test immediately after build |
| Reference prefix collision | 🟡 MEDIUM | Document code, monitor for collisions |
| SQLite 100k+ records | 🟢 LOW | Revisit if data grows |

See `docs/DECISION_LOG_V2.md` for details.

---

## 📝 Branches

- **master**: Stable (Phase 1-6 complete, squashed)
- **v2-tauri-react**: Current development (THIS BRANCH)

---

## 🔗 Useful Links

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic v2**: https://docs.pydantic.dev/latest/
- **Tauri**: https://tauri.app/
- **React**: https://react.dev/
- **TanStack Query**: https://tanstack.com/query/
- **shadcn/ui**: https://ui.shadcn.com/

---

## 📞 FAQ

**Q: Where do I start?**  
A: Read `docs/INDEX.md` then `docs/PHASE_1_READY.md`

**Q: How long is Phase 1?**  
A: ~1 hour 40 minutes (detailed 10-item checklist in `docs/PHASE_1_V2_PLAN.md`)

**Q: What happened to v1?**  
A: Archived in `old-docs/` (complete history preserved)

**Q: Where are the decisions documented?**  
A: `docs/DECISION_LOG_V2.md` (with rationale + alternatives)

**Q: What could go wrong?**  
A: Watch list in `docs/DECISION_LOG_V2.md` (CORS, collision, scalability)

---

## 📝 License

Private project - 2025

---

**Status**: 🟢 **READY TO CODE PHASE 1**  
**Branch**: `v2-tauri-react`  
**Last Update**: 26 Oct 2025  
**Next**: Start Phase 1 (Backend FastAPI)

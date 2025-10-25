# 🎯 PLAN D'ACTION DÉTAILLÉ - PHASE 1 À 5

**Objectif:** Migrer Plant Manager de Laravel → Python (FastAPI + PySimpleGUI)  
**Durée estimée:** 5-8 semaines (temps plein)  
**Cible:** Application desktop standalone avec tous les features

---

## 📌 PRIORISATION DES TÂCHES

### 🔴 CRITIQUE (Must have)
1. Backend API + DB setup
2. CRUD plantes
3. CRUD photos
4. Frontend UI basique (list, detail)
5. Export/Import

### 🟡 IMPORTANT (Should have)
1. Historiques (tous les types)
2. Tags & catégories
3. Filtres & recherche
4. Settings (lookups)
5. Statistiques

### 🟢 NICE TO HAVE (Could have)
1. Audit logging
2. Soft delete + recovery
3. Dark mode UI
4. Recommandations IA
5. Sync cloud

---

## 📅 PHASE 1: SETUP & INFRA (Week 1)

### Tâche 1.1: Structure projet Python
- [ ] Créer dossiers: `/backend` et `/frontend`
- [ ] Initialize Git pour nouveau repo (séparer du Laravel)
- [ ] Setup `.gitignore` (Python, __pycache__, .venv, data/, etc)
- [ ] Create `README.md` with installation instructions
- [ ] Create `/data` folder avec structure (photos/, exports/, db/)

**Sortie:** Repo prêt avec structure de base

### Tâche 1.2: Backend - Setup FastAPI
- [ ] Initialize virtual environment
- [ ] Create `requirements.txt` (fastapi, uvicorn, sqlalchemy, pydantic, etc)
- [ ] Create `app/main.py` (FastAPI app)
- [ ] Create `app/config.py` (settings, db url, etc)
- [ ] Setup SQLAlchemy ORM + database connection
- [ ] Create `app/utils/db.py` (init DB, session manager)
- [ ] Create basic health check endpoint: `GET /health`

**Sortie:** FastAPI runs on http://localhost:8000 ✅

### Tâche 1.3: Backend - Database Models
- [ ] Create `app/models/base.py` (BaseModel with timestamps)
- [ ] Create models: Plant, Photo, Location, PurchasePlace
- [ ] Create models: WateringFrequency, LightRequirement, FertilizerType
- [ ] Create models: WateringHistory, FertilizingHistory, RepottingHistory, DiseaseHistory, PlantHistory
- [ ] Create models: Tag, TagCategory
- [ ] Create models: AuditLog (for tracking)
- [ ] Add all relationships + foreign keys
- [ ] Create migrations folder (Alembic)

**Sortie:** All 15 models defined, migrations generated

### Tâche 1.4: Frontend - Setup PySimpleGUI
- [ ] Initialize virtual environment
- [ ] Create `requirements.txt` (pysimplegui, requests, pillow, etc)
- [ ] Create `app/main.py` (PySimpleGUI entry)
- [ ] Create `app/api_client.py` (wrapper autour requests, error handling)
- [ ] Create `app/config.py` (API base URL, timeouts, etc)
- [ ] Create basic connection test to backend

**Sortie:** Frontend can reach backend ✅

### Tâche 1.5: Documentation
- [ ] Update `README.md` with quick start
- [ ] Create `DEVELOPMENT.md` (setup pour devs)
- [ ] Create `API_DOCUMENTATION.md` (endpoints détaillés)
- [ ] Add both cahiers des charges aux repo

**Sortie:** Clear onboarding docs

---

## 📅 PHASE 2: CRUD PLANTES (Week 2-3)

### Tâche 2.1: Backend - Pydantic Schemas
- [ ] Create `app/schemas/plant_schema.py`
  - PlantCreate (pour POST)
  - PlantUpdate (pour PUT)
  - PlantResponse (pour GET)
  - PlantDetail (avec relations)
- [ ] Create schemas pour photos, historiques, etc
- [ ] Add validation rules (min/max lengths, enums, etc)

**Sortie:** All Pydantic models defined

### Tâche 2.2: Backend - Plant Service
- [ ] Create `app/services/plant_service.py`
  - `get_all_plants(skip, limit, filters)` - list with pagination
  - `get_plant(id)` - detail
  - `create_plant(data)` - create with validation
  - `update_plant(id, data)` - update
  - `delete_plant(id)` - soft delete
  - `archive_plant(id)` - archive
  - `restore_plant(id)` - restore
  - `get_archived_plants()` - list archived
  - `generate_reference(plant_data)` - auto-ref (TYPE-DATE-COUNTER)

**Sortie:** PlantService with all CRUD operations

### Tâche 2.3: Backend - Plant Routes
- [ ] Create `app/routes/plants.py`
- [ ] Implement 12 endpoints:
  ```
  GET    /api/plants
  POST   /api/plants
  GET    /api/plants/{id}
  PUT    /api/plants/{id}
  DELETE /api/plants/{id}
  POST   /api/plants/{id}/archive
  POST   /api/plants/{id}/restore
  GET    /api/plants/archived
  GET    /api/plants/search?q=...
  POST   /api/plants/generate-reference
  ```
- [ ] Add error handling (404, 400, 500)
- [ ] Add input validation (Pydantic)

**Sortie:** Backend can CRUD plants fully ✅

### Tâche 2.4: Frontend - Main Window
- [ ] Create `app/windows/main_window.py`
  - Menu bar (File, Edit, View, Help)
  - Search bar with autocomplete
  - Filter panel (Location, Tag, Difficulty, Type)
  - Plant table (columns: Photo thumbnail, Name, Location, Last Watering, Health, Actions)
  - Buttons: [+ New], [Statistics], [Settings], [Export]
  - Status bar at bottom

**Sortie:** UI can display list (empty initially)

### Tâche 2.5: Frontend - Plant List Integration
- [ ] Create API client methods:
  - `get_plants(filters)` - fetch from backend
  - `search_plants(query)` - search
  - `create_plant(data)` - POST
  - `update_plant(id, data)` - PUT
  - `delete_plant(id)` - DELETE
  - `archive_plant(id)` - archive

- [ ] Connect main window to API:
  - Load plants on startup
  - Refresh after CRUD
  - Show toast notifications
  - Show loading indicator

**Sortie:** Plant list loads from backend ✅

### Tâche 2.6: Frontend - Plant Form (Create/Edit)
- [ ] Create `app/windows/plant_form.py`
  - Tabbed interface:
    - Tab 1: Basic info (name, scientific_name, family, subfamily, etc)
    - Tab 2: Characteristics (temp, humidity, light, soil, etc)
    - Tab 3: Care (watering freq, fertilizing, location, purchase info)
    - Tab 4: Tags & Advanced
  - Buttons: [Save] [Cancel]
  - Dropdowns pour lookups (location, purchase_place, etc)
  - Form validation

**Sortie:** Can create new plant via form

### Tâche 2.7: Frontend - Plant Detail Window
- [ ] Create `app/windows/plant_detail.py`
  - Display plant info (read-only or edit mode)
  - Photo gallery with thumbnails
  - Buttons: [Edit] [Archive] [Delete] [Close]
  - Show key info in grid

**Sortie:** Can view plant details

### Tâche 2.8: Testing Phase 2
- [ ] Manual test: Create plant via UI
- [ ] Manual test: Edit plant
- [ ] Manual test: Delete plant (check soft delete)
- [ ] Manual test: Archive/restore
- [ ] Backend unit tests pour PlantService
- [ ] Backend integration tests pour Plant routes

**Sortie:** Phase 2 fully working ✅

---

## 📅 PHASE 3: PHOTOS & HISTORIQUES (Week 4)

### Tâche 3.1: Backend - Photo Service
- [ ] Create `app/services/photo_service.py`
  - `upload_photo(plant_id, file)` - save + convert WebP
  - `set_main_photo(photo_id)` - mark as main
  - `delete_photo(photo_id)` - soft delete
  - `get_photos(plant_id)` - list
  - `get_photo_path(filename)` - resolve filesystem path

**Sortie:** Photo service fully functional

### Tâche 3.2: Backend - Photo Routes
- [ ] Create `app/routes/photos.py`
  ```
  POST   /api/plants/{id}/photos
  GET    /api/plants/{id}/photos
  PATCH  /api/plants/{id}/photos/{photo_id}
  DELETE /api/plants/{id}/photos/{photo_id}
  GET    /api/photos/{filename}  (serve image)
  ```

**Sortie:** Photo API complete

### Tâche 3.3: Frontend - Photo Upload
- [ ] Add to plant form: Photo upload section
  - File picker
  - Drag & drop support
  - Preview thumbnail
  - Set as main checkbox
  - Delete button

**Sortie:** Can upload photos from UI

### Tâche 3.4: Backend - History Models & Services
- [ ] Create `app/services/history_service.py`
  - `create_watering_history(plant_id, data)`
  - `create_fertilizing_history(plant_id, data)`
  - `create_repotting_history(plant_id, data)`
  - `create_disease_history(plant_id, data)`
  - `create_plant_note(plant_id, data)` (PlantHistory)
  - Similar: `get_*`, `update_*`, `delete_*`
  - `get_all_histories(plant_id)` - combined view

**Sortie:** History service complete

### Tâche 3.5: Backend - History Routes
- [ ] Create `app/routes/histories.py`
  ```
  GET    /api/plants/{id}/watering-history
  POST   /api/plants/{id}/watering-history
  PUT    /api/plants/{id}/watering-history/{hid}
  DELETE /api/plants/{id}/watering-history/{hid}
  
  (same for fertilizing, repotting, disease, notes)
  ```

**Sortie:** History API complete

### Tâche 3.6: Frontend - Plant Detail Histories Tab
- [ ] Add to plant detail window: Histories tabbed view
  - Tab: Watering History (table: Date, Amount, Notes + [+Add] [Edit] [Delete])
  - Tab: Fertilizing History
  - Tab: Repotting History
  - Tab: Disease History
  - Tab: Notes
  - Each with CRUD buttons

**Sortie:** Can view & manage all histories ✅

### Tâche 3.7: Testing Phase 3
- [ ] Test photo upload (WebP conversion)
- [ ] Test photo display
- [ ] Test history creation/edit/delete
- [ ] Verify relationships (photo → plant, history → plant)

**Sortie:** Phase 3 working ✅

---

## 📅 PHASE 4: SETTINGS & ADVANCED (Week 5)

### Tâche 4.1: Backend - Lookup Services
- [ ] Create `app/services/settings_service.py`
  - CRUD pour Location
  - CRUD pour PurchasePlace
  - CRUD pour WateringFrequency
  - CRUD pour LightRequirement
  - CRUD pour FertilizerType
  - CRUD pour Tag & TagCategory

**Sortie:** Settings service complete

### Tâche 4.2: Backend - Settings Routes
- [ ] Create `app/routes/settings.py`
  ```
  GET    /api/locations
  POST   /api/locations
  PUT    /api/locations/{id}
  DELETE /api/locations/{id}
  
  (same for purchase-places, watering-frequencies, light-requirements, 
   fertilizer-types, tags, tag-categories)
  ```

**Sortie:** Settings API complete

### Tâche 4.3: Frontend - Settings Window
- [ ] Create `app/windows/settings_window.py`
  - Tabbed interface:
    - Tab: Locations (table + [+Add] [Edit] [Delete])
    - Tab: Purchase Places
    - Tab: Watering Frequencies
    - Tab: Light Requirements
    - Tab: Fertilizer Types
    - Tab: Tags & Categories

**Sortie:** Can manage all settings

### Tâche 4.4: Backend - Search & Filters
- [ ] Update PlantService:
  - `search_plants(query, skip, limit)` - full-text search
  - `filter_plants(location_id, tag_ids, difficulty, type, skip, limit)` - advanced filters
  - `get_plants_to_water(days=0)` - plants watered X days ago
  - `get_plants_to_fertilize(days=0)` - plants fertilized X days ago

**Sortie:** Search & filter endpoints

### Tâche 4.5: Frontend - Advanced Search
- [ ] Update main window:
  - Improve search bar with suggestions
  - Add filter panel (collapsible)
  - Save filter presets (in settings)?
  - Show "Watering today" / "Fertilize today" badges

**Sortie:** Search & filtering works ✅

### Tâche 4.6: Backend - Statistics
- [ ] Create `app/services/stats_service.py`
  - `get_total_plants()` - count
  - `get_plants_by_location()` - grouped counts
  - `get_plants_by_tag()` - grouped counts
  - `get_health_distribution()` - enum counts
  - `get_difficulty_distribution()` - enum counts
  - `get_upcoming_waterings(days=7)` - list
  - `get_upcoming_fertilizing(days=7)` - list

**Sortie:** Stats service complete

### Tâche 4.7: Backend - Statistics Routes
- [ ] Create `app/routes/statistics.py`
  ```
  GET    /api/statistics
  GET    /api/statistics/plants-by-location
  GET    /api/statistics/plants-by-tag
  GET    /api/statistics/upcoming-waterings
  GET    /api/statistics/upcoming-fertilizing
  ```

**Sortie:** Stats API complete

### Tâche 4.8: Frontend - Statistics Window
- [ ] Create `app/windows/statistics_window.py`
  - KPI cards: Total, To water, To fertilize, Sick, Archived
  - Charts:
    - Bar chart: Plants by location (matplotlib)
    - Pie chart: Plants by tag
    - Pie chart: Health distribution
  - Table: Upcoming waterings (next 7 days)

**Sortie:** Statistics window displays all data ✅

---

## 📅 PHASE 5: EXPORT/IMPORT & POLISH (Week 6-7)

### Tâche 5.1: Backend - Backup Service
- [ ] Create `app/services/backup_service.py`
  - `export_data(include_photos=True)` - export to ZIP
  - `create_zip_archive(data, photos)` - ZIP generation
  - `calculate_checksum(data)` - SHA256
  - `save_backup_info(metadata)` - save export metadata
  - `get_exports_list()` - list existing exports
  - `delete_export(filename)` - delete export file

**Sortie:** Backup service complete

### Tâche 5.2: Backend - Import Service
- [ ] Create `app/services/import_service.py`
  - `validate_zip(file)` - check ZIP structure
  - `parse_backup_json(backup.json)` - extract data
  - `preview_import(file)` - dry-run, return counts
  - `import_data(file, mode='MERGE')` - import
    - FRESH: clear all, import new
    - MERGE: add new, skip existing
    - REPLACE: overwrite existing
  - `import_photos(zip_file)` - restore photos

**Sortie:** Import service complete

### Tâche 5.3: Backend - Export/Import Routes
- [ ] Create `app/routes/export_import.py`
  ```
  POST   /api/export                       - trigger export
  GET    /api/exports                      - list exports
  DELETE /api/exports/{filename}           - delete export
  GET    /api/exports/{filename}/download  - download ZIP
  
  POST   /api/import/preview               - dry-run
  POST   /api/import                       - do import
  GET    /api/import/status                - check progress
  ```

**Sortie:** Export/Import API complete

### Tâche 5.4: Frontend - Export Dialog
- [ ] Create `app/windows/export_dialog.py`
  - Checkbox: [Include photos]
  - Button: [Export now]
  - Section: Previous exports (list with [Download] [Delete])
  - Progress bar during export
  - Toast: "Export successful!"

**Sortie:** Can export data

### Tâche 5.5: Frontend - Import Dialog
- [ ] Create `app/windows/import_dialog.py`
  - File picker: Select ZIP file
  - Preview section: Shows counts (plants, photos, tags)
  - Dropdown: Import mode (FRESH / MERGE / REPLACE)
  - Warning message for FRESH/REPLACE modes
  - Button: [Import]
  - Progress bar
  - Toast: "Import complete!"

**Sortie:** Can import data ✅

### Tâche 5.6: Backend - Audit Logging
- [ ] Create `app/services/audit_service.py`
  - `log_action(user, action, entity_id, entity_type, details)` - log to DB
  - `get_audit_logs(skip, limit, filters)` - query logs
  - Automatically log all: CREATE, UPDATE, DELETE

- [ ] Create `app/middleware/audit_middleware.py`
  - Intercept all POST/PUT/DELETE
  - Auto-log changes

**Sortie:** Audit logging working

### Tâche 5.7: Frontend - Audit Log Viewer
- [ ] Create `app/windows/audit_window.py`
  - Table: Date, Action, Entity, Details
  - Filters: Date range, Action type
  - Button: [Export as CSV]

**Sortie:** Can view audit logs

### Tâche 5.8: UI Polish & Theming
- [ ] Add light/dark mode toggle (PySimpleGUI theme)
- [ ] Consistent icons (emoji or unicode)
- [ ] Better error messages (toasts, dialogs)
- [ ] Loading spinners
- [ ] Keyboard shortcuts (Ctrl+N = new, Ctrl+S = save, etc)
- [ ] Right-click context menus

**Sortie:** UI polished & professional

### Tâche 5.9: Testing & QA
- [ ] Full end-to-end testing:
  - Create plant → Upload photo → Add histories → Export → Delete → Import
  - Verify all data preserved
  - Check photo WebP conversion
  - Verify timestamps
- [ ] Edge cases:
  - Very large photos
  - Special characters in names
  - Circular relationships?
  - Concurrent operations
- [ ] Performance testing:
  - Large plant count (1000+)
  - Large export/import
  - UI responsiveness

**Sortie:** All bugs fixed ✅

### Tâche 5.10: Documentation & README
- [ ] Update `README.md`:
  - Features list
  - Screenshots
  - Installation instructions (dev + user)
  - Troubleshooting section
- [ ] Create `CHANGELOG.md` (v1.0 features)
- [ ] Create `ROADMAP.md` (future features)
- [ ] Add inline code comments
- [ ] API docs (Swagger auto-generated by FastAPI)

**Sortie:** Complete documentation ✅

---

## 📅 PHASE 6: DEPLOYMENT (Week 8)

### Tâche 6.1: PyInstaller Setup
- [ ] Create build script:
  ```bash
  pyinstaller --onefile \
    --add-data "data:data" \
    --hidden-import=fastapi \
    --hidden-import=uvicorn \
    ... main.py
  ```
- [ ] Test exe on clean Windows machine
- [ ] Create installer (NSIS)?

**Sortie:** Single EXE file ✅

### Tâche 6.2: GitHub Release
- [ ] Tag: v1.0.0
- [ ] Create release notes
- [ ] Upload exe + source as ZIP
- [ ] Create installation guide

**Sortie:** Project published ✅

---

## 📊 ESTIMATION RÉALISTE

| Phase | Durée | Priorité |
|-------|-------|----------|
| Phase 1 (Setup) | 3-4 jours | 🔴 CRITIQUE |
| Phase 2 (CRUD Plants) | 4-5 jours | 🔴 CRITIQUE |
| Phase 3 (Photos & Historiques) | 5-6 jours | 🔴 CRITIQUE |
| Phase 4 (Settings & Stats) | 4-5 jours | 🟡 IMPORTANT |
| Phase 5 (Export/Import & Polish) | 5-6 jours | 🟡 IMPORTANT |
| Phase 6 (Deployment) | 1-2 jours | 🟢 NICE |
| **TOTAL** | **5-8 semaines** | |

**Risques:**
- Complexité UI (PySimpleGUI apprentissage)
- Edge cases non identifiés
- Performance DB avec 1000+ plantes

---

## ✅ DÉFINITION DE "DONE"

Chaque phase est complete quand:
1. ✅ Tous les endpoints testés & working
2. ✅ UI fonctionnelle end-to-end
3. ✅ Pas de bugs critiques (P0/P1)
4. ✅ Code commenté
5. ✅ Tests unitaires (au moins 70% coverage)

---

**Status:** Plan prêt → Commencer Phase 1! 🚀

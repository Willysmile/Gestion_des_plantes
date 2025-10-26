% PHASE 4B - RECAP DÉTAILLÉ POINT PAR POINT
% Date: 25 Octobre 2025
% Branch: 2.05 (Frontend Phase 4B)

# PHASE 4B - FRONTEND RECAP COMPLET

## 🎯 OBJECTIF GLOBAL

Créer l'interface utilisateur pour les 31 endpoints Phase 4A:
- Settings management (6 lookup types)
- Plant search & filtering
- Dashboard avec KPIs

---

## 📋 TASK 4.3: SETTINGS WINDOW

### 🎨 UI Layout
```
┌─────────────────────────────────────────────────────────┐
│  🔧 SETTINGS - PLANT LOOKUPS                            │
├─────────────────────────────────────────────────────────┤
│  [Locations] [Places] [Watering] [Light] [Fert] [Tags] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TAB CONTENT (example: Locations)                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Locations List:                        [Scroll] │   │
│  │ ┌──────────────────────────────────────────────┐│   │
│  │ │ • Salon              (ID: 1)    [Edit][Del] ││   │
│  │ │ • Chambre            (ID: 2)    [Edit][Del] ││   │
│  │ │ • Balcon             (ID: 3)    [Edit][Del] ││   │
│  │ │ • Cuisine            (ID: 4)    [Edit][Del] ││   │
│  │ │ • Jardin             (ID: 5)    [Edit][Del] ││   │
│  │ └──────────────────────────────────────────────┘│   │
│  │                                                 │   │
│  │ [+ Add New Location]  [Close]                   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 📂 Fichier
```
frontend/app/windows/settings_window.py
```

### 🔧 Implémentation Details

#### 6 Tabs avec Pattern Identique
```python
Tab 1: Locations
  └─ API: /api/settings/locations
  └─ Fields: name
  └─ Actions: GET list, CREATE, UPDATE, DELETE

Tab 2: Purchase Places
  └─ API: /api/settings/purchase-places
  └─ Fields: name
  └─ Actions: GET list, CREATE, UPDATE, DELETE

Tab 3: Watering Frequencies
  └─ API: /api/settings/watering-frequencies
  └─ Fields: name, days (integer)
  └─ Actions: GET list, CREATE, UPDATE, DELETE

Tab 4: Light Requirements
  └─ API: /api/settings/light-requirements
  └─ Fields: name
  └─ Actions: GET list, CREATE, UPDATE, DELETE

Tab 5: Fertilizer Types
  └─ API: /api/settings/fertilizer-types
  └─ Fields: name
  └─ Actions: GET list, CREATE, UPDATE, DELETE

Tab 6: Tags
  └─ API: /api/settings/tags
  └─ Fields: name, category_id
  └─ Actions: CREATE, DELETE (read-only list)
```

#### Per-Tab Components
```
List View:
  • Column([
      MultilineText(height=10, disabled=True),  # List display
    ])
  • Auto-refresh from API
  • Show: "ID: 1 - Name"

Action Buttons:
  • [+ Add New]: Opens input dialog
  • [Edit]: Select item, opens edit dialog
  • [Delete]: Select item, confirm deletion

Input Dialogs:
  • Add dialog:    Ask for new name (+ days if watering)
  • Edit dialog:   Pre-fill with current values
  • Delete dialog: Confirm deletion
```

### 🔄 API Calls Pattern
```python
# Get all
async def get_all_locations():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:8000/api/settings/locations")
        return resp.json()

# Create
async def create_location(name):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://127.0.0.1:8000/api/settings/locations",
            json={"name": name}
        )
        return resp.json() if resp.status_code == 201 else None

# Update
async def update_location(location_id, name):
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"http://127.0.0.1:8000/api/settings/locations/{location_id}",
            json={"name": name}
        )
        return resp.json() if resp.status_code == 200 else None

# Delete
async def delete_location(location_id):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f"http://127.0.0.1:8000/api/settings/locations/{location_id}"
        )
        return resp.status_code == 204
```

### ✅ Checklist 4.3
- [ ] Créer fichier `settings_window.py`
- [ ] Implémenter tabbed layout avec PySimpleGUI
- [ ] Tab Locations: CRUD complet
- [ ] Tab Purchase Places: CRUD complet
- [ ] Tab Watering Frequencies: CRUD complet (avec field days)
- [ ] Tab Light Requirements: CRUD complet
- [ ] Tab Fertilizer Types: CRUD complet
- [ ] Tab Tags: Create + Delete (read-only list)
- [ ] Error handling (network, 422, 404, 500)
- [ ] Test manuel: CRUD opérationnel pour chaque tab

### ⏱️ Temps Estimé
**60-90 minutes** (~300 lignes de code)

---

## 📋 TASK 4.6: MAIN WINDOW SEARCH UI

### 🎨 UI Layout - Ajouts à main_window.py
```
AVANT (current):
┌─────────────────────────────────┐
│ [List Plants]                   │
├─────────────────────────────────┤
│ • Plant 1                       │
│ • Plant 2                       │
│ ...                             │
└─────────────────────────────────┘

APRÈS (with search):
┌──────────────────────────────────────────────────────────┐
│ [Search] [Query________________] [🔍] [Advanced ▼]       │
├──────────────────────────────────────────────────────────┤
│ ▼ FILTERS (collapsible)                                  │
│   Location: [Dropdown]  Difficulty: [Dropdown]           │
│   Health: [Dropdown]    [Apply] [Reset]                  │
├──────────────────────────────────────────────────────────┤
│ 🌱 8 plants | ⏳ 3 to-water | 🧪 1 to-fertilize          │
├──────────────────────────────────────────────────────────┤
│ [List Plants - Search Results or Full List]              │
│ • Plant 1                                                │
│ • Plant 2 (highlighted if to-water)                      │
│ ...                                                      │
└──────────────────────────────────────────────────────────┘
```

### 📂 Fichier
```
frontend/app/windows/main_window.py (MODIFIER - pas créer nouveau)
```

### 🔧 Implémentation Details

#### 1. Search Bar (Top)
```python
search_layout = [
    [
        sg.Text("Search: "),
        sg.InputText(key="-SEARCH_INPUT-", size=(30, 1)),
        sg.Button("🔍 Search", key="-SEARCH_BTN-"),
        sg.Button("Advanced ▼", key="-ADVANCED_BTN-"),
    ]
]
```

#### 2. Filter Panel (Collapsible)
```python
filter_layout = [
    [
        sg.Column([
            [sg.Text("Location:"), sg.Combo(locations, key="-FILTER_LOC-", size=(15, 1))],
            [sg.Text("Difficulty:"), sg.Combo(difficulties, key="-FILTER_DIFF-", size=(15, 1))],
            [sg.Text("Health:"), sg.Combo(health_statuses, key="-FILTER_HEALTH-", size=(15, 1))],
            [sg.Button("Apply"), sg.Button("Reset")],
        ], key="-FILTER_COLUMN-", visible=False)
    ]
]
```

#### 3. Quick Badges (Top-Right)
```python
badges_layout = [
    [
        sg.Text("🌱 Badges:", font=("Arial", 10, "bold")),
        sg.Text("8 plants", key="-BADGE_TOTAL-", size=(10, 1)),
        sg.Text("⏳ 3 to-water", key="-BADGE_WATER-", size=(12, 1)),
        sg.Text("🧪 1 to-fertilize", key="-BADGE_FERT-", size=(15, 1)),
    ]
]
```

#### 4. API Calls for Search
```python
# Search
async def search_plants(query):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"http://127.0.0.1:8000/api/plants/search",
            params={"q": query}
        )
        return resp.json()

# Filter
async def filter_plants(location_id=None, difficulty=None, health_status=None):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"http://127.0.0.1:8000/api/plants/filter",
            params={
                "location_id": location_id,
                "difficulty": difficulty,
                "health_status": health_status,
            }
        )
        return resp.json()

# Quick badge counts
async def get_to_water_count():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "http://127.0.0.1:8000/api/plants/to-water",
            params={"days_ago": 0}
        )
        return len(resp.json())

async def get_to_fertilize_count():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "http://127.0.0.1:8000/api/plants/to-fertilize",
            params={"days_ago": 0}
        )
        return len(resp.json())
```

#### 5. Event Handling
```python
while True:
    event, values = window.read()
    
    if event == "-SEARCH_BTN-":
        query = values["-SEARCH_INPUT-"]
        results = await search_plants(query)
        update_plant_list(results)
    
    elif event == "-ADVANCED_BTN-":
        toggle_filter_visibility()
    
    elif event == "Apply":
        loc = values["-FILTER_LOC-"]
        diff = values["-FILTER_DIFF-"]
        health = values["-FILTER_HEALTH-"]
        results = await filter_plants(loc, diff, health)
        update_plant_list(results)
    
    elif event == "Reset":
        clear_filters()
        update_plant_list(all_plants)
    
    # Update badges periodically
    update_badges()
```

### ✅ Checklist 4.6
- [ ] Ajouter search bar top
- [ ] Implémenter search button + call API
- [ ] Ajouter filter panel (collapsible)
- [ ] Implémenter filter buttons + call API
- [ ] Ajouter quick badges (3 badges)
- [ ] Implémenter badge refresh (to-water, to-fertilize count)
- [ ] Intégrer avec liste plants existante
- [ ] Test: Rechercher, filtrer, voir badges update

### ⏱️ Temps Estimé
**60-90 minutes** (~150 lignes de code ajouté)

---

## 📋 TASK 4.9: DASHBOARD WINDOW

### 🎨 UI Layout
```
┌─────────────────────────────────────────────────┐
│  📊 PLANT DASHBOARD                             │
├─────────────────────────────────────────────────┤
│                                                 │
│  KPI Cards (7 total):                           │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐        │
│  │ Total   │  │ Active  │  │ Archived │        │
│  │ 8       │  │ 8       │  │ 0        │        │
│  └─────────┘  └─────────┘  └──────────┘        │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │Excellent │  │  Good    │  │   Poor   │      │
│  │ 0        │  │ 0        │  │ 0        │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                 │
│  ┌──────────┐                                   │
│  │  Photos  │                                   │
│  │ 1        │                                   │
│  └──────────┘                                   │
│                                                 │
│  ───────────────────────────────────────────    │
│                                                 │
│  Upcoming Waterings (Next 7 days)               │
│  ┌────────────────────────────────────────────┐ │
│  │ ID │ Plant   │ Last  │ Days  │ [Water]    │ │
│  ├────────────────────────────────────────────┤ │
│  │ 1  │ Rose    │ 5d    │ 5     │ [Water]    │ │
│  │ 2  │ Cactus  │ -     │ -     │ [Water]    │ │
│  └────────────────────────────────────────────┘ │
│                                                 │
│  Upcoming Fertilizing (Next 7 days)             │
│  ┌────────────────────────────────────────────┐ │
│  │ ID │ Plant   │ Last  │ Days  │ [Fert]     │ │
│  └────────────────────────────────────────────┘ │
│                                                 │
│  [Refresh] [Export] [Close]                     │
└─────────────────────────────────────────────────┘
```

### 📂 Fichier
```
frontend/app/windows/dashboard_window.py
```

### 🔧 Implémentation Details

#### 1. KPI Cards Layout
```python
kpi_layout = [
    [
        sg.Column([[sg.Text("Total", font=("Arial", 12, "bold")), sg.Text("8", key="-KPI_TOTAL-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="lightgray"),
        sg.Column([[sg.Text("Active", font=("Arial", 12, "bold")), sg.Text("8", key="-KPI_ACTIVE-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="lightgreen"),
        sg.Column([[sg.Text("Archived", font=("Arial", 12, "bold")), sg.Text("0", key="-KPI_ARCHIVED-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="lightcoral"),
    ],
    [
        sg.Column([[sg.Text("Excellent", font=("Arial", 12, "bold")), sg.Text("0", key="-KPI_EXCELLENT-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="gold"),
        sg.Column([[sg.Text("Good", font=("Arial", 12, "bold")), sg.Text("0", key="-KPI_GOOD-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="lightblue"),
        sg.Column([[sg.Text("Poor", font=("Arial", 12, "bold")), sg.Text("0", key="-KPI_POOR-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="lightyellow"),
    ],
    [
        sg.Column([[sg.Text("Photos", font=("Arial", 12, "bold")), sg.Text("1", key="-KPI_PHOTOS-", font=("Arial", 20, "bold"))]], pad=(10, 10), background_color="lightcyan"),
    ],
]
```

#### 2. Waterings Table
```python
watering_layout = [
    [sg.Text("Upcoming Waterings (Next 7 days)", font=("Arial", 12, "bold"))],
    [sg.Table(
        values=[],
        headings=["ID", "Plant", "Last Watered", "Days", "Action"],
        max_col_width=20,
        auto_size_columns=False,
        num_rows=5,
        key="-WATERING_TABLE-",
    )],
]
```

#### 3. Fertilizing Table
```python
fertilizing_layout = [
    [sg.Text("Upcoming Fertilizing (Next 7 days)", font=("Arial", 12, "bold"))],
    [sg.Table(
        values=[],
        headings=["ID", "Plant", "Last Fert", "Days", "Action"],
        max_col_width=20,
        auto_size_columns=False,
        num_rows=5,
        key="-FERTILIZING_TABLE-",
    )],
]
```

#### 4. API Calls
```python
# Get KPIs
async def get_dashboard_stats():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:8000/api/statistics/dashboard")
        return resp.json()

# Get waterings
async def get_upcoming_waterings():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:8000/api/statistics/upcoming-waterings?days=7")
        return resp.json()

# Get fertilizing
async def get_upcoming_fertilizing():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:8000/api/statistics/upcoming-fertilizing?days=7")
        return resp.json()
```

#### 5. Data Formatting
```python
# Format watering data for table
def format_watering_data(waterings):
    table_data = []
    for w in waterings:
        table_data.append([
            w["id"],
            w["name"],
            w.get("last_watered", "Never") or "Never",
            w.get("days_since", "-") or "-",
            "Water"  # Action button
        ])
    return table_data

# Same for fertilizing...
```

#### 6. Refresh Functionality
```python
while True:
    event, values = window.read(timeout=100)
    
    if event == "-REFRESH_BTN-" or first_load:
        # Load all data
        stats = await get_dashboard_stats()
        waterings = await get_upcoming_waterings()
        fertilizing = await get_upcoming_fertilizing()
        
        # Update KPIs
        window["-KPI_TOTAL-"].update(stats["total_plants"])
        window["-KPI_ACTIVE-"].update(stats["active_plants"])
        # ... etc
        
        # Update tables
        window["-WATERING_TABLE-"].update(format_watering_data(waterings))
        window["-FERTILIZING_TABLE-"].update(format_watering_data(fertilizing))
```

### ✅ Checklist 4.9
- [ ] Créer fichier `dashboard_window.py`
- [ ] Implémenter 7 KPI cards
- [ ] Appeler GET /statistics/dashboard
- [ ] Remplir les KPI avec données
- [ ] Implémenter table "Upcoming Waterings"
- [ ] Appeler GET /statistics/upcoming-waterings
- [ ] Remplir table waterings
- [ ] Implémenter table "Upcoming Fertilizing"
- [ ] Appeler GET /statistics/upcoming-fertilizing
- [ ] Remplir table fertilizing
- [ ] Bouton Refresh → reload toutes les données
- [ ] Bouton Export (bonus)
- [ ] Test: Vérifier affichage données correctes

### ⏱️ Temps Estimé
**45-60 minutes** (~280 lignes de code)

---

## 📋 TASK 4.11: INTEGRATION TESTS

### 📂 Fichier
```
test_phase4_integration.py
```

### 🔧 Test Scope

#### 1. Settings Window Tests
```python
# Test create location
test_create_location():
  - Open Settings Window
  - Click "+ Add Location"
  - Enter "Test Location"
  - Verify appears in list
  - Verify API was called

# Test edit location
test_edit_location():
  - Select location from list
  - Click Edit
  - Change name
  - Verify updated in list
  - Verify API was called

# Test delete location
test_delete_location():
  - Select location
  - Click Delete
  - Confirm deletion
  - Verify removed from list

# Test all 6 tabs (repeat above for each)
test_purchase_places_crud()
test_watering_frequencies_crud()
test_light_requirements_crud()
test_fertilizer_types_crud()
test_tags_crud()
```

#### 2. Search UI Tests
```python
test_search_plants():
  - Open Main Window
  - Enter search query
  - Click Search
  - Verify results displayed
  - Verify correct plants shown

test_filter_plants():
  - Click Filter button
  - Select difficulty, location, health
  - Click Apply
  - Verify filtered results

test_badges_update():
  - Open Main Window
  - Verify badges show counts
  - Add watering record
  - Verify badge updates
```

#### 3. Dashboard Tests
```python
test_kpi_display():
  - Open Dashboard Window
  - Verify all 7 KPIs displayed
  - Verify values are integers > 0

test_watering_table():
  - Verify table loads
  - Verify correct columns
  - Verify data displayed

test_fertilizing_table():
  - Verify table loads
  - Verify correct columns
  - Verify data displayed

test_refresh_button():
  - Click Refresh
  - Verify all data reloaded
  - Verify no errors
```

#### 4. End-to-End Flow
```python
test_e2e_settings_to_search():
  - Create new location in Settings
  - Go to Main Window
  - Filter by new location
  - Verify results filtered

test_e2e_full_workflow():
  - Open Settings
  - Create test data
  - Go to Main Window
  - Search/filter using test data
  - Open Dashboard
  - Verify KPIs updated
  - Verify no errors throughout
```

### 🔍 Test Framework
```python
# Use pytest + async
import pytest
import httpx

@pytest.mark.asyncio
async def test_settings_window_create():
    # Test implementation
    pass

# Run with:
# pytest test_phase4_integration.py -v
```

### ✅ Checklist 4.11
- [ ] Créer test_phase4_integration.py
- [ ] Écrire tests Settings Window (6 tabs)
- [ ] Écrire tests Search UI (search, filter, badges)
- [ ] Écrire tests Dashboard (KPIs, tables)
- [ ] Écrire tests end-to-end
- [ ] Run all tests
- [ ] Get 100% pass rate
- [ ] No hanging/timeout issues

### ⏱️ Temps Estimé
**60-120 minutes** (~400 lignes de code test)

---

## 📊 RÉSUMÉ PHASE 4B

| Task | Component | Time | Files | Status |
|------|-----------|------|-------|--------|
| 4.3 | Settings Window | 60-90 min | settings_window.py | ⏳ TODO |
| 4.6 | Main Window Search | 60-90 min | main_window.py (modify) | ⏳ TODO |
| 4.9 | Dashboard Window | 45-60 min | dashboard_window.py | ⏳ TODO |
| 4.11 | Integration Tests | 60-120 min | test_phase4_integration.py | ⏳ TODO |
| **TOTAL** | **Phase 4B** | **4-6 heures** | **4 files** | **⏳ READY** |

---

## 🔄 DEPENDENCIES

### Requirements
```
PySimpleGUI==4.60.5  (already installed or install with: pip install PySimpleGUI)
httpx               (async HTTP client)
pytest              (testing)
pytest-asyncio      (async test support)
```

### Backend Requirements
```
Backend server running on http://127.0.0.1:8000
Database with seed data loaded
All 31 endpoints accessible
```

---

## 🚀 START CHECKLIST

- [ ] Backend server running: `python -m uvicorn app.main:app --reload`
- [ ] Verify endpoints working: `http://127.0.0.1:8000/docs`
- [ ] Branch 2.05 created and active
- [ ] Ready to start 4.3 (Settings Window)

---

## 📝 NOTES

### Pattern Consistency
All tabs in 4.3 follow same CRUD pattern - reusable code structure

### Async Pattern
All API calls use `async with httpx.AsyncClient()` for non-blocking UI

### Error Handling
- Network timeouts: Show error dialog
- 422 (validation): Show validation error message
- 404 (not found): Show "Not found" message
- 500 (server error): Show generic error + log

### Testing Strategy
- Manual testing: Each feature as you build it
- Unit tests: Per-window functionality
- Integration tests: Full workflows

---

**Ready to start? Begin with Task 4.3 - Settings Window! 🎯**

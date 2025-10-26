# 🌿 GESTION DES PLANTES - How to Run

## Quick Start

### 1. Start the Backend (if not already running)
```bash
cd backend
source venv/bin/activate
python app/main.py
```

Server will be available at: `http://127.0.0.1:8000`

### 2. Launch the Frontend Application
```bash
cd /home/willysmile/Documents/Gestion_des_plantes
./backend/venv/bin/python run_app.py
```

## What You Get

### 🏠 Main Window
- **Search** plants by name
- **Advanced Filters** (location, difficulty, health status)
- **Quick Stats** badges (total plants, need watering, need fertilizing)
- **Plant List** with all plants in database

### 📊 Dashboard Window
- **7 KPI Cards**:
  - Total plants
  - Active plants
  - Archived plants
  - Health status (excellent, good, poor)
  - Total photos
- **Upcoming Waterings Table** (next 7 days)
- **Upcoming Fertilizing Table** (next 7 days)

### ⚙️ Settings Window
- **6 Management Tabs**:
  1. Locations - Add/Edit/Delete plant locations
  2. Purchase Places - Manage where plants were bought
  3. Watering Frequencies - Set watering schedules
  4. Light Requirements - Define light needs
  5. Fertilizer Types - Manage fertilizer types
  6. Tags - Create and manage plant tags

## Architecture

```
Frontend (PySimpleGUI 5.0.10)
├── MainWindow          (Search + Filter + Plant List)
├── SettingsWindow      (6 CRUD tabs for lookups)
└── DashboardWindow     (KPIs + Task tables)
        ↓
    httpx (async HTTP)
        ↓
Backend (FastAPI 0.104.1)
├── API Endpoints (31 total)
├── SQLAlchemy ORM
└── SQLite Database
```

## Requirements

- Python 3.11+
- PySimpleGUI 5.0.10 (Official version from PySimpleGUI.net)
- httpx (async HTTP client)
- FastAPI + SQLAlchemy (backend)

## Status

✅ **Phase 4B - COMPLETE & VALIDATED**

All 3 windows are:
- ✅ Fully implemented
- ✅ API-integrated
- ✅ Live tested
- ✅ Production ready

## Troubleshooting

### Windows don't launch?
```bash
# Reinstall PySimpleGUI from official server
pip uninstall PySimpleGUI
pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
```

### Backend connection error?
```bash
# Make sure backend is running
curl http://127.0.0.1:8000/api/plants
# Should return plant data
```

### Port 8000 already in use?
```bash
# Find and kill the process using port 8000
lsof -i :8000
kill -9 <PID>
```

## License

This project is part of "Gestion des Plantes" - a plant management application.

---

**Last Updated:** October 25, 2025  
**Status:** ✅ PRODUCTION READY

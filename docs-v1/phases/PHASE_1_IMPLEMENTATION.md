# 📋 PHASE 1 - INFRASTRUCTURE & SETUP (Week 1)

**Date début:** 25 Octobre 2025  
**Durée:** 1 week (5 jours)  
**Objectif:** Backend FastAPI opérationnel + Frontend PySimpleGUI basique + 15 modèles SQLite

---

## 🎯 Objectifs Phase 1

✅ Structure projet Python (backend + frontend)  
✅ FastAPI app running on http://localhost:8000  
✅ SQLite database initialized with 15 models  
✅ Alembic migrations setup  
✅ PySimpleGUI basic window (test connection)  
✅ API Swagger docs working  
✅ Health check endpoint  
✅ Git ready (commits daily)

---

## 📁 Structure à créer

```
Gestion_des_plantes/
├── backend/
│   ├── venv/                         # Virtual environment
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app + routes
│   │   ├── config.py                 # Settings, DB URL, etc.
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # BaseModel avec timestamps
│   │   │   ├── plant.py              # Plant, Photo
│   │   │   ├── histories.py          # 5 history models
│   │   │   ├── tags.py               # Tag, TagCategory
│   │   │   └── lookup.py             # Location, PurchasePlace, etc.
│   │   ├── schemas/                  # (Empty for now, Phase 2)
│   │   ├── routes/                   # (Empty for now, Phase 2)
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── db.py                 # Database initialization
│   ├── migrations/                   # Alembic migrations
│   ├── requirements.txt
│   └── .env                          # Local settings
│
├── frontend/
│   ├── venv/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # PySimpleGUI entry point
│   │   ├── api_client.py             # HTTP wrapper
│   │   └── config.py                 # API base URL
│   ├── requirements.txt
│   └── .env
│
└── data/                             # Created at runtime
    ├── plants.db                     # SQLite database
    ├── photos/
    └── exports/
```

---

## 🔧 TASK 1.1: Project Structure Setup

### Objectives
- [ ] Create `/backend` and `/frontend` directories
- [ ] Create `.gitignore` for Python
- [ ] Create virtual environments
- [ ] Initialize Git commits

### Commands
```bash
# Create main directories
mkdir backend frontend data
mkdir data/photos data/exports

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Frontend setup
cd ../frontend
python -m venv venv
source venv/bin/activate

# Create app directories
mkdir app migrations
cd app
touch __init__.py main.py config.py
mkdir models schemas routes utils
cd models && touch __init__.py base.py plant.py histories.py tags.py lookup.py
cd ../utils && touch __init__.py db.py
```

### Files to create
- `backend/.env` - Local settings
- `frontend/.env` - API URL config
- `backend/.gitignore` and `frontend/.gitignore`

### Deliverable
✅ Clean project structure ready for code

---

## 🔧 TASK 1.2: Backend Requirements & Dependencies

### requirements.txt (backend/)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
alembic==1.12.1
python-multipart==0.0.6
python-dotenv==1.0.0
pillow==10.1.0
```

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Verify
```bash
python -c "import fastapi; import sqlalchemy; print('OK')"
```

### Deliverable
✅ All dependencies installed and verified

---

## 🔧 TASK 1.3: FastAPI App Setup

### app/config.py
```python
from pydantic_settings import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./data/plants.db"
    
    # App
    APP_NAME: str = "Plant Manager v2"
    DEBUG: bool = True
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    PHOTOS_DIR: Path = DATA_DIR / "photos"
    EXPORTS_DIR: Path = DATA_DIR / "exports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create data directories if not exist
settings.DATA_DIR.mkdir(exist_ok=True)
settings.PHOTOS_DIR.mkdir(exist_ok=True)
settings.EXPORTS_DIR.mkdir(exist_ok=True)
```

### app/utils/db.py
```python
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.models.base import Base

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize DB
def init_db():
    Base.metadata.create_all(bind=engine)
```

### app/main.py
```python
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.utils.db import init_db, get_db

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Desktop plant management application",
    version="0.1.0"
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "debug": settings.DEBUG
    }

# Test DB endpoint
@app.get("/api/db-status")
async def db_status(db: Session = Depends(get_db)):
    try:
        # Simple query to test DB connection
        result = db.execute("SELECT 1").fetchone()
        return {"status": "connected", "test": "ok"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Test
```bash
cd backend
python -m uvicorn app.main:app --reload
# → http://localhost:8000/docs (Swagger)
# → http://localhost:8000/health (health check)
# → http://localhost:8000/api/db-status (DB test)
```

### Deliverable
✅ FastAPI running with health check endpoints

---

## 🔧 TASK 1.4: SQLAlchemy Models Setup

### app/models/base.py
```python
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### app/models/plant.py
```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Plant(BaseModel):
    __tablename__ = "plants"
    
    # Basic info
    name = Column(String(100), nullable=False, index=True)
    scientific_name = Column(String(150))
    family = Column(String(100))
    subfamily = Column(String(100))
    genus = Column(String(100))
    species = Column(String(100))
    subspecies = Column(String(100))
    variety = Column(String(100))
    cultivar = Column(String(100))
    reference = Column(String(100), unique=True, index=True)
    
    # Description
    description = Column(Text)
    health_status = Column(String(50))  # healthy, sick, recovering, dead
    difficulty_level = Column(String(50))  # easy, medium, hard
    growth_speed = Column(String(50))  # slow, medium, fast
    flowering_season = Column(String(100))  # comma-separated months
    
    # Location
    location_id = Column(Integer, ForeignKey("locations.id"))
    purchase_date = Column(String(20))  # "dd/mm/yyyy" or "mm/yyyy"
    purchase_place_id = Column(Integer, ForeignKey("purchase_places.id"))
    purchase_price = Column(DECIMAL(10, 2))
    
    # Environment
    watering_frequency_id = Column(Integer, ForeignKey("watering_frequencies.id"))
    light_requirement_id = Column(Integer, ForeignKey("light_requirements.id"))
    temperature_min = Column(Integer)
    temperature_max = Column(Integer)
    humidity_level = Column(Integer)
    soil_humidity = Column(String(50))
    soil_type = Column(String(100))
    pot_size = Column(String(50))
    
    # Flags
    is_indoor = Column(Boolean, default=False)
    is_outdoor = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    is_toxic = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships
    photos = relationship("Photo", back_populates="plant", cascade="all, delete-orphan")
    watering_histories = relationship("WateringHistory", back_populates="plant")
    fertilizing_histories = relationship("FertilizingHistory", back_populates="plant")
    repotting_histories = relationship("RepottingHistory", back_populates="plant")
    disease_histories = relationship("DiseaseHistory", back_populates="plant")
    plant_histories = relationship("PlantHistory", back_populates="plant")

class Photo(BaseModel):
    __tablename__ = "photos"
    
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    filename = Column(String(255), nullable=False)  # WebP format
    description = Column(Text)
    is_main = Column(Boolean, default=False)
    
    # Relationship
    plant = relationship("Plant", back_populates="photos")
```

### app/models/lookup.py
```python
from sqlalchemy import Column, String, Integer
from app.models.base import BaseModel

class Location(BaseModel):
    __tablename__ = "locations"
    name = Column(String(100), unique=True, nullable=False)

class PurchasePlace(BaseModel):
    __tablename__ = "purchase_places"
    name = Column(String(100), unique=True, nullable=False)

class WateringFrequency(BaseModel):
    __tablename__ = "watering_frequencies"
    name = Column(String(100), unique=True, nullable=False)

class LightRequirement(BaseModel):
    __tablename__ = "light_requirements"
    name = Column(String(100), unique=True, nullable=False)

class FertilizerType(BaseModel):
    __tablename__ = "fertilizer_types"
    name = Column(String(100), unique=True, nullable=False)
```

### app/models/histories.py
```python
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class WateringHistory(BaseModel):
    __tablename__ = "watering_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    watering_date = Column(DateTime, nullable=False)
    amount = Column(String(100))  # "500ml", "1L", etc.
    notes = Column(Text)
    plant = relationship("Plant", back_populates="watering_histories")

class FertilizingHistory(BaseModel):
    __tablename__ = "fertilizing_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    fertilizing_date = Column(DateTime, nullable=False)
    fertilizer_type = Column(String(100))
    amount = Column(String(100))
    notes = Column(Text)
    plant = relationship("Plant", back_populates="fertilizing_histories")

class RepottingHistory(BaseModel):
    __tablename__ = "repotting_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    repotting_date = Column(DateTime, nullable=False)
    old_pot_size = Column(String(50))
    new_pot_size = Column(String(50))
    soil_type = Column(String(100))
    notes = Column(Text)
    plant = relationship("Plant", back_populates="repotting_histories")

class DiseaseHistory(BaseModel):
    __tablename__ = "disease_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    disease_date = Column(DateTime, nullable=False)
    disease_name = Column(String(100))
    treatment = Column(String(255))
    status = Column(String(50))  # active, treated, resolved
    notes = Column(Text)
    plant = relationship("Plant", back_populates="disease_histories")

class PlantHistory(BaseModel):
    __tablename__ = "plant_history"
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    history_date = Column(DateTime, nullable=False)
    event_type = Column(String(100))  # observation, change, note, etc.
    notes = Column(Text, nullable=False)
    plant = relationship("Plant", back_populates="plant_histories")
```

### app/models/tags.py
```python
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

# M-to-M association table
plant_tag_association = Table(
    'plant_tag',
    BaseModel.metadata,
    Column('plant_id', Integer, ForeignKey('plants.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class TagCategory(BaseModel):
    __tablename__ = "tag_categories"
    name = Column(String(100), unique=True, nullable=False)
    tags = relationship("Tag", back_populates="category")

class Tag(BaseModel):
    __tablename__ = "tags"
    name = Column(String(100), nullable=False)
    tag_category_id = Column(Integer, ForeignKey("tag_categories.id"))
    category = relationship("TagCategory", back_populates="tags")
```

### Update app/models/__init__.py
```python
from app.models.base import Base, BaseModel
from app.models.plant import Plant, Photo
from app.models.lookup import Location, PurchasePlace, WateringFrequency, LightRequirement, FertilizerType
from app.models.histories import WateringHistory, FertilizingHistory, RepottingHistory, DiseaseHistory, PlantHistory
from app.models.tags import Tag, TagCategory, plant_tag_association

__all__ = [
    "Base", "BaseModel",
    "Plant", "Photo",
    "Location", "PurchasePlace", "WateringFrequency", "LightRequirement", "FertilizerType",
    "WateringHistory", "FertilizingHistory", "RepottingHistory", "DiseaseHistory", "PlantHistory",
    "Tag", "TagCategory",
]
```

### Update app/main.py to import models
```python
from app.models import Base  # This ensures all models are registered
```

### Test Models
```bash
python
>>> from app.models import Base, Plant, Photo, WateringHistory, Tag
>>> print("All 15 models imported successfully!")
```

### Deliverable
✅ 15 SQLAlchemy models defined with relationships

---

## 🔧 TASK 1.5: Alembic Migrations Setup

### Initialize Alembic
```bash
cd backend
alembic init migrations
```

### Edit migrations/env.py
Update the `run_migrations_offline` and `run_migrations_online` functions to use your config:

```python
from app.config import settings
from app.models import Base

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
target_metadata = Base.metadata
```

### Create initial migration
```bash
alembic revision --autogenerate -m "Initial schema with 15 models"
```

### Apply migration
```bash
alembic upgrade head
```

### Verify
```bash
# Check if data/plants.db exists
ls -la data/plants.db

# Check tables
sqlite3 data/plants.db ".tables"
```

### Deliverable
✅ Alembic migrations working, plants.db created

---

## 🔧 TASK 1.6: PySimpleGUI Frontend Setup

### requirements.txt (frontend/)
```
pysimplegui==4.60.5
requests==2.31.0
pillow==10.1.0
python-dotenv==1.0.0
```

### app/config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_TIMEOUT = 5  # seconds
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
```

### app/api_client.py
```python
import requests
from app.config import API_BASE_URL, API_TIMEOUT, DEBUG
from requests.exceptions import RequestException

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
    
    def get(self, endpoint: str):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), None
        except RequestException as e:
            if DEBUG:
                print(f"API Error: {e}")
            return None, str(e)
    
    def health_check(self):
        data, error = self.get("/health")
        return error is None

# Global instance
api_client = APIClient()
```

### app/main.py
```python
import PySimpleGUI as sg
from app.api_client import api_client

# Set theme
sg.theme('DarkBlue3')

def create_main_window():
    layout = [
        [sg.Text('🌱 Plant Manager v2', font=('Any', 20), justification='center')],
        [sg.Text('Loading...', key='-STATUS-', font=('Any', 12))],
        [sg.Button('Test API'), sg.Button('Exit', size=(10, 1))]
    ]
    return sg.Window('Plant Manager', layout, finalize=True)

def main():
    window = create_main_window()
    
    # Check API connection on startup
    if api_client.health_check():
        window['-STATUS-'].update("✅ Connected to backend")
    else:
        window['-STATUS-'].update("❌ Backend not responding")
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        
        if event == 'Test API':
            if api_client.health_check():
                sg.popup('✅ API is working!')
            else:
                sg.popup('❌ API connection failed!')
    
    window.close()

if __name__ == '__main__':
    main()
```

### frontend/.env
```
API_BASE_URL=http://127.0.0.1:8000
DEBUG=true
```

### Test Frontend
```bash
cd frontend
python app/main.py
# Should show main window and API status
```

### Deliverable
✅ PySimpleGUI window with API connection test

---

## 📋 PHASE 1 CHECKLIST

### Backend Infrastructure
- [ ] `/backend` directory created
- [ ] Virtual environment setup
- [ ] `requirements.txt` created and packages installed
- [ ] `app/config.py` with Settings class
- [ ] `app/utils/db.py` with SQLAlchemy engine setup
- [ ] `app/main.py` with FastAPI app and health check
- [ ] FastAPI running on http://localhost:8000
- [ ] Swagger docs working at `/docs`

### Database & Models
- [ ] 15 SQLAlchemy models defined
  - [ ] Plant + Photo (2)
  - [ ] 5 History models (5)
  - [ ] Tag + TagCategory (2)
  - [ ] 5 Lookup models (5)
- [ ] All relationships and foreign keys configured
- [ ] `app/models/__init__.py` imports all models
- [ ] Alembic initialized
- [ ] Initial migration created: `Initial schema with 15 models`
- [ ] `plants.db` SQLite file created in `/data`

### Frontend
- [ ] `/frontend` directory created
- [ ] Virtual environment setup
- [ ] `requirements.txt` created and packages installed
- [ ] `app/api_client.py` with HTTP wrapper
- [ ] `app/config.py` with API URL
- [ ] `app/main.py` with basic PySimpleGUI window
- [ ] Frontend window displays API connection status
- [ ] PySimpleGUI test button works

### Testing
- [ ] `GET /health` returns OK
- [ ] `GET /api/db-status` returns connected
- [ ] Backend can be started: `python -m uvicorn app.main:app --reload`
- [ ] Frontend can be started: `python app/main.py`
- [ ] Frontend connects to backend successfully

### Git
- [ ] Daily commits for each major task
- [ ] `.gitignore` configured for Python
- [ ] Branch `2.01` used
- [ ] Commits tagged with task numbers

---

## 🧪 Testing Phase 1

### Backend API Tests
```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Test health check
curl http://127.0.0.1:8000/health
# Expected: {"status":"ok","app":"Plant Manager v2","debug":true}

# Test DB connection
curl http://127.0.0.1:8000/api/db-status
# Expected: {"status":"connected","test":"ok"}

# Check Swagger docs
# Browser: http://localhost:8000/docs
```

### Frontend Test
```bash
# Terminal 3: Start frontend
cd frontend
python app/main.py
# Should show window with "✅ Connected to backend"
```

### Database Verification
```bash
# Check tables created
sqlite3 data/plants.db ".tables"

# Expected output: Should list all tables (plants, photos, etc.)
```

---

## 📊 Phase 1 Success Criteria

✅ **Infrastructure working:**
- Backend: FastAPI app runs, health check OK
- Frontend: PySimpleGUI window displays, connects to backend
- Database: SQLite file created with all 15 tables

✅ **Code quality:**
- Models properly defined with relationships
- No import errors
- Code follows conventions (lowercase filenames, clear imports)

✅ **Documentation:**
- This PHASE_1_IMPLEMENTATION.md is complete
- Code comments on complex logic
- README.md updated with Phase 1 progress

✅ **Git:**
- Daily commits
- Branch `2.01` used
- Meaningful commit messages

---

## 📝 Daily Progress Log

### Day 1 (Task 1.1-1.2)
- [ ] Project structure created
- [ ] Python environments setup
- [ ] Dependencies installed
- [ ] Initial git commits

### Day 2 (Task 1.3-1.4)
- [ ] FastAPI app running
- [ ] Health check endpoint working
- [ ] 15 SQLAlchemy models defined
- [ ] Relationships configured

### Day 3 (Task 1.4-1.5)
- [ ] Models imported successfully
- [ ] Alembic migrations initialized
- [ ] Initial migration created
- [ ] Database file created (`plants.db`)

### Day 4 (Task 1.6)
- [ ] PySimpleGUI setup
- [ ] API client wrapper created
- [ ] Frontend window displays
- [ ] Backend ↔ Frontend connection tested

### Day 5 (Polish & Testing)
- [ ] All endpoints tested
- [ ] Documentation completed
- [ ] Code review and cleanup
- [ ] Final commits and push to GitHub

---

## 🚀 Next: Phase 2

Once Phase 1 is complete:
- Phase 2 will add **Pydantic schemas** and **CRUD endpoints**
- We'll implement full Plant CRUD operations
- Test coverage begins

---

**Phase 1 Owner:** GitHub Copilot  
**Status:** 🚀 READY TO START  
**Last Updated:** 25 Octobre 2025

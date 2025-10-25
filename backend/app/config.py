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

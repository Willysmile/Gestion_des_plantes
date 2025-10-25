from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.utils.db import init_db, get_db
from app.models import Base
from app.routes.plants import router as plants_router
from app.routes.photos import router as photos_router, files_router
from app.scripts.seed_lookups import seed_all

# Initialize database
init_db()

# Seed lookup tables at startup
db = next(get_db())
try:
    seed_all(db)
finally:
    db.close()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Desktop plant management application",
    version="0.1.0"
)

# Include routers
app.include_router(plants_router)
app.include_router(photos_router)
app.include_router(files_router)

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

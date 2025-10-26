"""
Endpoints FastAPI pour les statistiques et le dashboard
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import get_db
from app.services.stats_service import StatsService

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("/dashboard", response_model=dict)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Récupère les 7 KPI du dashboard
    Retourne: {
        total_plants, active_plants, archived_plants,
        health_excellent, health_good, health_poor,
        total_photos
    }
    """
    return StatsService.get_dashboard_stats(db)


@router.get("/upcoming-waterings", response_model=List[dict])
async def get_upcoming_waterings(
    days: int = Query(7, ge=0, le=365, description="Nombre de jours à vérifier"),
    db: Session = Depends(get_db),
):
    """
    Plantes à arroser dans N jours
    Retourne les plantes jamais arrosées + celles arrosées il y a N jours ou plus
    """
    return StatsService.get_upcoming_waterings(db, days)


@router.get("/upcoming-fertilizing", response_model=List[dict])
async def get_upcoming_fertilizing(
    days: int = Query(7, ge=0, le=365, description="Nombre de jours à vérifier"),
    db: Session = Depends(get_db),
):
    """
    Plantes à fertiliser dans N jours
    Retourne les plantes jamais fertilisées + celles fertilisées il y a N jours ou plus
    """
    return StatsService.get_upcoming_fertilizing(db, days)

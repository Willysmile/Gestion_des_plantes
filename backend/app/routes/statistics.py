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


@router.get("/activity", response_model=dict)
async def get_activity(
    days: int = Query(30, ge=0, le=365, description="Nombre de jours à vérifier"),
    db: Session = Depends(get_db),
):
    """
    Activité des derniers N jours (arrosages et fertilisations)
    Retourne: {
        "watering_count": int,
        "fertilizing_count": int,
        "daily_activity": [
            {"date": "2025-11-06", "watering": 5, "fertilizing": 2},
            ...
        ]
    }
    """
    return StatsService.get_activity(db, days)


@router.get("/calendar", response_model=dict)
async def get_calendar(
    year: int = Query(2025),
    month: int = Query(11),
    db: Session = Depends(get_db),
):
    """
    Récupère les événements du calendrier pour un mois donné
    Retourne: {
        "events": [
            {"date": "2025-11-15", "type": "watering", "plant_id": 5, "plant_name": "Monstera", "count": 1},
            ...
        ],
        "summary": {
            "year": 2025,
            "month": 11,
            "total_days": 30,
            "active_days": 12,
            "water_events": 25,
            "fertilize_events": 8,
            "total_events": 33
        }
    }
    """
    return StatsService.get_calendar_events(db, year, month)


@router.get("/alerts", response_model=dict)
async def get_alerts(db: Session = Depends(get_db)):
    """
    Récupère les alertes avancées par sévérité
    Retourne: {
        "alerts": [
            {
                "id": "water_5_critical",
                "type": "watering",
                "plant_id": 5,
                "plant_name": "Monstera",
                "message": "Monstera - URGENT: Non arrosée depuis 20 jours",
                "severity": "critical",
                "action": "water",
                "date": "2025-10-20"
            },
            ...
        ],
        "by_severity": {
            "critical": [...],
            "high": [...],
            "medium": [...],
            "low": [...]
        },
        "summary": {
            "critical_count": 3,
            "high_count": 5,
            "medium_count": 10,
            "low_count": 8,
            "total_count": 26
        }
    }
    """
    return StatsService.get_advanced_alerts(db)


@router.get("/notifications", response_model=dict)
async def get_upcoming_notifications(
    days: int = Query(7, ge=1, le=365, description="Nombre de jours de prédictions"),
    db: Session = Depends(get_db),
):
    """
    Récupère les notifications prédictives basées sur les calendriers de prédictions
    Retourne les arrosages et fertilisations prédites pour les N prochains jours
    
    Retourne: {
        "waterings": [
            {
                "plant_id": 4,
                "plant_name": "Sansevieria",
                "predicted_date": "2025-11-12",
                "days_until": 2,
                "last_event_date": "2025-11-09"
            },
            ...
        ],
        "fertilizings": [
            {
                "plant_id": 5,
                "plant_name": "Monstera",
                "predicted_date": "2025-11-15",
                "days_until": 5,
                "last_event_date": "2025-11-08"
            },
            ...
        ],
        "summary": {
            "count_watering": 19,
            "count_fertilizing": 9,
            "days_ahead": 7,
            "total_count": 28,
            "most_urgent": "Arroser Sansevieria dans 2 jours"
        }
    }
    """
    return StatsService.get_upcoming_predictions(db, days)


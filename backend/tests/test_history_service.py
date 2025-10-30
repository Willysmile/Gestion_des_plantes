from datetime import date

import pytest

from app.services.history_service import HistoryService
from app.schemas.history_schema import (
    WateringHistoryCreate, WateringHistoryUpdate,
    FertilizingHistoryCreate, FertilizingHistoryUpdate,
    RepottingHistoryCreate, RepottingHistoryUpdate,
    DiseaseHistoryCreate, DiseaseHistoryUpdate,
    PlantHistoryCreate, PlantHistoryUpdate,
)
from app.models.plant import Plant


@pytest.mark.usefixtures("db")
def test_history_service_watering_flow(db):
    p = Plant(name="H1")
    db.add(p)
    db.commit()
    pid = p.id

    w = HistoryService.create_watering(db, pid, WateringHistoryCreate(date=date.today(), amount_ml=20))
    assert w.id

    got = HistoryService.get_watering(db, pid, w.id)
    assert got is not None

    HistoryService.update_watering(db, pid, w.id, WateringHistoryUpdate(notes="x"))
    assert HistoryService.get_watering(db, pid, w.id).notes == "x"

    assert HistoryService.delete_watering(db, pid, w.id) is True


@pytest.mark.usefixtures("db")
def test_history_service_other_types(db):
    p = Plant(name="H2")
    db.add(p)
    db.commit()
    pid = p.id

    # Fertilizing
    fh = HistoryService.create_fertilizing(db, pid, FertilizingHistoryCreate(date=date.today(), amount="1 unité"))
    assert fh.id
    HistoryService.update_fertilizing(db, pid, fh.id, FertilizingHistoryUpdate(notes="n"))
    assert HistoryService.delete_fertilizing(db, pid, fh.id) is True

    # Repotting
    rh = HistoryService.create_repotting(db, pid, RepottingHistoryCreate(date=date.today(), pot_size_before=10, pot_size_after=12))
    assert rh.id
    HistoryService.update_repotting(db, pid, rh.id, RepottingHistoryUpdate(notes="n"))
    assert HistoryService.delete_repotting(db, pid, rh.id) is True

    # Disease
    dh = HistoryService.create_disease(db, pid, DiseaseHistoryCreate(date=date.today(), recovered=False))
    assert dh.id
    HistoryService.update_disease(db, pid, dh.id, DiseaseHistoryUpdate(recovered=True))
    assert HistoryService.delete_disease(db, pid, dh.id) is True

    # Plant notes
    ph = HistoryService.create_plant_note(db, pid, PlantHistoryCreate(date=date.today(), note="n"))
    assert ph.id
    HistoryService.update_plant_note(db, pid, ph.id, PlantHistoryUpdate(note="m"))
    assert HistoryService.delete_plant_note(db, pid, ph.id) is True

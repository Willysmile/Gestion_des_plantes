import pytest

from app.services.lookup_service import (
    UnitService, DiseaseTypeService, TreatmentTypeService,
    PlantHealthStatusService, FertilizerTypeService
)
from app.schemas.lookup_schema import (
    UnitCreate, DiseaseTypeCreate, TreatmentTypeCreate,
    PlantHealthStatusCreate, FertilizerTypeCreate
)
from app.schemas.lookup_schema import (
    UnitUpdate, DiseaseTypeUpdate, TreatmentTypeUpdate,
    PlantHealthStatusUpdate, FertilizerTypeUpdate
)


@pytest.mark.usefixtures("db")
def test_unit_service_crud(db):
    # create
    unit = UnitService.create(db, UnitCreate(name="bâton", symbol="bt", description=None))
    assert unit.id is not None

    # get_all
    all_units = UnitService.get_all(db)
    assert any(u.id == unit.id for u in all_units)

    # get_by_id
    got = UnitService.get_by_id(db, unit.id)
    assert got is not None

    # update
    upd = UnitCreate(name="bâtons", symbol="bt")
    # UnitService.update expects a UnitUpdate-like object; reuse create for dict shape
    from app.schemas.lookup_schema import UnitUpdate
    updated = UnitService.update(db, unit.id, UnitUpdate(name="bâtons"))
    assert updated.name == "bâtons"

    # delete
    deleted = UnitService.delete(db, unit.id)
    assert deleted is not None


@pytest.mark.usefixtures("db")
def test_other_lookup_services_crud(db):
    # DiseaseType
    dt = DiseaseTypeService.create(db, DiseaseTypeCreate(name="Pythium", description="fungus"))
    assert dt.id
    assert DiseaseTypeService.get_by_id(db, dt.id).name == "Pythium"
    DiseaseTypeService.update(db, dt.id, DiseaseTypeUpdate(description="root rot"))
    assert "root" in (DiseaseTypeService.get_by_id(db, dt.id).description or "")
    DiseaseTypeService.delete(db, dt.id)

    # TreatmentType
    tt = TreatmentTypeService.create(db, TreatmentTypeCreate(name="Spray", description="apply"))
    assert tt.id
    TreatmentTypeService.update(db, tt.id, TreatmentTypeUpdate(description="spray now"))
    TreatmentTypeService.delete(db, tt.id)

    # PlantHealthStatus
    ph = PlantHealthStatusService.create(db, PlantHealthStatusCreate(name="good", description="ok"))
    assert ph.id
    PlantHealthStatusService.update(db, ph.id, PlantHealthStatusUpdate(description="fine"))
    PlantHealthStatusService.delete(db, ph.id)

    # FertilizerType
    ft = FertilizerTypeService.create(db, FertilizerTypeCreate(name="EngraisX", unit="unité", description="ok"))
    assert ft.id
    FertilizerTypeService.update(db, ft.id, FertilizerTypeUpdate(description="better"))
    FertilizerTypeService.delete(db, ft.id)

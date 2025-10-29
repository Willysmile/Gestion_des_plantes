from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import get_db
from app.services.lookup_service import (
    UnitService, DiseaseTypeService, TreatmentTypeService, PlantHealthStatusService, FertilizerTypeService
)
from app.schemas.lookup_schema import (
    UnitCreate, UnitUpdate, UnitResponse,
    DiseaseTypeCreate, DiseaseTypeUpdate, DiseaseTypeResponse,
    TreatmentTypeCreate, TreatmentTypeUpdate, TreatmentTypeResponse,
    PlantHealthStatusCreate, PlantHealthStatusUpdate, PlantHealthStatusResponse,
    FertilizerTypeCreate, FertilizerTypeUpdate, FertilizerTypeResponse
)

router = APIRouter(prefix="/api/settings", tags=["settings"])


# Unit routes
@router.get("/units", response_model=list[UnitResponse])
async def get_units(db: Session = Depends(get_db)):
    return UnitService.get_all(db)


@router.get("/units/{unit_id}", response_model=UnitResponse)
async def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = UnitService.get_by_id(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.post("/units", response_model=UnitResponse)
async def create_unit(unit: UnitCreate, db: Session = Depends(get_db)):
    return UnitService.create(db, unit)


@router.put("/units/{unit_id}", response_model=UnitResponse)
async def update_unit(unit_id: int, unit: UnitUpdate, db: Session = Depends(get_db)):
    db_unit = UnitService.update(db, unit_id, unit)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db_unit


@router.delete("/units/{unit_id}")
async def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    db_unit = UnitService.delete(db, unit_id)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"detail": "Unit deleted successfully"}


# Disease Type routes
@router.get("/disease-types", response_model=list[DiseaseTypeResponse])
async def get_disease_types(db: Session = Depends(get_db)):
    return DiseaseTypeService.get_all(db)


@router.get("/disease-types/{disease_type_id}", response_model=DiseaseTypeResponse)
async def get_disease_type(disease_type_id: int, db: Session = Depends(get_db)):
    disease_type = DiseaseTypeService.get_by_id(db, disease_type_id)
    if not disease_type:
        raise HTTPException(status_code=404, detail="Disease type not found")
    return disease_type


@router.post("/disease-types", response_model=DiseaseTypeResponse)
async def create_disease_type(disease_type: DiseaseTypeCreate, db: Session = Depends(get_db)):
    return DiseaseTypeService.create(db, disease_type)


@router.put("/disease-types/{disease_type_id}", response_model=DiseaseTypeResponse)
async def update_disease_type(disease_type_id: int, disease_type: DiseaseTypeUpdate, db: Session = Depends(get_db)):
    disease_type_db = DiseaseTypeService.update(db, disease_type_id, disease_type)
    if not disease_type_db:
        raise HTTPException(status_code=404, detail="Disease type not found")
    return disease_type_db


@router.delete("/disease-types/{disease_type_id}")
async def delete_disease_type(disease_type_id: int, db: Session = Depends(get_db)):
    disease_type = DiseaseTypeService.delete(db, disease_type_id)
    if not disease_type:
        raise HTTPException(status_code=404, detail="Disease type not found")
    return {"message": "Disease type deleted successfully"}


# Treatment Type routes
@router.get("/treatment-types", response_model=list[TreatmentTypeResponse])
async def get_treatment_types(db: Session = Depends(get_db)):
    return TreatmentTypeService.get_all(db)


@router.get("/treatment-types/{treatment_type_id}", response_model=TreatmentTypeResponse)
async def get_treatment_type(treatment_type_id: int, db: Session = Depends(get_db)):
    treatment_type = TreatmentTypeService.get_by_id(db, treatment_type_id)
    if not treatment_type:
        raise HTTPException(status_code=404, detail="Treatment type not found")
    return treatment_type


@router.post("/treatment-types", response_model=TreatmentTypeResponse)
async def create_treatment_type(treatment_type: TreatmentTypeCreate, db: Session = Depends(get_db)):
    return TreatmentTypeService.create(db, treatment_type)


@router.put("/treatment-types/{treatment_type_id}", response_model=TreatmentTypeResponse)
async def update_treatment_type(treatment_type_id: int, treatment_type: TreatmentTypeUpdate, db: Session = Depends(get_db)):
    treatment_type_db = TreatmentTypeService.update(db, treatment_type_id, treatment_type)
    if not treatment_type_db:
        raise HTTPException(status_code=404, detail="Treatment type not found")
    return treatment_type_db


@router.delete("/treatment-types/{treatment_type_id}")
async def delete_treatment_type(treatment_type_id: int, db: Session = Depends(get_db)):
    treatment_type = TreatmentTypeService.delete(db, treatment_type_id)
    if not treatment_type:
        raise HTTPException(status_code=404, detail="Treatment type not found")
    return {"message": "Treatment type deleted successfully"}


# Plant Health Status routes
@router.get("/plant-health-statuses", response_model=list[PlantHealthStatusResponse])
async def get_plant_health_statuses(db: Session = Depends(get_db)):
    return PlantHealthStatusService.get_all(db)


@router.get("/plant-health-statuses/{status_id}", response_model=PlantHealthStatusResponse)
async def get_plant_health_status(status_id: int, db: Session = Depends(get_db)):
    status = PlantHealthStatusService.get_by_id(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Plant health status not found")
    return status


@router.post("/plant-health-statuses", response_model=PlantHealthStatusResponse)
async def create_plant_health_status(status: PlantHealthStatusCreate, db: Session = Depends(get_db)):
    return PlantHealthStatusService.create(db, status)


@router.put("/plant-health-statuses/{status_id}", response_model=PlantHealthStatusResponse)
async def update_plant_health_status(status_id: int, status: PlantHealthStatusUpdate, db: Session = Depends(get_db)):
    status_db = PlantHealthStatusService.update(db, status_id, status)
    if not status_db:
        raise HTTPException(status_code=404, detail="Plant health status not found")
    return status_db


@router.delete("/plant-health-statuses/{status_id}")
async def delete_plant_health_status(status_id: int, db: Session = Depends(get_db)):
    status = PlantHealthStatusService.delete(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Plant health status not found")
    return {"message": "Plant health status deleted successfully"}


# Fertilizer Type routes (already exists, but added for completeness)
@router.get("/fertilizer-types", response_model=list[FertilizerTypeResponse])
async def get_fertilizer_types(db: Session = Depends(get_db)):
    return FertilizerTypeService.get_all(db)


@router.get("/fertilizer-types/{fertilizer_type_id}", response_model=FertilizerTypeResponse)
async def get_fertilizer_type(fertilizer_type_id: int, db: Session = Depends(get_db)):
    fertilizer_type = FertilizerTypeService.get_by_id(db, fertilizer_type_id)
    if not fertilizer_type:
        raise HTTPException(status_code=404, detail="Fertilizer type not found")
    return fertilizer_type


@router.post("/fertilizer-types", response_model=FertilizerTypeResponse)
async def create_fertilizer_type(fertilizer_type: FertilizerTypeCreate, db: Session = Depends(get_db)):
    return FertilizerTypeService.create(db, fertilizer_type)


@router.put("/fertilizer-types/{fertilizer_type_id}", response_model=FertilizerTypeResponse)
async def update_fertilizer_type(fertilizer_type_id: int, fertilizer_type: FertilizerTypeUpdate, db: Session = Depends(get_db)):
    fertilizer_type_db = FertilizerTypeService.update(db, fertilizer_type_id, fertilizer_type)
    if not fertilizer_type_db:
        raise HTTPException(status_code=404, detail="Fertilizer type not found")
    return fertilizer_type_db


@router.delete("/fertilizer-types/{fertilizer_type_id}")
async def delete_fertilizer_type(fertilizer_type_id: int, db: Session = Depends(get_db)):
    fertilizer_type = FertilizerTypeService.delete(db, fertilizer_type_id)
    if not fertilizer_type:
        raise HTTPException(status_code=404, detail="Fertilizer type not found")
    return {"message": "Fertilizer type deleted successfully"}

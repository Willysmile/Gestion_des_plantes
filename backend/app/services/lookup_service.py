from sqlalchemy.orm import Session
from app.models.lookup import Unit, DiseaseType, TreatmentType, PlantHealthStatus, FertilizerType
from app.schemas.lookup_schema import (
    UnitCreate, UnitUpdate, UnitResponse,
    DiseaseTypeCreate, DiseaseTypeUpdate, DiseaseTypeResponse,
    TreatmentTypeCreate, TreatmentTypeUpdate, TreatmentTypeResponse,
    PlantHealthStatusCreate, PlantHealthStatusUpdate, PlantHealthStatusResponse,
    FertilizerTypeCreate, FertilizerTypeUpdate, FertilizerTypeResponse
)


class UnitService:
    @staticmethod
    def get_all(db: Session):
        return db.query(Unit).all()

    @staticmethod
    def get_by_id(db: Session, unit_id: int):
        return db.query(Unit).filter(Unit.id == unit_id).first()

    @staticmethod
    def create(db: Session, unit: UnitCreate):
        db_unit = Unit(**unit.dict())
        db.add(db_unit)
        db.commit()
        db.refresh(db_unit)
        return db_unit

    @staticmethod
    def update(db: Session, unit_id: int, unit: UnitUpdate):
        db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
        if db_unit:
            for key, value in unit.dict(exclude_unset=True).items():
                setattr(db_unit, key, value)
            db.commit()
            db.refresh(db_unit)
        return db_unit

    @staticmethod
    def delete(db: Session, unit_id: int):
        db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
        if db_unit:
            db.delete(db_unit)
            db.commit()
        return db_unit


class DiseaseTypeService:
    @staticmethod
    def get_all(db: Session):
        return db.query(DiseaseType).all()

    @staticmethod
    def get_by_id(db: Session, disease_type_id: int):
        return db.query(DiseaseType).filter(DiseaseType.id == disease_type_id).first()

    @staticmethod
    def create(db: Session, disease_type: DiseaseTypeCreate):
        db_disease_type = DiseaseType(**disease_type.dict())
        db.add(db_disease_type)
        db.commit()
        db.refresh(db_disease_type)
        return db_disease_type

    @staticmethod
    def update(db: Session, disease_type_id: int, disease_type: DiseaseTypeUpdate):
        db_disease_type = db.query(DiseaseType).filter(DiseaseType.id == disease_type_id).first()
        if db_disease_type:
            update_data = disease_type.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_disease_type, key, value)
            db.commit()
            db.refresh(db_disease_type)
        return db_disease_type

    @staticmethod
    def delete(db: Session, disease_type_id: int):
        db_disease_type = db.query(DiseaseType).filter(DiseaseType.id == disease_type_id).first()
        if db_disease_type:
            db.delete(db_disease_type)
            db.commit()
        return db_disease_type


class TreatmentTypeService:
    @staticmethod
    def get_all(db: Session):
        return db.query(TreatmentType).all()

    @staticmethod
    def get_by_id(db: Session, treatment_type_id: int):
        return db.query(TreatmentType).filter(TreatmentType.id == treatment_type_id).first()

    @staticmethod
    def create(db: Session, treatment_type: TreatmentTypeCreate):
        db_treatment_type = TreatmentType(**treatment_type.dict())
        db.add(db_treatment_type)
        db.commit()
        db.refresh(db_treatment_type)
        return db_treatment_type

    @staticmethod
    def update(db: Session, treatment_type_id: int, treatment_type: TreatmentTypeUpdate):
        db_treatment_type = db.query(TreatmentType).filter(TreatmentType.id == treatment_type_id).first()
        if db_treatment_type:
            update_data = treatment_type.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_treatment_type, key, value)
            db.commit()
            db.refresh(db_treatment_type)
        return db_treatment_type

    @staticmethod
    def delete(db: Session, treatment_type_id: int):
        db_treatment_type = db.query(TreatmentType).filter(TreatmentType.id == treatment_type_id).first()
        if db_treatment_type:
            db.delete(db_treatment_type)
            db.commit()
        return db_treatment_type


class PlantHealthStatusService:
    @staticmethod
    def get_all(db: Session):
        return db.query(PlantHealthStatus).all()

    @staticmethod
    def get_by_id(db: Session, status_id: int):
        return db.query(PlantHealthStatus).filter(PlantHealthStatus.id == status_id).first()

    @staticmethod
    def create(db: Session, status: PlantHealthStatusCreate):
        db_status = PlantHealthStatus(**status.dict())
        db.add(db_status)
        db.commit()
        db.refresh(db_status)
        return db_status

    @staticmethod
    def update(db: Session, status_id: int, status: PlantHealthStatusUpdate):
        db_status = db.query(PlantHealthStatus).filter(PlantHealthStatus.id == status_id).first()
        if db_status:
            update_data = status.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_status, key, value)
            db.commit()
            db.refresh(db_status)
        return db_status

    @staticmethod
    def delete(db: Session, status_id: int):
        db_status = db.query(PlantHealthStatus).filter(PlantHealthStatus.id == status_id).first()
        if db_status:
            db.delete(db_status)
            db.commit()
        return db_status


class FertilizerTypeService:
    @staticmethod
    def get_all(db: Session):
        return db.query(FertilizerType).all()

    @staticmethod
    def get_by_id(db: Session, fertilizer_type_id: int):
        return db.query(FertilizerType).filter(FertilizerType.id == fertilizer_type_id).first()

    @staticmethod
    def create(db: Session, fertilizer_type: FertilizerTypeCreate):
        db_fertilizer_type = FertilizerType(**fertilizer_type.dict())
        db.add(db_fertilizer_type)
        db.commit()
        db.refresh(db_fertilizer_type)
        return db_fertilizer_type

    @staticmethod
    def update(db: Session, fertilizer_type_id: int, fertilizer_type: FertilizerTypeUpdate):
        db_fertilizer_type = db.query(FertilizerType).filter(FertilizerType.id == fertilizer_type_id).first()
        if db_fertilizer_type:
            update_data = fertilizer_type.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_fertilizer_type, key, value)
            db.commit()
            db.refresh(db_fertilizer_type)
        return db_fertilizer_type

    @staticmethod
    def delete(db: Session, fertilizer_type_id: int):
        db_fertilizer_type = db.query(FertilizerType).filter(FertilizerType.id == fertilizer_type_id).first()
        if db_fertilizer_type:
            db.delete(db_fertilizer_type)
            db.commit()
        return db_fertilizer_type

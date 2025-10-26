"""
Unit tests for Plant model and business logic
"""

import pytest
from app.models.plant import Plant
from app.schemas.plant_schema import PlantCreate, PlantUpdate
from app.services.plant_service import PlantService


class TestPlantModel:
    """Tests for Plant model"""
    
    def test_plant_creation(self, db):
        """Test creating a plant"""
        plant = Plant(
            name="Monstera Deliciosa",
            genus="Monstera",
            species="deliciosa",
            family="Araceae"
        )
        db.add(plant)
        db.commit()
        db.refresh(plant)
        
        assert plant.id is not None
        assert plant.name == "Monstera Deliciosa"
        assert plant.scientific_name == "Monstera deliciosa"  # Auto-generated
    
    def test_plant_scientific_name_auto_generation(self, db):
        """Test scientific name auto-generation"""
        plant = Plant(
            name="Philodendron",
            genus="Philodendron",
            species="philodendron",
            family="Araceae"
        )
        db.add(plant)
        db.commit()
        
        assert plant.scientific_name == "Philodendron philodendron"
    
    def test_plant_without_scientific_name(self, db):
        """Test plant without genus/species"""
        plant = Plant(name="Unknown Plant")
        db.add(plant)
        db.commit()
        
        assert plant.scientific_name is None


class TestPlantService:
    """Tests for PlantService business logic"""
    
    def test_generate_reference_basic(self, db):
        """Test reference generation"""
        ref = PlantService.generate_reference(db, "Araceae")
        assert ref == "ARACE-001"  # 5 letters from "Araceae"
    
    def test_generate_reference_sequential(self, db):
        """Test sequential reference generation"""
        # Create first plant with reference
        plant1 = Plant(
            name="Plant 1",
            family="Araceae",
            reference="ARACE-001"  # Correct prefix: 5 letters
        )
        db.add(plant1)
        db.commit()
        
        # Generate next reference
        ref2 = PlantService.generate_reference(db, "Araceae")
        assert ref2 == "ARACE-002"
    
    def test_generate_reference_different_families(self, db):
        """Test references for different families"""
        plant1 = Plant(name="Plant 1", family="Araceae", reference="ARACE-001")
        plant2 = Plant(name="Plant 2", family="Orchidaceae", reference="ORCHI-001")
        
        db.add(plant1)
        db.add(plant2)
        db.commit()
        
        ref1 = PlantService.generate_reference(db, "Araceae")
        ref2 = PlantService.generate_reference(db, "Orchidaceae")
        
        assert ref1 == "ARACE-002"
        assert ref2 == "ORCHI-002"
    
    def test_generate_reference_invalid_family(self, db):
        """Test reference generation with invalid family"""
        with pytest.raises(ValueError):
            PlantService.generate_reference(db, "")
    
    def test_create_plant(self, db):
        """Test creating plant via PlantService"""
        plant_data = PlantCreate(
            name="Monstera",
            family="Araceae",
            genus="Monstera",
            species="deliciosa"
        )
        
        plant = PlantService.create(db, plant_data)
        db.refresh(plant)
        
        assert plant.id is not None
        assert plant.name == "Monstera"
        assert plant.scientific_name == "Monstera deliciosa"
        assert plant.reference.startswith("ARACE-")  # 5 letters from Araceae
    
    def test_get_all_plants(self, db):
        """Test getting all plants"""
        plant1 = Plant(name="Plant 1")
        plant2 = Plant(name="Plant 2")
        
        db.add(plant1)
        db.add(plant2)
        db.commit()
        
        plants = PlantService.get_all(db)
        assert len(plants) == 2
    
    def test_get_plant_by_id(self, db):
        """Test getting plant by ID"""
        plant = Plant(name="Test Plant")
        db.add(plant)
        db.commit()
        
        retrieved = PlantService.get_by_id(db, plant.id)
        assert retrieved.id == plant.id
        assert retrieved.name == "Test Plant"


class TestPlantValidation:
    """Tests for PlantCreate schema validation"""
    
    def test_valid_plant_create(self):
        """Test valid plant creation data"""
        data = PlantCreate(
            name="Monstera",
            temperature_min=15,
            temperature_max=25,
            humidity_level=60
        )
        assert data.name == "Monstera"
    
    def test_temperature_validation(self):
        """Test temperature min/max validation"""
        with pytest.raises(ValueError):
            PlantCreate(
                name="Plant",
                temperature_min=25,
                temperature_max=15  # Invalid: min > max
            )
    
    def test_humidity_validation(self):
        """Test humidity range validation"""
        with pytest.raises(ValueError):
            PlantCreate(
                name="Plant",
                humidity_level=150  # Invalid: > 100
            )
    
    def test_price_validation(self):
        """Test price validation"""
        with pytest.raises(ValueError):
            PlantCreate(
                name="Plant",
                purchase_price=-10  # Invalid: negative
            )

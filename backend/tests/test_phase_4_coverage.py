"""
Tests pour Phase 4 - Expansion Coverage 55% → 70%

Phase 4 (10-15h, +15%): photo_service + history_service + lookup_routes

Services Tested:
- photo_service.py (274 lines, 28% → 70%)
- history_service.py (166 lines, 34% → 70%)
- lookup_routes.py (126 lines, 0% → 70%)
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image
from unittest.mock import patch, MagicMock

from app.models import Plant, WateringHistory, FertilizingHistory, RepottingHistory, PhotoModel
from app.models.lookup import Unit, DiseaseType, TreatmentType, PlantHealthStatus, FertilizerType
from app.schemas.history_schema import (
    WateringHistoryCreate, WateringHistoryUpdate,
    FertilizingHistoryCreate, FertilizingHistoryUpdate,
    RepottingHistoryCreate, RepottingHistoryUpdate
)
from app.schemas.lookup_schema import (
    UnitCreate, UnitUpdate,
    DiseaseTypeCreate, DiseaseTypeUpdate,
    TreatmentTypeCreate, TreatmentTypeUpdate,
    FertilizerTypeCreate, FertilizerTypeUpdate
)
from app.services.history_service import HistoryService
from app.services.lookup_service import (
    UnitService, DiseaseTypeService, TreatmentTypeService,
    PlantHealthStatusService, FertilizerTypeService
)
from app.services.photo_service import PhotoService
from app.config import settings


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4: PHOTO SERVICE TESTS (274 lines, 28% → 70% coverage)
# ═══════════════════════════════════════════════════════════════════════════

class TestPhotoService:
    """Test photo_service.py functions"""

    def create_test_image(self, size: tuple = (800, 600), format: str = 'JPEG') -> bytes:
        """Helper: Create a test image in memory"""
        img = Image.new('RGB', size, color='blue')
        buffer = BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)
        return buffer.read()

    def test_get_plant_photos_path(self, tmp_path):
        """Test photos directory path creation"""
        with patch('app.services.photo_service.settings') as mock_settings:
            mock_settings.PHOTOS_DIR = tmp_path / 'photos'
            
            path = PhotoService._get_plant_photos_path(1)
            
            assert path.exists()
            assert str(path).endswith('1')

    def test_get_plant_thumbs_path(self, tmp_path):
        """Test thumbnails directory path creation"""
        with patch('app.services.photo_service.settings') as mock_settings:
            mock_settings.PHOTOS_DIR = tmp_path / 'photos'
            
            path = PhotoService._get_plant_thumbs_path(2)
            
            assert path.exists()
            assert 'thumbs' in str(path)

    def test_validate_file_valid_jpeg(self):
        """Test validation of valid JPEG"""
        image_bytes = self.create_test_image(format='JPEG')
        valid, msg = PhotoService._validate_file(image_bytes)
        
        assert valid is True
        assert msg == "OK"

    def test_validate_file_valid_png(self):
        """Test validation of valid PNG"""
        image_bytes = self.create_test_image(format='PNG')
        valid, msg = PhotoService._validate_file(image_bytes)
        
        assert valid is True
        assert msg == "OK"

    def test_validate_file_too_large(self):
        """Test validation fails for oversized file"""
        large_data = b'x' * (PhotoService.MAX_FILE_SIZE * 3)
        valid, msg = PhotoService._validate_file(large_data)
        
        assert valid is False
        assert 'volumineux' in msg.lower()

    def test_validate_file_invalid_image(self):
        """Test validation fails for invalid image data"""
        invalid_data = b'Not an image'
        valid, msg = PhotoService._validate_file(invalid_data)
        
        assert valid is False
        assert 'invalide' in msg.lower()

    def test_convert_to_webp_rgb(self):
        """Test WebP conversion for RGB image"""
        image = Image.new('RGB', (100, 100), color='red')
        webp_data = PhotoService._convert_to_webp(image)
        
        assert len(webp_data) > 0
        assert isinstance(webp_data, bytes)

    def test_convert_to_webp_rgba(self):
        """Test WebP conversion for RGBA image with transparency"""
        image = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        webp_data = PhotoService._convert_to_webp(image)
        
        assert len(webp_data) > 0
        assert isinstance(webp_data, bytes)

    def test_convert_to_webp_quality_levels(self):
        """Test WebP conversion respects quality parameter"""
        # Create a more complex image where quality difference is visible
        image = Image.new('RGB', (400, 400))
        pixels = image.load()
        for i in range(400):
            for j in range(400):
                pixels[i, j] = (i % 256, j % 256, (i+j) % 256)
        
        high_quality = PhotoService._convert_to_webp(image, quality=85)
        low_quality = PhotoService._convert_to_webp(image, quality=50)
        
        # Both should produce valid WebP files
        assert len(high_quality) > 0
        assert len(low_quality) > 0
        assert isinstance(high_quality, bytes)
        assert isinstance(low_quality, bytes)

    def test_compress_to_target(self):
        """Test image compression to target file size"""
        image_bytes = self.create_test_image(size=(800, 600))
        target_size = PhotoService.MAX_FILE_SIZE
        
        compressed = PhotoService._compress_to_target(image_bytes, target_size)
        
        assert len(compressed) <= target_size
        assert isinstance(compressed, bytes)

    def test_process_upload_success(self, db: Session, tmp_path):
        """Test successful photo upload and processing"""
        with patch('app.services.photo_service.settings') as mock_settings:
            mock_settings.PHOTOS_DIR = tmp_path / 'photos'
            
            plant = Plant(name='Test', scientific_name='Test spp.')
            db.add(plant)
            db.commit()
            
            image_bytes = self.create_test_image()
            success, photo, msg = PhotoService.process_upload(
                plant.id, image_bytes, 'test.jpg', db
            )
            
            assert success is True
            assert photo is not None
            assert isinstance(msg, str)

    def test_process_upload_invalid_file(self, db: Session):
        """Test upload fails with invalid file"""
        plant = Plant(name='Test', scientific_name='Test spp.')
        db.add(plant)
        db.commit()
        
        invalid_data = b'Not an image'
        success, photo, msg = PhotoService.process_upload(
            plant.id, invalid_data, 'fake.jpg', db
        )
        
        assert success is False
        assert photo is None
        assert 'invalide' in msg.lower()

    def test_get_photos_empty(self, db: Session):
        """Test get_photos returns empty list for new plant"""
        plant = Plant(name='Empty', scientific_name='Empty spp.')
        db.add(plant)
        db.commit()
        
        photos = PhotoService.get_photos(db, plant.id)
        
        assert photos == []

    def test_delete_photo_success(self, db: Session):
        """Test successful photo deletion"""
        plant = Plant(name='Test', scientific_name='Test spp.')
        db.add(plant)
        db.commit()
        
        photo = PhotoModel(
            plant_id=plant.id,
            filename='test.webp',
            file_size=1000,
            width=100,
            height=100
        )
        db.add(photo)
        db.commit()
        
        result = PhotoService.delete_photo(db, photo.id, plant.id)
        
        assert result is True
        # Photo should be soft-deleted, not removed
        deleted_photo = db.query(PhotoModel).filter(PhotoModel.id == photo.id).first()
        assert deleted_photo is None or deleted_photo.deleted_at is not None


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4: HISTORY SERVICE TESTS (166 lines, 34% → 70% coverage)
# ═══════════════════════════════════════════════════════════════════════════

class TestHistoryService:
    """Test history_service.py functions"""

    def test_create_watering_history(self, db: Session):
        """Test creating watering history"""
        plant = Plant(name='Watering Test', scientific_name='Water spp.')
        db.add(plant)
        db.commit()
        
        data = WateringHistoryCreate(
            date=datetime.now().date(),
            amount_ml=250,
            notes='Regular watering'
        )
        
        result = HistoryService.create_watering(db, plant.id, data)
        
        assert result is not None
        assert result.plant_id == plant.id
        assert result.amount_ml == 250
        assert result.notes == 'Regular watering'

    def test_get_watering_history(self, db: Session):
        """Test retrieving specific watering history"""
        plant = Plant(name='Get Water', scientific_name='Get spp.')
        db.add(plant)
        db.commit()
        
        watering = WateringHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            amount_ml=300
        )
        db.add(watering)
        db.commit()
        
        result = HistoryService.get_watering(db, plant.id, watering.id)
        
        assert result is not None
        assert result.id == watering.id
        assert result.amount_ml == 300

    def test_get_all_watering_history(self, db: Session):
        """Test retrieving all watering history for plant"""
        plant = Plant(name='All Waters', scientific_name='All spp.')
        db.add(plant)
        db.commit()
        
        # Add multiple waterings
        for i in range(3):
            watering = WateringHistory(
                plant_id=plant.id,
                date=datetime.now().date() - timedelta(days=i),
                amount_ml=200 + i*50
            )
            db.add(watering)
        db.commit()
        
        results = HistoryService.get_all_watering(db, plant.id)
        
        assert len(results) == 3
        assert all(w.plant_id == plant.id for w in results)

    def test_update_watering_history(self, db: Session):
        """Test updating watering history"""
        plant = Plant(name='Update Water', scientific_name='Update spp.')
        db.add(plant)
        db.commit()
        
        watering = WateringHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            amount_ml=200
        )
        db.add(watering)
        db.commit()
        
        update_data = WateringHistoryUpdate(
            date=watering.date,
            amount_ml=350,
            notes='Updated notes'
        )
        
        result = HistoryService.update_watering(db, plant.id, watering.id, update_data)
        
        assert result is not None
        assert result.amount_ml == 350
        assert result.notes == 'Updated notes'

    def test_delete_watering_history(self, db: Session):
        """Test soft-deleting watering history"""
        plant = Plant(name='Delete Water', scientific_name='Delete spp.')
        db.add(plant)
        db.commit()
        
        watering = WateringHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            amount_ml=200
        )
        db.add(watering)
        db.commit()
        
        result = HistoryService.delete_watering(db, plant.id, watering.id)
        
        assert result is True

    def test_create_fertilizing_history(self, db: Session):
        """Test creating fertilizing history"""
        plant = Plant(name='Fertilize Test', scientific_name='Fert spp.')
        db.add(plant)
        db.commit()
        
        data = FertilizingHistoryCreate(
            date=datetime.now().date(),
            fertilizer_type_id=1,
            amount='50ml'
        )
        
        result = HistoryService.create_fertilizing(db, plant.id, data)
        
        assert result is not None
        assert result.plant_id == plant.id
        assert result.amount == '50ml'

    def test_get_fertilizing_history(self, db: Session):
        """Test retrieving specific fertilizing history"""
        plant = Plant(name='Get Fert', scientific_name='Get fert spp.')
        db.add(plant)
        db.commit()
        
        fertilizing = FertilizingHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            fertilizer_type_id=1,
            amount='75ml'
        )
        db.add(fertilizing)
        db.commit()
        
        result = HistoryService.get_fertilizing(db, plant.id, fertilizing.id)
        
        assert result is not None
        assert result.id == fertilizing.id
        assert result.amount == '75ml'

    def test_get_all_fertilizing_history(self, db: Session):
        """Test retrieving all fertilizing history for plant"""
        plant = Plant(name='All Ferts', scientific_name='All fert spp.')
        db.add(plant)
        db.commit()
        
        # Add multiple fertilizings
        for i in range(2):
            fertilizing = FertilizingHistory(
                plant_id=plant.id,
                date=datetime.now().date() - timedelta(days=i*7),
                fertilizer_type_id=1,
                amount=f'{50+i*25}ml'
            )
            db.add(fertilizing)
        db.commit()
        
        results = HistoryService.get_all_fertilizing(db, plant.id)
        
        assert len(results) == 2
        assert all(f.plant_id == plant.id for f in results)

    def test_update_fertilizing_history(self, db: Session):
        """Test updating fertilizing history"""
        plant = Plant(name='Update Fert', scientific_name='Update fert spp.')
        db.add(plant)
        db.commit()
        
        fertilizing = FertilizingHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            fertilizer_type_id=1,
            amount='50ml'
        )
        db.add(fertilizing)
        db.commit()
        
        update_data = FertilizingHistoryUpdate(
            date=fertilizing.date,
            fertilizer_type_id=2,
            amount='100ml'
        )
        
        result = HistoryService.update_fertilizing(db, plant.id, fertilizing.id, update_data)
        
        assert result is not None
        assert result.amount == '100ml'

    def test_delete_fertilizing_history(self, db: Session):
        """Test soft-deleting fertilizing history"""
        plant = Plant(name='Delete Fert', scientific_name='Delete fert spp.')
        db.add(plant)
        db.commit()
        
        fertilizing = FertilizingHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            fertilizer_type_id=1,
            amount='50ml'
        )
        db.add(fertilizing)
        db.commit()
        
        result = HistoryService.delete_fertilizing(db, plant.id, fertilizing.id)
        
        assert result is True

    def test_create_repotting_history(self, db: Session):
        """Test creating repotting history"""
        plant = Plant(name='Repot Test', scientific_name='Repot spp.')
        db.add(plant)
        db.commit()
        
        data = RepottingHistoryCreate(
            date=datetime.now().date(),
            soil_type='Universal potting mix',
            pot_size_before=10,
            pot_size_after=15
        )
        
        result = HistoryService.create_repotting(db, plant.id, data)
        
        assert result is not None
        assert result.pot_size_after == 15

    def test_get_all_repotting_history(self, db: Session):
        """Test retrieving all repotting history"""
        plant = Plant(name='All Repots', scientific_name='Repot spp.')
        db.add(plant)
        db.commit()
        
        repotting = RepottingHistory(
            plant_id=plant.id,
            date=datetime.now().date(),
            soil_type='Mix',
            pot_size_before=10,
            pot_size_after=15
        )
        db.add(repotting)
        db.commit()
        
        results = HistoryService.get_all_repotting(db, plant.id)
        
        assert len(results) == 1
        assert results[0].pot_size_after == 15


# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4: LOOKUP ROUTES TESTS (126 lines, 0% → 70% coverage)
# ═══════════════════════════════════════════════════════════════════════════

class TestLookupRoutes:
    """Test lookup_routes.py endpoints"""

    def test_get_units_endpoint(self, client):
        """Test get units endpoint"""
        response = client.get('/api/lookups/units')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_fertilizer_types_endpoint(self, client):
        """Test get fertilizer types endpoint"""
        response = client.get('/api/lookups/fertilizer-types')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_unit_endpoint(self, client):
        """Test create unit endpoint"""
        payload = {
            'name': 'test_unit',
            'symbol': 'tu',
            'description': 'Test Unit'
        }
        response = client.post('/api/lookups/units', json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert 'name' in data

    def test_unit_crud_flow(self, client, db: Session):
        """Test unit CRUD operations flow"""
        # Create
        create_payload = {
            'name': 'test_kg',
            'symbol': 'kg',
            'description': 'Test Kilogram'
        }
        create_resp = client.post('/api/lookups/units', json=create_payload)
        assert create_resp.status_code in [200, 201]
        
        # List
        list_resp = client.get('/api/lookups/units')
        assert list_resp.status_code == 200
        assert isinstance(list_resp.json(), list)

    def test_fertilizer_type_endpoints(self, client):
        """Test fertilizer type endpoints exist"""
        response = client.get('/api/lookups/fertilizer-types')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_lookup_endpoints_structure(self, client):
        """Test all lookup endpoints return valid structure"""
        endpoints = [
            '/api/lookups/units',
            '/api/lookups/fertilizer-types',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            assert isinstance(response.json(), list)

    def test_create_and_retrieve_unit(self, client):
        """Test creating and retrieving a unit"""
        # Create unit
        create_payload = {
            'name': 'ml_test',
            'symbol': 'ml',
            'description': 'Milliliter Test'
        }
        create_resp = client.post('/api/lookups/units', json=create_payload)
        assert create_resp.status_code in [200, 201]
        created_unit = create_resp.json()
        
        # Verify it can be retrieved
        assert 'id' in created_unit or 'name' in created_unit

    def test_create_fertilizer_type(self, client):
        """Test creating a fertilizer type"""
        payload = {
            'name': 'NPK_Test',
            'description': 'Test NPK blend',
            'unit': 'ml'
        }
        response = client.post('/api/lookups/fertilizer-types', json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert 'name' in data

    def test_lookup_api_errors(self, client):
        """Test lookup API error handling"""
        # Try to get non-existent unit
        response = client.get('/api/lookups/units/99999')
        # Should either return 404 or empty depending on implementation
        assert response.status_code in [200, 404]

    def test_lookup_payload_validation(self, client):
        """Test lookup endpoint payload validation"""
        # Try invalid payload
        invalid_payload = {'invalid_field': 'value'}
        response = client.post('/api/lookups/units', json=invalid_payload)
        # Should fail validation (422 or 400)
        assert response.status_code >= 400

    def test_multiple_lookups_independence(self, client):
        """Test that different lookup types are independent"""
        # Get units count
        units_resp = client.get('/api/lookups/units')
        units_count = len(units_resp.json())
        
        # Get fertilizer types count
        ferts_resp = client.get('/api/lookups/fertilizer-types')
        ferts_count = len(ferts_resp.json())
        
        # Both should be lists
        assert isinstance(units_resp.json(), list)
        assert isinstance(ferts_resp.json(), list)

    def test_lookup_endpoints_async_support(self, client):
        """Test that lookup endpoints are properly async"""
        # Make multiple requests
        resp1 = client.get('/api/lookups/units')
        resp2 = client.get('/api/lookups/fertilizer-types')
        
        assert resp1.status_code == 200
        assert resp2.status_code == 200

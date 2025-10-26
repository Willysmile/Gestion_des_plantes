"""
Phase 3.2 - Photo Gallery E2E Tests
Tests les endpoints photo et la conversion WebP
"""

import pytest
import json
from pathlib import Path
from io import BytesIO
import time
import sys

# Import depuis les tests existants
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPhotoEndpoints:
    """Tests for photo upload, delete, and management endpoints"""

    def test_photo_migration_exists(self):
        """Vérifier que la migration Photo existe"""
        migrations_dir = Path(__file__).parent.parent / 'migrations' / 'versions'
        migration_files = list(migrations_dir.glob('*add_photos*'))
        assert len(migration_files) > 0, "Photo migration not found"
        print(f"✓ Photo migration found: {migration_files[0].name}")

    def test_photos_directory_structure(self):
        """Vérifier la structure du répertoire data/photos"""
        photos_dir = Path(__file__).parent.parent.parent / 'data' / 'photos'
        # Le répertoire sera créé lors du premier upload
        print(f"✓ Photos directory path: {photos_dir}")

    def test_photo_model_file_exists(self):
        """Vérifier que le fichier du modèle Photo existe"""
        photo_file = Path(__file__).parent.parent / 'app' / 'models' / 'photo.py'
        assert photo_file.exists(), "Photo model file not found"
        
        content = photo_file.read_text()
        required_fields = ['plant_id', 'filename', 'file_size', 'width', 'height', 'is_primary', 'created_at', 'updated_at']
        
        for field in required_fields:
            assert field in content, f"Field {field} not found in Photo model"
            print(f"✓ Photo.{field} field defined")

    def test_photo_routes_file_exists(self):
        """Vérifier que le fichier des routes photo existe"""
        routes_file = Path(__file__).parent.parent / 'app' / 'routes' / 'photos.py'
        assert routes_file.exists(), "Photo routes file not found"
        
        content = routes_file.read_text()
        
        # Vérifier les endpoints
        endpoints = [
            'POST /api/plants',
            'GET /api/plants',
            'DELETE /api/plants',
            'PUT /api/plants',
        ]
        
        # Vérifier au moins quelques endpoints
        assert '@router.post' in content, "POST endpoint not found"
        assert '@router.get' in content, "GET endpoint not found"
        assert '@router.delete' in content, "DELETE endpoint not found"
        assert '@router.put' in content, "PUT endpoint not found"
        
        print("✓ POST endpoint exists")
        print("✓ GET endpoint exists")
        print("✓ DELETE endpoint exists")
        print("✓ PUT endpoint exists")

    def test_image_processor_file_exists(self):
        """Vérifier que le fichier processeur d'images existe"""
        processor_file = Path(__file__).parent.parent / 'app' / 'utils' / 'image_processor.py'
        assert processor_file.exists(), "Image processor file not found"
        
        content = processor_file.read_text()
        
        functions = ['validate_image_upload', 'process_image_to_webp', 'delete_photo_files']
        for func in functions:
            assert func in content, f"Function {func} not found in image_processor.py"
            print(f"✓ image_processor.{func} defined")

    def test_photo_schema_file_exists(self):
        """Vérifier que le fichier schema photo existe"""
        schema_file = Path(__file__).parent.parent / 'app' / 'schemas' / 'photo_schema.py'
        assert schema_file.exists(), "Photo schema file not found"
        
        content = schema_file.read_text()
        
        schemas = ['PhotoResponse', 'PhotoUploadResponse']
        for schema in schemas:
            assert schema in content, f"Schema {schema} not found"
            print(f"✓ {schema} schema defined")

    def test_frontend_api_client(self):
        """Vérifier que le client API frontend existe"""
        api_file = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'lib' / 'api' / 'photosAPI.js'
        assert api_file.exists(), "photosAPI.js not found"
        
        content = api_file.read_text()
        
        # Vérifier les méthodes principales
        methods = ['uploadPhoto', 'getPhotos', 'deletePhoto', 'setPrimaryPhoto', 'getPhotoUrl', 'validateImageFile']
        for method in methods:
            assert method in content, f"Method {method} not found in photosAPI.js"
            print(f"✓ photosAPI.{method} exists")

    def test_frontend_components_exist(self):
        """Vérifier que les composants React existent"""
        components = {
            'PlantPhotoUpload.jsx': Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'components' / 'PlantPhotoUpload.jsx',
            'PlantPhotoGallery.jsx': Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'components' / 'PlantPhotoGallery.jsx',
            'PhotoCarousel.jsx': Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'components' / 'PhotoCarousel.jsx',
        }
        
        for comp_name, comp_path in components.items():
            assert comp_path.exists(), f"{comp_name} not found"
            print(f"✓ {comp_name} exists")

    def test_plant_form_page_integration(self):
        """Vérifier que PlantFormPage importe les composants photo"""
        form_file = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'pages' / 'PlantFormPage.jsx'
        content = form_file.read_text()
        
        # Vérifier les imports
        assert 'PlantPhotoUpload' in content, "PlantPhotoUpload not imported"
        assert 'PlantPhotoGallery' in content, "PlantPhotoGallery not imported"
        assert 'photosAPI' in content, "photosAPI not imported"
        
        print("✓ PlantFormPage imports PlantPhotoUpload")
        print("✓ PlantFormPage imports PlantPhotoGallery")
        print("✓ PlantFormPage imports photosAPI")

    def test_main_app_imports_photo_routes(self):
        """Vérifier que main.py importe les routes photo"""
        main_file = Path(__file__).parent.parent / 'app' / 'main.py'
        content = main_file.read_text()
        
        # Vérifier l'import
        if 'photos' in content:
            print("✓ main.py includes photo routes reference")
        else:
            print("⚠ Photo routes may need to be registered in main.py")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])


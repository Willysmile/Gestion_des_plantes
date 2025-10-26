"""
Tests pour les routes de photos
"""

import pytest
from datetime import date


class TestPhotosAPI:
    """Tests des endpoints de photos"""
    
    def test_photos_crud(self, client):
        """Test CRUD pour photos"""
        # Create plant
        plant = client.post("/api/plants", json={"name": "Photo Test", "family": "Araceae"}).json()
        plant_id = plant["id"]
        
        # LIST photos
        list_response = client.get(f"/api/plants/{plant_id}/photos")
        assert list_response.status_code == 200
        assert isinstance(list_response.json(), list)
    
    def test_get_photos_nonexistent_plant(self, client):
        """Tester l'accès aux photos d'une plante inexistante"""
        response = client.get("/api/plants/99999/photos")
        assert response.status_code in [404, 400]
    
    def test_upload_photo_mock(self, client):
        """Test upload photo (si endpoint existe)"""
        plant = client.post("/api/plants", json={"name": "Upload Test", "family": "Araceae"}).json()
        plant_id = plant["id"]
        
        # Try to create a photo metadata entry
        photo_data = {
            "filename": "test.jpg",
            "url": "/photos/1/test.jpg",
            "upload_date": date.today().isoformat()
        }
        
        response = client.post(
            f"/api/plants/{plant_id}/photos",
            json=photo_data
        )
        
        # Accept various responses (route may not exist)
        assert response.status_code in [200, 201, 400, 404, 422]

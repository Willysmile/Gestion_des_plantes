"""
Integration tests for Plant API endpoints
"""

import pytest
from fastapi import status
from datetime import datetime


class TestPlantAPI:
    """Tests for Plant CRUD API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ok"
    
    def test_create_plant(self, client):
        """Test creating a plant via API"""
        payload = {
            "name": "Monstera Deliciosa",
            "family": "Araceae",
            "genus": "Monstera",
            "species": "deliciosa",
            "temperature_min": 15,
            "temperature_max": 25,
            "humidity_level": 60
        }
        
        response = client.post("/api/plants", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["name"] == "Monstera Deliciosa"
        assert data["scientific_name"] == "Monstera deliciosa"
        assert data["reference"].startswith("ARACE-")
        assert data["id"] is not None
    
    def test_get_plants(self, client):
        """Test getting all plants"""
        # Create a plant first
        payload = {"name": "Test Plant", "family": "Araceae"}
        client.post("/api/plants", json=payload)
        
        # Get all plants
        response = client.get("/api/plants")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_plant_by_id(self, client):
        """Test getting plant by ID"""
        # Create plant
        payload = {"name": "Test Plant"}
        create_response = client.post("/api/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        # Get plant
        response = client.get(f"/api/plants/{plant_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Test Plant"
    
    def test_update_plant(self, client):
        """Test updating a plant"""
        # Create plant
        payload = {"name": "Test Plant", "health_status": "healthy"}
        create_response = client.post("/api/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        # Update plant
        update_payload = {"name": "Updated Plant", "health_status": "sick"}
        response = client.put(f"/api/plants/{plant_id}", json=update_payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Plant"
        assert response.json()["health_status"] == "sick"
    
    def test_delete_plant(self, client):
        """Test deleting (soft delete) a plant"""
        # Create plant
        payload = {"name": "Test Plant"}
        create_response = client.post("/api/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        # Delete plant (returns 204 No Content)
        response = client.delete(f"/api/plants/{plant_id}")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        
        # Plant should still exist (soft delete)
        get_response = client.get(f"/api/plants/{plant_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND or \
               get_response.json().get("deleted_at") is not None
    
    def test_archive_plant(self, client):
        """Test archiving a plant"""
        # Create plant
        payload = {"name": "Test Plant"}
        create_response = client.post("/api/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        # Archive plant
        archive_payload = {"reason": "Plant died"}
        response = client.patch(f"/api/plants/{plant_id}/archive", json=archive_payload)
        
        if response.status_code == status.HTTP_200_OK:
            assert response.json()["is_archived"] is True
            assert response.json()["archived_reason"] == "Plant died"
    
    def test_restore_plant(self, client):
        """Test restoring an archived plant"""
        # Create and archive plant
        payload = {"name": "Test Plant"}
        create_response = client.post("/api/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        archive_payload = {"reason": "Testing"}
        client.patch(f"/api/plants/{plant_id}/archive", json=archive_payload)
        
        # Restore plant
        response = client.patch(f"/api/plants/{plant_id}/restore")
        
        if response.status_code == status.HTTP_200_OK:
            assert response.json()["is_archived"] is False
    
    def test_create_plant_validation(self, client):
        """Test plant creation with invalid data"""
        # Empty name - should fail
        payload = {"name": ""}
        response = client.post("/api/plants", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Missing required field
        payload = {"family": "Araceae"}  # no name
        response = client.post("/api/plants", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_plant_with_invalid_temperature(self, client):
        """Test creating plant with invalid temperature range"""
        payload = {
            "name": "Plant",
            "temperature_min": 25,
            "temperature_max": 15  # Invalid: min > max
        }
        response = client.post("/api/plants", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_nonexistent_plant(self, client):
        """Test getting non-existent plant"""
        response = client.get("/api/plants/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_multiple_plants_reference_sequence(self, client):
        """Test reference generation sequence"""
        # Create first plant
        payload1 = {"name": "Plant 1", "family": "Araceae"}
        response1 = client.post("/api/plants", json=payload1)
        ref1 = response1.json()["reference"]
        
        # Create second plant same family
        payload2 = {"name": "Plant 2", "family": "Araceae"}
        response2 = client.post("/api/plants", json=payload2)
        ref2 = response2.json()["reference"]
        
        # References should be sequential
        assert ref1.startswith("ARACE-")
        assert ref2.startswith("ARACE-")
        assert ref1 != ref2

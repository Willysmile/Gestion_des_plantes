"""
Integration tests for Plant API endpoints
"""

import pytest
from fastapi import status


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
        
        response = client.post("/plants", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["name"] == "Monstera Deliciosa"
        assert data["scientific_name"] == "Monstera deliciosa"
        assert data["reference"].startswith("ARACA-")
    
    def test_get_plants(self, client):
        """Test getting all plants"""
        # Create a plant first
        payload = {"name": "Test Plant", "family": "Araceae"}
        client.post("/plants", json=payload)
        
        # Get all plants
        response = client.get("/plants")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data) > 0
        assert data[0]["name"] == "Test Plant"
    
    def test_get_plant_by_id(self, client):
        """Test getting plant by ID"""
        # Create plant
        payload = {"name": "Test Plant"}
        create_response = client.post("/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        # Get plant
        response = client.get(f"/plants/{plant_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Test Plant"
    
    def test_update_plant(self, client):
        """Test updating a plant"""
        # Create plant
        payload = {"name": "Test Plant", "health_status": "healthy"}
        create_response = client.post("/plants", json=payload)
        plant_id = create_response.json()["id"]
        
        # Update plant
        update_payload = {"name": "Updated Plant", "health_status": "sick"}
        response = client.put(f"/plants/{plant_id}", json=update_payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Plant"
        assert response.json()["health_status"] == "sick"
    
    def test_create_plant_validation(self, client):
        """Test plant creation with invalid data"""
        # Empty name
        payload = {"name": ""}
        response = client.post("/plants", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Invalid temperature range
        payload = {"name": "Plant", "temperature_min": 25, "temperature_max": 15}
        response = client.post("/plants", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

"""
Integration tests for plants routes covering all endpoints and error cases
"""

import pytest


def test_list_plants_basic(client):
    """Test GET /api/plants basic listing"""
    # Create a few plants
    client.post("/api/plants", json={"name": "Plant 1"})
    client.post("/api/plants", json={"name": "Plant 2"})
    
    resp = client.get("/api/plants")
    assert resp.status_code == 200
    plants = resp.json()
    assert isinstance(plants, list)
    assert len(plants) >= 2


def test_generate_reference_endpoint(client):
    """Test POST /api/plants/generate-reference"""
    resp = client.post("/api/plants/generate-reference?family=Araceae")
    assert resp.status_code == 200
    data = resp.json()
    assert "reference" in data
    assert data["reference"].startswith("ARAC")


def test_generate_reference_with_short_family(client):
    """Test reference generation with short family"""
    resp = client.post("/api/plants/generate-reference?family=Ivy")
    assert resp.status_code == 200
    data = resp.json()
    assert data["reference"].startswith("IVY")


def test_generate_reference_empty_family_error(client):
    """Test that empty family returns error"""
    resp = client.post("/api/plants/generate-reference?family=")
    assert resp.status_code == 422  # Validation error


def test_list_plants_pagination(client):
    """Test pagination with skip and limit"""
    # Create 10 plants
    for i in range(10):
        client.post("/api/plants", json={"name": f"Plant {i}"})
    
    # Get page 1
    resp = client.get("/api/plants?skip=0&limit=5")
    assert resp.status_code == 200
    page1 = resp.json()
    assert len(page1) == 5
    
    # Get page 2
    resp = client.get("/api/plants?skip=5&limit=5")
    assert resp.status_code == 200
    page2 = resp.json()
    assert len(page2) == 5
    
    # Verify no overlap
    page1_ids = {p["id"] for p in page1}
    page2_ids = {p["id"] for p in page2}
    assert len(page1_ids & page2_ids) == 0


def test_list_plants_include_archived(client):
    """Test listing with include_archived parameter"""
    # Create active plant
    resp1 = client.post("/api/plants", json={"name": "Active"})
    active_id = resp1.json()["id"]
    
    # Create and archive plant
    resp2 = client.post("/api/plants", json={"name": "Archived"})
    archived_id = resp2.json()["id"]
    client.post(f"/api/plants/{archived_id}/archive")
    
    # Get without archived
    resp = client.get("/api/plants?archived=false")
    assert resp.status_code == 200
    results = resp.json()
    ids = {p["id"] for p in results}
    assert active_id in ids
    assert archived_id not in ids
    
    # Get with archived
    resp = client.get("/api/plants?archived=true")
    assert resp.status_code == 200
    results = resp.json()
    ids = {p["id"] for p in results}
    assert archived_id in ids


def test_create_plant_with_all_fields(client):
    """Test creating plant with comprehensive data"""
    plant_data = {
        "name": "Complete Plant",
        "scientific_name": "Monstera deliciosa",
        "family": "Araceae",
        "genus": "Monstera",
        "species": "deliciosa",
        "description": "A beautiful climbing plant",
        "health_status": "healthy",
        "difficulty_level": "easy",
        "growth_speed": "fast",
        "location_id": 1,
        "temperature_min": 15,
        "temperature_max": 25,
        "humidity_level": 60,
        "soil_type": "loamy",
        "is_indoor": True,
        "is_favorite": True,
        "is_toxic": False
    }
    resp = client.post("/api/plants", json=plant_data)
    assert resp.status_code == 201
    plant = resp.json()
    assert plant["name"] == "Complete Plant"
    assert plant["temperature_min"] == 15


def test_create_plant_validation_errors(client):
    """Test that invalid data is rejected"""
    # Invalid: temperature_min > temperature_max
    resp = client.post("/api/plants", json={
        "name": "Bad Plant",
        "temperature_min": 30,
        "temperature_max": 20
    })
    assert resp.status_code == 422


def test_update_plant_partial(client):
    """Test updating only specific fields"""
    resp = client.post("/api/plants", json={"name": "Original"})
    plant_id = resp.json()["id"]
    
    # Update only name
    resp = client.put(f"/api/plants/{plant_id}", json={"name": "Updated"})
    assert resp.status_code == 200
    plant = resp.json()
    assert plant["name"] == "Updated"


def test_get_plant_not_found_returns_404(client):
    """Test that getting non-existent plant returns 404"""
    resp = client.get("/api/plants/99999")
    assert resp.status_code == 404


def test_update_plant_not_found_returns_404(client):
    """Test that updating non-existent plant returns 404"""
    resp = client.put("/api/plants/99999", json={"name": "Updated"})
    assert resp.status_code == 404


def test_delete_plant_not_found_returns_404(client):
    """Test that deleting non-existent plant returns 404"""
    resp = client.delete("/api/plants/99999")
    assert resp.status_code == 404


def test_regenerate_reference_updates_reference(client):
    """Test that regenerate-reference creates new reference"""
    # Create plant with family
    resp = client.post("/api/plants", json={"name": "Test", "family": "Araceae"})
    plant_id = resp.json()["id"]
    original_ref = resp.json()["reference"]
    
    # Regenerate reference
    resp = client.post(f"/api/plants/{plant_id}/regenerate-reference")
    assert resp.status_code == 200
    new_plant = resp.json()
    # New reference should have same prefix but potentially different number
    assert new_plant["reference"].startswith("ARAC")


def test_regenerate_reference_no_family_returns_400(client):
    """Test that regenerate-reference fails without family"""
    resp = client.post("/api/plants", json={"name": "No Family"})
    plant_id = resp.json()["id"]
    
    resp = client.post(f"/api/plants/{plant_id}/regenerate-reference")
    assert resp.status_code == 400


def test_regenerate_reference_nonexistent_plant_returns_404(client):
    """Test that regenerating reference for non-existent plant returns 404"""
    resp = client.post("/api/plants/99999/regenerate-reference")
    assert resp.status_code == 404


def test_archive_plant_not_found_returns_404(client):
    """Test that archiving non-existent plant returns 404"""
    resp = client.post("/api/plants/99999/archive")
    assert resp.status_code == 404


def test_restore_plant_not_found_returns_404(client):
    """Test that restoring non-existent plant returns 404"""
    resp = client.post("/api/plants/99999/restore")
    assert resp.status_code == 404

"""
Integration tests for settings routes
Covers all lookup-related CRUD endpoints for locations, purchase places, watering frequencies, light requirements, etc.
"""

import pytest


def test_get_locations(client):
    """Test GET /api/settings/locations"""
    resp = client.get("/api/settings/locations")
    assert resp.status_code == 200
    locations = resp.json()
    assert isinstance(locations, list)


def test_create_location(client):
    """Test POST /api/settings/locations"""
    resp = client.post("/api/settings/locations", json={"name": "Living Room", "description": "Bright spot"})
    assert resp.status_code == 201
    location = resp.json()
    assert location["name"] == "Living Room"


def test_get_location_by_id(client):
    """Test GET /api/settings/locations/{id}"""
    # Create location
    create_resp = client.post("/api/settings/locations", json={"name": "Bedroom"})
    location_id = create_resp.json()["id"]
    
    resp = client.get(f"/api/settings/locations/{location_id}")
    assert resp.status_code == 200
    location = resp.json()
    assert location["id"] == location_id


def test_get_location_not_found(client):
    """Test GET /api/settings/locations/{id} when not found"""
    resp = client.get("/api/settings/locations/99999")
    assert resp.status_code == 404


def test_update_location(client):
    """Test PUT /api/settings/locations/{id}"""
    create_resp = client.post("/api/settings/locations", json={"name": "Office"})
    location_id = create_resp.json()["id"]
    
    resp = client.put(f"/api/settings/locations/{location_id}", json={"name": "Home Office"})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["name"] == "Home Office"


def test_delete_location(client):
    """Test DELETE /api/settings/locations/{id}"""
    create_resp = client.post("/api/settings/locations", json={"name": "Storage"})
    location_id = create_resp.json()["id"]
    
    resp = client.delete(f"/api/settings/locations/{location_id}")
    assert resp.status_code == 204


def test_get_purchase_places(client):
    """Test GET /api/settings/purchase-places"""
    resp = client.get("/api/settings/purchase-places")
    assert resp.status_code == 200
    places = resp.json()
    assert isinstance(places, list)


def test_create_purchase_place(client):
    """Test POST /api/settings/purchase-places"""
    resp = client.post("/api/settings/purchase-places", json={"name": "Garden Center", "phone": "555-1234"})
    assert resp.status_code == 201
    place = resp.json()
    assert place["name"] == "Garden Center"


def test_get_purchase_place_by_id(client):
    """Test GET /api/settings/purchase-places/{id}"""
    create_resp = client.post("/api/settings/purchase-places", json={"name": "Nursery"})
    place_id = create_resp.json()["id"]
    
    resp = client.get(f"/api/settings/purchase-places/{place_id}")
    assert resp.status_code == 200
    place = resp.json()
    assert place["id"] == place_id


def test_get_watering_frequencies(client):
    """Test GET /api/settings/watering-frequencies"""
    resp = client.get("/api/settings/watering-frequencies")
    assert resp.status_code == 200
    freqs = resp.json()
    assert isinstance(freqs, list)


def test_get_light_requirements(client):
    """Test GET /api/settings/light-requirements"""
    resp = client.get("/api/settings/light-requirements")
    assert resp.status_code == 200
    lights = resp.json()
    assert isinstance(lights, list)


def test_get_fertilizer_types(client):
    """Test GET /api/settings/fertilizer-types"""
    resp = client.get("/api/settings/fertilizer-types")
    assert resp.status_code == 200
    fertilizers = resp.json()
    assert isinstance(fertilizers, list)


def test_get_tag_categories(client):
    """Test GET /api/settings/tag-categories"""
    resp = client.get("/api/settings/tag-categories")
    assert resp.status_code == 200
    categories = resp.json()
    assert isinstance(categories, list)


def test_get_tags(client):
    """Test GET /api/settings/tags"""
    resp = client.get("/api/settings/tags")
    assert resp.status_code == 200
    tags = resp.json()
    assert isinstance(tags, list)


def test_create_tag(client):
    """Test POST /api/settings/tags"""
    resp = client.post("/api/settings/tags", json={"name": "TestTag123", "category_id": 1})
    assert resp.status_code == 201
    tag = resp.json()
    assert tag["name"] == "TestTag123"


def test_get_diseases(client):
    """Test GET /api/settings/diseases"""
    resp = client.get("/api/settings/diseases")
    assert resp.status_code == 200
    diseases = resp.json()
    assert isinstance(diseases, list)


def test_create_disease(client):
    """Test POST /api/settings/diseases"""
    resp = client.post("/api/settings/diseases", json={"name": "TestDisease123"})
    assert resp.status_code == 201
    disease = resp.json()
    assert disease["name"] == "TestDisease123"


def test_get_treatments(client):
    """Test GET /api/settings/treatments"""
    resp = client.get("/api/settings/treatments")
    assert resp.status_code == 200
    treatments = resp.json()
    assert isinstance(treatments, list)


def test_create_purchase_place_error_handling(client):
    """Test error handling for purchase places"""
    # Try to create without required name
    resp = client.post("/api/settings/purchase-places", json={"phone": "555-1234"})
    assert resp.status_code == 422


def test_update_location_not_found(client):
    """Test updating non-existent location"""
    resp = client.put("/api/settings/locations/99999", json={"name": "Updated"})
    assert resp.status_code == 404


def test_delete_location_not_found(client):
    """Test deleting non-existent location"""
    resp = client.delete("/api/settings/locations/99999")
    assert resp.status_code == 404

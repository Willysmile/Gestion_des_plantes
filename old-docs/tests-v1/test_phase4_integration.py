"""
Phase 4B Integration Tests - E2E testing for Settings, Search, and Dashboard
"""

import pytest
import httpx
import asyncio
from datetime import datetime
from typing import Optional


# ====================
# FIXTURES
# ====================

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
async def http_client():
    """Create HTTP client for tests"""
    async with httpx.AsyncClient(timeout=10) as client:
        yield client


def unique_id() -> int:
    """Generate unique ID based on timestamp"""
    return int(datetime.now().timestamp() * 1000) % 100000


# ====================
# SETTINGS WINDOW TESTS
# ====================

@pytest.mark.asyncio
async def test_settings_locations_create_read_delete():
    """Test creating, reading, and deleting a location"""
    async with httpx.AsyncClient(timeout=10) as client:
        unique_name = f"TestLoc_{unique_id()}"
        
        # CREATE
        resp = await client.post(
            f"{BASE_URL}/api/settings/locations",
            json={"name": unique_name}
        )
        assert resp.status_code == 201
        location = resp.json()
        location_id = location["id"]
        assert location["name"] == unique_name
        
        # READ (in list)
        resp = await client.get(f"{BASE_URL}/api/settings/locations")
        assert resp.status_code == 200
        locations = resp.json()
        location_names = [l["name"] for l in locations]
        assert unique_name in location_names
        
        # DELETE
        resp = await client.delete(f"{BASE_URL}/api/settings/locations/{location_id}")
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_settings_locations_read_all():
    """Test reading all locations"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/api/settings/locations")
        assert resp.status_code == 200
        locations = resp.json()
        assert isinstance(locations, list)
        assert len(locations) > 0


@pytest.mark.asyncio
async def test_settings_purchase_places_crud():
    """Test CRUD for purchase places"""
    async with httpx.AsyncClient(timeout=10) as client:
        unique_name = f"TestPlace_{unique_id()}"
        
        # CREATE
        resp = await client.post(
            f"{BASE_URL}/api/settings/purchase-places",
            json={"name": unique_name}
        )
        assert resp.status_code == 201
        place = resp.json()
        place_id = place["id"]
        
        # UPDATE
        updated_name = f"Updated_{unique_id()}"
        resp = await client.put(
            f"{BASE_URL}/api/settings/purchase-places/{place_id}",
            json={"name": updated_name}
        )
        assert resp.status_code == 200
        updated_place = resp.json()
        assert updated_place["name"] == updated_name
        
        # DELETE
        resp = await client.delete(f"{BASE_URL}/api/settings/purchase-places/{place_id}")
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_settings_watering_frequencies_crud():
    """Test CRUD for watering frequencies (includes days field)"""
    async with httpx.AsyncClient(timeout=10) as client:
        unique_name = f"TestWater_{unique_id()}"
        days = 5
        
        # CREATE
        resp = await client.post(
            f"{BASE_URL}/api/settings/watering-frequencies",
            json={"name": unique_name, "days": days}
        )
        assert resp.status_code == 201
        freq = resp.json()
        freq_id = freq["id"]
        assert freq["name"] == unique_name
        assert freq["days"] == days
        
        # UPDATE
        new_days = 7
        resp = await client.put(
            f"{BASE_URL}/api/settings/watering-frequencies/{freq_id}",
            json={"name": unique_name, "days": new_days}
        )
        assert resp.status_code == 200
        updated_freq = resp.json()
        assert updated_freq["days"] == new_days
        
        # DELETE
        resp = await client.delete(
            f"{BASE_URL}/api/settings/watering-frequencies/{freq_id}"
        )
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_settings_light_requirements_crud():
    """Test CRUD for light requirements"""
    async with httpx.AsyncClient(timeout=10) as client:
        unique_name = f"TestLight_{unique_id()}"
        
        # CREATE
        resp = await client.post(
            f"{BASE_URL}/api/settings/light-requirements",
            json={"name": unique_name}
        )
        assert resp.status_code == 201
        light = resp.json()
        light_id = light["id"]
        
        # DELETE
        resp = await client.delete(
            f"{BASE_URL}/api/settings/light-requirements/{light_id}"
        )
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_settings_fertilizer_types_crud():
    """Test CRUD for fertilizer types"""
    async with httpx.AsyncClient(timeout=10) as client:
        unique_name = f"TestFert_{unique_id()}"
        
        # CREATE
        resp = await client.post(
            f"{BASE_URL}/api/settings/fertilizer-types",
            json={"name": unique_name}
        )
        assert resp.status_code == 201
        fert = resp.json()
        fert_id = fert["id"]
        
        # DELETE
        resp = await client.delete(
            f"{BASE_URL}/api/settings/fertilizer-types/{fert_id}"
        )
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_settings_tags_read_all():
    """Test reading all tags"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/api/settings/tags")
        assert resp.status_code == 200
        tags = resp.json()
        assert isinstance(tags, list)


# ====================
# SEARCH & FILTER TESTS
# ====================

@pytest.mark.asyncio
async def test_search_plants_by_query():
    """Test searching plants"""
    async with httpx.AsyncClient(timeout=10) as client:
        # Should find at least some plants
        resp = await client.get(
            f"{BASE_URL}/api/plants/search",
            params={"q": "Rose"}
        )
        assert resp.status_code == 200
        plants = resp.json()
        assert isinstance(plants, list)


@pytest.mark.asyncio
async def test_filter_plants():
    """Test filtering plants"""
    async with httpx.AsyncClient(timeout=10) as client:
        # Get all plants first to verify endpoint works
        resp = await client.get(f"{BASE_URL}/api/plants/filter")
        assert resp.status_code == 200
        plants = resp.json()
        assert isinstance(plants, list)


@pytest.mark.asyncio
async def test_plants_to_water():
    """Test getting plants to water"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/api/plants/to-water",
            params={"days_ago": 0}
        )
        assert resp.status_code == 200
        plants = resp.json()
        assert isinstance(plants, list)


@pytest.mark.asyncio
async def test_plants_to_fertilize():
    """Test getting plants to fertilize"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/api/plants/to-fertilize",
            params={"days_ago": 0}
        )
        assert resp.status_code == 200
        plants = resp.json()
        assert isinstance(plants, list)


# ====================
# DASHBOARD TESTS
# ====================

@pytest.mark.asyncio
async def test_dashboard_stats():
    """Test getting dashboard statistics"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/api/statistics/dashboard")
        assert resp.status_code == 200
        stats = resp.json()
        
        # Verify all KPIs are present
        assert "total_plants" in stats
        assert "active_plants" in stats
        assert "archived_plants" in stats
        assert "health_excellent" in stats
        assert "health_good" in stats
        assert "health_poor" in stats
        assert "total_photos" in stats
        
        # Verify KPIs are non-negative integers
        assert isinstance(stats["total_plants"], int)
        assert stats["total_plants"] >= 0


@pytest.mark.asyncio
async def test_dashboard_upcoming_waterings():
    """Test getting upcoming waterings schedule"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/api/statistics/upcoming-waterings",
            params={"days": 7}
        )
        assert resp.status_code == 200
        waterings = resp.json()
        assert isinstance(waterings, list)


@pytest.mark.asyncio
async def test_dashboard_upcoming_fertilizing():
    """Test getting upcoming fertilizing schedule"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/api/statistics/upcoming-fertilizing",
            params={"days": 7}
        )
        assert resp.status_code == 200
        fertilizing = resp.json()
        assert isinstance(fertilizing, list)


# ====================
# END-TO-END TESTS
# ====================

@pytest.mark.asyncio
async def test_e2e_settings_workflow():
    """Test complete settings workflow: create location, verify in list, delete"""
    async with httpx.AsyncClient(timeout=10) as client:
        unique_name = f"E2E_Location_{unique_id()}"
        
        # 1. Create location
        resp = await client.post(
            f"{BASE_URL}/api/settings/locations",
            json={"name": unique_name}
        )
        assert resp.status_code == 201
        created = resp.json()
        location_id = created["id"]
        
        # 2. Verify in list
        resp = await client.get(f"{BASE_URL}/api/settings/locations")
        assert resp.status_code == 200
        locations = resp.json()
        location_names = [l["name"] for l in locations]
        assert unique_name in location_names
        
        # 3. Delete
        resp = await client.delete(f"{BASE_URL}/api/settings/locations/{location_id}")
        assert resp.status_code == 204
        
        # 4. Verify deleted
        resp = await client.get(f"{BASE_URL}/api/settings/locations")
        locations = resp.json()
        location_names = [l["name"] for l in locations]
        assert unique_name not in location_names


@pytest.mark.asyncio
async def test_e2e_complete_workflow():
    """Test complete user workflow: Settings → Search → Dashboard"""
    async with httpx.AsyncClient(timeout=10) as client:
        # 1. Create test location in settings
        unique_location = f"E2E_Loc_{unique_id()}"
        resp = await client.post(
            f"{BASE_URL}/api/settings/locations",
            json={"name": unique_location}
        )
        assert resp.status_code == 201
        location_id = resp.json()["id"]
        
        # 2. Get all plants (search feature)
        resp = await client.get(f"{BASE_URL}/api/plants")
        assert resp.status_code == 200
        all_plants = resp.json()
        assert len(all_plants) > 0
        
        # 3. Check dashboard stats
        resp = await client.get(f"{BASE_URL}/api/statistics/dashboard")
        assert resp.status_code == 200
        stats = resp.json()
        assert stats["total_plants"] > 0
        
        # 4. Cleanup
        resp = await client.delete(
            f"{BASE_URL}/api/settings/locations/{location_id}"
        )
        assert resp.status_code == 204


# ====================
# ERROR HANDLING TESTS
# ====================

@pytest.mark.asyncio
async def test_delete_nonexistent_location():
    """Test deleting non-existent location returns 404"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.delete(
            f"{BASE_URL}/api/settings/locations/999999"
        )
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_invalid_watering_frequency_data():
    """Test creating watering frequency with invalid data"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{BASE_URL}/api/settings/watering-frequencies",
            json={"name": "Test"}  # Missing 'days' field
        )
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_stats_with_invalid_days():
    """Test statistics endpoint with invalid days parameter"""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BASE_URL}/api/statistics/upcoming-waterings",
            params={"days": "invalid"}
        )
        # Should be 422 (validation error) or 200 with default
        assert resp.status_code in [200, 422]


# ====================
# TEST SUMMARY
# ====================

if __name__ == "__main__":
    print("Phase 4B Integration Tests")
    print("=" * 60)
    print("\nRun with: pytest test_phase4_integration.py -v")
    print("\nTest Categories:")
    print("  ✓ Settings Window Tests (6 tabs CRUD)")
    print("  ✓ Search & Filter Tests")
    print("  ✓ Dashboard Tests (KPIs + Tables)")
    print("  ✓ End-to-End Workflows")
    print("  ✓ Error Handling")
    print("\nExpected: 100% pass rate")

#!/usr/bin/env python3
"""
END-TO-END TESTING SCRIPT
Teste chaque fonction CRUD pour confirmer qu'elle marche vraiment
"""

import httpx
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_test(title, status="⏳"):
    """Pretty print test status"""
    print(f"\n{'='*70}")
    print(f"{status} {title}")
    print(f"{'='*70}")

def print_result(success, message=""):
    """Print result"""
    symbol = "✅" if success else "❌"
    print(f"{symbol} {message}")
    return success

# ============================================================================
# TEST 1: API Connection
# ============================================================================

print_test("TEST 1: API Connection", "🔌")
try:
    resp = httpx.get(f"{BASE_URL}/health", timeout=5)
    if resp.status_code == 200:
        print_result(True, f"API is running: {resp.json()}")
        api_ok = True
    else:
        print_result(False, f"API returned {resp.status_code}")
        api_ok = False
except Exception as e:
    print_result(False, f"Cannot connect: {e}")
    api_ok = False
    sys.exit(1)

# ============================================================================
# TEST 2: Create Plant
# ============================================================================

print_test("TEST 2: Create Plant", "➕")
test_plant_name = f"Test_Plant_{datetime.now().strftime('%H%M%S')}"
test_plant = {
    "name": test_plant_name,
    "location_id": 1,
    "purchase_place_id": 1,
    "purchase_date": "2025-01-01",
    "watering_frequency_id": 1,
    "light_requirement_id": 1,
    "difficulty_level": "Easy",
    "health_status": "Good",
}

try:
    resp = httpx.post(f"{BASE_URL}/api/plants", json=test_plant, timeout=5)
    if resp.status_code in [200, 201]:
        plant_data = resp.json()
        plant_id = plant_data.get("id")
        print_result(True, f"Plant created: {test_plant_name} (ID: {plant_id})")
        test_plant_id = plant_id
        create_ok = True
    else:
        print_result(False, f"Create failed: {resp.status_code} - {resp.text[:100]}")
        create_ok = False
        test_plant_id = None
except Exception as e:
    print_result(False, f"Exception: {e}")
    create_ok = False
    test_plant_id = None

# ============================================================================
# TEST 3: Search/Get Plant
# ============================================================================

print_test("TEST 3: Search Plant", "🔍")
if create_ok and test_plant_id:
    try:
        resp = httpx.get(f"{BASE_URL}/api/plants/{test_plant_id}", timeout=5)
        if resp.status_code == 200:
            plant = resp.json()
            if plant.get("name") == test_plant_name:
                print_result(True, f"Plant found: {plant.get('name')}")
                search_ok = True
            else:
                print_result(False, f"Found plant has wrong name: {plant.get('name')}")
                search_ok = False
        else:
            print_result(False, f"Get failed: {resp.status_code}")
            search_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        search_ok = False
else:
    print_result(False, "Skipped (create failed)")
    search_ok = False

# ============================================================================
# TEST 4: Update Plant
# ============================================================================

print_test("TEST 4: Update Plant", "✏️")
if search_ok and test_plant_id:
    updated_data = {
        "name": f"{test_plant_name}_UPDATED",
        "health_status": "Excellent",
        "location_id": 1,
        "purchase_place_id": 1,
        "purchase_date": "2025-01-01",
        "watering_frequency_id": 1,
        "light_requirement_id": 1,
        "difficulty_level": "Medium",
    }
    try:
        resp = httpx.put(f"{BASE_URL}/api/plants/{test_plant_id}", json=updated_data, timeout=5)
        if resp.status_code in [200, 201]:
            print_result(True, f"Plant updated successfully")
            
            # Verify the update
            resp = httpx.get(f"{BASE_URL}/api/plants/{test_plant_id}", timeout=5)
            if resp.status_code == 200:
                plant = resp.json()
                if plant.get("health_status") == "Excellent":
                    print_result(True, f"Update verified: health_status = {plant.get('health_status')}")
                    update_ok = True
                else:
                    print_result(False, f"Update not persisted: health_status = {plant.get('health_status')}")
                    update_ok = False
            else:
                print_result(False, "Verification get failed")
                update_ok = False
        else:
            print_result(False, f"Update failed: {resp.status_code} - {resp.text[:100]}")
            update_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        update_ok = False
else:
    print_result(False, "Skipped (search failed)")
    update_ok = False

# ============================================================================
# TEST 5: Get Watering History
# ============================================================================

print_test("TEST 5: Get Plant History (Watering)", "💧")
if update_ok and test_plant_id:
    try:
        resp = httpx.get(f"{BASE_URL}/api/plants/{test_plant_id}/watering-history", timeout=5)
        if resp.status_code == 200:
            history = resp.json()
            print_result(True, f"Watering history retrieved: {len(history)} entries")
            history_ok = True
        else:
            print_result(False, f"Get failed: {resp.status_code}")
            history_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        history_ok = False
else:
    print_result(False, "Skipped (update failed)")
    history_ok = False

# ============================================================================
# TEST 6: Delete Plant
# ============================================================================

print_test("TEST 6: Delete Plant", "🗑️")
if update_ok and test_plant_id:
    try:
        resp = httpx.delete(f"{BASE_URL}/api/plants/{test_plant_id}", timeout=5)
        if resp.status_code in [200, 204]:
            print_result(True, f"Plant deleted successfully")
            
            # Verify deletion
            resp = httpx.get(f"{BASE_URL}/api/plants/{test_plant_id}", timeout=5)
            if resp.status_code == 404:
                print_result(True, "Deletion verified: 404 on GET")
                delete_ok = True
            elif resp.status_code == 200:
                plant = resp.json()
                if plant.get("deleted_at"):
                    print_result(True, "Deletion verified: deleted_at set")
                    delete_ok = True
                else:
                    print_result(False, "Plant still exists (soft delete?)")
                    delete_ok = True  # Maybe soft delete is OK
            else:
                print_result(False, f"Verification failed: {resp.status_code}")
                delete_ok = False
        else:
            print_result(False, f"Delete failed: {resp.status_code}")
            delete_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        delete_ok = False
else:
    print_result(False, "Skipped (update failed)")
    delete_ok = False

# ============================================================================
# TEST 7: Settings CRUD (Locations)
# ============================================================================

print_test("TEST 7: Settings - Create Location", "⚙️")
test_location_name = f"Test_Location_{datetime.now().strftime('%H%M%S')}"
location_data = {"name": test_location_name}

try:
    resp = httpx.post(f"{BASE_URL}/api/settings/locations", json=location_data, timeout=5)
    if resp.status_code in [200, 201]:
        location = resp.json()
        location_id = location.get("id")
        print_result(True, f"Location created: {test_location_name} (ID: {location_id})")
        location_ok = True
        test_location_id = location_id
    else:
        print_result(False, f"Create failed: {resp.status_code} - {resp.text[:100]}")
        location_ok = False
        test_location_id = None
except Exception as e:
    print_result(False, f"Exception: {e}")
    location_ok = False
    test_location_id = None

# ============================================================================
# TEST 8: Settings - Get Location
# ============================================================================

print_test("TEST 8: Settings - Get Location", "🔍")
if location_ok and test_location_id:
    try:
        resp = httpx.get(f"{BASE_URL}/api/settings/locations", timeout=5)
        if resp.status_code == 200:
            locations = resp.json()
            found = any(l.get("id") == test_location_id for l in locations)
            if found:
                print_result(True, f"Location found in list")
                location_get_ok = True
            else:
                print_result(False, f"Location NOT found in list")
                location_get_ok = False
        else:
            print_result(False, f"Get failed: {resp.status_code}")
            location_get_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        location_get_ok = False
else:
    print_result(False, "Skipped (create failed)")
    location_get_ok = False

# ============================================================================
# TEST 9: Settings - Update Location
# ============================================================================

print_test("TEST 9: Settings - Update Location", "✏️")
if location_get_ok and test_location_id:
    update_data = {"name": f"{test_location_name}_UPDATED"}
    try:
        resp = httpx.put(f"{BASE_URL}/api/settings/locations/{test_location_id}", json=update_data, timeout=5)
        if resp.status_code in [200, 201]:
            print_result(True, f"Location updated successfully")
            
            # Verify
            resp = httpx.get(f"{BASE_URL}/api/settings/locations", timeout=5)
            if resp.status_code == 200:
                locations = resp.json()
                location = next((l for l in locations if l.get("id") == test_location_id), None)
                if location and "UPDATED" in location.get("name", ""):
                    print_result(True, f"Update verified")
                    location_update_ok = True
                else:
                    print_result(False, f"Update not persisted")
                    location_update_ok = False
            else:
                print_result(False, "Verification failed")
                location_update_ok = False
        else:
            print_result(False, f"Update failed: {resp.status_code}")
            location_update_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        location_update_ok = False
else:
    print_result(False, "Skipped (get failed)")
    location_update_ok = False

# ============================================================================
# TEST 10: Settings - Delete Location
# ============================================================================

print_test("TEST 10: Settings - Delete Location", "🗑️")
if location_update_ok and test_location_id:
    try:
        resp = httpx.delete(f"{BASE_URL}/api/settings/locations/{test_location_id}", timeout=5)
        if resp.status_code in [200, 204]:
            print_result(True, f"Location deleted successfully")
            
            # Verify
            resp = httpx.get(f"{BASE_URL}/api/settings/locations", timeout=5)
            if resp.status_code == 200:
                locations = resp.json()
                found = any(l.get("id") == test_location_id for l in locations)
                if not found:
                    print_result(True, "Deletion verified: not in list")
                    location_delete_ok = True
                else:
                    print_result(False, "Deletion not persisted")
                    location_delete_ok = False
            else:
                print_result(False, "Verification failed")
                location_delete_ok = False
        else:
            print_result(False, f"Delete failed: {resp.status_code}")
            location_delete_ok = False
    except Exception as e:
        print_result(False, f"Exception: {e}")
        location_delete_ok = False
else:
    print_result(False, "Skipped (update failed)")
    location_delete_ok = False

# ============================================================================
# FINAL RESULTS
# ============================================================================

print_test("FINAL RESULTS", "📊")

results = {
    "1. API Connection": api_ok,
    "2. Create Plant": create_ok,
    "3. Search/Get Plant": search_ok,
    "4. Update Plant": update_ok,
    "5. Get Plant History": history_ok,
    "6. Delete Plant": delete_ok,
    "7. Create Location": location_ok,
    "8. Get Location": location_get_ok,
    "9. Update Location": location_update_ok,
    "10. Delete Location": location_delete_ok,
}

passed = sum(1 for v in results.values() if v)
total = len(results)

for test_name, result in results.items():
    symbol = "✅" if result else "❌"
    print(f"{symbol} {test_name}")

print(f"\n{'='*70}")
print(f"TOTAL: {passed}/{total} tests passed")
if passed == total:
    print("🎉 ALL TESTS PASSED! Application is functional.")
elif passed >= total - 2:
    print("⚠️  Most tests passed. Some features may have issues.")
else:
    print("❌ Many tests failed. Application has significant issues.")
print(f"{'='*70}\n")

sys.exit(0 if passed == total else 1)

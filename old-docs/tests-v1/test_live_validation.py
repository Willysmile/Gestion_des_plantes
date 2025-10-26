"""
LIVE TEST - Phase 4B Frontend Validation
Tests the UI windows in real-time with actual user interactions
"""

import subprocess
import sys
import time
import httpx
import asyncio
from datetime import datetime

print("\n" + "="*70)
print("  🚀 PHASE 4B - LIVE FRONTEND TEST")
print("="*70)
print(f"  Started: {datetime.now().strftime('%H:%M:%S')}")
print("="*70 + "\n")

BASE_URL = "http://127.0.0.1:8000"


async def test_settings_window_api():
    """Test Settings Window API interactions"""
    print("\n📝 TEST 1: Settings Window - API Validation")
    print("-" * 70)
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Get all locations
            print("  ▶️  GET /settings/locations")
            resp = await client.get(f"{BASE_URL}/api/settings/locations")
            assert resp.status_code == 200
            locations = resp.json()
            print(f"     ✅ Returned {len(locations)} locations")
            
            # Create a location
            test_name = f"LiveTest_Loc_{int(time.time() * 1000) % 100000}"
            print(f"  ▶️  POST /settings/locations (name: {test_name})")
            resp = await client.post(
                f"{BASE_URL}/api/settings/locations",
                json={"name": test_name}
            )
            assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.text}"
            created = resp.json()
            loc_id = created["id"]
            print(f"     ✅ Created location ID {loc_id}")
            
            # Update it
            updated_name = f"Updated_{test_name}"
            print(f"  ▶️  PUT /settings/locations/{loc_id} (name: {updated_name})")
            resp = await client.put(
                f"{BASE_URL}/api/settings/locations/{loc_id}",
                json={"name": updated_name}
            )
            assert resp.status_code == 200
            updated = resp.json()
            assert updated["name"] == updated_name
            print(f"     ✅ Updated location successfully")
            
            # Delete it
            print(f"  ▶️  DELETE /settings/locations/{loc_id}")
            resp = await client.delete(f"{BASE_URL}/api/settings/locations/{loc_id}")
            assert resp.status_code == 204
            print(f"     ✅ Deleted location successfully")
            
            print("  ✅ Settings Window API - ALL PASS\n")
            return True
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}\n")
        return False


async def test_search_and_filter():
    """Test Search/Filter functionality"""
    print("\n🔍 TEST 2: Search & Filter - Validation")
    print("-" * 70)
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Get all plants
            print("  ▶️  GET /plants (all)")
            resp = await client.get(f"{BASE_URL}/api/plants")
            assert resp.status_code == 200
            all_plants = resp.json()
            print(f"     ✅ Returned {len(all_plants)} plants")
            
            # Search for a plant
            print("  ▶️  GET /plants/search?q=Rose")
            resp = await client.get(
                f"{BASE_URL}/api/plants/search",
                params={"q": "Rose"}
            )
            assert resp.status_code == 200
            search_results = resp.json()
            print(f"     ✅ Search returned {len(search_results)} results")
            
            # Get to-water count
            print("  ▶️  GET /plants/to-water?days_ago=0")
            resp = await client.get(
                f"{BASE_URL}/api/plants/to-water",
                params={"days_ago": 0}
            )
            assert resp.status_code == 200
            to_water = resp.json()
            print(f"     ✅ Plants to water: {len(to_water)}")
            
            # Get to-fertilize count
            print("  ▶️  GET /plants/to-fertilize?days_ago=0")
            resp = await client.get(
                f"{BASE_URL}/api/plants/to-fertilize",
                params={"days_ago": 0}
            )
            assert resp.status_code == 200
            to_fert = resp.json()
            print(f"     ✅ Plants to fertilize: {len(to_fert)}")
            
            print("  ✅ Search & Filter - ALL PASS\n")
            return True
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}\n")
        return False


async def test_dashboard_apis():
    """Test Dashboard APIs"""
    print("\n📊 TEST 3: Dashboard - KPIs & Tables Validation")
    print("-" * 70)
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Get dashboard stats
            print("  ▶️  GET /statistics/dashboard")
            resp = await client.get(f"{BASE_URL}/api/statistics/dashboard")
            assert resp.status_code == 200
            stats = resp.json()
            print(f"     ✅ KPIs returned:")
            for key, value in stats.items():
                print(f"        • {key}: {value}")
            
            # Get upcoming waterings
            print("  ▶️  GET /statistics/upcoming-waterings?days=7")
            resp = await client.get(
                f"{BASE_URL}/api/statistics/upcoming-waterings",
                params={"days": 7}
            )
            assert resp.status_code == 200
            waterings = resp.json()
            print(f"     ✅ Upcoming waterings: {len(waterings)} plants")
            
            # Get upcoming fertilizing
            print("  ▶️  GET /statistics/upcoming-fertilizing?days=7")
            resp = await client.get(
                f"{BASE_URL}/api/statistics/upcoming-fertilizing",
                params={"days": 7}
            )
            assert resp.status_code == 200
            ferts = resp.json()
            print(f"     ✅ Upcoming fertilizing: {len(ferts)} plants")
            
            print("  ✅ Dashboard APIs - ALL PASS\n")
            return True
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}\n")
        return False


async def main():
    """Run all live tests"""
    print("\n🧪 Running Live API Validation Tests...\n")
    
    results = []
    
    # Test 1: Settings Window
    result1 = await test_settings_window_api()
    results.append(("Settings Window API", result1))
    
    # Test 2: Search & Filter
    result2 = await test_search_and_filter()
    results.append(("Search & Filter", result2))
    
    # Test 3: Dashboard
    result3 = await test_dashboard_apis()
    results.append(("Dashboard APIs", result3))
    
    # Summary
    print("\n" + "="*70)
    print("  📋 TEST SUMMARY")
    print("="*70)
    
    all_pass = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:.<50} {status}")
        if not result:
            all_pass = False
    
    print("="*70)
    
    if all_pass:
        print("\n  🎉 ALL LIVE TESTS PASSED!")
        print("  Ready to test UI windows manually\n")
        print("  Next steps:")
        print("  1. Run: python -m frontend.app.windows.settings_window")
        print("  2. Run: python -m frontend.app.main")
        print("  3. Run: python -m frontend.app.windows.dashboard_window")
        print()
    else:
        print("\n  ❌ SOME TESTS FAILED - Check output above\n")
    
    return all_pass


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)

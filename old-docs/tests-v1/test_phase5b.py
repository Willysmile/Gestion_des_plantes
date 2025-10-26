#!/usr/bin/env python3
"""
Phase 5B Testing Script - Validates all functionality
"""

import asyncio
import httpx
import sys

API_URL = "http://127.0.0.1:8000"

async def test_api_endpoints():
    """Test all critical API endpoints"""
    print("\n" + "="*80)
    print("🧪 TESTING CRITICAL API ENDPOINTS")
    print("="*80)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Test 1: Get all plants
            print("\n✅ Test 1: GET /api/plants")
            try:
                resp = await client.get(f"{API_URL}/api/plants")
                if resp.status_code == 200:
                    plants = resp.json()
                    print(f"  ✓ Success! Found {len(plants)} plants")
                    tests_passed += 1
                else:
                    print(f"  ✗ Failed: {resp.status_code}")
                    tests_failed += 1
            except Exception as e:
                print(f"  ✗ Error: {e}")
                tests_failed += 1
            
            # Test 2: Get dashboard stats
            print("\n✅ Test 2: GET /api/statistics/dashboard")
            try:
                resp = await client.get(f"{API_URL}/api/statistics/dashboard")
                if resp.status_code == 200:
                    stats = resp.json()
                    print(f"  ✓ Success! Total plants: {stats.get('total_plants', 0)}")
                    tests_passed += 1
                else:
                    print(f"  ✗ Failed: {resp.status_code}")
                    tests_failed += 1
            except Exception as e:
                print(f"  ✗ Error: {e}")
                tests_failed += 1
            
            # Test 3: Get upcoming waterings
            print("\n✅ Test 3: GET /api/statistics/upcoming-waterings")
            try:
                resp = await client.get(f"{API_URL}/api/statistics/upcoming-waterings?days=7")
                if resp.status_code == 200:
                    waterings = resp.json()
                    print(f"  ✓ Success! Found {len(waterings)} plants to water")
                    tests_passed += 1
                else:
                    print(f"  ✗ Failed: {resp.status_code}")
                    tests_failed += 1
            except Exception as e:
                print(f"  ✗ Error: {e}")
                tests_failed += 1
            
            # Test 4: Get upcoming fertilizing
            print("\n✅ Test 4: GET /api/statistics/upcoming-fertilizing")
            try:
                resp = await client.get(f"{API_URL}/api/statistics/upcoming-fertilizing?days=7")
                if resp.status_code == 200:
                    ferts = resp.json()
                    print(f"  ✓ Success! Found {len(ferts)} plants to fertilize")
                    tests_passed += 1
                else:
                    print(f"  ✗ Failed: {resp.status_code}")
                    tests_failed += 1
            except Exception as e:
                print(f"  ✗ Error: {e}")
                tests_failed += 1
            
            # Test 5: Get all locations
            print("\n✅ Test 5: GET /api/settings/locations")
            try:
                resp = await client.get(f"{API_URL}/api/settings/locations")
                if resp.status_code == 200:
                    locs = resp.json()
                    print(f"  ✓ Success! Found {len(locs)} locations")
                    tests_passed += 1
                else:
                    print(f"  ✗ Failed: {resp.status_code}")
                    tests_failed += 1
            except Exception as e:
                print(f"  ✗ Error: {e}")
                tests_failed += 1
    
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        return False
    
    print("\n" + "="*80)
    print(f"📊 RESULTS: {tests_passed} passed, {tests_failed} failed")
    print("="*80)
    
    return tests_failed == 0

async def test_ui_imports():
    """Test if all UI modules import correctly"""
    print("\n" + "="*80)
    print("🧪 TESTING UI MODULE IMPORTS")
    print("="*80)
    
    try:
        # Add frontend to path so imports work
        import sys
        sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')
        
        print("\n✅ Test 1: Import dialogs module")
        from app.dialogs import create_add_plant_dialog
        print("  ✓ dialogs.py imports successfully")
        
        print("\n✅ Test 2: Import MainWindow")
        from app.main import MainWindow
        print("  ✓ main.py imports successfully")
        
        print("\n✅ Test 3: Import SettingsWindow")
        from app.windows.settings_window import SettingsWindow
        print("  ✓ settings_window.py imports successfully")
        
        print("\n✅ Test 4: Import DashboardWindow")
        from app.windows.dashboard_window import DashboardWindow
        print("  ✓ dashboard_window.py imports successfully")
        
        print("\n" + "="*80)
        print("✅ ALL UI IMPORTS SUCCESSFUL")
        print("="*80)
        return True
    
    except Exception as e:
        print(f"\n❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "🧪 PHASE 5B END-TO-END TESTING" + " "*28 + "║")
    print("║" + " "*20 + "Comprehensive Validation Suite" + " "*27 + "║")
    print("╚" + "="*78 + "╝")
    
    # Test API
    api_ok = await test_api_endpoints()
    
    # Test imports
    imports_ok = await test_ui_imports()
    
    print("\n" + "="*80)
    if api_ok and imports_ok:
        print("🎉 ALL TESTS PASSED - APPLICATION READY FOR PHASE 5B!")
    else:
        print("⚠️  SOME TESTS FAILED - CHECK ERRORS ABOVE")
    print("="*80 + "\n")
    
    return api_ok and imports_ok

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)

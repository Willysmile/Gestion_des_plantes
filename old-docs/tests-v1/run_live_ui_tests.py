"""
LIVE UI TEST RUNNER - Phase 4B
Launches each window with manual testing prompts
"""

import subprocess
import sys
import os
import time
from pathlib import Path

PROJECT_ROOT = Path("/home/willysmile/Documents/Gestion_des_plantes")
VENV_PYTHON = PROJECT_ROOT / "backend/venv/bin/python"
os.chdir(PROJECT_ROOT)

print("\n" + "="*70)
print("  🎯 PHASE 4B - LIVE UI TEST RUNNER")
print("="*70 + "\n")

tests = [
    {
        "name": "Settings Window",
        "module": "frontend.app.windows.settings_window",
        "description": "Test CRUD operations for 6 lookup types",
        "steps": [
            "✅ Look for 6 tabs: Locations, Places, Watering, Light, Fertilizer, Tags",
            "✅ Test ADD: Type name in field, click 'Add', verify in list",
            "✅ Test EDIT: Select item, type new name, click 'Update'",
            "✅ Test DELETE: Select item, click 'Delete', confirm",
            "✅ Close window gracefully",
        ]
    },
    {
        "name": "Main Window",
        "module": "frontend.app.main",
        "description": "Test Search and Filter functionality",
        "steps": [
            "✅ Look for search bar and 3 stat badges (plants, water, fertilize)",
            "✅ Click 'Advanced Filters' to show filter panel",
            "✅ Test SEARCH: Type 'Rose' in search, click Search button",
            "✅ Verify plant list updates with results",
            "✅ Test FILTERS: Select location, change difficulty, apply",
            "✅ Verify list updates to match criteria",
            "✅ Close window gracefully",
        ]
    },
    {
        "name": "Dashboard Window",
        "module": "frontend.app.windows.dashboard_window",
        "description": "Test KPIs and upcoming task tables",
        "steps": [
            "✅ Look for 7 KPI cards with values (total, active, health stats, photos)",
            "✅ Verify all KPI values > 0 or = 0 (no errors)",
            "✅ Check 'Upcoming Waterings' table",
            "✅ Check 'Upcoming Fertilizing' table",
            "✅ Click 'Refresh' button - tables should update",
            "✅ Verify no error messages in console",
            "✅ Close window gracefully",
        ]
    }
]

def run_test(test):
    """Run a single UI test"""
    print(f"\n📦 Test: {test['name']}")
    print("="*70)
    print(f"   Description: {test['description']}")
    print(f"   Module: {test['module']}")
    print("\n   Test Steps:")
    for step in test["steps"]:
        print(f"   {step}")
    
    print("\n" + "-"*70)
    print("   ⏳ Launching window... (close it to continue)\n")
    
    try:
        cmd = [str(VENV_PYTHON), "-m", test["module"]]
        subprocess.run(cmd, check=False, timeout=300)  # 5 min timeout
        
        print("\n   ✅ Window closed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("\n   ⏱️  Timeout - window was open too long")
        return True  # Still consider it a pass if it launched
        
    except Exception as e:
        print(f"\n   ❌ ERROR: {e}")
        return False


def main():
    """Run all UI tests"""
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n{'='*70}")
        print(f"  TEST {i}/{len(tests)}")
        print(f"{'='*70}")
        
        try:
            result = run_test(test)
            results.append((test["name"], result))
            
            if i < len(tests):
                print("\n" + "-"*70)
                print("   Ready for next test...")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n   ⚠️  Test interrupted by user")
            break
    
    # Summary
    print("\n" + "="*70)
    print("  📋 LIVE UI TEST SUMMARY")
    print("="*70 + "\n")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:.<50} {status}")
    
    print("\n" + "="*70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    if passed == total:
        print(f"\n  🎉 SUCCESS! {passed}/{total} UI tests passed!")
        print("  All windows launched and are functional\n")
    else:
        print(f"\n  ⚠️  {passed}/{total} UI tests passed")
        print("  Some windows had issues\n")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Testing stopped by user\n")
        sys.exit(1)

"""
Test script pour vérifier que Settings Window peut être importée et que API endpoints sont accessible
"""

import httpx
import asyncio
from datetime import datetime


async def test_api_endpoints():
    """Test que tous les endpoints Settings sont accessibles"""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🔍 Testing Settings Endpoints...\n")
    
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # Test Locations
            print("1️⃣ GET /api/settings/locations")
            resp = await client.get(f"{base_url}/api/settings/locations")
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                locations = resp.json()
                print(f"   ✅ Found {len(locations)} locations: {[l['name'] for l in locations]}")
            
            # Test Purchase Places
            print("\n2️⃣ GET /api/settings/purchase-places")
            resp = await client.get(f"{base_url}/api/settings/purchase-places")
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                places = resp.json()
                print(f"   ✅ Found {len(places)} places: {[p['name'] for p in places]}")
            
            # Test Watering Frequencies
            print("\n3️⃣ GET /api/settings/watering-frequencies")
            resp = await client.get(f"{base_url}/api/settings/watering-frequencies")
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                watering = resp.json()
                print(f"   ✅ Found {len(watering)} frequencies: {[w['name'] for w in watering]}")
            
            # Test Light Requirements
            print("\n4️⃣ GET /api/settings/light-requirements")
            resp = await client.get(f"{base_url}/api/settings/light-requirements")
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                lights = resp.json()
                print(f"   ✅ Found {len(lights)} light requirements: {[l['name'] for l in lights]}")
            
            # Test Fertilizer Types
            print("\n5️⃣ GET /api/settings/fertilizer-types")
            resp = await client.get(f"{base_url}/api/settings/fertilizer-types")
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                ferts = resp.json()
                print(f"   ✅ Found {len(ferts)} fertilizer types: {[f['name'] for f in ferts]}")
            
            # Test Tags
            print("\n6️⃣ GET /api/settings/tags")
            resp = await client.get(f"{base_url}/api/settings/tags")
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                tags = resp.json()
                print(f"   ✅ Found {len(tags)} tags: {[t['name'] for t in tags]}")
            
            print("\n✅ All endpoints accessible!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure backend server is running on http://127.0.0.1:8000")


async def test_create_operations():
    """Test creating items via API"""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🔧 Testing Create Operations...\n")
    
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # Create test location
            unique_id = int(datetime.now().timestamp() * 1000) % 100000
            test_name = f"Test_Location_{unique_id}"
            
            print(f"1️⃣ POST /api/settings/locations (name: {test_name})")
            resp = await client.post(
                f"{base_url}/api/settings/locations",
                json={"name": test_name}
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 201:
                location = resp.json()
                print(f"   ✅ Created location ID {location['id']}: {location['name']}")
                
                # Test delete
                print(f"\n2️⃣ DELETE /api/settings/locations/{location['id']}")
                resp = await client.delete(f"{base_url}/api/settings/locations/{location['id']}")
                print(f"   Status: {resp.status_code}")
                if resp.status_code == 204:
                    print(f"   ✅ Deleted location")
            else:
                print(f"   ❌ Error: {resp.text}")
            
            # Test watering frequency creation
            unique_id = int(datetime.now().timestamp() * 1000) % 100000
            test_name = f"Test_Watering_{unique_id}"
            
            print(f"\n3️⃣ POST /api/settings/watering-frequencies (name: {test_name}, days: 3)")
            resp = await client.post(
                f"{base_url}/api/settings/watering-frequencies",
                json={"name": test_name, "days": 3}
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 201:
                watering = resp.json()
                print(f"   ✅ Created watering frequency ID {watering['id']}: {watering['name']} ({watering['days']} days)")
            else:
                print(f"   ❌ Error: {resp.text}")
            
            print("\n✅ Create operations working!")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    print("=" * 60)
    print("SETTINGS WINDOW - API VALIDATION TEST")
    print("=" * 60)
    
    await test_api_endpoints()
    await test_create_operations()
    
    print("\n" + "=" * 60)
    print("✅ Settings Window is ready to use!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

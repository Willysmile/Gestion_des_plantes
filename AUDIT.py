#!/usr/bin/env python3
"""
AUDIT COMPLET - Vérification de tous les endpoints et fonctionnalités
"""

import httpx
import json
import sys
from pathlib import Path

def test_api():
    """Test tous les endpoints critiques"""
    print("\n" + "="*70)
    print("🔍 AUDIT API ENDPOINTS")
    print("="*70)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Health check
    print("\n1️⃣  HEALTH CHECK")
    try:
        resp = httpx.get(f"{base_url}/health", timeout=3)
        print(f"   ✅ Health: {resp.status_code} → {resp.json()}")
    except Exception as e:
        print(f"   ❌ Health: FAILED - {e}")
        return False
    
    # Test 2: Get plants
    print("\n2️⃣  GET /api/plants")
    try:
        resp = httpx.get(f"{base_url}/api/plants", timeout=3)
        data = resp.json()
        print(f"   ✅ Status: {resp.status_code}")
        print(f"   📊 Count: {len(data) if isinstance(data, list) else 'N/A'}")
        if isinstance(data, list) and len(data) > 0:
            print(f"   📝 First plant: {data[0].get('name', 'N/A')}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 3: Get specific plant history (endpoint réel)
    print("\n3️⃣  GET /api/plants/1/watering-history (ENDPOINT RÉEL)")
    try:
        resp = httpx.get(f"{base_url}/api/plants/1/watering-history", timeout=3)
        print(f"   ✅ Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   📊 Count: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"   ⚠️  Response: {resp.text[:100]}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 4: Test endpoint que le FRONTEND appelle (FAUX)
    print("\n4️⃣  GET /api/histories/watering?plant_id=1 (ENDPOINT FRONTEND - FAUX?)")
    try:
        resp = httpx.get(f"{base_url}/api/histories/watering?plant_id=1", timeout=3)
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text[:100]}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 5: Dashboard stats
    print("\n5️⃣  GET /api/statistics/dashboard")
    try:
        resp = httpx.get(f"{base_url}/api/statistics/dashboard", timeout=3)
        print(f"   ✅ Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   📊 Response keys: {list(data.keys())}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 6: Settings - Locations
    print("\n6️⃣  GET /api/settings/locations")
    try:
        resp = httpx.get(f"{base_url}/api/settings/locations", timeout=3)
        print(f"   ✅ Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   📊 Count: {len(data) if isinstance(data, list) else 'N/A'}")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    return True


def check_database():
    """Vérifier la structure de la BD"""
    print("\n" + "="*70)
    print("💾 AUDIT BASE DE DONNÉES")
    print("="*70)
    
    try:
        # Importer SQLAlchemy
        from backend.app.utils.db import engine, Base
        from backend.app.models.plant import Plant, Photo
        from backend.app.models.histories import WateringHistory
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Connexion BD réussie")
        print(f"📊 Tables ({len(tables)}):")
        for table in sorted(tables):
            print(f"   • {table}")
        
        # Check sample data
        from sqlalchemy.orm import Session
        session = Session(engine)
        plant_count = session.query(Plant).count()
        watering_count = session.query(WateringHistory).count()
        photo_count = session.query(Photo).count()
        session.close()
        
        print(f"\n📈 Sample data:")
        print(f"   • Plants: {plant_count}")
        print(f"   • Watering histories: {watering_count}")
        print(f"   • Photos: {photo_count}")
        
    except Exception as e:
        print(f"❌ BD check failed: {e}")


def check_frontend_code():
    """Vérifier les appels API dans le code frontend"""
    print("\n" + "="*70)
    print("📄 AUDIT CODE FRONTEND")
    print("="*70)
    
    main_py = Path("/home/willysmile/Documents/Gestion_des_plantes/frontend/app/main.py")
    
    with open(main_py) as f:
        content = f.read()
    
    # Chercher les appels API
    print("\n🔎 Appels API trouvés dans main.py:")
    
    import re
    api_calls = re.findall(r'f?["\']([^"\']*(?:/api/|http)[^"\']*)["\']', content)
    
    for api_call in set(api_calls):
        print(f"   • {api_call}")
    
    # Chercher les erreurs évidentes
    if "/api/histories/watering" in content:
        print(f"\n⚠️  PROBLÈME: Code appelle '/api/histories/watering'")
        print(f"   Mais endpoint réel est: '/{'{plant_id}'}/watering-history'")
    
    if "popup_warning" in content:
        print(f"⚠️  PROBLÈME: popup_warning utilisé (n'existe pas en PySimpleGUI 5.0.10)")


if __name__ == "__main__":
    print("\n🚀 DÉMARRAGE AUDIT COMPLET")
    print("="*70)
    
    # Attendre que l'API soit prête
    import time
    for i in range(5):
        try:
            httpx.get("http://127.0.0.1:8000/health", timeout=2)
            print("✅ API démarée et prête")
            break
        except:
            print(f"⏳ Attente API ({i+1}/5)...")
            time.sleep(1)
    
    test_api()
    check_database()
    check_frontend_code()
    
    print("\n" + "="*70)
    print("✅ AUDIT TERMINÉ")
    print("="*70 + "\n")

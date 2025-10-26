"""
Test MainWindow import and instantiation
"""

import sys
import os
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')

try:
    print("📝 Importing MainWindow...")
    from app.main import MainWindow
    print("✅ Import successful")
    
    print("\n📝 Creating MainWindow instance...")
    window = MainWindow()
    print("✅ Instance created successfully")
    
    print("\n📝 Window attributes:")
    print(f"   - Base URL: {window.api_base_url}")
    print(f"   - Window object: {window.window}")
    
    print("\n✅ ALL CHECKS PASSED - MainWindow is ready to use")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

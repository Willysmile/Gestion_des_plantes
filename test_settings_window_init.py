"""
Minimal SettingsWindow test - Check if it launches without errors
"""

import sys
import asyncio
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes')

try:
    print("📝 Importing SettingsWindow...")
    from frontend.app.windows.settings_window import SettingsWindow
    print("✅ Import successful")
    
    print("\n📝 Creating SettingsWindow instance...")
    window = SettingsWindow()
    print("✅ Instance created successfully")
    
    print("\n📝 Window attributes:")
    print(f"   - Base URL: {window.api_base_url}")
    print(f"   - Window object: {window.window}")
    
    print("\n✅ ALL CHECKS PASSED - Window is ready to use")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

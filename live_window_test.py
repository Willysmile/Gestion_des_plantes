#!/usr/bin/env python3
"""
LIVE TEST - Launch one window interactively
"""

import sys
sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')

print("\n" + "="*70)
print("  🎯 LIVE WINDOW TEST - Interactive")
print("="*70 + "\n")

print("Choose window to test:")
print("  1. SettingsWindow (6 tabs CRUD)")
print("  2. MainWindow (Search + Filters)")
print("  3. DashboardWindow (KPIs + Tables)")
print()

choice = input("Enter choice (1-3): ").strip()

try:
    if choice == "1":
        print("\n📝 Launching SettingsWindow...")
        from app.windows.settings_window import SettingsWindow
        window = SettingsWindow()
        window.show()
        
    elif choice == "2":
        print("\n🔍 Launching MainWindow...")
        from app.main import MainWindow
        window = MainWindow()
        window.show()
        
    elif choice == "3":
        print("\n📊 Launching DashboardWindow...")
        from app.windows.dashboard_window import DashboardWindow
        window = DashboardWindow()
        window.show()
        
    else:
        print("❌ Invalid choice")
        sys.exit(1)
        
    print("\n✅ Window closed successfully")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

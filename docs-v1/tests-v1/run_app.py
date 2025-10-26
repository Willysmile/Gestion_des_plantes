#!/usr/bin/env python3
"""
GESTION DES PLANTES - Application Launcher
Full application with MainWindow (search/filter) + DashboardWindow + SettingsWindow
"""

import sys
import asyncio
import PySimpleGUI as sg

sys.path.insert(0, '/home/willysmile/Documents/Gestion_des_plantes/frontend')

from app.main import MainWindow
from app.windows.dashboard_window import DashboardWindow
from app.windows.settings_window import SettingsWindow


def launch_app():
    """Launch the complete application"""
    print("\n" + "="*70)
    print("  🌿 GESTION DES PLANTES - Application")
    print("="*70 + "\n")
    
    try:
        # Configure PySimpleGUI theme
        sg.theme('DarkBlue3')
        sg.set_options(
            font=("Arial", 10),
            element_padding=(5, 5),
            button_element_size=(15, 1)
        )
        
        print("🚀 Starting application...\n")
        print("📝 Initializing MainWindow...")
        main_window = MainWindow()
        
        print("✅ MainWindow ready")
        print("\n" + "="*70)
        print("  🌱 Application launched!")
        print("="*70)
        print("\nFeatures:")
        print("  • 🔍 Search for plants")
        print("  • 📊 View dashboard with KPIs")
        print("  • ⚙️  Manage settings")
        print("  • 📈 Monitor plant status")
        print("\n" + "="*70 + "\n")
        
        # Show main window
        main_window.show()
        
        print("\n✅ Application closed gracefully\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    launch_app()

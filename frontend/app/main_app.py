"""
PHASE 6 - Single Window Tabbed Application
One window with 4 tabs: Plants, Dashboard, Settings, About
Simplified and stable architecture
"""

import PySimpleGUI as sg
import httpx
from typing import List, Dict, Optional

try:
    from app.dialogs import (
        create_add_plant_dialog,
        create_edit_plant_dialog,
        create_confirm_delete_dialog,
        show_plant_details
    )
except ImportError:
    from frontend.app.dialogs import (
        create_add_plant_dialog,
        create_edit_plant_dialog,
        create_confirm_delete_dialog,
        show_plant_details
    )

sg.theme('DarkBlue3')


class TabbedApp:
    """Single window application with tabbed interface"""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
        self.window = None
        self.plants_list = []
        
    # ==================== API CALLS ====================
    
    def get_all_plants(self) -> List[Dict]:
        """Get all plants from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/plants")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            sg.popup_error(f"❌ Error fetching plants:\n{e}")
            return []
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/statistics/dashboard")
                if resp.status_code == 200:
                    return resp.json()
                return {}
        except Exception as e:
            print(f"❌ Error fetching dashboard: {e}")
            return {}
    
    def get_upcoming_waterings(self) -> List[Dict]:
        """Get upcoming waterings"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/statistics/upcoming-waterings")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching waterings: {e}")
            return []
    
    def get_upcoming_fertilizing(self) -> List[Dict]:
        """Get upcoming fertilizing"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/statistics/upcoming-fertilizing")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching fertilizing: {e}")
            return []
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/locations")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching locations: {e}")
            return []
    
    def get_all_purchase_places(self) -> List[Dict]:
        """Get all purchase places"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/purchase_places")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching purchase places: {e}")
            return []
    
    def get_all_watering_frequencies(self) -> List[Dict]:
        """Get all watering frequencies"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/watering_frequencies")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching watering frequencies: {e}")
            return []
    
    def get_all_light_requirements(self) -> List[Dict]:
        """Get all light requirements"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/light_requirements")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching light requirements: {e}")
            return []
    
    def add_plant(self, data: Dict) -> bool:
        """Add new plant"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(f"{self.api_base_url}/api/plants", json=data)
                return resp.status_code == 201
        except Exception as e:
            sg.popup_error(f"❌ Error adding plant:\n{e}")
            return False
    
    def update_plant(self, plant_id: int, data: Dict) -> bool:
        """Update existing plant"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(f"{self.api_base_url}/api/plants/{plant_id}", json=data)
                return resp.status_code == 200
        except Exception as e:
            sg.popup_error(f"❌ Error updating plant:\n{e}")
            return False
    
    def delete_plant(self, plant_id: int) -> bool:
        """Delete plant"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(f"{self.api_base_url}/api/plants/{plant_id}")
                return resp.status_code == 200
        except Exception as e:
            sg.popup_error(f"❌ Error deleting plant:\n{e}")
            return False
    
    # ==================== UI LAYOUTS ====================
    
    def create_plants_tab(self) -> list:
        """Create Plants tab layout"""
        return [
            [sg.Text("🌱 PLANT MANAGER", font=("Arial", 14, "bold"))],
            [sg.Text("_" * 80)],
            
            # Search and Filter
            [
                sg.Text("Search:"),
                sg.InputText(key="-SEARCH-", size=(20, 1)),
                sg.Button("🔍 Search", size=(10, 1)),
                sg.Button("📋 All Plants", size=(10, 1)),
            ],
            
            [sg.Text("_" * 80)],
            
            # Plant List
            [
                sg.Listbox(
                    values=[],
                    size=(80, 15),
                    key="-PLANT-LIST-",
                    enable_events=True,
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE
                )
            ],
            
            [sg.Text("_" * 80)],
            
            # Action Buttons
            [
                sg.Button("➕ Add Plant", size=(12, 1)),
                sg.Button("✏️ Edit", size=(12, 1)),
                sg.Button("🗑️ Delete", size=(12, 1)),
                sg.Button("👁️ View Details", size=(12, 1)),
            ]
        ]
    
    def create_dashboard_tab(self) -> list:
        """Create Dashboard tab layout"""
        return [
            [sg.Text("📊 DASHBOARD", font=("Arial", 14, "bold"))],
            [sg.Text("_" * 80)],
            
            # KPI Cards
            [
                sg.Frame("", [
                    [
                        sg.Column([[sg.Text("Total Plants"), sg.Text("0", key="-KPI-TOTAL-", font=("Arial", 16, "bold"))]]),
                        sg.Column([[sg.Text("Active"), sg.Text("0", key="-KPI-ACTIVE-", font=("Arial", 16, "bold"))]]),
                        sg.Column([[sg.Text("Archived"), sg.Text("0", key="-KPI-ARCHIVED-", font=("Arial", 16, "bold"))]]),
                        sg.Column([[sg.Text("Excellent"), sg.Text("0", key="-KPI-EXCELLENT-", font=("Arial", 16, "bold"))]]),
                    ]
                ], border_width=0)
            ],
            
            [sg.Text("_" * 80)],
            
            # Upcoming Waterings
            [sg.Text("💧 Upcoming Waterings (7 days)", font=("Arial", 12, "bold"))],
            [
                sg.Listbox(
                    values=[],
                    size=(80, 5),
                    key="-WATERINGS-LIST-",
                    disabled=True
                )
            ],
            
            [sg.Text("_" * 80)],
            
            # Upcoming Fertilizing
            [sg.Text("🧪 Upcoming Fertilizing (7 days)", font=("Arial", 12, "bold"))],
            [
                sg.Listbox(
                    values=[],
                    size=(80, 5),
                    key="-FERTILIZING-LIST-",
                    disabled=True
                )
            ],
            
            [sg.Text("_" * 80)],
            
            [sg.Button("🔄 Refresh", size=(12, 1))]
        ]
    
    def create_settings_tab(self) -> list:
        """Create Settings tab layout"""
        return [
            [sg.Text("⚙️ SETTINGS", font=("Arial", 14, "bold"))],
            [sg.Text("_" * 80)],
            [sg.Text("Settings management coming soon...")],
            [sg.Text("Manage locations, purchase places, watering frequencies, etc.")],
        ]
    
    def create_about_tab(self) -> list:
        """Create About tab layout"""
        return [
            [sg.Text("ℹ️ ABOUT", font=("Arial", 14, "bold"))],
            [sg.Text("_" * 80)],
            [sg.Text("🌿 Gestion des Plantes", font=("Arial", 12, "bold"))],
            [sg.Text("Version: 1.0 - Phase 6")],
            [sg.Text("")],
            [sg.Text("A beautiful plant management application")],
            [sg.Text("with dashboard, statistics, and settings.")],
            [sg.Text("")],
            [sg.Text("Backend: FastAPI")],
            [sg.Text("Frontend: PySimpleGUI 5.0.10")],
            [sg.Text("Database: SQLite")],
        ]
    
    def create_window(self):
        """Create main window with tabs"""
        
        tab_group = [
            [
                sg.Tab("🌱 Plants", self.create_plants_tab()),
                sg.Tab("📊 Dashboard", self.create_dashboard_tab()),
                sg.Tab("⚙️ Settings", self.create_settings_tab()),
                sg.Tab("ℹ️ About", self.create_about_tab()),
            ]
        ]
        
        layout = [
            [sg.TabGroup(tab_group, key="-TAB-GROUP-", enable_events=True)],
            [sg.Text("_" * 80)],
            [sg.Button("❌ Exit", size=(12, 1))]
        ]
        
        self.window = sg.Window(
            "🌿 Gestion des Plantes - Plant Manager",
            layout,
            size=(900, 700),
            finalize=True
        )
    
    # ==================== EVENT HANDLERS ====================
    
    def load_plants_display(self):
        """Load and display all plants"""
        self.plants_list = self.get_all_plants()
        plant_display = [
            f"🌱 {p['name']} - {p['location_id']} (Health: {p['health_status']})"
            for p in self.plants_list
        ]
        self.window["-PLANT-LIST-"].update(plant_display)
    
    def load_dashboard(self):
        """Load dashboard data"""
        stats = self.get_dashboard_stats()
        waterings = self.get_upcoming_waterings()
        fertilizing = self.get_upcoming_fertilizing()
        
        # Update KPI cards
        self.window["-KPI-TOTAL-"].update(str(stats.get("total_plants", 0)))
        self.window["-KPI-ACTIVE-"].update(str(stats.get("active_plants", 0)))
        self.window["-KPI-ARCHIVED-"].update(str(stats.get("archived_plants", 0)))
        self.window["-KPI-EXCELLENT-"].update(str(stats.get("excellent_health", 0)))
        
        # Update tables
        watering_display = [
            f"🌱 {w['plant_name']} - {w['next_watering_date']}"
            for w in waterings[:7]
        ]
        self.window["-WATERINGS-LIST-"].update(watering_display)
        
        fertilizing_display = [
            f"🧪 {f['plant_name']} - {f['next_fertilizing_date']}"
            for f in fertilizing[:7]
        ]
        self.window["-FERTILIZING-LIST-"].update(fertilizing_display)
    
    def run(self):
        """Main application loop"""
        self.create_window()
        self.load_plants_display()
        self.load_dashboard()
        
        while True:
            event, values = self.window.read()
            
            if event == sg.WINDOW_CLOSED or event == "❌ Exit":
                break
            
            # ========== PLANTS TAB ==========
            elif event == "🔍 Search":
                search_query = values.get("-SEARCH-", "").strip()
                if search_query:
                    filtered = [p for p in self.plants_list 
                               if search_query.lower() in p['name'].lower()]
                    plant_display = [
                        f"🌱 {p['name']} - {p['location_id']} (Health: {p['health_status']})"
                        for p in filtered
                    ]
                    self.window["-PLANT-LIST-"].update(plant_display)
            
            elif event == "📋 All Plants":
                self.load_plants_display()
            
            elif event == "➕ Add Plant":
                locations = self.get_all_locations()
                location_names = [l["name"] for l in locations]
                places = self.get_all_purchase_places()
                place_names = [p["name"] for p in places]
                frequencies = self.get_all_watering_frequencies()
                freq_names = [f["name"] for f in frequencies]
                light_reqs = self.get_all_light_requirements()
                light_names = [l["name"] for l in light_reqs]
                
                data = create_add_plant_dialog(location_names, place_names, freq_names, light_names)
                if data:
                    if self.add_plant(data):
                        sg.popup_ok("✅ Plant added successfully!")
                        self.load_plants_display()
                    else:
                        sg.popup_error("❌ Failed to add plant")
            
            elif event == "✏️ Edit":
                selected_indices = self.window["-PLANT-LIST-"].get_indexes()
                if not selected_indices:
                    sg.popup_warning("⚠️ Please select a plant first")
                    continue
                
                plant_index = selected_indices[0]
                if plant_index < len(self.plants_list):
                    selected_plant = self.plants_list[plant_index]
                    locations = self.get_all_locations()
                    location_names = [l["name"] for l in locations]
                    places = self.get_all_purchase_places()
                    place_names = [p["name"] for p in places]
                    frequencies = self.get_all_watering_frequencies()
                    freq_names = [f["name"] for f in frequencies]
                    light_reqs = self.get_all_light_requirements()
                    light_names = [l["name"] for l in light_reqs]
                    
                    updated_data = create_edit_plant_dialog(selected_plant, location_names, place_names, freq_names, light_names)
                    if updated_data:
                        if self.update_plant(selected_plant["id"], updated_data):
                            sg.popup_ok("✅ Plant updated successfully!")
                            self.load_plants_display()
            
            elif event == "🗑️ Delete":
                selected_indices = self.window["-PLANT-LIST-"].get_indexes()
                if not selected_indices:
                    sg.popup_warning("⚠️ Please select a plant first")
                    continue
                
                plant_index = selected_indices[0]
                if plant_index < len(self.plants_list):
                    selected_plant = self.plants_list[plant_index]
                    if create_confirm_delete_dialog(selected_plant["name"]):
                        if self.delete_plant(selected_plant["id"]):
                            sg.popup_ok("✅ Plant deleted successfully!")
                            self.load_plants_display()
            
            elif event == "👁️ View Details":
                selected_indices = self.window["-PLANT-LIST-"].get_indexes()
                if not selected_indices:
                    sg.popup_warning("⚠️ Please select a plant first")
                    continue
                
                plant_index = selected_indices[0]
                if plant_index < len(self.plants_list):
                    selected_plant = self.plants_list[plant_index]
                    show_plant_details(selected_plant, [], [])
            
            # ========== DASHBOARD TAB ==========
            elif event == "🔄 Refresh":
                self.load_dashboard()
        
        self.window.close()


if __name__ == "__main__":
    app = TabbedApp()
    app.run()

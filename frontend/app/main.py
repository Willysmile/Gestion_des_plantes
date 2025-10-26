"""
Main Window - Plant Manager with Search, Filter, and Quick Badges
Phase 5A - Event Handlers & CRUD Operations
"""

import PySimpleGUI as sg
import httpx
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from app.api_client import api_client
from app.dialogs import (
    create_add_plant_dialog,
    create_edit_plant_dialog,
    create_confirm_delete_dialog,
    show_plant_details
)

sg.theme('DarkBlue3')


class MainWindow:
    """Main window for plant management with search and filter capabilities"""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
        self.window = None
        self.plants_list = []
        self.filter_visible = False
        
    def get_all_plants(self) -> List[Dict]:
        """Get all plants"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/plants")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching plants: {e}")
            return []
    
    def search_plants(self, query: str) -> List[Dict]:
        """Search plants by query"""
        if not query:
            return self.get_all_plants()
        
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"{self.api_base_url}/api/plants/search",
                    params={"q": query}
                )
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error searching plants: {e}")
            return []
    
    def filter_plants(self, location_id: Optional[int] = None, 
                          difficulty: Optional[str] = None,
                          health_status: Optional[str] = None) -> List[Dict]:
        """Filter plants by criteria"""
        try:
            with httpx.Client(timeout=10) as client:
                params = {}
                if location_id:
                    params["location_id"] = location_id
                if difficulty:
                    params["difficulty"] = difficulty
                if health_status:
                    params["health_status"] = health_status
                
                resp = client.get(
                    f"{self.api_base_url}/api/plants/filter",
                    params=params if params else None
                )
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error filtering plants: {e}")
            return []
    
    def get_to_water_count(self) -> int:
        """Get count of plants to water"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"{self.api_base_url}/api/plants/to-water",
                    params={"days_ago": 0}
                )
                if resp.status_code == 200:
                    return len(resp.json())
                return 0
        except Exception as e:
            return 0
    
    def get_to_fertilize_count(self) -> int:
        """Get count of plants to fertilize"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"{self.api_base_url}/api/plants/to-fertilize",
                    params={"days_ago": 0}
                )
                if resp.status_code == 200:
                    return len(resp.json())
                return 0
        except Exception as e:
            return 0
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations for filter dropdown"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/locations")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
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
            return []
    
    def create_plant(self, plant_data: Dict) -> bool:
        """Create a new plant"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/plants",
                    json=plant_data
                )
                if resp.status_code in [200, 201]:
                    print(f"✅ Plant '{plant_data.get('name')}' created successfully")
                    return True
                else:
                    error_msg = resp.text[:200] if resp.text else "Unknown error"
                    print(f"❌ Create failed ({resp.status_code}): {error_msg}")
                    sg.popup_error(f"❌ Error creating plant:\n{error_msg}")
                    return False
        except Exception as e:
            print(f"❌ Exception creating plant: {str(e)}")
            sg.popup_error(f"❌ Error creating plant:\n{str(e)}")
            return False
    
    def update_plant(self, plant_id: int, plant_data: Dict) -> bool:
        """Update an existing plant"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(
                    f"{self.api_base_url}/api/plants/{plant_id}",
                    json=plant_data
                )
                if resp.status_code in [200, 201]:
                    print(f"✅ Plant '{plant_data.get('name')}' updated successfully")
                    return True
                else:
                    error_msg = resp.text[:200] if resp.text else "Unknown error"
                    print(f"❌ Update failed ({resp.status_code}): {error_msg}")
                    sg.popup_error(f"❌ Error updating plant:\n{error_msg}")
                    return False
        except Exception as e:
            print(f"❌ Exception updating plant: {str(e)}")
            sg.popup_error(f"❌ Error updating plant:\n{str(e)}")
            return False
    
    def delete_plant(self, plant_id: int) -> bool:
        """Delete a plant"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/plants/{plant_id}"
                )
                if resp.status_code in [200, 204]:
                    print(f"✅ Plant {plant_id} deleted successfully")
                    return True
                else:
                    error_msg = resp.text[:200] if resp.text else "Unknown error"
                    print(f"❌ Delete failed ({resp.status_code}): {error_msg}")
                    sg.popup_error(f"❌ Error deleting plant:\n{error_msg}")
                    return False
        except Exception as e:
            print(f"❌ Exception deleting plant: {str(e)}")
            sg.popup_error(f"❌ Error deleting plant:\n{str(e)}")
            return False
    
    def get_plant_watering_history(self, plant_id: int) -> List[Dict]:
        """Get watering history for a plant"""
        try:
            with httpx.Client(timeout=10) as client:
                # FIXED: Correct endpoint path
                resp = client.get(f"{self.api_base_url}/api/plants/{plant_id}/watering-history")
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 404:
                    print(f"⚠️  No watering history found for plant {plant_id}")
                    return []
                else:
                    print(f"❌ API Error {resp.status_code}: {resp.text[:100]}")
                    return []
        except Exception as e:
            print(f"❌ Error loading watering history: {str(e)}")
            return []
    
    def get_plant_fertilizing_history(self, plant_id: int) -> List[Dict]:
        """Get fertilizing history for a plant"""
        try:
            with httpx.Client(timeout=10) as client:
                # FIXED: Correct endpoint path
                resp = client.get(f"{self.api_base_url}/api/plants/{plant_id}/fertilizing-history")
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 404:
                    print(f"⚠️  No fertilizing history found for plant {plant_id}")
                    return []
                else:
                    print(f"❌ API Error {resp.status_code}: {resp.text[:100]}")
                    return []
        except Exception as e:
            print(f"❌ Error loading fertilizing history: {str(e)}")
            return []
    
    def build_layout(self) -> List:
        """Build main window layout"""
        layout = [
            [sg.Text("🌱 PLANT MANAGER - v2.0", font=("Arial", 14, "bold"))],
            [
                sg.Text("Search:"),
                sg.InputText(size=(30, 1), key="-SEARCH_INPUT-"),
                sg.Button("🔍 Search", key="-SEARCH_BTN-"),
                sg.Button("Advanced ▼", key="-ADVANCED_BTN-"),
            ],
            [
                sg.Column([
                    [sg.Text("Location:"), sg.Combo([], key="-FILTER_LOC-", size=(20, 1))],
                    [sg.Text("Difficulty:"), sg.Combo(["Easy", "Medium", "Difficult"], key="-FILTER_DIFF-", size=(20, 1))],
                    [sg.Text("Health:"), sg.Combo(["Excellent", "Good", "Poor"], key="-FILTER_HEALTH-", size=(20, 1))],
                    [sg.Button("Apply Filters"), sg.Button("Reset Filters")],
                ], key="-FILTER_COLUMN-", visible=False)
            ],
            [
                sg.Text("📊 Quick Stats:", font=("Arial", 10, "bold")),
                sg.Text("🌱 ?", key="-BADGE_TOTAL-", size=(8, 1)),
                sg.Text("⏳ ?", key="-BADGE_WATER-", size=(8, 1)),
                sg.Text("🧪 ?", key="-BADGE_FERT-", size=(10, 1)),
            ],
            [sg.Text("_" * 80)],
            [sg.Text("Plant List", font=("Arial", 12, "bold"))],
            [sg.Listbox([], size=(60, 15), key="-PLANTS_LIST-", enable_events=True)],
            [
                sg.Button("👁️ View Details", key="-VIEW_PLANT_BTN-"),
                sg.Button("➕ Add Plant", key="-ADD_PLANT_BTN-"),
                sg.Button("✏️ Edit Plant", key="-EDIT_PLANT_BTN-"),
                sg.Button("🗑️ Delete Plant", key="-DELETE_PLANT_BTN-"),
            ],
            [
                sg.Button("⚙️ Settings", key="-SETTINGS_BTN-"),
                sg.Button("📊 Dashboard", key="-DASHBOARD_BTN-"),
                sg.Button("🔄 Refresh", key="-REFRESH_BTN-"),
                sg.Button("❌ Exit", key="-EXIT_BTN-"),
            ],
        ]
        return layout
    
    def show(self):
        """Show window and handle events - fully synchronous"""
        layout = self.build_layout()
        self.window = sg.Window("🌱 Plant Manager - v2.0", layout, finalize=True)
        
        # Load initial data on first show
        try:
            self._load_initial_data()
        except Exception as e:
            sg.popup_error(f"❌ Failed to load initial data:\n{e}")
        
        while True:
            event, values = self.window.read(timeout=500)
            
            if event == sg.WINDOW_CLOSED or event == "-EXIT_BTN-":
                break
            
            if event == "__TIMEOUT__":
                continue
            
            # Handle events synchronously
            try:
                self._handle_event(event, values)
            except Exception as e:
                print(f"Error handling event {event}: {e}")
                if str(e):
                    sg.popup_error(f"❌ Error: {str(e)[:100]}")
        
        if self.window:
            self.window.close()
    
    def _load_initial_data(self):
        """Load initial data"""
        try:
            locations = self.get_all_locations()
            location_names = [l["name"] for l in locations] if locations else []
            self.window["-FILTER_LOC-"].update(values=location_names)
        except Exception as e:
            print(f"❌ Error loading locations: {e}")
        
        try:
            self.plants_list = self.get_all_plants()
            self._update_plants_display()
        except Exception as e:
            print(f"❌ Error loading plants: {e}")
            self.plants_list = []
            self._update_plants_display()
        
        try:
            self._update_badges()
        except Exception as e:
            print(f"❌ Error updating badges: {e}")
    
    def _update_badges(self):
        """Update badge counts"""
        try:
            total = len(self.plants_list)
            to_water = self.get_to_water_count()
            to_fert = self.get_to_fertilize_count()
            
            self.window["-BADGE_TOTAL-"].update(f"🌱 {total}")
            self.window["-BADGE_WATER-"].update(f"⏳ {to_water}")
            self.window["-BADGE_FERT-"].update(f"🧪 {to_fert}")
        except Exception as e:
            print(f"❌ Error updating badges: {e}")
    
    def _update_plants_display(self):
        """Update plants list display"""
        if not self.plants_list:
            self.window["-PLANTS_LIST-"].update([])
            return
        
        display_items = [
            f"[{p['id']}] {p['name']} - {p.get('health_status', '?')}"
            for p in self.plants_list
        ]
        self.window["-PLANTS_LIST-"].update(display_items)
    
    def _handle_event(self, event: str, values: Dict):
        """Handle window events"""
        if event == "-SEARCH_BTN-":
            query = values["-SEARCH_INPUT-"]
            self.plants_list = self.search_plants(query)
            self._update_plants_display()
            self._update_badges()
        
        elif event == "-ADVANCED_BTN-":
            self.filter_visible = not self.filter_visible
            self.window["-FILTER_COLUMN-"].update(visible=self.filter_visible)
        
        elif event == "Apply Filters":
            loc = values["-FILTER_LOC-"] if values["-FILTER_LOC-"] else None
            diff = values["-FILTER_DIFF-"] if values["-FILTER_DIFF-"] else None
            health = values["-FILTER_HEALTH-"] if values["-FILTER_HEALTH-"] else None
            self.plants_list = self.filter_plants(loc, diff, health)
            self._update_plants_display()
            self._update_badges()
        
        elif event == "Reset Filters":
            self.window["-FILTER_LOC-"].update("")
            self.window["-FILTER_DIFF-"].update("")
            self.window["-FILTER_HEALTH-"].update("")
            self.plants_list = self.get_all_plants()
            self._update_plants_display()
            self._update_badges()
        
        elif event == "-REFRESH_BTN-":
            self.plants_list = self.get_all_plants()
            self._update_plants_display()
            self._update_badges()
        
        # ===== VIEW PLANT DETAILS =====
        elif event == "-VIEW_PLANT_BTN-" or event == "-PLANTS_LIST-":
            selected_indices = self.window["-PLANTS_LIST-"].get_indexes()
            if not selected_indices:
                sg.popup_ok("⚠️ Please select a plant to view")
                return
            
            plant_index = selected_indices[0]
            if plant_index < len(self.plants_list):
                selected_plant = self.plants_list[plant_index]
                
                # Load plant history
                watering_history = self.get_plant_watering_history(selected_plant["id"])
                fertilizing_history = self.get_plant_fertilizing_history(selected_plant["id"])
                
                action = show_plant_details(selected_plant, watering_history, fertilizing_history)
                
                if action == "edit":
                    # Open edit dialog
                    locations = self.get_all_locations()
                    location_names = [l["name"] for l in locations]
                    updated_data = create_edit_plant_dialog(selected_plant, location_names)
                    if updated_data:
                        if self.update_plant(selected_plant["id"], updated_data):
                            sg.popup_ok("✅ Plant updated successfully!")
                            self.plants_list = self.get_all_plants()
                            self._update_plants_display()
                            self._update_badges()
                        else:
                            sg.popup_error("❌ Failed to update plant")
                
                elif action == "delete":
                    if create_confirm_delete_dialog(selected_plant["name"]):
                        if self.delete_plant(selected_plant["id"]):
                            sg.popup_ok("✅ Plant deleted successfully!")
                            self.plants_list = self.get_all_plants()
                            self._update_plants_display()
                            self._update_badges()
                        else:
                            sg.popup_error("❌ Failed to delete plant")
        
        # ===== NEW PLANT CRUD HANDLERS =====
        elif event == "-ADD_PLANT_BTN-":
            locations = self.get_all_locations()
            location_names = [l["name"] for l in locations]
            places = self.get_all_purchase_places()
            place_names = [p["name"] for p in places]
            frequencies = self.get_all_watering_frequencies()
            freq_names = [f["name"] for f in frequencies]
            light_reqs = self.get_all_light_requirements()
            light_names = [l["name"] for l in light_reqs]
            
            plant_data = create_add_plant_dialog(location_names, place_names, freq_names, light_names)
            if plant_data:
                if self.create_plant(plant_data):
                    sg.popup_ok("✅ Plant added successfully!")
                    self.plants_list = self.get_all_plants()
                    self._update_plants_display()
                    self._update_badges()
                else:
                    sg.popup_error("❌ Failed to add plant")
        
        elif event == "-EDIT_PLANT_BTN-":
            if not self.plants_list:
                sg.popup_error("❌ No plants to edit")
                return
            
            # Create simple selection dialog
            plant_choices = [f"[{p['id']}] {p['name']}" for p in self.plants_list]
            popup_layout = [
                [sg.Text("Select plant to edit:")],
                [sg.Listbox(plant_choices, size=(30, 5), key="-PLANT_CHOICE-", default_values=[plant_choices[0]] if plant_choices else [])],
                [sg.Button("Edit"), sg.Button("Cancel")]
            ]
            popup_window = sg.Window("Select Plant", popup_layout)
            p_event, p_values = popup_window.read()
            popup_window.close()
            
            if p_event == "Edit" and p_values["-PLANT_CHOICE-"]:
                selected = p_values["-PLANT_CHOICE-"][0]
                # Get selected plant
                plant_idx = plant_choices.index(selected)
                plant = self.plants_list[plant_idx]
                
                locations = self.get_all_locations()
                location_names = [l["name"] for l in locations]
                places = self.get_all_purchase_places()
                place_names = [p["name"] for p in places]
                frequencies = self.get_all_watering_frequencies()
                freq_names = [f["name"] for f in frequencies]
                light_reqs = self.get_all_light_requirements()
                light_names = [l["name"] for l in light_reqs]
                
                updated_data = create_edit_plant_dialog(plant, location_names, place_names, freq_names, light_names)
                if updated_data:
                    if self.update_plant(plant['id'], updated_data):
                        sg.popup_ok("✅ Plant updated successfully!")
                        self.plants_list = self.get_all_plants()
                        self._update_plants_display()
                        self._update_badges()
                    else:
                        sg.popup_error("❌ Failed to update plant")
        
        elif event == "-DELETE_PLANT_BTN-":
            if not self.plants_list:
                sg.popup_error("❌ No plants to delete")
                return
            
            # Create simple selection dialog
            plant_choices = [f"[{p['id']}] {p['name']}" for p in self.plants_list]
            popup_layout = [
                [sg.Text("Select plant to delete:")],
                [sg.Listbox(plant_choices, size=(30, 5), key="-PLANT_CHOICE-", default_values=[plant_choices[0]] if plant_choices else [])],
                [sg.Button("Delete"), sg.Button("Cancel")]
            ]
            popup_window = sg.Window("Delete Plant", popup_layout)
            p_event, p_values = popup_window.read()
            popup_window.close()
            
            if p_event == "Delete" and p_values["-PLANT_CHOICE-"]:
                selected = p_values["-PLANT_CHOICE-"][0]
                # Get selected plant
                plant_idx = plant_choices.index(selected)
                plant = self.plants_list[plant_idx]
                
                if create_confirm_delete_dialog(plant['name']):
                    if self.delete_plant(plant['id']):
                        sg.popup_ok("✅ Plant deleted successfully!")
                        self.plants_list = self.get_all_plants()
                        self._update_plants_display()
                        self._update_badges()
                    else:
                        sg.popup_error("❌ Failed to delete plant")
        
        elif event == "-SETTINGS_BTN-":
            try:
                from app.windows.settings_window import SettingsWindow
                settings = SettingsWindow(self.api_base_url)
                settings.show()
                # Refresh after settings window closes
                self.plants_list = self.get_all_plants()
                self._update_plants_display()
                self._update_badges()
            except Exception as e:
                sg.popup_error(f"❌ Error opening settings: {str(e)}")
        
        elif event == "-DASHBOARD_BTN-":
            try:
                from app.windows.dashboard_window import DashboardWindow
                dashboard = DashboardWindow(self.api_base_url)
                dashboard.show()
            except Exception as e:
                sg.popup_error(f"❌ Error opening dashboard: {str(e)}")


def create_main_window():
    """Create and show main window"""
    window = MainWindow()
    window.show()


def main():
    create_main_window()


if __name__ == '__main__':
    main()

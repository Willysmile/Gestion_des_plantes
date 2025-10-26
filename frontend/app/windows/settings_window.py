"""
Settings Window - Manage lookup tables (locations, places, watering, light, fertilizer, tags)
Phase 4B - Frontend Settings UI
"""

import PySimpleGUI as sg
import httpx
from typing import List, Dict, Optional

import PySimpleGUI as sg
import httpx
import asyncio
from datetime import datetime
from typing import List, Dict, Optional


class SettingsWindow:
    """Settings window for managing lookup data (Locations, Places, Watering, etc.)"""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
        self.window = None
        self.setup_gui_theme()
        
    def setup_gui_theme(self):
        """Configure PySimpleGUI theme"""
        sg.theme('DarkBlue3')
        
    def get_all_locations(self) -> List[Dict]:
        """Get all locations from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/locations")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching locations: {e}")
            return []
    
    def create_location(self, name: str) -> Optional[Dict]:
        """Create new location"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/settings/locations",
                    json={"name": name}
                )
                if resp.status_code == 201:
                    return resp.json()
                else:
                    print(f"❌ Error creating location: {resp.status_code} - {resp.text}")
                    return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def update_location(self, location_id: int, name: str) -> Optional[Dict]:
        """Update location"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(
                    f"{self.api_base_url}/api/settings/locations/{location_id}",
                    json={"name": name}
                )
                if resp.status_code == 200:
                    return resp.json()
                else:
                    print(f"❌ Error updating location: {resp.status_code} - {resp.text}")
                    return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_location(self, location_id: int) -> bool:
        """Delete location"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/settings/locations/{location_id}"
                )
                if resp.status_code == 204:
                    return True
                else:
                    print(f"❌ Error deleting location: {resp.status_code} - {resp.text}")
                    return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    # PURCHASE PLACES
    def get_all_purchase_places(self) -> List[Dict]:
        """Get all purchase places from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/purchase-places")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching purchase places: {e}")
            return []
    
    def create_purchase_place(self, name: str) -> Optional[Dict]:
        """Create new purchase place"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/settings/purchase-places",
                    json={"name": name}
                )
                if resp.status_code == 201:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def update_purchase_place(self, place_id: int, name: str) -> Optional[Dict]:
        """Update purchase place"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(
                    f"{self.api_base_url}/api/settings/purchase-places/{place_id}",
                    json={"name": name}
                )
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_purchase_place(self, place_id: int) -> bool:
        """Delete purchase place"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/settings/purchase-places/{place_id}"
                )
                if resp.status_code == 204:
                    return True
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    # WATERING FREQUENCIES
    def get_all_watering_frequencies(self) -> List[Dict]:
        """Get all watering frequencies from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/watering-frequencies")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching watering frequencies: {e}")
            return []
    
    def create_watering_frequency(self, name: str, days: int) -> Optional[Dict]:
        """Create new watering frequency"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/settings/watering-frequencies",
                    json={"name": name, "days": days}
                )
                if resp.status_code == 201:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def update_watering_frequency(self, freq_id: int, name: str, days: int) -> Optional[Dict]:
        """Update watering frequency"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(
                    f"{self.api_base_url}/api/settings/watering-frequencies/{freq_id}",
                    json={"name": name, "days": days}
                )
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_watering_frequency(self, freq_id: int) -> bool:
        """Delete watering frequency"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/settings/watering-frequencies/{freq_id}"
                )
                if resp.status_code == 204:
                    return True
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    # LIGHT REQUIREMENTS
    def get_all_light_requirements(self) -> List[Dict]:
        """Get all light requirements from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/light-requirements")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching light requirements: {e}")
            return []
    
    def create_light_requirement(self, name: str) -> Optional[Dict]:
        """Create new light requirement"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/settings/light-requirements",
                    json={"name": name}
                )
                if resp.status_code == 201:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def update_light_requirement(self, req_id: int, name: str) -> Optional[Dict]:
        """Update light requirement"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(
                    f"{self.api_base_url}/api/settings/light-requirements/{req_id}",
                    json={"name": name}
                )
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_light_requirement(self, req_id: int) -> bool:
        """Delete light requirement"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/settings/light-requirements/{req_id}"
                )
                if resp.status_code == 204:
                    return True
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    # FERTILIZER TYPES
    def get_all_fertilizer_types(self) -> List[Dict]:
        """Get all fertilizer types from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/fertilizer-types")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching fertilizer types: {e}")
            return []
    
    def create_fertilizer_type(self, name: str) -> Optional[Dict]:
        """Create new fertilizer type"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/settings/fertilizer-types",
                    json={"name": name}
                )
                if resp.status_code == 201:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def update_fertilizer_type(self, fert_id: int, name: str) -> Optional[Dict]:
        """Update fertilizer type"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.put(
                    f"{self.api_base_url}/api/settings/fertilizer-types/{fert_id}",
                    json={"name": name}
                )
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_fertilizer_type(self, fert_id: int) -> bool:
        """Delete fertilizer type"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/settings/fertilizer-types/{fert_id}"
                )
                if resp.status_code == 204:
                    return True
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    # TAGS
    def get_all_tags(self) -> List[Dict]:
        """Get all tags from API"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/settings/tags")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching tags: {e}")
            return []
    
    def create_tag(self, name: str, category_id: int) -> Optional[Dict]:
        """Create new tag"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{self.api_base_url}/api/settings/tags",
                    json={"name": name, "category_id": category_id}
                )
                if resp.status_code == 201:
                    return resp.json()
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def delete_tag(self, tag_id: int) -> bool:
        """Delete tag"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.delete(
                    f"{self.api_base_url}/api/settings/tags/{tag_id}"
                )
                if resp.status_code == 204:
                    return True
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def create_locations_tab(self):
        """Create Locations tab"""
        layout = [
            [sg.Text("Locations", font=("Arial", 12, "bold"))],
            [sg.Multiline(size=(50, 10), key="-LOC_LIST-", disabled=True)],
            [
                sg.Button("+ Add Location", key="-LOC_ADD-"),
                sg.Button("Edit", key="-LOC_EDIT-"),
                sg.Button("Delete", key="-LOC_DELETE-"),
                sg.Button("Refresh", key="-LOC_REFRESH-"),
            ],
        ]
        return sg.Tab("Locations", layout)
    
    def create_places_tab(self):
        """Create Purchase Places tab"""
        layout = [
            [sg.Text("Purchase Places", font=("Arial", 12, "bold"))],
            [sg.Multiline(size=(50, 10), key="-PLACE_LIST-", disabled=True)],
            [
                sg.Button("+ Add Place", key="-PLACE_ADD-"),
                sg.Button("Edit", key="-PLACE_EDIT-"),
                sg.Button("Delete", key="-PLACE_DELETE-"),
                sg.Button("Refresh", key="-PLACE_REFRESH-"),
            ],
        ]
        return sg.Tab("Purchase Places", layout)
    
    def create_watering_tab(self):
        """Create Watering Frequencies tab"""
        layout = [
            [sg.Text("Watering Frequencies", font=("Arial", 12, "bold"))],
            [sg.Multiline(size=(50, 10), key="-WATER_LIST-", disabled=True)],
            [
                sg.Button("+ Add Frequency", key="-WATER_ADD-"),
                sg.Button("Edit", key="-WATER_EDIT-"),
                sg.Button("Delete", key="-WATER_DELETE-"),
                sg.Button("Refresh", key="-WATER_REFRESH-"),
            ],
        ]
        return sg.Tab("Watering", layout)
    
    def create_light_tab(self):
        """Create Light Requirements tab"""
        layout = [
            [sg.Text("Light Requirements", font=("Arial", 12, "bold"))],
            [sg.Multiline(size=(50, 10), key="-LIGHT_LIST-", disabled=True)],
            [
                sg.Button("+ Add Light", key="-LIGHT_ADD-"),
                sg.Button("Edit", key="-LIGHT_EDIT-"),
                sg.Button("Delete", key="-LIGHT_DELETE-"),
                sg.Button("Refresh", key="-LIGHT_REFRESH-"),
            ],
        ]
        return sg.Tab("Light", layout)
    
    def create_fert_tab(self):
        """Create Fertilizer Types tab"""
        layout = [
            [sg.Text("Fertilizer Types", font=("Arial", 12, "bold"))],
            [sg.Multiline(size=(50, 10), key="-FERT_LIST-", disabled=True)],
            [
                sg.Button("+ Add Fertilizer", key="-FERT_ADD-"),
                sg.Button("Edit", key="-FERT_EDIT-"),
                sg.Button("Delete", key="-FERT_DELETE-"),
                sg.Button("Refresh", key="-FERT_REFRESH-"),
            ],
        ]
        return sg.Tab("Fertilizer", layout)
    
    def create_tags_tab(self):
        """Create Tags tab (read-only list, create/delete only)"""
        layout = [
            [sg.Text("Tags", font=("Arial", 12, "bold"))],
            [sg.Multiline(size=(50, 10), key="-TAGS_LIST-", disabled=True)],
            [
                sg.Button("+ Add Tag", key="-TAGS_ADD-"),
                sg.Button("Delete", key="-TAGS_DELETE-"),
                sg.Button("Refresh", key="-TAGS_REFRESH-"),
            ],
        ]
        return sg.Tab("Tags", layout)
    
    def build_layout(self) -> List:
        """Build main window layout"""
        tabs = [
            self.create_locations_tab(),
            self.create_places_tab(),
            self.create_watering_tab(),
            self.create_light_tab(),
            self.create_fert_tab(),
            self.create_tags_tab(),
        ]
        
        layout = [
            [sg.Text("🔧 SETTINGS - PLANT LOOKUPS", font=("Arial", 14, "bold"))],
            [sg.TabGroup([tabs])],
            [sg.Button("Close", key="-CLOSE-")],
        ]
        return layout
    
    def show(self):
        """Show window and handle events"""
        layout = self.build_layout()
        self.window = sg.Window(
            "🌱 Plant Manager - Settings", 
            layout, 
            finalize=True
        )
        
        # Initial load of all data
        try:
            self._load_all_data()
        except Exception as e:
            sg.popup_error(f"❌ Error loading settings data:\n{e}")
        
        while True:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == "-CLOSE-":
                break
            
            # Handle events asynchronously
            try:
                self._handle_event(event, values)
            except Exception as e:
                sg.popup_error(f"❌ Error: {e}")
        
        if self.window:
            self.window.close()
    
    def _load_all_data(self):
        """Load all data from API"""
        locations = self.get_all_locations()
        self._update_list_display("-LOC_LIST-", locations)
        
        places = self.get_all_purchase_places()
        self._update_list_display("-PLACE_LIST-", places)
        
        watering = self.get_all_watering_frequencies()
        self._update_watering_display("-WATER_LIST-", watering)
        
        lights = self.get_all_light_requirements()
        self._update_list_display("-LIGHT_LIST-", lights)
        
        ferts = self.get_all_fertilizer_types()
        self._update_list_display("-FERT_LIST-", ferts)
        
        tags = self.get_all_tags()
        self._update_list_display("-TAGS_LIST-", tags)
    
    def _update_list_display(self, key: str, items: List[Dict]):
        """Update a multiline text display with items"""
        if not items:
            self.window[key].update("No items")
            return
        
        display_text = "\n".join([f"[{item['id']}] {item['name']}" for item in items])
        self.window[key].update(display_text)
    
    def _update_watering_display(self, key: str, items: List[Dict]):
        """Update watering frequencies display (includes days)"""
        if not items:
            self.window[key].update("No items")
            return
        
        display_text = "\n".join([
            f"[{item['id']}] {item['name']} ({item.get('days', '?')} days)"
            for item in items
        ])
        self.window[key].update(display_text)
    
    def _handle_event(self, event: str, values: Dict):
        """Handle window events"""
        # LOCATIONS
        if event == "-LOC_ADD-":
            name = sg.popup_get_text("Enter location name:")
            if name and name.strip():
                result = self.create_location(name.strip())
                if result:
                    sg.popup_ok("✅ Location created!")
                    locations = self.get_all_locations()
                    self._update_list_display("-LOC_LIST-", locations)
                else:
                    sg.popup_error("❌ Failed to create location")
        
        elif event == "-LOC_EDIT-":
            name = sg.popup_get_text("Enter new location name:")
            if name and name.strip():
                loc_text = self.window["-LOC_LIST-"].get()
                selected_id = self._extract_id_from_display(loc_text)
                if selected_id:
                    result = self.update_location(selected_id, name.strip())
                    if result:
                        sg.popup_ok("✅ Location updated!")
                        locations = self.get_all_locations()
                        self._update_list_display("-LOC_LIST-", locations)
                    else:
                        sg.popup_error("❌ Failed to update location")
        
        elif event == "-LOC_DELETE-":
            loc_text = self.window["-LOC_LIST-"].get()
            selected_id = self._extract_id_from_display(loc_text)
            if selected_id and sg.popup_yes_no("Confirm deletion?") == "Yes":
                if self.delete_location(selected_id):
                    sg.popup_ok("✅ Location deleted!")
                    locations = self.get_all_locations()
                    self._update_list_display("-LOC_LIST-", locations)
                else:
                    sg.popup_error("❌ Failed to delete")
        
        elif event == "-LOC_REFRESH-":
            locations = self.get_all_locations()
            self._update_list_display("-LOC_LIST-", locations)
        
        # PURCHASE PLACES
        elif event == "-PLACE_ADD-":
            name = sg.popup_get_text("Enter purchase place name:")
            if name and name.strip():
                result = self.create_purchase_place(name.strip())
                if result:
                    sg.popup_ok("✅ Purchase place created!")
                    places = self.get_all_purchase_places()
                    self._update_list_display("-PLACE_LIST-", places)
                else:
                    sg.popup_error("❌ Failed to create")
        
        elif event == "-PLACE_EDIT-":
            name = sg.popup_get_text("Enter new purchase place name:")
            if name and name.strip():
                place_text = self.window["-PLACE_LIST-"].get()
                selected_id = self._extract_id_from_display(place_text)
                if selected_id:
                    result = self.update_purchase_place(selected_id, name.strip())
                    if result:
                        sg.popup_ok("✅ Purchase place updated!")
                        places = self.get_all_purchase_places()
                        self._update_list_display("-PLACE_LIST-", places)
                    else:
                        sg.popup_error("❌ Failed to update")
        
        elif event == "-PLACE_DELETE-":
            place_text = self.window["-PLACE_LIST-"].get()
            selected_id = self._extract_id_from_display(place_text)
            if selected_id and sg.popup_yes_no("Confirm deletion?") == "Yes":
                if self.delete_purchase_place(selected_id):
                    sg.popup_ok("✅ Deleted!")
                    places = self.get_all_purchase_places()
                    self._update_list_display("-PLACE_LIST-", places)
                else:
                    sg.popup_error("❌ Failed to delete")
        
        elif event == "-PLACE_REFRESH-":
            places = self.get_all_purchase_places()
            self._update_list_display("-PLACE_LIST-", places)
        
        # WATERING FREQUENCIES
        elif event == "-WATER_ADD-":
            layout = [
                [sg.Text("Name:"), sg.InputText(key="-WATER_NAME-")],
                [sg.Text("Days:"), sg.InputText(key="-WATER_DAYS-", size=(5, 1))],
                [sg.Button("Create"), sg.Button("Cancel")],
            ]
            window = sg.Window("Add Watering Frequency", layout)
            event2, values2 = window.read()
            window.close()
            
            if event2 == "Create" and values2["-WATER_NAME-"] and values2["-WATER_DAYS-"]:
                try:
                    days = int(values2["-WATER_DAYS-"])
                    result = self.create_watering_frequency(values2["-WATER_NAME-"], days)
                    if result:
                        sg.popup_ok("✅ Watering frequency created!")
                        watering = self.get_all_watering_frequencies()
                        self._update_watering_display("-WATER_LIST-", watering)
                except ValueError:
                    sg.popup_error("Days must be a number")
        
        elif event == "-WATER_EDIT-":
            layout = [
                [sg.Text("Name:"), sg.InputText(key="-WATER_NAME-")],
                [sg.Text("Days:"), sg.InputText(key="-WATER_DAYS-", size=(5, 1))],
                [sg.Button("Update"), sg.Button("Cancel")],
            ]
            window = sg.Window("Edit Watering Frequency", layout)
            event2, values2 = window.read()
            window.close()
            
            if event2 == "Update" and values2["-WATER_NAME-"] and values2["-WATER_DAYS-"]:
                try:
                    days = int(values2["-WATER_DAYS-"])
                    water_text = self.window["-WATER_LIST-"].get()
                    selected_id = self._extract_id_from_display(water_text)
                    if selected_id:
                        result = self.update_watering_frequency(selected_id, values2["-WATER_NAME-"], days)
                        if result:
                            sg.popup_ok("✅ Watering frequency updated!")
                            watering = self.get_all_watering_frequencies()
                            self._update_watering_display("-WATER_LIST-", watering)
                        else:
                            sg.popup_error("❌ Failed to update")
                except ValueError:
                    sg.popup_error("Days must be a number")
        
        elif event == "-WATER_DELETE-":
            water_text = self.window["-WATER_LIST-"].get()
            selected_id = self._extract_id_from_display(water_text)
            if selected_id and sg.popup_yes_no("Confirm deletion?") == "Yes":
                if self.delete_watering_frequency(selected_id):
                    sg.popup_ok("✅ Deleted!")
                    watering = self.get_all_watering_frequencies()
                    self._update_watering_display("-WATER_LIST-", watering)
                else:
                    sg.popup_error("❌ Failed to delete")
        
        elif event == "-WATER_REFRESH-":
            watering = self.get_all_watering_frequencies()
            self._update_watering_display("-WATER_LIST-", watering)
        
        # LIGHT REQUIREMENTS
        elif event == "-LIGHT_ADD-":
            name = sg.popup_get_text("Enter light requirement name:")
            if name and name.strip():
                result = self.create_light_requirement(name.strip())
                if result:
                    sg.popup_ok("✅ Light requirement created!")
                    lights = self.get_all_light_requirements()
                    self._update_list_display("-LIGHT_LIST-", lights)
        
        elif event == "-LIGHT_EDIT-":
            name = sg.popup_get_text("Enter new light requirement name:")
            if name and name.strip():
                light_text = self.window["-LIGHT_LIST-"].get()
                selected_id = self._extract_id_from_display(light_text)
                if selected_id:
                    result = self.update_light_requirement(selected_id, name.strip())
                    if result:
                        sg.popup_ok("✅ Light requirement updated!")
                        lights = self.get_all_light_requirements()
                        self._update_list_display("-LIGHT_LIST-", lights)
                    else:
                        sg.popup_error("❌ Failed to update")
        
        elif event == "-LIGHT_DELETE-":
            light_text = self.window["-LIGHT_LIST-"].get()
            selected_id = self._extract_id_from_display(light_text)
            if selected_id and sg.popup_yes_no("Confirm deletion?") == "Yes":
                if self.delete_light_requirement(selected_id):
                    sg.popup_ok("✅ Deleted!")
                    lights = self.get_all_light_requirements()
                    self._update_list_display("-LIGHT_LIST-", lights)
                else:
                    sg.popup_error("❌ Failed to delete")
        
        elif event == "-LIGHT_REFRESH-":
            lights = self.get_all_light_requirements()
            self._update_list_display("-LIGHT_LIST-", lights)
        
        # FERTILIZER TYPES
        elif event == "-FERT_ADD-":
            name = sg.popup_get_text("Enter fertilizer type name:")
            if name and name.strip():
                result = self.create_fertilizer_type(name.strip())
                if result:
                    sg.popup_ok("✅ Fertilizer type created!")
                    ferts = self.get_all_fertilizer_types()
                    self._update_list_display("-FERT_LIST-", ferts)
        
        elif event == "-FERT_EDIT-":
            name = sg.popup_get_text("Enter new fertilizer type name:")
            if name and name.strip():
                fert_text = self.window["-FERT_LIST-"].get()
                selected_id = self._extract_id_from_display(fert_text)
                if selected_id:
                    result = self.update_fertilizer_type(selected_id, name.strip())
                    if result:
                        sg.popup_ok("✅ Fertilizer type updated!")
                        ferts = self.get_all_fertilizer_types()
                        self._update_list_display("-FERT_LIST-", ferts)
                    else:
                        sg.popup_error("❌ Failed to update")
        
        elif event == "-FERT_DELETE-":
            fert_text = self.window["-FERT_LIST-"].get()
            selected_id = self._extract_id_from_display(fert_text)
            if selected_id and sg.popup_yes_no("Confirm deletion?") == "Yes":
                if self.delete_fertilizer_type(selected_id):
                    sg.popup_ok("✅ Deleted!")
                    ferts = self.get_all_fertilizer_types()
                    self._update_list_display("-FERT_LIST-", ferts)
                else:
                    sg.popup_error("❌ Failed to delete")
        
        elif event == "-FERT_REFRESH-":
            ferts = self.get_all_fertilizer_types()
            self._update_list_display("-FERT_LIST-", ferts)
        
        # TAGS
        elif event == "-TAGS_ADD-":
            layout = [
                [sg.Text("Name:"), sg.InputText(key="-TAG_NAME-")],
                [sg.Text("Category ID:"), sg.InputText(key="-TAG_CAT-", size=(5, 1))],
                [sg.Button("Create"), sg.Button("Cancel")],
            ]
            window = sg.Window("Add Tag", layout)
            event2, values2 = window.read()
            window.close()
            
            if event2 == "Create" and values2["-TAG_NAME-"] and values2["-TAG_CAT-"]:
                try:
                    cat_id = int(values2["-TAG_CAT-"])
                    result = self.create_tag(values2["-TAG_NAME-"], cat_id)
                    if result:
                        sg.popup_ok("✅ Tag created!")
                        tags = self.get_all_tags()
                        self._update_list_display("-TAGS_LIST-", tags)
                except ValueError:
                    sg.popup_error("Category ID must be a number")
        
        elif event == "-TAGS_EDIT-":
            layout = [
                [sg.Text("Name:"), sg.InputText(key="-TAG_NAME-")],
                [sg.Text("Category ID:"), sg.InputText(key="-TAG_CAT-", size=(5, 1))],
                [sg.Button("Update"), sg.Button("Cancel")],
            ]
            window = sg.Window("Edit Tag", layout)
            event2, values2 = window.read()
            window.close()
            
            if event2 == "Update" and values2["-TAG_NAME-"] and values2["-TAG_CAT-"]:
                try:
                    cat_id = int(values2["-TAG_CAT-"])
                    tags_text = self.window["-TAGS_LIST-"].get()
                    selected_id = self._extract_id_from_display(tags_text)
                    if selected_id:
                        result = self.update_tag(selected_id, values2["-TAG_NAME-"], cat_id)
                        if result:
                            sg.popup_ok("✅ Tag updated!")
                            tags = self.get_all_tags()
                            self._update_list_display("-TAGS_LIST-", tags)
                        else:
                            sg.popup_error("❌ Failed to update")
                except ValueError:
                    sg.popup_error("Category ID must be a number")
        
        elif event == "-TAGS_DELETE-":
            tags_text = self.window["-TAGS_LIST-"].get()
            selected_id = self._extract_id_from_display(tags_text)
            if selected_id and sg.popup_yes_no("Confirm deletion?") == "Yes":
                if self.delete_tag(selected_id):
                    sg.popup_ok("✅ Deleted!")
                    tags = self.get_all_tags()
                    self._update_list_display("-TAGS_LIST-", tags)
                else:
                    sg.popup_error("❌ Failed to delete")
        
        elif event == "-TAGS_REFRESH-":
            tags = self.get_all_tags()
            self._update_list_display("-TAGS_LIST-", tags)
    
    def _extract_id_from_display(self, display_text: str) -> Optional[int]:
        """Extract ID from first line of display (format: [ID] Name)"""
        try:
            if "[" in display_text and "]" in display_text:
                id_str = display_text.split("[")[1].split("]")[0]
                return int(id_str)
        except (IndexError, ValueError):
            pass
        return None


def main():
    """Run settings window"""
    window = SettingsWindow()
    window.show()


if __name__ == "__main__":
    main()

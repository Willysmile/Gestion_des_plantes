"""Plant and Settings dialogs for user input"""

import PySimpleGUI as sg
from typing import List, Dict
from datetime import datetime


def create_add_plant_dialog(
    locations_list=None, 
    places_list=None, 
    frequencies_list=None, 
    light_list=None
):
    """Show dialog to add new plant with accordion sections
    
    Args:
        locations_list: List of available locations
        places_list: List of purchase places
        frequencies_list: List of watering frequencies
        light_list: List of light requirements
        
    Returns:
        dict with plant data or None if cancelled
    """
    if locations_list is None:
        locations_list = []
    if places_list is None:
        places_list = []
    if frequencies_list is None:
        frequencies_list = []
    if light_list is None:
        light_list = []
    
    # Section states (collapsed/expanded)
    section_states = {
        "basic": True,      # Expanded
        "taxonomy": False,  # Collapsed
        "description": False,
        "purchase": False,
        "location": True,   # Expanded
        "environment": False,
        "metadata": False
    }
    
    def toggle_section(name):
        section_states[name] = not section_states[name]
    
    # Build layout
    layout = [
        [sg.Text("🌱 Add New Plant", font=("Arial", 14, "bold"))],
        [sg.Text("_" * 80)],
        
        # BASIC INFO (Expanded by default)
        [sg.Button("▼ 📌 BASIC INFO", key="-BTN_BASIC-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Plant Name:*"), sg.InputText(key="-NAME-", size=(30, 1))],
            [sg.Text("Scientific Name:"), sg.InputText(key="-SCI_NAME-", size=(30, 1), disabled=True)],
            [sg.Text("(Auto-generated from Genus + Species)"), sg.Text("", font=("Arial", 8, "italic"))],
            [sg.Text("Favorite:"), sg.Checkbox("⭐ Mark as favorite", key="-FAVORITE-")],
        ], key="-COL_BASIC-")],
        
        # TAXONOMY
        [sg.Button("▶ 🔬 TAXONOMY", key="-BTN_TAXONOMY-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Family:"), sg.InputText(key="-FAMILY-", size=(30, 1))],
            [sg.Text("Subfamily:"), sg.InputText(key="-SUBFAMILY-", size=(30, 1))],
            [sg.Text("Genus:*"), sg.InputText(key="-GENUS-", size=(30, 1))],
            [sg.Text("Species:*"), sg.InputText(key="-SPECIES-", size=(30, 1))],
            [sg.Text("Subspecies:"), sg.InputText(key="-SUBSPECIES-", size=(30, 1))],
            [sg.Text("Variety:"), sg.InputText(key="-VARIETY-", size=(30, 1))],
            [sg.Text("Cultivar:"), sg.InputText(key="-CULTIVAR-", size=(30, 1))],
        ], key="-COL_TAXONOMY-", visible=False)],
        
        # DESCRIPTION
        [sg.Button("▶ 📝 DESCRIPTION", key="-BTN_DESCRIPTION-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Description:")],
            [sg.Multiline(size=(65, 4), key="-DESCRIPTION-")],
            [sg.Text("Reference:"), sg.InputText(key="-REFERENCE-", size=(30, 1))],
            [sg.Text("Flowering Season:"), sg.InputText(key="-FLOWERING-", size=(30, 1))],
        ], key="-COL_DESCRIPTION-", visible=False)],
        
        # PURCHASE
        [sg.Button("▶ 🛒 PURCHASE", key="-BTN_PURCHASE-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Purchase Date:"), sg.InputText(key="-PURCHASE_DATE-", size=(30, 1)), sg.Button("📅", size=(2, 1))],
            [sg.Text("Purchase Place:"), sg.Combo(places_list, key="-PURCHASE_PLACE-", size=(28, 1))],
            [sg.Text("Purchase Price (€):"), sg.InputText(key="-PURCHASE_PRICE-", size=(30, 1))],
        ], key="-COL_PURCHASE-", visible=False)],
        
        # LOCATION & MAINTENANCE (Expanded by default)
        [sg.Button("▼ 📍 LOCATION & MAINTENANCE", key="-BTN_LOCATION-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Current Location:"), sg.Combo(locations_list, key="-LOCATION-", size=(28, 1))],
            [sg.Text("Watering Frequency:"), sg.Combo(frequencies_list, key="-WATERING_FREQ-", size=(28, 1))],
            [sg.Text("Light Requirement:"), sg.Combo(light_list, key="-LIGHT-", size=(28, 1))],
            [sg.Text("Difficulty:"), sg.Combo(["Easy", "Medium", "Hard"], key="-DIFF-", size=(28, 1))],
            [sg.Text("Health Status:"), sg.Combo(["Healthy", "Sick", "Recovering"], key="-HEALTH-", size=(28, 1))],
        ], key="-COL_LOCATION-")],
        
        # ENVIRONMENT
        [sg.Button("▶ 🌡️ ENVIRONMENT", key="-BTN_ENVIRONMENT-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Temperature Min (°C):"), sg.InputText(key="-TEMP_MIN-", size=(30, 1))],
            [sg.Text("Temperature Max (°C):"), sg.InputText(key="-TEMP_MAX-", size=(30, 1))],
            [sg.Text("Humidity Level (%):"), sg.InputText(key="-HUMIDITY-", size=(30, 1))],
            [sg.Text("Soil Humidity:"), sg.Combo(["Dry", "Moderate", "Humid"], key="-SOIL_HUMIDITY-", size=(28, 1))],
            [sg.Text("Soil Type:"), sg.InputText(key="-SOIL_TYPE-", size=(30, 1))],
            [sg.Text("Soil pH:"), sg.InputText(key="-SOIL_PH-", size=(30, 1))],
            [sg.Text("Pot Size (cm):"), sg.InputText(key="-POT_SIZE-", size=(30, 1))],
            [sg.Text("Growth Speed:"), sg.Combo(["Slow", "Normal", "Fast"], key="-GROWTH_SPEED-", size=(28, 1))],
            [sg.Text("Max Height (cm):"), sg.InputText(key="-MAX_HEIGHT-", size=(30, 1))],
        ], key="-COL_ENVIRONMENT-", visible=False)],
        
        # METADATA
        [sg.Button("▶ ⚙️ METADATA", key="-BTN_METADATA-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Checkbox("🏠 Indoor", key="-INDOOR-"), sg.Checkbox("🌳 Outdoor", key="-OUTDOOR-")],
            [sg.Checkbox("☠️ Toxic", key="-TOXIC-"), sg.Checkbox("📦 Archived", key="-ARCHIVED-")],
        ], key="-COL_METADATA-", visible=False)],
        
        # Separator and buttons
        [sg.Text("_" * 80)],
        [sg.Text("* Required fields", font=("Arial", 8, "italic"))],
        [sg.Button("✅ Add Plant", size=(15, 1)), sg.Button("❌ Cancel", size=(15, 1))]
    ]
    
    window = sg.Window("Add Plant", layout, modal=True, finalize=True)
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "❌ Cancel":
            window.close()
            return None
        
        # Toggle sections
        if event == "-BTN_BASIC-":
            toggle_section("basic")
            window["-COL_BASIC-"].update(visible=section_states["basic"])
            window["-BTN_BASIC-"].update("▼ 📌 BASIC INFO" if section_states["basic"] else "▶ 📌 BASIC INFO")
        elif event == "-BTN_TAXONOMY-":
            toggle_section("taxonomy")
            window["-COL_TAXONOMY-"].update(visible=section_states["taxonomy"])
            window["-BTN_TAXONOMY-"].update("▼ 🔬 TAXONOMY" if section_states["taxonomy"] else "▶ 🔬 TAXONOMY")
        elif event == "-BTN_DESCRIPTION-":
            toggle_section("description")
            window["-COL_DESCRIPTION-"].update(visible=section_states["description"])
            window["-BTN_DESCRIPTION-"].update("▼ 📝 DESCRIPTION" if section_states["description"] else "▶ 📝 DESCRIPTION")
        elif event == "-BTN_PURCHASE-":
            toggle_section("purchase")
            window["-COL_PURCHASE-"].update(visible=section_states["purchase"])
            window["-BTN_PURCHASE-"].update("▼ 🛒 PURCHASE" if section_states["purchase"] else "▶ 🛒 PURCHASE")
        elif event == "-BTN_LOCATION-":
            toggle_section("location")
            window["-COL_LOCATION-"].update(visible=section_states["location"])
            window["-BTN_LOCATION-"].update("▼ 📍 LOCATION & MAINTENANCE" if section_states["location"] else "▶ 📍 LOCATION & MAINTENANCE")
        elif event == "-BTN_ENVIRONMENT-":
            toggle_section("environment")
            window["-COL_ENVIRONMENT-"].update(visible=section_states["environment"])
            window["-BTN_ENVIRONMENT-"].update("▼ 🌡️ ENVIRONMENT" if section_states["environment"] else "▶ 🌡️ ENVIRONMENT")
        elif event == "-BTN_METADATA-":
            toggle_section("metadata")
            window["-COL_METADATA-"].update(visible=section_states["metadata"])
            window["-BTN_METADATA-"].update("▼ ⚙️ METADATA" if section_states["metadata"] else "▶ ⚙️ METADATA")
        
        elif event == "✅ Add Plant":
            # Validate required fields
            if not values["-NAME-"].strip():
                sg.popup_error("❌ Plant name is required!")
                continue
            
            if not values["-GENUS-"].strip() or not values["-SPECIES-"].strip():
                sg.popup_error("❌ Genus and Species are required for scientific name generation!")
                continue
            
            # Generate scientific name from genus + species
            genus = values["-GENUS-"].strip().capitalize()
            species = values["-SPECIES-"].strip().lower()
            scientific_name = f"{genus} {species}"
            
            # Parse numeric fields
            try:
                temp_min = float(values["-TEMP_MIN-"]) if values["-TEMP_MIN-"].strip() else None
                temp_max = float(values["-TEMP_MAX-"]) if values["-TEMP_MAX-"].strip() else None
                humidity = float(values["-HUMIDITY-"]) if values["-HUMIDITY-"].strip() else None
                soil_ph = float(values["-SOIL_PH-"]) if values["-SOIL_PH-"].strip() else None
                pot_size = values["-POT_SIZE-"].strip() or None
                max_height = float(values["-MAX_HEIGHT-"]) if values["-MAX_HEIGHT-"].strip() else None
                purchase_price = float(values["-PURCHASE_PRICE-"]) if values["-PURCHASE_PRICE-"].strip() else None
            except ValueError:
                sg.popup_error("❌ Please enter valid numbers for numeric fields!")
                continue
            
            window.close()
            return {
                # Basic
                "name": values["-NAME-"].strip(),
                "scientific_name": scientific_name,
                "is_favorite": values["-FAVORITE-"],
                
                # Taxonomy
                "family": values["-FAMILY-"].strip() or None,
                "subfamily": values["-SUBFAMILY-"].strip() or None,
                "genus": values["-GENUS-"].strip() or None,
                "species": values["-SPECIES-"].strip() or None,
                "subspecies": values["-SUBSPECIES-"].strip() or None,
                "variety": values["-VARIETY-"].strip() or None,
                "cultivar": values["-CULTIVAR-"].strip() or None,
                
                # Description
                "description": values["-DESCRIPTION-"].strip() or None,
                "reference": values["-REFERENCE-"].strip() or None,
                "flowering_season": values["-FLOWERING-"].strip() or None,
                
                # Purchase
                "purchase_date": values["-PURCHASE_DATE-"].strip() or None,
                "purchase_place_id": values["-PURCHASE_PLACE-"] or None,
                "purchase_price": purchase_price,
                
                # Location & Maintenance
                "location_id": values["-LOCATION-"] or None,
                "watering_frequency_id": values["-WATERING_FREQ-"] or None,
                "light_requirement_id": values["-LIGHT-"] or None,
                "difficulty": values["-DIFF-"] or None,
                "health_status": values["-HEALTH-"] or None,
                
                # Environment
                "temperature_min": temp_min,
                "temperature_max": temp_max,
                "humidity_level": humidity,
                "soil_humidity": values["-SOIL_HUMIDITY-"] or None,
                "soil_type": values["-SOIL_TYPE-"].strip() or None,
                "soil_ideal_ph": soil_ph,
                "pot_size": pot_size,
                "growth_speed": values["-GROWTH_SPEED-"] or None,
                "max_height": max_height,
                
                # Metadata
                "is_indoor": values["-INDOOR-"],
                "is_outdoor": values["-OUTDOOR-"],
                "is_toxic": values["-TOXIC-"],
                "is_archived": values["-ARCHIVED-"]
            }
    
    return None


def create_edit_plant_dialog(
    plant: dict, 
    locations_list=None, 
    places_list=None, 
    frequencies_list=None, 
    light_list=None
):
    """Show dialog to edit existing plant with accordion sections
    
    Args:
        plant: Current plant data to edit
        locations_list: List of available locations
        places_list: List of purchase places
        frequencies_list: List of watering frequencies
        light_list: List of light requirements
        
    Returns:
        dict with updated plant data or None if cancelled
    """
    if locations_list is None:
        locations_list = []
    if places_list is None:
        places_list = []
    if frequencies_list is None:
        frequencies_list = []
    if light_list is None:
        light_list = []
    
    # Section states (collapsed/expanded)
    section_states = {
        "basic": True,      # Expanded
        "taxonomy": False,  # Collapsed
        "description": False,
        "purchase": False,
        "location": True,   # Expanded
        "environment": False,
        "metadata": False
    }
    
    def toggle_section(name):
        section_states[name] = not section_states[name]
    
    # Build layout
    layout = [
        [sg.Text(f"✏️ Edit Plant: {plant.get('name', '')}", font=("Arial", 14, "bold"))],
        [sg.Text("_" * 80)],
        
        # BASIC INFO (Expanded by default)
        [sg.Button("▼ 📌 BASIC INFO", key="-BTN_BASIC-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Plant Name:*"), sg.InputText(default_text=plant.get('name', ''), key="-NAME-", size=(30, 1))],
            [sg.Text("Scientific Name:"), sg.InputText(default_text=plant.get('scientific_name', ''), key="-SCI_NAME-", size=(30, 1), disabled=True)],
            [sg.Text("(Auto-generated from Genus + Species)"), sg.Text("", font=("Arial", 8, "italic"))],
            [sg.Text("Favorite:"), sg.Checkbox("⭐ Mark as favorite", key="-FAVORITE-", default=plant.get('is_favorite', False))],
        ], key="-COL_BASIC-")],
        
        # TAXONOMY
        [sg.Button("▶ 🔬 TAXONOMY", key="-BTN_TAXONOMY-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Family:"), sg.InputText(default_text=plant.get('family', ''), key="-FAMILY-", size=(30, 1))],
            [sg.Text("Subfamily:"), sg.InputText(default_text=plant.get('subfamily', ''), key="-SUBFAMILY-", size=(30, 1))],
            [sg.Text("Genus:*"), sg.InputText(default_text=plant.get('genus', ''), key="-GENUS-", size=(30, 1))],
            [sg.Text("Species:*"), sg.InputText(default_text=plant.get('species', ''), key="-SPECIES-", size=(30, 1))],
            [sg.Text("Subspecies:"), sg.InputText(default_text=plant.get('subspecies', ''), key="-SUBSPECIES-", size=(30, 1))],
            [sg.Text("Variety:"), sg.InputText(default_text=plant.get('variety', ''), key="-VARIETY-", size=(30, 1))],
            [sg.Text("Cultivar:"), sg.InputText(default_text=plant.get('cultivar', ''), key="-CULTIVAR-", size=(30, 1))],
        ], key="-COL_TAXONOMY-", visible=False)],
        
        # DESCRIPTION
        [sg.Button("▶ 📝 DESCRIPTION", key="-BTN_DESCRIPTION-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Description:")],
            [sg.Multiline(default_text=plant.get('description', ''), size=(65, 4), key="-DESCRIPTION-")],
            [sg.Text("Reference:"), sg.InputText(default_text=plant.get('reference', ''), key="-REFERENCE-", size=(30, 1))],
            [sg.Text("Flowering Season:"), sg.InputText(default_text=plant.get('flowering_season', ''), key="-FLOWERING-", size=(30, 1))],
        ], key="-COL_DESCRIPTION-", visible=False)],
        
        # PURCHASE
        [sg.Button("▶ 🛒 PURCHASE", key="-BTN_PURCHASE-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Purchase Date:"), sg.InputText(default_text=plant.get('purchase_date', ''), key="-PURCHASE_DATE-", size=(30, 1)), sg.Button("📅", size=(2, 1))],
            [sg.Text("Purchase Place:"), sg.Combo(places_list, default_value=plant.get('purchase_place_id', ''), key="-PURCHASE_PLACE-", size=(28, 1))],
            [sg.Text("Purchase Price (€):"), sg.InputText(default_text=str(plant.get('purchase_price', '') or ''), key="-PURCHASE_PRICE-", size=(30, 1))],
        ], key="-COL_PURCHASE-", visible=False)],
        
        # LOCATION & MAINTENANCE (Expanded by default)
        [sg.Button("▼ 📍 LOCATION & MAINTENANCE", key="-BTN_LOCATION-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Current Location:"), sg.Combo(locations_list, default_value=plant.get('location_id', ''), key="-LOCATION-", size=(28, 1))],
            [sg.Text("Watering Frequency:"), sg.Combo(frequencies_list, default_value=plant.get('watering_frequency_id', ''), key="-WATERING_FREQ-", size=(28, 1))],
            [sg.Text("Light Requirement:"), sg.Combo(light_list, default_value=plant.get('light_requirement_id', ''), key="-LIGHT-", size=(28, 1))],
            [sg.Text("Difficulty:"), sg.Combo(["Easy", "Medium", "Hard"], default_value=plant.get('difficulty', ''), key="-DIFF-", size=(28, 1))],
            [sg.Text("Health Status:"), sg.Combo(["Healthy", "Sick", "Recovering"], default_value=plant.get('health_status', ''), key="-HEALTH-", size=(28, 1))],
        ], key="-COL_LOCATION-")],
        
        # ENVIRONMENT
        [sg.Button("▶ 🌡️ ENVIRONMENT", key="-BTN_ENVIRONMENT-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Text("Temperature Min (°C):"), sg.InputText(default_text=str(plant.get('temperature_min', '') or ''), key="-TEMP_MIN-", size=(30, 1))],
            [sg.Text("Temperature Max (°C):"), sg.InputText(default_text=str(plant.get('temperature_max', '') or ''), key="-TEMP_MAX-", size=(30, 1))],
            [sg.Text("Humidity Level (%):"), sg.InputText(default_text=str(plant.get('humidity_level', '') or ''), key="-HUMIDITY-", size=(30, 1))],
            [sg.Text("Soil Humidity:"), sg.Combo(["Dry", "Moderate", "Humid"], default_value=plant.get('soil_humidity', ''), key="-SOIL_HUMIDITY-", size=(28, 1))],
            [sg.Text("Soil Type:"), sg.InputText(default_text=plant.get('soil_type', ''), key="-SOIL_TYPE-", size=(30, 1))],
            [sg.Text("Soil pH:"), sg.InputText(default_text=str(plant.get('soil_ideal_ph', '') or ''), key="-SOIL_PH-", size=(30, 1))],
            [sg.Text("Pot Size (cm):"), sg.InputText(default_text=plant.get('pot_size', ''), key="-POT_SIZE-", size=(30, 1))],
            [sg.Text("Growth Speed:"), sg.Combo(["Slow", "Normal", "Fast"], default_value=plant.get('growth_speed', ''), key="-GROWTH_SPEED-", size=(28, 1))],
            [sg.Text("Max Height (cm):"), sg.InputText(default_text=str(plant.get('max_height', '') or ''), key="-MAX_HEIGHT-", size=(30, 1))],
        ], key="-COL_ENVIRONMENT-", visible=False)],
        
        # METADATA
        [sg.Button("▶ ⚙️ METADATA", key="-BTN_METADATA-", size=(77, 1)), sg.Button("", size=(1,1), visible=False)],
        [sg.Col([
            [sg.Checkbox("🏠 Indoor", key="-INDOOR-", default=plant.get('is_indoor', False)), sg.Checkbox("🌳 Outdoor", key="-OUTDOOR-", default=plant.get('is_outdoor', False))],
            [sg.Checkbox("☠️ Toxic", key="-TOXIC-", default=plant.get('is_toxic', False)), sg.Checkbox("📦 Archived", key="-ARCHIVED-", default=plant.get('is_archived', False))],
        ], key="-COL_METADATA-", visible=False)],
        
        # Separator and buttons
        [sg.Text("_" * 80)],
        [sg.Text("* Required fields", font=("Arial", 8, "italic"))],
        [sg.Button("💾 Save", size=(15, 1)), sg.Button("❌ Cancel", size=(15, 1))]
    ]
    
    window = sg.Window("Edit Plant", layout, modal=True, finalize=True)
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "❌ Cancel":
            window.close()
            return None
        
        # Toggle sections
        if event == "-BTN_BASIC-":
            toggle_section("basic")
            window["-COL_BASIC-"].update(visible=section_states["basic"])
            window["-BTN_BASIC-"].update("▼ 📌 BASIC INFO" if section_states["basic"] else "▶ 📌 BASIC INFO")
        elif event == "-BTN_TAXONOMY-":
            toggle_section("taxonomy")
            window["-COL_TAXONOMY-"].update(visible=section_states["taxonomy"])
            window["-BTN_TAXONOMY-"].update("▼ 🔬 TAXONOMY" if section_states["taxonomy"] else "▶ 🔬 TAXONOMY")
        elif event == "-BTN_DESCRIPTION-":
            toggle_section("description")
            window["-COL_DESCRIPTION-"].update(visible=section_states["description"])
            window["-BTN_DESCRIPTION-"].update("▼ 📝 DESCRIPTION" if section_states["description"] else "▶ 📝 DESCRIPTION")
        elif event == "-BTN_PURCHASE-":
            toggle_section("purchase")
            window["-COL_PURCHASE-"].update(visible=section_states["purchase"])
            window["-BTN_PURCHASE-"].update("▼ 🛒 PURCHASE" if section_states["purchase"] else "▶ 🛒 PURCHASE")
        elif event == "-BTN_LOCATION-":
            toggle_section("location")
            window["-COL_LOCATION-"].update(visible=section_states["location"])
            window["-BTN_LOCATION-"].update("▼ 📍 LOCATION & MAINTENANCE" if section_states["location"] else "▶ 📍 LOCATION & MAINTENANCE")
        elif event == "-BTN_ENVIRONMENT-":
            toggle_section("environment")
            window["-COL_ENVIRONMENT-"].update(visible=section_states["environment"])
            window["-BTN_ENVIRONMENT-"].update("▼ 🌡️ ENVIRONMENT" if section_states["environment"] else "▶ 🌡️ ENVIRONMENT")
        elif event == "-BTN_METADATA-":
            toggle_section("metadata")
            window["-COL_METADATA-"].update(visible=section_states["metadata"])
            window["-BTN_METADATA-"].update("▼ ⚙️ METADATA" if section_states["metadata"] else "▶ ⚙️ METADATA")
        
        elif event == "💾 Save":
            # Validate required fields
            if not values["-NAME-"].strip():
                sg.popup_error("❌ Plant name is required!")
                continue
            
            if not values["-GENUS-"].strip() or not values["-SPECIES-"].strip():
                sg.popup_error("❌ Genus and Species are required for scientific name generation!")
                continue
            
            # Generate scientific name from genus + species
            genus = values["-GENUS-"].strip().capitalize()
            species = values["-SPECIES-"].strip().lower()
            scientific_name = f"{genus} {species}"
            
            # Parse numeric fields
            try:
                temp_min = float(values["-TEMP_MIN-"]) if values["-TEMP_MIN-"].strip() else None
                temp_max = float(values["-TEMP_MAX-"]) if values["-TEMP_MAX-"].strip() else None
                humidity = float(values["-HUMIDITY-"]) if values["-HUMIDITY-"].strip() else None
                soil_ph = float(values["-SOIL_PH-"]) if values["-SOIL_PH-"].strip() else None
                pot_size = values["-POT_SIZE-"].strip() or None
                max_height = float(values["-MAX_HEIGHT-"]) if values["-MAX_HEIGHT-"].strip() else None
                purchase_price = float(values["-PURCHASE_PRICE-"]) if values["-PURCHASE_PRICE-"].strip() else None
            except ValueError:
                sg.popup_error("❌ Please enter valid numbers for numeric fields!")
                continue
            
            window.close()
            return {
                "id": plant.get("id"),  # Keep ID for update
                # Basic
                "name": values["-NAME-"].strip(),
                "scientific_name": scientific_name,
                "is_favorite": values["-FAVORITE-"],
                
                # Taxonomy
                "family": values["-FAMILY-"].strip() or None,
                "subfamily": values["-SUBFAMILY-"].strip() or None,
                "genus": values["-GENUS-"].strip() or None,
                "species": values["-SPECIES-"].strip() or None,
                "subspecies": values["-SUBSPECIES-"].strip() or None,
                "variety": values["-VARIETY-"].strip() or None,
                "cultivar": values["-CULTIVAR-"].strip() or None,
                
                # Description
                "description": values["-DESCRIPTION-"].strip() or None,
                "reference": values["-REFERENCE-"].strip() or None,
                "flowering_season": values["-FLOWERING-"].strip() or None,
                
                # Purchase
                "purchase_date": values["-PURCHASE_DATE-"].strip() or None,
                "purchase_place_id": values["-PURCHASE_PLACE-"] or None,
                "purchase_price": purchase_price,
                
                # Location & Maintenance
                "location_id": values["-LOCATION-"] or None,
                "watering_frequency_id": values["-WATERING_FREQ-"] or None,
                "light_requirement_id": values["-LIGHT-"] or None,
                "difficulty": values["-DIFF-"] or None,
                "health_status": values["-HEALTH-"] or None,
                
                # Environment
                "temperature_min": temp_min,
                "temperature_max": temp_max,
                "humidity_level": humidity,
                "soil_humidity": values["-SOIL_HUMIDITY-"] or None,
                "soil_type": values["-SOIL_TYPE-"].strip() or None,
                "soil_ideal_ph": soil_ph,
                "pot_size": pot_size,
                "growth_speed": values["-GROWTH_SPEED-"] or None,
                "max_height": max_height,
                
                # Metadata
                "is_indoor": values["-INDOOR-"],
                "is_outdoor": values["-OUTDOOR-"],
                "is_toxic": values["-TOXIC-"],
                "is_archived": values["-ARCHIVED-"]
            }
    
    return None


def create_confirm_delete_dialog(plant_name: str) -> bool:
    """Show confirmation before delete
    
    Args:
        plant_name: Name of plant to delete
        
    Returns:
        True if confirmed, False otherwise
    """
    result = sg.popup_yes_no(
        f"⚠️ Are you sure you want to delete '{plant_name}'?\n\nThis cannot be undone.",
        title="Confirm Delete",
        button_color=("white", "red")
    )
    return result == "Yes"


def show_plant_details(plant: dict, watering_history: List[Dict] = None, fertilizing_history: List[Dict] = None) -> str:
    """Show detailed view of a plant with history tabs
    
    Args:
        plant: Plant data dictionary
        watering_history: List of watering history entries
        fertilizing_history: List of fertilizing history entries
        
    Returns:
        Action: "view", "edit", "close" or "delete"
    """
    if watering_history is None:
        watering_history = []
    if fertilizing_history is None:
        fertilizing_history = []
    
    plant_id = plant.get("id", "?")
    name = plant.get("name", "Unknown")
    scientific_name = plant.get("scientific_name", "N/A")
    location = plant.get("location_id", "N/A")
    difficulty = plant.get("difficulty", "N/A")
    health = plant.get("health_status", "N/A")
    archived = "✅ Yes" if plant.get("is_archived", False) else "❌ No"
    
    # Format details text
    details = f"""
🌱 PLANT DETAILS
{"="*50}

ID:                     {plant_id}
Name:                   {name}
Scientific Name:        {scientific_name}
Location:               {location}
Difficulty Level:       {difficulty}
Health Status:          {health}
Archived:               {archived}

{"="*50}
"""
    
    # Format watering history
    watering_text = "Recent Watering History:\n"
    if watering_history:
        for entry in watering_history[-5:]:  # Last 5 entries
            date = entry.get("date_watered", "?")
            notes = entry.get("notes", "-")
            watering_text += f"  • {date}: {notes}\n"
    else:
        watering_text += "  (No watering history recorded)\n"
    
    # Format fertilizing history
    fertilizing_text = "Recent Fertilizing History:\n"
    if fertilizing_history:
        for entry in fertilizing_history[-5:]:  # Last 5 entries
            date = entry.get("date_fertilized", "?")
            fert_type = entry.get("fertilizer_type", "?")
            fertilizing_text += f"  • {date}: {fert_type}\n"
    else:
        fertilizing_text += "  (No fertilizing history recorded)\n"
    
    # Create tabbed layout
    tab_group = [
        [sg.Tab("📋 Info", [
            [sg.Text(details, font=("Courier", 10))]
        ])],
        [sg.Tab("💧 Watering", [
            [sg.Multiline(watering_text, size=(50, 12), disabled=True)]
        ])],
        [sg.Tab("🧪 Fertilizing", [
            [sg.Multiline(fertilizing_text, size=(50, 12), disabled=True)]
        ])]
    ]
    
    layout = [
        [sg.TabGroup(tab_group, key="-TABS-")],
        [sg.Text("_" * 50)],
        [
            sg.Button("✏️ Edit", size=(12, 1)),
            sg.Button("🗑️ Delete", size=(12, 1)),
            sg.Button("❌ Close", size=(12, 1))
        ]
    ]
    
    window = sg.Window(f"🌱 {name}", layout, modal=False, finalize=True)
    
    while True:
        event, _ = window.read(timeout=100)
        
        if event == sg.WINDOW_CLOSED or event == "❌ Close":
            window.close()
            return "close"
        elif event == "✏️ Edit":
            window.close()
            return "edit"
        elif event == "🗑️ Delete":
            window.close()
            return "delete"

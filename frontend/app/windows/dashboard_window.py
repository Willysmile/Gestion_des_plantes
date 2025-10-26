"""
Dashboard Window - KPI cards and upcoming tasks tables
Phase 4B - Frontend Dashboard UI
"""

import PySimpleGUI as sg
import httpx
from typing import List, Dict, Optional
from datetime import datetime


class DashboardWindow:
    """Dashboard window showing KPIs and upcoming tasks"""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
        self.window = None
        
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard KPIs"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{self.api_base_url}/api/statistics/dashboard")
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "total_plants": data.get("total_plants", 0),
                        "active_plants": data.get("active_plants", 0),
                        "archived_plants": data.get("archived_plants", 0),
                        "health_excellent": data.get("health_excellent", 0),
                        "health_good": data.get("health_good", 0),
                        "health_poor": data.get("health_poor", 0),
                        "total_photos": data.get("total_photos", 0),
                    }
                return {
                    "total_plants": 0, "active_plants": 0, "archived_plants": 0,
                    "health_excellent": 0, "health_good": 0, "health_poor": 0,
                    "total_photos": 0
                }
        except Exception as e:
            print(f"❌ Error fetching dashboard stats: {e}")
            return {
                "total_plants": 0, "active_plants": 0, "archived_plants": 0,
                "health_excellent": 0, "health_good": 0, "health_poor": 0,
                "total_photos": 0
            }
    
    def get_upcoming_waterings(self, days: int = 7) -> List[Dict]:
        """Get plants to water in next X days"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"{self.api_base_url}/api/statistics/upcoming-waterings",
                    params={"days": days}
                )
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching waterings: {e}")
            return []
    
    def get_upcoming_fertilizing(self, days: int = 7) -> List[Dict]:
        """Get plants to fertilize in next X days"""
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"{self.api_base_url}/api/statistics/upcoming-fertilizing",
                    params={"days": days}
                )
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            print(f"❌ Error fetching fertilizing: {e}")
            return []
    
    def create_kpi_cards_layout(self) -> List:
        """Create KPI cards layout"""
        layout = [
            [sg.Text("📊 KEY PERFORMANCE INDICATORS", font=("Arial", 12, "bold"))],
            [sg.Text("_" * 80)],
            [
                sg.Column([
                    [sg.Text("Total Plants", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_TOTAL-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="lightgray"),
                sg.Column([
                    [sg.Text("Active", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_ACTIVE-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="lightgreen"),
                sg.Column([
                    [sg.Text("Archived", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_ARCHIVED-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="lightcoral"),
            ],
            [
                sg.Column([
                    [sg.Text("Excellent", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_EXCELLENT-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="gold"),
                sg.Column([
                    [sg.Text("Good", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_GOOD-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="lightblue"),
                sg.Column([
                    [sg.Text("Poor", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_POOR-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="lightyellow"),
            ],
            [
                sg.Column([
                    [sg.Text("Photos", font=("Arial", 10, "bold"), size=(12, 1))],
                    [sg.Text("0", key="-KPI_PHOTOS-", font=("Arial", 24, "bold"), size=(10, 1))],
                ], pad=(10, 10), background_color="lightcyan"),
            ],
        ]
        return layout
    
    def create_watering_table_layout(self) -> List:
        """Create upcoming waterings table layout"""
        layout = [
            [sg.Text("⏳ UPCOMING WATERINGS (Next 7 days)", font=("Arial", 12, "bold"))],
            [sg.Text("_" * 80)],
            [sg.Table(
                values=[],
                headings=["ID", "Plant", "Last", "Days", "Status"],
                max_col_width=20,
                auto_size_columns=False,
                num_rows=5,
                key="-WATERING_TABLE-",
                display_row_numbers=False,
            )],
        ]
        return layout
    
    def create_fertilizing_table_layout(self) -> List:
        """Create upcoming fertilizing table layout"""
        layout = [
            [sg.Text("🧪 UPCOMING FERTILIZING (Next 7 days)", font=("Arial", 12, "bold"))],
            [sg.Text("_" * 80)],
            [sg.Table(
                values=[],
                headings=["ID", "Plant", "Last", "Days", "Status"],
                max_col_width=20,
                auto_size_columns=False,
                num_rows=5,
                key="-FERTILIZING_TABLE-",
                display_row_numbers=False,
            )],
        ]
        return layout
    
    def build_layout(self) -> List:
        """Build dashboard layout"""
        layout = [
            [sg.Text("📊 DASHBOARD - PLANT OVERVIEW", font=("Arial", 14, "bold"))],
            self.create_kpi_cards_layout(),
            [sg.Text("_" * 80)],
            self.create_watering_table_layout(),
            [sg.Text("_" * 80)],
            self.create_fertilizing_table_layout(),
            [sg.Text("_" * 80)],
            [
                sg.Button("Refresh", key="-REFRESH_BTN-"),
                sg.Button("Export (TODO)", key="-EXPORT_BTN-", disabled=True),
                sg.Button("Close", key="-CLOSE_BTN-"),
            ],
        ]
        return layout
    
    def show(self):
        """Show dashboard window"""
        layout = self.build_layout()
        self.window = sg.Window(
            "🌱 Dashboard - Plant Overview", 
            layout, 
            size=(900, 900), 
            finalize=True
        )
        
        # Initial load
        try:
            self._load_all_data()
        except Exception as e:
            sg.popup_error(f"❌ Failed to load dashboard data:\n{e}")
        
        while True:
            event, values = self.window.read(timeout=1000)
            
            if event == sg.WINDOW_CLOSED or event == "-CLOSE_BTN-":
                break
            
            if event == "-REFRESH_BTN-":
                try:
                    self._load_all_data()
                    sg.popup_ok("✅ Dashboard refreshed!", auto_close=True, auto_close_duration=1)
                except Exception as e:
                    sg.popup_error(f"❌ Refresh failed:\n{e}")
            
            try:
                self._handle_event(event, values)
            except Exception as e:
                print(f"Error handling event {event}: {e}")
        
        if self.window:
            self.window.close()
    
    def _load_all_data(self):
        """Load all dashboard data"""
        if self.window is None:
            return
            
        # Load KPIs
        try:
            stats = self.get_dashboard_stats()
            self._update_kpi_cards(stats)
        except Exception as e:
            print(f"❌ Error loading KPI stats: {e}")
            self._update_kpi_cards({})
        
        # Load tables
        try:
            waterings = self.get_upcoming_waterings(7)
            self._update_watering_table(waterings)
        except Exception as e:
            print(f"❌ Error loading waterings: {e}")
            self._update_watering_table([])
        
        try:
            fertilizing = self.get_upcoming_fertilizing(7)
            self._update_fertilizing_table(fertilizing)
        except Exception as e:
            print(f"❌ Error loading fertilizing: {e}")
            self._update_fertilizing_table([])
    
    def _update_kpi_cards(self, stats: Dict):
        """Update KPI card values"""
        try:
            self.window["-KPI_TOTAL-"].update(str(stats.get("total_plants", 0)))
            self.window["-KPI_ACTIVE-"].update(str(stats.get("active_plants", 0)))
            self.window["-KPI_ARCHIVED-"].update(str(stats.get("archived_plants", 0)))
            self.window["-KPI_EXCELLENT-"].update(str(stats.get("health_excellent", 0)))
            self.window["-KPI_GOOD-"].update(str(stats.get("health_good", 0)))
            self.window["-KPI_POOR-"].update(str(stats.get("health_poor", 0)))
            self.window["-KPI_PHOTOS-"].update(str(stats.get("total_photos", 0)))
        except Exception as e:
            print(f"❌ Error updating KPI cards: {e}")
    
    def _update_watering_table(self, waterings: List[Dict]):
        """Update watering table"""
        try:
            table_data = []
            if not waterings:
                table_data = [["—", "No upcoming waterings", "—", "—", "✅"]]
            else:
                for w in waterings:
                    table_data.append([
                        str(w.get("id", "?")),
                        w.get("name", "?"),
                        w.get("last_watered", "Never"),
                        str(w.get("days_since", "-")),
                        "⏳ NOW!" if w.get("days_since", 999) == 0 else "📅 Soon"
                    ])
            
            self.window["-WATERING_TABLE-"].update(values=table_data)
        except Exception as e:
            print(f"❌ Error updating watering table: {e}")
    
    def _update_fertilizing_table(self, fertilizing: List[Dict]):
        """Update fertilizing table"""
        try:
            table_data = []
            if not fertilizing:
                table_data = [["—", "No upcoming fertilizing", "—", "—", "✅"]]
            else:
                for f in fertilizing:
                    table_data.append([
                        str(f.get("id", "?")),
                        f.get("name", "?"),
                        f.get("last_fertilized", "Never"),
                        str(f.get("days_since", "-")),
                        "🧪 NOW!" if f.get("days_since", 999) == 0 else "📅 Soon"
                    ])
            
            self.window["-FERTILIZING_TABLE-"].update(values=table_data)
        except Exception as e:
            print(f"❌ Error updating fertilizing table: {e}")
    
    def _handle_event(self, event: str, values: Dict):
        """Handle dashboard events"""
        if event == "-EXPORT_BTN-":
            sg.popup("Export feature not implemented yet (Task 4.11)")


def main():
    """Run dashboard window"""
    dashboard = DashboardWindow()
    dashboard.show()


if __name__ == "__main__":
    main()

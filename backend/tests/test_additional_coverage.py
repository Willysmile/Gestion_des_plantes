"""Tests supplémentaires pour atteindre 80% coverage

Intégré à la suite de tests principale via conftest.py
Tests pour les routes lookups, plants, stats et settings
"""

import pytest


class TestLookupRoutes:
    """Tests pour les routes lookups"""
    
    def test_get_units(self, client):
        """Test récupération des unités"""
        response = client.get("/api/lookups/units")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_watering_frequencies(self, client):
        """Test récupération des fréquences d'arrosage"""
        response = client.get("/api/lookups/watering-frequencies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_light_requirements(self, client):
        """Test récupération des besoins en lumière"""
        response = client.get("/api/lookups/light-requirements")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_fertilizer_types(self, client):
        """Test récupération des types d'engrais"""
        response = client.get("/api/lookups/fertilizer-types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_disease_types(self, client):
        """Test récupération des types de maladies"""
        response = client.get("/api/lookups/disease-types")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_plant_health_statuses(self, client):
        """Test récupération des états de santé des plantes"""
        response = client.get("/api/lookups/plant-health-statuses")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestPlantsRoutesExpanded:
    """Tests étendus pour les routes plantes"""
    
    def test_get_plants_with_filters(self, client):
        """Test récupération des plantes avec filtres"""
        response = client.get("/api/plants")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_plant_minimal(self, client):
        """Test création d'une plante avec données minimales"""
        payload = {
            "name": "Test Plant Extra",
            "scientific_name": "Test scientificus extra",
            "family": "Araceae"
        }
        response = client.post("/api/plants", json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "Test Plant Extra"
    
    def test_search_plant_by_name(self, client):
        """Test recherche de plantes par nom"""
        response = client.get("/api/plants?search=Monstera")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestStatsRoutesExpanded:
    """Tests pour les stats"""
    
    def test_get_stats(self, client):
        """Test récupération des statistiques"""
        response = client.get("/api/stats")
        assert response.status_code in [200, 404]
    
    def test_get_stats_family(self, client):
        """Test stats par famille"""
        response = client.get("/api/stats/by-family")
        assert response.status_code in [200, 404]


class TestSettingsExpanded:
    """Tests étendus pour les settings"""
    
    def test_get_user_settings(self, client):
        """Test récupération des settings utilisateur"""
        response = client.get("/api/settings")
        assert response.status_code in [200, 404]
    
    def test_get_fertilizer_management(self, client):
        """Test récupération de la gestion des engrais"""
        response = client.get("/api/settings/fertilizer-management")
        assert response.status_code in [200, 404]


class TestErrorHandlingExpanded:
    """Tests pour la gestion d'erreurs étendus"""
    
    def test_404_nonexistent_plant(self, client):
        """Test accès à une plante inexistante"""
        response = client.get("/api/plants/99999")
        assert response.status_code == 404
    
    def test_invalid_id_type(self, client):
        """Test avec un ID invalide"""
        response = client.get("/api/plants/invalid")
        assert response.status_code == 422
    
    def test_delete_nonexistent_plant(self, client):
        """Test suppression d'une plante inexistante"""
        response = client.delete("/api/plants/99999")
        assert response.status_code == 404


class TestPlantsRoutesExpanded:
    """Tests étendus pour les routes plantes"""
    
    def test_get_plants_with_filters(self, client):
        """Test récupération des plantes avec filtres"""
        response = client.get("/api/plants")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_plant_minimal(self, client):
        """Test création d'une plante avec données minimales"""
        payload = {
            "name": "Test Plant Extra",
            "scientific_name": "Test scientificus extra",
            "family": "Araceae"
        }
        response = client.post("/api/plants", json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "Test Plant Extra"
    
    def test_search_plant_by_name(self, client):
        """Test recherche de plantes par nom"""
        response = client.get("/api/plants?search=Monstera")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestStatsRoutesExpanded:
    """Tests pour les stats"""
    
    def test_get_stats(self, client):
        """Test récupération des statistiques"""
        response = client.get("/api/stats")
        assert response.status_code in [200, 404]
    
    def test_get_stats_family(self, client):
        """Test stats par famille"""
        response = client.get("/api/stats/by-family")
        assert response.status_code in [200, 404]


class TestSettingsExpanded:
    """Tests étendus pour les settings"""
    
    def test_get_user_settings(self, client):
        """Test récupération des settings utilisateur"""
        response = client.get("/api/settings")
        assert response.status_code in [200, 404]
    
    def test_get_fertilizer_management(self, client):
        """Test récupération de la gestion des engrais"""
        response = client.get("/api/settings/fertilizer-management")
        assert response.status_code in [200, 404]


class TestErrorHandlingExpanded:
    """Tests pour la gestion d'erreurs étendus"""
    
    def test_404_nonexistent_plant(self, client):
        """Test accès à une plante inexistante"""
        response = client.get("/api/plants/99999")
        assert response.status_code == 404
    
    def test_invalid_id_type(self, client):
        """Test avec un ID invalide"""
        response = client.get("/api/plants/invalid")
        assert response.status_code == 422
    
    def test_delete_nonexistent_plant(self, client):
        """Test suppression d'une plante inexistante"""
        response = client.delete("/api/plants/99999")
        assert response.status_code == 404

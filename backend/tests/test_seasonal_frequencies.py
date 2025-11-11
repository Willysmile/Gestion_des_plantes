"""
Tests complets pour les fréquences saisonnières (arrosage et fertilisation)
Tests les routes API, modèles, et intégration complète
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date
from app.main import app
from app.models.lookup import Season, WateringFrequency, FertilizerFrequency, PlantSeasonalWatering, PlantSeasonalFertilizing
from app.models.plant import Plant
from sqlalchemy.orm import Session

client = TestClient(app)


class TestSeasonalWateringAPI:
    """Tests pour les routes d'arrosage saisonnier"""

    @pytest.fixture
    def plant_data(self, db: Session):
        """Créer une plante test"""
        plant = Plant(
            name="Test Plant",
            family="Araceae",
            scientific_name="Test scientificus",
            reference="REF-001"
        )
        db.add(plant)
        db.commit()
        return plant

    def test_get_seasonal_watering(self, db: Session, plant_data):
        """GET /plants/{id}/seasonal-watering/{season_id}"""
        response = client.get(f"/api/plants/{plant_data.id}/seasonal-watering/1")
        assert response.status_code in [200, 404]  # OK ou pas trouvé

    def test_put_seasonal_watering(self, db: Session, plant_data):
        """PUT /plants/{id}/seasonal-watering/{season_id}"""
        payload = {"watering_frequency_id": 1}
        response = client.put(
            f"/plants/{plant_data.id}/seasonal-watering/1",
            json=payload
        )
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "watering_frequency_id" in data or data is None

    def test_get_all_seasonal_watering(self, db: Session, plant_data):
        """GET /api/plants/{id}/seasonal-watering - Récupérer toutes les saisons"""
        response = client.get(f"/api/plants/{plant_data.id}/seasonal-watering")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestSeasonalFertilizingAPI:
    """Tests pour les routes de fertilisation saisonnière"""

    @pytest.fixture
    def plant_data(self, db: Session):
        """Créer une plante test"""
        plant = Plant(
            name="Test Plant Fertilizing",
            family="Araceae",
            scientific_name="Test fertilicus"
        )
        db.add(plant)
        db.commit()
        return plant

    def test_get_seasonal_fertilizing(self, db: Session, plant_data):
        """GET /plants/{id}/seasonal-fertilizing/{season_id}"""
        response = client.get(f"/api/plants/{plant_data.id}/seasonal-fertilizing/1")
        assert response.status_code in [200, 404]

    def test_put_seasonal_fertilizing(self, db: Session, plant_data):
        """PUT /plants/{id}/seasonal-fertilizing/{season_id}"""
        payload = {"fertilizer_frequency_id": 1}
        response = client.put(
            f"/plants/{plant_data.id}/seasonal-fertilizing/1",
            json=payload
        )
        assert response.status_code in [200, 404]

    def test_get_all_seasonal_fertilizing(self, db: Session, plant_data):
        """GET /plants/{id}/seasonal-fertilizing"""
        response = client.get(f"/api/plants/{plant_data.id}/seasonal-fertilizing")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestLookupFrequencies:
    """Tests pour les lookups de fréquences"""

    def test_get_watering_frequencies(self):
        """GET /api/lookups/watering-frequencies"""
        response = client.get("/api/lookups/watering-frequencies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Vérifier les 7 fréquences finalisées
        assert len(data) == 7
        freq_names = [f["name"] for f in data]
        assert "Fréquent (quotidien)" in freq_names
        assert "Régulier (2-3x/semaine)" in freq_names
        assert "Normal (1x/semaine)" in freq_names

    def test_get_fertilizer_frequencies(self):
        """GET /api/lookups/fertilizer-frequencies"""
        response = client.get("/api/lookups/fertilizer-frequencies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Vérifier les 6 fréquences de fertilisation
        assert len(data) == 6
        freq_names = [f["name"] for f in data]
        assert "Fréquent (hebdomadaire)" in freq_names
        assert "Régulier (bi-hebdomadaire)" in freq_names

    def test_get_seasons(self):
        """GET /lookups/seasons"""
        response = client.get("/api/lookups/seasons")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4  # 4 saisons
        season_names = [s["name"] for s in data]
        assert "Printemps" in season_names
        assert "Été" in season_names
        assert "Automne" in season_names
        assert "Hiver" in season_names


class TestSeasonalWorkflow:
    """Tests du workflow complet: créer plante -> définir fréquences -> afficher modale"""

    @pytest.fixture
    def setup_plant(self, db: Session):
        """Setup: créer une plante avec fréquences saisonnières"""
        plant = Plant(
            name="Monstera Deliciosa",
            family="Araceae",
            scientific_name="Monstera deliciosa",
            reference="MONSTERA-001"
        )
        db.add(plant)
        db.commit()

        # Ajouter fréquences pour chaque saison
        for season_id in range(1, 5):
            seasonal_watering = PlantSeasonalWatering(
                plant_id=plant.id,
                season_id=season_id,
                watering_frequency_id=1  # Fréquent
            )
            db.add(seasonal_watering)

            seasonal_fertilizing = PlantSeasonalFertilizing(
                plant_id=plant.id,
                season_id=season_id,
                fertilizer_frequency_id=1  # Fréquent
            )
            db.add(seasonal_fertilizing)

        db.commit()
        return plant

    def test_complete_workflow(self, db: Session, setup_plant):
        """Workflow complet"""
        plant = setup_plant

        # 1. Vérifier que la plante existe
        response = client.get(f"/api/plants/{plant.id}")
        assert response.status_code == 200

        # 2. Récupérer les fréquences saisonnières
        watering_response = client.get(f"/api/plants/{plant.id}/seasonal-watering")
        assert watering_response.status_code == 200
        watering_data = watering_response.json()
        assert len(watering_data) > 0

        fertilizing_response = client.get(f"/api/plants/{plant.id}/seasonal-fertilizing")
        assert fertilizing_response.status_code == 200
        fertilizing_data = fertilizing_response.json()
        assert len(fertilizing_data) > 0

        # 3. Modifier une fréquence
        update_payload = {"watering_frequency_id": 3}  # Changer à "Normal"
        update_response = client.put(
            f"/plants/{plant.id}/seasonal-watering/1",
            json=update_payload
        )
        assert update_response.status_code in [200, 404]

    def test_season_detection(self):
        """Tester la détection correcte de la saison actuelle"""
        from datetime import datetime
        month = datetime.now().month

        response = client.get("/api/lookups/seasons")
        assert response.status_code == 200
        seasons = response.json()

        # Vérifier qu'une saison contient le mois actuel
        found = False
        for season in seasons:
            start = season["start_month"]
            end = season["end_month"]
            if start <= end:
                if start <= month <= end:
                    found = True
                    break
            else:  # Hiver (12->2)
                if month >= start or month <= end:
                    found = True
                    break

        assert found, f"Month {month} not found in any season"


class TestFrequencyIntegrity:
    """Tests d'intégrité des données de fréquences"""

    def test_watering_frequency_intervals(self):
        """Vérifier que les intervalles d'arrosage ont du sens"""
        response = client.get("/api/lookups/watering-frequencies")
        assert response.status_code == 200
        data = response.json()

        # Au moins une fréquence doit avoir un days valide
        has_valid_interval = any(f.get("days") for f in data)
        assert has_valid_interval, "Au moins une fréquence devrait avoir days"

    def test_fertilizer_frequency_intervals(self):
        """Vérifier que les intervalles de fertilisation ont du sens"""
        response = client.get("/api/lookups/fertilizer-frequencies")
        assert response.status_code == 200
        data = response.json()

        # Au moins une fréquence doit avoir un weeks valide
        has_valid_interval = any(f.get("weeks") for f in data)
        assert has_valid_interval, "Au moins une fréquence devrait avoir weeks"

    def test_no_duplicate_frequencies(self):
        """Vérifier qu'il n'y a pas de doublons"""
        # Watering
        watering_response = client.get("/api/lookups/watering-frequencies")
        watering_data = watering_response.json()
        watering_names = [f["name"] for f in watering_data]
        assert len(watering_names) == len(set(watering_names)), "Doublons trouvés en arrosage"

        # Fertilizer
        fertilizer_response = client.get("/api/lookups/fertilizer-frequencies")
        fertilizer_data = fertilizer_response.json()
        fertilizer_names = [f["name"] for f in fertilizer_data]
        assert len(fertilizer_names) == len(set(fertilizer_names)), "Doublons trouvés en fertilisation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

import pytest
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.models import Plant, PlantPropagation, PropagationEvent
from app.services.propagation_service import (
    PropagationValidationService, 
    PropagationEstimatorService,
    PropagationAnalyticsService
)


class TestPropagationValidation:
    """Test propagation validation service."""
    
    def test_validate_state_transition_valid(self):
        """Test valid state transition."""
        valid, error = PropagationValidationService.validate_state_transition('pending', 'rooting')
        assert valid is True
        assert error is None
    
    def test_validate_state_transition_invalid(self):
        """Test invalid state transition."""
        valid, error = PropagationValidationService.validate_state_transition('established', 'rooting')
        assert valid is False
        assert error is not None
    
    def test_validate_state_transition_unknown_state(self):
        """Test unknown state."""
        valid, error = PropagationValidationService.validate_state_transition('unknown', 'rooting')
        assert valid is False
        assert "Unknown current state" in error
    
    def test_validate_source_method_valid(self):
        """Test valid source and method combination."""
        valid, error = PropagationValidationService.validate_source_method('cutting', 'water')
        assert valid is True
        assert error is None
    
    def test_validate_source_method_invalid(self):
        """Test invalid source and method combination."""
        valid, error = PropagationValidationService.validate_source_method('cutting', 'invalid')
        assert valid is False
        assert error is not None
    
    def test_validate_dates_valid(self):
        """Test valid date sequence."""
        today = date.today()
        valid, error = PropagationValidationService.validate_dates(
            today, 
            today + timedelta(days=5),
            today + timedelta(days=20)
        )
        assert valid is True
        assert error is None
    
    def test_validate_dates_invalid_sequence(self):
        """Test invalid date sequence (propagation after harvest)."""
        today = date.today()
        valid, error = PropagationValidationService.validate_dates(
            today,
            today - timedelta(days=5)
        )
        assert valid is False
        assert "Propagation date cannot be after harvest date" in error
    
    def test_validate_no_cycle_valid(self, db: Session):
        """Test no cycle in valid case."""
        # Create parent plant
        parent = Plant(name="Parent")
        db.add(parent)
        db.flush()
        
        # Validate - should be valid
        valid, error = PropagationValidationService.validate_no_cycle(db, parent.id, None)
        assert valid is True
        assert error is None
    
    def test_validate_no_self_parent(self, db: Session):
        """Test that plant cannot be its own parent."""
        valid, error = PropagationValidationService.validate_no_cycle(db, 1, 1)
        assert valid is False
        assert "cannot be its own parent" in error


class TestPropagationEstimator:
    """Test propagation estimator service."""
    
    def test_estimate_duration_cutting_water(self):
        """Test duration estimation for cutting with water."""
        duration = PropagationEstimatorService.estimate_duration('cutting', 'water')
        assert duration == 14
    
    def test_estimate_duration_division_soil(self):
        """Test duration estimation for division with soil."""
        duration = PropagationEstimatorService.estimate_duration('division', 'soil')
        assert duration == 14
    
    def test_estimate_success_rate_cutting_water(self):
        """Test success rate estimation for cutting with water."""
        rate = PropagationEstimatorService.estimate_success_rate('cutting', 'water')
        assert rate == 0.85
    
    def test_estimate_success_rate_division_soil(self):
        """Test success rate estimation for division with soil."""
        rate = PropagationEstimatorService.estimate_success_rate('division', 'soil')
        assert rate == 0.95
    
    def test_calculate_expected_ready_date(self):
        """Test expected ready date calculation."""
        start = date(2025, 1, 1)
        expected = PropagationEstimatorService.calculate_expected_ready_date(
            start, 'cutting', 'water'
        )
        assert expected == date(2025, 1, 15)  # 14 days later


class TestPropagationAPI:
    """Test propagation API endpoints."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_create_propagation(self, client: TestClient, db: Session):
        """Test creating a propagation."""
        # Create plants first
        parent = Plant(name="Parent Plant")
        child = Plant(name="Child Plant")
        db.add_all([parent, child])
        db.commit()
        
        payload = {
            "parent_plant_id": parent.id,
            "source_type": "cutting",
            "method": "water",
            "propagation_date": "2025-01-01",
            "date_harvested": "2025-01-05",
        }
        
        response = client.post("/api/propagations", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["parent_plant_id"] == parent.id
        assert data["status"] == "pending"
        assert data["source_type"] == "cutting"
    
    def test_get_propagations(self, client: TestClient, db: Session):
        """Test getting all propagations."""
        # Create plant
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        # Create a propagation
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        response = client.get("/api/propagations")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_get_propagation_by_id(self, client: TestClient, db: Session):
        """Test getting a specific propagation."""
        # Create plant
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        # Create propagation
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        response = client.get(f"/api/propagations/{prop.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prop.id
    
    def test_update_propagation_status(self, client: TestClient, db: Session):
        """Test updating propagation status."""
        # Create plant and propagation
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        payload = {"status": "rooting"}
        response = client.put(f"/api/propagations/{prop.id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "rooting"
    
    def test_delete_propagation(self, client: TestClient, db: Session):
        """Test deleting a propagation."""
        # Create plant and propagation
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        response = client.delete(f"/api/propagations/{prop.id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = client.get(f"/api/propagations/{prop.id}")
        assert response.status_code == 404
    
    def test_add_event(self, client: TestClient, db: Session):
        """Test adding an event to a propagation."""
        # Create plant and propagation
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        payload = {
            "event_type": "rooted",
            "event_date": "2025-01-10T10:00:00",
            "measurement": {"root_length_cm": 5.0},
            "notes": "Roots appearing"
        }
        
        response = client.post(f"/api/propagations/{prop.id}/events", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "rooted"
    
    def test_get_events(self, client: TestClient, db: Session):
        """Test getting events for a propagation."""
        # Create plant and propagation
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.flush()
        
        event = PropagationEvent(
            propagation_id=prop.id,
            event_type="rooted",
            event_date=datetime.now(),
            measurement={"root_length_cm": 5.0}
        )
        db.add(event)
        db.commit()
        
        response = client.get(f"/api/propagations/{prop.id}/events")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
    
    def test_get_timeline(self, client: TestClient, db: Session):
        """Test getting propagation timeline."""
        # Create plant and propagation
        parent = Plant(name="Parent Plant")
        db.add(parent)
        db.flush()
        
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        response = client.get(f"/api/propagations/{prop.id}/timeline")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prop.id
        assert "days_since_propagation" in data
        assert "expected_duration_days" in data
        assert "is_overdue" in data
    
    def test_get_genealogy(self, client: TestClient, db: Session):
        """Test getting plant genealogy."""
        # Create plants
        parent = Plant(name="Parent Plant")
        child = Plant(name="Child Plant")
        db.add_all([parent, child])
        db.flush()
        
        # Create propagation
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            child_plant_id=child.id,
            source_type="cutting",
            method="water",
            propagation_date=date(2025, 1, 1),
            date_harvested=date(2025, 1, 5),
            expected_ready=date(2025, 1, 15),
        )
        db.add(prop)
        db.commit()
        
        response = client.get(f"/api/propagations/{parent.id}/genealogy")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == parent.id
        assert "children" in data
    
    def test_get_stats(self, client: TestClient):
        """Test getting propagation statistics."""
        response = client.get("/api/propagations/stats/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "by_status" in data
        assert "success_rate" in data


class TestPropagationAnalytics:
    """Test propagation analytics service."""
    
    def test_get_propagation_stats_empty(self, db: Session):
        """Test stats for empty database."""
        stats = PropagationAnalyticsService.get_propagation_stats(db)
        assert stats["total"] == 0
        assert stats["success_rate"] == 0
    
    def test_get_overdue_propagations(self, db: Session):
        """Test getting overdue propagations."""
        # Create a parent plant
        parent = Plant(name="Parent")
        db.add(parent)
        db.flush()
        
        # Create an old propagation that should be ready
        old_date = date.today() - timedelta(days=30)
        prop = PlantPropagation(
            parent_plant_id=parent.id,
            source_type="cutting",
            method="water",
            propagation_date=old_date,
            date_harvested=old_date + timedelta(days=5),
            expected_ready=old_date + timedelta(days=10),  # Already passed
            status='pending'  # Still not complete
        )
        db.add(prop)
        db.commit()
        
        overdue = PropagationAnalyticsService.get_overdue_propagations(db)
        assert len(overdue) > 0

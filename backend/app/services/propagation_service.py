from datetime import datetime, date, timedelta
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import PlantPropagation, PropagationEvent, Plant


class PropagationValidationService:
    """Service for validating propagation operations (anti-cycle, state transitions, etc.)."""
    
    # Valid state transitions (from -> to)
    VALID_TRANSITIONS = {
        'pending': ['rooting', 'failed', 'abandoned'],
        'rooting': ['rooted', 'failed', 'abandoned'],
        'rooted': ['growing', 'ready-to-pot', 'failed', 'abandoned'],
        'growing': ['ready-to-pot', 'failed', 'abandoned'],
        'ready-to-pot': ['potted', 'failed', 'abandoned'],
        'potted': ['transplanted', 'established', 'failed', 'abandoned'],
        'transplanted': ['established', 'failed', 'abandoned'],
        'established': ['failed', 'abandoned'],
        'failed': [],
        'abandoned': [],
    }
    
    # Valid combinations of source_type and method
    VALID_COMBINATIONS = {
        'cutting': ['water', 'soil', 'air-layer', 'substrate'],
        'seeds': ['water', 'soil', 'substrate'],
        'division': ['soil', 'substrate'],
        'offset': ['water', 'soil'],
    }
    
    @staticmethod
    def validate_state_transition(current_state: str, new_state: str) -> Tuple[bool, Optional[str]]:
        """Check if state transition is valid."""
        if current_state not in PropagationValidationService.VALID_TRANSITIONS:
            return False, f"Unknown current state: {current_state}"
        
        valid_next_states = PropagationValidationService.VALID_TRANSITIONS[current_state]
        if new_state not in valid_next_states:
            return False, f"Cannot transition from {current_state} to {new_state}"
        
        return True, None
    
    @staticmethod
    def validate_source_method(source_type: str, method: str) -> Tuple[bool, Optional[str]]:
        """Check if source_type and method combination is valid."""
        if source_type not in PropagationValidationService.VALID_COMBINATIONS:
            return False, f"Unknown source type: {source_type}"
        
        valid_methods = PropagationValidationService.VALID_COMBINATIONS[source_type]
        if method not in valid_methods:
            return False, f"Method '{method}' not valid for source type '{source_type}'"
        
        return True, None
    
    @staticmethod
    def validate_no_cycle(db: Session, parent_plant_id: int, child_plant_id: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate that propagation doesn't create a cycle in the plant genealogy.
        Anti-cycle validation: Check if parent is already a descendant of child.
        """
        if not child_plant_id:
            return True, None
        
        if parent_plant_id == child_plant_id:
            return False, "A plant cannot be its own parent"
        
        # Get all descendants of child_plant_id
        descendants = PropagationValidationService._get_all_descendants(db, child_plant_id)
        
        if parent_plant_id in descendants:
            return False, f"Plant {parent_plant_id} is already a descendant of plant {child_plant_id}. This would create a cycle."
        
        return True, None
    
    @staticmethod
    def _get_all_descendants(db: Session, plant_id: int) -> set:
        """Get all descendants of a plant through propagation relationships."""
        descendants = set()
        to_check = [plant_id]
        
        while to_check:
            current_id = to_check.pop(0)
            
            # Find all children of current plant (where current_id is parent)
            children = db.query(PlantPropagation.child_plant_id).filter(
                and_(
                    PlantPropagation.parent_plant_id == current_id,
                    PlantPropagation.child_plant_id.isnot(None)
                )
            ).all()
            
            for (child_id,) in children:
                if child_id not in descendants:
                    descendants.add(child_id)
                    to_check.append(child_id)
        
        return descendants
    
    @staticmethod
    def validate_dates(propagation_date: date, date_harvested: date, expected_ready: Optional[date] = None) -> Tuple[bool, Optional[str]]:
        """Validate date logic."""
        if propagation_date > date_harvested:
            return False, "Propagation date cannot be after harvest date"
        
        if expected_ready and date_harvested > expected_ready:
            return False, "Expected ready date cannot be before harvest date"
        
        return True, None


class PropagationEstimatorService:
    """Service for estimating propagation duration and success rates."""
    
    # Duration estimates in days
    DURATION_ESTIMATES = {
        ('cutting', 'water'): 14,
        ('cutting', 'soil'): 21,
        ('cutting', 'air-layer'): 30,
        ('cutting', 'substrate'): 21,
        ('seeds', 'water'): 21,
        ('seeds', 'soil'): 28,
        ('seeds', 'substrate'): 28,
        ('division', 'soil'): 14,
        ('division', 'substrate'): 14,
        ('offset', 'water'): 10,
        ('offset', 'soil'): 14,
    }
    
    # Success rate estimates (0-1 scale)
    SUCCESS_ESTIMATES = {
        ('cutting', 'water'): 0.85,
        ('cutting', 'soil'): 0.80,
        ('cutting', 'air-layer'): 0.95,
        ('cutting', 'substrate'): 0.75,
        ('seeds', 'water'): 0.70,
        ('seeds', 'soil'): 0.75,
        ('seeds', 'substrate'): 0.72,
        ('division', 'soil'): 0.95,
        ('division', 'substrate'): 0.90,
        ('offset', 'water'): 0.90,
        ('offset', 'soil'): 0.88,
    }
    
    @staticmethod
    def estimate_duration(source_type: str, method: str) -> int:
        """Estimate duration in days for a propagation method."""
        return PropagationEstimatorService.DURATION_ESTIMATES.get(
            (source_type, method), 21
        )
    
    @staticmethod
    def estimate_success_rate(source_type: str, method: str) -> float:
        """Estimate success rate (0-1) for a propagation method."""
        return PropagationEstimatorService.SUCCESS_ESTIMATES.get(
            (source_type, method), 0.80
        )
    
    @staticmethod
    def calculate_expected_ready_date(propagation_date: date, source_type: str, method: str) -> date:
        """Calculate expected ready date based on duration estimate."""
        duration = PropagationEstimatorService.estimate_duration(source_type, method)
        return propagation_date + timedelta(days=duration)


class PropagationAnalyticsService:
    """Service for analyzing propagation data and providing statistics."""
    
    @staticmethod
    def get_propagation_stats(db: Session, parent_plant_id: Optional[int] = None) -> Dict[str, Any]:
        """Get statistics about propagations."""
        query = db.query(PlantPropagation)
        
        if parent_plant_id:
            query = query.filter(PlantPropagation.parent_plant_id == parent_plant_id)
        
        propagations = query.all()
        
        if not propagations:
            return {
                'total': 0,
                'by_status': {},
                'by_source_type': {},
                'by_method': {},
                'success_rate': 0,
                'average_duration_days': 0,
            }
        
        # Count by status
        status_counts = {}
        for prop in propagations:
            status_counts[prop.status] = status_counts.get(prop.status, 0) + 1
        
        # Count by source type
        source_counts = {}
        for prop in propagations:
            source_counts[prop.source_type] = source_counts.get(prop.source_type, 0) + 1
        
        # Count by method
        method_counts = {}
        for prop in propagations:
            method_counts[prop.method] = method_counts.get(prop.method, 0) + 1
        
        # Calculate success rate
        successful = len([p for p in propagations if p.status in ['established']])
        total = len(propagations)
        success_rate = (successful / total) if total > 0 else 0
        
        # Calculate average duration
        completed = [p for p in propagations if p.success_date]
        avg_duration = 0
        if completed:
            durations = [(p.success_date - p.propagation_date).days for p in completed]
            avg_duration = sum(durations) / len(durations)
        
        return {
            'total': total,
            'by_status': status_counts,
            'by_source_type': source_counts,
            'by_method': method_counts,
            'success_rate': round(success_rate, 2),
            'average_duration_days': round(avg_duration, 1),
        }
    
    @staticmethod
    def get_overdue_propagations(db: Session) -> List[PlantPropagation]:
        """Get all propagations that are overdue for their expected ready date."""
        today = datetime.utcnow().date()
        
        propagations = db.query(PlantPropagation).filter(
            and_(
                PlantPropagation.status.notin_(['established', 'failed', 'abandoned']),
                PlantPropagation.expected_ready.isnot(None),
                PlantPropagation.expected_ready < today
            )
        ).all()
        
        return propagations
    
    @staticmethod
    def get_genealogy_tree(db: Session, plant_id: int, include_parents: bool = True, include_children: bool = True) -> Dict[str, Any]:
        """Get genealogy tree for a plant (parents and children)."""
        tree = {
            'id': plant_id,
            'parents': [],
            'children': [],
        }
        
        if include_parents:
            # Get all propagations where this plant is the child
            parent_propagations = db.query(PlantPropagation).filter(
                PlantPropagation.child_plant_id == plant_id
            ).all()
            
            for prop in parent_propagations:
                tree['parents'].append({
                    'plant_id': prop.parent_plant_id,
                    'propagation_id': prop.id,
                    'source_type': prop.source_type,
                    'method': prop.method,
                    'propagation_date': prop.propagation_date.isoformat() if prop.propagation_date else None,
                    'status': prop.status,
                })
        
        if include_children:
            # Get all propagations where this plant is the parent
            child_propagations = db.query(PlantPropagation).filter(
                and_(
                    PlantPropagation.parent_plant_id == plant_id,
                    PlantPropagation.child_plant_id.isnot(None)
                )
            ).all()
            
            for prop in child_propagations:
                tree['children'].append({
                    'plant_id': prop.child_plant_id,
                    'propagation_id': prop.id,
                    'source_type': prop.source_type,
                    'method': prop.method,
                    'propagation_date': prop.propagation_date.isoformat() if prop.propagation_date else None,
                    'status': prop.status,
                })
        
        return tree

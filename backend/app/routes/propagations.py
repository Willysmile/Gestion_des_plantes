from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from app.utils.db import get_db
from app.models import PlantPropagation, PropagationEvent, Plant
from app.schemas.propagation import (
    PlantPropagationCreate, PlantPropagationUpdate, PlantPropagationResponse,
    PropagationEventCreate, PropagationEventUpdate, PropagationEventResponse,
    PropagationTimelineResponse, PropagationConversionRequest, PropagationStatsResponse,
    GenealogyTreeResponse, PropagationCalendarEvent
)
from app.services.propagation_service import (
    PropagationValidationService, PropagationEstimatorService, PropagationAnalyticsService
)

router = APIRouter(prefix="/api/propagations", tags=["propagations"])


# ============================================================================
# CRUD OPERATIONS
# ============================================================================

@router.get("", response_model=List[PlantPropagationResponse])
def get_propagations(
    db: Session = Depends(get_db),
    parent_plant_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
):
    """Get all propagations with optional filters."""
    query = db.query(PlantPropagation)
    
    if parent_plant_id:
        query = query.filter(PlantPropagation.parent_plant_id == parent_plant_id)
    
    if status:
        query = query.filter(PlantPropagation.status == status)
    
    propagations = query.offset(skip).limit(limit).all()
    return propagations


@router.post("", response_model=PlantPropagationResponse, status_code=status.HTTP_201_CREATED)
def create_propagation(
    propagation: PlantPropagationCreate,
    db: Session = Depends(get_db),
):
    """Create a new propagation."""
    # Validate parent plant exists
    parent = db.query(Plant).filter(Plant.id == propagation.parent_plant_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail=f"Parent plant {propagation.parent_plant_id} not found")
    
    # Validate child plant exists if provided
    if propagation.child_plant_id:
        child = db.query(Plant).filter(Plant.id == propagation.child_plant_id).first()
        if not child:
            raise HTTPException(status_code=404, detail=f"Child plant {propagation.child_plant_id} not found")
    
    # Validate source_type and method combination
    valid, error = PropagationValidationService.validate_source_method(propagation.source_type, propagation.method)
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Validate no cycle
    valid, error = PropagationValidationService.validate_no_cycle(
        db, propagation.parent_plant_id, propagation.child_plant_id
    )
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Validate dates
    valid, error = PropagationValidationService.validate_dates(
        propagation.propagation_date, propagation.date_harvested, propagation.expected_ready
    )
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Create propagation
    db_propagation = PlantPropagation(
        parent_plant_id=propagation.parent_plant_id,
        child_plant_id=propagation.child_plant_id,
        source_type=propagation.source_type,
        method=propagation.method,
        propagation_date=propagation.propagation_date,
        date_harvested=propagation.date_harvested,
        expected_ready=propagation.expected_ready or PropagationEstimatorService.calculate_expected_ready_date(
            propagation.propagation_date,
            propagation.source_type,
            propagation.method
        ),
        status='pending',
        success_rate_estimate=propagation.success_rate_estimate or PropagationEstimatorService.estimate_success_rate(
            propagation.source_type, propagation.method
        ),
        notes=propagation.notes,
    )
    
    db.add(db_propagation)
    db.commit()
    db.refresh(db_propagation)
    return db_propagation


@router.get("/{propagation_id}", response_model=PlantPropagationResponse)
def get_propagation(propagation_id: int, db: Session = Depends(get_db)):
    """Get a specific propagation."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    return propagation


@router.put("/{propagation_id}", response_model=PlantPropagationResponse)
def update_propagation(
    propagation_id: int,
    update_data: PlantPropagationUpdate,
    db: Session = Depends(get_db),
):
    """Update a propagation."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    
    # Validate state transition if status is being changed
    if update_data.status and update_data.status != propagation.status:
        valid, error = PropagationValidationService.validate_state_transition(propagation.status, update_data.status)
        if not valid:
            raise HTTPException(status_code=400, detail=error)
    
    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(propagation, key, value)
    
    db.commit()
    db.refresh(propagation)
    return propagation


@router.delete("/{propagation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_propagation(propagation_id: int, db: Session = Depends(get_db)):
    """Delete a propagation."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    
    db.delete(propagation)
    db.commit()


# ============================================================================
# EVENTS
# ============================================================================

@router.post("/{propagation_id}/events", response_model=PropagationEventResponse, status_code=status.HTTP_201_CREATED)
def add_event(
    propagation_id: int,
    event: PropagationEventCreate,
    db: Session = Depends(get_db),
):
    """Add an event to a propagation."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    
    db_event = PropagationEvent(
        propagation_id=propagation_id,
        event_date=event.event_date,
        event_type=event.event_type,
        measurement=event.measurement,
        notes=event.notes,
        photo_url=event.photo_url,
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/{propagation_id}/events", response_model=List[PropagationEventResponse])
def get_events(propagation_id: int, db: Session = Depends(get_db)):
    """Get all events for a propagation."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    
    return propagation.events


# ============================================================================
# TIMELINE & TRACKING
# ============================================================================

@router.get("/{propagation_id}/timeline", response_model=PropagationTimelineResponse)
def get_timeline(propagation_id: int, db: Session = Depends(get_db)):
    """Get timeline view of a propagation (with calculated fields)."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    
    return PropagationTimelineResponse(
        id=propagation.id,
        parent_plant_id=propagation.parent_plant_id,
        child_plant_id=propagation.child_plant_id,
        source_type=propagation.source_type,
        method=propagation.method,
        status=propagation.status,
        propagation_date=propagation.propagation_date,
        date_harvested=propagation.date_harvested,
        expected_ready=propagation.expected_ready,
        success_date=propagation.success_date,
        days_since_propagation=propagation.days_since_propagation,
        expected_duration_days=propagation.expected_duration_days,
        is_overdue=propagation.is_overdue,
        success_rate_estimate=propagation.success_rate_estimate,
        notes=propagation.notes,
    )


# ============================================================================
# CONVERSION (Propagation -> Plant)
# ============================================================================

@router.post("/{propagation_id}/convert", response_model=PlantPropagationResponse)
def convert_to_plant(
    propagation_id: int,
    conversion: PropagationConversionRequest,
    db: Session = Depends(get_db),
):
    """Convert a propagation to an established plant."""
    propagation = db.query(PlantPropagation).filter(PlantPropagation.id == propagation_id).first()
    if not propagation:
        raise HTTPException(status_code=404, detail="Propagation not found")
    
    # Check if child plant exists
    child = db.query(Plant).filter(Plant.id == conversion.child_plant_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child plant not found")
    
    # Validate no cycle
    valid, error = PropagationValidationService.validate_no_cycle(
        db, propagation.parent_plant_id, conversion.child_plant_id
    )
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Update propagation
    propagation.child_plant_id = conversion.child_plant_id
    propagation.status = 'established'
    propagation.success_date = conversion.success_date or date.today()
    
    db.commit()
    db.refresh(propagation)
    return propagation


# ============================================================================
# GENEALOGY
# ============================================================================

@router.get("/{plant_id}/genealogy", response_model=GenealogyTreeResponse)
def get_genealogy(plant_id: int, db: Session = Depends(get_db)):
    """Get genealogy tree for a plant (parents and children)."""
    tree = PropagationAnalyticsService.get_genealogy_tree(db, plant_id)
    return GenealogyTreeResponse(
        id=tree['id'],
        parents=tree['parents'],
        children=tree['children'],
    )


# ============================================================================
# STATISTICS & ANALYTICS
# ============================================================================

@router.get("/stats/overview", response_model=PropagationStatsResponse)
def get_stats_overview(
    parent_plant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Get statistics about propagations."""
    stats = PropagationAnalyticsService.get_propagation_stats(db, parent_plant_id)
    return PropagationStatsResponse(**stats)


@router.get("/alerts/overdue", response_model=List[PlantPropagationResponse])
def get_overdue_propagations(db: Session = Depends(get_db)):
    """Get all propagations that are overdue for their expected ready date."""
    overdue = PropagationAnalyticsService.get_overdue_propagations(db)
    return overdue


# ============================================================================
# CALENDAR
# ============================================================================

@router.get("/calendar/month", response_model=List[PropagationCalendarEvent])
def get_calendar_events(
    year: int = Query(...),
    month: int = Query(...),
    db: Session = Depends(get_db),
):
    """Get propagation events for a specific month."""
    from datetime import datetime
    
    # Calculate date range
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    # Get all propagations with dates in this month
    propagations = db.query(PlantPropagation).filter(
        (PlantPropagation.propagation_date >= start_date) |
        (PlantPropagation.expected_ready >= start_date) |
        (PlantPropagation.success_date >= start_date)
    ).all()
    
    events = []
    for prop in propagations:
        events.append(PropagationCalendarEvent(
            id=prop.id,
            parent_plant_id=prop.parent_plant_id,
            child_plant_id=prop.child_plant_id,
            source_type=prop.source_type,
            method=prop.method,
            status=prop.status,
            propagation_date=prop.propagation_date,
            expected_ready=prop.expected_ready,
            success_date=prop.success_date,
            is_overdue=prop.is_overdue,
        ))
    
    return events


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

@router.post("/batch/create", response_model=List[PlantPropagationResponse], status_code=status.HTTP_201_CREATED)
def batch_create_propagations(
    propagations: List[PlantPropagationCreate],
    db: Session = Depends(get_db),
):
    """Create multiple propagations at once."""
    created = []
    
    try:
        for prop_data in propagations:
            # Validate
            valid, error = PropagationValidationService.validate_source_method(
                prop_data.source_type, prop_data.method
            )
            if not valid:
                raise HTTPException(status_code=400, detail=f"Invalid propagation: {error}")
            
            # Create
            db_prop = PlantPropagation(
                parent_plant_id=prop_data.parent_plant_id,
                child_plant_id=prop_data.child_plant_id,
                source_type=prop_data.source_type,
                method=prop_data.method,
                propagation_date=prop_data.propagation_date,
                date_harvested=prop_data.date_harvested,
                expected_ready=prop_data.expected_ready or PropagationEstimatorService.calculate_expected_ready_date(
                    prop_data.propagation_date,
                    prop_data.source_type,
                    prop_data.method
                ),
                status='pending',
                success_rate_estimate=prop_data.success_rate_estimate or PropagationEstimatorService.estimate_success_rate(
                    prop_data.source_type, prop_data.method
                ),
                notes=prop_data.notes,
            )
            
            db.add(db_prop)
            created.append(db_prop)
        
        db.commit()
        for prop in created:
            db.refresh(prop)
        
        return created
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# EXPORT
# ============================================================================

@router.get("/export/csv")
def export_propagations_csv(
    parent_plant_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Export propagations as CSV."""
    import csv
    import io
    from fastapi.responses import StreamingResponse
    
    query = db.query(PlantPropagation)
    if parent_plant_id:
        query = query.filter(PlantPropagation.parent_plant_id == parent_plant_id)
    
    propagations = query.all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            'id', 'parent_plant_id', 'child_plant_id', 'source_type', 'method',
            'propagation_date', 'date_harvested', 'expected_ready', 'success_date',
            'status', 'success_rate_estimate', 'notes'
        ]
    )
    
    writer.writeheader()
    for prop in propagations:
        writer.writerow({
            'id': prop.id,
            'parent_plant_id': prop.parent_plant_id,
            'child_plant_id': prop.child_plant_id,
            'source_type': prop.source_type,
            'method': prop.method,
            'propagation_date': prop.propagation_date,
            'date_harvested': prop.date_harvested,
            'expected_ready': prop.expected_ready,
            'success_date': prop.success_date,
            'status': prop.status,
            'success_rate_estimate': prop.success_rate_estimate,
            'notes': prop.notes,
        })
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=propagations.csv"}
    )

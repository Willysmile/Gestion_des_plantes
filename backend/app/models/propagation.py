from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime, 
    Text, JSON, ForeignKey, Index, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.models import Base


class PlantPropagation(Base):
    """Model for tracking plant propagation (cuttings, division, seeds, offsets)."""
    
    __tablename__ = 'plant_propagations'
    __table_args__ = (
        Index('idx_parent_plant', 'parent_plant_id'),
        Index('idx_child_plant', 'child_plant_id'),
        Index('idx_status', 'status'),
        Index('idx_source_method', 'source_type', 'method'),
        CheckConstraint('parent_plant_id != child_plant_id', name='no_self_parent'),
    )
    
    id = Column(Integer, primary_key=True)
    parent_plant_id = Column(Integer, ForeignKey('plants.id', ondelete='CASCADE'), nullable=False)
    child_plant_id = Column(Integer, ForeignKey('plants.id', ondelete='SET NULL'), nullable=True)
    
    # Propagation metadata
    source_type = Column(String(50), nullable=False)  # cutting, seeds, division, offset
    method = Column(String(50), nullable=False)  # water, soil, air-layer, substrate
    
    # Dates
    propagation_date = Column(Date, nullable=False)
    date_harvested = Column(Date, nullable=False)
    expected_ready = Column(Date, nullable=True)
    success_date = Column(Date, nullable=True)
    
    # Status tracking (9 states)
    status = Column(String(50), nullable=False, server_default='pending')
    # pending, rooting, rooted, growing, ready-to-pot, potted, transplanted, established, failed, abandoned
    
    # Measurements
    current_root_length_cm = Column(Float, nullable=True)
    current_leaves_count = Column(Integer, nullable=True)
    current_roots_count = Column(Integer, nullable=True)
    
    # Additional data
    notes = Column(Text, nullable=True)
    success_rate_estimate = Column(Float, nullable=False, server_default='0.85')
    is_active = Column(Boolean, nullable=False, server_default='true')
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent_plant = relationship('Plant', foreign_keys=[parent_plant_id], backref='propagations_as_parent')
    child_plant = relationship('Plant', foreign_keys=[child_plant_id], backref='propagations_as_child')
    events = relationship('PropagationEvent', back_populates='propagation', cascade='all, delete-orphan')
    
    @property
    def days_since_propagation(self) -> int:
        """Calculate days since propagation started."""
        return (datetime.utcnow().date() - self.propagation_date).days if self.propagation_date else 0
    
    @property
    def expected_duration_days(self) -> int:
        """Calculate expected duration based on source_type and method."""
        duration_map = {
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
        return duration_map.get((self.source_type, self.method), 21)
    
    @property
    def expected_ready_date(self) -> date:
        """Get or calculate expected ready date."""
        if self.expected_ready:
            return self.expected_ready
        from datetime import timedelta
        return self.propagation_date + timedelta(days=self.expected_duration_days)
    
    @property
    def is_overdue(self) -> bool:
        """Check if propagation is overdue for ready state."""
        if self.status in ['established', 'failed', 'abandoned']:
            return False
        return datetime.utcnow().date() > self.expected_ready_date
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'parent_plant_id': self.parent_plant_id,
            'child_plant_id': self.child_plant_id,
            'source_type': self.source_type,
            'method': self.method,
            'propagation_date': self.propagation_date.isoformat() if self.propagation_date else None,
            'date_harvested': self.date_harvested.isoformat() if self.date_harvested else None,
            'expected_ready': self.expected_ready.isoformat() if self.expected_ready else None,
            'success_date': self.success_date.isoformat() if self.success_date else None,
            'status': self.status,
            'current_root_length_cm': self.current_root_length_cm,
            'current_leaves_count': self.current_leaves_count,
            'current_roots_count': self.current_roots_count,
            'notes': self.notes,
            'success_rate_estimate': self.success_rate_estimate,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'days_since_propagation': self.days_since_propagation,
            'expected_duration_days': self.expected_duration_days,
            'is_overdue': self.is_overdue,
        }


class PropagationEvent(Base):
    """Model for tracking events in a propagation's lifecycle."""
    
    __tablename__ = 'propagation_events'
    __table_args__ = (
        Index('idx_propagation_events', 'propagation_id', 'event_date'),
    )
    
    id = Column(Integer, primary_key=True)
    propagation_id = Column(Integer, ForeignKey('plant_propagations.id', ondelete='CASCADE'), nullable=False)
    
    # Event tracking
    event_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    event_type = Column(String(50), nullable=False)  # rooted, leaves-grown, ready-to-pot, potted, transplanted, failed, etc.
    
    # Event details
    measurement = Column(JSON, nullable=True)  # {"root_length_cm": 5, "leaves_count": 8, ...}
    notes = Column(Text, nullable=True)
    photo_url = Column(String(255), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    propagation = relationship('PlantPropagation', back_populates='events')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'propagation_id': self.propagation_id,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'event_type': self.event_type,
            'measurement': self.measurement,
            'notes': self.notes,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

"""
Photo model for plant photos
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base


class Photo(Base):
    """
    Photo model for storing plant photos in WebP format
    
    Stores:
    - filename: WebP file stored in data/photos/{plant_id}/filename
    - file_size: Size of the WebP file (max 800KB)
    - width, height: Original image dimensions
    - is_primary: Whether this is the main photo
    """
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Filename stored in data/photos/{plant_id}/ directory
    # Format: photo_1.webp (large), photo_1_medium.webp, photo_1_thumbnail.webp
    filename = Column(String(255), nullable=False)
    
    # File size in bytes (max 800KB = 800000 bytes)
    file_size = Column(Integer, nullable=False)
    
    # Original image dimensions
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    
    # Whether this is the main/primary photo for the plant
    is_primary = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to Plant
    plant = relationship("Plant", back_populates="photos")

    def __repr__(self):
        return f"<Photo(id={self.id}, plant_id={self.plant_id}, filename={self.filename})>"

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

plant_tag_association = Table(
    'plant_tag',
    BaseModel.metadata,
    Column('plant_id', Integer, ForeignKey('plants.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class TagCategory(BaseModel):
    __tablename__ = "tag_categories"
    name = Column(String(100), unique=True, nullable=False)
    tags = relationship("Tag", back_populates="category")

class Tag(BaseModel):
    __tablename__ = "tags"
    name = Column(String(100), nullable=False)
    tag_category_id = Column(Integer, ForeignKey("tag_categories.id"))
    category = relationship("TagCategory", back_populates="tags")

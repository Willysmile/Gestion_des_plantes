"""
Routes pour CRUD des Tags et TagCategories
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.tags import Tag, TagCategory
from app.schemas.tag_schema import (
    TagResponse, TagCreate, TagUpdate, 
    TagCategoryResponse, TagCategoryCreate, TagCategoryWithTags
)
from typing import List

router = APIRouter(prefix="/api/tags", tags=["tags"])

# ============ TAG CATEGORIES ROUTES ============

@router.get("/categories", response_model=List[TagCategoryWithTags])
def get_tag_categories(db: Session = Depends(get_db)):
    """Récupère toutes les catégories avec leurs tags"""
    categories = db.query(TagCategory).all()
    return categories


@router.get("/categories/{category_id}", response_model=TagCategoryWithTags)
def get_tag_category(category_id: int, db: Session = Depends(get_db)):
    """Récupère une catégorie spécifique avec ses tags"""
    category = db.query(TagCategory).filter(TagCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    return category


@router.post("/categories", response_model=TagCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_tag_category(data: TagCategoryCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle catégorie de tags"""
    # Vérifier si la catégorie existe déjà
    existing = db.query(TagCategory).filter(TagCategory.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Catégorie déjà existante")
    
    category = TagCategory(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/categories/{category_id}", response_model=TagCategoryResponse)
def update_tag_category(category_id: int, data: TagCategoryCreate, db: Session = Depends(get_db)):
    """Met à jour une catégorie de tags"""
    category = db.query(TagCategory).filter(TagCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag_category(category_id: int, db: Session = Depends(get_db)):
    """Supprime une catégorie de tags (et ses tags)"""
    category = db.query(TagCategory).filter(TagCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    # Vérifier si des tags utilisent cette catégorie
    tags_count = db.query(Tag).filter(Tag.tag_category_id == category_id).count()
    if tags_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Impossible de supprimer : {tags_count} tag(s) utilisent cette catégorie"
        )
    
    db.delete(category)
    db.commit()


# ============ TAGS ROUTES ============

@router.get("", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    """Récupère tous les tags"""
    tags = db.query(Tag).all()
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Récupère un tag spécifique"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    return tag


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    """Crée un nouveau tag"""
    # Vérifier que la catégorie existe
    category = db.query(TagCategory).filter(TagCategory.id == data.tag_category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    # Vérifier que le tag n'existe pas déjà dans cette catégorie
    existing = db.query(Tag).filter(
        Tag.name == data.name,
        Tag.tag_category_id == data.tag_category_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ce tag existe déjà dans cette catégorie")
    
    tag = Tag(name=data.name, tag_category_id=data.tag_category_id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, data: TagUpdate, db: Session = Depends(get_db)):
    """Met à jour un tag"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    
    if data.name:
        tag.name = data.name
    if data.tag_category_id:
        # Vérifier que la catégorie existe
        category = db.query(TagCategory).filter(TagCategory.id == data.tag_category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")
        tag.tag_category_id = data.tag_category_id
    
    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Supprime un tag"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")
    
    db.delete(tag)
    db.commit()

# 🌱 Plant Propagation & Genealogy Feature - V2 (Enhanced)

**Branch:** 2.20  
**Priority:** BASSE-MOYENNE (implement after HIGH priority features)  
**Time Estimation:** 11-16 hours with improvements (9-11h MVP + 2-5h améliorations critiques)  
**Status:** ✅ Specification Complete + Improvements from propagation_improvements.md

---

## 🎯 Executive Summary

Complete rewrite of plant parent-child tracking based on **13 identified improvements**:
- ✅ **Eliminate data duplication** (single source of truth in plant_propagations table)
- ✅ **Prevent circular genealogy** (anti-cycle validation)
- ✅ **Atomic creation** (plant + propagation in single transaction)
- ✅ **Granular status tracking** (5-state lifecycle: pending → rooting → rooted → transplanted → established)
- ✅ **Optimized queries** (recursive CTEs instead of N+1 queries)
- ✅ **Rich notifications** (alerts for stalled propagations)

---

## 📊 Database Schema (Improved)

### Table: `plant_propagations`
**Single source of truth - NO duplicate columns in `plants` table**

```sql
CREATE TABLE plant_propagations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Core relationships (1:1 parent-child per record)
    parent_plant_id INTEGER NOT NULL,
    child_plant_id INTEGER NOT NULL,
    
    -- Propagation metadata
    propagation_type VARCHAR(50) NOT NULL, -- division, bouture, semis, marcottage, autre
    propagation_date DATE NOT NULL,
    propagation_method VARCHAR(100),      -- ex: "eau douce", "perlite", "sphaigne"
    quantity INTEGER DEFAULT 1,            -- metadata: how many divisions total
    
    -- Status tracking (5-state machine)
    status VARCHAR(20) DEFAULT 'pending',  -- pending, rooting, rooted, transplanted, established
    success_date DATE,                     -- when transitioned to 'established'
    
    -- Audit & history
    notes TEXT,                            -- user observations
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,                   -- soft delete
    archived_at DATETIME,                  -- historical preservation
    
    -- Constraints
    UNIQUE KEY uq_parent_child (parent_plant_id, child_plant_id),
    CONSTRAINT fk_parent FOREIGN KEY (parent_plant_id) REFERENCES plants(id),
    CONSTRAINT fk_child FOREIGN KEY (child_plant_id) REFERENCES plants(id),
    CONSTRAINT check_different CHECK (parent_plant_id != child_plant_id),
    CONSTRAINT check_valid_status CHECK (status IN ('pending', 'rooting', 'rooted', 'transplanted', 'established', 'failed', 'abandoned'))
);

-- Performance indexes
CREATE INDEX idx_parent_status ON plant_propagations(parent_plant_id, status);
CREATE INDEX idx_parent_date ON plant_propagations(parent_plant_id, propagation_date DESC);
CREATE INDEX idx_child_id ON plant_propagations(child_plant_id);
CREATE INDEX idx_type_status ON plant_propagations(propagation_type, status);
CREATE INDEX idx_deleted_at ON plant_propagations(deleted_at);
CREATE INDEX idx_archived_at ON plant_propagations(archived_at);
```

### Table: `plants` (NO CHANGES - No duplication)
**⚠️ CRITICAL: Do NOT add parent_plant_id, propagation_type, propagation_date columns!**

Use JOIN to plant_propagations when needed via views or API queries.

### Optional: View for easier querying
```sql
CREATE VIEW plants_with_propagation AS
SELECT 
    p.*,
    pp.parent_plant_id,
    pp.propagation_type,
    pp.propagation_date,
    pp.status as propagation_status
FROM plants p
LEFT JOIN plant_propagations pp ON p.id = pp.child_plant_id AND pp.deleted_at IS NULL;
```

---

## 🔐 Critical Improvements Implementation

### 1. Anti-Cycle Validation (CRITICAL)
**Problem:** Circular genealogies crash recursive queries.

```python
# app/services/propagation_service.py

def check_circular_dependency(
    db: Session, 
    parent_id: int, 
    child_id: int,
    max_depth: int = 100
) -> bool:
    """
    Verify no cycle created by this parent-child relationship.
    Returns True if safe, raises HTTPException if cycle detected.
    
    Algorithm: Traverse parent_id's ancestors looking for child_id
    """
    if parent_id == child_id:
        raise HTTPException(400, "Une plante ne peut pas être sa propre parent")
    
    visited = set()
    current = parent_id
    depth = 0
    
    # Walk up the lineage
    while current and depth < max_depth:
        if current == child_id:
            raise HTTPException(
                400, 
                f"Création impossible: cycle détecté dans la généalogie. "
                f"{child_id} est ancêtre de {parent_id}"
            )
        
        visited.add(current)
        
        # Find parent of current
        parent_rel = db.query(PlantPropagation).filter(
            PlantPropagation.child_plant_id == current,
            PlantPropagation.deleted_at.is_(None)
        ).first()
        
        current = parent_rel.parent_plant_id if parent_rel else None
        depth += 1
    
    return True


# Usage in routes:
@router.post("/{parent_id}/propagate")
async def create_propagation(
    parent_id: int,
    data: PropagationCreate,
    db: Session = Depends(get_db)
):
    # Validate no cycle
    check_circular_dependency(db, parent_id, data.child_plant_id)
    
    # Create with confidence
    propagation = PlantPropagation(...)
    db.add(propagation)
    db.commit()
    return propagation
```

### 2. Atomic Plant + Propagation Creation
**Problem:** 2-step creation risks orphaned plants.

```python
class PropagationCreateComplete(BaseModel):
    """Create plant AND propagation in single transaction"""
    child_plant_name: str
    child_plant_species: Optional[str] = None
    propagation_type: str
    propagation_date: date
    propagation_method: Optional[str] = None
    notes: Optional[str] = None
    copy_parent_care_schedule: bool = True


@router.post("/{parent_id}/propagate-complete")
async def create_propagation_with_plant(
    parent_id: int,
    data: PropagationCreateComplete,
    db: Session = Depends(get_db)
):
    """Create child plant + propagation atomically"""
    
    parent = db.query(Plant).filter(Plant.id == parent_id).first()
    if not parent:
        raise HTTPException(404, "Plante mère introuvable")
    
    # Validate no cycle (even though child doesn't exist yet)
    try:
        with db.begin_nested():  # Savepoint
            # 1. Create child plant
            child_plant = Plant(
                name=data.child_plant_name,
                species=data.child_plant_species or parent.species,
                location=parent.location
            )
            db.add(child_plant)
            db.flush()  # Get ID without committing
            
            # 2. Validate cycle before committing
            check_circular_dependency(db, parent_id, child_plant.id)
            
            # 3. Create propagation
            propagation = PlantPropagation(
                parent_plant_id=parent_id,
                child_plant_id=child_plant.id,
                propagation_type=data.propagation_type,
                propagation_date=data.propagation_date,
                propagation_method=data.propagation_method,
                notes=data.notes,
                status="pending"
            )
            db.add(propagation)
            
            # 4. Copy care schedule if requested
            if data.copy_parent_care_schedule:
                copy_watering_schedule(db, parent_id, child_plant.id)
            
            db.commit()
            
        return {
            "plant": child_plant,
            "propagation": propagation,
            "message": "Propagation créée avec succès"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erreur: {str(e)}")
```

### 3. Granular Status Tracking
**Problem:** Simple pending/success/failed doesn't track progression.**

```python
class PropagationStatus(str, Enum):
    PENDING = "pending"              # Just created
    ROOTING = "rooting"              # Callus forming, root primordia
    ROOTED = "rooted"                # Roots visible/established
    TRANSPLANTED = "transplanted"    # Moved to soil/final medium
    ESTABLISHED = "established"      # Growing well, stable (SUCCESS)
    FAILED = "failed"                # Died/rotted (FAILURE)
    ABANDONED = "abandoned"          # Gave up on propagation

# Valid state transitions
STATUS_TRANSITIONS = {
    'pending': ['rooting', 'failed', 'abandoned'],
    'rooting': ['rooted', 'failed', 'abandoned'],
    'rooted': ['transplanted', 'failed', 'abandoned'],
    'transplanted': ['established', 'failed'],
    'established': [],    # Terminal
    'failed': [],         # Terminal
    'abandoned': [],      # Terminal
}

@router.put("/{parent_id}/propagations/{child_id}/status")
async def update_propagation_status(
    parent_id: int,
    child_id: int,
    new_status: PropagationStatus,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update status with transition validation"""
    
    prop = get_propagation(db, parent_id, child_id)
    
    # Validate transition
    if new_status not in STATUS_TRANSITIONS.get(prop.status, []):
        raise HTTPException(
            400,
            f"Transition invalide: {prop.status} → {new_status}. "
            f"Options: {STATUS_TRANSITIONS[prop.status]}"
        )
    
    # Update
    prop.status = new_status
    if notes:
        prop.notes = f"{prop.notes}\n[{date.today().isoformat()}] {notes}"
    
    if new_status == PropagationStatus.ESTABLISHED:
        prop.success_date = date.today()
    
    db.commit()
    return prop
```

### 4. Optimized Genealogy Query (CTE Recursive)
**Problem:** N+1 queries for genealogy tree.

```python
def get_genealogy_optimized(
    db: Session, 
    plant_id: int, 
    max_depth: int = 5
) -> dict:
    """
    Get full genealogy in ONE query using recursive CTE.
    Performance: 1 query instead of N+1 → 12x faster
    """
    
    query = text("""
        WITH RECURSIVE genealogy AS (
            -- Base case: start plant
            SELECT 
                p.id,
                p.name,
                p.species,
                CAST(NULL AS INTEGER) as parent_id,
                CAST(NULL AS VARCHAR) as propagation_type,
                0 AS level,
                CAST(p.id AS TEXT) AS path
            FROM plants p
            WHERE p.id = :plant_id
            
            UNION ALL
            
            -- Recursive case: traverse children
            SELECT 
                p.id,
                p.name,
                p.species,
                pp.parent_plant_id,
                pp.propagation_type,
                g.level + 1,
                g.path || '/' || CAST(p.id AS TEXT)
            FROM plants p
            JOIN plant_propagations pp ON p.id = pp.child_plant_id
            JOIN genealogy g ON pp.parent_plant_id = g.id
            WHERE g.level < :max_depth
            AND pp.deleted_at IS NULL
        )
        SELECT * FROM genealogy
        ORDER BY level, id;
    """)
    
    result = db.execute(query, {
        "plant_id": plant_id,
        "max_depth": max_depth
    }).fetchall()
    
    return build_tree_from_flat(result)
```

### 5. Propagation Alerts & Notifications
**Problem:** Users don't know when propagations need attention.**

```python
def check_propagation_alerts(db: Session) -> List[dict]:
    """Generate contextual alerts"""
    
    today = date.today()
    alerts = []
    
    # 1. Rooting stuck > 45 days
    stuck = db.query(PlantPropagation).filter(
        PlantPropagation.status == 'rooting',
        PlantPropagation.propagation_date < today - timedelta(days=45)
    ).all()
    
    for prop in stuck:
        alerts.append({
            "type": "warning",
            "severity": "medium",
            "message": f"{prop.child_plant.name}: En enracinement depuis "
                      f"{(today - prop.propagation_date).days} jours",
            "action": "Vérifier les racines, considérer l'échec?",
            "propagation_id": prop.id
        })
    
    # 2. Ready to transplant
    ready = db.query(PlantPropagation).filter(
        PlantPropagation.status == 'rooted',
        PlantPropagation.success_date < today - timedelta(days=7)
    ).all()
    
    for prop in ready:
        alerts.append({
            "type": "info",
            "severity": "low",
            "message": f"{prop.child_plant.name}: Racines bien développées",
            "action": "Mettre en terre maintenant",
            "propagation_id": prop.id
        })
    
    # 3. Recently transplanted - monitor
    recent = db.query(PlantPropagation).filter(
        PlantPropagation.status == 'transplanted',
        PlantPropagation.updated_at > today - timedelta(days=14)
    ).all()
    
    for prop in recent:
        alerts.append({
            "type": "reminder",
            "severity": "low",
            "message": f"{prop.child_plant.name}: Transplantée il y a "
                      f"{(today - prop.updated_at.date()).days}j",
            "action": "Surveiller reprise (arrosage régulier)",
            "propagation_id": prop.id
        })
    
    return sorted(alerts, key=lambda x: {'warning': 0, 'info': 1, 'reminder': 2}.get(x['type'], 3))


@router.get("/propagations/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    """Get all active alerts"""
    return check_propagation_alerts(db)
```

---

## 🔌 API Endpoints (Complete)

### Propagation Management

```
POST   /api/plants/{parent_id}/propagate-complete
       └─ Create child plant + propagation atomically
       ├─ Request: { child_plant_name, propagation_type, propagation_date, copy_parent_care_schedule? }
       └─ Response: { plant, propagation, message }

POST   /api/plants/{parent_id}/propagate
       └─ Create propagation for existing child plant
       ├─ Request: { child_plant_id, propagation_type, propagation_date, ... }
       └─ Response: { propagation }

PUT    /api/plants/{parent_id}/propagations/{child_id}/status
       └─ Update propagation status with validation
       ├─ Request: { new_status, notes? }
       ├─ Validation: Checks transition is allowed
       └─ Response: { propagation }

GET    /api/plants/{id}/children
       └─ Get all children of a plant (direct only)
       └─ Response: [ { id, name, propagation_type, status } ]

GET    /api/plants/{id}/genealogy
       └─ Get full genealogy tree (with ancestry)
       ├─ Query params: ?max_depth=5
       └─ Response: { id, name, children: [...], ancestors: [...] }

GET    /api/plants/{id}/genealogy/export
       └─ Export genealogy as JSON/CSV/SVG
       ├─ Query params: ?format=json|csv|svg
       └─ Response: File or JSON

GET    /api/propagations/alerts
       └─ Get all active alerts (stalled, ready, etc.)
       └─ Response: [ { type, severity, message, action } ]

GET    /api/propagations/stats
       └─ Global propagation statistics
       └─ Response: { total, success_rate, avg_rooting_days, by_type: {...} }

DELETE /api/plants/{parent_id}/propagations/{child_id}
       └─ Soft delete propagation
       └─ Response: { success: true }
```

---

## 📊 Statistics Available

```python
{
    "total_propagations": 42,
    "success_rate": 0.88,
    
    "by_type": {
        "division": { "total": 15, "success": 14, "rate": 0.93 },
        "bouture": { "total": 20, "success": 16, "rate": 0.80 },
        "semis": { "total": 5, "success": 2, "rate": 0.40 },
        "marcottage": { "total": 2, "success": 2, "rate": 1.0 }
    },
    
    "status_distribution": {
        "pending": 3,
        "rooting": 2,
        "rooted": 1,
        "transplanted": 0,
        "established": 35,
        "failed": 1
    },
    
    "avg_rooting_days": 21,
    "avg_to_established_days": 45,
    "most_propagated_species": "Monstera deliciosa",
    "best_propagation_method": "division"
}
```

---

## 🎨 Frontend UI Components

### 1. Genealogy Tree View
- **Library:** React Flow or D3.js
- **Features:** Zoom, pan, click nodes for details
- **Shows:** Parent → Children relationships with propagation types

### 2. Propagation Timeline
- **Timeline component** showing chronological progression
- **Status indicators** with dates
- **Notes & photos** integrated
- **Transitions** validated on UI

### 3. Propagation Alerts Banner
- **Alert system** showing stalled/ready propagations
- **Action buttons** to update status
- **Severity levels:** warning (red), info (blue), reminder (gray)

### 4. Propagation Form
- **Multi-step form** for atomic creation
- **Validation** before submission
- **Copy schedule option** for cloned plants

---

## ✅ Testing Strategy

### Unit Tests
```python
def test_circular_dependency_detection():
    """Prevent cycles"""
    create_prop(A → B); create_prop(B → C)
    with pytest.raises(HTTPException):
        create_prop(C → A)

def test_atomic_creation_rollback():
    """Verify transaction safety"""
    with raises(exception):
        create_propagation_with_plant(invalid_data)
    assert no_orphaned_plants()

def test_status_transitions():
    """Validate state machine"""
    prop = create(status='pending')
    update(status='rooting')  # ✅ OK
    with raises:
        update(status='transplanted')  # ❌ Skip rooted
```

### Integration Tests
```python
def test_genealogy_performance(1_parent_5_children_25_grandchildren):
    """Verify CTE query < 500ms"""
    start = time.time()
    genealogy = get_genealogy(parent_id)
    assert time.time() - start < 0.5
```

### E2E Tests
```javascript
it('should prevent circular genealogy in UI', () => {
    createProp(A → B);
    visitPropagationForm(B);
    selectParent(A);
    clickCreate();
    expectError("cycle détecté");
});
```

---

## 📈 Implementation Roadmap

### Phase 1: Foundation (5-6 hours)
- [ ] Create plant_propagations table with indexes
- [ ] Implement cycle validation
- [ ] Add atomic creation endpoint
- [ ] Write unit tests

### Phase 2: Logic & Safety (3-4 hours)
- [ ] Granular status tracking
- [ ] Optimized genealogy query (CTE)
- [ ] Soft delete & archiving
- [ ] Integration tests

### Phase 3: UX & Insights (2-3 hours)
- [ ] Alerts system
- [ ] Statistics endpoint
- [ ] Frontend tree/timeline components
- [ ] E2E tests

### Phase 4: Polish (1-2 hours)
- [ ] Export genealogy
- [ ] Advanced filters
- [ ] Documentation
- [ ] Edge cases

**Total: 11-16 hours**

---

## 🚀 Future Enhancements

1. **Hybridization tracking** (multiple parents)
2. **Tissue culture propagation** tracking
3. **Success prediction** (ML based on species/method)
4. **Propagation calendar** integration
5. **Batch operations** (propagate multiple children at once)
6. **Photo timeline** of propagation progress
7. **Community propagation methods** database

---

## 📚 Reference Materials

- Source document: `/docs/propagation_improvements.md` (13 detailed improvements)
- Original spec: `/PLANT_PROPAGATION_FEATURE.md` (MVP design)
- Database audit: `/docs/DATABASE_AUDIT.md`

---

**Status:** ✅ Ready for implementation  
**Last Updated:** 9 Nov 2025  
**Version:** 2.0 (Enhanced with critical improvements)

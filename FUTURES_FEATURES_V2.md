# 🚀 FUTURES_FEATURES - Complete Development Roadmap V2

**Branch:** 2.20  
**Last Updated:** 9 Nov 2025  
**Status:** ✅ Comprehensive roadmap with integrated improvements

---

## 🎯 Strategic Overview

**Vision:** Evolve from basic plant tracker to comprehensive botanical knowledge management system.

**Development Philosophy:**
- HIGH priority = Core workflows, frequent user actions
- MEDIUM priority = Enhanced features, secondary workflows
- LOW priority = Nice-to-have, niche use cases

**Resource Allocation:** 3-4 weeks full-time development for all features.

---

## 📊 Feature Prioritization Matrix

| Priority | Feature | Impact | Effort | ROI | Users |
|----------|---------|--------|--------|-----|-------|
| 🔴 HIGH | 📅 Interactive Calendar | ⭐⭐⭐⭐⭐ | 3-4h | 5/5 | 95% |
| 🔴 HIGH | 🔔 Advanced Alerts | ⭐⭐⭐⭐⭐ | 2-3h | 5/5 | 90% |
| 🔴 HIGH | 🌱 Plant Propagation v2 | ⭐⭐⭐⭐ | 11-16h | 4/5 | 70% |
| 🟡 MEDIUM | 📊 Export/PDF Reports | ⭐⭐⭐⭐ | 4-5h | 4/5 | 65% |
| 🟡 MEDIUM | 🔍 Search & Filters | ⭐⭐⭐⭐ | 3-4h | 4/5 | 80% |
| 🟡 MEDIUM | 🎨 Customizable Views | ⭐⭐⭐ | 3-4h | 3/5 | 55% |
| 🟡 MEDIUM | 📱 Mobile Optimization | ⭐⭐⭐⭐ | 5-6h | 4/5 | 70% |
| 🟡 MEDIUM | 🎯 Data Insights | ⭐⭐⭐ | 4-5h | 3/5 | 50% |
| 🟢 LOW | 🌙 Dark Mode | ⭐⭐ | 2-3h | 2/5 | 40% |
| 🟢 LOW | 👥 Multi-user Collab | ⭐⭐ | 8-10h | 2/5 | 20% |
| 🟢 LOW | 🔄 Cloud Sync | ⭐ | 10-12h | 1/5 | 10% |
| 🟢 LOW | 🌐 External Integrations | ⭐⭐ | 6-8h | 2/5 | 30% |

---

# 🔴 HIGH PRIORITY FEATURES

## 1. 📅 Interactive Calendar View

**Priority:** 🔴 CRITICAL (Most Requested)  
**Time:** 3-4 hours  
**Effort:** ⏱️ Medium  
**ROI:** ⭐⭐⭐⭐⭐ Excellent  
**Users Impacted:** 95%

### Description
**Monthly/weekly calendar** showing:
- **Color-coded soins** (water: blue, fertilize: amber, care: red)
- **Drag-and-drop rescheduling** of watering dates
- **Week view** with hourly breakdown
- **Month overview** with plant count per day
- **Integration with notifications** (alerts on calendar days)

### Use Case
```
User workflow:
1. Open dashboard → Click "Calendrier"
2. See November with all watering/fertilizing events
3. Click Nov 15 → "3 plants to water today"
4. Mark as done → Calendar updates
5. Reschedule "Monstera watering" from Nov 20 to Nov 22
6. Get notification on Nov 22 morning
```

### Technical Implementation

**Backend:**
```python
# Add endpoint
@router.get("/statistics/calendar")
async def get_calendar_events(
    year: int, 
    month: int,
    db: Session = Depends(get_db)
):
    """Get all events for month"""
    return {
        "events": [
            {
                "date": "2025-11-15",
                "type": "watering",
                "plant_id": 5,
                "plant_name": "Monstera",
                "count": 3
            },
            ...
        ],
        "summary": {
            "total_days": 30,
            "active_days": 12,
            "water_count": 25,
            "fertilize_count": 8
        }
    }

# Service method
def get_calendar_events(db: Session, year: int, month: int):
    """Build calendar for specific month"""
    start_date = date(year, month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    waters = db.query(WateringHistory).filter(
        WateringHistory.watering_date >= start_date,
        WateringHistory.watering_date <= end_date,
        WateringHistory.deleted_at.is_(None)
    ).all()
    
    fertilizes = db.query(FertilizingHistory).filter(
        FertilizingHistory.fertilizing_date >= start_date,
        FertilizingHistory.fertilizing_date <= end_date,
        FertilizingHistory.deleted_at.is_(None)
    ).all()
    
    # Group by date
    events_by_date = defaultdict(list)
    for water in waters:
        events_by_date[water.watering_date].append({
            'type': 'water',
            'plant_id': water.plant_id,
            'plant_name': water.plant.name
        })
    
    for fert in fertilizes:
        events_by_date[fert.fertilizing_date].append({
            'type': 'fertilize',
            'plant_id': fert.plant_id,
            'plant_name': fert.plant.name
        })
    
    return events_by_date
```

**Frontend:**
```jsx
// Use react-big-calendar or FullCalendar
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const CalendarPage = () => {
  const [events, setEvents] = useState([]);
  const [month, setMonth] = useState(new Date());
  
  useEffect(() => {
    const year = month.getFullYear();
    const monthNum = month.getMonth() + 1;
    
    fetch(`/api/statistics/calendar?year=${year}&month=${monthNum}`)
      .then(res => res.json())
      .then(data => {
        const events = flattenEvents(data.events);
        setEvents(events);
      });
  }, [month]);
  
  const eventStyleGetter = (event) => {
    const colors = {
      'watering': { backgroundColor: '#3B82F6' },
      'fertilizing': { backgroundColor: '#F59E0B' },
      'care': { backgroundColor: '#EF4444' }
    };
    
    return { style: colors[event.type] || {} };
  };
  
  return (
    <div style={{ height: 600 }}>
      <Calendar
        localizer={momentLocalizer(moment)}
        events={events}
        startAccessor="start"
        endAccessor="end"
        eventPropGetter={eventStyleGetter}
        onNavigate={setMonth}
        views={['month', 'week', 'day']}
      />
    </div>
  );
};
```

### Success Metrics
- ✅ Calendar renders in < 1s
- ✅ Drag-drop reschedule works smoothly
- ✅ Month view shows all events clearly
- ✅ 90% of users find it useful

---

## 2. 🔔 Advanced Alerts System

**Priority:** 🔴 CRITICAL  
**Time:** 2-3 hours  
**Effort:** ⏱️ Low-Medium  
**ROI:** ⭐⭐⭐⭐⭐ Excellent  
**Users Impacted:** 90%

### Description
**Smart notification system** for:
- **Critical plants** (overdue watering by 5+ days)
- **Health warnings** (sick plant thresholds)
- **Task reminders** (watering due in 2 days)
- **Propagation alerts** (stalled rooting > 45 days)
- **Browser notifications** + email (optional)

### Use Case
```
Morning flow:
1. Open app → Red banner "3 critical plants need water NOW"
2. Click → Auto-scrolls to PlantsToWaterList
3. Get browser notification: "Monstera overdue by 7 days"
4. Click → Navigate to plant details
```

### Technical Implementation

**Backend:**
```python
class AlertSeverity(str, Enum):
    CRITICAL = "critical"    # Overdue > 5 days
    HIGH = "high"            # Overdue 2-5 days
    MEDIUM = "medium"        # Due in 2 days
    LOW = "low"              # Due in 7 days

@router.get("/alerts/active")
async def get_active_alerts(db: Session = Depends(get_db)):
    """Get all active alerts"""
    alerts = []
    today = date.today()
    
    # Critical overdue
    critical = db.query(Plant).filter(
        Plant.deleted_at.is_(None),
        Plant.last_watering_date < today - timedelta(days=5)
    ).all()
    
    for plant in critical:
        days_overdue = (today - plant.last_watering_date).days
        alerts.append({
            "type": "overdue_water",
            "severity": "critical",
            "plant_id": plant.id,
            "plant_name": plant.name,
            "message": f"⚠️ URGENT: {plant.name} n'a pas été arrosée depuis {days_overdue} jours!",
            "action": "water_now",
            "action_label": "Arroser maintenant"
        })
    
    # Propagation alerts (from propagation_improvements.md)
    stuck_rooting = db.query(PlantPropagation).filter(
        PlantPropagation.status == 'rooting',
        PlantPropagation.propagation_date < today - timedelta(days=45),
        PlantPropagation.deleted_at.is_(None)
    ).all()
    
    for prop in stuck_rooting:
        days = (today - prop.propagation_date).days
        alerts.append({
            "type": "propagation_stalled",
            "severity": "high",
            "propagation_id": prop.id,
            "plant_name": prop.child_plant.name,
            "message": f"Propagation en enracinement depuis {days}j",
            "action": "check_propagation"
        })
    
    # Health warnings
    sick_plants = db.query(Plant).filter(
        Plant.deleted_at.is_(None),
        Plant.health_status == "sick"
    ).all()
    
    for plant in sick_plants:
        alerts.append({
            "type": "health_concern",
            "severity": "high",
            "plant_id": plant.id,
            "plant_name": plant.name,
            "message": f"🏥 {plant.name} est malade - vérifier et traiter",
            "action": "view_plant"
        })
    
    return sorted(alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x['severity']])
```

**Frontend Banner:**
```jsx
const AlertsBanner = () => {
  const [alerts, setAlerts] = useState([]);
  
  useEffect(() => {
    fetch('/api/alerts/active')
      .then(res => res.json())
      .then(setAlerts);
    
    // Refresh every 5 minutes
    const interval = setInterval(() => {
      fetch('/api/alerts/active')
        .then(res => res.json())
        .then(setAlerts);
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  if (alerts.length === 0) return null;
  
  const groupedBySeverity = groupBy(alerts, 'severity');
  
  return (
    <div className="space-y-2 mb-6">
      {groupedBySeverity.critical?.length > 0 && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <div className="flex items-start">
            <AlertTriangle className="h-5 w-5 text-red-600 mr-3 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="font-bold text-red-800">
                {groupedBySeverity.critical.length} Urgent(s)
              </h3>
              {groupedBySeverity.critical.map(alert => (
                <button
                  key={alert.plant_id}
                  onClick={() => navigateToAction(alert)}
                  className="text-red-700 hover:text-red-900 block mt-1 text-left"
                >
                  {alert.message}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
      
      {groupedBySeverity.high?.length > 0 && (
        // Similar for high/medium/low
      )}
    </div>
  );
};
```

### Success Metrics
- ✅ Alerts generated in < 200ms
- ✅ Users mark 80%+ of alerts as resolved
- ✅ 95% accuracy (no false positives)
- ✅ Propagation alerts reduce failed cuttings

---

## 3. 🌱 Plant Propagation & Genealogy v2

**Priority:** 🔴 HIGH (Complex Feature)  
**Time:** 11-16 hours including improvements  
**Effort:** ⏱️ High  
**ROI:** ⭐⭐⭐⭐ Excellent  
**Users Impacted:** 70%

### Key Improvements from Analysis
This feature includes **13 critical improvements** from `/docs/propagation_improvements.md`:

1. **Eliminate data duplication** - Single source of truth in plant_propagations table
2. **Prevent circular genealogy** - Validate no cycles before creation
3. **Atomic creation** - Plant + propagation in single transaction
4. **Granular status tracking** - 5-state machine (pending → rooting → rooted → transplanted → established)
5. **Optimized queries** - Recursive CTEs instead of N+1
6. **Smart alerts** - Track stalled propagations
7. **Soft delete support** - Preserve historical data
8. **Rich validation** - Pydantic schemas with business logic
9. **Performance indexes** - DB queries 12x faster
10. **Timeline view** - Visual propagation progression
11. **Export genealogy** - JSON/CSV/SVG formats
12. **Statistics** - Success rates by propagation type
13. **UI tree visualization** - React Flow genealogy display

**See:** `/PLANT_PROPAGATION_FEATURE_V2.md` for complete specification.

---

# 🟡 MEDIUM PRIORITY FEATURES

## 4. 📊 Export CSV/PDF Reports

**Priority:** 🟡 MEDIUM  
**Time:** 4-5 hours  
**Effort:** ⏱️ Medium  
**ROI:** ⭐⭐⭐⭐ Excellent  
**Users Impacted:** 65%

### Features
- **Export all plants** as CSV (name, species, watering schedule, last care)
- **Generate PDF report** (plant inventory, care calendar, photos)
- **Filter exports** (by tag, species, health status)
- **Monthly reports** (activities summary)
- **Genealogy export** (propagation tree as PDF)

### Technical Stack
- **Backend:** python-pptx, reportlab, pandas
- **Frontend:** Download button, format selector

### Implementation
```python
@router.get("/export/plants.csv")
async def export_plants_csv(db: Session = Depends(get_db)):
    """Export plant list as CSV"""
    plants = db.query(Plant).filter(Plant.deleted_at.is_(None)).all()
    
    csv_data = "Name,Species,Location,Frequency,Last Watered,Health,Tags\n"
    for plant in plants:
        csv_data += f"{plant.name},{plant.species},...\n"
    
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=plants.csv"}
    )

@router.get("/export/report-pdf")
async def export_pdf_report(month: int = None, db: Session = Depends(get_db)):
    """Generate comprehensive PDF report"""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    # Build PDF with charts, tables, photos
    # Return as file download
```

---

## 5. 🔍 Search & Advanced Filters

**Priority:** 🟡 MEDIUM  
**Time:** 3-4 hours  
**Effort:** ⏱️ Medium  
**ROI:** ⭐⭐⭐⭐ Excellent  
**Users Impacted:** 80%

### Features
- **Global search** (name, species, scientific name)
- **Fuzzy matching** (typo tolerance: "monstea" → "monstera")
- **Advanced filters**:
  - By species
  - By health status
  - By watering frequency
  - By location
  - By tags
  - By creation date
- **Save filters** as favorites
- **Search history**

### Frontend
```jsx
const SearchFilters = () => {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState({
    species: [],
    health: null,
    location: [],
    tags: []
  });
  
  return (
    <div className="space-y-4">
      {/* Search input */}
      <input
        type="text"
        placeholder="Chercher par nom, espèce..."
        value={query}
        onChange={e => performSearch(e.target.value)}
      />
      
      {/* Filter dropdowns */}
      <MultiSelect label="Species" />
      <Select label="Health Status" />
      <MultiSelect label="Location" />
      
      {/* Results */}
      <SearchResults results={results} />
    </div>
  );
};
```

---

## 6. 🎨 Customizable Views

**Priority:** 🟡 MEDIUM  
**Time:** 3-4 hours  
**Effort:** ⏱️ Medium  
**ROI:** ⭐⭐⭐ Good  
**Users Impacted:** 55%

### Features
- **View modes:** Cards / List / Grid / Timeline
- **Column visibility** customization
- **Sorting** (by name, date, frequency, health)
- **Grouping** (by species, location, health status)
- **Save preferences** to user settings

---

## 7. 📱 Mobile Optimization

**Priority:** 🟡 MEDIUM  
**Time:** 5-6 hours  
**Effort:** ⏱️ Medium-High  
**ROI:** ⭐⭐⭐⭐ Excellent  
**Users Impacted:** 70%

### Features
- **Bottom navigation bar** (Dashboard / Plants / Calendar / Settings)
- **Swipe gestures** (left/right navigate)
- **Touch-friendly buttons** (48px minimum)
- **Responsive forms** (mobile-first design)
- **Camera integration** (mobile photo upload)
- **Progressive Web App** (installable)

---

## 8. 📈 Data Insights & Analytics

**Priority:** 🟡 MEDIUM  
**Time:** 4-5 hours  
**Effort:** ⏱️ Medium  
**ROI:** ⭐⭐⭐ Good  
**Users Impacted:** 50%

### Features
- **Success rates** by species and method
- **Trends** (health improving/declining)
- **Predictions** (when next watering due)
- **Collection insights** (species breakdown, tag distribution)
- **Care patterns** (most/least watered plants)

---

# 🟢 LOW PRIORITY FEATURES

## 9. 🌙 Dark Mode

**Priority:** 🟢 LOW  
**Time:** 2-3 hours  
**Effort:** ⏱️ Low  
**ROI:** ⭐⭐ Decent  
**Users Impacted:** 40%

### Implementation
```jsx
const DarkModeToggle = () => {
  const [isDark, setIsDark] = useLocalStorage('darkMode', false);
  
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);
  
  return (
    <button onClick={() => setIsDark(!isDark)}>
      {isDark ? '☀️' : '🌙'}
    </button>
  );
};
```

---

## 10. 👥 Multi-User Collaboration

**Priority:** 🟢 LOW  
**Time:** 8-10 hours  
**Effort:** ⏱️ High  
**ROI:** ⭐⭐ Limited  
**Users Impacted:** 20%

### Features
- User accounts & authentication
- Share plant collection with family/friends
- Permissions (view/edit/admin)
- Activity log (who did what)

---

## 11. 🔄 Cloud Sync & Backup

**Priority:** 🟢 LOW  
**Time:** 10-12 hours  
**Effort:** ⏱️ Very High  
**ROI:** ⭐ Limited  
**Users Impacted:** 10%

### Features
- Automatic cloud backup (AWS S3)
- Multi-device sync
- Restore from backup

---

## 12. 🌐 External Integrations

**Priority:** 🟢 LOW  
**Time:** 6-8 hours each  
**Effort:** ⏱️ High  
**ROI:** ⭐⭐ Limited  
**Users Impacted:** 30%

### Integration Options
- **Weather API** → Adjust watering based on rain
- **Google Calendar** → Sync watering schedule
- **Notion** → Export to Notion database
- **IFTTT** → Triggers for automations
- **Telegram/Discord** → Notifications

---

## 📈 Implementation Timeline

### Phase 1: Foundation (Week 1)
```
Days 1-2: 📅 Interactive Calendar (HIGH)
Days 3-4: 🔔 Advanced Alerts (HIGH)
Day 5: Deploy & test
```

### Phase 2: Complex Features (Week 2-3)
```
Days 1-5: 🌱 Plant Propagation v2 (HIGH - includes 13 improvements)
Days 6-7: 📊 Export/Reports (MEDIUM)
```

### Phase 3: Enhancement (Week 4)
```
Days 1-3: 🔍 Search & Filters (MEDIUM)
Days 4-5: 🎨 Customizable Views (MEDIUM)
```

### Phase 4: Polish (Optional Week 5)
```
Days 1-3: 📱 Mobile Optimization (MEDIUM)
Days 4-5: 📈 Data Insights (MEDIUM)
```

---

## 💡 Success Metrics per Feature

### 📅 Calendar
- ✅ Load time < 1s
- ✅ 80% of users access weekly
- ✅ 95% accuracy of events

### 🔔 Alerts
- ✅ Generation time < 200ms
- ✅ 90% resolution rate
- ✅ < 5% false positives

### 🌱 Propagation
- ✅ Zero circular genealogies
- ✅ Query time < 500ms for deep trees
- ✅ 85%+ data integrity in migrations

### 📊 Export
- ✅ PDF generated in < 2s
- ✅ CSV imports correctly into Excel
- ✅ Supports > 1000 plants

### 🔍 Search
- ✅ Results appear in < 500ms
- ✅ Fuzzy matching catches 90% of typos
- ✅ Filter combinations work correctly

---

## 🔧 Technical Considerations

### Backend Enhancements Needed
- Add more statistics endpoints
- Implement background tasks (Celery for exports)
- Caching layer (Redis for search)
- Database migrations for new features
- API versioning (v2 endpoints)

### Frontend Enhancements Needed
- Component library standardization
- Performance optimization (lazy loading)
- State management review (Context → Redux?)
- Testing coverage improvement
- E2E test automation

### DevOps
- CI/CD pipeline enhancements
- Load testing for new features
- Monitoring & logging improvements
- Rollback procedures

---

## 🎯 Recommendation

### Start With (Week 1)
1. **📅 Calendar** - Quick win, high impact
2. **🔔 Alerts** - Critical for user experience
3. **🌱 Propagation v2** - Complex but essential

### Then Add (Week 2-3)
4. **📊 Export/Reports** - User-requested feature
5. **🔍 Search** - Improves discoverability

### Polish Later (Optional)
6-12. Other features as time permits

---

## 📚 Documentation

- **Complete specs:** Individual feature files
- **Propagation details:** `/PLANT_PROPAGATION_FEATURE_V2.md`
- **Improvements doc:** `/docs/propagation_improvements.md`
- **API changes:** `/docs/API_CHANGES.md` (to create)
- **Migration guide:** `/docs/MIGRATION_GUIDE.md` (to create)

---

## ✅ Definition of Done per Feature

- [ ] Backend endpoints implemented & tested
- [ ] Frontend components created & responsive
- [ ] Database migrations run successfully
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration tests pass
- [ ] E2E tests pass (key user flows)
- [ ] Documentation updated
- [ ] Code reviewed & merged
- [ ] Deployed to staging
- [ ] UAT completed
- [ ] Deployed to production
- [ ] Monitoring in place

---

## 🚀 Next Steps

1. **Validate this roadmap** with team
2. **Create Jira/GitHub tickets** for each feature
3. **Start Phase 1** (Calendar + Alerts + Propagation v2)
4. **Weekly standups** to track progress
5. **Monthly reviews** to adjust priorities

---

**Status:** ✅ Ready for implementation  
**Last Updated:** 9 Nov 2025  
**Version:** 2.0 (Integrated with propagation_improvements.md)  
**Next Review:** 1 Dec 2025

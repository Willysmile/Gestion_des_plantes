# Phase 3 - Plan de Développement

## 🎯 Objectifs Phase 3

Transformer le MVP en application polished avec validation, photos, historiques et tests E2E.

**Timeline estimée:** 3-4 jours (20-25h)
**Priorité:** Validation > Photos > Timeline > Tests

---

## 📋 Phase 3.1 - Form Validation (5h)

### Objectifs
- Client-side validation avec Zod
- Messages d'erreur en français
- Required fields highlighting
- Real-time validation feedback
- Better UX on submit errors

### Dépendances à ajouter
```bash
npm install zod
```

### Fichiers à modifier
1. **frontend/src/lib/schemas.js** (CREATE)
   - Zod schemas pour Plant
   - Champs obligatoires: name, family, genus
   - Types: string, number, boolean, enum
   - Custom messages en français

2. **frontend/src/pages/PlantFormPage.jsx** (MODIFY)
   - Valider avec schema.parse()
   - Afficher erreurs par champ
   - Highlight champs invalides (red border)
   - Disable submit si invalid

3. **frontend/src/lib/api.js** (MODIFY)
   - Ajouter validation avant POST/PUT
   - Erreurs backend formatting

### Test cases
- [ ] Required field empty = error
- [ ] Invalid email = error
- [ ] Valid data = submit works
- [ ] Special chars in name = allowed
- [ ] Negative temp = error

---

## 🖼️ Phase 3.2 - Photo Gallery (8h)

### Objectifs
- Upload photo endpoint (backend)
- Gallery view in detail page
- Image carousel
- Delete photo
- Thumbnail generation

### Backend Changes (4h)
1. **backend/app/routes/photos.py** (MODIFY)
   - POST /api/plants/{id}/photos (upload)
   - GET /api/plants/{id}/photos (list)
   - DELETE /api/plants/{id}/photos/{photo_id}
   - Image validation (mime type, size)

2. **backend/app/models/photos.py** (CHECK)
   - Photo model already exists
   - Add constraints: max file size, allowed types

3. **backend/app/services/photos_service.py** (CHECK/EXTEND)
   - Image upload logic
   - Thumbnail generation
   - Error handling

### Frontend Changes (4h)
1. **frontend/src/components/PhotoGallery.jsx** (CREATE)
   - Display photos in grid
   - Lightbox/modal on click
   - Delete button on hover
   - Upload button + file input

2. **frontend/src/pages/PlantDetailPage.jsx** (MODIFY)
   - Add PhotoGallery component
   - Show photo count badge

3. **frontend/src/lib/api.js** (MODIFY)
   - photosAPI.upload(plantId, file)
   - photosAPI.delete(plantId, photoId)
   - photosAPI.list(plantId)

### Test cases
- [ ] Upload JPG/PNG works
- [ ] File size validation works
- [ ] Gallery displays photos
- [ ] Delete photo works
- [ ] Thumbnail generates

---

## 📅 Phase 3.3 - History Timeline (7h)

### Objectifs
- Display all history events
- Timeline visual component
- Filter by event type
- Sort by date

### Backend (No changes needed)
- Endpoints already exist at /api/plants/{id}/histories

### Frontend Changes (7h)
1. **frontend/src/components/HistoryTimeline.jsx** (CREATE)
   - Timeline UI (vertical line + events)
   - Event cards with:
     - Date + time
     - Event type icon (watering, disease, repot, fertilize, notes)
     - Description
     - Author (if tracked)
   - Color-coded by type

2. **frontend/src/pages/PlantDetailPage.jsx** (MODIFY)
   - Add HistoryTimeline component
   - Tab: Details / History / Photos

3. **frontend/src/hooks/useHistory.js** (CREATE)
   - Custom hook for history data
   - Fetch from /api/plants/{id}/histories
   - Sort by date desc

4. **frontend/src/lib/api.js** (MODIFY)
   - historiesAPI.getAll(plantId)
   - historiesAPI.getWaterings(plantId)
   - historiesAPI.getDiseases(plantId)
   - etc.

### Test cases
- [ ] Timeline displays events
- [ ] Events sorted by date
- [ ] Filter by type works
- [ ] Icons display correctly

---

## 🧪 Phase 3.4 - E2E Tests (5h)

### Objectifs
- Test full user flows with Cypress
- CRUD operations end-to-end
- Photo upload E2E
- Form validation E2E

### Setup (1h)
```bash
npm install --save-dev cypress
npx cypress open
```

### Test files to create (4h)
1. **frontend/cypress/e2e/dashboard.cy.js**
   - Load dashboard
   - Search plants
   - Filter plants

2. **frontend/cypress/e2e/crud.cy.js**
   - Create plant
   - Edit plant
   - Delete plant
   - Archive/Restore plant

3. **frontend/cypress/e2e/form-validation.cy.js**
   - Required fields validation
   - Error messages display

4. **frontend/cypress/e2e/photos.cy.js**
   - Upload photo
   - View gallery
   - Delete photo

### Test cases (each file)
- [ ] Happy path works
- [ ] Error handling works
- [ ] UI updates correctly

---

## 📊 Priority & Effort Map

```
Effort vs Value Matrix:

HIGH VALUE, MEDIUM EFFORT:
├─ Form Validation (5h)     ⭐⭐⭐⭐⭐
└─ E2E Tests (5h)           ⭐⭐⭐⭐

HIGH VALUE, HIGH EFFORT:
├─ Photo Gallery (8h)       ⭐⭐⭐⭐
└─ History Timeline (7h)    ⭐⭐⭐

LOW VALUE, LOW EFFORT:
└─ Polish UI (2h)           ⭐⭐
```

**Recommended Order:**
1. Form Validation (quick win + better UX)
2. Photo Gallery (core feature)
3. History Timeline (nice-to-have)
4. E2E Tests (quality assurance)

---

## 🚀 Getting Started Phase 3

### Day 1 (6h)
```bash
# Start with validation
npm install zod

# Create schemas.js
touch frontend/src/lib/schemas.js

# Update PlantFormPage.jsx
# Add validation logic

# Test: Create plant with validation
```

### Day 2 (8h)
```bash
# Continue with photos
# Implement PhotoGallery component
# Test upload flow

# Or continue with timeline
# Implement HistoryTimeline component
```

### Day 3 (6h)
```bash
# Add E2E tests
npm install --save-dev cypress
npx cypress open

# Write test cases
```

### Day 4+ (5h)
```bash
# Polish & refinements
# Performance tuning
# Documentation
```

---

## 📝 Checklist Prêt à Commencer

- [ ] Lire ce document
- [ ] Créer branche Phase 3: `git checkout -b phase-3-validation`
- [ ] Installer Zod: `npm install zod`
- [ ] Créer `frontend/src/lib/schemas.js`
- [ ] Commencer avec Form Validation
- [ ] Test en local
- [ ] Commit + Push
- [ ] Repeat pour chaque feature

---

**Next:** Prêt pour Phase 3.1 - Form Validation! 🎯

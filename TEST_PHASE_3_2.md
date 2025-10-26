# Phase 3.2 - Tests E2E Photo Gallery

## Résumé des Tâches Complétées

### ✅ Backend (100%)
- [x] Photo Model + Migration (ORM SQLAlchemy + Alembic)
- [x] POST /api/plants/{id}/photos (Upload WebP, 3 versions)
- [x] GET /api/plants/{id}/photos (List photos)
- [x] DELETE /api/plants/{id}/photos/{photo_id} (Remove photo)
- [x] PUT /api/plants/{id}/photos/{photo_id}/set-primary (Set primary)
- [x] GET /api/photos/{plant_id}/{filename} (Serve WebP)

### ✅ Frontend (100%)
- [x] photosAPI.js (All methods: upload, delete, list, setPrimary, getPhotoUrl)
- [x] PlantPhotoUpload.jsx (Drag & drop, preview, progress)
- [x] PlantPhotoGallery.jsx (Responsive grid, thumbnails, hover delete)
- [x] PhotoCarousel.jsx (Modal, navigation, keyboard shortcuts)
- [x] PlantFormPage integration (Section photos + upload + gallery)

## Plan de Test E2E

### Test 1: Upload Photo
**Objectif:** Tester l'upload d'une image et la conversion WebP

**Étapes:**
1. Créer une plante de test
2. Aller à la page d'édition
3. Utiliser le composant PlantPhotoUpload pour uploader une image
4. Vérifier:
   - ✅ Image préviewée
   - ✅ Progress bar visible (0-100%)
   - ✅ Appel API réussi
   - ✅ Photo apparaît dans la galerie
   - ✅ Fichier WebP généré (vérifier data/photos/{plant_id}/)
   - ✅ Fichier < 800KB (max size)

### Test 2: Gallery Display
**Objectif:** Tester l'affichage de la galerie

**Étapes:**
1. Après upload, vérifier la galerie:
   - ✅ Thumbnail 150x150px affiché
   - ✅ Badge "Principale" visible sur première photo
   - ✅ Bouton hover (delete + set primary)
   - ✅ Grille responsive (2-4 colonnes)

### Test 3: Carousel Navigation
**Objectif:** Tester la navigation du carousel

**Étapes:**
1. Cliquer sur une thumbnail pour ouvrir le carousel
2. Tester:
   - ✅ Modal plein écran
   - ✅ Image large 1200px affichée
   - ✅ Boutons prev/next fonctionnels
   - ✅ Compteur (1/1, 2/2, etc.)
   - ✅ Navigation clavier (← → ESC)

### Test 4: Delete Photo
**Objectif:** Tester la suppression de photo

**Étapes:**
1. Dans la galerie, hover et cliquer delete sur une photo
2. Confirmer la suppression
3. Vérifier:
   - ✅ Photo disparaît de la galerie
   - ✅ Fichier supprimé (3 versions: large, medium, thumbnail)
   - ✅ BD mise à jour
   - ✅ Si photo était principale, reassigner à une autre

### Test 5: Set Primary Photo
**Objectif:** Tester le changement de photo principale

**Étapes:**
1. Upload 2+ photos
2. Sur une non-principale, cliquer sur bouton étoile
3. Vérifier:
   - ✅ Badge "Principale" change
   - ✅ BD mise à jour (is_primary flag)
   - ✅ Galerie rafraîchit correctement

### Test 6: Form Submission with Photos
**Objectif:** Tester la sauvegarde du formulaire avec photos

**Étapes:**
1. Éditer une plante avec photos
2. Cliquer "Mettre à jour"
3. Vérifier:
   - ✅ Photos restent dans la galerie
   - ✅ Formulaire sauvegarde correctement
   - ✅ Redirection vers dashboard

## Résumé Architecture

```
Data: data/photos/{plant_id}/
  ├── photo_1_large.webp     (1200x1200, ~800KB)
  ├── photo_1_medium.webp    (400x400, ~300KB)
  ├── photo_1_thumbnail.webp (150x150, ~50KB)
  ├── photo_2_large.webp
  ├── photo_2_medium.webp
  └── photo_2_thumbnail.webp

Database: photos table
  - id (PK)
  - plant_id (FK → plants)
  - filename (e.g., "photo_1")
  - file_size (bytes)
  - width, height
  - is_primary (bool)
  - created_at, updated_at

API Endpoints:
  POST   /api/plants/{id}/photos
  GET    /api/plants/{id}/photos
  DELETE /api/plants/{id}/photos/{photo_id}
  PUT    /api/plants/{id}/photos/{photo_id}/set-primary
  GET    /api/photos/{plant_id}/{filename}

Frontend Components:
  PlantPhotoUpload  → Drag & drop upload
  PlantPhotoGallery → Grid display
  PhotoCarousel     → Full-screen viewer
```

## Commits Effectués

1. `9c46c21` - Photo model + migration + schemas
2. `3c2c4d3` - Image processor utility + photo routes
3. `32951b3` - photosAPI client + PlantPhotoUpload
4. `52a51b6` - PlantPhotoGallery + PhotoCarousel + Integration

## Checklist Finale

- [x] Backend infrastructure complète
- [x] Frontend components complètes
- [x] Integration PlantFormPage
- [ ] Tests manuels E2E
- [ ] Documentation complète

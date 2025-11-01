# 📋 PLAN DE TESTS COMPLETS - PHASE 4

**Date:** 2 novembre 2025  
**Branch:** 2.20  
**Objectif:** Valider tous les flows actuels de l'application

---

## 🎯 RÉSUMÉ EXÉCUTIF

### Scope de test
- ✅ Fréquences saisonnières (arrosage + fertilisation)
- ✅ Formulaires create/edit plantes
- ✅ Modal plant detail
- ✅ Page fullscreen `/plants/{id}`
- ✅ Gallery photo + carousel
- ✅ Historiques (4 types)
- ✅ Responsive mobile

### Résultats attendus
- **Backend:** Tous les tests API passent ✅
- **Frontend:** Tous les flows E2E complètes ✅
- **Mobile:** Responsive sur écrans < 768px ✅

---

## 📝 TESTS UNITAIRES BACKEND

### Fichier: `backend/tests/test_seasonal_frequencies.py`

#### 1. TestSeasonalWateringAPI
```python
✓ test_get_seasonal_watering
✓ test_put_seasonal_watering  
✓ test_get_all_seasonal_watering
```

**Attendu:**
- GET retourne la fréquence ou 404
- PUT met à jour la fréquence
- GET all retourne liste de toutes les saisons

#### 2. TestSeasonalFertilizingAPI
```python
✓ test_get_seasonal_fertilizing
✓ test_put_seasonal_fertilizing
✓ test_get_all_seasonal_fertilizing
```

**Attendu:**
- GET retourne la fréquence fertilisation ou 404
- PUT met à jour correctement
- GET all retourne 4 entrées (4 saisons)

#### 3. TestLookupFrequencies
```python
✓ test_get_watering_frequencies
✓ test_get_fertilizer_frequencies
✓ test_get_seasons
```

**Attendu:**
- Watering: Exactement 7 fréquences
  - Fréquent (quotidien)
  - Régulier (2-3x/semaine)
  - Normal (1x/semaine)
  - Rare (2x/mois)
  - Très rare (1x/mois)
  - Garder humide
  - Laisser sécher

- Fertilizer: Exactement 6 fréquences
  - Fréquent (hebdomadaire)
  - Régulier (bi-hebdomadaire)
  - Normal (mensuel)
  - Rare (6 semaines)
  - Très rare (trimestriel)
  - Aucune fertilisation

- Seasons: 4 saisons avec mois corrects
  - Printemps (3-5)
  - Été (6-8)
  - Automne (9-11)
  - Hiver (12-2)

#### 4. TestSeasonalWorkflow
```python
✓ test_complete_workflow
✓ test_season_detection
```

**Attendu:**
- Créer plante → Ajouter fréquences → Récupérer → Modifier fonctionne
- Détection saison actuelle correcte

#### 5. TestFrequencyIntegrity
```python
✓ test_watering_frequency_intervals
✓ test_fertilizer_frequency_intervals
✓ test_no_duplicate_frequencies
```

**Attendu:**
- Tous les intervals sont valides (pas NULL sauf exceptions)
- Pas de doublons dans les noms

---

## 🧪 TESTS E2E FRONTEND

### Fichier: `frontend/src/__tests__/e2e/plant-flows.e2e.cy.js`

#### 1. Create Plant with Seasonal Frequencies
```javascript
✓ should create a new plant with seasonal watering frequencies
✓ should display seasonal frequencies in modal
✓ should update seasonal frequencies
```

**Attendu:**
- Form créer plante affiche 4 selects par saison (arrosage + fertilisation)
- Données sauvegardées en base
- Modale affiche fréquences sauvegardées
- Éditer une fréquence fonctionne

#### 2. Modal Plant Detail
```javascript
✓ should display all card sections
✓ should open action forms
✓ should handle photo carousel correctly
✓ should display gallery thumbnails
```

**Attendu:**
- Modale affiche: Besoins, Arrosage saison, Fertilisation saison, 4 historiques
- 4 boutons "Créer" fonctionnent (ouvre formulaire sans fermer modale)
- Carousel peut fermer sans fermer modale
- Galerie thumbnails cliquables

#### 3. Plant Detail Page (/plants/{id})
```javascript
✓ should display exact same content as modal
✓ should be able to edit from detail page
```

**Attendu:**
- Page fullscreen identique à modale
- Bouton éditer fonctionne

#### 4. Home Page / Plant List
```javascript
✓ should display plant cards
✓ should filter/search plants
✓ should open plant detail from card
```

**Attendu:**
- Liste des plantes affichée
- Search/filter fonctionne
- Click card ouvre modale

#### 5. Mobile Responsiveness
```javascript
✓ should adapt modal layout for mobile
✓ should make forms mobile-friendly
✓ should display buttons correctly on mobile
```

**Attendu:**
- Sur mobile (< 768px):
  - Colonnes se stackent (1 colonne au lieu de 2)
  - Inputs/selects cliquables et lisibles
  - Boutons accessibles
  - Text readable (pas de zoom nécessaire)

#### 6. Complete Workflow
```javascript
✓ should complete full user journey
```

**Attendu:**
- Créer plante → Ouvrir modale → Créer arrosage → Vérifier historique → Retour accueil
- Tout fonctionne sans erreurs

---

## 🚀 COMMENT LANCER LES TESTS

### Tests Backend
```bash
cd backend

# Tous les tests
pytest tests/test_seasonal_frequencies.py -v

# Test spécifique
pytest tests/test_seasonal_frequencies.py::TestLookupFrequencies::test_get_watering_frequencies -v

# Avec coverage
pytest tests/test_seasonal_frequencies.py --cov=app --cov-report=html
```

### Tests E2E Frontend (Cypress)
```bash
cd frontend

# Lancer Cypress UI
npx cypress open

# Lancer tests headless
npx cypress run --spec "src/__tests__/e2e/plant-flows.e2e.cy.js"

# Avec vidéo
npx cypress run --spec "src/__tests__/e2e/plant-flows.e2e.cy.js" --record
```

---

## ✅ CHECKLIST DE VALIDATION

### Backend
- [ ] `test_seasonal_frequencies.py` passe 100%
- [ ] Aucun duplicate fréquence
- [ ] API routes retournent bon status
- [ ] Données persist correctement
- [ ] Saisons détectées correctement

### Frontend - Flows
- [ ] Créer plante avec saisons
- [ ] Modal affiche fréquences
- [ ] Éditer fréquences fonctionne
- [ ] Page /plants/{id} identique modale
- [ ] Carousel n'interfère pas modale
- [ ] Gallery fonctionne
- [ ] Tous 4 boutons actions ouvrent formes

### Frontend - Mobile
- [ ] Modal responsive (1 colonne)
- [ ] Form create responsive
- [ ] Buttons cliquables
- [ ] Text readable
- [ ] Pas de horizontal scroll

### Edge Cases
- [ ] Plant sans photos
- [ ] Plant sans historiques
- [ ] Plant sans fréquences saisonnières définies
- [ ] Détection saison à la frontière (ex: 1er mars)
- [ ] Saison hiver (cross-year 12->2)

---

## 📊 RÉSULTATS ATTENDUS

### Coverage Frontend
- Plant list: > 90%
- Plant detail modal: > 85%
- Plant form: > 80%
- Responsive: Validated

### Coverage Backend
- Seasonal routes: > 95%
- Lookup routes: > 95%
- Models: > 90%

### Performance
- Modal load: < 500ms
- Photo carousel: < 300ms
- Form submit: < 1s

---

## 📌 NOTES IMPORTANTES

1. **Fréquences:** 7 arrosage + 6 fertilisation (pas de doublons)
2. **Saisons:** Exactement 4 avec mois corrects
3. **Modal:** Identique à `/plants/{id}` fullscreen
4. **Mobile:** < 768px = 1 colonne
5. **Actions:** Créer form ne ferme pas modale

---

## 🔄 PROCHAINES ÉTAPES APRÈS TESTS

Si tous les tests ✅:
1. Commit `test: Add comprehensive test suite for seasonal frequencies`
2. Commencer PHASE 5: Optimisations UX/UI
3. Ajouter animations + improved responsive

Si des tests ❌:
1. Debug problème identifié
2. Fix le code
3. Re-run tests
4. Recommencer

---

**Rédigé:** 2 novembre 2025  
**Version:** 1.0

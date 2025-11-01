# 🌐 Guide des Tests Live en Navigateur - Phase 3.1

**Status:** ✅ Prêt à tester  
**URL:** http://localhost:5173  
**Backend:** http://localhost:8001  
**Date:** 26 octobre 2025

---

## 🎯 Objectif

Vérifier que TOUTES les validations fonctionnent correctement dans le formulaire:
- ✅ Validations format (Zod côté client)
- ✅ Auto-corrections (subsp., var., cultivar)
- ✅ Validations inter-champs (genus+species)
- ✅ Messages d'erreur français
- ✅ Red styling on error
- ✅ Création et édition plantes

---

## 📋 Étapes Préalables

### 1. Vérifier les Serveurs
```bash
# Backend
curl http://localhost:8001/api/plants | head

# Frontend (juste ouvrir dans le navigateur)
# http://localhost:5173
```

### 2. Ouvrir Navigateur
```
http://localhost:5173
```

### 3. Ouvrir Console Developer (F12)
```
- Appuyer sur F12
- Onglet "Console"
- On verra les logs Zod
```

---

## 🧪 Test 1: Validation Genus (Majuscule Requise)

### 1.1 ❌ Genus Minuscule - DOIT ÉCHOUER

**Actions:**
1. Cliquer "Nouvelle Plante"
2. Remplir:
   - Name: "Test Validation 1"
   - Family: "Orchidaceae"
3. Dans Genus, entrer: **"phalaenopsis"** (minuscule)
4. Appuyer Tab ou cliquer sur Species

**Attendre et Observer:**

✅ **Attendu:**
```
- Red border autour du champ Genus
- Fond rouge clair (bg-red-50)
- Message d'erreur en rouge:
  "Le genre doit commencer par une majuscule suivie de minuscules (ex: Phalaenopsis)"
```

❓ **Si pas visible:**
- Vérifier Console (F12) pour les logs Zod
- Vérifier que schemas.js est chargé

---

### 1.2 ✅ Corriger le Genus - DOIT PASSER

**Actions:**
1. Effacer le contenu du champ Genus
2. Entrer: **"Phalaenopsis"** (majuscule correct)
3. Appuyer Tab ou cliquer ailleurs

**Attendre et Observer:**

✅ **Attendu:**
```
- Red border DISPARAIT
- Message d'erreur DISPARAIT
- Champ redevient normal
```

---

### 1.3 ❌ Genus Tout Majuscule - DOIT ÉCHOUER

**Actions:**
1. Effacer et entrer: **"PHALAENOPSIS"** (tout majuscule)
2. Appuyer Tab

**Attendre et Observer:**

✅ **Attendu:**
```
- Red border réapparait
- Même message d'erreur: "Le genre doit commencer par une majuscule..."
```

---

## 🧪 Test 2: Validation Species (Minuscule Requise)

### 2.1 ❌ Species Majuscule - DOIT ÉCHOUER

**Actions:**
1. Remplir Genus: "Phalaenopsis" (correct)
2. Dans Species, entrer: **"Amabilis"** (majuscule)
3. Appuyer Tab

**Attendre et Observer:**

✅ **Attendu:**
```
- Red border autour du champ Species
- Message d'erreur:
  "L'espèce doit être entièrement minuscule (ex: amabilis)"
```

---

### 2.2 ✅ Species Minuscule - DOIT PASSER

**Actions:**
1. Effacer et entrer: **"amabilis"** (minuscule)
2. Appuyer Tab

**Attendre et Observer:**

✅ **Attendu:**
```
- Red border DISPARAIT
- Message d'erreur DISPARAIT
```

---

## 🧪 Test 3: Règle Inter-Champs (Ensemble ou Rien)

### 3.1 ❌ Species Sans Genus - DOIT ÉCHOUER

**Actions:**
1. Vider le champ Genus
2. Remplir Species: "amabilis"
3. Cliquer "Créer"

**Attendre et Observer:**

✅ **Attendu:**
```
- Erreur sur le champ Genus:
  "Le genre est obligatoire si l'espèce est fournie"
- Formulaire ne se soumet pas
```

---

### 3.2 ❌ Genus Sans Species - DOIT ÉCHOUER

**Actions:**
1. Remplir Genus: "Phalaenopsis"
2. Vider Species
3. Cliquer "Créer"

**Attendre et Observer:**

✅ **Attendu:**
```
- Erreur sur le champ Species:
  "Le genre et l'espèce doivent être fournis ensemble"
- Formulaire ne se soumet pas
```

---

### 3.3 ✅ Genus ET Species - DOIT PASSER

**Actions:**
1. Remplir Genus: "Phalaenopsis"
2. Remplir Species: "amabilis"
3. Vérifier: Pas d'erreur sur ces deux champs

**Attendre et Observer:**

✅ **Attendu:**
```
- Pas de red border
- Pas d'erreur
- Prêt à créer
```

---

## 🧪 Test 4: Auto-Correction Subspecies

### 4.1 Subspecies Auto-Préfixe

**Actions:**
1. Créer une nouvelle plante
2. Remplir:
   - Name: "Test Subspecies"
   - Family: "Orchidaceae"
   - Genus: "Phalaenopsis"
   - Species: "amabilis"
3. Dans Subspecies, entrer: **"rosenstromii"** (sans "subsp.")
4. Cliquer "Créer"

**Attendre et Observer:**

✅ **Attendu:**
```
1. Plante créée sans erreur ✅
2. Voir message: "Plante créée avec succès!"
3. Redirection dashboard
4. Cliquer "Éditer" sur la plante
5. Subspecies affiche: "subsp. rosenstromii" (préfixe auto-ajouté!)
```

---

### 4.2 Subspecies Déjà avec Préfixe

**Actions:**
1. Créer une autre plante
2. Dans Subspecies, entrer: **"subsp. alba"** (avec "subsp.")
3. Cliquer "Créer"
4. Éditer et vérifier

**Attendre et Observer:**

✅ **Attendu:**
```
- Stocké tel quel: "subsp. alba"
- Pas de duplication du préfixe
```

---

## 🧪 Test 5: Auto-Correction Variety

### Procédure identique au Test 4

**Actions:**
1. Créer plante
2. Variety: **"alba"** (sans "var.")
3. Vérifier après création: "var. alba" ✅

---

## 🧪 Test 6: Auto-Correction Cultivar

### Procédure identique au Test 4

**Actions:**
1. Créer plante
2. Cultivar: **"White Dream"** (sans guillemets)
3. Vérifier après création: "'White Dream'" ✅

**Note:** Cultivar peut être majuscule (contrairement à species)

---

## 🧪 Test 7: Création Plante Minimale

### Actions:
```
Name: "Ma première plante"
Family: "Araceae"
[Tous les autres champs vides]
Cliquer "Créer"
```

### Attendre et Observer:

✅ **Attendu:**
```
- ✅ Validation passe
- ✅ Plante créée (pas d'erreur)
- ✅ Reference auto-générée visible
- ✅ Visible au dashboard
```

---

## 🧪 Test 8: Création Plante Complète

### Remplir TOUS les champs:

```
=== INFORMATIONS DE BASE ===
Name: "Phalaenopsis élégante"
Family: "Orchidaceae"
Subfamily: "epidendroideae"
Genus: "Phalaenopsis"
Species: "amabilis"
Subspecies: "rosenstromii"  (auto → "subsp. rosenstromii")
Variety: "alba"             (auto → "var. alba")
Cultivar: "Pink Dream"      (auto → "'Pink Dream'")

=== ENVIRONNEMENT ===
Temp min: 15
Temp max: 25
Humidity: 70
Soil type: "terreau"
Watering Frequency: [Sélectionner une]
Light Requirement: [Sélectionner une]
Location: [Sélectionner une]

=== DESCRIPTION ET SOINS ===
Description: "Magnifique orchidée d'intérieur très facile"
Care Instructions: "Arroser une fois par semaine avec eau tiède. Éviter eau stagnante."
Difficulty Level: "medium"
Growth Speed: "slow"
Flowering Season: "Hiver"

=== PROPRIÉTÉS ===
Favorite: ☑️ (coché)
Indoor: ☑️ (coché)
Outdoor: ☐ (non coché)
Toxic: ☐ (non coché)
```

### Cliquer "Créer"

### Attendre et Observer:

✅ **Attendu:**
```
- ✅ Validation passe (tous les champs valides)
- ✅ Plante créée
- ✅ Reference générée: "ORCHI-XXX" (auto)
- ✅ Scientific_name généré: "Phalaenopsis amabilis"
- ✅ Visible au dashboard
```

---

## 🧪 Test 9: Édition - Reference & Scientific_name Lecture-Seule

### Actions:
1. Cliquer "Éditer" sur la plante créée (Test 8)
2. Observer

### Attendre et Observer:

✅ **Attendu:**
```
- Reference affichée en gris (bg-gray-100): "ORCHI-XXX"
- Scientific_name affichée en gris: "Phalaenopsis amabilis"
- Champs NE PEUVENT PAS être modifiés
- Tous les autres champs pré-remplis
```

### Modifier et Sauvegarder:
1. Modifier un champ (ex: Family → "Araucariaceae")
2. Cliquer "Mettre à jour"
3. Vérifier: Reference inchangée

---

## 🧪 Test 10: Messages d'Erreur Français

### Tester CHAQUE message:

```
❌ Laisser Name vide
   → "Le nom est obligatoire"

❌ Laisser Family vide
   → "La famille est obligatoire"

❌ Genus minuscule
   → "Le genre doit commencer par une majuscule..."

❌ Species majuscule
   → "L'espèce doit être entièrement minuscule..."

❌ Species sans Genus
   → "Le genre est obligatoire si l'espèce est fournie"

❌ Genus sans Species
   → "Le genre et l'espèce doivent être fournis ensemble"

❌ Subspecies majuscule
   → "La sous-espèce doit être minuscule..."

❌ Variety majuscule
   → "La variété doit être minuscule..."
```

---

## 📊 Checklist des Observations

### Validations Format
- [ ] Genus minuscule → Red border + message
- [ ] Genus majuscule complet → Red border
- [ ] Species majuscule → Red border + message
- [ ] Subspecies majuscule → Red border + message
- [ ] Variety majuscule → Red border + message

### Règles Inter-Champs
- [ ] Species sans Genus → Erreur "Genus obligatoire"
- [ ] Genus sans Species → Erreur "ensemble"

### Auto-Corrections
- [ ] Subspecies "rosenstromii" → "subsp. rosenstromii"
- [ ] Variety "alba" → "var. alba"
- [ ] Cultivar "White Dream" → "'White Dream'"

### Création/Édition
- [ ] Plante minimale créée
- [ ] Plante complète créée
- [ ] Reference auto-générée
- [ ] Scientific_name auto-généré
- [ ] Édition: Reference lecture-seule
- [ ] Édition: Scientific_name lecture-seule

### UI/UX
- [ ] Red border disparait quand corrigé
- [ ] Messages français affichés
- [ ] Formulaire responsive
- [ ] Erreurs claires et utiles

### Dashboard
- [ ] Plantes créées visibles
- [ ] Tous les champs s'affichent
- [ ] Édition fonctionne
- [ ] Suppression fonctionne

---

## 🔍 Debug - Si Erreur

### Console Browser (F12)

**Voir les logs Zod:**
```javascript
// Copier dans console:
console.log("Checking validation...");

// Regarder les erreurs de validation
// Les logs devraient afficher:
// { success: false, errors: { fieldName: "message d'erreur" } }
```

### Network Tab (F12)

**Voir les requêtes API:**
1. Onglet "Network"
2. Créer une plante
3. Observer:
   - POST /api/plants
   - Payload: sans reference, sans scientific_name ✅
   - Response: { id, reference, scientific_name, ... } ✅

### Backend Logs

```bash
# Voir les logs du backend:
# Chercher: "POST /api/plants"
# Chercher les 201 (Created) ou 422 (Validation Error)
```

---

## ✅ Fin des Tests

### Une fois TOUS les tests passés:

1. ✅ Mettre à jour TEST_RESULTS_PHASE_3_1.md
2. ✅ Cocher toutes les cases
3. ✅ Commiter les résultats
4. ✅ Phase 3.1 = COMPLÈTE ✅

---

**Bon testage! 🌱✅**


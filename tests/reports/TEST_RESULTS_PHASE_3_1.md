# 🧪 Résultats des Tests Live - Phase 3.1

**Date:** 26 octobre 2025  
**Tester:** Live in Browser (http://localhost:5173)  
**Backend:** http://localhost:8001

---

## 📊 Résumé Exécutif

```
Tests Total:     30+
Tests Passés:    ⏳ En cours...
Tests Échoués:   ⏳ En cours...
Coverage:        ⏳ En cours...
```

---

## 🧪 Test 1: Validation Genus - Format Majuscule

### 1.1 ❌ Genus minuscule (phalaenopsis)

**Input:**
```
Name: "Test Phalaenopsis 1"
Family: "Orchidaceae"
Genus: "phalaenopsis"  ← minuscule
Species: [vide]
```

**Expected:** ❌ Erreur rouge  
**Message attendu:** "Le genre doit commencer par une majuscule..."

**Résultat:** ⏳ À tester

---

### 1.2 ✅ Genus correct (Phalaenopsis)

**Input:**
```
Name: "Test Phalaenopsis 2"
Family: "Orchidaceae"
Genus: "Phalaenopsis"  ← correct
Species: [vide]
```

**Expected:** ✅ OK (pas d'erreur sur genus)

**Résultat:** ⏳ À tester

---

### 1.3 ❌ Genus tout majuscule (PHALAENOPSIS)

**Input:**
```
Name: "Test Phalaenopsis 3"
Family: "Orchidaceae"
Genus: "PHALAENOPSIS"  ← tout majuscule
Species: [vide]
```

**Expected:** ❌ Erreur rouge  
**Message attendu:** "Le genre doit commencer par une majuscule suivie de minuscules..."

**Résultat:** ⏳ À tester

---

## 🧪 Test 2: Validation Species - Format Minuscule

### 2.1 ❌ Species majuscule (Amabilis)

**Input:**
```
Name: "Test Species 1"
Family: "Orchidaceae"
Genus: "Phalaenopsis"
Species: "Amabilis"  ← majuscule
```

**Expected:** ❌ Erreur rouge sur species  
**Message attendu:** "L'espèce doit être entièrement minuscule..."

**Résultat:** ⏳ À tester

---

### 2.2 ✅ Species correct (amabilis)

**Input:**
```
Name: "Test Species 2"
Family: "Orchidaceae"
Genus: "Phalaenopsis"
Species: "amabilis"  ← correct
```

**Expected:** ✅ OK (pas d'erreur)

**Résultat:** ⏳ À tester

---

## 🧪 Test 3: Règle Inter-Champs - Genus Obligatoire si Species

### 3.1 ❌ Species sans Genus

**Input:**
```
Name: "Test Rule 1"
Family: "Orchidaceae"
Genus: [vide]
Species: "amabilis"  ← sans genus!
```

**Expected:** ❌ Erreur sur genus  
**Message attendu:** "Le genre est obligatoire si l'espèce est fournie"

**Résultat:** ⏳ À tester

---

### 3.2 ❌ Genus sans Species

**Input:**
```
Name: "Test Rule 2"
Family: "Orchidaceae"
Genus: "Phalaenopsis"  ← sans species!
Species: [vide]
```

**Expected:** ❌ Erreur  
**Message attendu:** "Le genre et l'espèce doivent être fournis ensemble"

**Résultat:** ⏳ À tester

---

### 3.3 ✅ Genus et Species ensemble

**Input:**
```
Name: "Test Rule 3"
Family: "Orchidaceae"
Genus: "Phalaenopsis"
Species: "amabilis"
```

**Expected:** ✅ OK

**Résultat:** ⏳ À tester

---

## 🧪 Test 4: Auto-Correction Subspecies

### 4.1 Auto-ajout du préfixe "subsp."

**Input:**
```
Subspecies: "rosenstromii"  ← sans "subsp."
```

**Expected:** ✅ Stocké comme "subsp. rosenstromii"

**Résultat:** ⏳ À tester

**Vérification:** Éditer la plante et voir que subspecies = "subsp. rosenstromii"

---

### 4.2 Subspecies déjà avec préfixe

**Input:**
```
Subspecies: "subsp. alba"  ← déjà avec "subsp."
```

**Expected:** ✅ Gardé tel quel "subsp. alba"

**Résultat:** ⏳ À tester

---

### 4.3 ❌ Subspecies majuscule (Rosenstromii)

**Input:**
```
Subspecies: "Rosenstromii"  ← majuscule
```

**Expected:** ❌ Erreur rouge  
**Message attendu:** "La sous-espèce doit être minuscule..."

**Résultat:** ⏳ À tester

---

## 🧪 Test 5: Auto-Correction Variety

### 5.1 Auto-ajout du préfixe "var."

**Input:**
```
Variety: "alba"  ← sans "var."
```

**Expected:** ✅ Stocké comme "var. alba"

**Résultat:** ⏳ À tester

**Vérification:** Éditer la plante et voir que variety = "var. alba"

---

### 5.2 Variety déjà avec préfixe

**Input:**
```
Variety: "var. variegata"  ← déjà avec "var."
```

**Expected:** ✅ Gardé tel quel "var. variegata"

**Résultat:** ⏳ À tester

---

### 5.3 ❌ Variety majuscule (Alba)

**Input:**
```
Variety: "Alba"  ← majuscule
```

**Expected:** ❌ Erreur rouge  
**Message attendu:** "La variété doit être minuscule..."

**Résultat:** ⏳ À tester

---

## 🧪 Test 6: Auto-Correction Cultivar (Guillemets)

### 6.1 Auto-ajout des guillemets simples

**Input:**
```
Cultivar: "White Dream"  ← sans guillemets
```

**Expected:** ✅ Stocké comme "'White Dream'"

**Résultat:** ⏳ À tester

**Vérification:** Éditer la plante et voir que cultivar = "'White Dream'"

---

### 6.2 Cultivar déjà avec guillemets

**Input:**
```
Cultivar: "'Pink Dream'"  ← déjà avec guillemets
```

**Expected:** ✅ Gardé tel quel "'Pink Dream'"

**Résultat:** ⏳ À tester

---

### 6.3 ✅ Cultivar peut être majuscule (PINK DREAM)

**Input:**
```
Cultivar: "PINK DREAM"  ← majuscule (exception!)
```

**Expected:** ✅ Stocké comme "'PINK DREAM'" (les majuscules sont acceptées)

**Résultat:** ⏳ À tester

---

## 🧪 Test 7: Création Plante Minimale

### Input:
```
Name: "Ma première plante"
Family: "Araceae"
Genus: [vide]
Species: [vide]
Subspecies: [vide]
Variety: [vide]
Cultivar: [vide]
[Autres champs optionnels vides]
```

### Expected:
- ✅ Validation passe
- ✅ Plante créée sans erreur
- ✅ Reference auto-générée (visible après)
- ✅ Scientific_name vide ou auto-généré (visible après)
- ✅ Redirection dashboard

### Résultat:
⏳ À tester

### ID créé:
[sera rempli]

### Reference générée:
[sera rempli]

---

## 🧪 Test 8: Création Plante Complète

### Input:
```
Name: "Phalaenopsis élégante"
Family: "Orchidaceae"
Subfamily: "epidendroideae"
Genus: "Phalaenopsis"
Species: "amabilis"
Subspecies: "rosenstromii"  (auto → "subsp. rosenstromii")
Variety: "alba"             (auto → "var. alba")
Cultivar: "White Dream"     (auto → "'White Dream'")

Environment:
- Temp min: 15
- Temp max: 25
- Humidity: 70
- Soil type: "terreau"
- Watering frequency: [Sélectionner une]
- Light requirement: [Sélectionner une]
- Location: [Sélectionner une]

Description:
- Description: "Magnifique orchidée d'intérieur"
- Care Instructions: "Arroser avec eau tiède une fois par semaine. Éviter l'eau stagnante."
- Difficulty Level: "medium"
- Growth Speed: "slow"
- Flowering Season: "Hiver"

Propriétés:
- is_indoor: true
- is_favorite: true
- is_toxic: false
```

### Expected:
- ✅ Validation passe
- ✅ Plante créée sans erreur
- ✅ Reference auto-générée (ex: PHA-001)
- ✅ Scientific_name auto-généré: "Phalaenopsis amabilis"
- ✅ Subspecies stocké: "subsp. rosenstromii"
- ✅ Variety stocké: "var. alba"
- ✅ Cultivar stocké: "'White Dream'"
- ✅ Visible au dashboard avec tous les champs

### Résultat:
⏳ À tester

### ID créé:
[sera rempli]

### Reference générée:
[sera rempli]

### Scientific Name généré:
[sera rempli]

---

## 🧪 Test 9: Édition Plante (Reference & Scientific Name Lecture-Seule)

### Procédure:
1. Créer une plante complète (Test 8)
2. Cliquer "Éditer" sur la plante
3. Observer l'affichage

### Expected:
- ✅ Reference affichée en gris (lecture-seule): "PHA-001"
- ✅ Scientific_name affichée en gris (lecture-seule): "Phalaenopsis amabilis"
- ✅ Tous les autres champs pré-remplis
- ✅ Modifier Family et re-sauvegarder
- ✅ Reference inchangée
- ✅ Mise à jour réussie

### Résultat:
⏳ À tester

---

## 🧪 Test 10: Messages d'Erreur en Français

### Expected Messages:
- [ ] "Le nom est obligatoire" - laisser name vide
- [ ] "La famille est obligatoire" - laisser family vide
- [ ] "Le genre doit commencer par une majuscule..." - genus minuscule
- [ ] "L'espèce doit être entièrement minuscule..." - species majuscule
- [ ] "Le genre est obligatoire si l'espèce est fournie" - species sans genus
- [ ] "Le genre et l'espèce doivent être fournis ensemble" - genus sans species
- [ ] "La sous-espèce doit être minuscule..." - subspecies majuscule
- [ ] "La variété doit être minuscule..." - variety majuscule

### Résultat:
⏳ À tester

---

## 📋 Résumé Final

### Tests Passés: ⏳
```
[ ] Test 1.1 - Genus minuscule
[ ] Test 1.2 - Genus correct
[ ] Test 1.3 - Genus majuscule
[ ] Test 2.1 - Species majuscule
[ ] Test 2.2 - Species minuscule
[ ] Test 3.1 - Species sans Genus
[ ] Test 3.2 - Genus sans Species
[ ] Test 3.3 - Genus + Species
[ ] Test 4.1 - Subspecies auto-préfixe
[ ] Test 4.2 - Subspecies avec préfixe
[ ] Test 4.3 - Subspecies majuscule
[ ] Test 5.1 - Variety auto-préfixe
[ ] Test 5.2 - Variety avec préfixe
[ ] Test 5.3 - Variety majuscule
[ ] Test 6.1 - Cultivar auto-guillemets
[ ] Test 6.2 - Cultivar avec guillemets
[ ] Test 6.3 - Cultivar majuscule
[ ] Test 7 - Plante minimale
[ ] Test 8 - Plante complète
[ ] Test 9 - Édition lecture-seule
[ ] Test 10 - Messages français
```

### Notes Additionnelles:

[À remplir au fur et à mesure des tests]

---

**Status:** En cours de test 🧪


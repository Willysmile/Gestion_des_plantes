# 🧪 Test Plan - Phase 3.1 Validation Taxonomique

## État des Serveurs
- Backend: ✅ Tourne sur port 8001
- Frontend: ✅ Tourne sur port 5173

---

## 🎯 Tests à Effectuer

### **Test 1: Validation Genus - Format Majuscule**

#### 1.1 ❌ Genus minuscule (doit échouer)
```
Genus: "phalaenopsis"
Expected: ❌ Erreur rouge
Message: "Le genre doit commencer par une majuscule suivie de minuscules..."
```

#### 1.2 ✅ Genus correct (doit passer)
```
Genus: "Phalaenopsis"
Expected: ✅ OK (pas d'erreur)
```

#### 1.3 ❌ Genus tout majuscule (doit échouer)
```
Genus: "PHALAENOPSIS"
Expected: ❌ Erreur rouge
Message: "Le genre doit commencer par une majuscule suivie de minuscules..."
```

---

### **Test 2: Validation Species - Format Minuscule**

#### 2.1 ❌ Species majuscule (doit échouer)
```
Genus: "Phalaenopsis"
Species: "Amabilis"
Expected: ❌ Erreur rouge sur species
Message: "L'espèce doit être entièrement minuscule..."
```

#### 2.2 ✅ Species correct (doit passer)
```
Genus: "Phalaenopsis"
Species: "amabilis"
Expected: ✅ OK
```

---

### **Test 3: Règle Inter-Champs - Genus Obligatoire si Species**

#### 3.1 ❌ Species sans Genus (doit échouer)
```
Genus: [vide]
Species: "amabilis"
Expected: ❌ Erreur
Message: "Le genre est obligatoire si l'espèce est fournie"
```

#### 3.2 ❌ Genus sans Species (doit échouer)
```
Genus: "Phalaenopsis"
Species: [vide]
Expected: ❌ Erreur
Message: "Le genre et l'espèce doivent être fournis ensemble"
```

#### 3.3 ✅ Genus et Species ensemble (doit passer)
```
Genus: "Phalaenopsis"
Species: "amabilis"
Expected: ✅ OK
```

---

### **Test 4: Auto-Correction Subspecies**

#### 4.1 Auto-ajout du préfixe "subsp."
```
Input: "rosenstromii"
Expected: Stocké comme "subsp. rosenstromii" ✅
Au prochain chargement: Affiche "subsp. rosenstromii"
```

#### 4.2 Subspecies déjà avec préfixe
```
Input: "subsp. rosenstromii"
Expected: Gardé tel quel "subsp. rosenstromii" ✅
```

#### 4.3 ❌ Subspecies majuscule (doit échouer)
```
Input: "Rosenstromii"
Expected: ❌ Erreur
Message: "La sous-espèce doit être minuscule..."
```

---

### **Test 5: Auto-Correction Variety**

#### 5.1 Auto-ajout du préfixe "var."
```
Input: "alba"
Expected: Stocké comme "var. alba" ✅
Au prochain chargement: Affiche "var. alba"
```

#### 5.2 Variety déjà avec préfixe
```
Input: "var. alba"
Expected: Gardé tel quel "var. alba" ✅
```

#### 5.3 ❌ Variety majuscule (doit échouer)
```
Input: "Alba"
Expected: ❌ Erreur
Message: "La variété doit être minuscule..."
```

---

### **Test 6: Auto-Correction Cultivar (Guillemets)**

#### 6.1 Auto-ajout des guillemets simples
```
Input: "White Dream"
Expected: Stocké comme "'White Dream'" ✅
Au prochain chargement: Affiche "'White Dream'"
```

#### 6.2 Cultivar déjà avec guillemets
```
Input: "'Pink Dream'"
Expected: Gardé tel quel "'Pink Dream'" ✅
```

#### 6.3 ✅ Cultivar peut être majuscule (contrairement à species)
```
Input: "PINK DREAM"
Expected: Stocké comme "'PINK DREAM'" ✅ (exception pour cultivar)
```

---

### **Test 7: Création Plante Complète**

#### 7.1 Plante Minimaliste (seulement obligatoires)
```
Name: "Monstera"
Family: "Araceae"
Expected: ✅ Créé sans erreur
Reference: Auto-généré (ex: MON-001)
Scientific_name: Auto-généré (ex: empty jusqu'à genus+species)
```

#### 7.2 Plante Complète avec Taxonomie
```
Name: "Phalaenopsis hybride"
Family: "Orchidaceae"
Subfamily: "epidendroideae"
Genus: "Phalaenopsis"
Species: "amabilis"
Subspecies: "rosenstromii"  (auto → "subsp. rosenstromii")
Variety: "alba"             (auto → "var. alba")
Cultivar: "Pink Dream"      (auto → "'Pink Dream'")

Expected: ✅ Créé sans erreur
Reference: Auto-généré (ex: PHA-001)
Scientific_name: Phalaenopsis amabilis (auto-généré)
```

#### 7.3 Plante Complète avec tous les champs
```
+ Environnement: temp_min=10, temp_max=25, humidity=70, soil_type="terreau"
+ Sélectionner: watering_frequency (ex: Hebdomadaire), light_requirement (ex: Lumière vive)
+ Description: "Belle plante d'intérieur"
+ Care Instructions: "Arroser quand le sol est sec"
+ Difficulty Level: "medium"
+ Growth Speed: "fast"
+ Flowering Season: "Été"
+ Propriétés: is_indoor=true, is_favorite=true, is_toxic=false

Expected: ✅ Créé et visible au dashboard
```

---

### **Test 8: Édition Plante (Reference & Scientific Name en Lecture-Seule)**

#### 8.1 Ouvrir une plante créée
```
Expected: 
- ✅ Tous les champs pré-remplis
- ✅ Reference affichée en gris (lecture-seule): "MON-001"
- ✅ Scientific_name affichée en gris (lecture-seule): "Monstera deliciosa"
```

#### 8.2 Modifier et re-sauvegarder
```
Modifier: Family "Araceae" → "Araucariaceae"
Expected: ✅ Mise à jour sans erreur
Reference: Inchangée "MON-001"
Scientific_name: Recalculée si genus/species changés
```

---

### **Test 9: Messages d'Erreur en Français**

#### 9.1 Tous les messages doivent être en français
```
✅ "Le nom est obligatoire"
✅ "La famille est obligatoire"
✅ "Le genre doit commencer par une majuscule..."
✅ "L'espèce doit être entièrement minuscule..."
✅ "Le genre et l'espèce doivent être fournis ensemble"
✅ "La sous-espèce doit être minuscule..."
✅ "La variété doit être minuscule..."
✅ "Les instructions de soin doivent contenir au maximum 1000 caractères"
```

---

### **Test 10: Erreurs et Red Styling**

#### 10.1 Champ invalide → Red border + Red text
```
- Genus: "phalaenopsis" → border-red-500 + bg-red-50 ✅
- Message d'erreur en rouge ✅
```

#### 10.2 Erreur cleared au changement
```
- Utilisateur corrige: "phalaenopsis" → "Phalaenopsis"
- ✅ Red border disparait immédiatement
- ✅ Message d'erreur disparait
```

---

## 📋 Checklist de Testage

### Validations Immédiates (Client-side)
- [ ] Genus format majuscule validé
- [ ] Species format minuscule validé
- [ ] Subspecies format minuscule validé
- [ ] Variety format minuscule validé
- [ ] Cultivar auto-guillemets
- [ ] Genus+Species ensemble ou rien
- [ ] Name + Family obligatoires

### Auto-Transformations
- [ ] Subspecies "rosenstromii" → "subsp. rosenstromii"
- [ ] Variety "alba" → "var. alba"
- [ ] Cultivar "White Dream" → "'White Dream'"

### Création Plante
- [ ] Création minimale (name + family)
- [ ] Création complète avec taxonomie
- [ ] Auto-générations exclus du payload
- [ ] Reference générée par backend
- [ ] Scientific_name générée par backend

### Édition Plante
- [ ] Reference affichée lecture-seule
- [ ] Scientific_name affichée lecture-seule
- [ ] Modification champs fonctionne
- [ ] API PATCH envoie les bonnes données

### UI/UX
- [ ] Red styling on error
- [ ] Messages d'erreur français
- [ ] Erreurs cleared au changement
- [ ] Formulaire responsive
- [ ] Lookups affichés

---

## 🎬 Procédure de Test

1. **Ouvrir navigateur:** http://localhost:5173
2. **Cliquer "Créer une plante" ou "Nouvelle plante"**
3. **Tester chaque validation** (voir tests ci-dessus)
4. **Observer red borders + messages**
5. **Créer plantes valides** (minimales et complètes)
6. **Vérifier au dashboard** que les données s'affichent
7. **Éditer une plante** et vérifier reference/scientific_name lecture-seule
8. **Tester API** avec console logs

---

## 🔍 Logs Console à Observer

### Frontend Console (F12)
```javascript
// Validation Zod logs:
console.log("Validation result:", validation)
console.log("Errors:", fieldErrors)
console.log("Data to send:", dataToSend)

// Réponse API:
console.log("Create response:", response.data)
console.log("Error:", error.response?.data?.detail)
```

### Network Tab (F12)
```
POST http://localhost:8001/api/plants
Payload: { name, family, genus, species, ..., (NO reference, NO scientific_name) }
Response: { id, reference, scientific_name, ... } ✅
```

---

**Bon testage! 🌱✅**


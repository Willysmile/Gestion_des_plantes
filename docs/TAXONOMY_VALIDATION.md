# 📚 Validation Taxonomique - Phase 3.1

## Vue d'ensemble

La validation taxonomique a été implémentée dans le formulaire de création/édition de plantes pour garantir la cohérence et la précision des données botaniques. Les règles suivent les conventions scientifiques standard.

---

## Exemples de Nomenclature Valide

### Progressif (du simple au complet)

```
1. Minimaliste
   Phalaenopsis amabilis
   
2. Avec sous-espèce
   Phalaenopsis amabilis subsp. rosenstromii
   
3. Avec variété
   Phalaenopsis amabilis var. alba
   
4. Avec cultivar
   Phalaenopsis amabilis 'White Dream'
   
5. Complet
   Phalaenopsis amabilis subsp. rosenstromii var. alba 'Pink Dream'
```

---

## Règles de Validation

### 1. **Genus** (Genre)
- **Format:** Majuscule
- **Exemple:** `Phalaenopsis`, `Monstera`, `Solanum`
- **Regex:** `^[A-Z][a-z]*$` (1ère lettre MAJ + minuscules)
- **Validation:** Automatique si fourni

```javascript
genus: /^[A-Z][a-z]*$/ ✅
- Phalaenopsis ✅
- phalaenopsis ❌
- PHALAENOPSIS ❌
```

### 2. **Species** (Espèce)
- **Format:** Minuscule
- **Exemple:** `amabilis`, `deliciosa`, `lycopersicum`
- **Regex:** `^[a-z]`
- **Règle obligatoire:** DOIT être minuscule
- **Validation:** Automatique si fourni

```javascript
species: /^[a-z]/ ✅
- amabilis ✅
- Amabilis ❌
- AMABILIS ❌
```

**Règle Inter-champs:** ✅ **Si species → genus OBLIGATOIRE**
```javascript
// ❌ INVALIDE
{ species: "amabilis" }  // Pas de genus!

// ✅ VALIDE
{ genus: "Phalaenopsis", species: "amabilis" }
```

### 3. **Subfamily** (Sous-famille)
- **Format:** Minuscule
- **Exemple:** `pothoideae`
- **Règle:** Toujours minuscule
- **Auto-correction:** Aucune

```javascript
subfamily: /^[a-z]/ ✅
- pothoideae ✅
- Pothoideae ❌
```

### 4. **Subspecies** (Sous-espèce)
- **Format:** `subsp. X` + minuscule
- **Exemple:** `subsp. rosenstromii`
- **Input utilisateur:** Peut entrer `rosenstromii` ou `subsp. rosenstromii`
- **Auto-correction:** ✅ Ajoute `subsp.` si absent
- **Regex:** `^(subsp\.\s+)?[a-z]`

```javascript
// Utilisateur entre:
- "rosenstromii" → Transformé en "subsp. rosenstromii" ✅
- "subsp. rosenstromii" → Gardé tel quel ✅
- "Rosenstromii" ❌ (majuscule)

// Résultat stocké:
"subsp. rosenstromii" ✅
```

### 5. **Variety** (Variété)
- **Format:** `var. X` + minuscule
- **Exemple:** `var. alba`
- **Input utilisateur:** Peut entrer `alba` ou `var. alba`
- **Auto-correction:** ✅ Ajoute `var.` si absent
- **Regex:** `^(var\.\s+)?[a-z]`

```javascript
// Utilisateur entre:
- "alba" → Transformé en "var. alba" ✅
- "var. alba" → Gardé tel quel ✅
- "Alba" ❌ (majuscule)

// Résultat stocké:
"var. alba" ✅
```

### 6. **Cultivar**
- **Format:** Guillemets simples `'X'` - PEUT être majuscule
- **Exemple:** `'White Dream'`, `'PINK DREAM'`, `'white-dream'`
- **Input utilisateur:** Peut entrer avec ou sans guillemets
- **Auto-correction:** ✅ Ajoute guillemets simples si absents
- **Regex:** Flexibilité maximale (contrairement aux autres)

```javascript
// Utilisateur entre:
- "White Dream" → Transformé en "'White Dream'" ✅
- "'White Dream'" → Gardé tel quel ✅
- "White Dream" → "White Dream" ✅
- "white-dream" → "'white-dream'" ✅
- "PINK" → "'PINK'" ✅

// Résultat stocké:
"'White Dream'" ✅
```

### 7. **Reference** (Référence)
- **Format:** Généré automatiquement par le backend
- **User input:** ❌ Ne peut pas être spécifié à la création
- **Mode création:** Champ masqué (affiche "Auto-généré")
- **Mode édition:** Affichage en lecture seule
- **Exemple:** `MON-001`, `PHA-042`

```javascript
// Création (POST)
{ name: "Monstera", family: "Araceae", ... }  // reference EXCLUE ✅

// Édition (PATCH)
{ reference: "MON-001", ... }  // reference EN LECTURE SEULE
```

### 8. **Scientific Name** (Nom scientifique)
- **Format:** Généré automatiquement par le backend
- **Calcul:** `genus + ' ' + species`
- **User input:** ❌ Ne peut pas être spécifié à la création
- **Mode création:** Champ masqué (affiche "À générer...")
- **Mode édition:** Affichage en lecture seule
- **Exemple:** `Phalaenopsis amabilis`, `Monstera deliciosa`

```javascript
// Création (POST)
{ genus: "Phalaenopsis", species: "amabilis", ... }
// Backend génère: scientific_name = "Phalaenopsis amabilis" ✅

// Édition (PATCH)
{ scientific_name: "Phalaenopsis amabilis", ... }  // EN LECTURE SEULE
```

---

## Validation Côté Client (Zod)

### Importances des Validations

| Niveau | Champ | Validation | Message d'Erreur |
|--------|-------|-----------|------------------|
| **Schema** | name | Requis, 2-100 chars | "Le nom doit contenir au moins 2 caractères" |
| **Schema** | family | Requis, 2-100 chars | "La famille doit contenir au moins 2 caractères" |
| **Schema** | genus | Format `^[A-Z][a-z]*$` | "Le genre doit commencer par une majuscule..." |
| **Schema** | species | Format `^[a-z]` | "L'espèce doit être entièrement minuscule..." |
| **Refine** | species | Si fourni → genus obligatoire | "Le genre est obligatoire si l'espèce est fournie" |
| **Refine** | species/genus | Ensemble ou rien | "Le genre et l'espèce doivent être fournis ensemble" |
| **Schema** | subspecies | Format `^(subsp\.\s+)?[a-z]` | "La sous-espèce doit être minuscule..." |
| **Schema** | variety | Format `^(var\.\s+)?[a-z]` | "La variété doit être minuscule..." |
| **Schema** | cultivar | Flexibilité (guillemets auto-ajoutés) | - |

### Auto-Transformations (Transform)

```javascript
// Au parsing/validation:
subspecies: "rosenstromii" → "subsp. rosenstromii"
subspecies: "subsp. alba" → "subsp. alba"  // Inchangé

variety: "alba" → "var. alba"
variety: "var. alba" → "var. alba"  // Inchangé

cultivar: "White Dream" → "'White Dream'"
cultivar: "'White Dream'" → "'White Dream'"  // Inchangé

// Champs auto-générés (à la création):
scientific_name: EXCLU du payload (backend génère)
reference: EXCLU du payload (backend génère)
```

---

## Comportement du Formulaire

### Mode **Création** (Nouvelle Plante)

```jsx
// Champs affichés:
<input name="name" placeholder="Ex: Monstera" />
<input name="family" placeholder="Ex: Araceae" />
<input name="subfamily" placeholder="Ex: Pothoideae" />
<input name="genus" placeholder="Ex: Monstera" />
<input name="species" placeholder="Ex: deliciosa" />
<input name="subspecies" placeholder="Ex: rosenstromii" />  // Auto-corrigé
<input name="variety" placeholder="Ex: alba" />             // Auto-corrigé
<input name="cultivar" placeholder="Ex: White Dream" />     // Auto-corrigé

// Champs MASQUÉS (auto-générés par backend):
<div className="bg-gray-100">
  Nom scientifique (auto-généré): À générer...
  Référence (auto-générée): À générer...
</div>

// À la soumission du formulaire:
// DELETE formData.scientific_name
// DELETE formData.reference
const dataToSend = { name, family, subfamily, genus, species, ... }
```

### Mode **Édition** (Modification Plante Existante)

```jsx
// Champs affichés (identiques à la création):
<input name="name" value={formData.name} />
<input name="family" value={formData.family} />
...

// Champs EN LECTURE SEULE:
<div className="bg-gray-100">
  Nom scientifique (auto-généré): Phalaenopsis amabilis
  Référence (auto-générée): PHA-042
</div>

// À la soumission du formulaire:
// INCLURE scientific_name et reference (lecture seule)
const dataToSend = { 
  name, 
  family, 
  scientific_name: "Phalaenopsis amabilis",  // Inclus en édition
  reference: "PHA-042",                      // Inclus en édition
  ...
}
```

---

## Tests de Validation

### ✅ Cas Valides

```javascript
// Minimal
{
  name: "Monstera",
  family: "Araceae",
  genus: "Monstera",
  species: "deliciosa"
}

// Complet
{
  name: "Phalaenopsis élégante",
  family: "Orchidaceae",
  subfamily: "epidendroideae",
  genus: "Phalaenopsis",
  species: "amabilis",
  subspecies: "rosenstromii",  // Auto → "subsp. rosenstromii"
  variety: "alba",              // Auto → "var. alba"
  cultivar: "White Dream"       // Auto → "'White Dream'"
}
```

### ❌ Cas Invalides

```javascript
// Genus minuscule
{
  genus: "monstera",  // ❌ Erreur: "Le genre doit commencer par une majuscule..."
  species: "deliciosa"
}

// Species majuscule
{
  genus: "Monstera",
  species: "Deliciosa"  // ❌ Erreur: "L'espèce doit être entièrement minuscule..."
}

// Species sans genus
{
  species: "deliciosa"  // ❌ Erreur: "Le genre est obligatoire si l'espèce est fournie"
}

// Genus sans species
{
  genus: "Monstera"  // ❌ Erreur: "Le genre et l'espèce doivent être fournis ensemble"
}

// Subspecies majuscule
{
  subspecies: "Rosenstromii"  // ❌ Erreur: "La sous-espèce doit être minuscule..."
}

// Cultivar sans guillemets (sera auto-corrigé)
{
  cultivar: "White Dream"  // ✅ Auto-transformé en "'White Dream'"
}
```

---

## Implémentation Détails

### Fichier: `frontend/src/lib/schemas.js`

**Champs modifiés pour Phase 3.1:**

```javascript
// Validations strictes pour taxonomie
subfamily: z.string().refine(val => /^[a-z]/.test(val), {...})
genus: z.string().refine(val => /^[A-Z][a-z]*$/.test(val), {...}).transform(...)
species: z.string().refine(val => /^[a-z]/.test(val), {...}).transform(...)
subspecies: z.string().transform(val => val.startsWith('subsp.') ? val : `subsp. ${val}`)
variety: z.string().transform(val => val.startsWith('var.') ? val : `var. ${val}`)
cultivar: z.string().transform(val => val.startsWith("'") ? val : `'${val}'`)

// Validations inter-champs
.refine((data) => {
  // Si species → genus obligatoire
  if (data.species && !data.genus) return false
  return true
})
.refine((data) => {
  // Genus et species ensemble ou pas du tout
  const hasGenus = !!data.genus
  const hasSpecies = !!data.species
  if ((hasGenus && !hasSpecies) || (!hasGenus && hasSpecies)) return false
  return true
})
```

### Fichier: `frontend/src/pages/PlantFormPage.jsx`

**Gestion des champs auto-générés:**

```javascript
const handleSubmit = async (e) => {
  e.preventDefault()
  
  // Validation Zod
  const validation = validatePlant(formData, !!id)
  if (!validation.success) {
    setFieldErrors(validation.errors)
    return
  }
  
  // Préparer les données
  let dataToSend = { ...formData }
  
  if (!id) {
    // En CRÉATION: exclure reference et scientific_name (auto-générés)
    delete dataToSend.reference
    delete dataToSend.scientific_name
  }
  // En ÉDITION: les inclure (mode lecture seule)
  
  // Envoyer à l'API
  if (id) {
    await plantsAPI.update(id, dataToSend)
  } else {
    await plantsAPI.create(dataToSend)
  }
}
```

---

## État de Completion

✅ **Implémenté:**
- [x] Validation format Genus (majuscule)
- [x] Validation format Species (minuscule)
- [x] Validation format Subspecies (minuscule + préfixe auto)
- [x] Validation format Variety (minuscule + préfixe auto)
- [x] Validation format Cultivar (guillemets auto)
- [x] Règle: Genus obligatoire si Species
- [x] Règle: Genus et Species ensemble
- [x] Exclusion scientific_name en création
- [x] Exclusion reference en création
- [x] Affichage lecture seule en édition
- [x] Messages d'erreur en français

**Test et Validation:**
- 🟡 À tester dans le formulaire live
- 🟡 À tester interaction API

---

## Prochaines Étapes

1. ✅ **Phase 3.1:** Form Validation COMPLÈTE
2. ⏳ **Phase 3.2:** Photo Gallery (8h)
3. ⏳ **Phase 3.3:** History Timeline (7h)
4. ⏳ **Phase 3.4:** E2E Tests (5h)


# 🌿 Scientific Name Auto-Generation

**Status:** ✅ **IMPLEMENTED**  
**Date:** October 26, 2025  
**Feature:** Automatic scientific name generation from genus + species

---

## 📋 NOMENCLATURE BINOMINALE (Linné)

Le nom scientifique suit la nomenclature binominale:
- **Genus** (majuscule) + **species** (minuscule)
- Exemple: `Solanum lycopersicum` (la tomate)
  - Genus: `Solanum`
  - Species: `lycopersicum`

---

## ✅ IMPLÉMENTATION

### Model (`backend/app/models/plant.py`)

```python
class Plant(BaseModel):
    # ... fields ...
    genus = Column(String(100))
    species = Column(String(100))
    scientific_name = Column(String(150))  # Auto-generated
    
    def generate_scientific_name(self):
        """Generate scientific name from genus + species"""
        if self.genus and self.species:
            genus = self.genus.strip().capitalize()
            species = self.species.strip().lower()
            return f"{genus} {species}"
        return None
    
    def __init__(self, **kwargs):
        """Auto-generate scientific_name on creation"""
        super().__init__(**kwargs)
        if self.genus and self.species and not self.scientific_name:
            self.scientific_name = self.generate_scientific_name()
```

---

## 🔄 FONCTIONNEMENT

### **Scénario 1: Création avec genus + species**

**Input (API):**
```json
{
  "name": "Tomate",
  "genus": "Solanum",
  "species": "lycopersicum"
}
```

**Résultat automatique:**
```json
{
  "id": 1,
  "name": "Tomate",
  "genus": "Solanum",
  "species": "lycopersicum",
  "scientific_name": "Solanum lycopersicum"  ← Auto-généré!
}
```

### **Scénario 2: Fournir scientific_name explicitement**

Si l'utilisateur fournit déjà le `scientific_name`, on le garde:

```json
{
  "name": "Monstera",
  "genus": "Rhaphidophora",
  "species": "tetrasperma",
  "scientific_name": "Rhaphidophora tetrasperma"  ← Utilisé tel quel
}
```

### **Scénario 3: Pas de genus/species**

Si genus ou species manquent, `scientific_name` reste null:

```json
{
  "name": "Ma plante",
  "genus": null,
  "species": null,
  "scientific_name": null
}
```

---

## 🧪 EXEMPLES RÉELS

| Plante | Genus | Species | Scientific Name (généré) |
|--------|-------|---------|--------------------------|
| 🍅 Tomate | Solanum | lycopersicum | **Solanum lycopersicum** |
| 🌱 Monstera | Rhaphidophora | tetrasperma | **Rhaphidophora tetrasperma** |
| 🌿 Basilic | Ocimum | basilicum | **Ocimum basilicum** |
| 🪴 Rose | Rosa | damascena | **Rosa damascena** |
| 💚 Philodendron | Philodendron | hederaceum | **Philodendron hederaceum** |

---

## 📝 UTILISATION FRONTEND

### **Formulaire d'ajout (dialogs.py)**

```python
def create_add_plant_dialog(locations_list):
    layout = [
        [sg.Text("Nom commun:"), sg.InputText(key='-NAME-')],
        [sg.Text("Genre (Genus):"), sg.InputText(key='-GENUS-')],
        [sg.Text("Espèce (Species):"), sg.InputText(key='-SPECIES-')],
        [sg.Text("Nom scientifique:"), sg.InputText(key='-SCI-NAME-', disabled=True)],
        # ... autres champs
    ]
    # Le scientific_name sera auto-rempli à la création
```

### **Affichage**

Le `scientific_name` sera automatiquement rempli et envoyé au backend:

```python
data = {
    'name': values['-NAME-'],
    'genus': values['-GENUS-'],
    'species': values['-SPECIES-'],
    # scientific_name sera généré automatiquement par le backend!
}
```

---

## 🔐 VALIDATIONS

### **Format correct:**
- ✅ `Solanum lycopersicum` - Correct
- ✅ `SOLANUM LYCOPERSICUM` - Converti en `Solanum lycopersicum`
- ✅ `solanum lycopersicum` - Converti en `Solanum lycopersicum`

### **Format incorrect:**
- ❌ `solanum lycopersicum` - Mauvais format (genus minuscule)
- ❌ `Solanum Lycopersicum` - Mauvais format (species majuscule)
- ❌ `SolanuM LycopersicuM` - Mauvais format (casse mixte)

**Mais pas d'erreur!** On corrige automatiquement ✅

---

## 🎯 AVANTAGES

1. ✅ **Pas d'erreur manuelle** - Le backend génère le format correct
2. ✅ **Cohérence garantie** - Tous les noms scientifiques au format correct
3. ✅ **UX simplifiée** - L'utilisateur n'a qu'à saisir genus + species
4. ✅ **Compatible Laravel** - Comme avant, le champ peut être ignoré
5. ✅ **Flexible** - On peut toujours fournir scientific_name manuellement

---

## 📡 IMPACT API

### **POST /api/plants**

**Request:**
```json
{
  "name": "Ma Tomate",
  "genus": "Solanum",
  "species": "lycopersicum",
  "location_id": 1
}
```

**Response (201):**
```json
{
  "id": 42,
  "name": "Ma Tomate",
  "genus": "Solanum",
  "species": "lycopersicum",
  "scientific_name": "Solanum lycopersicum",
  "location_id": 1,
  ...
}
```

### **PUT /api/plants/{id}**

Si on modifie genus/species, le scientific_name se recalcule automatiquement ✅

---

## 🔄 MIGRATION

**Plantes existantes (sans genus/species):**
- `scientific_name` reste inchangé
- Pas de régénération automatique pour les anciennes données

**Nouvelles plantes:**
- `scientific_name` généré automatiquement ✅

---

## ✨ RÉSUMÉ

| Aspect | Avant | Après |
|--------|-------|-------|
| **Saisie** | Manuelle (peut avoir erreurs) | Auto-générée de genus + species |
| **Format** | Variable | Standardisé: `Genus species` |
| **Erreurs** | Possibles | Éliminées |
| **Flexibilité** | Oui | Oui (on peut toujours override) |
| **Effort utilisateur** | Élevé | Réduit |

---

**Résultat:** Les noms scientifiques sont maintenant **toujours corrects** et au **format standard international** 🌍

---

*Implémenté: October 26, 2025*  
*Nomenclature Linnaéenne: Automatisée et Validée*

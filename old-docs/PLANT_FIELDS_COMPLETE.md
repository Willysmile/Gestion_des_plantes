# 🌱 COMPLET DES CHAMPS PLANTE

**Date:** 26 octobre 2025  
**Statut:** Documentation complète de tous les champs disponibles

---

## 📊 RÉSUMÉ

| Catégorie | Total | Éditables | Visibles | Non Exposés |
|-----------|-------|-----------|----------|-------------|
| **Taxonomie** | 7 | 5 | 7 | 0 |
| **Description** | 4 | 4 | 4 | 0 |
| **Localisation** | 3 | 3 | 3 | 0 |
| **Achat** | 3 | 3 | 2 | 1 |
| **Environnement** | 9 | 9 | 0 | 9 |
| **Maintenance** | 5 | 0 | 3 | 2 |
| **Métadonnées** | 4 | 1 | 2 | 2 |
| **TOTAL** | **35** | **25** | **21** | **14** |

---

## 📚 DÉTAIL COMPLET PAR CATÉGORIE

### 🔬 TAXONOMIE (7 champs)

**Importance:** ⭐⭐⭐⭐⭐ Fondamentale pour identifier la plante

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 1 | `family` | String(100) | ✅ **OUI** | ✅ OUI | Famille botanique (ex: Solanaceae) |
| 2 | `subfamily` | String(100) | ✅ **OUI** | ✅ OUI | Sous-famille botanique |
| 3 | `genus` | String(100) | ✅ **OUI** | ✅ OUI | Genre 🔬 **UTILISÉ pour auto-générer scientific_name** |
| 4 | `species` | String(100) | ✅ **OUI** | ✅ OUI | Espèce 🔬 **UTILISÉ pour auto-générer scientific_name** |
| 5 | `subspecies` | String(100) | ✅ **OUI** | ✅ OUI | Sous-espèce (optionnel) |
| 6 | `variety` | String(100) | ✅ **OUI** | ✅ OUI | Variété cultivée (ex: "Beefsteak") |
| 7 | `cultivar` | String(100) | ✅ **OUI** | ✅ OUI | Cultivar spécifique |

**Auto-génération:**
```
genus = "Solanum" (capitalisé)
species = "lycopersicum" (minuscule)
↓
scientific_name = "Solanum lycopersicum" 🔬
```

---

### 📝 DESCRIPTION (4 champs)

**Importance:** ⭐⭐⭐⭐ Informations générales sur la plante

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 8 | `description` | Text | ✅ **OUI** | ✅ OUI | Description libre, caractéristiques, utilisation |
| 9 | `reference` | String(255) | ✅ **OUI** | ✅ OUI | Identifiant unique pour recherches (ISBN, URL, code) |
| 10 | `flowering_season` | String(50) | ✅ **OUI** | ✅ OUI | Saison de floraison (ex: "Printemps-Été") |
| 11 | `scientific_name` | String(255) | ✅ OUI (manuel) | ✅ OUI | **AUTO-GÉNÉRÉ** de genus + species (peut être overridé) |

**Exemple:**
```
description = "Tomate productive, excellente pour salades, goût sucré"
reference = "ISBN:978-2-01-234567-8"
flowering_season = "Mai-Septembre"
scientific_name = "Solanum lycopersicum" (auto-généré)
```

---

### 📍 LOCALISATION (3 champs)

**Importance:** ⭐⭐⭐⭐ Gestion physique de la plante

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 12 | `location_id` | FK (Locations) | ✅ **OUI** (dropdown) | ✅ OUI | Emplacement actuel (ex: "Salon", "Cuisine", "Balcon") |
| 13 | `purchase_place_id` | FK (Places) | ✅ **OUI** (dropdown) | ✅ OUI | Où a été achetée (ex: "Pépinière A", "Marché", "Amazon") |
| 14 | `purchase_date` | Date | ✅ **OUI** | ✅ OUI | Date d'achat (détermine l'âge de la plante) |

**Exemple:**
```
location_id = 5 ("Balcon Nord")
purchase_place_id = 12 ("Pépinière Le Vert")
purchase_date = "2025-10-01"
```

---

### 🛒 ACHAT (3 champs)

**Importance:** ⭐⭐⭐ Information historique et budgétaire

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 15 | `purchase_price` | Decimal(10,2) | ✅ **OUI** | ❌ NON | Prix d'achat en € |
| 16 | `price_category` | Enum | ✅ **OUI** | ✅ OUI | Catégorie prix (budget/standard/premium) |
| 17 | `is_favorite` | Boolean | ✅ **OUI** | ✅ OUI | Plante favorite ⭐ |

**Exemple:**
```
purchase_price = 15.99
price_category = "standard"
is_favorite = true
```

---

### 🌡️ ENVIRONNEMENT (9 champs) ⚠️ NON EXPOSÉS ACTUELLEMENT

**Importance:** ⭐⭐⭐⭐⭐ Critique pour les soins corrects

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 18 | `temperature_min` | Float | ✅ **À AJOUTER** | ❌ NON | Température minimale en °C |
| 19 | `temperature_max` | Float | ✅ **À AJOUTER** | ❌ NON | Température maximale en °C |
| 20 | `humidity_level` | Float (0-100) | ✅ **À AJOUTER** | ❌ NON | Taux d'humidité idéal en % |
| 21 | `soil_humidity` | Enum | ✅ **À AJOUTER** | ❌ NON | Humidité du sol (sec/modéré/humide) |
| 22 | `soil_type` | String(100) | ✅ **À AJOUTER** | ❌ NON | Type de sol (terreau, argile, sable, etc.) |
| 23 | `soil_ideal_ph` | Float (0-14) | ✅ **À AJOUTER** | ❌ NON | pH idéal du sol |
| 24 | `pot_size` | String(50) | ✅ **À AJOUTER** | ❌ NON | Taille de pot recommandée (ex: "20cm") |
| 25 | `growth_speed` | Enum | ✅ **À AJOUTER** | ❌ NON | Vitesse de croissance (lent/normal/rapide) |
| 26 | `max_height` | Float | ✅ **À AJOUTER** | ❌ NON | Hauteur maximale en cm |

**Exemple:**
```
temperature_min = 15.0
temperature_max = 28.0
humidity_level = 65.0
soil_humidity = "modéré"
soil_type = "terreau universel"
soil_ideal_ph = 6.5
pot_size = "20cm"
growth_speed = "normal"
max_height = 180.0
```

---

### 🔄 MAINTENANCE (5 champs)

**Importance:** ⭐⭐⭐⭐ Historique des soins

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 27 | `watering_frequency_id` | FK (Frequencies) | ✅ **OUI** (dropdown) | ✅ OUI | Fréquence arrosage (tous les 3j, 1x/semaine, etc.) |
| 28 | `last_watering_date` | DateTime | ❌ NON | ✅ OUI | Dernière date d'arrosage (auto-updaté) |
| 29 | `light_requirement_id` | FK (Light) | ✅ **OUI** (dropdown) | ✅ OUI | Besoin lumière (faible/modéré/élevé/direct) |
| 30 | `fertilizing_frequency` | Enum | ✅ **À AJOUTER** | ❌ NON | Fréquence d'engrais (tous les 14j, mensuel, etc.) |
| 31 | `last_fertilizing_date` | DateTime | ❌ NON | ✅ OUI | Dernière date d'engrais (auto-updaté) |

**Exemple:**
```
watering_frequency_id = 3 ("Tous les 3 jours")
last_watering_date = "2025-10-25 14:30:00"
light_requirement_id = 2 ("Lumière modérée")
fertilizing_frequency = "monthly"
last_fertilizing_date = "2025-10-01 10:00:00"
```

---

### ⚙️ MÉTADONNÉES (4 champs)

**Importance:** ⭐⭐ Système et état

| # | Champ | Type | Éditable | Visible | Description |
|---|-------|------|----------|---------|-------------|
| 32 | `is_indoor` | Boolean | ✅ **OUI** | ✅ OUI | Peut vivre à l'intérieur |
| 33 | `is_outdoor` | Boolean | ✅ **OUI** | ✅ OUI | Peut vivre à l'extérieur |
| 34 | `is_toxic` | Boolean | ✅ **OUI** | ✅ OUI | Toxique pour animaux/enfants ⚠️ |
| 35 | `is_archived` | Boolean | ✅ **OUI** | ✅ OUI | Plante archivée (mortes, vendues) |

**Exemple:**
```
is_indoor = true
is_outdoor = true
is_toxic = false
is_archived = false
```

---

## 📊 RÉSUMÉ CHAMPS ÉDITABLE

### ✅ ACTUELLEMENT DANS LE FORMULAIRE (5 champs)
```
1. name              ← Nom simple
2. scientific_name   ← AUTO-GÉNÉRÉ
3. location          ← dropdown
4. difficulty        ← dropdown
5. health_status     ← dropdown
```

### ➕ À AJOUTER AU FORMULAIRE (20+ champs)

**Phase 1 - Taxonomie Complète (6 champs):**
- family, subfamily, genus, species, subspecies, variety, cultivar

**Phase 2 - Description (3 champs):**
- description, reference, flowering_season

**Phase 3 - Achat (3 champs):**
- purchase_date, purchase_place, purchase_price

**Phase 4 - Environnement (9 champs) ⚠️ IMPORTANT:**
- temperature_min, temperature_max, humidity_level
- soil_humidity, soil_type, soil_ideal_ph
- pot_size, growth_speed, max_height

**Phase 5 - Maintenance (2 champs):**
- watering_frequency, light_requirement, fertilizing_frequency

**Phase 6 - Métadonnées (4 champs):**
- is_indoor, is_outdoor, is_toxic, is_favorite

---

## 🎯 PROPOSITIONS D'INTERFACE

### Option 1: Accordéon Collapsible (Recommandé)
```
Formulaire Add/Edit Plant
├── 📌 INFORMATIONS BASIQUES (expanded)
│   ├─ Name
│   ├─ Scientific Name (auto-gen)
│   └─ Favorite ⭐
├── 🔬 TAXONOMIE (collapsed)
│   ├─ Family
│   ├─ Subfamily
│   ├─ Genus
│   ├─ Species
│   ├─ Subspecies
│   ├─ Variety
│   └─ Cultivar
├── 📝 DESCRIPTION (collapsed)
│   ├─ Description
│   ├─ Reference
│   └─ Flowering Season
├── 🛒 ACHAT (collapsed)
│   ├─ Purchase Date
│   ├─ Purchase Place
│   └─ Price
├── 📍 LOCALISATION (expanded)
│   ├─ Current Location
│   ├─ Light Requirement
│   ├─ Watering Frequency
│   └─ Difficulty
├── 🌡️ ENVIRONNEMENT (collapsed)
│   ├─ Temperature Min
│   ├─ Temperature Max
│   ├─ Humidity Level
│   ├─ Soil Humidity
│   ├─ Soil Type
│   ├─ Soil pH
│   ├─ Pot Size
│   ├─ Growth Speed
│   └─ Max Height
└── ⚙️ MÉTADONNÉES (collapsed)
    ├─ Indoor
    ├─ Outdoor
    ├─ Toxic ⚠️
    └─ Archived
```

### Option 2: Onglets Multiples
```
Add/Edit Plant
├── Tab 1: Basic Info (Name, Scientific, Favorite)
├── Tab 2: Taxonomy (Family, Genus, Species, etc.)
├── Tab 3: Description & Purchase
├── Tab 4: Environment (Temperature, Humidity, Soil)
├── Tab 5: Location & Maintenance
└── Tab 6: Metadata
```

### Option 3: Deux Niveaux (Recommandé - Équilibre)
```
Simple Form (Toujours visible)
├─ Name
├─ Scientific Name
├─ Location
├─ Difficulty
├─ Health Status

Advanced Form (Click "⚙️ Advanced")
├─ Taxonomie complète
├─ Description
├─ Environnement
├─ Achat
└─ Métadonnées
```

---

## 🔧 PROCHAINES ÉTAPES

**Phase IMMÉDIATE:**
1. ✅ Documenter tous les champs (CE FICHIER)
2. ⏳ Modifier `dialogs.py` pour ajouter les champs
3. ⏳ Tester les nouveaux formulaires
4. ⏳ Commit les changements

**Phase OPTIONNELLE:**
- Ajouter validation de types
- Ajouter tooltips d'aide
- Ajouter valeurs par défaut
- Implémenter photos/pièces jointes
- Implémenter historique complet (watering log, fertilizing log, repotting log)

---

## 📋 CHECKLIST DÉPLOIEMENT

- [ ] Tous les champs documentés ✅
- [ ] Interface définie (accordéon vs onglets vs deux niveaux)
- [ ] dialogs.py modifié avec tous les champs
- [ ] Validation des entrées ajoutée
- [ ] Test unitaire des champs
- [ ] Test d'intégration avec API
- [ ] Documentation utilisateur
- [ ] Commit et merge

---

*Généré: 26 octobre 2025*  
*Statut: Documentation Complète ✅*

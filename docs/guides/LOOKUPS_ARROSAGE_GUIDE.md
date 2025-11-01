# 📋 Lookups d'Arrosage - Guide Complet

## 🔍 Où les Trouver

### Backend
Les lookups sont disponibles via ces endpoints API:

```
GET http://localhost:8000/api/lookups/watering-methods
GET http://localhost:8000/api/lookups/water-types
GET http://localhost:8000/api/lookups/seasons
```

### Base de Données
Les données sont stockées dans 3 tables SQLite:
- `watering_methods` - Méthodes d'arrosage
- `water_types` - Types d'eau
- `seasons` - Saisons

### Frontend
Code source:
- **API Client**: `/frontend/src/lib/api.js` - Méthodes lookupsAPI
- **Config**: `/frontend/src/config.js` - Endpoints mappés
- **Service**: `/frontend/src/pages/PlantFormPage.jsx` - Chargement des lookups

---

## 📦 Les 3 Lookups Disponibles

### 1️⃣ WATERING METHODS (Méthodes d'arrosage)
**Endpoint**: `GET /api/lookups/watering-methods`

```json
[
  { "id": 1, "name": "Par le dessus", "description": "Verser directement sur le sol" },
  { "id": 2, "name": "Par le dessous", "description": "Tremper le pot dans un bac d'eau" },
  { "id": 3, "name": "Par brumisation", "description": "Vaporiser sur les feuilles" },
  { "id": 4, "name": "Goutte à goutte", "description": "Arrosage automatique lent et régulier" },
  { "id": 5, "name": "Immersion", "description": "Immerger le pot quelques minutes" }
]
```

**Utilisation**: Indiquer la méthode préférée pour arroser une plante (ex: "Par brumisation" pour les fougères)

---

### 2️⃣ WATER TYPES (Types d'eau)
**Endpoint**: `GET /api/lookups/water-types`

```json
[
  { "id": 1, "name": "Pluie", "description": "Eau de pluie (idéale)" },
  { "id": 2, "name": "Robinet reposée", "description": "Eau du robinet reposée 24h minimum" },
  { "id": 3, "name": "Filtrée", "description": "Eau filtrée (meilleure qualité)" },
  { "id": 4, "name": "Distillée", "description": "Eau distillée (pour plantes sensibles)" }
]
```

**Utilisation**: Sélectionner le type d'eau à utiliser pour arroser (ex: "Eau de pluie" pour les plantes sensibles)

---

### 3️⃣ SEASONS (Saisons)
**Endpoint**: `GET /api/lookups/seasons`

```json
[
  { "id": 1, "name": "Printemps", "start_month": 3, "end_month": 5, "description": "Croissance active, plus d'eau" },
  { "id": 2, "name": "Été", "start_month": 6, "end_month": 8, "description": "Croissance active, maximum d'eau" },
  { "id": 3, "name": "Automne", "start_month": 9, "end_month": 11, "description": "Repos végétatif, moins d'eau" },
  { "id": 4, "name": "Hiver", "start_month": 12, "end_month": 2, "description": "Repos végétatif, minimum d'eau" }
]
```

**Utilisation**: Adapter la fréquence d'arrosage selon la saison (ex: 7 jours en été, 14 jours en hiver)

---

## 🛠️ Comment Les Utiliser au Frontend

### 1. Charger les Lookups (déjà fait dans PlantFormPage)

```javascript
// Dans frontend/src/pages/PlantFormPage.jsx
useEffect(() => {
  const loadLookups = async () => {
    const [methods, types, seasons] = await Promise.all([
      lookupsAPI.getWateringMethods(),
      lookupsAPI.getWaterTypes(),
      lookupsAPI.getSeasons(),
    ])
    setLookups({
      wateringMethods: methods.data || [],
      waterTypes: types.data || [],
      seasons: seasons.data || [],
    })
  }
  loadLookups()
}, [])
```

### 2. Afficher dans un Dropdown

```jsx
// Exemple: Sélectionner une méthode d'arrosage
<select>
  <option value="">-- Choisir --</option>
  {lookups.wateringMethods.map(method => (
    <option key={method.id} value={method.id}>
      {method.name}
    </option>
  ))}
</select>
```

### 3. Récupérer les Données via API

```javascript
// Dans n'importe quel composant
import { lookupsAPI } from '../lib/api'

// Charger une seule fois
const methods = await lookupsAPI.getWateringMethods()
const types = await lookupsAPI.getWaterTypes()
const seasons = await lookupsAPI.getSeasons()
```

### 4. Accéder via config.js

```javascript
import { API_ENDPOINTS } from '../config'

// Les endpoints sont mappés comme:
API_ENDPOINTS.LOOKUPS.WATERING_METHODS  // '/lookups/watering-methods'
API_ENDPOINTS.LOOKUPS.WATER_TYPES       // '/lookups/water-types'
API_ENDPOINTS.LOOKUPS.SEASONS           // '/lookups/seasons'
```

---

## 🎯 Cas d'Usage

### Cas 1: Formulaire de Création de Plante
Ajouter des champs pour sélectionner:
- Méthode d'arrosage préférée
- Type d'eau à utiliser
- Fréquence d'arrosage par saison

### Cas 2: Historique d'Arrosage
Enregistrer pour chaque arrosage:
- Quelle méthode a été utilisée
- Quel type d'eau a été utilisé
- En quelle saison (pour analyse saisonnière)

### Cas 3: Recommandations Saisonnières
Adapter les rappels d'arrosage:
```
Printemps/Été: Plus d'eau (croissance active)
Automne/Hiver: Moins d'eau (repos végétatif)
```

---

## 📂 Structure des Fichiers

```
Backend:
├── app/models/lookup.py                    # Tables WateringMethod, WaterType, Season
├── app/routes/lookups.py                   # Endpoints /api/lookups/*
├── app/services/settings_service.py        # Méthodes get_watering_methods(), etc.
├── app/scripts/seed_watering_lookups.py    # Données d'initialisation
├── migrations/versions/005_add_watering_*  # Migration

Frontend:
├── src/lib/api.js                          # lookupsAPI.getWateringMethods(), etc.
├── src/config.js                           # API_ENDPOINTS.LOOKUPS.*
├── src/pages/PlantFormPage.jsx             # Chargement et utilisation
```

---

## ✅ Checklist d'Intégration

- [x] Tables de base de données créées
- [x] Endpoints API implémentés
- [x] Données seedées
- [x] Méthodes lookupsAPI ajoutées
- [x] Config.js mise à jour
- [x] PlantFormPage chargent les lookups
- [ ] Afficher les dropdowns dans le formulaire plante
- [ ] Ajouter champs au modèle Plant (preferred_watering_method_id, etc.)
- [ ] Enregistrer dans WateringHistory avec méthode et type d'eau

---

## 🔗 Liens Utiles

- **Migration**: `/backend/migrations/versions/005_add_watering_configuration_tables.py`
- **Seed Data**: `/backend/app/scripts/seed_watering_lookups.py`
- **API Routes**: `/backend/app/routes/lookups.py` (lignes ~180+)
- **Frontend Config**: `/frontend/src/config.js` (ligne ~67-69)
- **Frontend API Client**: `/frontend/src/lib/api.js` (ligne ~190+)

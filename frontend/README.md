# Gestion des Plantes - Frontend

React + Vite + Tailwind CSS frontend pour Gestion des Plantes.

## Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## Project Structure

```
src/
├── components/      # Composants réutilisables
│   └── Layout.jsx  # Layout principal
├── pages/          # Pages
│   ├── DashboardPage.jsx      # Liste des plantes
│   ├── PlantDetailPage.jsx    # Détails d'une plante
│   └── PlantFormPage.jsx      # Create/Edit form
├── hooks/          # Hooks personnalisés
│   └── usePlants.js           # Gestion des plantes
├── lib/            # Utilitaires
│   └── api.js      # Client API
├── App.jsx         # Main app
├── main.jsx        # Entry point
└── index.css       # Tailwind CSS
```

## API Integration

L'app utilise axios pour communiquer avec le backend FastAPI.

Base URL: `http://localhost:8001/api`

### Endpoints utilisés

- `GET /api/plants` - Liste toutes les plantes
- `GET /api/plants/{id}` - Récupère les détails d'une plante
- `POST /api/plants` - Crée une nouvelle plante
- `PUT /api/plants/{id}` - Met à jour une plante
- `DELETE /api/plants/{id}` - Supprime une plante (soft delete)
- `PATCH /api/plants/{id}/archive` - Archive une plante
- `PATCH /api/plants/{id}/restore` - Restaure une plante

### Lookups

- `GET /api/lookups/locations` - Lieux de stockage
- `GET /api/lookups/watering-frequencies` - Fréquences d'arrosage
- `GET /api/lookups/light-requirements` - Besoins en lumière

## Features

### Phase 2 MVP ✅

- [x] Dashboard avec liste des plantes
- [x] Recherche et filtrage par nom/famille
- [x] Voir détails d'une plante
- [x] Créer une nouvelle plante
- [x] Éditer une plante
- [x] Supprimer une plante (soft delete)
- [x] Archiver/Restaurer une plante
- [x] Dropdowns pour lookups

### Phase 3 (Optionnel)

- [ ] Gallery de photos
- [ ] Timeline d'historique
- [ ] Statistiques
- [ ] Paramètres utilisateur
- [ ] Tags et catégories

## Development

### Environment Variables

Créez un `.env.local` si besoin:

```env
VITE_API_URL=http://localhost:8001/api
```

### Styling

- Tailwind CSS pour le style
- Lucide React pour les icônes
- Design system simple et propre

## Testing

Phase 2: Tests manuels via `npm run dev`
Phase 3: Ajouter pytest E2E

## Build & Deploy

```bash
# Build
npm run build

# Output: dist/
```

Later: Intégration Tauri pour packaging desktop.

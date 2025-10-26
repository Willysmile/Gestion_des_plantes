# Phase 2 - Décisions Stratégiques

## 1️⃣ Tauri vs React Dev

**RECOMMANDATION: React dev d'abord, Tauri après**

✅ Avantages:
- Itération rapide (hot reload)
- Debugging plus facile
- Tests avant packaging
- Vite + React = super rapide (dev en 30s)

Plan:
```bash
# Semaine 1: React dev
npm create vite@latest gestion-plantes -- --template react
cd gestion-plantes
npm install

# Tests en dev mode
npm run dev  # http://localhost:5173

# Semaine 2: Intégration Tauri
cd ..
cargo create-tauri-app --template react --typescript
# Copier code React dedans
```

❌ Éviter: Tauri d'emblée = friction, complexité build

---

## 2️⃣ TanStack Query vs useState

**RECOMMANDATION: useState + fetch minimaliste pour MVP**

Analyse:
| Aspect | useState | TanStack Query |
|--------|----------|---|
| Setup time | 5 min | 30 min |
| MVP needs? | ✅ 100% | ❌ 200% |
| Caching | Manual | Auto |
| Refetch | Manual | Auto |
| Error handling | Basic | Pro |
| Size | ~2KB | ~35KB |

**Phase 2 Strategy:**
```javascript
// MVP: Hook simple
useEffect(() => {
  fetch('/api/plants')
    .then(r => r.json())
    .then(setPlants)
}, [])

// Si trop complexe → TanStack Query Phase 3
```

✅ Best of both:
- Start with `useState` + custom hook
- Custom hook = easy to switch to TanStack Query later

---

## 3️⃣ shadcn/ui Components

**RECOMMANDATION: Minimal set MVP**

Installation minimale (5 composants):
```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add select
npx shadcn-ui@latest add dialog
```

Optionnel Phase 3:
- table (pour historiques)
- tabs (plant details)
- badge (status)

Raison: Chaque composant = ~5KB gzipped

---

## 4️⃣ Timeline Phase 2

**RECOMMANDATION: Rapide Prototype 2-3 jours**

### Jour 1 (4h): Setup
- Vite + React + TypeScript ✅
- Tailwind CSS ✅
- shadcn/ui (5 composants) ✅
- API client hook ✅

### Jour 2 (6h): UI Core
- Layout (sidebar, header) ✅
- Plant list page ✅
- Plant create/edit modal ✅
- Basic filtering ✅

### Jour 3 (4h): Integration
- Connect to backend API ✅
- Error handling ✅
- Loading states ✅
- Basic E2E test ✅

**Total: 14 heures de travail = 2 jours solidaires**

---

## 🎯 Phase 2 MVP Feature Set

```
✅ Dashboard
  ├─ List all plants (API: GET /api/plants)
  ├─ Search/filter by family
  └─ Sort by name/date

✅ Plant Management
  ├─ Create plant (API: POST /api/plants)
  ├─ View details (API: GET /api/plants/{id})
  ├─ Edit plant (API: PUT /api/plants/{id})
  ├─ Delete (soft) (API: DELETE /api/plants/{id})
  └─ Archive/Restore (API: PATCH /api/plants/{id}/archive)

✅ Navigation
  ├─ Main dashboard
  ├─ Plant details view
  └─ Create/edit form

❌ Phase 3+
  ├─ Photo gallery
  ├─ History timeline
  ├─ Statistics
  └─ Settings
```

---

## 📦 Stack Final MVP

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0"  // simpler que fetch
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "shadcn-ui": "^0.8.0"
  }
}
```

---

## ✅ DÉCISIONS FINALES

| Question | Réponse | Justification |
|----------|---------|---|
| **Tauri ou React dev?** | React dev d'abord | Itération rapide, test avant build |
| **TanStack Query?** | useState custom hook | MVP simple, upgrade facile |
| **shadcn/ui complets?** | Non, 5 composants | MVP first, extensible |
| **Timeline?** | 2-3 jours | Rapide prototype, phase 3 pour polish |

---

## 🚀 Commandes Démarrage

```bash
# 1. Create Vite React project
npm create vite@latest gestion-plantes -- --template react

# 2. Setup dependencies
cd gestion-plantes
npm install axios react-router-dom

# 3. Add Tailwind + shadcn
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npx shadcn-ui@latest init -y

# 4. Add core components
npx shadcn-ui@latest add button card input select dialog

# 5. Start dev
npm run dev
```

**Prêt?** Lancez-vous ! 🚀

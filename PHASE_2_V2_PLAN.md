# 🎨 PHASE 2 - Frontend Setup (Tauri + React + TypeScript)

**Date**: 26 Oct 2025  
**Branche**: `v2-tauri-react`  
**Objectif**: Créer moderne Tauri desktop app avec React + TypeScript + Tailwind

---

## 📋 Checklist Phase 2

- [ ] 2.1 - Create Tauri + React project
- [ ] 2.2 - Setup TypeScript + Tailwind CSS
- [ ] 2.3 - Install shadcn/ui components
- [ ] 2.4 - Setup TanStack Query (React Query)
- [ ] 2.5 - Create API client (httpx wrapper)
- [ ] 2.6 - Setup Zod validation schemas
- [ ] 2.7 - Create basic layout + navigation
- [ ] 2.8 - Test Tauri build + app launch
- [ ] 2.9 - Setup ESLint + Prettier
- [ ] 2.10 - Commit: "feat: Bootstrap Tauri + React frontend v2"

---

## 🎯 Détails Phase 2

### 2.1 - Create Tauri + React Project

**Command:**
```bash
cd /home/willysmile/Documents/Gestion_des_plantes

# Create Tauri project with React template
npm create tauri-app@latest -- \
  --project-name gestion-plantes \
  --package-name com.example.gestione-plantes \
  --manager npm \
  --template react \
  --typescript

cd frontend
npm install
```

**Result structure:**
```
frontend/
├── src/
│   ├── components/    (React components)
│   ├── pages/         (Page components)
│   ├── hooks/         (Custom hooks)
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/
│   ├── tauri.conf.json
│   └── src/           (Rust backend)
├── package.json
└── tsconfig.json
```

### 2.2 - Setup TypeScript + Tailwind CSS

**Install Tailwind:**
```bash
cd frontend
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Config tailwind.config.js:**
```javascript
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Update src/index.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 2.3 - Install shadcn/ui Components

**Setup shadcn/ui:**
```bash
cd frontend
npx shadcn-ui@latest init

# Select Tailwind + React default options
```

**Install components needed:**
```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add select
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add table
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add spinner
npx shadcn-ui@latest add toast
```

### 2.4 - Setup TanStack Query (React Query)

**Install:**
```bash
cd frontend
npm install @tanstack/react-query
```

**Create `src/hooks/useQuery.ts`:**
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export const useGetPlants = () => {
  return useQuery({
    queryKey: ['plants'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/api/plants');
      return response.json();
    },
  });
};

export const useCreatePlant = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (newPlant) => {
      const response = await fetch('http://localhost:8000/api/plants', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPlant),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plants'] });
    },
  });
};
```

### 2.5 - Create API Client

**Create `src/api/client.ts`:**
```typescript
const API_BASE = 'http://localhost:8000/api';

export const api = {
  // Plants
  plants: {
    getAll: () => fetch(`${API_BASE}/plants`).then(r => r.json()),
    getById: (id: number) => fetch(`${API_BASE}/plants/${id}`).then(r => r.json()),
    create: (plant) => fetch(`${API_BASE}/plants`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(plant),
    }).then(r => r.json()),
    update: (id: number, plant) => fetch(`${API_BASE}/plants/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(plant),
    }).then(r => r.json()),
    delete: (id: number) => fetch(`${API_BASE}/plants/${id}`, {
      method: 'DELETE',
    }).then(r => r.json()),
    archive: (id: number, reason: string) => fetch(`${API_BASE}/plants/${id}/archive`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    }).then(r => r.json()),
    restore: (id: number) => fetch(`${API_BASE}/plants/${id}/restore`, {
      method: 'PATCH',
    }).then(r => r.json()),
  },
  
  // Stats
  stats: {
    getKpis: () => fetch(`${API_BASE}/stats`).then(r => r.json()),
  },
};
```

### 2.6 - Setup Zod Validation

**Install:**
```bash
cd frontend
npm install zod
```

**Create `src/schemas/plant.ts`:**
```typescript
import { z } from 'zod';

export const PlantCreateSchema = z.object({
  name: z.string().min(1, 'Name required'),
  family: z.string().optional(),
  scientific_name: z.string().optional(),
  temperature_min: z.number().optional(),
  temperature_max: z.number().optional(),
  // ... other fields
}).refine(
  (data) => !data.temperature_min || !data.temperature_max || 
    data.temperature_min < data.temperature_max,
  {
    message: "temperature_min must be < temperature_max",
    path: ["temperature_min"],
  }
);

export type PlantCreate = z.infer<typeof PlantCreateSchema>;
```

### 2.7 - Create Basic Layout

**Create `src/App.tsx`:**
```typescript
import { useGetPlants } from './hooks/useQuery';
import PlantsList from './pages/PlantsList';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';

export default function App() {
  const [activeTab, setActiveTab] = React.useState('plants');

  return (
    <div className="h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="flex gap-4 p-4">
          <button onClick={() => setActiveTab('plants')} 
                  className={activeTab === 'plants' ? 'font-bold' : ''}>
            🌱 Plants
          </button>
          <button onClick={() => setActiveTab('dashboard')} 
                  className={activeTab === 'dashboard' ? 'font-bold' : ''}>
            📊 Dashboard
          </button>
          <button onClick={() => setActiveTab('settings')} 
                  className={activeTab === 'settings' ? 'font-bold' : ''}>
            ⚙️ Settings
          </button>
        </div>
      </nav>

      <main className="p-4">
        {activeTab === 'plants' && <PlantsList />}
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'settings' && <Settings />}
      </main>
    </div>
  );
}
```

### 2.8 - Test Tauri Build + Launch

**Development:**
```bash
cd frontend
npm run tauri dev
```

**Build:**
```bash
npm run tauri build
```

**Result:** Desktop app window with React running inside Tauri!

### 2.9 - Setup ESLint + Prettier

**Install:**
```bash
cd frontend
npm install --save-dev eslint prettier eslint-config-prettier
```

**Create `.eslintrc.json`:**
```json
{
  "extends": ["react-app", "prettier"]
}
```

**Create `.prettierrc.json`:**
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### 2.10 - Commit

```bash
git add frontend/
git commit -m "feat: Bootstrap Tauri + React frontend v2

- Initialize Tauri project with React + TypeScript
- Setup Tailwind CSS + shadcn/ui components
- Setup TanStack Query for data fetching
- Create API client for backend communication
- Setup Zod validation schemas
- Create basic layout with tab navigation
- Configure ESLint + Prettier
- Ready for phase 3 (UI components implementation)"
```

---

## 📊 Tech Stack Summary

| Tech | Purpose |
|------|---------|
| **Tauri** | Desktop app framework (lightweight, secure) |
| **React** | UI framework |
| **TypeScript** | Type safety |
| **Tailwind** | Styling |
| **shadcn/ui** | Pre-built components |
| **TanStack Query** | Data fetching + caching |
| **Zod** | Client-side validation |
| **Vite** | Build tool (fast) |

---

## 🔗 Integration Points (Phase 3)

- ✅ Connect to Phase 1 backend (http://localhost:8000)
- ✅ Create PlantsList page with card view
- ✅ Create add/edit/delete dialogs
- ✅ Create Dashboard page with KPIs
- ✅ Create Settings page with theme selector

---

## ⏱️ Estimation

- **Create Tauri project**: 5 min
- **Setup Tailwind + shadcn**: 15 min
- **Install TanStack Query**: 5 min
- **Create API client**: 10 min
- **Setup Zod schemas**: 10 min
- **Create basic layout**: 15 min
- **Test + debug**: 10 min
- **ESLint + Prettier**: 5 min
- **Documentation**: 5 min
- **Total**: ~80 min (1h 20min)

---

## 📝 Key Points

- **CORS**: Backend must allow `http://localhost:5173` (Tauri dev) and `tauri://localhost` (prod)
- **API Prefix**: All endpoints under `/api/` for consistency
- **Error Handling**: Implement proper error boundaries + error messages
- **Loading States**: Show spinners during data fetching
- **Responsive**: Design mobile-first (even though desktop app)

**Status**: 🔄 Ready to start after Phase 1  
**Next Phase**: Phase 3 - UI Components (Plants, Dashboard, Settings)

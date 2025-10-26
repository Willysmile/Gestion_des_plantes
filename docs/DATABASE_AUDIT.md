# Audit des Tables Existantes - Phase 2

## 📊 Tableau Complet des Tables

| # | Table | Colonnes | Type | Statut | Pertinence Phase 2 |
|---|-------|----------|------|--------|-------------------|
| **1** | **plants** | 35 champs | Principal | ✅ Core | **CRITIQUE** ✅ |
| **2** | **photos** | 6 champs | Relation | ✅ Complet | Important 🟡 |
| **3** | **watering_histories** | 5 champs | Historique | ✅ Complet | Phase 3 🔵 |
| **4** | **fertilizing_histories** | 6 champs | Historique | ✅ Complet | Phase 3 🔵 |
| **5** | **repotting_histories** | 6 champs | Historique | ✅ Complet | Phase 3 🔵 |
| **6** | **disease_histories** | 8 champs | Historique | ✅ Complet | Phase 3 🔵 |
| **7** | **plant_histories** | 6 champs | Historique | ✅ Complet | Phase 3 🔵 |
| **8** | **locations** | 3 champs | Lookup | ✅ Complet | Optional 🟡 |
| **9** | **purchase_places** | 3 champs | Lookup | ✅ Complet | Optional 🟡 |
| **10** | **watering_frequencies** | 3 champs | Lookup | ✅ Complet | Important 🟡 |
| **11** | **light_requirements** | 3 champs | Lookup | ✅ Complet | Important 🟡 |
| **12** | **fertilizer_types** | 3 champs | Lookup | ✅ Complet | Phase 3 🔵 |
| **13** | **tag_categories** | 2 champs | Lookup | ✅ Complet | Optional 🟡 |
| **14** | **tags** | 3 champs | Lookup | ✅ Complet | Optional 🟡 |
| **15** | **plant_tag** | 2 champs | Junction | ✅ M2M | Optional 🟡 |

---

## 🎯 Analyse par Priorité Phase 2

### 🔴 CRITIQUE (Phase 2 MVP)

#### 1. **plants** - 35 champs
```
✅ Tous les champs
✅ Bien structurés
✅ Soft delete + archive
✅ Relationships complètes

Utilisation Phase 2:
- Dashboard: List all + filter
- Detail view: afficher tous les champs
- CRUD: create, edit, delete, archive
```

**Champs utilisés Phase 2:**
- name ✅
- scientific_name ✅ (auto-gen)
- family ✅
- reference ✅ (auto-gen)
- description ✅
- location_id ✅ (dropdown)
- watering_frequency_id ✅ (dropdown)
- light_requirement_id ✅ (dropdown)
- temperature_min/max ✅
- humidity_level ✅
- soil_type ✅
- health_status ✅
- is_favorite ✅
- is_archived ✅
- archived_reason ✅

---

### 🟡 IMPORTANT (Phase 2, mais optionnel)

#### 2. **photos** - 6 champs
```
✅ Relation complète
✅ Soft delete

Phase 2 utilisation:
- OPTIONNEL pour MVP
- Photos affichées en Phase 3
- Garder pour futurs uploads
```

#### 10. **watering_frequencies** - Lookup
```
✅ Petit, simple
✅ Bon pour dropdown

Phase 2:
- Select dans plant form
- Pre-populated seeds
- Ex: "Weekly", "Bi-weekly", "Monthly"
```

#### 11. **light_requirements** - Lookup
```
✅ Petit, simple
✅ Bon pour dropdown

Phase 2:
- Select dans plant form
- Pre-populated seeds
- Ex: "Full sun", "Partial shade", "Indirect"
```

#### 8. **locations** - Lookup
```
⚠️ Peut être optionnel

Phase 2:
- OPTIONNEL pour MVP
- Si temps: ajouter select
- Sinon: text input simple
```

#### 9. **purchase_places** - Lookup
```
⚠️ Optionnel pour MVP

Phase 2:
- OPTIONNEL, peut être string simple
```

---

### 🔵 PHASE 3+ (Garder, ne pas utiliser Phase 2)

#### Histories (4 tables)
```
- watering_histories
- fertilizing_histories
- repotting_histories
- disease_histories

Phase 2: NE PAS UTILISER (manque d'UI)
Phase 3: Timeline view complète
```

#### Tags (3 tables)
```
- tag_categories
- tags
- plant_tag (junction)

Phase 2: NE PAS UTILISER (complexe)
Phase 3: Tags système complet
```

#### Fertilizer Types
```
Phase 2: NE PAS UTILISER
Phase 3: Historique fertilisation
```

---

## ✅ RECOMMANDATION PHASE 2

### MVP Frontend - Tables à Utiliser

```
✅ OBLIGATOIRE:
  └─ plants (tous les 35 champs)

🟡 SI TEMPS:
  ├─ watering_frequencies (dropdown)
  ├─ light_requirements (dropdown)
  └─ locations (optionnel)

❌ IGNORER:
  ├─ photos (phase 3)
  ├─ *_histories (phase 3)
  ├─ tags (phase 3)
  └─ purchase_places (non critique)
```

### Frontend MVP Schema

```typescript
// Ce qu'on affiche Phase 2

interface Plant {
  // Auto
  id: number
  reference: string        // ARAC-001
  scientific_name: string  // Monstera deliciosa
  created_at: string
  
  // Input obligatoire
  name: string
  family: string
  
  // Input optionnel
  genus?: string
  species?: string
  description?: string
  
  // Selects (lookups)
  watering_frequency_id?: number
  light_requirement_id?: number
  location_id?: number
  
  // Inputs
  temperature_min?: number
  temperature_max?: number
  humidity_level?: number
  soil_type?: string
  health_status?: string
  
  // Flags
  is_favorite: boolean
  is_indoor: boolean
  is_outdoor: boolean
  is_archived: boolean
  archived_reason?: string
}
```

---

## 🚀 Action Items Phase 2

- [ ] Dashboard affiche: name, family, reference, health_status, is_favorite
- [ ] Detail view: tous les 35 champs (read-only + editable)
- [ ] Create form: 15-20 champs essentiels
- [ ] Dropdowns: watering_frequencies, light_requirements, locations
- [ ] Filter: par family, par health_status, par location
- [ ] Archive/Restore buttons
- [ ] Delete (soft) with reason

---

## 📈 Couverture Estimée Phase 2

| Composant | Couverture | Notes |
|-----------|-----------|-------|
| Plants table | 100% | Tous les champs accessibles |
| Photos table | 0% | Phase 3 |
| Histories | 0% | Phase 3 |
| Tags | 0% | Phase 3 |
| Lookups | 60% | Watering, Light - oui; Others - non |

**Total Phase 2: ~60% des tables utilisées**

---

## 💡 Conclusion

La structure est **EXCELLENT** et bien conçue :

✅ **Strengths:**
- Soft delete (important)
- Archive system (important)
- Bien normalisé
- Lookups extensibles
- Relations propres

⚠️ **Pour Phase 2:**
- Focus sur **plants** table (100%)
- Ajouter 2-3 dropdowns (lookups)
- Ignorer histories & tags
- Photos: optionnel

**= Démarrage rapide et clean ! 🚀**

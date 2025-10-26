# 📋 LOGIQUE MÉTIER - Plant Manager Laravel

**Date:** 26 Octobre 2025  
**Projet:** Plants (Laravel)  
**Purpose:** Documenter les règles métier, workflows, et logiques d'audit

---

## 🎯 TABLE DES MATIÈRES

1. [Création du Nom Scientifique](#création-du-nom-scientifique)
2. [Génération de la Référence](#génération-de-la-référence)
3. [Gestion des Arrosages](#gestion-des-arrosages)
4. [Classification des Besoins](#classification-des-besoins)
5. [Archivage & Restauration](#archivage--restauration)
6. [Historiques & Audit](#historiques--audit)
7. [Validation des Données](#validation-des-données)
8. [Règles de Cohérence](#règles-de-cohérence)

---

## 📝 CRÉATION DU NOM SCIENTIFIQUE

### Logique actuelle (Plant model)

```php
public function getGeneratedScientificNameAttribute(): ?string
{
    // Format: "Genus species"
    // Exemple: "Phalaenopsis amabilis"
    
    if (empty($this->genus) && empty($this->species)) {
        return $this->scientific_name; // Fallback
    }
    
    $parts = [];
    if ($this->genus) $parts[] = $this->genus;
    if ($this->species) $parts[] = $this->species;
    
    return implode(' ', $parts) ?: null;
}
```

### Règles métier

| Field | Format | Règle | Exemple |
|-------|--------|-------|---------|
| `genus` | String | Premier caractère majuscule | "Phalaenopsis" |
| `species` | String | Minuscules (convention botanique) | "amabilis" |
| `subspecies` | String | Optional, format: subsp. name | "subsp. rosenstromii" |
| `variety` | String | Optional, format: var. name | "var. alba" |
| `cultivar` | String | Optional, format: 'Name' (guillemets) | "'White Dream'" |

### Nom complet généré

```
getFullNameAttribute()
Format: "Genus species subsp. name var. name 'Cultivar'"

Exemples:
- "Phalaenopsis amabilis" (minimal)
- "Phalaenopsis amabilis 'White Dream'" (avec cultivar)
- "Phalaenopsis amabilis subsp. rosenstromii var. alba 'Pink Dream'" (complet)
```

### Validation

- **Genus:** Capitalisé (1ère lettre maj, reste minuscules)
- **Species:** Minuscules obligatoires
- **Length:** Chaque partie max 255 caractères
- **Format date achat:** `dd/mm/yyyy` ou `mm/yyyy` (custom rule: FlexibleDate)

---

## 🔖 GÉNÉRATION DE LA RÉFÉRENCE

### Logique actuelle (PlantController.generateReferenceAPI)

```
Format: "{FAMILY}-{NUMBER}"
Exemples: "ARA-001", "ARA-002", "PHI-001"
```

### Algorithme

```php
public function generateReferenceAPI(Request $request)
{
    // 1. Extraire les 3 premières lettres de la famille
    $familyPrefix = strtoupper(substr($request->input('family', ''), 0, 3));
    
    // 2. Chercher toutes les références avec ce préfixe
    $lastPlant = Plant::where('reference', 'like', $familyPrefix . '-%')
        ->latest()
        ->first();
    
    // 3. Extraire le numéro courant
    $currentNumber = $lastPlant 
        ? (int) substr($lastPlant->reference, -3) 
        : 0;
    
    // 4. Incrémenter et formater avec padding
    $nextNumber = $currentNumber + 1;
    $reference = $familyPrefix . '-' . str_pad($nextNumber, 3, '0', STR_PAD_LEFT);
    
    return response()->json(['reference' => $reference]);
}
```

### Règles métier

| Aspect | Règle | Exemple |
|--------|-------|---------|
| **Préfixe** | 3 premières lettres famille (MAJUSCULES) | "ARA" (Araceae) |
| **Séparateur** | Tiret (-) | "ARA-" |
| **Numéro** | Compteur séquentiel (3 chiffres, padded) | "001", "002", "100" |
| **Unicité** | Unique par plante | Pas 2 plantes même référence |
| **Immuabilité** | Ne change pas après création | Pas de modification |
| **Format complet** | `{FAMILY}-{3DIGITS}` | "ARA-001" |

### Cas limites

- Famille vide? → Préfixe par défaut (ou erreur validation)
- Famille < 3 caractères? → Padding avec zeros ou caractères
- Référence manuelle? → Acceptée si unique (validation exists)

**Validation (StorePlantRequest):**
```php
'reference' => 'nullable|string|max:50|unique:plants,reference',
```

---

## 💧 GESTION DES ARROSAGES

### Modèle WateringHistory

```php
protected $table = 'watering_history';

protected $fillable = [
    'plant_id',           // FK → Plant
    'watering_date',      // DATE (format: YYYY-MM-DD)
    'amount',             // String (ex: "250ml", "1L")
    'notes',              // Optional notes (ex: "Leaf spray")
];

protected $casts = [
    'watering_date' => 'datetime',
];
```

### Fréquences d'arrosage (lookup table)

**Table: watering_frequencies**

| ID | Nom (FR) | Description | Fréquence (jours) |
|----|----------|-------------|-------------------|
| 1 | Quotidienne | Arroser chaque jour | 1 |
| 2 | Tous les 3 jours | | 3 |
| 3 | Hebdomadaire | Arroser 1x par semaine | 7 |
| 4 | Bi-hebdomadaire | Arroser 2x par mois | 14 |
| 5 | Mensuelle | Arroser 1x par mois | 30 |

### Règles métier

| Règle | Validation | Audit |
|-------|-----------|-------|
| **watering_date** | DATE format (YYYY-MM-DD) | Loggé si modification |
| **amount** | String (ex: "250ml") | Peut être vide (notes suffisent) |
| **notes** | Optional, max 255 chars | Loggé si modification |
| **last_watering_date (Plant)** | Auto-updateé au create | Synced depuis WateringHistory |
| **Pas de future date** | watering_date ≤ today() | Validation côté formulaire |

### Workflow arrosage

```
1. User clique "Enregistrer arrosage"
2. Form submit: {plant_id, watering_date, amount, notes}
3. Validate: date ≤ today(), plant exists
4. Create WateringHistory entry
5. Update Plant.last_watering_date = watering_date
6. Log audit: "arrosage_ajouté" (plant_id, date, amount)
7. Toast: "Arrosage enregistré!"
```

### Dates importantes

- **last_watering_date:** Dernière date d'arrosage (mis à jour auto)
- **next_watering_date:** Calculé = last_watering_date + (fréquence en jours)
- **Days since watering:** today() - last_watering_date

**Stats dashboard:**
```
Plantes à arroser aujourd'hui: 
  WHERE next_watering_date <= today()
  
Plantes à arroser dans 3 jours:
  WHERE next_watering_date BETWEEN today() AND today() + 3 days
```

---

## 🌞 CLASSIFICATION DES BESOINS

### Besoin en lumière (LightRequirement lookup)

**Table: light_requirements**

| ID | Nom (FR) | Description | Icon | Lumens min |
|----|----------|-------------|------|-----------|
| 1 | Lumière directe | Soleil direct 4+ heures | ☀️ | 3000+ |
| 2 | Lumière vive | Lumière indirecte proche fenêtre | 🌤️ | 1500-3000 |
| 3 | Lumière indirecte | Lumière filtrée, pas soleil direct | 🌥️ | 500-1500 |
| 4 | Ombre partielle | Peu de lumière, loin de fenêtre | 🌦️ | 100-500 |
| 5 | Ombre complète | Plante d'intérieur très éloignée | 🌙 | < 100 |

### Environnement climatique

**Fields sur Plant model:**

| Field | Type | Range | Règle | Exemple |
|-------|------|-------|-------|---------|
| `temperature_min` | INT | -50 à +50°C | < temperature_max | 15 |
| `temperature_max` | INT | -50 à +50°C | > temperature_min | 25 |
| `humidity_level` | INT | 0-100% | Validation: 0-100 | 60 |
| `soil_humidity` | STRING | - | Enum (dry, normal, wet) | "normal" |
| `soil_ideal_ph` | DECIMAL | 0-14 | Validation: between 0,14 | 6.5 |
| `soil_type` | STRING | - | Description libre | "Terreau drainant" |

### Validation (StorePlantRequest)

```php
'temperature_min' => 'nullable|numeric|lt:temperature_max',
'temperature_max' => 'nullable|numeric|gt:temperature_min',
'humidity_level' => 'nullable|numeric|min:0|max:100',
'soil_ideal_ph' => 'nullable|numeric|between:0,14',
'light_requirement' => 'required|integer|min:1|max:5',
```

### Règles de cohérence

```
SI temperature_min EST défini
  → temperature_max DOIT être > temperature_min
  
SI humidity_level EST défini
  → DOIT être entre 0 et 100
  
SI soil_ideal_ph EST défini
  → DOIT être entre 0 et 14 (échelle pH)
```

---

## 📦 ARCHIVAGE & RESTAURATION

### Modèle

**Table: plants (colonnes archive)**

```php
// Archivage
'is_archived' => 'boolean' (default: false),
'archived_date' => 'datetime',
'archived_reason' => 'string',

// Soft delete
'deleted_at' => 'datetime' (SoftDeletes trait),
```

### Workflow archivage

```
User clic "Archiver cette plante"
  ↓
Form: {reason: "Plante mortes", ...}
  ↓
Plant::update({
  is_archived: true,
  archived_date: now(),
  archived_reason: "Plante morte"
})
  ↓
Log audit: "plante_archivée" 
  (plant_id, reason, timestamp)
  ↓
Masquée de la liste "Actives"
Visible en "/plants/archived"
```

### Workflow restauration

```
User clic "Restaurer" (depuis archived list)
  ↓
Plant::update({
  is_archived: false,
  archived_date: null,
  archived_reason: null
})
  ↓
Log audit: "plante_restaurée" 
  (plant_id, timestamp)
  ↓
Réapparaît en liste "Actives"
```

### Règles métier

| Aspect | Règle | Conséquence |
|--------|-------|------------|
| **is_archived** | Boolean flag | Filtre liste par défaut |
| **archived_date** | Timestamp immutable | Trace de quand c'était | 
| **archived_reason** | String optional | Justification pour audit |
| **Soft delete** | deleted_at timestamp | Recovery window? |
| **Récupération** | Peut restaurer dans 30j? | À définir |

---

## 📊 HISTORIQUES & AUDIT

### 5 types d'historiques

#### 1. WateringHistory (Arrosage)

```php
[plant_id, watering_date, amount, notes]
Audit: CREATE, UPDATE, DELETE
```

#### 2. FertilizingHistory (Fertilisation)

```php
[plant_id, fertilizing_date, fertilizer_type_id, amount, notes]
FK: fertilizer_type_id → FertilizerTypes table
Audit: CREATE, UPDATE, DELETE
```

#### 3. RepottingHistory (Rempotage)

```php
[plant_id, repotting_date, old_pot_size, new_pot_size, soil_type, notes]
Audit: CREATE, UPDATE, DELETE
```

#### 4. DiseaseHistory (Maladie)

```php
[plant_id, disease_date, name, treatment, recovery_status, notes]
recovery_status: IN ('in_progress', 'recovered', 'died')
Audit: CREATE, UPDATE, DELETE
Impacts Plant.health_status?
```

#### 5. PlantHistory (Notes générales)

```php
[plant_id, body (text)]
Audit: CREATE, UPDATE, DELETE
```

### AuditLog model

**Table: audit_logs**

```php
protected $fillable = [
    'user_id',              // FK → users (NULL si no auth)
    'action',               // 'CREATE', 'UPDATE', 'DELETE', 'ARCHIVE', 'RESTORE'
    'entity_type',          // 'Plant', 'WateringHistory', etc
    'entity_id',            // ID de l'entité modifiée
    'old_values',           // JSON: {"field": "old_value"}
    'new_values',           // JSON: {"field": "new_value"}
    'details',              // String: human-readable summary
    'ip_address',           // For tracking
    'created_at',           // Timestamp
];
```

### Événements auditables

| Action | Trigger | Log | Details |
|--------|---------|-----|---------|
| **CREATE** | Plant created | action='CREATE' | 'Plante créée: {name}' |
| **UPDATE** | Plant updated | action='UPDATE', old/new values | 'Champ {field}: {old} → {new}' |
| **DELETE** | Plant soft-deleted | action='DELETE' | 'Plante supprimée: {name}' |
| **ARCHIVE** | Plant archived | action='ARCHIVE' | 'Archivée: {reason}' |
| **RESTORE** | Plant restored | action='RESTORE' | 'Restaurée' |
| **ADD_HISTORY** | Arrosage/fert added | action='CREATE' entity='WateringHistory' | 'Arrosage enregistré: {date}' |
| **ADD_DISEASE** | Maladie logged | action='CREATE' entity='DiseaseHistory' | 'Maladie: {name}, traitement: {treatment}' |

### Implémentation

**Middleware ou Observer pattern:**

```php
// Observer Pattern (Laravel)
class PlantObserver
{
    public function created(Plant $plant) { 
        AuditLog::create([
            'action' => 'CREATE',
            'entity_type' => 'Plant',
            'entity_id' => $plant->id,
            'new_values' => json_encode($plant->toArray()),
            'details' => "Plante créée: {$plant->name}",
        ]);
    }
    
    public function updated(Plant $plant) {
        $changes = $plant->getChanges();
        AuditLog::create([
            'action' => 'UPDATE',
            'entity_type' => 'Plant',
            'entity_id' => $plant->id,
            'old_values' => json_encode($plant->getOriginal()),
            'new_values' => json_encode($changes),
            'details' => "Mis à jour: " . implode(', ', array_keys($changes)),
        ]);
    }
}

Plant::observe(PlantObserver::class);
```

---

## ✅ VALIDATION DES DONNÉES

### StorePlantRequest rules

```php
// Obligatoires
'name' => 'required|string|max:255',
'watering_frequency' => 'required|integer|min:1|max:5',
'light_requirement' => 'required|integer|min:1|max:5',

// Taxonomie (optional)
'scientific_name' => 'nullable|string|max:255',
'family' => 'nullable|string|max:255',
'genus' => 'nullable|string|max:255',
'species' => 'nullable|string|max:255',

// Dates
'purchase_date' => ['nullable', 'string', new FlexibleDate],
  → Accepte: "dd/mm/yyyy" ou "mm/yyyy"
'last_watering_date' => 'nullable|date',
'next_repotting_date' => 'nullable|date|after_or_equal:last_repotting_date',

// Environnement
'temperature_min' => 'nullable|numeric|lt:temperature_max',
'temperature_max' => 'nullable|numeric|gt:temperature_min',
'humidity_level' => 'nullable|numeric|min:0|max:100',
'soil_ideal_ph' => 'nullable|numeric|between:0,14',

// Caractéristiques
'growth_speed' => 'nullable|string|in:lente,moyenne,rapide',
'difficulty_level' => 'nullable|integer|min:1|max:5',
'is_toxic' => 'nullable|boolean',

// Photos
'main_photo' => 'nullable|image|max:5120',  // 5MB

// Tags
'tags' => ['nullable', 'array', new ValidateTags()],
'tags.*' => 'integer',

// Archive
'archived_reason' => 'nullable|string|required_if:is_archived,1',
```

### Custom validation rules

**FlexibleDate rule:**
```php
// Accepte "dd/mm/yyyy" ou "mm/yyyy"
// Rejette: "2025-01-01", "janvier 2025"
```

**ValidateTags rule:**
```php
// Vérifie que tous les tags existent en BD
// Que les IDs fournis sont valides
```

---

## 🔗 RÈGLES DE COHÉRENCE

### Cascades et contraintes

| Règle | Implémentation | Audit |
|-------|----------------|-------|
| **Plant → Photos** | Cascade delete (soft) | Loggé |
| **Plant → Histories** | Cascade delete (soft) | Loggé |
| **Plant → Tags** | Many-to-many detach | Loggé |
| **Location → Plants** | Nullable (plant peut pas avoir location) | Pas d'impact |
| **WateringFrequency → Plant** | Cannot delete si plants l'utilisent | Erreur validation |

### Immuabilité

| Field | Changeable? | Notes |
|-------|-----------|-------|
| `reference` | ❌ Non | Générée auto, identifiant permanent |
| `created_at` | ❌ Non | Timestamp de création |
| `archived_date` | ❌ À l'archivage seulement | Reset on restore |
| `genus/species` | ✅ Oui | Peut être corrigé |
| `health_status` | ✅ Oui | Peut évoluer |

### Dates cohérentes

```
purchase_date ≤ today()
  → Pas d'achats futurs

last_watering_date ≤ today()
  → Pas d'arrosages futurs

last_repotting_date ≤ next_repotting_date
  → Validation: after_or_equal

archived_date = NOW() (quand archived)
archived_date = NULL (quand restaurée)
```

---

## 📝 RÉSUMÉ PAR ENTITÉ

### Plant

**Création:**
- Nom + fréquence arrosage + besoin lumière (obligatoires)
- Taxonomie (genus/species) → génère nom scientifique
- Référence auto-générée: {FAMILY}-{COUNTER}

**Modifications:**
- Toutes les mises à jour loggées (old/new values)
- Dates cohérentes validées
- Photos managées (upload, conversion WebP)

**Archivage:**
- Marque is_archived=true + archived_date + raison
- Peut restaurer (is_archived=false, dates reset)

### Historiques

**Arrosage:**
- Date + amount + notes
- Auto-update Plant.last_watering_date
- Stats: "à arroser aujourd'hui"

**Fertilisation:**
- Date + type_engrais + quantité
- Link: FertilizerType FK

**Rempotage:**
- Date + ancienne/nouvelle taille pot + sol

**Maladie:**
- Nom + traitement + statut récupération
- Impact sur Plant.health_status

**Notes:**
- Texte libre (PlantHistory)

### Audit

**AuditLog:**
- Chaque action (CREATE/UPDATE/DELETE/ARCHIVE/RESTORE)
- Old/new values (JSON)
- Human-readable details
- Timestamp + user_id

---

## 🎯 À IMPLÉMENTER EN PYTHON

Lors de la migration vers Python:

1. **Même logique de génération référence** (FAMILY-COUNTER)
2. **Même validation des données** (temp_min < temp_max, pH 0-14, etc)
3. **Même historiques** (5 types)
4. **Observer pattern** pour audit (ou middleware)
5. **Même dates/formats** (dd/mm/yyyy flexible, ISO pour DB)
6. **Même taxonomie** (genus/species → full name)

---

**Document vivant:** À mettre à jour si changements métier

**Dernière mise à jour:** 26 Octobre 2025

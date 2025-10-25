# 📱 CAHIER DES CHARGES - PLANT MANAGER v2 (Python Desktop)

**Date:** 25 Octobre 2025  
**Projet:** Migration de Laravel → Python (FastAPI + PySimpleGUI)  
**Type:** Application Desktop Standalone (SQLite local)  
**Multi-user:** ❌ NON (mode single user)

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#vue-densemble)
2. [Stack technique](#stack-technique)
3. [Modèles de données](#modèles-de-données)
4. [Fonctionnalités](#fonctionnalités)
5. [Architecture API](#architecture-api)
6. [Spécifications UI](#spécifications-ui)
7. [Flux de données](#flux-de-données)
8. [Installation & Déploiement](#installation--déploiement)

---

## 🎯 VUE D'ENSEMBLE

### Objectifs
- ✅ Repartir de zéro (pas de migration de données Laravel)
- ✅ Application desktop standalone (pas de serveur externe)
- ✅ Aucune installation complexe (pip + Python c'est tout)
- ✅ Gestion complète des plantes avec historiques
- ✅ Gestion des photos avec stockage local
- ✅ Export/Import de données

### Cas d'usage principal
Un utilisateur gère sa collection de plantes en local, peut consulter les historiques et exporter ses données.

---

## 🛠️ STACK TECHNIQUE

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Base de données:** SQLite (fichier unique `plants.db`)
- **ORM:** SQLAlchemy
- **Serveur:** Uvicorn (local, http://localhost:8000)
- **Validation:** Pydantic

### Frontend
- **Framework UI:** PySimpleGUI
- **Client HTTP:** requests
- **Image handling:** Pillow

### Stockage
- **Base de données:** `data/plants.db` (SQLite)
- **Photos:** `data/photos/` (dossier local)
- **Exports:** `data/exports/` (ZIP avec JSON + photos)

### Déploiement
- **Packager:** PyInstaller (exécutable unique)
- **Distribution:** Single EXE (Windows) ou binary (Linux/Mac)

---

## 💾 MODÈLES DE DONNÉES

### 1. **Plant** (Plante)
```
id                  INT PRIMARY KEY
name                STR (nom commun)
scientific_name     STR (nom scientifique)
family              STR (famille botanique)
subfamily           STR
genus               STR
species             STR
subspecies          STR
variety             STR
cultivar            STR
reference           STR (identifiant unique pour l'utilisateur)
description         STR (max 200 chars)
health_status       STR (enum: healthy, sick, recovering, dead)
difficulty_level    STR (enum: easy, medium, hard)
growth_speed        STR (enum: slow, medium, fast)
is_indoor           BOOL
is_outdoor          BOOL
is_favorite         BOOL
is_toxic            BOOL
flowering_season    STR (comma-separated months)

# Localisation & Achat
location_id         FK → Location
purchase_date       STR (format: "dd/mm/yyyy" ou "mm/yyyy")
purchase_place_id   FK → PurchasePlace
purchase_price      DECIMAL

# Environnement
watering_frequency_id  FK → WateringFrequency
light_requirement_id   FK → LightRequirement
temperature_min     INT (°C)
temperature_max     INT (°C)
humidity_level      INT (%)
soil_humidity       STR
soil_ideal_ph       DECIMAL
soil_type           STR

# Care
pot_size            STR (ex: "15cm")
max_height          INT (cm)
last_watering_date  DATETIME
last_fertilizing_date DATETIME
fertilizing_frequency STR
last_repotting_date DATETIME
next_repotting_date DATETIME

# Metadata
info_url            STR (lien externe)
main_photo          STR (filename)
created_at          DATETIME
updated_at          DATETIME
is_archived         BOOL
archived_date       DATETIME
archived_reason     STR
deleted_at          DATETIME (soft delete)
```

### 2. **Photo**
```
id                  INT PRIMARY KEY
plant_id            FK → Plant
filename            STR (UUID.webp)
mime_type           STR (image/webp)
size                INT (bytes)
description         STR (optionnel)
is_main             BOOL (true = photo de couverture)
created_at          DATETIME
deleted_at          DATETIME (soft delete)
```

### 3. **WateringHistory**
```
id                  INT PRIMARY KEY
plant_id            FK → Plant
watering_date       DATE
amount              STR (ex: "250ml")
notes               STR (optionnel)
created_at          DATETIME
```

### 4. **FertilizingHistory**
```
id                  INT PRIMARY KEY
plant_id            FK → Plant
fertilizing_date    DATE
fertilizer_type_id  FK → FertilizerType
amount              STR
notes               STR
created_at          DATETIME
```

### 5. **RepottingHistory**
```
id                  INT PRIMARY KEY
plant_id            FK → Plant
repotting_date      DATE
old_pot_size        STR
new_pot_size        STR
soil_type           STR
notes               STR
created_at          DATETIME
```

### 6. **DiseaseHistory**
```
id                  INT PRIMARY KEY
plant_id            FK → Plant
disease_date        DATE
name                STR (ex: "Moisissure")
treatment           STR (traitement appliqué)
recovery_status     STR (enum: in_progress, recovered, died)
notes               STR
created_at          DATETIME
```

### 7. **PlantHistory**
```
id                  INT PRIMARY KEY
plant_id            FK → Plant
body                STR (notes générales)
created_at          DATETIME
```

### 8. **Tag** (Étiquette / Catégorie)
```
id                  INT PRIMARY KEY
name                STR (ex: "Succulente", "Toxique")
tag_category_id     FK → TagCategory
created_at          DATETIME
```

### 9. **TagCategory**
```
id                  INT PRIMARY KEY
name                STR (catégorie: ex "Type", "Propriété")
created_at          DATETIME
```

### 10. **Plant-Tag** (Relation Many-to-Many)
```
plant_id            FK → Plant
tag_id              FK → Tag
```

### Lookup Tables (Énumérations)

**Location** (Emplacements)
```
id, name (ex: "Fenêtre sud", "Bureau")
```

**PurchasePlace** (Lieux d'achat)
```
id, name (ex: "Pépinière X", "Amazon")
```

**WateringFrequency** (Fréquence d'arrosage)
```
id, name (ex: "Journellement", "Chaque 3 jours")
```

**LightRequirement** (Besoin en lumière)
```
id, name (ex: "Lumière indirecte", "Ombre partielle")
```

**FertilizerType** (Types d'engrais)
```
id, name, unit (ex: "NPK 10-10-10", unit: "ml")
```

---

## 🎨 FONCTIONNALITÉS

### 1. **Gestion des Plantes** ✅
- [x] Créer une plante (form complet)
- [x] Visualiser une plante (détails complets)
- [x] Modifier une plante
- [x] Supprimer une plante (soft delete)
- [x] Archiver/Restaurer une plante
- [x] Lister toutes les plantes (avec filtres & recherche)
- [x] Exporter référence automatique (format: TYPE-DATE-COUNTER)

### 2. **Photos** 🖼️
- [x] Upload photo(s) pour une plante
- [x] Conversion auto en WebP
- [x] Définir photo principale
- [x] Supprimer photo
- [x] Affichage galerie

### 3. **Historiques** 📝
- [x] **Arrosage** - Enregistrer date, quantité, notes
- [x] **Fertilisation** - Enregistrer date, type, quantité, notes
- [x] **Rempotage** - Enregistrer date, ancienne/nouvelle taille pot, type sol
- [x] **Maladies** - Enregistrer nom, traitement, date, statut récupération
- [x] **Notes générales** - Notes libres (PlantHistory)
- [x] Voir tous les historiques d'une plante
- [x] Modifier/Supprimer entrée historique

### 4. **Taxonomie Botanique** 🌿
Fileds complète pour classification :
- [x] Nom commun + Nom scientifique
- [x] Famille, Sous-famille, Genre, Espèce, Sous-espèce
- [x] Variété, Cultivar

### 5. **Paramètres & Lookup** ⚙️
- [x] Gestion des emplacements (Location)
- [x] Gestion des lieux d'achat (PurchasePlace)
- [x] Gestion des types d'engrais (FertilizerType)
- [x] Gestion des fréquences d'arrosage (WateringFrequency)
- [x] Gestion des besoins lumineux (LightRequirement)
- [x] Gestion des catégories de tags (TagCategory)
- [x] Gestion des tags (Tag)

### 6. **Tags & Catégories** 🏷️
- [x] Associer multiples tags à une plante
- [x] Tags organisés par catégorie
- [x] Filtrer par tag
- [x] Admin: Créer/Modifier/Supprimer tags

### 7. **Recherche & Filtres** 🔍
- [x] Recherche par nom (texte)
- [x] Filtrer par location
- [x] Filtrer par tag
- [x] Filtrer par statut (santé)
- [x] Filtrer par niveau difficulté
- [x] Filtrer par type (indoor/outdoor)
- [x] Filtrer par favoris

### 8. **Export/Import** 📦
- [x] Exporter toutes les données en ZIP (JSON + photos)
- [x] Importer depuis ZIP
- [x] Checksum SHA256 pour intégrité
- [x] Métadonnées dans export (date, counts, version)
- [x] Dry-run preview avant import

### 9. **Reset & Récupération** 🔄
- [x] Réinitialiser base (optionnel: avec backup automatique)
- [x] Soft delete sur les plantes (30j pour récupérer?)
- [x] Audit log de tous les changements
- [x] Récupérer item supprimé

### 10. **Statistiques** 📊
- [x] Nombre total de plantes
- [x] Plantes par location
- [x] Plantes par tag
- [x] Plantes à arroser aujourd'hui
- [x] Plantes à fertiliser aujourd'hui
- [x] Santé générale (% maladies)
- [x] Plantes archivées/supprimées

---

## 🔌 ARCHITECTURE API

### Endpoints FastAPI

**Base URL:** `http://localhost:8000/api`

#### 🌱 PLANTS
```
GET    /plants                      - Lister toutes les plantes
GET    /plants/{id}                 - Détails d'une plante
POST   /plants                      - Créer plante
PUT    /plants/{id}                 - Modifier plante
DELETE /plants/{id}                 - Supprimer (soft delete)
POST   /plants/{id}/archive         - Archiver
POST   /plants/{id}/restore         - Restaurer
GET    /plants/archived             - Lister plantes archivées
POST   /plants/generate-reference   - Générer référence automatique
```

#### 📷 PHOTOS
```
POST   /plants/{id}/photos          - Upload photo
PATCH  /plants/{id}/photos/{photoId} - Modifier (is_main, description)
DELETE /plants/{id}/photos/{photoId} - Supprimer photo
GET    /plants/{id}/photos          - Lister photos d'une plante
```

#### 🚿 WATERING HISTORY
```
GET    /plants/{id}/watering-history           - Lister
POST   /plants/{id}/watering-history           - Créer
PUT    /plants/{id}/watering-history/{hid}     - Modifier
DELETE /plants/{id}/watering-history/{hid}     - Supprimer
```

#### 🧂 FERTILIZING HISTORY
```
GET    /plants/{id}/fertilizing-history        - Lister
POST   /plants/{id}/fertilizing-history        - Créer
PUT    /plants/{id}/fertilizing-history/{hid}  - Modifier
DELETE /plants/{id}/fertilizing-history/{hid}  - Supprimer
```

#### 🪴 REPOTTING HISTORY
```
GET    /plants/{id}/repotting-history          - Lister
POST   /plants/{id}/repotting-history          - Créer
PUT    /plants/{id}/repotting-history/{hid}    - Modifier
DELETE /plants/{id}/repotting-history/{hid}    - Supprimer
```

#### 🦠 DISEASE HISTORY
```
GET    /plants/{id}/disease-history            - Lister
POST   /plants/{id}/disease-history            - Créer
PUT    /plants/{id}/disease-history/{hid}      - Modifier
DELETE /plants/{id}/disease-history/{hid}      - Supprimer
```

#### 📝 PLANT HISTORY (Notes)
```
GET    /plants/{id}/histories                  - Lister notes
POST   /plants/{id}/histories                  - Créer note
PUT    /plants/{id}/histories/{hid}            - Modifier note
DELETE /plants/{id}/histories/{hid}            - Supprimer note
```

#### 🏷️ TAGS
```
GET    /tags                                   - Lister tous les tags
POST   /tags                                   - Créer tag
PUT    /tags/{id}                              - Modifier tag
DELETE /tags/{id}                              - Supprimer tag
GET    /tag-categories                         - Lister catégories
POST   /tag-categories                         - Créer catégorie
DELETE /tag-categories/{id}                    - Supprimer catégorie
```

#### ⚙️ SETTINGS / LOOKUP
```
GET    /locations                              - Lister emplacements
POST   /locations                              - Créer emplacement
PUT    /locations/{id}                         - Modifier
DELETE /locations/{id}                         - Supprimer

GET    /purchase-places                        - Lister lieux d'achat
POST   /purchase-places                        - Créer
PUT    /purchase-places/{id}                   - Modifier
DELETE /purchase-places/{id}                   - Supprimer

GET    /watering-frequencies                   - Lister fréquences
POST   /watering-frequencies                   - Créer
PUT    /watering-frequencies/{id}              - Modifier
DELETE /watering-frequencies/{id}              - Supprimer

GET    /light-requirements                     - Lister besoins lumière
POST   /light-requirements                     - Créer
PUT    /light-requirements/{id}                - Modifier
DELETE /light-requirements/{id}                - Supprimer

GET    /fertilizer-types                       - Lister types engrais
POST   /fertilizer-types                       - Créer
PUT    /fertilizer-types/{id}                  - Modifier
DELETE /fertilizer-types/{id}                  - Supprimer
```

#### 📦 EXPORT/IMPORT
```
POST   /export                                 - Exporter données
POST   /import/preview                         - Preview import
POST   /import                                 - Importer données
GET    /exports                                - Lister fichiers export
DELETE /exports/{filename}                     - Supprimer export
```

#### 🔄 RESET & RÉCUPÉRATION
```
GET    /audit-logs                             - Historique audit
GET    /deleted-items                          - Items supprimés (soft delete)
POST   /recover/{id}                           - Récupérer item
POST   /reset/preview                          - Preview réinitialisation
POST   /reset                                  - Réinitialiser (avec backup)
```

#### 📊 STATISTIQUES
```
GET    /statistics                             - Toutes stats
GET    /statistics/plants-today-watering       - Plantes à arroser
GET    /statistics/plants-today-fertilizing   - Plantes à fertiliser
```

---

## 🖥️ SPÉCIFICATIONS UI (PySimpleGUI)

### Structure de fenêtres

#### 1. **Main Window** (Accueil/Liste)
- ✅ Barre de menu (File, Edit, View, Help)
- ✅ Barre de recherche avec autocomplete
- ✅ Onglets : "Toutes", "Archivées", "Favorites", "Malade"
- ✅ Filtres : Location, Tag, Difficulté, Type (indoor/outdoor)
- ✅ Tableau avec colonnes : Photo (thumbnail), Nom, Location, Dernière arrosage, Santé, Actions (Edit, Delete, Archive)
- ✅ Boutons : [+ Nouvelle], [Statistiques], [Paramètres], [Export]

#### 2. **Plant Form** (Créer/Modifier)
- ✅ Tabs : Infos de base | Photos | Caractéristiques | Care & History
- ✅ **Tab 1 - Infos de base:**
  - Nom, Nom scientifique
  - Famille, Sous-famille, Genre, Espèce, Subspecies, Variété, Cultivar
  - Description (200 chars max)
  - Health Status, Difficulty, Growth Speed
  - Indoor / Outdoor checkboxes
  - Favorite / Toxic checkboxes
  
- ✅ **Tab 2 - Photos:**
  - Bouton [Upload Photo]
  - Galerie avec thumbnails
  - Checkbox "Photo principale" pour chaque
  - Bouton [Supprimer]
  
- ✅ **Tab 3 - Caractéristiques:**
  - Température min/max
  - Humidité %
  - pH sol idéal
  - Type sol
  - Light Requirement
  - Pot size
  - Max height
  - Flowering season (multi-select mois)
  - Lien info (URL)
  
- ✅ **Tab 4 - Achat & Care:**
  - Purchase date (date picker: dd/mm/yyyy)
  - Purchase place (dropdown)
  - Purchase price
  - Location (dropdown)
  - Référence
  - Watering frequency
  - Fertilizing frequency
  - Last dates (auto-filled)
  
- ✅ Boutons: [Sauvegarder] [Annuler]

#### 3. **Plant Detail Window** (Consultation)
- ✅ Photo principale (grande)
- ✅ Infos de base
- ✅ Onglets : Infos | Photos | Historiques (Arrosage, Fertilisation, Rempotage, Maladies, Notes)
- ✅ Pour chaque historique :
  - Tableau avec colonnes : Date, Info, Notes
  - Boutons : [+ Ajouter], [Modifier], [Supprimer]
  - Export historique (CSV)
- ✅ Boutons: [Modifier] [Archiver] [Supprimer] [Fermer]

#### 4. **Settings Window**
- ✅ Tabs : Locations | Purchase Places | Watering Freq | Light Req | Fertilizer Types | Tags
- ✅ Pour chaque tab :
  - Tableau (liste des items)
  - Boutons: [+ Ajouter] [Modifier] [Supprimer]
- ✅ Checkbox: "Afficher dans les plantes archivées"

#### 5. **Tags Management**
- ✅ Tableau avec colonnes : Catégorie | Nom
- ✅ Dropdown "Catégorie"
- ✅ Boutons: [+ Ajouter Tag] [+ Ajouter Catégorie] [Modifier] [Supprimer]

#### 6. **Statistics Window**
- ✅ KPI Cards : Total plantes, À arroser, À fertiliser, Malade, Archivées
- ✅ Graphique : Plantes par location
- ✅ Graphique : Plantes par tag
- ✅ Graphique : Santé (sain / malade / récupération)
- ✅ Tableau : Arrosages prévus (prochains 7 jours)

#### 7. **Export/Import Window**
- ✅ **Export:**
  - Bouton [Exporter maintenant]
  - Checkbox [Inclure photos]
  - Liste des exports existants
  - Boutons: [Télécharger] [Supprimer]
  
- ✅ **Import:**
  - Bouton [Sélectionner fichier ZIP]
  - Preview : Nombre plantes, photos, tags
  - Dropdown : Mode (FRESH / MERGE / REPLACE)
  - Bouton [Importer]

#### 8. **Reset Window**
- ✅ Warning message
- ✅ Checkbox [Créer backup automatique avant reset]
- ✅ Bouton [Réinitialiser] (confirmation dialog)
- ✅ Progress bar pendant reset

#### 9. **Audit Log / Recovery Window**
- ✅ Tableau : Date | Utilisateur | Action | Entity | Details
- ✅ Filtres: Type action, Date range
- ✅ Pour items supprimés :
  - Tableau : Plant name | Date suppression | Action [Récupérer]

### Design & Couleurs
- **Thème:** Light/Dark toggle
- **Palette:** Verte (nature)
  - Primary: #2ecc71 (vert)
  - Secondary: #3498db (bleu)
  - Danger: #e74c3c (rouge)
  - Neutral: #95a5a6 (gris)

---

## 🔄 FLUX DE DONNÉES

### Flow: Créer une plante
```
UI (PySimpleGUI)
  ↓ User remplit form + upload photo
  ↓ POST /plants {name, scientific_name, ...}
Backend (FastAPI)
  ↓ Validate avec Pydantic
  ↓ Save Plant en DB
  ↓ Move uploaded photo en WebP
  ↓ Return {id, ...}
  ↓
UI
  ↓ Affiche toast "Plante créée!"
  ↓ Refresh liste plantes
```

### Flow: Arroser une plante
```
UI → POST /plants/{id}/watering-history {watering_date, amount, notes}
Backend → Create WateringHistory
         → Update Plant.last_watering_date
         → Return {success: true}
UI → Toast "Arrosage enregistré"
   → Refresh détails plante
```

### Flow: Exporter données
```
UI [Export button]
  ↓
GET /export?include_photos=true
Backend
  ↓ Collect all Plants + Relations
  ↓ Copy photos en ZIP
  ↓ Generate backup.json + metadata.json
  ↓ Return ZIP file (stream)
  ↓
UI → Save ZIP en /data/exports/
   → Toast "Export terminé!"
```

### Flow: Importer données
```
UI [Select ZIP file]
  ↓
POST /import/preview {file}
Backend → Parse ZIP
        → Extract JSON
        → Validate (dry-run)
        → Return {plants_count, tags_count, warnings}
UI → Show dialog: "50 plantes trouvées, OK?"
  ↓ User clicks OK
  ↓
POST /import {file, mode: "MERGE"}
Backend → Import data (mode check)
        → Update DB
        → Return {imported_count}
UI → Toast "Import complété!"
```

---

## 📦 INSTALLATION & DÉPLOIEMENT

### Structure du projet

```
plant_manager_python/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py (entry point FastAPI)
│   │   ├── models/
│   │   │   ├── plant.py
│   │   │   ├── photo.py
│   │   │   ├── history.py (watering, fertilizing, etc)
│   │   │   ├── tag.py
│   │   │   └── ...
│   │   ├── schemas/
│   │   │   ├── plant_schema.py (Pydantic)
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── plant_service.py
│   │   │   ├── backup_service.py
│   │   │   ├── image_service.py
│   │   │   └── ...
│   │   ├── routes/
│   │   │   ├── plants.py
│   │   │   ├── photos.py
│   │   │   ├── export_import.py
│   │   │   └── ...
│   │   ├── utils/
│   │   │   ├── db.py (SQLAlchemy setup)
│   │   │   ├── constants.py
│   │   │   └── ...
│   │   └── config.py
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
│
├── frontend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py (PySimpleGUI entry)
│   │   ├── windows/
│   │   │   ├── main_window.py
│   │   │   ├── plant_form.py
│   │   │   ├── plant_detail.py
│   │   │   ├── settings.py
│   │   │   ├── export_import.py
│   │   │   └── ...
│   │   ├── components/
│   │   │   ├── dialogs.py
│   │   │   ├── tables.py
│   │   │   └── ...
│   │   ├── api_client.py (requests wrapper)
│   │   ├── config.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── run.py
│
├── data/
│   ├── plants.db (SQLite - sera créé)
│   ├── photos/ (images WebP)
│   └── exports/ (ZIP backups)
│
├── README.md
├── INSTALLATION.md
├── .gitignore
└── requirements-all.txt (dependencies complètes)
```

### Dépendances Backend

```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
pydantic-settings==2.1.0
pillow==10.1.0
python-multipart==0.0.6
python-dateutil==2.8.2
```

### Dépendances Frontend

```
PySimpleGUI==4.60.5
requests==2.31.0
Pillow==10.1.0
matplotlib==3.8.2
```

### Installation (utilisateur final)

#### Option 1: Source (Dev)
```bash
# Clone repo
git clone https://github.com/Willysmile/Plants.git plant_manager_python
cd plant_manager_python

# Terminal 1: Backend
cd backend
pip install -r requirements.txt
python run.py  # Lance sur http://localhost:8000

# Terminal 2: Frontend
cd frontend
pip install -r requirements.txt
python run.py  # Lance UI PySimpleGUI
```

#### Option 2: Exécutable (Prod)
```bash
# Download plant_manager.exe (ou .app/.bin selon OS)
./plant_manager.exe
# (inclut backend + frontend, lance tout automatiquement)
```

### Build Exécutable (PyInstaller)

```bash
# Backend + Frontend en single EXE
pyinstaller --onefile \
  --add-data "data:data" \
  --hidden-import=fastapi \
  --hidden-import=uvicorn \
  --hidden-import=sqlalchemy \
  ./backend/main.py \
  ./frontend/main.py
```

---

## 🔐 Sécurité & Intégrité

### Backup/Checksum
- ✅ Tous les exports inclus SHA256 checksum
- ✅ Validation checksum lors import
- ✅ Audit log de toutes les opérations
- ✅ Soft delete (30j recovery window)

### Données
- ✅ SQLite local (chiffrement optionnel)
- ✅ Photos en WebP optimisées
- ✅ Pas de données sensibles
- ✅ Export portable (ZIP standard)

---

## 📝 NOTES

### Différences avec Laravel
1. **Pas de multi-user** → simplification massive
2. **SQLite local** → pas de serveur MySQL
3. **PySimpleGUI** → interface desktop native
4. **Single binary** → déploiement trivial
5. **Même features, meilleur DX** pour partage/installation

### À ne PAS implémenter
- ❌ Authentification (single user)
- ❌ Multi-user permissions
- ❌ API authentication/tokens
- ❌ Email verification
- ❌ User registration

### Extensibilité future
- 🔮 Thème clair/sombre
- 🔮 Synchronisation cloud
- 🔮 Mode multi-user (SQLite → PostgreSQL)
- 🔮 Mobile version
- 🔮 Recommandations IA (care tips)

---

## ✅ CHECKLIST FINALE

- [ ] Backend API complète ✅
- [ ] Base de données SQLite ✅
- [ ] Frontend PySimpleGUI ✅
- [ ] Export/Import ZIP ✅
- [ ] Gestion photos WebP ✅
- [ ] Historiques tous types ✅
- [ ] Tags & catégories ✅
- [ ] Audit logs ✅
- [ ] Tests unitaires
- [ ] Documentation code
- [ ] README complet
- [ ] Build PyInstaller
- [ ] Deploy sur GitHub

---

**Prêt à coder! 🚀**

# 🚀 Installation sur un Nouveau PC - Gestion des Plantes

**Date:** 24 décembre 2025  
**Version:** 2.0.0

---

## 📋 PRÉREQUIS

### Logiciels Requis

1. **Git** (pour cloner le projet)
   ```bash
   sudo apt install git  # Ubuntu/Debian
   ```

2. **Python 3.11+**
   ```bash
   sudo apt install python3.11 python3.11-venv python3-pip
   ```

3. **Node.js 18+ et npm**
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install -y nodejs
   ```

4. **Pillow dependencies** (pour traitement images)
   ```bash
   sudo apt install libjpeg-dev zlib1g-dev libwebp-dev
   ```

---

## 📥 ÉTAPE 1: CLONER LE PROJET

### Option A: Via GitHub (si clé SSH configurée)

```bash
cd ~/Documents/Apps
git clone git@github.com:Willysmile/Gestion_des_plantes.git
cd Gestion_des_plantes
```

### Option B: Via HTTPS

```bash
cd ~/Documents/Apps
git clone https://github.com/Willysmile/Gestion_des_plantes.git
cd Gestion_des_plantes
```

### Option C: Copie directe depuis USB/réseau

```bash
# Copier le dossier complet depuis l'autre PC
cp -r /media/usb/Gestion_des_plantes ~/Documents/Apps/
cd ~/Documents/Apps/Gestion_des_plantes
```

---

## 🔧 ÉTAPE 2: CONFIGURATION BACKEND

### 1. Créer environnement virtuel Python

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows
```

### 2. Installer dépendances Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configuration base de données

```bash
# Créer dossiers nécessaires
mkdir -p data/photos

# Si vous avez une base de données existante:
# - Copier backend/data/plants.db depuis l'ancien PC
# - Copier backend/data/photos/ depuis l'ancien PC

# Si nouvelle installation (base vide):
alembic upgrade head  # Créer toutes les tables
```

### 4. Variables d'environnement (optionnel)

```bash
# Créer fichier .env dans backend/
cat > .env << EOF
DATABASE_URL=sqlite:///./data/plants.db
PHOTOS_DIR=./data/photos
MAX_PHOTO_SIZE_MB=5
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
EOF
```

---

## 🎨 ÉTAPE 3: CONFIGURATION FRONTEND

### 1. Installer dépendances Node.js

```bash
cd ../frontend
npm install
```

### 2. Vérifier configuration

Le fichier `frontend/src/config.js` devrait pointer vers le backend:

```javascript
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api',
  PHOTOS_URL: 'http://localhost:8000/api/photos'
}
```

---

## 🚀 ÉTAPE 4: DÉMARRAGE

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate  # Si pas déjà activé
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Output attendu:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

**Output attendu:**
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 3. Ouvrir dans navigateur

```
http://localhost:5173
```

---

## 📊 ÉTAPE 5: VÉRIFICATION INSTALLATION

### Checklist Rapide

- [ ] Backend répond sur `http://localhost:8000/docs` (Swagger UI)
- [ ] Frontend s'affiche sur `http://localhost:5173`
- [ ] Pas d'erreurs CORS dans la console navigateur
- [ ] Liste des plantes s'affiche (vide si nouvelle DB)
- [ ] Possibilité de créer une plante test

### Test Backend API

```bash
# Test simple
curl http://localhost:8000/api/plants

# Devrait retourner:
{
  "items": [],
  "total": 0,
  "page": 1,
  "size": 50
}
```

### Test Upload Photo

```bash
# Créer une plante test
curl -X POST http://localhost:8000/api/plants \
  -H "Content-Type: application/json" \
  -d '{
    "common_name": "Test Plant",
    "species": "Test Species"
  }'

# Upload photo
curl -X POST http://localhost:8000/api/plants/1/photos \
  -F "file=@/path/to/image.jpg"
```

---

## 🔄 ÉTAPE 6: MIGRATION DONNÉES (si ancien PC)

### Copier Base de Données

```bash
# Sur l'ancien PC
cd ~/Documents/Apps/Gestion_des_plantes/backend
tar -czf backup_$(date +%Y%m%d).tar.gz data/

# Transférer vers nouveau PC (USB, réseau, etc.)

# Sur le nouveau PC
cd ~/Documents/Apps/Gestion_des_plantes/backend
tar -xzf backup_20251224.tar.gz
```

### Vérifier Migrations

```bash
cd backend
source venv/bin/activate
alembic current  # Voir version actuelle
alembic upgrade head  # Appliquer migrations manquantes
```

---

## 🐛 DÉPANNAGE

### Erreur: "ModuleNotFoundError: No module named 'PIL'"

```bash
pip install Pillow
```

### Erreur: "Cannot find module 'vite'"

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erreur CORS dans navigateur

Vérifier que `backend/app/main.py` contient:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Port 8000 déjà utilisé

```bash
# Changer le port backend
uvicorn app.main:app --reload --port 8001

# Mettre à jour frontend/src/config.js
# BASE_URL: 'http://localhost:8001/api'
```

### Problème permissions photos

```bash
chmod -R 755 backend/data/photos
```

### Base de données corrompue

```bash
cd backend
rm data/plants.db
alembic upgrade head  # Recréer DB vide
```

---

## 📚 COMMANDES UTILES

### Backend

```bash
# Activer environnement virtuel
source backend/venv/bin/activate

# Démarrer serveur
uvicorn app.main:app --reload

# Voir logs détaillés
uvicorn app.main:app --reload --log-level debug

# Lancer tests
pytest

# Créer migration
alembic revision --autogenerate -m "description"

# Appliquer migrations
alembic upgrade head

# Revenir à migration précédente
alembic downgrade -1
```

### Frontend

```bash
# Démarrer dev server
npm run dev

# Build production
npm run build

# Prévisualiser build
npm run preview

# Linter
npm run lint
```

### Git

```bash
# Voir branches
git branch -a

# Changer de branche
git checkout feature/quick-wins

# Voir derniers commits
git log --oneline -10

# Voir modifications
git status
git diff

# Tirer dernières modifications
git pull origin feature/quick-wins
```

---

## 🎯 CONFIGURATION GITHUB SSH (optionnel)

### Générer clé SSH

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Accepter emplacement par défaut
# Entrer passphrase (optionnel)
```

### Ajouter clé à GitHub

```bash
# Afficher clé publique
cat ~/.ssh/id_ed25519.pub

# Copier et ajouter sur GitHub:
# https://github.com/settings/keys
```

### Tester connexion

```bash
ssh -T git@github.com
# Devrait afficher: "Hi Willysmile! You've successfully authenticated..."
```

---

## 📦 STRUCTURE PROJET

```
Gestion_des_plantes/
├── backend/
│   ├── app/
│   │   ├── models/         # 28 modèles SQLAlchemy
│   │   ├── routes/         # 10 fichiers routes
│   │   ├── services/       # 8 services
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # Point d'entrée FastAPI
│   ├── data/
│   │   ├── plants.db       # Base SQLite
│   │   └── photos/         # Photos stockées
│   ├── migrations/         # 12 migrations Alembic
│   ├── tests/              # Tests pytest
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── pages/          # 17 pages React
│   │   ├── components/     # 29 composants
│   │   ├── hooks/          # 26 hooks
│   │   └── lib/api/        # Clients API
│   ├── package.json
│   └── vite.config.js
└── docs/
    ├── AUDIT_COMPLET_PROJET.md  # Documentation complète
    └── ...
```

---

## ✅ CHECKLIST POST-INSTALLATION

- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] API accessible sur /docs
- [ ] Peut créer/modifier/supprimer plante
- [ ] Peut uploader photo
- [ ] Photos convertissent en WebP
- [ ] Historiques fonctionnent
- [ ] Propagations visibles
- [ ] Audit logs enregistrés
- [ ] Pas d'erreurs console navigateur

---

## 🆘 SUPPORT

### Fichiers de log

- **Backend:** Console où uvicorn tourne
- **Frontend:** Console développeur navigateur (F12)
- **Database:** SQLite viewer (DB Browser for SQLite)

### Documentation

- **Backend API:** http://localhost:8000/docs
- **Audit complet:** `docs/AUDIT_COMPLET_PROJET.md`
- **Quick Start:** `QUICKSTART.md`

### Ressources

- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Alembic:** https://alembic.sqlalchemy.org/

---

## 🎉 C'EST TERMINÉ !

Votre installation est prête. Vous pouvez maintenant:

1. ✅ Gérer vos plantes
2. ✅ Uploader des photos
3. ✅ Tracker les propagations
4. ✅ Consulter l'historique
5. ✅ Visualiser les statistiques

**Bon jardinage ! 🌱**

---

**Dernière mise à jour:** 24 décembre 2025  
**Version:** 2.0.0  
**Auteur:** GitHub Copilot

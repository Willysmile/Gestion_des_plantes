# 🔄 Synchronisation avec l'Autre PC

## 📦 État Actuel

**✅ Commits locaux effectués:**
- `a1fa9d7` - feat: Add photo reordering with drag-and-drop
- `4fb1e01` - docs: Add complete installation guide for new PC setup

**⚠️ Problème:** Push bloqué par clé SSH manquante/invalide

---

## 🚀 OPTION 1: Pousser depuis CE PC (recommandé)

### Si vous avez configuré SSH:

```bash
cd ~/Documents/Apps/Gestion_des_plantes

# Vérifier clé SSH existe
ls -la ~/.ssh/id_*.pub

# Si pas de clé, en générer une:
ssh-keygen -t ed25519 -C "votre_email@exemple.com"

# Copier la clé publique
cat ~/.ssh/id_ed25519.pub

# Ajouter sur GitHub: https://github.com/settings/keys
# Puis:
ssh -T git@github.com  # Tester

# Pousser les commits
git push origin feature/quick-wins
```

### Alternative HTTPS:

```bash
cd ~/Documents/Apps/Gestion_des_plantes

# Changer remote en HTTPS
git remote set-url origin https://github.com/Willysmile/Gestion_des_plantes.git

# Pousser (demandera username/token GitHub)
git push origin feature/quick-wins

# Entrer vos identifiants GitHub
```

---

## 💾 OPTION 2: Transférer via USB/Réseau

### Sur CE PC:

```bash
cd ~/Documents/Apps/Gestion_des_plantes

# Créer archive complète
tar -czf gestion_plantes_backup_$(date +%Y%m%d).tar.gz \
  --exclude='backend/venv' \
  --exclude='frontend/node_modules' \
  --exclude='backend/__pycache__' \
  --exclude='backend/data/photos' \
  .

# Copier vers USB
cp gestion_plantes_backup_*.tar.gz /media/usb/
```

### Sur l'AUTRE PC:

```bash
# Extraire archive
cd ~/Documents/Apps
tar -xzf /media/usb/gestion_plantes_backup_*.tar.gz

# Suivre guide INSTALLATION_NOUVEAU_PC.md
```

---

## 🔀 OPTION 3: Merger vers main (après push)

### Une fois les commits poussés:

```bash
cd ~/Documents/Apps/Gestion_des_plantes

# Passer sur main
git checkout main

# Tirer dernières modifications
git pull origin main

# Merger feature/quick-wins
git merge feature/quick-wins

# Pousser main
git push origin main

# Nettoyer branche feature (optionnel)
git branch -d feature/quick-wins
git push origin --delete feature/quick-wins
```

---

## 📋 CHECKLIST AVANT SYNC

- [ ] Tous les fichiers importants sont commités
- [ ] Base de données sauvegardée (`backend/data/plants.db`)
- [ ] Photos sauvegardées (`backend/data/photos/`)
- [ ] Variables d'environnement documentées
- [ ] Tests passent (si applicable)

---

## 🎯 SUR L'AUTRE PC

### 1. Cloner/Tirer le projet

```bash
# Si nouveau PC (pas encore cloné):
git clone https://github.com/Willysmile/Gestion_des_plantes.git
cd Gestion_des_plantes
git checkout feature/quick-wins  # Ou main

# Si déjà cloné:
cd ~/Documents/Apps/Gestion_des_plantes
git fetch origin
git checkout feature/quick-wins  # Ou main
git pull origin feature/quick-wins
```

### 2. Installer dépendances

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 3. Migrer base de données

```bash
cd backend

# Si base vide:
alembic upgrade head

# Si base existante copiée depuis ancien PC:
alembic current  # Vérifier version
alembic upgrade head  # Appliquer nouvelles migrations
```

### 4. Démarrer application

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 🆘 Résolution Problème SSH

### Erreur: "Permission denied (publickey)"

```bash
# 1. Vérifier clé SSH existe
ls ~/.ssh/id_*.pub

# 2. Si non, créer:
ssh-keygen -t ed25519 -C "votre_email@exemple.com"

# 3. Ajouter à ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 4. Copier clé publique
cat ~/.ssh/id_ed25519.pub

# 5. Ajouter sur GitHub:
# https://github.com/settings/keys

# 6. Tester
ssh -T git@github.com
```

### Alternative: Utiliser HTTPS

```bash
git remote set-url origin https://github.com/Willysmile/Gestion_des_plantes.git
git push origin feature/quick-wins
# Entrer token GitHub (pas password)
```

---

## 📊 Fichiers Importants à Transférer

### Essentiels:
- `backend/data/plants.db` - Base de données SQLite
- `backend/data/photos/` - Toutes les photos

### Configuration:
- `backend/.env` (si vous en avez créé un)
- `frontend/src/config.js` (normalement déjà commité)

### Optionnel:
- `.git/` - Tout l'historique Git (si copie USB)

---

## ✅ Vérification Post-Sync

Sur l'autre PC, vérifier que:

```bash
# Git à jour
git log --oneline -5
# Devrait montrer vos 2 derniers commits

# Dépendances installées
cd backend && pip list | grep -E "fastapi|pillow|alembic"
cd ../frontend && npm list --depth=0 | grep -E "react|vite|dnd-kit"

# Migrations à jour
cd backend
alembic current
# Devrait montrer: 5bf7f24bfad9 (head)

# Application démarre
uvicorn app.main:app --reload  # Backend
npm run dev  # Frontend
```

---

## 🎉 Résumé

1. **PC Actuel:** 2 commits locaux prêts
2. **Action:** Pousser vers GitHub (SSH ou HTTPS)
3. **Autre PC:** Pull + npm install + pip install + alembic upgrade
4. **Vérifier:** Application fonctionne

**Tout est prêt pour le transfert ! 🚀**

---

**Date:** 24 décembre 2025  
**Branche:** feature/quick-wins  
**Commits:** a1fa9d7, 4fb1e01

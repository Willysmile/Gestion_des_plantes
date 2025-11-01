# 🌱 Gestion des Plantes

> Une application web moderne et intuitive pour prendre soin de vos plantes d'intérieur et extérieur.

Suivez l'arrosage, trackez la croissance, organisez vos plantes et ne laissez plus aucune plante sans attention !

---

## 🚀 Démarrer en 5 minutes

### Prérequis
- Python 3.9+
- Node.js 16+
- Git

### Installation & Lancement

**1️⃣ Cloner et installer les dépendances**

```bash
git clone <repo-url>
cd Gestion_des_plantes

# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd ../frontend
npm install
```

**2️⃣ Lancer le backend (Terminal 1)**

```bash
cd backend
python -m uvicorn app.main:app --reload
# L'API sera disponible à http://localhost:8000
# Documentation interactive : http://localhost:8000/docs
```

**3️⃣ Lancer le frontend (Terminal 2)**

```bash
cd frontend
npm run dev
# L'app s'ouvrira automatiquement à http://localhost:5173
```

### 4️⃣ Première utilisation

1. Ouvrez http://localhost:5173 
2. Créez votre première plante
3. Configurez l'arrosage automatique
4. C'est parti ! 🎉

---

## 💡 Fonctionnalités Principales

- ✅ **Créer et gérer vos plantes** - Cataloguez toutes vos plantes avec photos
- ✅ **Suivi d'arrosage** - Rappels automatiques et historique
- ✅ **Fiches plantes détaillées** - Besoins en eau, lumière, température, etc.
- ✅ **Galerie photo** - Suivez la croissance de vos plantes
- ✅ **Export de données** - Sauvegardez vos collections en CSV/JSON
- ✅ **Archive & Restauration** - Gérez vos anciennes plantes
- ✅ **Interface responsive** - Fonctionne sur desktop et mobile
- ✅ **API REST complète** - Pour l'intégration

---

## 📚 Documentation

- **[DEMARRER_ICI.md](docs/DEMARRER_ICI.md)** ← **Guide complet pour débuter**
- **[docs/INDEX.md](docs/INDEX.md)** - Index de toute la documentation
- **[docs/guides/](docs/guides/)** - Tutoriels et guides d'utilisation

---

## 🛠️ Stack Technologique

### Backend
- **FastAPI** - Framework API moderne et rapide (Python)
- **SQLAlchemy** - ORM pour la base de données
- **Pydantic** - Validation des données
- **Alembic** - Migrations de schéma
- **pytest** - Tests automatisés

### Frontend
- **Vue.js 3** - Framework frontend progressif
- **Vite** - Build tool ultra-rapide
- **TailwindCSS** - Styling utilitaire
- **Axios/Fetch** - Communication avec l'API

### Base de Données
- **PostgreSQL** (production)
- **SQLite** (développement)

---

## 🧑‍💻 Architecture Technique (pour développeurs)

```
Gestion_des_plantes/
├── backend/                # 🐍 API FastAPI
│   ├── app/
│   │   ├── main.py         # Point d'entrée
│   │   ├── config.py       # Configuration
│   │   ├── models/         # Modèles de données (SQLAlchemy)
│   │   ├── schemas/        # Validation (Pydantic)
│   │   ├── routes/         # Endpoints API (CRUD, etc.)
│   │   ├── services/       # Logique métier
│   │   └── utils/          # Utilitaires
│   ├── migrations/         # Migrations Alembic
│   ├── tests/              # Tests unitaires
│   ├── requirements.txt    # Dépendances Python
│   └── pytest.ini
│
├── frontend/               # 🎨 Interface web
│   ├── src/
│   │   ├── components/     # Composants Vue
│   │   ├── pages/          # Pages de l'app
│   │   ├── stores/         # État global
│   │   └── services/       # Appels API
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── docs/                   # 📚 Documentation
├── tests/                  # 🧪 Tests d'intégration
├── data/                   # 💾 Données applicatives
└── tools/                  # 🔧 Outils utilitaires
```

### Points clés de l'architecture
- **Service Layer Pattern** - Logique métier séparée des routes
- **REST API** - Endpoints standards et documentés
- **Soft Delete** - Archive au lieu de supprimer
- **Dependency Injection** - Meilleure testabilité

---

## 🧪 Tests

```bash
# Lancer les tests backend
cd backend
pytest

# Avec couverture de code
pytest --cov

# Tests spécifiques
pytest tests/test_plants.py -v
```

---

## 🔧 Commandes Utiles

```bash
# Backend - Créer migration après modification du modèle
cd backend
alembic revision --autogenerate -m "Description"

# Backend - Appliquer les migrations
alembic upgrade head

# Frontend - Build pour production
cd frontend
npm run build

# Frontend - Lint et format
npm run lint
npm run format
```

---

## 🐛 Troubleshooting

**L'API ne répond pas ?**
- Vérifiez que le backend tourne : `http://localhost:8000/docs`
- Vérifiez les logs dans le terminal backend

**L'app frontend ne se charge pas ?**
- Vérifiez que npm run dev tourne correctement
- Effacez le cache : `rm -rf node_modules .nuxt && npm install`

**Problèmes de base de données ?**
- Pour SQLite de développement : `rm backend/plants.db`
- Relancez les migrations : `alembic upgrade head`

---

## 📋 Licence & Crédits

### 📜 Licence
Ce projet est distribué sous **licence libre** - libre d'utilisation, modification et distribution.

### 🧠 Conception & Développement

- **Concept & Architecture :** [Willysmile](https://github.com/Willysmile)
- **Développement :** 
  - GitHub Copilot et ses agents IA
  - Claude Haiku 3.5
  - Développement collaboratif homme/IA

### 📦 Ressources & Dépendances

Merci aux projets open-source qui rendent possible ce projet :

- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue.js](https://vuejs.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Vite](https://vitejs.dev/)
- [TailwindCSS](https://tailwindcss.com/)
- Et bien d'autres...

---

## 🚀 Prochaines Étapes

1. 📖 Lire [DEMARRER_ICI.md](docs/DEMARRER_ICI.md) pour l'installation complète
2. 🌱 Créer votre première plante
3. 📸 Ajouter des photos
4. ⏰ Configurer l'arrosage automatique
5. 🌿 Cultiver avec succès !

---

## 💬 Besoin d'aide ?

- Consultez la [documentation](docs/INDEX.md)
- Vérifiez [DEMARRER_ICI.md](docs/DEMARRER_ICI.md)
- Explorez les [guides](docs/guides/)

---

**Faites prospérer vos plantes ! 🌿🪴🌻**

*Dernière mise à jour : 1er novembre 2025*  
*Version : v2.10*

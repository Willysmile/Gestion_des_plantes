# 🌱 Futures Fonctionnalités - Gestion des Plantes

## État Actuel (v2.20) ✅
- Dashboard unifié avec actions + analytics
- Graphiques Recharts (santé, activité)
- API statistiques complètes
- Suivi arrosage/fertilisation/maladies
- Gestion photos plantes
- Tags et catégories

---

## Phase Suivante - Priorité HAUTE 🔴

### 1. 📅 Calendrier Interactif Vue Mensuelle
**Objectif:** Planifier visuellement les soins des plantes

**Fonctionnalités:**
- Vue calendrier mois/semaine/jour
- Code couleur par type de soin:
  - 🔵 Bleu = À arroser
  - 🟠 Ambre = À fertiliser
  - 🔴 Rouge = Critique/Maladie
- Affichage des plantes pour chaque jour
- Drag & drop pour reprogrammer
- Indicateurs visuels (points de couleur)

**Détails Techniques:**
- Composant: `CalendarView.jsx`
- Endpoint: Générer automatiquement les dates basées sur `watering_frequency_id`
- Librairie: `react-big-calendar` ou `fullcalendar`
- Backend: Nouvelle route `/statistics/calendar?month=2025-11`

**Estimation:** 3-4h

---

### 2. 🔔 Système d'Alertes Avancé
**Objectif:** Notifier les actions urgentes

**Fonctionnalités:**
- Badge rouge sur plantes critiques
- Popup "Soin urgent: Monstera" au chargement
- Historique des alertes ignorées
- Son optionnel pour urgences
- Toast notifications en haut

**Détails Techniques:**
- Contexte: `AlertContext.jsx` (nouveau)
- LocalStorage: Historique alertes (7 jours)
- Route backend: `/statistics/critical-plants`
- Composant: `AlertBanner.jsx`

**Estimation:** 2-3h

---

## Phase Suivante - Priorité MOYENNE 🟠

### 3. 📊 Export Avancé (CSV/PDF)
**Objectif:** Générer rapports et exports

**Fonctionnalités:**
- Export CSV: Plantes + historiques
- Export PDF: Rapport formaté avec graphiques
- Sélection de colonnes personnalisée
- Filtres export (plantes, période, type de soin)
- Étiquettes pour impression

**Détails Techniques:**
- Librairie: `papaparse` (CSV), `jspdf` + `html2canvas` (PDF)
- Route backend: `POST /export/csv` et `POST /export/pdf`
- Composant: `ExportModal.jsx`

**Estimation:** 4-5h

---

### 4. 🔍 Recherche et Filtres Avancés
**Objectif:** Trouver rapidement les plantes

**Fonctionnalités:**
- Barre de recherche globale
- Filtres: santé, localisation, type, fréquence
- Tri: par nom, santé, date arrosage
- Sauvegarde filtres favoris
- Suggestions autocomplete

**Détails Techniques:**
- Composant: `SearchBar.jsx` + `FilterPanel.jsx`
- Hook: `useSearchFilter.js`
- Route backend: `GET /plants/search?q=...&filters=...`

**Estimation:** 3-4h

---

### 5. 🎨 Vues Personnalisables
**Objectif:** Adapter l'affichage à ses besoins

**Fonctionnalités:**
- Cartes vs Listes vs Grille
- Colonnes visibles/masquées
- Taille des éléments (compact/normal/large)
- Ordre de tri personnalisé
- Thème sombre/clair

**Détails Techniques:**
- Contexte: `ViewPreferencesContext.jsx`
- LocalStorage: Préférences utilisateur
- Composant: `ViewSettings.jsx`

**Estimation:** 3-4h

---

## Phase Suivante - Priorité BASSE 🟡

### 6. 📱 Mode Mobile Optimisé
**Objectif:** Application mobile-first

**Fonctionnalités:**
- Bottom navigation (au lieu de header)
- Swipe gestures (gauche/droite pour naviguer)
- Touch-optimized buttons
- Responsive images
- Orientation portrait/paysage

**Estimation:** 5-6h

---

### 7. 🌙 Mode Sombre Complet
**Objectif:** Support du dark mode

**Fonctionnalités:**
- Toggle dans paramètres
- Sauvegarde préférence
- Tous les composants adaptés
- Variantes Tailwind dark:

**Estimation:** 2-3h

---

### 8. 👥 Collaboration Multi-utilisateur
**Objectif:** Partager sa collection

**Fonctionnalités:**
- Comptes utilisateur (authentification)
- Partage de collections
- Historique qui a fait quoi
- Permissions (lecture/édition)

**Détails Techniques:**
- Backend: JWT authentication
- Modèle: Users + Collections + Sharing permissions
- Frontend: Login/Register pages

**Estimation:** 8-10h

---

### 9. 🔄 Synchronisation Cloud
**Objectif:** Sauvegarder en cloud

**Fonctionnalités:**
- Sauvegarde automatique
- Sync multi-appareils
- Backup/restore
- Versionning des modifications

**Estimation:** 10-12h

---

### 10. 🌐 Intégrations Externes
**Objectif:** Connecter à d'autres services

**Fonctionnalités:**
- Météo locale pour recommandations
- Import Google Calendar
- Export vers Notion/Trello
- IFTTT workflows

**Estimation:** 6-8h par intégration

---

## 🚀 Recommandation Ordre de Priorité

```
Semaine 1:  📅 Calendrier + 🔔 Alertes (RAPIDE ET UTILE)
Semaine 2:  📊 Export + 🔍 Recherche (PRODUCTIVITÉ)
Semaine 3:  🎨 Vues perso + 🌙 Dark mode (CONFORT)
Semaine 4+: 📱 Mobile + 👥 Multi-user (ÉVOLUTION)
```

---

## 📝 Notes Techniques

### Technologies Recommandées:
- **Calendrier:** `react-big-calendar` ou `fullcalendar`
- **Export:** `papaparse`, `jspdf`, `html2canvas`
- **Recherche:** `fuse.js` (fuzzy search local) + Algolia (cloud optionnel)
- **Thème:** Tailwind CSS avec `next-themes` ou contexte custom
- **État global:** Context API (déjà utilisé)

### Architecture Backend à Préparer:
```
GET  /statistics/calendar           → Dates soins par mois
GET  /statistics/critical-plants    → Alertes urgentes
GET  /plants/search?q=...           → Recherche fuzzy
POST /export/csv                    → Export CSV
POST /export/pdf                    → Export PDF
```

### Métriques de Succès:
- Temps de recherche d'une plante < 2s
- Alertes affichées < 1s après chargement
- Export généré < 3s
- Calendrier charge < 1s
- Tous les tests E2E passent

---

## ✨ Vision Long Terme

L'objectif est de faire de cette app la **meilleure solution open-source pour gérer une collection de plantes**, avec:
- ✅ Tracking automatisé
- ✅ Recommandations intelligentes
- ✅ Communauté d'utilisateurs
- ✅ Intégrations avec services populaires
- ✅ Mobile-first experience

---

**Dernière mise à jour:** 9 Nov 2025
**Branche:** 2.20
**État:** Phase de consolidation complète ✅

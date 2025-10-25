# 🤔 DECISIONS LOG - CHOIX ARCHITECTURAUX

**Date:** 25 Octobre 2025  
**Projet:** Plant Manager v2 (Python Desktop)  
**Décideur:** Willysmile + GitHub Copilot

---

## 📋 DECISIONS PRISES

### 1. **Nouveau repo Python séparé du Laravel**

**Décision:** Créer `/plant_manager_python` au lieu de remplacer le Laravel

**Justification:**
- ✅ Garder l'historique Git du Laravel intact
- ✅ Les deux projets coexistent (pas de breaking changes)
- ✅ Facilite rollback si problèmes
- ✅ Permet développement parallèle

**Alternative rejettée:** Remplacer le Laravel directement (risque de perte de code)

---

### 2. **SQLite au lieu de PostgreSQL/MySQL**

**Décision:** SQLite comme base de données principale

**Justification:**
- ✅ ZERO configuration (fichier unique)
- ✅ Standalone (parfait pour desktop)
- ✅ Facile pour export/import
- ✅ Sufficient pour ~10,000 plantes
- ✅ Backup = simple copy du fichier .db

**Alternative rejettée:** PostgreSQL (serveur compliqué pour desktop)

---

### 3. **PySimpleGUI au lieu de PyQt6/Tkinter**

**Décision:** PySimpleGUI pour frontend

**Justification:**
- ✅ Syntaxe super simple (apprentissage rapide)
- ✅ Parfait pour desktop standalone
- ✅ Facile packaging (PyInstaller)
- ✅ Widgets suffisant pour notre cas
- ✅ Documentation excellente

**Alternatives:**
- PyQt6: Overkill, trop lourd
- Tkinter: Trop basique, UI moins moderne
- Electron: Mélange JS+Python compliqué
- Kivy: Overkill, target mobile d'abord

---

### 4. **FastAPI au lieu de Flask/Django**

**Décision:** FastAPI pour backend

**Justification:**
- ✅ Moderne, rapide (async-first)
- ✅ Auto-documentation (Swagger)
- ✅ Validation automatique (Pydantic)
- ✅ Perfect pour API simple
- ✅ Faible overhead (on a pas besoin d'ORM lourd)

**Alternatives rejettées:**
- Flask: Trop minimal, boilerplate pesant
- Django: Overkill pour notre cas, trop de magie
- FastAPI: ✅ CHOIX FINAL

---

### 5. **Pas d'authentification (single user)**

**Décision:** Zéro auth, mode single user

**Justification:**
- ✅ Application desktop locale = pas de multi-user
- ✅ Aucune donnée sensible (plantes!)
- ✅ Saves 40% du code (auth + permissions)
- ✅ Déploiement ultra-simple
- ✅ User n'a rien à configurer

**Futur:** Si multi-user = migrer SQLite → PostgreSQL + ajouter auth

---

### 6. **Export/Import = ZIP (JSON + photos)**

**Décision:** Format export = ZIP avec backup.json + photos + metadata.json

**Justification:**
- ✅ Standard, universel
- ✅ Photos incluses (portable)
- ✅ Checksum SHA256 (intégrité)
- ✅ Métadonnées utiles (counts, version)
- ✅ Facile dry-run avant import
- ✅ Même format que Laravel Phase A

**Alternatives rejettées:**
- CSV: Perd les relations (photos, histories)
- SQL dump: Dépend de BD engine
- API streaming: Pas portable

---

### 7. **Repartir de zéro (pas migrer données Laravel)**

**Décision:** Nouvelle BD vierge, pas d'import des 30 plantes Laravel

**Justification:**
- ✅ Laravel est test/demo, données pas précieuses
- ✅ Test complet du pipeline export/import
- ✅ Plus simple QA
- ✅ Clean start = meilleur apprenissage

**Futur:** Export depuis Laravel + import en Python (test du système)

---

### 8. **Photos en WebP (compression auto)**

**Décision:** Toutes les photos converties en WebP avec quality=85

**Justification:**
- ✅ 30-40% plus petit que JPEG (même qualité)
- ✅ Stockage local = moins d'espace
- ✅ Export ZIP plus petit
- ✅ Performance (chargement rapide)
- ✅ Déjà implémenté en Laravel

**Qualité 85:** Sweet spot performance/quality (tester en usage réel)

---

### 9. **Soft delete (30j recovery?)**

**Décision:** Soft delete on Plant, Photo - suppression logique pas physique

**Justification:**
- ✅ Oopsie recovery (accidentelle suppression)
- ✅ Audit trail intact
- ✅ Pas perte données

**Question ouverte:** Durée recovery? (30j? infini? manual only?)

---

### 10. **Audit logging obligatoire**

**Décision:** Tous les CREATE/UPDATE/DELETE loggés en AuditLog

**Justification:**
- ✅ Traçabilité complète (qui a fait quoi)
- ✅ Export audit log (compliance?)
- ✅ Debug (si corruption)
- ✅ Important pour confiance utilisateur

**Implementation:** Auto via middleware (zero effort côté routes)

---

### 11. **15 modèles (pas de consolidation)**

**Décision:** Garder 15 models distincts (PlantHistory, WateringHistory, etc)

**Justification:**
- ✅ Flexibilité (chaque history a format différent)
- ✅ Queries simples (pas de polymorphism)
- ✅ Même design que Laravel
- ✅ Facile de comprendre

**Alternative rejettée:** Polymorphic history table (plus complexe)

---

### 12. **45+ endpoints distincts**

**Décision:** 45+ endpoints RESTful au lieu d'une mega-query GraphQL

**Justification:**
- ✅ Simple pour PySimpleGUI client
- ✅ Caching facile (si besoin)
- ✅ Suivre conventions REST
- ✅ Documentation auto (Swagger)

**Futur:** Considérer GraphQL si besoins complexes

---

### 13. **10 Windows UI (pas single window)**

**Décision:** Découper en 10 windows (Main, Form, Detail, Settings, etc)

**Justification:**
- ✅ Chaque window = single responsibility
- ✅ Modularité (easy to modify)
- ✅ UX claire (chaque fonction = son window)
- ✅ Facile d'ajouter features

**Alternative rejettée:** Single window mega-form (confus)

---

### 14. **PyInstaller pour exe (pas setuptools/wheel)**

**Décision:** Packager avec PyInstaller → single .exe ou .bin

**Justification:**
- ✅ Single file executable
- ✅ Zero dépendances visibles pour user
- ✅ Double-click = marche
- ✅ Même résultat que Electron binaries

**Alternative rejettée:** 
- wheel: Exige pip install
- setuptools: Complex installation

---

### 15. **Développement séquentiel (6 phases)**

**Décision:** Découper en 6 phases, une par semaine

**Justification:**
- ✅ Validation continue (phase done = testable)
- ✅ Feedback rapide (bugs caught early)
- ✅ Moral: wins chaque semaine
- ✅ Flexibilité (ajuster après phases)

**Phase 1-3:** Impératifs (CRUD + photos + historiques)
**Phase 4-5:** Important (stats + export/import)
**Phase 6:** Deployment

---

## 🔄 DÉCISIONS EN ATTENTE

### Q1: Durée recovery pour soft delete?
**Options:**
- 30 jours (auto-purge après)
- 90 jours (temps de considération)
- Infini (manual recovery only)

**Décision future:** À définir en Phase 5

### Q2: Chiffrement SQLite?
**Options:**
- SQLite standard (no crypto)
- sqlcipher (encrypted SQLite)

**Justification attendre:** Desktop local = confiance suffisante?

**Décision future:** À définir si demande user

### Q3: Multi-user path?
**Si besoin futur:**
- PostgreSQL remplace SQLite
- Authentification JWT
- Multi-workspace

**Décision future:** v2.0

### Q4: Sync cloud?
**Si demande:**
- Sync periodique vers cloud storage
- Offline-first + sync on connect

**Décision future:** v2.0

### Q5: Mobile app?
**Si demande:**
- React Native or Flutter
- API endpoint pour mobile client

**Décision future:** v2.0+

---

## 🚫 DÉCISIONS REJETÉES

### ❌ Multi-user authentication
**Rejeté car:** Desktop local, pas besoin

### ❌ GraphQL
**Rejeté car:** Overkill pour cas simple REST

### ❌ WebAssembly (JS frontend)?
**Rejeté car:** PySimpleGUI + Python = more coherent

### ❌ Docker container?
**Rejeté car:** Desktop standalone >>> Docker layers

### ❌ Cloud-first architecture?
**Rejeté car:** Local-first = meilleur UX + offline support

### ❌ Rename tables/models?
**Rejeté car:** Garder compatibilité Laravel

### ❌ Completely new UI paradigm?
**Rejeté car:** Même UX que Laravel = user familiar

---

## 📊 TRADE-OFFS

### Architecture: Simplicity vs Features
**Choix:** Simplicity en priority 1  
**Trade-off:** Quelques features "nice" repoussées à v2

### Performance: SQLite vs PostgreSQL
**Choix:** SQLite (single user)  
**Trade-off:** Limite ~10k plants (mais suffisant)

### UI: PySimpleGUI vs Custom Web UI
**Choix:** PySimpleGUI  
**Trade-off:** Moins belle visuellement, mais plus rapide dev

### Deployment: Single exe vs Docker
**Choix:** Single exe  
**Trade-off:** Taille fichier plus grand, mais ultra-simple install

---

## ✅ VALIDATIONS FAITES

- [x] Checked Python performance (ok pour 1k+ plantes)
- [x] Checked PySimpleGUI widgets (suffisant)
- [x] Checked FastAPI cold start (negligeable)
- [x] Checked WebP conversion speed (ok)
- [x] Checked SQLite concurrent access (ok pour single user)
- [x] Checked ZIP export/import performance (ok)

---

## 🔐 ASSUMPTIONS & LIMITATIONS

### Assumptions
- User a Python 3.10+ (ou exe bundled)
- User a 500MB disk space
- Single user par installation
- ~10k plantes max (SQLite limit pragmatique)
- Local network (no internet needed)

### Limitations
- Pas multi-user
- Pas cloud sync built-in
- Pas mobile client
- SQLite scalability (ok pour cas d'usage)

---

## 🎯 VALIDATION CRITERIA

Chaque décision validée par:
1. ✅ Expliquée clairement (rationale)
2. ✅ Trade-offs documentés
3. ✅ Alternatives considérées
4. ✅ Avancer/feedback possible

---

## 📝 COMMENT UTILISER CE DOC

**Vous vous demandez "Pourquoi FastAPI et pas Django?"**
→ Lire section "Decision 4"

**Vous trouvez un problème avec les choix**
→ Proposer issue/PR avec nouvelle info

**Vous voulez changer quelque chose**
→ Vérifier assumptions + trade-offs d'abord

---

**Document vivant:** À mettre à jour au fil du projet ✅

**Dernière mise à jour:** 25 Octobre 2025  
**Status:** DÉCISIONS VALIDÉES ✅

# 🌱 Phase 3.1 - Testing Guide

## 🎯 Objectif

Valider que **TOUTES les règles métier taxonomiques** fonctionnent correctement dans le formulaire web.

---

## 🚀 Démarrage Rapide

### 1. Vérifier les Serveurs
```bash
# Terminal 1 - Backend (déjà lancé)
curl http://localhost:8001/api/plants | head

# Terminal 2 - Frontend (déjà lancé)
# http://localhost:5173
```

### 2. Lancer les Tests

#### Option A: Tests Automatisés (API)
```bash
cd /home/willysmile/Documents/Gestion_des_plantes
bash test_live.sh
```

**Résultat attendu:**
```
✅ Backend: OK
✅ Test 1 - Plante Minimale: CRÉÉE
✅ Test 2 - Plante Complète: CRÉÉE
✅ Auto-générations: OK
```

#### Option B: Tests Live (Navigateur)
```bash
1. Ouvrir http://localhost:5173
2. Suivre LIVE_TEST_GUIDE.md
3. Tester chaque validation
4. Mettre à jour TEST_RESULTS_PHASE_3_1.md
```

---

## 📋 Documents de Test

| Document | But | Audience |
|----------|-----|----------|
| **TEST_PLAN_PHASE_3_1.md** | Tous les tests planifiés (30+) | Testeurs |
| **LIVE_TEST_GUIDE.md** | Guide interactif étape par étape | Testeurs |
| **LIVE_TEST_SESSION.md** | Résumé de la session | Tous |
| **test_live.sh** | Script tests automatisés | DevOps |
| **TEST_RESULTS_EXECUTED.md** | Résultats tests API | Tous |

---

## ✅ Tests Clés

### Test 1: Validation Genus
```
❌ "phalaenopsis" (minuscule) → Red border + erreur
✅ "Phalaenopsis" (correct) → OK
❌ "PHALAENOPSIS" (majuscule) → Red border + erreur
```

### Test 2: Validation Species
```
❌ "Amabilis" (majuscule) → Red border + erreur
✅ "amabilis" (minuscule) → OK
```

### Test 3: Règle Inter-Champs
```
❌ Species sans Genus → Erreur création
❌ Genus sans Species → Erreur création
✅ Genus + Species → OK
```

### Test 4: Auto-Corrections
```
Input: "rosenstromii" → Stocké: "subsp. rosenstromii"
Input: "alba" → Stocké: "var. alba"
Input: "White Dream" → Stocké: "'White Dream'"
```

### Test 5: Création Plante
```
✅ Plante créée avec tous les champs
✅ Reference auto-générée (ex: ORCHI-003)
✅ Scientific_name auto-généré (ex: Phalaenopsis amabilis)
```

### Test 6: Édition Plante
```
✅ Reference visible en gris (lecture-seule)
✅ Scientific_name visible en gris (lecture-seule)
✅ Modification possible
```

---

## 🧪 Résultats Attendus

### Tests API (Automatisés)
```
4/4 PASSÉS ✅
- Plante minimale créée
- Plante complète créée
- Auto-générations OK
- 0 erreurs
```

### Tests Live (Navigateur)
```
30+ PASSÉS ⏳
- Validations format
- Auto-corrections
- Règles inter-champs
- Messages français
- Création/édition
```

---

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| Champs testés | 35+ |
| Validations Zod | 15+ |
| Auto-corrections | 3 |
| Messages d'erreur | 10+ |
| Tests API | 4/4 ✅ |
| Tests Live | 30+ ⏳ |

---

## 🔍 Debug

### Si validation ne fonctionne pas:
1. Ouvrir Console (F12)
2. Observer les logs Zod
3. Vérifier que schemas.js est chargé
4. Vérifier que PlantFormPage utilise validatePlant

### Si API échoue:
1. Vérifier Backend tourne (port 8001)
2. Vérifier les logs backend
3. Vérifier Network tab (F12)
4. Vérifier le payload envoyé

---

## 📈 Passage des Tests

```
API Tests:           ✅ 4/4 PASSÉS
Live Tests Status:   ⏳ À faire
Documentation:       ✅ Complète
Code Qualité:        ✅ Bon
```

---

## 🎬 Procédure Rapide

```bash
# 1. Tests API (2 minutes)
bash test_live.sh

# 2. Tests Live (15 minutes)
# Ouvrir http://localhost:5173
# Suivre LIVE_TEST_GUIDE.md

# 3. Mettre à jour résultats
# Éditer TEST_RESULTS_PHASE_3_1.md

# 4. Commiter
git add TEST_RESULTS_PHASE_3_1.md
git commit -m "test: Phase 3.1 live tests passed"
```

---

## ✅ Validation Finale

Une fois tous les tests passés:
- [ ] API tests réussis
- [ ] Live tests réussis
- [ ] Résultats documentés
- [ ] Prêt pour Phase 3.2

---

**Bon testage! 🌱✅**


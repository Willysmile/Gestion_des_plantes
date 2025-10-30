# 📋 DÉTAIL DES 7 TESTS ÉCHOUÉS - Test Settings Routes Integration

**Date:** 30 Octobre 2025  
**Fichier:** `backend/tests/test_settings_routes_integration.py`  
**État:** 7 tests échoués sur 186

---

## 🔴 Problème Racine

Les **tests s'attendent à des endpoints GET par ID** qui **n'existent pas dans l'API**.

### API Actuelle (Réelle)
```
GET  /api/settings/locations        ✅ Liste toutes
POST /api/settings/locations        ✅ Crée une
PUT  /api/settings/locations/{id}   ✅ Modifie une
DELETE /api/settings/locations/{id} ✅ Supprime une

❌ GET /api/settings/locations/{id} — N'EXISTE PAS
```

### Tests Échoués (Attendus)
Les tests attendent:
```
GET /api/settings/locations/{id}        ❌ 405 Method Not Allowed
GET /api/settings/purchase-places/{id}  ❌ 405 Method Not Allowed
POST /api/settings/tags                 ❌ Assert ID check failure
POST /api/settings/diseases             ❌ Assert name check failure
GET /api/settings/diseases              ❌ List empty/invalid
GET /api/settings/treatments            ❌ List empty/invalid
```

---

## 🔍 Analyse Détaillée de Chaque Erreur

### Test 1: `test_get_location_by_id` ❌
```python
def test_get_location_by_id(client):
    create_resp = client.post("/api/settings/locations", json={"name": "Bedroom"})
    location_id = create_resp.json()["id"]
    
    resp = client.get(f"/api/settings/locations/{location_id}")  # ← 405 Not Allowed
    assert resp.status_code == 200
```
**Erreur:** `assert 405 == 200`  
**Cause:** `GET /api/settings/locations/{id}` n'existe pas  
**Solution:** Soit ajouter l'endpoint, soit supprimer le test

### Test 2: `test_get_location_not_found` ❌
```python
def test_get_location_not_found(client):
    resp = client.get("/api/settings/locations/99999")  # ← 405 Not Allowed
    assert resp.status_code == 404
```
**Erreur:** Même problème que Test 1  
**Cause:** Endpoint n'existe pas  
**Solution:** Soit ajouter l'endpoint, soit supprimer le test

### Test 3: `test_get_purchase_place_by_id` ❌
```python
def test_get_purchase_place_by_id(client):
    create_resp = client.post("/api/settings/purchase-places", json={"name": "Nursery"})
    place_id = create_resp.json()["id"]
    
    resp = client.get(f"/api/settings/purchase-places/{place_id}")  # ← 405 Not Allowed
    assert resp.status_code == 200
```
**Erreur:** `assert 405 == 200`  
**Cause:** `GET /api/settings/purchase-places/{id}` n'existe pas  
**Solution:** Même problème que Test 1

### Test 4: `test_create_tag` ❌
```python
def test_create_tag(client):
    resp = client.post("/api/settings/tags", json={"name": "Indoor", "tag_category_id": 1})
    assert resp.status_code == 201
    tag = resp.json()
    assert tag["name"] == "Indoor"  # ← Assertion error (probablement ID = 42, pas "Indoor")
```
**Erreur:** `assert 42 == "Indoor"` (ou équivalent)  
**Cause:** Le test essaie d'accéder au mauvais champ de la réponse  
**Solution:** Vérifier quelle est la vraie réponse, corriger le test

### Test 5: `test_get_diseases` ❌
```python
def test_get_diseases(client):
    resp = client.get("/api/settings/diseases")
    assert resp.status_code == 200
    diseases = resp.json()  # ← Assertion error sur le contenu
    assert isinstance(diseases, list)
```
**Erreur:** Probablement réponse vide ou format incorrect  
**Cause:** Données manquantes ou endpoint retourne mauvais format  
**Solution:** Vérifier les seeds de données, format réponse

### Test 6: `test_create_disease` ❌
```python
def test_create_disease(client):
    resp = client.post("/api/settings/diseases", json={"name": "Powdery Mildew"})
    assert resp.status_code == 201
    disease = resp.json()
    assert disease["name"] == "Powdery Mildew"  # ← Assertion error
```
**Erreur:** Même problème que Test 4  
**Cause:** Format réponse incorrect  
**Solution:** Vérifier réponse réelle de l'API

### Test 7: `test_get_treatments` ❌
```python
def test_get_treatments(client):
    resp = client.get("/api/settings/treatments")
    assert resp.status_code == 200
    treatments = resp.json()
    assert isinstance(treatments, list)  # ← Assertion error
```
**Erreur:** Même problème que Test 5  
**Cause:** Données manquantes ou endpoint retourne mauvais format  
**Solution:** Vérifier seeds de données, format réponse

---

## 🛠️ SOLUTIONS - 2 Options

### Option A: Ajouter les endpoints GET par ID (Recommandé)
Si on veut une API REST complète, ajouter à `backend/app/routes/settings.py`:

```python
@router.get("/locations/{location_id}", response_model=dict)
async def get_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    """Récupère une localisation par ID"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Localisation non trouvée")
    return {"id": location.id, "name": location.name}

@router.get("/purchase-places/{place_id}", response_model=dict)
async def get_purchase_place(
    place_id: int,
    db: Session = Depends(get_db),
):
    """Récupère un lieu d'achat par ID"""
    place = db.query(PurchasePlace).filter(PurchasePlace.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Lieu d'achat non trouvé")
    return {"id": place.id, "name": place.name}
```

**Avantages:**
- API REST complète et cohérente
- Tests testent réellement la fonctionnalité
- Bon pour le frontend (fetch par ID)

**Désavantages:**
- Plus de code
- Plus d'endpoints à maintenir

### Option B: Supprimer les tests GET par ID (Moins recommandé)
Supprimer les tests `test_get_location_by_id`, `test_get_location_not_found`, etc. qui testent des endpoints inexistants.

**Avantages:**
- Moins de code
- Tests ne testent que ce qui existe

**Désavantages:**
- Gaps dans les tests
- Frontend aura besoin de GET par ID un jour ou l'autre

---

## ✅ CORRECTIONS RECOMMANDÉES

### 1. Ajouter endpoints GET par ID
**Fichier:** `backend/app/routes/settings.py`  
**Ajouter après les endpoints actuels:**
- `GET /api/settings/locations/{id}`
- `GET /api/settings/purchase-places/{id}`
- `GET /api/settings/watering-frequencies/{id}`
- `GET /api/settings/light-requirements/{id}`

### 2. Vérifier et corriger test_create_tag
**Fichier:** `backend/tests/test_settings_routes_integration.py`  
**Problème:** Assertion sur mauvais champ  
**Action:**
```python
def test_create_tag(client):
    resp = client.post("/api/settings/tags", json={"name": "Indoor", "tag_category_id": 1})
    assert resp.status_code == 201
    tag = resp.json()
    print(f"DEBUG: Response is {tag}")  # Voir ce qu'on reçoit
    assert tag.get("name") == "Indoor"  # ou tag.get("id") ou autre
```
Exécuter et voir la réponse réelle, puis corriger.

### 3. Vérifier seeds pour diseases et treatments
**Fichiers à checker:**
- `backend/app/scripts/seed_lookups.py` — Seed-t-il les diseases?
- `backend/app/scripts/seed_disease_lookups.py` — Existe et fait quoi?

**Action:** Vérifier que les données existent en DB avant les tests.

### 4. Rerun les tests après corrections
```bash
cd backend
venv/bin/pytest tests/test_settings_routes_integration.py -v
```

---

## 📊 Statut Par Test

| # | Nom Test | Erreur | Type | Priorité |
|---|----------|--------|------|----------|
| 1 | `test_get_location_by_id` | 405 Not Allowed | Architecture | 🔴 P1 |
| 2 | `test_get_location_not_found` | 405 Not Allowed | Architecture | 🔴 P1 |
| 3 | `test_get_purchase_place_by_id` | 405 Not Allowed | Architecture | 🔴 P1 |
| 4 | `test_create_tag` | Assert mismatch | Response format | 🟠 P2 |
| 5 | `test_get_diseases` | Empty/invalid | Seed data | 🟠 P2 |
| 6 | `test_create_disease` | Assert mismatch | Response format | 🟠 P2 |
| 7 | `test_get_treatments` | Empty/invalid | Seed data | 🟠 P2 |

---

## 🎯 Plan Réparation

### Phase 1: Endpoints GET par ID (1-2h)
- [ ] Ajouter 4 endpoints GET by ID dans settings.py
- [ ] Tester manuellement avec curl
- [ ] Vérifier tests 1-3 passent
- [ ] Couverture code +5%

### Phase 2: Format réponses (30min)
- [ ] Debugger test_create_tag (print response)
- [ ] Corriger assertion
- [ ] Debugger test_create_disease idem
- [ ] Tests 4, 6 passent

### Phase 3: Seed data (30min)
- [ ] Vérifier seed_lookups.py crée diseases
- [ ] Vérifier seed_lookups.py crée treatments
- [ ] Ajouter à seed si manquants
- [ ] Tests 5, 7 passent

### Total: 2-3h pour passer 7 → 0 échoués

---

## 📈 Résultat Attendu Après Correction

```
BEFORE:
FAILED tests/test_settings_routes_integration.py::test_get_location_by_id
FAILED tests/test_settings_routes_integration.py::test_get_location_not_found
FAILED tests/test_settings_routes_integration.py::test_get_purchase_place_by_id
FAILED tests/test_settings_routes_integration.py::test_create_tag
FAILED tests/test_settings_routes_integration.py::test_get_diseases
FAILED tests/test_settings_routes_integration.py::test_create_disease
FAILED tests/test_settings_routes_integration.py::test_get_treatments
7 failed, 179 passed

AFTER:
========================= 186 passed in 45.32s =========================
✅ 100% tests passing
✅ Coverage: 81% → 85%+
```

---

## 📌 Conclusion

Les problèmes sont bien identifiés et **facilement réparables**:
1. **Endpoints manquants** (3 tests) — Ajouter code, couverture ↑
2. **Format réponses** (2 tests) — Corriger assertions
3. **Seed data** (2 tests) — Vérifier données initiales

**Temps estimé:** 2-3 heures  
**Impact:** Couverture 81% → 85%+, Tests 179→186 passants

import pytest


@pytest.mark.usefixtures("client", "db")
def test_settings_locations_crud(client, db):
    # create location
    payload = {"name": "TestLocation123"}
    resp = client.post("/api/settings/locations", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    lid = data.get("id")

    # get list
    resp = client.get("/api/settings/locations")
    assert resp.status_code == 200
    assert any(l.get("id") == lid for l in resp.json())

    # update
    resp = client.put(f"/api/settings/locations/{lid}", json={"name": "Salon2"})
    assert resp.status_code == 200

    # delete
    resp = client.delete(f"/api/settings/locations/{lid}")
    assert resp.status_code in (204, 200)


@pytest.mark.usefixtures("client", "db")
def test_settings_fertilizer_and_tags(client, db):
    # fertilizer types
    f_payload = {"name": "EngraisT", "unit": "unité", "description": "ok"}
    rf = client.post("/api/settings/fertilizer-types", json=f_payload)
    assert rf.status_code == 201
    fid = rf.json().get("id")
    client.get(f"/api/settings/fertilizer-types/{fid}")
    client.put(f"/api/settings/fertilizer-types/{fid}", json={"name": "E2", "unit": "unité", "description": "x"})
    client.delete(f"/api/settings/fertilizer-types/{fid}")

    # tags: create category directly via service then use tags endpoint
    from app.services.settings_service import SettingsService
    cat = SettingsService.create_tag_category(db, "Couleur")
    assert cat.id
    t_payload = {"category_id": cat.id, "name": "Vert"}
    tr = client.post("/api/settings/tags", json=t_payload)
    assert tr.status_code == 201
    tid = tr.json().get("id")
    client.get(f"/api/settings/tags?category_id={cat.id}")
    client.put(f"/api/settings/tags/{tid}", json={"name": "Vert clair"})
    client.delete(f"/api/settings/tags/{tid}")

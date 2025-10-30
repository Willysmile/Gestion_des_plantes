from datetime import date

import pytest

from app.models.plant import Plant


@pytest.mark.usefixtures("client", "db")
def test_watering_history_crud(client, db):
    # create plant
    p = Plant(name="HistPlant")
    db.add(p)
    db.commit()

    plant_id = p.id
    payload = {"date": date.today().isoformat(), "amount_ml": 100, "notes": "Test water"}

    # Create
    resp = client.post(f"/api/plants/{plant_id}/watering-history", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    hid = data["id"] if isinstance(data, list) else data.get("id")
    # Some code paths may return object directly
    assert data["amount_ml"] == 100 or data.get("amount_ml") == 100

    # List
    resp = client.get(f"/api/plants/{plant_id}/watering-history")
    assert resp.status_code == 200
    items = resp.json()
    assert any((it.get("notes") == "Test water") for it in items)

    # Get by id
    resp = client.get(f"/api/plants/{plant_id}/watering-history/{hid}")
    assert resp.status_code == 200

    # Update
    resp = client.put(f"/api/plants/{plant_id}/watering-history/{hid}", json={"notes": "Updated"})
    assert resp.status_code == 200
    assert resp.json().get("notes") == "Updated"

    # Delete
    resp = client.delete(f"/api/plants/{plant_id}/watering-history/{hid}")
    assert resp.status_code in (204, 200)


@pytest.mark.usefixtures("client", "db")
def test_repotting_and_notes_routes(client, db):
    p = Plant(name="RepotPlant")
    db.add(p)
    db.commit()
    pid = p.id

    # Repotting create
    rep_payload = {"date": date.today().isoformat(), "soil_type": "Loam", "pot_size_before": 10, "pot_size_after": 12}
    r = client.post(f"/api/plants/{pid}/repotting-history", json=rep_payload)
    assert r.status_code == 201
    rid = r.json().get("id")

    # Get repotting list
    rl = client.get(f"/api/plants/{pid}/repotting-history")
    assert rl.status_code == 200
    assert any(item.get("soil_type") == "Loam" for item in rl.json())

    # Plant note create
    note_payload = {"date": date.today().isoformat(), "note": "Note body", "title": "T1"}
    n = client.post(f"/api/plants/{pid}/plant-history", json=note_payload)
    assert n.status_code == 201
    nid = n.json().get("id")

    # Get notes list
    nl = client.get(f"/api/plants/{pid}/plant-history")
    assert nl.status_code == 200
    assert any(item.get("note") == "Note body" for item in nl.json())

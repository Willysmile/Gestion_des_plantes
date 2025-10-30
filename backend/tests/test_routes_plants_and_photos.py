import io
from pathlib import Path
from PIL import Image


def make_test_jpeg_bytes():
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_plant_crud_and_archive_restore(client):
    # Create plant
    resp = client.post("/api/plants", json={"name": "Test Plant"})
    assert resp.status_code == 201
    data = resp.json()
    plant_id = data["id"] if isinstance(data, list) else data.get("id")
    assert plant_id is not None

    # List plants
    resp = client.get("/api/plants")
    assert resp.status_code == 200
    lst = resp.json()
    assert any(p["id"] == plant_id for p in lst)

    # Get plant by id
    resp = client.get(f"/api/plants/{plant_id}")
    assert resp.status_code == 200
    detail = resp.json()
    assert detail["name"] == "Test Plant"

    # Update plant
    resp = client.put(f"/api/plants/{plant_id}", json={"name": "Renamed"})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["name"] == "Renamed"

    # Archive
    resp = client.post(f"/api/plants/{plant_id}/archive")
    assert resp.status_code == 200
    archived = resp.json()
    assert archived["is_archived"] is True

    # Restore
    resp = client.post(f"/api/plants/{plant_id}/restore")
    assert resp.status_code == 200
    restored = resp.json()
    assert restored["is_archived"] is False

    # Regenerate reference (should work when family present)
    # First set family
    resp = client.put(f"/api/plants/{plant_id}", json={"family": "Araceae"})
    assert resp.status_code == 200
    resp = client.post(f"/api/plants/{plant_id}/regenerate-reference")
    assert resp.status_code == 200
    new_obj = resp.json()
    assert "reference" in new_obj

    # Delete (soft)
    resp = client.delete(f"/api/plants/{plant_id}")
    assert resp.status_code == 204

    # Now GET should 404
    resp = client.get(f"/api/plants/{plant_id}")
    assert resp.status_code == 404


def test_photo_upload_and_serve(client, tmp_path, monkeypatch):
    # Create a plant
    resp = client.post("/api/plants", json={"name": "Photo Plant"})
    assert resp.status_code == 201
    plant = resp.json()
    plant_id = plant.get("id")

    # Monkeypatch photos dir to tmp
    from app import config

    photos_dir = tmp_path / "photos_test"
    photos_dir.mkdir()
    monkeypatch.setattr(config.settings, "PHOTOS_DIR", photos_dir)

    # Prepare a small jpeg bytes
    img_bytes = make_test_jpeg_bytes()

    files = {"file": ("photo.jpg", img_bytes, "image/jpeg")}
    resp = client.post(f"/api/plants/{plant_id}/photos", files=files)
    assert resp.status_code == 201
    up = resp.json()
    assert "id" in up
    filename = up.get("filename")

    # List photos
    resp = client.get(f"/api/plants/{plant_id}/photos")
    assert resp.status_code == 200
    photos = resp.json()
    assert any(p["filename"] == filename for p in photos)

    # Serve file (files router)
    resp = client.get(f"/api/photos/{plant_id}/{filename}")
    assert resp.status_code == 200
    assert resp.headers.get("content-type") == "image/webp"

    # Set primary via route
    pid = photos[0]["id"]
    resp = client.put(f"/api/plants/{plant_id}/photos/{pid}/set-primary")
    assert resp.status_code == 200
    obj = resp.json()
    assert obj["is_primary"] is True

    # Delete photo
    resp = client.delete(f"/api/plants/{plant_id}/photos/{pid}")
    assert resp.status_code == 204

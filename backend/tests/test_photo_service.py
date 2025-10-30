import os
from pathlib import Path
from io import BytesIO
import shutil

import pytest
from PIL import Image

from app.services.photo_service import PhotoService
from app.config import settings
from app.models.photo import Photo


def make_test_image_bytes(format="JPEG", size=(800, 600), color=(100, 150, 200)):
    img = Image.new("RGB", size, color)
    buf = BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_validate_file_rejects_non_image():
    data = b"this is not an image"
    valid, msg = PhotoService._validate_file(data)
    assert not valid
    assert "Fichier invalide" in msg or "cannot identify" in msg.lower()


def test_validate_file_too_large():
    big = b"0" * (PhotoService.MAX_FILE_SIZE * 2 + 1)
    valid, msg = PhotoService._validate_file(big)
    assert not valid
    assert "trop volumineux" in msg.lower()


def test_convert_and_compress_roundtrip():
    img_bytes = make_test_image_bytes(format="PNG")
    img = Image.open(BytesIO(img_bytes))
    webp = PhotoService._convert_to_webp(img, quality=75)
    assert isinstance(webp, (bytes, bytearray))
    assert len(webp) > 0


def test_convert_with_transparency():
    # Create an RGBA image (with alpha) to exercise transparency handling
    img = Image.new("RGBA", (200, 200), (255, 0, 0, 128))
    webp = PhotoService._convert_to_webp(img, quality=80)
    assert isinstance(webp, (bytes, bytearray))
    assert len(webp) > 0


def test_compress_to_target_small_size():
    # Create a reasonably large JPEG and ask for very small target to force compression/resizing
    img_bytes = make_test_image_bytes(format="JPEG", size=(1600, 1200))
    out = PhotoService._compress_to_target(img_bytes, target_size=1000)
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0


@pytest.mark.usefixtures("db")
def test_process_upload_success_and_file_creation(tmp_path, db):
    # point photos dir to tmp
    original = settings.PHOTOS_DIR
    try:
        settings.PHOTOS_DIR = Path(tmp_path)
        plant_id = 42
        img_bytes = make_test_image_bytes(format="JPEG", size=(1200, 900))

        ok, photo_obj, msg = PhotoService.process_upload(plant_id, img_bytes, "test.jpg", db)
        assert ok is True
        assert photo_obj is not None
        assert "upload" in msg.lower() or "succ" in msg.lower()

        # Files exist
        file_path = settings.PHOTOS_DIR / str(plant_id) / photo_obj.filename
        thumb_path = settings.PHOTOS_DIR / str(plant_id) / "thumbs" / photo_obj.filename
        assert file_path.exists()
        assert thumb_path.exists()

        # DB record
        db_photo = db.query(Photo).filter(Photo.id == photo_obj.id).first()
        assert db_photo is not None
        assert db_photo.is_primary is True
    finally:
        settings.PHOTOS_DIR = original


@pytest.mark.usefixtures("db")
def test_process_upload_quota_exceeded(tmp_path, db):
    original = settings.PHOTOS_DIR
    try:
        settings.PHOTOS_DIR = Path(tmp_path)
        plant_id = 99
        plant_dir = settings.PHOTOS_DIR / str(plant_id)
        plant_dir.mkdir(parents=True)
        # create fake large webp files to exceed quota
        thumbs = plant_dir / "thumbs"
        thumbs.mkdir()
        # create files totaling > MAX_TOTAL_PER_PLANT
        big_size = PhotoService.MAX_TOTAL_PER_PLANT + 1000
        f = plant_dir / "existing.webp"
        with open(f, "wb") as fh:
            fh.write(b"0" * big_size)

        img_bytes = make_test_image_bytes(format="JPEG")
        ok, photo_obj, msg = PhotoService.process_upload(plant_id, img_bytes, "t.jpg", db)
        assert ok is False
        assert "Quota" in msg or "Quota" in msg.capitalize() or "Quota" in msg
    finally:
        settings.PHOTOS_DIR = original


@pytest.mark.usefixtures("db")
def test_delete_and_set_main_photo(tmp_path, db):
    original = settings.PHOTOS_DIR
    try:
        settings.PHOTOS_DIR = Path(tmp_path)
        plant_id = 77
        img_bytes = make_test_image_bytes(format="JPEG")

        # upload first
        ok1, photo1, _ = PhotoService.process_upload(plant_id, img_bytes, "a.jpg", db)
        assert ok1
        # upload second
        ok2, photo2, _ = PhotoService.process_upload(plant_id, img_bytes, "b.jpg", db)
        assert ok2

        # By default first is primary
        p1 = db.query(Photo).filter(Photo.id == photo1.id).first()
        p2 = db.query(Photo).filter(Photo.id == photo2.id).first()
        assert p1.is_primary or p2.is_primary

        # set second as main
        PhotoService.set_main_photo(db, photo2.id, plant_id)
        p1 = db.query(Photo).filter(Photo.id == photo1.id).first()
        p2 = db.query(Photo).filter(Photo.id == photo2.id).first()
        assert p2.is_primary is True
        assert p1.is_primary is False

        # delete second
        result = PhotoService.delete_photo(db, photo2.id, plant_id)
        assert result is True
        # ensure file removed
        path2 = PhotoService.get_file_path(p2)
        thumb2 = PhotoService.get_thumbnail_path(p2)
        assert not path2.exists()
        assert not thumb2.exists()

    finally:
        settings.PHOTOS_DIR = original

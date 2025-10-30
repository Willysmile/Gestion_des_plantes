import io
from pathlib import Path
from PIL import Image
import tempfile

import pytest

from app.utils import image_processor
from app.config import settings


def create_image_bytes(format="PNG", size=(100, 100), color=(255, 0, 0)):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color)
    img.save(buf, format=format)
    return buf.getvalue()


def test_validate_image_upload_valid():
    data = create_image_bytes("PNG")
    res = image_processor.validate_image_upload(data, "test.png")
    assert res["valid"] is True
    assert res["mime_type"] == "image/png"


def test_validate_image_upload_too_large():
    # Create bytes larger than MAX_UPLOAD_SIZE
    big = b"0" * (image_processor.MAX_UPLOAD_SIZE + 1)
    res = image_processor.validate_image_upload(big, "big.png")
    assert res["valid"] is False
    assert "exceeds" in res["error"]


def test_process_image_and_delete_files(monkeypatch, tmp_path):
    # Point PHOTOS_DIR to a temporary directory
    monkeypatch.setattr(settings, "PHOTOS_DIR", Path(tmp_path))

    data = create_image_bytes("JPEG", size=(800, 600))

    # Process to webp
    out = image_processor.process_image_to_webp(data, plant_id=42, photo_id=7)
    assert out["success"] is True
    files = out["files"]
    assert "large" in files and "medium" in files and "thumbnail" in files

    # Check files exist on disk
    plant_dir = Path(tmp_path) / "42"
    for v in files.values():
        filepath = plant_dir / v["filename"]
        assert filepath.exists()

    # Delete by pattern (no filename given)
    deleted = image_processor.delete_photo_files(plant_id=42, photo_id=7)
    assert deleted is True

    # Directory should be removed
    assert not plant_dir.exists()

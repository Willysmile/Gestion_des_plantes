import pytest

from app.services.settings_service import SettingsService


@pytest.mark.usefixtures("db")
def test_location_crud(db):
    # Create
    loc = SettingsService.create_location(db, "Salon")
    assert loc.id is not None
    assert loc.name == "Salon"

    # Get
    fetched = SettingsService.get_location(db, loc.id)
    assert fetched is not None
    assert fetched.name == "Salon"

    # Update
    updated = SettingsService.update_location(db, loc.id, "Salon Modifié")
    assert updated is not None
    assert updated.name == "Salon Modifié"

    # Delete
    deleted = SettingsService.delete_location(db, loc.id)
    assert deleted is True
    assert SettingsService.get_location(db, loc.id) is None


@pytest.mark.usefixtures("db")
def test_purchase_place_crud(db):
    place = SettingsService.create_purchase_place(db, "Jardinerie")
    assert place.id is not None
    assert place.name == "Jardinerie"

    got = SettingsService.get_purchase_place(db, place.id)
    assert got is not None

    updated = SettingsService.update_purchase_place(db, place.id, "Magasin")
    assert updated.name == "Magasin"

    assert SettingsService.delete_purchase_place(db, place.id) is True
    assert SettingsService.get_purchase_place(db, place.id) is None


@pytest.mark.usefixtures("db")
def test_watering_frequency_crud(db):
    freq = SettingsService.create_watering_frequency(db, "Hebdo", 7)
    assert freq.id is not None
    assert freq.days_interval == 7

    all_freqs = SettingsService.get_watering_frequencies(db)
    assert any(f.id == freq.id for f in all_freqs)

    updated = SettingsService.update_watering_frequency(db, freq.id, "Bihebdo", 14)
    assert updated.days_interval == 14

    assert SettingsService.delete_watering_frequency(db, freq.id) is True
    assert SettingsService.get_watering_frequency(db, freq.id) is None


@pytest.mark.usefixtures("db")
def test_light_requirement_crud(db):
    lr = SettingsService.create_light_requirement(db, "Plein soleil")
    assert lr.id is not None

    all_lr = SettingsService.get_light_requirements(db)
    assert any(r.id == lr.id for r in all_lr)

    updated = SettingsService.update_light_requirement(db, lr.id, "Mi-ombre")
    assert updated.name == "Mi-ombre"

    assert SettingsService.delete_light_requirement(db, lr.id) is True


@pytest.mark.usefixtures("db")
def test_fertilizer_type_crud(db):
    ft = SettingsService.create_fertilizer_type(db, "Engrais A", unit="unité", description="Test")
    assert ft.id is not None
    assert ft.unit == "unité"

    all_ft = SettingsService.get_fertilizer_types(db)
    assert any(f.id == ft.id for f in all_ft)

    updated = SettingsService.update_fertilizer_type(db, ft.id, "Engrais B", unit="ml", description=None)
    assert updated.name == "Engrais B"
    assert updated.unit == "ml"

    assert SettingsService.delete_fertilizer_type(db, ft.id) is True


@pytest.mark.usefixtures("db")
def test_tag_category_and_tag_crud(db):
    cat = SettingsService.create_tag_category(db, "Couleur")
    assert cat.id is not None

    tag = SettingsService.create_tag(db, cat.id, "Vert")
    assert tag is not None
    assert tag.name == "Vert"

    tags = SettingsService.get_tags(db, category_id=cat.id)
    assert any(t.id == tag.id for t in tags)

    updated_tag = SettingsService.update_tag(db, tag.id, "Vert clair")
    assert updated_tag.name == "Vert clair"

    assert SettingsService.delete_tag(db, tag.id) is True
    assert SettingsService.delete_tag_category(db, cat.id) is True


@pytest.mark.usefixtures("db")
def test_get_disease_types_empty(db):
    # Should return empty list when none seeded
    dt = SettingsService.get_disease_types(db)
    assert isinstance(dt, list)
    assert dt == []

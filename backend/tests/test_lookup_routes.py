import pytest


def test_get_lookup_collections_empty(client):
    endpoints = [
        "/api/lookups/units",
        "/api/lookups/disease-types",
        "/api/lookups/treatment-types",
        "/api/lookups/plant-health-statuses",
        "/api/lookups/fertilizer-types",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


@pytest.mark.parametrize("path", [
    "/api/lookups/units/1",
    "/api/lookups/disease-types/1",
    "/api/lookups/treatment-types/1",
    "/api/lookups/plant-health-statuses/1",
    "/api/lookups/fertilizer-types/1",
])
def test_get_lookup_by_id_not_found(client, path):
    if "fertilizer-types" in path:
        # This route expects DELETE/PUT for specific fertilizer ids
        resp = client.delete(path)
        assert resp.status_code == 404
    else:
        resp = client.get(path)
        assert resp.status_code == 404

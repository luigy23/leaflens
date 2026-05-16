def test_list_species(client):
    resp = client.get("/api/species")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["count"] == 3
    common_names = {item["common_name"] for item in body["items"]}
    assert "Aloe Vera" in common_names


def test_search_species(client):
    resp = client.get("/api/species?q=pothos")
    assert resp.status_code == 200
    body = resp.get_json()
    assert any("Pothos" in item["common_name"] for item in body["items"])


def test_get_species_by_id(client):
    # First retrieve list to obtain a valid id
    items = client.get("/api/species").get_json()["items"]
    sp_id = items[0]["id"]
    resp = client.get(f"/api/species/{sp_id}")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["id"] == sp_id
    assert body["care"]["light_level"] == "bright-indirect"
    assert len(body["toxicity"]) == 2


def test_get_unknown_species(client):
    resp = client.get("/api/species/9999")
    assert resp.status_code == 404

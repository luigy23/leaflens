def test_health_returns_ok(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["status"] == "ok"
    assert body["model_name"] == "stub-classifier"
    assert body["num_classes"] == 47

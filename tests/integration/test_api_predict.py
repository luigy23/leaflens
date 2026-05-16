from __future__ import annotations

import io

from PIL import Image


def make_jpeg(width: int = 300, height: int = 300) -> bytes:
    img = Image.new("RGB", (width, height), color=(40, 120, 60))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


def test_predict_returns_topk(client):
    data = {
        "image": (io.BytesIO(make_jpeg()), "plant.jpg", "image/jpeg"),
    }
    resp = client.post("/api/predict", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    body = resp.get_json()
    assert len(body["topk"]) == 3
    assert body["topk"][0]["common_name"] == "Aloe Vera"
    assert body["topk"][0]["care"]["light_level"] == "bright-indirect"
    assert body["low_confidence"] is False


def test_predict_missing_image_returns_400(client):
    resp = client.post("/api/predict", data={}, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_predict_rejects_too_small(client):
    data = {
        "image": (io.BytesIO(make_jpeg(16, 16)), "tiny.jpg", "image/jpeg"),
    }
    resp = client.post("/api/predict", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_predict_rejects_unsupported_type(client):
    data = {
        "image": (io.BytesIO(b"not a real file"), "weird.txt", "text/plain"),
    }
    resp = client.post("/api/predict", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400

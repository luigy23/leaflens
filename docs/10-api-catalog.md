# 10. API Catalog

LeafLens exposes a small REST API served by Flask. All responses are JSON unless explicitly noted. CORS is enabled for the production frontend origin only.

Base URL (production): `https://leaflens-api.onrender.com`
Base URL (development): `http://localhost:5000`

## 10.1 Endpoint summary

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/health` | Liveness probe and model metadata. |
| `POST` | `/api/predict` | Identify a plant from an uploaded image. |
| `GET` | `/api/species` | List all known species. |
| `GET` | `/api/species/<id>` | Retrieve the full care card for one species. |

## 10.2 GET /api/health

Returns a 200 OK if the model is loaded and ready to serve.

### Response 200

```json
{
  "status": "ok",
  "model_name": "vit-base-patch16-224",
  "model_version": "1.0.0",
  "num_classes": 47,
  "loaded_at": "2026-05-15T19:30:00Z"
}
```

## 10.3 POST /api/predict

Identifies a plant from a single uploaded image.

### Request

- Content type: `multipart/form-data`
- Form field: `image` — the file to classify
- Optional query: `k` — number of top results to return (default 3, max 5)

```http
POST /api/predict?k=3 HTTP/1.1
Content-Type: multipart/form-data; boundary=----X

------X
Content-Disposition: form-data; name="image"; filename="plant.jpg"
Content-Type: image/jpeg

<binary>
------X--
```

### Response 200

```json
{
  "topk": [
    {
      "rank": 1,
      "species_id": 17,
      "scientific_name": "Epipremnum aureum",
      "common_name": "Golden Pothos",
      "confidence": 0.9241,
      "care": {
        "watering_days_min": 7,
        "watering_days_max": 10,
        "light_level": "bright-indirect",
        "temperature_min_c": 18,
        "temperature_max_c": 30,
        "humidity_pct": "40-60",
        "fertilizer_schedule": "monthly in spring and summer"
      },
      "toxicity": [
        { "animal": "cat", "level": "toxic", "notes": "calcium oxalate crystals" },
        { "animal": "dog", "level": "toxic", "notes": "calcium oxalate crystals" }
      ]
    },
    {
      "rank": 2,
      "species_id": 21,
      "scientific_name": "Philodendron hederaceum",
      "common_name": "Heartleaf Philodendron",
      "confidence": 0.0481,
      "care": { "..." : "..." },
      "toxicity": []
    },
    {
      "rank": 3,
      "species_id": 32,
      "scientific_name": "Scindapsus pictus",
      "common_name": "Satin Pothos",
      "confidence": 0.0205,
      "care": { "..." : "..." },
      "toxicity": []
    }
  ],
  "model_name": "vit-base-patch16-224",
  "latency_ms": 412,
  "low_confidence": false
}
```

### Errors

| Code | Reason | Body |
|---|---|---|
| 400 | No `image` field, unsupported content type, file too large, image dimensions too small | `{"error": "<message>"}` |
| 415 | Body is not `multipart/form-data` | `{"error": "expected multipart/form-data"}` |
| 500 | Internal error during inference | `{"error": "internal_error", "request_id": "..."}` |

## 10.4 GET /api/species

Returns the full catalog.

### Query parameters

- `q` — optional case-insensitive substring filter on common or scientific names.

### Response 200

```json
{
  "count": 47,
  "items": [
    { "id": 1,  "scientific_name": "Aloe vera",        "common_name": "Aloe Vera" },
    { "id": 2,  "scientific_name": "Anthurium andraeanum", "common_name": "Anthurium" },
    "..."
  ]
}
```

## 10.5 GET /api/species/{id}

Returns the full care card for a species, used for both the catalog detail page and as a building block for `/api/predict`.

### Response 200

```json
{
  "id": 17,
  "scientific_name": "Epipremnum aureum",
  "common_name": "Golden Pothos",
  "family": "Araceae",
  "origin": "Solomon Islands",
  "description": "A trailing vine with heart-shaped, often variegated leaves...",
  "image_url": "https://cdn.example.com/species/17.jpg",
  "care": {
    "watering_days_min": 7,
    "watering_days_max": 10,
    "light_level": "bright-indirect",
    "temperature_min_c": 18,
    "temperature_max_c": 30,
    "humidity_pct": "40-60",
    "fertilizer_schedule": "monthly in spring and summer"
  },
  "toxicity": [
    { "animal": "cat", "level": "toxic", "notes": "calcium oxalate crystals" },
    { "animal": "dog", "level": "toxic", "notes": "calcium oxalate crystals" }
  ]
}
```

### Errors

| Code | Reason |
|---|---|
| 404 | No species with that id |

## 10.6 Rate limits and quotas

A single deployed instance on Render free tier supports approximately 4 requests per second sustained. No authentication is required. A soft per-IP rate limit of 60 requests per minute is applied via `flask-limiter`; over-limit requests receive a `429 Too Many Requests`.

# 7. Data Dictionary & Entity-Relationship Model

## 7.1 Logical entities

LeafLens persists a small relational schema that backs the species catalog. The deep learning side of the system uses CSV manifests for reproducibility, separate from the database.

### Entities

| Entity | Purpose |
|---|---|
| `Species` | One row per botanical species recognized by the model. |
| `CareProfile` | One row per species describing watering, light, temperature, humidity, and fertilization. |
| `ToxicityRecord` | One row per (species, animal) pair indicating toxicity level. |
| `Prediction` | One row per inference request (optional analytics table, no images stored). |

### Relationships

- A `Species` has exactly one `CareProfile` (1:1).
- A `Species` has zero or more `ToxicityRecord` entries (1:N), typically two: one for cats and one for dogs.
- A `Prediction` references a `Species` as its top-1 result (N:1).

## 7.2 Entity-relationship diagram (textual)

```
+---------------------+        1     1   +-----------------------+
|      Species        |------------------|     CareProfile        |
+---------------------+                  +-----------------------+
| PK id               |                  | PK id                  |
|    scientific_name  |                  | FK species_id (unique) |
|    common_name      |                  |    watering_days_min   |
|    family           |                  |    watering_days_max   |
|    origin           |                  |    light_level         |
|    description      |                  |    temperature_min_c   |
|    image_url        |                  |    temperature_max_c   |
+---------------------+                  |    humidity_pct        |
        | 1                              |    fertilizer_schedule |
        | N                              +-----------------------+
+---------------------+
|   ToxicityRecord    |
+---------------------+
| PK id               |
| FK species_id       |
|    animal (enum)    |
|    level  (enum)    |
|    notes            |
+---------------------+

+---------------------+
|     Prediction      |
+---------------------+
| PK id               |
|    created_at       |
| FK top1_species_id  |
|    top1_confidence  |
|    top3_species_ids |
|    model_name       |
|    latency_ms       |
|    user_agent       |
+---------------------+
```

## 7.3 Data dictionary

### Table `species`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK, autoincrement | Internal identifier. |
| `scientific_name` | varchar(120) | not null, unique | Latin binomial, e.g. `Epipremnum aureum`. |
| `common_name` | varchar(120) | not null | Most common English name, e.g. `Golden Pothos`. |
| `family` | varchar(80) | nullable | Botanical family, e.g. `Araceae`. |
| `origin` | varchar(120) | nullable | Native region. |
| `description` | text | nullable | One-paragraph natural-language description. |
| `image_url` | varchar(255) | nullable | URL of a representative image. |
| `created_at` | timestamp | default now() | Row creation timestamp. |

### Table `care_profiles`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK | Internal identifier. |
| `species_id` | integer | FK → species.id, unique | One profile per species. |
| `watering_days_min` | integer | not null | Lower bound of watering interval in days. |
| `watering_days_max` | integer | not null | Upper bound of watering interval in days. |
| `light_level` | varchar(40) | not null | One of: `low`, `medium-indirect`, `bright-indirect`, `direct`. |
| `temperature_min_c` | integer | not null | Minimum tolerated temperature in Celsius. |
| `temperature_max_c` | integer | not null | Maximum tolerated temperature in Celsius. |
| `humidity_pct` | varchar(40) | nullable | Recommended humidity range as a string like `40-60`. |
| `fertilizer_schedule` | varchar(80) | nullable | Natural-language schedule, e.g. `monthly in spring and summer`. |

### Table `toxicity_records`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | integer | PK | Internal identifier. |
| `species_id` | integer | FK → species.id | Species this record applies to. |
| `animal` | varchar(10) | not null, enum(`cat`, `dog`) | Animal in question. |
| `level` | varchar(20) | not null, enum(`safe`, `mild`, `toxic`) | Toxicity level. |
| `notes` | varchar(255) | nullable | Symptom summary or source. |

### Table `predictions`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | bigint | PK | Internal identifier. |
| `created_at` | timestamp | default now() | When the prediction was made. |
| `top1_species_id` | integer | FK → species.id | Top-1 prediction. |
| `top1_confidence` | float | not null | Softmax probability of top-1. |
| `top3_species_ids` | int[] | not null | Array of three species ids. |
| `model_name` | varchar(40) | not null | Which model produced the prediction. |
| `latency_ms` | integer | not null | Server-side latency. |
| `user_agent` | varchar(255) | nullable | For client analytics only. |

> **Privacy note.** Uploaded images are never persisted. The `predictions` table records anonymous outcomes only.

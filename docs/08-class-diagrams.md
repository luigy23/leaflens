# 8. Class Diagrams

The system is organized into three layers: a **model layer** (PyTorch training and inference), a **service layer** (Flask backend with ORM and routing), and a **client layer** (React components and hooks). The class diagrams below describe the Python backend in detail; the React side is described separately because it follows a functional-component model.

## 8.1 Model layer

```
+-----------------------------+
|      PlantClassifier        |  <<abstract>>
+-----------------------------+
| - model: nn.Module          |
| - device: torch.device      |
| - class_names: list[str]    |
+-----------------------------+
| + load(path)                |
| + predict(image) -> Result  |
| + predict_topk(image, k)    |
+-----------------------------+
            ^
            |
+-----------+-----------+------------------+
|                       |                  |
+----------------+   +-------------+   +--------------+
| EfficientNetB0 |   |  ResNet50   |   |   ViTBase    |
+----------------+   +-------------+   +--------------+

+-----------------------------+
|     PredictionResult        |  <<dataclass>>
+-----------------------------+
| top1_id: int                |
| top1_name: str              |
| top1_confidence: float      |
| topk: list[(int, str, float)]|
| latency_ms: int             |
+-----------------------------+

+-----------------------------+
|     PlantImageDataset       |  <<extends torch.utils.data.Dataset>>
+-----------------------------+
| - manifest: pd.DataFrame    |
| - transform: Callable       |
+-----------------------------+
| + __len__()                 |
| + __getitem__(idx)          |
+-----------------------------+

+-----------------------------+
|       Trainer               |
+-----------------------------+
| - model: PlantClassifier    |
| - train_loader: DataLoader  |
| - val_loader: DataLoader    |
| - optimizer                 |
| - loss_fn                   |
| - device                    |
+-----------------------------+
| + train_one_epoch()         |
| + validate()                |
| + fit(epochs)               |
| + save_checkpoint(path)     |
+-----------------------------+
```

## 8.2 Service layer (Flask + SQLAlchemy)

```
+-------------------------+
|         App             |
+-------------------------+
| - flask: Flask          |
| - db: SQLAlchemy        |
| - classifier            |
+-------------------------+
| + create_app(config)    |
| + register_blueprints() |
+-------------------------+

+-------------------------+      uses      +--------------------+
|   PredictController     |--------------->|  PlantClassifier   |
+-------------------------+                +--------------------+
| + post_predict()        |
| + get_species(id)       |
| + list_species()        |
| + healthcheck()         |
+-------------------------+

ORM models (SQLAlchemy declarative):

+-----------------+        +--------------------+
|    Species      | 1----1 |   CareProfile      |
+-----------------+        +--------------------+
| id              |        | id                 |
| scientific_name |        | species_id (FK)    |
| common_name     |        | watering_days_min  |
| family          |        | watering_days_max  |
| origin          |        | light_level        |
| description     |        | temperature_min_c  |
| image_url       |        | temperature_max_c  |
+-----------------+        | humidity_pct       |
        | 1                | fertilizer_schedule|
        | N                +--------------------+
+-----------------+
| ToxicityRecord  |
+-----------------+
| id              |
| species_id (FK) |
| animal          |
| level           |
| notes           |
+-----------------+

+-----------------+
|   Prediction    |
+-----------------+
| id              |
| created_at      |
| top1_species_id |
| top1_confidence |
| top3_species_ids|
| model_name      |
| latency_ms      |
+-----------------+
```

## 8.3 Service layer responsibilities

- **`PredictController.post_predict`** — receives the multipart upload, validates content type and size, decodes the image with Pillow, forwards to `PlantClassifier.predict_topk(k=3)`, then enriches each candidate with its `Species` + `CareProfile` + toxicity records from the database. Persists a `Prediction` row for analytics.
- **`PredictController.list_species`** — returns the alphabetized catalog as a JSON array.
- **`PredictController.get_species`** — returns a full care card by species id.
- **`PredictController.healthcheck`** — returns a `200 OK` with model name and version.

## 8.4 Frontend component tree (React)

```
<App>
  ├── <Header />
  ├── <Router>
  │     ├── <HomePage>
  │     │     ├── <UploadDropzone />
  │     │     ├── <LoadingState />
  │     │     └── <ResultCard>
  │     │           ├── <Top1Banner />
  │     │           ├── <TopKAlternatives />
  │     │           └── <CareCard />
  │     │
  │     ├── <CatalogPage>
  │     │     └── <SpeciesGrid />
  │     │
  │     ├── <SpeciesDetailPage>
  │     │     └── <CareCard />
  │     │
  │     └── <AboutPage />
  └── <Footer />

Hooks:
  - usePrediction()    -> POST /api/predict
  - useCatalog()       -> GET  /api/species
  - useSpecies(id)     -> GET  /api/species/{id}
  - useLocalHistory()  -> read/write window.localStorage
```

# 12. Architecture

## 12.1 High-level architecture

LeafLens is a three-tier web application with an additional asynchronous training pipeline that runs offline. The runtime path is synchronous and short: upload → preprocess → infer → enrich → respond.

```
                    ┌──────────────────────────────────────────────┐
                    │            Browser (React SPA)               │
                    │  - Upload, history, catalog, about pages     │
                    │  - Tailwind, react-query, axios              │
                    └────────────────────┬─────────────────────────┘
                                         │ HTTPS / multipart
                                         ▼
                    ┌──────────────────────────────────────────────┐
                    │        Flask API (gunicorn + Render)         │
                    │  - /api/predict                              │
                    │  - /api/species, /api/species/<id>           │
                    │  - /api/health                               │
                    │  - flask-limiter, flask-cors                 │
                    └───────┬───────────────────────┬──────────────┘
                            │                       │
              SQLAlchemy ORM│                       │ PyTorch inference
                            ▼                       ▼
            ┌──────────────────────────┐  ┌──────────────────────────┐
            │   PostgreSQL (Render)    │  │   PyTorch model (ViT)    │
            │  - species               │  │   - loaded at boot       │
            │  - care_profiles         │  │   - MPS / CPU            │
            │  - toxicity_records      │  └──────────────────────────┘
            │  - predictions           │
            └──────────────────────────┘

                    ┌──────────────────────────────────────────────┐
                    │   Offline training pipeline (local laptop)   │
                    │   1. Kaggle download → data/raw              │
                    │   2. split_data.py → train/val/test CSV      │
                    │   3. train.py → checkpoints/                 │
                    │   4. evaluate.py → metrics + confusion mat   │
                    │   5. export best checkpoint → backend/       │
                    └──────────────────────────────────────────────┘
```

## 12.2 Component responsibilities

### Frontend (React)

- Single-page application bundled with Vite.
- Routing: `react-router-dom`.
- Data fetching: `axios` wrapped in `react-query` hooks (`usePrediction`, `useCatalog`, `useSpecies`).
- Styling: Tailwind CSS with a custom green palette.
- File upload: native `<input type="file" />` plus a drag-and-drop overlay; image preview generated from `URL.createObjectURL`.
- Local history: last ten predictions in `window.localStorage` keyed by ISO timestamp.

### Backend (Flask)

- Application factory pattern (`create_app(config)`) for testability.
- Blueprints: `predict`, `species`, `health`.
- ORM: SQLAlchemy with declarative models in `backend/db/models.py`.
- Model loading: a single `PlantClassifier` instance instantiated at application startup and held in `current_app.config["classifier"]`. Subsequent requests reuse it (no per-request cost).
- Input validation: `marshmallow` schemas guard request bodies and query strings.
- Rate limiting: `flask-limiter` with in-memory storage, 60 req/min per IP.
- Logging: structured JSON to stdout, captured by Render's log drain.

### Database (PostgreSQL)

- Managed PostgreSQL instance on Render free tier (1 GB storage).
- Migrations: `alembic`, with one initial migration that creates all four tables and seeds the species/care/toxicity rows from a YAML fixture.
- Connection pooling: SQLAlchemy default with `pool_size=5, max_overflow=10`.

### Model layer (PyTorch)

- Three architectures fine-tuned during training: EfficientNet-B0, ResNet-50, ViT-Base/16. Each backbone is initialized from torchvision/timm pretrained weights; the final classification head is replaced with a 47-way linear layer.
- The best checkpoint (selected on validation accuracy) is exported to `backend/model_artifacts/best.pt` along with the `class_names.json` mapping.
- At inference time the model runs on the CPU (Render free tier has no GPU). On the developer laptop the same code path uses the Metal Performance Shaders backend through `torch.device("mps")`.

## 12.3 Inference data flow (sequence)

```
Browser            Flask                Classifier            Database
   │                 │                       │                    │
   │ multipart POST  │                       │                    │
   ├────────────────▶│                       │                    │
   │                 │ validate & decode     │                    │
   │                 │ image                 │                    │
   │                 │                       │                    │
   │                 │ predict_topk(image,3) │                    │
   │                 ├──────────────────────▶│                    │
   │                 │   logits → softmax    │                    │
   │                 │◀──────────────────────┤                    │
   │                 │                       │                    │
   │                 │ SELECT species, care, toxicity for 3 ids   │
   │                 ├───────────────────────────────────────────▶│
   │                 │◀───────────────────────────────────────────┤
   │                 │                       │                    │
   │                 │ INSERT INTO predictions (analytics row)    │
   │                 ├───────────────────────────────────────────▶│
   │                 │                       │                    │
   │   JSON payload  │                       │                    │
   │◀────────────────┤                       │                    │
```

## 12.4 Deployment topology

| Component | Provider | Tier | Notes |
|---|---|---|---|
| Static frontend | Vercel | Hobby (free) | Built from `frontend/` on every push to `main`. |
| Backend API | Render | Free web service | Auto-deploys from `backend/` on every push to `main`. |
| Database | Render | Free PostgreSQL | 1 GB storage, sleeps after 90 days idle. |
| Model artifact | Bundled in backend Docker image | — | < 400 MB total image size. |

## 12.5 Configuration & secrets

- `.env.production` at the backend root, populated from Render's environment variables: `DATABASE_URL`, `SECRET_KEY`, `LOG_LEVEL`, `ALLOWED_ORIGINS`.
- Frontend reads `VITE_API_BASE_URL` from Vercel environment.
- No secret is ever committed to the repository; `.env*` is gitignored.

## 12.6 Scalability notes

The free tier is the only realistic constraint. The architecture as designed supports a single replica with one worker process; the model is shared in-memory and an inference takes around 400 ms on CPU. If the deployment ever needed to scale, the obvious moves are: (1) move inference to a queued worker, (2) cache the catalog endpoints in a CDN, (3) shard `predictions` writes. None of these are needed for the academic delivery.

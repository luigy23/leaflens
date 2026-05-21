# LeafLens — Folder Inventory

Everything for the AI final project lives inside this single folder:

```
~/Documents/GitHub/leaflens
```

Total size on disk: **~6.7 GB** (4.9 GB of that is the dataset).

This folder is **fully self-contained** — code, dataset, model checkpoints,
documentation, slides, and the database file. You can move it to an external
drive, hand it in, or zip it up without anything breaking.

---

## Top-level map

| Path | Size | What's in it |
|---|---|---|
| `README.md` | 7 KB | Public-facing readme with badges and quickstart |
| `INVENTORY.md` | this file | What lives where |
| `CLAUDE.md` | 3 KB | Engineering context (for future AI sessions) |
| `requirements.txt` | <1 KB | Pinned Python dependencies |
| `pytest.ini`, `Dockerfile`, `render.yaml`, `.env.example` | small | Config files |
| `.python-version` | <1 KB | Pins Python 3.13 for direnv / pyenv |
| `.github/workflows/ci.yml` | small | GitHub Actions CI (lint + tests) |
| `.gitignore` | <1 KB | What git ignores |
| **`data/`** | **4.9 GB** | The dataset (raw images + split manifests) |
| **`models/`** | **524 MB** | PyTorch architecture code + trained checkpoints |
| **`backend/`** | 172 KB | Flask API, ORM, curated species catalog YAML |
| **`frontend/`** | 76 MB | React + Vite app (most of it is node_modules) |
| **`docs/`** | 120 KB | 17-section English documentation set |
| **`presentation/`** | 8 MB | .pptx deck + HTML reveal.js deck + cheat sheet |
| **`scripts/`** | 36 KB | All utility scripts |
| **`tests/`** | 24 KB | Unit + integration tests |
| `notebooks/` | empty | For ad-hoc EDA, currently empty |
| `.venv/` | 1.2 GB | Python virtualenv with torch + flask + etc. |
| `.dev-logs/` | small | Backend and frontend stdout when running dev.sh |

---

## Where each thing is

### 📊 Dataset

```
data/
├── raw/
│   └── house_plant_species/        ← 14,774 images, 47 species folders
│       ├── African Violet (Saintpaulia ionantha)/
│       ├── Aloe Vera/
│       ├── Anthurium (Anthurium andraeanum)/
│       ├── ... (44 more)
│       └── ZZ Plant (Zamioculcas zamiifolia)/
└── processed/
    ├── train.csv                   ← 10,341 rows (70%)
    ├── val.csv                     ←  2,216 rows (15%)
    ├── test.csv                    ←  2,217 rows (15%)
    └── class_distribution.csv      ← per-class counts
```

> **Provenance.** Kaggle dataset `kacpergregorowicz/house-plant-species` version 4.
> Originally downloaded via `scripts/download_dataset.py` to the kagglehub cache
> at `~/.cache/kagglehub/...` and then copied into this folder for portability.

### 🧠 AI / models

```
models/
├── architectures.py                ← EfficientNet, ResNet50, ViT factories
├── dataset.py                      ← PyTorch Dataset + transforms
├── train.py                        ← Training loop
├── evaluate.py                     ← Test-set evaluation
├── inference.py                    ← PlantClassifier used by the API
├── __init__.py
└── checkpoints/
    ├── best.pt                     ← Deployed model (= resnet50_best.pt)
    ├── efficientnet_best.pt        ← EfficientNet-B0 checkpoint (16 MB)
    ├── resnet50_best.pt            ← ResNet-50 checkpoint (90 MB)
    ├── vit_best.pt                 ← ViT-Base checkpoint (327 MB, partial training)
    ├── *_best.eval.json            ← Per-architecture metrics (top-1, top-3, F1, confusion matrix)
    └── *_history.json              ← Per-epoch training history
```

### 🖥 Backend

```
backend/
├── app.py                          ← Flask application factory
├── wsgi.py                         ← gunicorn entrypoint
├── config.py                       ← Config classes (dev, test)
├── leaflens.db                     ← SQLite (47 species + 47 care + 94 toxicity records)
├── data/
│   └── species.yaml                ← Curated knowledge base (all 47 species)
├── db/
│   ├── models.py                   ← Species, CareProfile, ToxicityRecord, Prediction
│   ├── seed.py                     ← Idempotent YAML → DB seeder
│   └── __init__.py
└── routes/
    ├── health.py                   ← GET  /api/health
    ├── predict.py                  ← POST /api/predict
    └── species.py                  ← GET  /api/species, /api/species/<id>
```

### 🎨 Frontend

```
frontend/
├── package.json                    ← React 18 + Vite + Tailwind
├── vite.config.js                  ← Dev proxy to backend on port 5001
├── tailwind.config.js
├── postcss.config.js
├── index.html
├── public/leaf.svg                 ← Favicon
├── src/
│   ├── main.jsx                    ← Entry point
│   ├── App.jsx                     ← Router
│   ├── index.css                   ← Tailwind + custom CSS
│   ├── api/client.js               ← axios wrapper
│   ├── components/                 ← Header, Footer, UploadDropzone, ResultCard, CareCard, LoadingState
│   └── pages/                      ← HomePage, CatalogPage, SpeciesDetailPage, AboutPage
└── node_modules/                   ← Dependencies
```

### 📚 Documentation (17 sections in English)

```
docs/
├── 01-introduction.md
├── 02-problem.md
├── 03-objectives.md
├── 04-state-of-the-art.md
├── 05-requirements.md
├── 06-use-cases.md
├── 07-data-model.md
├── 08-class-diagrams.md
├── 09-mockups.md
├── 10-api-catalog.md
├── 11-testing.md
├── 12-architecture.md
├── 13-results.md                   ← Final metrics + ResNet-50 selection
├── 14-future-work.md
├── 15-presentation-outline.md      ← Slide-by-slide script
├── 16-deployment-guide.md          ← Render + Vercel walkthrough
└── 17-presentation-cheatsheet.md   ← Numbers + paths + Q&A for the defense
```

### 🎤 Presentation

```
presentation/
├── LeafLens.pptx                   ← PowerPoint (12 slides, opens in Keynote/PowerPoint)
├── build_slides.js                 ← Regenerate the .pptx
├── package.json
└── html/                           ← Reveal.js HTML deck (recommended)
    ├── index.html
    ├── styles.css
    └── README.md
```

### 🔧 Scripts

```
scripts/
├── setup.sh                        ← One-shot install of venv + npm deps
├── dev.sh                          ← Start backend + frontend together
├── download_dataset.py             ← Kaggle → data/raw/  (not needed anymore — already copied)
├── split_data.py                   ← 70/15/15 stratified split, seed 42
├── build_species_catalog.py        ← Generate placeholder catalog entries
├── seed_db.py                      ← Seed PostgreSQL/SQLite from species.yaml
└── cleanup.sh                      ← Remove venv/datasets/checkpoints (--hard deletes the repo)
```

### 🧪 Tests

```
tests/
├── conftest.py                     ← Shared pytest fixtures + StubClassifier
├── unit/
│   ├── test_preprocessing.py
│   └── test_split.py
└── integration/
    ├── test_api_health.py
    ├── test_api_predict.py
    └── test_api_species.py
```

---

## Running the project from this folder

```bash
cd ~/Documents/GitHub/leaflens

# 1. First time only: install dependencies
./scripts/setup.sh

# 2. (One-time) seed the database
source .venv/bin/activate && python scripts/seed_db.py

# 3. Launch backend + frontend together
./scripts/dev.sh

# Open http://localhost:5173 in the browser.
# Press Ctrl+C to stop everything.
```

## Reproducing the training results

```bash
source .venv/bin/activate

# Splits are already in data/processed/ — no need to re-split.
# To retrain a model:
python -m models.train --arch resnet50 --epochs 15
python -m models.evaluate --arch resnet50
```

## Quick checks (defense backup)

| What | Where | Expected |
|---|---|---|
| Final test top-1 (ResNet-50) | `models/checkpoints/resnet50_best.eval.json` → `top1` | 0.9238 |
| Final test top-3 (ResNet-50) | same file → `top3` | 0.9802 |
| Number of species in DB | `sqlite3 backend/leaflens.db "SELECT COUNT(*) FROM species"` | 47 |
| Care profiles | `sqlite3 backend/leaflens.db "SELECT COUNT(*) FROM care_profiles"` | 47 |
| Toxicity records | `sqlite3 backend/leaflens.db "SELECT COUNT(*) FROM toxicity_records"` | 94 |
| Image count in raw dataset | `find data/raw -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) \| wc -l` | 14774 |
| Image count in train manifest | `tail -n +2 data/processed/train.csv \| wc -l` | 10341 |

## Cleanup (after grading)

```bash
./scripts/cleanup.sh           # Removes venv, models, datasets, node_modules
./scripts/cleanup.sh --hard    # Additionally deletes the entire repo
```

---

**Public repository**: https://github.com/luigy23/leaflens

The git remote contains everything in this folder *except* the large generated
artifacts (`data/raw/`, `models/checkpoints/`, `.venv/`, `frontend/node_modules/`,
`backend/leaflens.db`, `.dev-logs/`). All of those are in `.gitignore` because
they're either huge or local-only.

<div align="center">

# 🌿 LeafLens

**AI-powered houseplant identification and care assistant.**
Upload a photo, get the species, get the care card, know if it's safe for your pets.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.12-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Tests](https://github.com/luigy23/leaflens/actions/workflows/ci.yml/badge.svg)](https://github.com/luigy23/leaflens/actions)
[![License](https://img.shields.io/badge/License-Academic-blue)](#license)

</div>

---

## ✨ What it does

Take a photo of any houseplant. LeafLens identifies the species among **47 of the most common indoor plants worldwide**, and returns:

- 🧠 Top-1 species name + confidence + 2 alternatives
- 💧 Watering schedule and light requirements
- 🌡️ Temperature, humidity, and fertilizer recommendations
- 🐾 Pet safety badge (toxic / mild / safe for cats and dogs, sourced from ASPCA)

End-to-end latency under **1 second** on the deployed instance.

---

## 📊 Headline results

The deployed model achieves **92.38% top-1 accuracy** on the held-out test set. Three architectures were compared:

| Model | Params | Test top-1 | Test top-3 | Macro F1 | Latency (MPS) |
|---|---|---|---|---|---|
| EfficientNet-B0 | 4.1 M | 92.02% | 98.06% | 0.9147 | ~100 ms |
| **ResNet-50** *(deployed)* | 23.6 M | **92.38%** | 98.02% | 0.9116 | ~200 ms |
| ViT-Base/16 † | 85.8 M | 90.17% | 97.88% | 0.8992 | ~400 ms |

> † ViT training was halted at epoch 3 — its trajectory was below both CNN baselines and would not have overtaken them within the patience budget. Justified at length in [`docs/13-results.md`](docs/13-results.md).

Targets from the project objectives (≥85% top-1, ≥95% top-3) cleared by all three.

---

## 🏗️ Architecture

```
            ┌──────────────────────────┐
   Browser  │      React + Vite SPA    │
            │  Upload, catalog, about  │
            └─────────────┬────────────┘
                          │ HTTPS multipart
                          ▼
            ┌──────────────────────────┐
            │   Flask API (gunicorn)   │
            │  /api/predict, /species  │
            │  /health                 │
            └──────┬───────────────┬───┘
       SQLAlchemy  │               │  PyTorch
                   ▼               ▼
        ┌─────────────────┐  ┌──────────────────┐
        │  PostgreSQL     │  │  ResNet-50       │
        │  47 species     │  │  fine-tuned head │
        │  47 care cards  │  │  loaded at boot  │
        │  94 toxicity    │  │                  │
        └─────────────────┘  └──────────────────┘
```

Full architecture diagram and component descriptions: [`docs/12-architecture.md`](docs/12-architecture.md).

---

## 🚀 Quick start

```bash
# 1. Clone and install
git clone https://github.com/luigy23/leaflens
cd leaflens
./scripts/setup.sh    # creates .venv, installs Python + Node deps

# 2. Download dataset (requires Kaggle API token in ~/.kaggle/kaggle.json)
python scripts/download_dataset.py

# 3. Split data 70/15/15 with fixed seed
python scripts/split_data.py

# 4. Train a model (ResNet-50, ~30 min on M-series Mac)
python -m models.train --arch resnet50 --epochs 15

# 5. Seed the database with the curated 47-species catalog
python scripts/seed_db.py

# 6. Run the backend (port 5001)
python -c "from backend.app import create_app; create_app().run(port=5001)"

# 7. Run the frontend (separate terminal)
cd frontend && VITE_API_BASE_URL=http://localhost:5001 npm run dev
```

Open http://localhost:5173 and drop in a photo.

---

## 🧪 Tech stack

- **AI**: PyTorch 2.12, timm 1.0, torchvision 0.27 — transfer learning with ImageNet pretrained backbones
- **Backend**: Flask 3.1, SQLAlchemy 2.0, PostgreSQL (SQLite locally), gunicorn
- **Frontend**: React 18, Vite 5, Tailwind CSS 3, react-router-dom 6, axios
- **Dataset**: [Kaggle House Plant Species](https://www.kaggle.com/datasets/kacpergregorowicz/house-plant-species) (47 classes, 14,774 images)
- **Tests**: pytest, pytest-flask, pytest-cov
- **CI**: GitHub Actions (lint + tests on every push)
- **Deployment target**: Docker → Render free tier + Vercel hobby tier

---

## 📁 Project structure

```
leaflens/
├── backend/           # Flask app, ORM models, routes, curated species YAML
├── data/              # Raw dataset (symlinked) and processed CSV splits
├── docs/              # 16-section English documentation set
├── frontend/          # React + Vite + Tailwind SPA
├── models/            # PyTorch architectures, training, evaluation, inference
├── scripts/           # Dataset download, split, seed, setup, cleanup
└── tests/             # Unit + integration tests
```

---

## 📚 Documentation

All documentation is in English under [`docs/`](docs/):

| | |
|---|---|
| 1. [Introduction](docs/01-introduction.md) | 9. [GUI Mockups](docs/09-mockups.md) |
| 2. [Problem](docs/02-problem.md) | 10. [API Catalog](docs/10-api-catalog.md) |
| 3. [Objectives](docs/03-objectives.md) | 11. [Testing](docs/11-testing.md) |
| 4. [State of the Art](docs/04-state-of-the-art.md) | 12. [Architecture](docs/12-architecture.md) |
| 5. [Requirements](docs/05-requirements.md) | 13. [Results & Discussion](docs/13-results.md) |
| 6. [Use Cases](docs/06-use-cases.md) | 14. [Future Work](docs/14-future-work.md) |
| 7. [Data Model (ER)](docs/07-data-model.md) | 15. [Presentation Outline](docs/15-presentation-outline.md) |
| 8. [Class Diagrams](docs/08-class-diagrams.md) | 16. [Deployment Guide](docs/16-deployment-guide.md) |

---

## 🧹 Cleanup

When you're done grading, free the disk:

```bash
./scripts/cleanup.sh          # removes venv, datasets, checkpoints, node_modules
./scripts/cleanup.sh --hard   # additionally deletes the entire repo
```

---

## 📜 License

Academic project for the **Artificial Intelligence** course (BEINSOF52) at **Universidad Surcolombiana**, May 2026.

Author: **Luigy Leonardo** ([@luigy23](https://github.com/luigy23))
Instructor: **Juan Antonio Castro Silva**

Care information curated from publicly available references (ASPCA toxic plant database, RHS plant finder, Missouri Botanical Garden, Pl@ntNet).

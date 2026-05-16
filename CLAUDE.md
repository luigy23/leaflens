# LeafLens — Project Context

## What this is

Final project #1 for the Artificial Intelligence course (BEINSOF52, Universidad Surcolombiana, Prof. Juan Antonio Castro Silva).

**Goal**: AI-powered houseplant identification with care instructions. User uploads a photo, the system classifies the species (47 classes) and returns watering, light, temperature, fertilization, and pet-toxicity info.

## Rubric (60% of final grade, this project = 50% of that)

| Weight | Item |
|---|---|
| 10% | Presentation in English |
| 40% | Documentation in English (full set: intro, problem, objectives, SoTA, requirements, use cases, ER model, class diagrams, mockups, API docs, tests, architecture, results, future work) |
| 5% | AI model (classification task) |
| 10% | Best practices: 70-15-15 split, class balancing, **≥3 models compared**, proper metrics, model serialization, separated training/inference scripts, Python+Flask+TensorFlow/PyTorch |
| 10% | Backend: Flask + PostgreSQL/MongoDB |
| 10% | Frontend: React or React Native |
| 5% | Cloud deployment (AWS/GCP/Azure/Heroku/Render/etc.) |
| 10% | IoT use — **NOT REQUIRED** for this project (instructor confirmed it was a suggestion) |

## Constraints

- Solo developer (no partner)
- 1-week timeline
- Apple Silicon M4 Air, 16GB RAM (no NVIDIA GPU — use MPS backend in PyTorch)
- Free-tier cloud only

## Architecture

```
User photo upload → React UI → Flask API → PyTorch inference (best model) → PostgreSQL lookup (care info) → JSON response → React display
```

## Key decisions

- **Dataset**: Kaggle "House Plant Species" by kacpergregorowicz (47 species). Smaller than PlantNet-300K (which is 30GB+) — manageable on disk and tractable in 1 week.
- **Models**: 3 architectures via transfer learning — EfficientNet-B0 (light), ResNet50 (classic baseline), ViT-Base (modern transformer). All pretrained on ImageNet, last layers replaced for 47-class output.
- **No training from scratch** — only fine-tuning (~10-30 epochs, frozen backbone for first phase, then unfreeze top blocks).
- **Care info source**: Curated JSON/CSV seeded into PostgreSQL. Sourced from Wikipedia / Trefle / Perenual API references.
- **Cloud**: Render free tier for backend, Vercel/Netlify for frontend, model loaded server-side.

## Important conventions

- All user-facing strings, docs, comments, commit messages: **English**
- Code style: black + ruff for Python, prettier for JS/TS
- Tests required: unit, functional, integration (rubric requirement)
- Reproducibility: save train/val/test splits as CSV manifests with image paths and labels

## Cleanup at project end

A `scripts/cleanup.sh` will:
- Remove `.venv/`
- Remove `data/raw/` and `data/processed/`
- Remove `models/checkpoints/`
- Remove `node_modules/` in frontend
- Optionally remove the entire repo

User wants minimal disk footprint after grading.

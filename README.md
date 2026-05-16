# LeafLens 🌿🔍

> AI-powered houseplant identification and care assistant.

LeafLens is a computer vision web application that identifies houseplants from a photo and returns care instructions: watering schedule, light requirements, temperature range, fertilization tips, and toxicity warnings for pets.

## Stack

- **Model**: Transfer learning with 3 architectures (EfficientNet-B0, ResNet50, ViT-Base) on Kaggle's House Plant Species dataset (47 species)
- **Backend**: Flask + PostgreSQL
- **Frontend**: React + Tailwind CSS
- **Deployment**: Render / HuggingFace Spaces

## Project Structure

```
leaflens/
├── data/                # Datasets (raw and processed) — gitignored
├── models/              # Training scripts and saved checkpoints
├── backend/             # Flask API + database layer
├── frontend/            # React web app
├── docs/                # Full project documentation (English)
├── scripts/             # Utility scripts (download, split, cleanup)
├── tests/               # Unit, integration and functional tests
└── notebooks/           # Exploratory data analysis
```

## Quickstart

```bash
# 1. Install Python dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Download dataset (requires Kaggle API credentials)
python scripts/download_dataset.py

# 3. Split data (70/15/15) with reproducible CSV manifests
python scripts/split_data.py

# 4. Train models
python models/train.py --arch efficientnet
python models/train.py --arch resnet50
python models/train.py --arch vit

# 5. Run backend
cd backend && flask run

# 6. Run frontend (in another terminal)
cd frontend && npm install && npm run dev
```

## Documentation

Full English documentation is in [`docs/`](docs/):

1. [Introduction](docs/01-introduction.md)
2. [Problem Statement](docs/02-problem.md)
3. [Objectives](docs/03-objectives.md)
4. [State of the Art](docs/04-state-of-the-art.md)
5. [Requirements](docs/05-requirements.md)
6. [Use Cases & User Stories](docs/06-use-cases.md)
7. [Data Dictionary & ER Model](docs/07-data-model.md)
8. [Class Diagrams](docs/08-class-diagrams.md)
9. [GUI Mockups](docs/09-mockups.md)
10. [API Catalog](docs/10-api-catalog.md)
11. [Testing](docs/11-testing.md)
12. [Architecture](docs/12-architecture.md)
13. [Results & Discussion](docs/13-results.md)
14. [Future Work](docs/14-future-work.md)

## License

Academic project for the Artificial Intelligence course (BEINSOF52) — Universidad Surcolombiana.

Author: Luigy Leonardo
Instructor: Juan Antonio Castro Silva

#!/usr/bin/env bash
# LeafLens — one-shot developer setup
#
# Creates a Python 3.11+ virtualenv, installs backend dependencies,
# installs frontend dependencies, and prints the next manual steps.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "==> LeafLens setup at $REPO_ROOT"

# 1. Python virtualenv
PY=""
for candidate in python3.13 python3.12 python3.11; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "ERROR: Python 3.11+ not found. Install with: brew install python@3.13"
    exit 1
fi

echo "==> Using $($PY --version)"

if [ ! -d .venv ]; then
    echo "==> Creating virtualenv at .venv"
    "$PY" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2. Frontend
if command -v npm >/dev/null 2>&1; then
    echo "==> Installing frontend dependencies"
    (cd frontend && npm install)
else
    echo "WARN: npm not found — skipping frontend install."
fi

# 3. Pre-flight checks
echo ""
echo "==> Next steps:"
echo ""
echo "  1. Set up Kaggle credentials if you haven't:"
echo "       https://www.kaggle.com/settings → 'Create New Token'"
echo "       mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/"
echo "       chmod 600 ~/.kaggle/kaggle.json"
echo ""
echo "  2. Download the dataset:"
echo "       python scripts/download_dataset.py"
echo ""
echo "  3. Generate train/val/test splits:"
echo "       python scripts/split_data.py"
echo ""
echo "  4. Build the species catalog placeholders:"
echo "       python scripts/build_species_catalog.py"
echo ""
echo "  5. Train a model (start with EfficientNet — fastest):"
echo "       python -m models.train --arch efficientnet --epochs 15"
echo ""
echo "  6. Seed the database:"
echo "       python scripts/seed_db.py"
echo ""
echo "  7. Run the backend:"
echo "       FLASK_APP=backend.app:create_app flask run --debug"
echo ""
echo "  8. Run the frontend (separate terminal):"
echo "       cd frontend && npm run dev"
echo ""
echo "==> Done."

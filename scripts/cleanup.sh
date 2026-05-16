#!/usr/bin/env bash
# LeafLens — cleanup script
# Removes generated artifacts (venv, datasets, model checkpoints, node_modules).
# Run with --hard to additionally delete the entire repository.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "LeafLens cleanup starting at: $REPO_ROOT"

# Python virtualenv
if [ -d "$REPO_ROOT/.venv" ]; then
    echo "Removing .venv ..."
    rm -rf "$REPO_ROOT/.venv"
fi

# Raw and processed datasets
if [ -d "$REPO_ROOT/data/raw" ]; then
    echo "Removing data/raw ..."
    rm -rf "$REPO_ROOT/data/raw"/*
fi
if [ -d "$REPO_ROOT/data/processed" ]; then
    echo "Removing data/processed ..."
    rm -rf "$REPO_ROOT/data/processed"/*
fi

# Model checkpoints
if [ -d "$REPO_ROOT/models/checkpoints" ]; then
    echo "Removing models/checkpoints ..."
    rm -rf "$REPO_ROOT/models/checkpoints"/*
fi

# Frontend node_modules
if [ -d "$REPO_ROOT/frontend/node_modules" ]; then
    echo "Removing frontend/node_modules ..."
    rm -rf "$REPO_ROOT/frontend/node_modules"
fi

# Python caches
find "$REPO_ROOT" -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
find "$REPO_ROOT" -type d -name ".pytest_cache" -prune -exec rm -rf {} + 2>/dev/null || true
find "$REPO_ROOT" -type d -name ".ipynb_checkpoints" -prune -exec rm -rf {} + 2>/dev/null || true

# Kaggle cache (shared across projects, prompt before delete)
KAGGLE_CACHE="$HOME/.cache/kagglehub/datasets/kacpergregorowicz/house-plant-species"
if [ -d "$KAGGLE_CACHE" ]; then
    echo ""
    echo "Kaggle cache found at: $KAGGLE_CACHE"
    read -p "Delete it too? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$KAGGLE_CACHE"
        echo "Kaggle cache removed."
    fi
fi

# Ollama models (in case shared with the second project)
# Not touched here — see Project 2 cleanup script.

echo ""
echo "Standard cleanup complete."

# Hard cleanup: delete the whole repo
if [ "${1:-}" = "--hard" ]; then
    echo ""
    read -p "HARD MODE: delete entire repo at $REPO_ROOT? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$HOME"
        rm -rf "$REPO_ROOT"
        echo "Repo deleted."
    fi
fi

"""
Download the House Plant Species dataset from Kaggle.

Requires Kaggle API credentials. Place kaggle.json in ~/.kaggle/ or set
KAGGLE_USERNAME and KAGGLE_KEY environment variables.

Usage:
    python scripts/download_dataset.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import kagglehub

DATASET_SLUG = "kacpergregorowicz/house-plant-species"
TARGET_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def main() -> int:
    print(f"Downloading dataset: {DATASET_SLUG}")
    try:
        cache_path = Path(kagglehub.dataset_download(DATASET_SLUG))
    except Exception as exc:
        print(f"ERROR: download failed: {exc}", file=sys.stderr)
        print(
            "Make sure your Kaggle API token is configured at ~/.kaggle/kaggle.json",
            file=sys.stderr,
        )
        return 1

    print(f"Dataset cached at: {cache_path}")

    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    if any(TARGET_DIR.iterdir()):
        print(f"WARNING: {TARGET_DIR} not empty — skipping copy")
        return 0

    for item in cache_path.iterdir():
        dest = TARGET_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    print(f"Dataset ready at: {TARGET_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

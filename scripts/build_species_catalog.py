"""Generate a starter YAML catalog entry for every class found in the dataset.

Run this after `scripts/download_dataset.py`. It scans the raw dataset for
class folders, looks up any species already curated in
`backend/data/species.yaml`, and appends placeholder entries for the
missing ones so the catalog covers all 47 species.

The generated placeholders use conservative default care values; you are
expected to refine them by hand.

Usage:
    python scripts/build_species_catalog.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
CATALOG = REPO_ROOT / "backend" / "data" / "species.yaml"


DEFAULT_CARE = {
    "watering_days_min": 7,
    "watering_days_max": 10,
    "light_level": "bright-indirect",
    "temperature_min_c": 18,
    "temperature_max_c": 27,
    "humidity_pct": "40-60",
    "fertilizer_schedule": "monthly in spring and summer",
}

DEFAULT_TOXICITY = [
    {"animal": "cat", "level": "safe", "notes": None},
    {"animal": "dog", "level": "safe", "notes": None},
]


def discover_class_names(root: Path) -> list[str]:
    candidates = [p for p in root.iterdir() if p.is_dir()]
    if not candidates:
        return []
    if len(candidates) == 1:
        nested = [p for p in candidates[0].iterdir() if p.is_dir()]
        if nested:
            return [p.name for p in nested]
    return [p.name for p in candidates]


def load_existing(path: Path) -> tuple[list[dict], set[str], set[str]]:
    if not path.exists():
        return [], set(), set()
    with path.open() as f:
        entries = yaml.safe_load(f) or []
    sci = {e["scientific_name"] for e in entries}
    com = {e["common_name"].lower() for e in entries}
    return entries, sci, com


def main() -> int:
    if not RAW_DIR.exists() or not any(RAW_DIR.iterdir()):
        print(f"ERROR: dataset not found at {RAW_DIR}", file=sys.stderr)
        return 1

    class_names = sorted(discover_class_names(RAW_DIR))
    if not class_names:
        print(f"ERROR: no class folders discovered under {RAW_DIR}", file=sys.stderr)
        return 1

    existing, existing_sci, existing_common = load_existing(CATALOG)

    added = 0
    for class_name in class_names:
        # Heuristic: Kaggle folder names are usually common names. We use them
        # as both common_name and as a placeholder scientific_name "Unknown <name>"
        # so that you can edit them by hand later without breaking the seeder.
        normalized = class_name.strip()
        if normalized.lower() in existing_common:
            continue

        placeholder_sci = f"Unknown {normalized}"
        if placeholder_sci in existing_sci:
            continue

        existing.append(
            {
                "scientific_name": placeholder_sci,
                "common_name": normalized,
                "family": None,
                "origin": None,
                "description": "Placeholder entry — please curate.",
                "image_url": None,
                "care": dict(DEFAULT_CARE),
                "toxicity": [dict(t) for t in DEFAULT_TOXICITY],
            }
        )
        added += 1

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    with CATALOG.open("w") as f:
        yaml.dump(existing, f, sort_keys=False, allow_unicode=True)

    print(f"Catalog updated: {len(existing)} entries total, {added} new placeholders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

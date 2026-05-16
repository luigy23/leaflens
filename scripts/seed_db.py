"""Seed the database from backend/data/species.yaml.

Usage:
    python scripts/seed_db.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from backend.app import create_app  # noqa: E402
from backend.db.seed import seed_from_yaml  # noqa: E402


def main() -> int:
    app = create_app()
    with app.app_context():
        count = seed_from_yaml()
    print(f"Seeded {count} species.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

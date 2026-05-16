"""Seed the species catalog from a YAML fixture.

The YAML file is bundled with the repository at backend/data/species.yaml.
The seeder is idempotent: it inserts species not yet present and updates
existing ones. It does NOT delete species.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from . import db
from .models import CareProfile, Species, ToxicityRecord

SEED_FILE = Path(__file__).resolve().parent.parent / "data" / "species.yaml"


def seed_from_yaml(path: Path | None = None) -> int:
    """Seed (or update) the species catalog. Returns the number of species
    written."""
    path = Path(path) if path else SEED_FILE
    if not path.exists():
        raise FileNotFoundError(f"seed file not found: {path}")

    with path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        raise ValueError(f"expected a list of species in {path}")

    written = 0
    for entry in data:
        sp = Species.query.filter_by(scientific_name=entry["scientific_name"]).first()
        if sp is None:
            sp = Species(scientific_name=entry["scientific_name"])
            db.session.add(sp)

        sp.common_name = entry["common_name"]
        sp.family = entry.get("family")
        sp.origin = entry.get("origin")
        sp.description = entry.get("description")
        sp.image_url = entry.get("image_url")

        care = entry["care"]
        if sp.care_profile is None:
            sp.care_profile = CareProfile(species=sp, **care)
        else:
            for key, value in care.items():
                setattr(sp.care_profile, key, value)

        # Replace toxicity records wholesale (simpler than diffing).
        sp.toxicity_records.clear()
        for tox in entry.get("toxicity", []):
            sp.toxicity_records.append(
                ToxicityRecord(
                    animal=tox["animal"], level=tox["level"], notes=tox.get("notes")
                )
            )

        written += 1

    db.session.commit()
    return written

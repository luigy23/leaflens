"""Shared pytest fixtures."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from backend.app import create_app
from backend.config import TestConfig
from backend.db import db
from backend.db.models import CareProfile, Species, ToxicityRecord


@dataclass
class _StubPrediction:
    rank: int
    class_id: int
    class_name: str
    confidence: float


class StubClassifier:
    """A deterministic stand-in for PlantClassifier used in integration tests."""

    model_name = "stub-classifier"
    num_classes = 47

    def predict(self, image_bytes: bytes, k: int = 3):
        from models.inference import PredictionResult, TopKItem

        topk = [
            TopKItem(rank=1, class_id=0, class_name="Aloe Vera", confidence=0.91),
            TopKItem(rank=2, class_id=1, class_name="Golden Pothos", confidence=0.05),
            TopKItem(rank=3, class_id=2, class_name="Snake Plant", confidence=0.04),
        ][:k]
        return PredictionResult(
            topk=topk,
            model_name=self.model_name,
            latency_ms=10,
            low_confidence=topk[0].confidence < 0.40,
        )


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        _seed_minimal_catalog()
        app.config["classifier"] = StubClassifier()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def _seed_minimal_catalog():
    species = [
        ("Aloe vera", "Aloe Vera"),
        ("Epipremnum aureum", "Golden Pothos"),
        ("Sansevieria trifasciata", "Snake Plant"),
    ]
    for sci, com in species:
        sp = Species(scientific_name=sci, common_name=com)
        sp.care_profile = CareProfile(
            watering_days_min=7,
            watering_days_max=10,
            light_level="bright-indirect",
            temperature_min_c=18,
            temperature_max_c=27,
            humidity_pct="40-60",
            fertilizer_schedule="monthly in spring and summer",
        )
        sp.toxicity_records = [
            ToxicityRecord(animal="cat", level="safe"),
            ToxicityRecord(animal="dog", level="safe"),
        ]
        db.session.add(sp)
    db.session.commit()

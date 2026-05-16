"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-replace-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{REPO_ROOT / 'backend' / 'leaflens.db'}",
    )
    # Render sometimes hands out postgres:// URIs which SQLAlchemy 2 rejects.
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
    MIN_IMAGE_DIMENSION = 224

    CHECKPOINT_PATH = os.environ.get(
        "CHECKPOINT_PATH",
        str(REPO_ROOT / "models" / "checkpoints" / "best.pt"),
    )

    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.environ.get(
            "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000"
        ).split(",")
        if origin.strip()
    ]

    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "60 per minute")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    CHECKPOINT_PATH = ""  # tests use a stub classifier
    RATELIMIT_DEFAULT = "10000 per minute"

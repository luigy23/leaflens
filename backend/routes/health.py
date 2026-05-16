"""Liveness probe and model metadata endpoint."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify

bp = Blueprint("health", __name__)


@bp.get("/api/health")
def health():
    classifier = current_app.config.get("classifier")
    if classifier is None:
        return (
            jsonify(
                {
                    "status": "starting",
                    "model_name": None,
                    "model_version": None,
                    "num_classes": 0,
                    "checked_at": datetime.now(timezone.utc).isoformat(),
                }
            ),
            503,
        )

    return jsonify(
        {
            "status": "ok",
            "model_name": classifier.model_name,
            "model_version": "1.0.0",
            "num_classes": classifier.num_classes,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
    )

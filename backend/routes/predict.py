"""Image upload + prediction endpoint."""

from __future__ import annotations

import io

from flask import Blueprint, current_app, jsonify, request
from PIL import Image, UnidentifiedImageError

from ..db import db
from ..db.models import Prediction, Species

bp = Blueprint("predict", __name__)


def _bad_request(message: str):
    return jsonify({"error": message}), 400


@bp.post("/api/predict")
def predict():
    classifier = current_app.config.get("classifier")
    if classifier is None:
        return jsonify({"error": "model_not_loaded"}), 503

    if "image" not in request.files:
        return _bad_request("missing 'image' field")

    file = request.files["image"]
    if file.mimetype not in current_app.config["ALLOWED_IMAGE_TYPES"]:
        return _bad_request(f"unsupported content type: {file.mimetype}")

    raw = file.read()
    if not raw:
        return _bad_request("empty file")

    try:
        with Image.open(io.BytesIO(raw)) as img:
            width, height = img.size
            if min(width, height) < current_app.config["MIN_IMAGE_DIMENSION"]:
                return _bad_request(
                    f"image too small ({width}x{height}); minimum side is "
                    f"{current_app.config['MIN_IMAGE_DIMENSION']}px"
                )
    except UnidentifiedImageError:
        return _bad_request("corrupted or unrecognized image")

    k = request.args.get("k", default=3, type=int)
    k = max(1, min(k, 5))

    result = classifier.predict(raw, k=k)

    # Enrich each top-k item with database info
    enriched = []
    for item in result.topk:
        sp = Species.query.filter_by(scientific_name=item.class_name).first()
        if sp is None:
            # Fallback: also try common name match if the class label uses it.
            sp = Species.query.filter(
                Species.common_name.ilike(item.class_name)
            ).first()
        if sp is None:
            enriched.append(
                {
                    "rank": item.rank,
                    "species_id": None,
                    "scientific_name": item.class_name,
                    "common_name": item.class_name,
                    "confidence": item.confidence,
                    "care": None,
                    "toxicity": [],
                }
            )
            continue

        enriched.append(
            {
                "rank": item.rank,
                "species_id": sp.id,
                "scientific_name": sp.scientific_name,
                "common_name": sp.common_name,
                "confidence": item.confidence,
                "care": sp.care_profile.to_dict() if sp.care_profile else None,
                "toxicity": [t.to_dict() for t in sp.toxicity_records],
            }
        )

    # Persist analytics row (no image payload)
    try:
        record = Prediction(
            top1_species_id=enriched[0]["species_id"],
            top1_confidence=enriched[0]["confidence"],
            top3_species_ids=[item["species_id"] for item in enriched],
            model_name=result.model_name,
            latency_ms=result.latency_ms,
            user_agent=(request.user_agent.string or "")[:255],
        )
        db.session.add(record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        # Analytics failure should not break user-facing prediction.

    return jsonify(
        {
            "topk": enriched,
            "model_name": result.model_name,
            "latency_ms": result.latency_ms,
            "low_confidence": result.low_confidence,
        }
    )

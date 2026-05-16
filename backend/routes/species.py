"""Catalog browsing endpoints."""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from ..db import db
from ..db.models import Species

bp = Blueprint("species", __name__)


@bp.get("/api/species")
def list_species():
    q = request.args.get("q", type=str)
    query = Species.query.order_by(Species.common_name)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Species.common_name.ilike(like), Species.scientific_name.ilike(like))
        )
    items = [
        {
            "id": sp.id,
            "scientific_name": sp.scientific_name,
            "common_name": sp.common_name,
        }
        for sp in query.all()
    ]
    return jsonify({"count": len(items), "items": items})


@bp.get("/api/species/<int:species_id>")
def get_species(species_id: int):
    sp = db.session.get(Species, species_id)
    if sp is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify(sp.to_dict(include_care=True))

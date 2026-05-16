"""SQLAlchemy models for the species catalog and analytics."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON

from . import db


class Species(db.Model):
    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(120), nullable=False, unique=True)
    common_name = db.Column(db.String(120), nullable=False)
    family = db.Column(db.String(80))
    origin = db.Column(db.String(120))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    care_profile = db.relationship(
        "CareProfile", uselist=False, back_populates="species", cascade="all, delete-orphan"
    )
    toxicity_records = db.relationship(
        "ToxicityRecord", back_populates="species", cascade="all, delete-orphan"
    )

    def to_dict(self, include_care: bool = True) -> dict:
        data = {
            "id": self.id,
            "scientific_name": self.scientific_name,
            "common_name": self.common_name,
            "family": self.family,
            "origin": self.origin,
            "description": self.description,
            "image_url": self.image_url,
        }
        if include_care:
            data["care"] = self.care_profile.to_dict() if self.care_profile else None
            data["toxicity"] = [t.to_dict() for t in self.toxicity_records]
        return data


class CareProfile(db.Model):
    __tablename__ = "care_profiles"

    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(
        db.Integer, db.ForeignKey("species.id"), nullable=False, unique=True
    )
    watering_days_min = db.Column(db.Integer, nullable=False)
    watering_days_max = db.Column(db.Integer, nullable=False)
    light_level = db.Column(db.String(40), nullable=False)
    temperature_min_c = db.Column(db.Integer, nullable=False)
    temperature_max_c = db.Column(db.Integer, nullable=False)
    humidity_pct = db.Column(db.String(40))
    fertilizer_schedule = db.Column(db.String(120))

    species = db.relationship("Species", back_populates="care_profile")

    def to_dict(self) -> dict:
        return {
            "watering_days_min": self.watering_days_min,
            "watering_days_max": self.watering_days_max,
            "light_level": self.light_level,
            "temperature_min_c": self.temperature_min_c,
            "temperature_max_c": self.temperature_max_c,
            "humidity_pct": self.humidity_pct,
            "fertilizer_schedule": self.fertilizer_schedule,
        }


class ToxicityRecord(db.Model):
    __tablename__ = "toxicity_records"

    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"), nullable=False)
    animal = db.Column(db.String(10), nullable=False)  # 'cat' or 'dog'
    level = db.Column(db.String(20), nullable=False)  # 'safe' | 'mild' | 'toxic'
    notes = db.Column(db.String(255))

    species = db.relationship("Species", back_populates="toxicity_records")

    def to_dict(self) -> dict:
        return {"animal": self.animal, "level": self.level, "notes": self.notes}


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    top1_species_id = db.Column(db.Integer, db.ForeignKey("species.id"), nullable=True)
    top1_confidence = db.Column(db.Float, nullable=False)
    top3_species_ids = db.Column(JSON, nullable=False)
    model_name = db.Column(db.String(40), nullable=False)
    latency_ms = db.Column(db.Integer, nullable=False)
    user_agent = db.Column(db.String(255))

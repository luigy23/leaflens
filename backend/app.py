"""Application factory."""

from __future__ import annotations

import logging
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from .config import Config
from .db import db
from .routes import health_bp, predict_bp, species_bp


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["ALLOWED_ORIGINS"]}})

    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(species_bp)

    logging.basicConfig(level=logging.INFO)

    with app.app_context():
        db.create_all()
        _maybe_load_classifier(app)

    return app


def _maybe_load_classifier(app: Flask) -> None:
    """Load the model on startup if a checkpoint is available.

    Failure to load is logged but does not crash the app — health check will
    report the missing model.
    """
    checkpoint = Path(app.config.get("CHECKPOINT_PATH", ""))
    if not checkpoint or not checkpoint.exists():
        app.logger.warning(
            "No checkpoint at %s; classifier endpoints will return 503.",
            checkpoint or "<unset>",
        )
        app.config["classifier"] = None
        return

    try:
        from models.inference import PlantClassifier

        app.config["classifier"] = PlantClassifier(checkpoint_path=checkpoint)
        app.logger.info("Loaded classifier from %s", checkpoint)
    except Exception as exc:
        app.logger.error("Failed to load classifier: %s", exc)
        app.config["classifier"] = None


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)

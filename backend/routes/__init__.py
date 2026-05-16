from .health import bp as health_bp
from .predict import bp as predict_bp
from .species import bp as species_bp

__all__ = ["health_bp", "predict_bp", "species_bp"]

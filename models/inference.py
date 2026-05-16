"""Runtime inference wrapper used by the Flask backend.

A single `PlantClassifier` instance is created at app startup; subsequent
requests reuse it for low-latency prediction.
"""

from __future__ import annotations

import io
import time
from dataclasses import dataclass
from pathlib import Path

import torch
from PIL import Image
from torch.nn import functional as F

from .architectures import build_model
from .dataset import build_transforms

DEFAULT_CHECKPOINT = (
    Path(__file__).resolve().parent.parent / "models" / "checkpoints" / "best.pt"
)


@dataclass
class TopKItem:
    rank: int
    class_id: int
    class_name: str
    confidence: float


@dataclass
class PredictionResult:
    topk: list[TopKItem]
    model_name: str
    latency_ms: int
    low_confidence: bool


class PlantClassifier:
    LOW_CONFIDENCE_THRESHOLD = 0.40

    def __init__(self, checkpoint_path: Path | None = None, device: str | None = None):
        path = Path(checkpoint_path) if checkpoint_path else DEFAULT_CHECKPOINT
        if not path.exists():
            raise FileNotFoundError(
                f"checkpoint not found at {path}. "
                "Train at least one model first or set CHECKPOINT_PATH."
            )

        payload = torch.load(path, map_location="cpu", weights_only=False)
        self.arch = payload["arch"]
        self.class_names: list[str] = payload["class_names"]
        self.num_classes = len(self.class_names)
        self.model_name = f"leaflens-{self.arch}"

        if device:
            self.device = torch.device(device)
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        self.model = build_model(self.arch, num_classes=self.num_classes)
        self.model.load_state_dict(payload["state_dict"])
        self.model.to(self.device).eval()

        self.transform = build_transforms(training=False)

    def predict(self, image_bytes: bytes, k: int = 3) -> PredictionResult:
        started = time.perf_counter()
        with Image.open(io.BytesIO(image_bytes)) as img:
            img = img.convert("RGB")
        tensor = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs = F.softmax(logits, dim=1).squeeze(0).cpu()

        k = max(1, min(k, self.num_classes))
        confidences, indices = torch.topk(probs, k)
        items = [
            TopKItem(
                rank=rank + 1,
                class_id=int(idx),
                class_name=self.class_names[int(idx)],
                confidence=float(conf),
            )
            for rank, (conf, idx) in enumerate(zip(confidences.tolist(), indices.tolist()))
        ]

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return PredictionResult(
            topk=items,
            model_name=self.model_name,
            latency_ms=elapsed_ms,
            low_confidence=items[0].confidence < self.LOW_CONFIDENCE_THRESHOLD,
        )

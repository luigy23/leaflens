"""Evaluate a trained checkpoint on the test set.

Outputs to stdout and writes a JSON report next to the checkpoint.

═══════════════════════════════════════════════════════════════════════════
  PIPELINE — sigue PASO 1 .. PASO 5
═══════════════════════════════════════════════════════════════════════════
  PASO 1 — Cargar el checkpoint entrenado (.pt) y la lista de clases
  PASO 2 — Construir el DataLoader del TEST set (sin shuffle, sin sampler)
  PASO 3 — Recrear el modelo y cargar pesos · inferencia sin gradientes
  PASO 4 — Calcular métricas: top-1, top-3, Macro F1, Weighted F1
  PASO 5 — Imprimir reporte por clase + guardar JSON con confusion matrix
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    top_k_accuracy_score,
)
from torch.utils.data import DataLoader

from .architectures import build_model
from .dataset import PlantImageDataset, build_transforms

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = REPO_ROOT / "data" / "processed"
CKPT_DIR = REPO_ROOT / "models" / "checkpoints"


def pick_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", required=True)
    parser.add_argument("--checkpoint", default=None)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 1 — Cargar el checkpoint entrenado y la lista de clases
    # ═══════════════════════════════════════════════════════════════════════
    # El checkpoint guarda: arch, state_dict, class_names, val_acc, epoch.
    ckpt_path = Path(args.checkpoint) if args.checkpoint else CKPT_DIR / f"{args.arch}_best.pt"
    if not ckpt_path.exists():
        raise SystemExit(f"checkpoint not found: {ckpt_path}")

    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    class_names = payload["class_names"]
    num_classes = len(class_names)

    device = pick_device()
    print(f"Device: {device}")

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 2 — DataLoader del TEST set (test.csv, nunca visto en training)
    # ═══════════════════════════════════════════════════════════════════════
    # IMPORTANTE: usa transforms DETERMINISTAS (sin augmentation) — solo
    # resize + center crop + normalize. No usa sampler ni shuffle.
    test_ds = PlantImageDataset(
        PROCESSED / "test.csv", REPO_ROOT, transform=build_transforms(training=False)
    )
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 3 — Recrear modelo, cargar pesos, inferencia sin gradientes
    # ═══════════════════════════════════════════════════════════════════════
    model = build_model(args.arch, num_classes=num_classes)
    model.load_state_dict(payload["state_dict"])
    model.to(device).eval()                              # eval() desactiva dropout y batchnorm-stats updates

    all_logits: list[np.ndarray] = []
    all_labels: list[int] = []
    with torch.no_grad():                                # no_grad → ahorra memoria, infiere más rápido
        for images, labels in test_loader:
            images = images.to(device)
            logits = model(images).cpu().numpy()         # logits = scores antes de softmax
            all_logits.append(logits)
            all_labels.extend(labels.tolist())

    logits_np = np.concatenate(all_logits)
    preds = logits_np.argmax(axis=1)                     # top-1 predicción = índice del logit máximo

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 4 — Calcular métricas
    # ═══════════════════════════════════════════════════════════════════════
    # top-1: % de aciertos exactos en la predicción más confiada
    # top-3: % donde la clase correcta está en las 3 más probables
    # macro f1: F1 promediada SIN ponderar por tamaño de clase (justo con minoritarias)
    # weighted f1: F1 ponderada por # de muestras (refleja accuracy global)
    # → Si macro ≈ weighted, significa que el balanceo funcionó.
    top1 = float((preds == np.array(all_labels)).mean())
    top3 = float(top_k_accuracy_score(all_labels, logits_np, k=3, labels=list(range(num_classes))))
    macro_f1 = float(f1_score(all_labels, preds, average="macro"))
    weighted_f1 = float(f1_score(all_labels, preds, average="weighted"))

    print(f"top1: {top1:.4f}")
    print(f"top3: {top3:.4f}")
    print(f"macro f1: {macro_f1:.4f}")
    print(f"weighted f1: {weighted_f1:.4f}")
    print(classification_report(all_labels, preds, target_names=class_names, zero_division=0))

    # Confusion matrix 47×47 — útil para ver qué clases se confunden entre sí.
    cm = confusion_matrix(all_labels, preds, labels=list(range(num_classes)))

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 5 — Guardar reporte JSON con todas las métricas
    # ═══════════════════════════════════════════════════════════════════════
    # El archivo *.eval.json queda al lado del checkpoint para auditoría.
    report = {
        "checkpoint": str(ckpt_path.relative_to(REPO_ROOT)),
        "arch": args.arch,
        "top1": top1,
        "top3": top3,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "class_names": class_names,
        "confusion_matrix": cm.tolist(),
    }
    report_path = ckpt_path.with_suffix(".eval.json")
    with report_path.open("w") as f:
        json.dump(report, f, indent=2)
    print(f"Report written to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

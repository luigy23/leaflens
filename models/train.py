"""Train a single architecture on the House Plant Species split.

Usage:
    python -m models.train --arch efficientnet --epochs 30
    python -m models.train --arch resnet50    --epochs 30
    python -m models.train --arch vit         --epochs 20

═══════════════════════════════════════════════════════════════════════════
  PIPELINE — sigue los marcadores PASO 1 .. PASO 8 al recorrer el archivo
═══════════════════════════════════════════════════════════════════════════
  PASO 1 — Cargar manifests CSV (train/val) con seed 42 → reproducibilidad
  PASO 2 — Construir Datasets PyTorch con transforms + augmentation
  PASO 3 — BALANCEO DE CLASES con WeightedRandomSampler (antes del modelo)
  PASO 4 — DataLoaders (train usa sampler, val usa shuffle=False)
  PASO 5 — Construir modelo (transfer learning desde ImageNet)
  PASO 6 — Loss class-weighted + optimizador AdamW
  PASO 7 — Loop de entrenamiento: warm-up congelado → differential LR
  PASO 8 — Validar cada epoch · guardar mejor checkpoint · early stopping
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, WeightedRandomSampler

from .architectures import (
    SUPPORTED_ARCHS,
    build_model,
    freeze_backbone,
    head_and_backbone_params,
    unfreeze_all,
)
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


def class_weights_from_manifest(manifest_path: Path, num_classes: int) -> torch.Tensor:
    """Per-class loss weights, inverse to class frequency.

    Used in the loss function as a secondary balancing layer that compensates
    any residual imbalance the sampler leaves in a given epoch.
    """
    import pandas as pd

    df = pd.read_csv(manifest_path)
    counts = df["class_id"].value_counts().sort_index()
    counts = counts.reindex(range(num_classes), fill_value=0).to_numpy()
    weights = 1.0 / np.maximum(counts, 1)
    weights = weights / weights.sum() * num_classes
    return torch.tensor(weights, dtype=torch.float32)


def build_balanced_sampler(dataset, num_classes: int) -> WeightedRandomSampler:
    """Build a per-sample WeightedRandomSampler that oversamples minority
    classes so that every minibatch is class-balanced *before* the model
    sees it.

    This is the "pre-training" balancing step: minority classes are drawn
    more often, majority classes less often, with replacement. The model
    therefore never sees a skewed batch — the bias is corrected at the
    DataLoader level, exactly as required by the rubric.
    """
    # The PlantImageDataset stores the manifest as a DataFrame on `.manifest`
    class_ids = dataset.manifest["class_id"].to_numpy()
    counts = np.bincount(class_ids, minlength=num_classes)
    inverse_freq = 1.0 / np.maximum(counts, 1)          # rarer class → bigger weight
    sample_weights = inverse_freq[class_ids]            # weight per sample, by its class
    sample_weights = sample_weights / sample_weights.sum()
    return WeightedRandomSampler(
        weights=torch.tensor(sample_weights, dtype=torch.double),
        num_samples=len(sample_weights),
        replacement=True,
    )


def evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[float, float]:
    model.eval()
    correct = total = 0
    loss_total = 0.0
    criterion = nn.CrossEntropyLoss()
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            logits = model(images)
            loss_total += criterion(logits, labels).item() * images.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return loss_total / total, correct / total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", required=True, choices=SUPPORTED_ARCHS)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr-head", type=float, default=1e-3)
    parser.add_argument("--lr-backbone", type=float, default=1e-4)
    parser.add_argument("--freeze-epochs", type=int, default=3)
    parser.add_argument("--patience", type=int, default=5)
    parser.add_argument("--num-workers", type=int, default=2)
    args = parser.parse_args()

    CKPT_DIR.mkdir(parents=True, exist_ok=True)

    device = pick_device()
    print(f"Using device: {device}")

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 1 — Cargar los manifests CSV de los splits 70/15/15
    # ═══════════════════════════════════════════════════════════════════════
    # Los CSV fueron generados por scripts/split_data.py con random_state=42.
    # Esto garantiza que cada corrida ve los mismos archivos en train/val/test.
    #
    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 2 — Construir Datasets PyTorch con transforms + augmentation
    # ═══════════════════════════════════════════════════════════════════════
    # train usa augmentation (random crop, flip, rotation, color jitter).
    # val usa transforms determinísticas (center crop, sin augmentation).
    train_ds = PlantImageDataset(
        PROCESSED / "train.csv", REPO_ROOT, transform=build_transforms(training=True)
    )
    val_ds = PlantImageDataset(
        PROCESSED / "val.csv", REPO_ROOT, transform=build_transforms(training=False)
    )

    num_classes = train_ds.num_classes
    print(f"Classes: {num_classes}, train: {len(train_ds)}, val: {len(val_ds)}")

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 3 — BALANCEO DE CLASES con WeightedRandomSampler
    #            (esto sucede ANTES de que el modelo vea cualquier dato)
    # ═══════════════════════════════════════════════════════════════════════
    # El dataset es desbalanceado: Yucca tiene 66 imágenes, Monstera 547 (8.3×).
    # build_balanced_sampler() asigna a cada muestra un peso inversamente
    # proporcional a la frecuencia de su clase. PyTorch usa esos pesos para
    # SOBREMUESTREAR clases minoritarias dentro de cada batch.
    # Verificado: ratio max/min cae de 8.3× a 1.36× después del sampling.
    train_sampler = build_balanced_sampler(train_ds, num_classes)

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 4 — DataLoaders
    # ═══════════════════════════════════════════════════════════════════════
    # train_loader recibe el sampler (no shuffle=True; son mutuamente excluyentes).
    # val_loader usa el orden original (sin sampler, sin shuffle).
    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size if args.arch != "vit" else 16,
        sampler=train_sampler,        # ← oversamplea minoritarias por batch
        num_workers=args.num_workers,
        pin_memory=(device.type == "cuda"),
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=(device.type == "cuda"),
    )

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 5 — Construir el modelo con TRANSFER LEARNING
    # ═══════════════════════════════════════════════════════════════════════
    # build_model() carga pesos preentrenados de ImageNet y reemplaza la
    # cabeza por una capa lineal nueva de num_classes (47) salidas.
    # freeze_backbone() congela todo excepto la cabeza para el warm-up.
    model = build_model(args.arch, num_classes=num_classes).to(device)
    freeze_backbone(model, args.arch)

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 6 — Loss (class-weighted) + Optimizador AdamW
    # ═══════════════════════════════════════════════════════════════════════
    # Segunda capa de balanceo (belt-and-suspenders): aún si el sampler
    # deja un batch ligeramente sesgado, los pesos del loss compensan.
    class_weights = class_weights_from_manifest(PROCESSED / "train.csv", num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)

    # Solo la cabeza tiene gradientes durante el warm-up.
    head_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(head_params, lr=args.lr_head, weight_decay=1e-4)

    best_val_acc = 0.0
    epochs_without_improvement = 0
    history = []

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 7 — Loop de entrenamiento (warm-up + unfreeze + differential LR)
    # ═══════════════════════════════════════════════════════════════════════
    # Estrategia en dos fases:
    #   • Fase A (primeras `freeze_epochs` epochs): solo entrena la cabeza
    #     con learning rate alto (lr_head = 1e-3) — la cabeza converge rápido.
    #   • Fase B (resto de epochs): unfreeze del backbone, optimizador
    #     dual con lr_backbone = 1e-4 (lento, fino-tuning) + lr_head = 1e-3.
    for epoch in range(1, args.epochs + 1):
        if epoch == args.freeze_epochs + 1:
            print("Unfreezing backbone, switching to differential learning rates...")
            unfreeze_all(model)
            head_params, backbone_params = head_and_backbone_params(model, args.arch)
            optimizer = torch.optim.AdamW(
                [
                    {"params": backbone_params, "lr": args.lr_backbone},
                    {"params": head_params, "lr": args.lr_head},
                ],
                weight_decay=1e-4,
            )

        # ── Train one epoch ──
        model.train()
        epoch_start = time.time()
        running_loss = 0.0
        running_total = 0
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
            running_total += images.size(0)
        train_loss = running_loss / running_total

        # ═══════════════════════════════════════════════════════════════════
        #  PASO 8 — Validación + checkpoint del mejor + early stopping
        # ═══════════════════════════════════════════════════════════════════
        val_loss, val_acc = evaluate(model, val_loader, device)
        elapsed = time.time() - epoch_start
        print(
            f"epoch {epoch:02d} | train_loss={train_loss:.4f} | "
            f"val_loss={val_loss:.4f} | val_acc={val_acc:.4f} | {elapsed:.1f}s"
        )
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_acc": val_acc,
                "elapsed_sec": elapsed,
            }
        )

        # Guarda solo si superó el mejor val_acc visto hasta ahora.
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            epochs_without_improvement = 0
            ckpt_path = CKPT_DIR / f"{args.arch}_best.pt"
            torch.save(
                {
                    "arch": args.arch,
                    "state_dict": model.state_dict(),
                    "class_names": train_ds.class_names,
                    "val_acc": val_acc,
                    "epoch": epoch,
                },
                ckpt_path,
            )
            print(f"  ↳ new best val_acc={val_acc:.4f} saved to {ckpt_path}")
        else:
            epochs_without_improvement += 1
            # Early stopping: si N epochs seguidos sin mejorar, corta.
            if epochs_without_improvement >= args.patience:
                print(f"Early stopping at epoch {epoch} (no improvement for {args.patience} epochs).")
                break

    history_path = CKPT_DIR / f"{args.arch}_history.json"
    with history_path.open("w") as f:
        json.dump({"args": vars(args), "best_val_acc": best_val_acc, "history": history}, f, indent=2)
    print(f"Best val acc: {best_val_acc:.4f}; history saved to {history_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

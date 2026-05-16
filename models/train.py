"""Train a single architecture on the House Plant Species split.

Usage:
    python -m models.train --arch efficientnet --epochs 30
    python -m models.train --arch resnet50    --epochs 30
    python -m models.train --arch vit         --epochs 20
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

from .architectures import SUPPORTED_ARCHS, build_model, freeze_backbone, unfreeze_all
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
    import pandas as pd

    df = pd.read_csv(manifest_path)
    counts = df["class_id"].value_counts().sort_index()
    counts = counts.reindex(range(num_classes), fill_value=0).to_numpy()
    weights = 1.0 / np.maximum(counts, 1)
    weights = weights / weights.sum() * num_classes
    return torch.tensor(weights, dtype=torch.float32)


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

    train_ds = PlantImageDataset(
        PROCESSED / "train.csv", REPO_ROOT, transform=build_transforms(training=True)
    )
    val_ds = PlantImageDataset(
        PROCESSED / "val.csv", REPO_ROOT, transform=build_transforms(training=False)
    )

    num_classes = train_ds.num_classes
    print(f"Classes: {num_classes}, train: {len(train_ds)}, val: {len(val_ds)}")

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size if args.arch != "vit" else 16,
        shuffle=True,
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

    model = build_model(args.arch, num_classes=num_classes).to(device)
    freeze_backbone(model, args.arch)

    weights = class_weights_from_manifest(PROCESSED / "train.csv", num_classes).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights)

    head_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(head_params, lr=args.lr_head, weight_decay=1e-4)

    best_val_acc = 0.0
    epochs_without_improvement = 0
    history = []

    for epoch in range(1, args.epochs + 1):
        if epoch == args.freeze_epochs + 1:
            print("Unfreezing backbone, switching to differential learning rates...")
            unfreeze_all(model)
            optimizer = torch.optim.AdamW(
                [
                    {"params": [p for n, p in model.named_parameters() if "head" not in n and "fc" not in n and "classifier" not in n], "lr": args.lr_backbone},
                    {"params": [p for n, p in model.named_parameters() if "head" in n or "fc" in n or "classifier" in n], "lr": args.lr_head},
                ],
                weight_decay=1e-4,
            )

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

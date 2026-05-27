"""
Split the House Plant Species dataset into train/validation/test sets
following a 70/15/15 stratified split with a fixed seed for reproducibility.

Outputs:
    data/processed/train.csv
    data/processed/val.csv
    data/processed/test.csv
    data/processed/class_distribution.csv

Each manifest CSV has columns: image_path, class_name, class_id

Usage:
    python scripts/split_data.py

═══════════════════════════════════════════════════════════════════════════
  PIPELINE — sigue PASO 1 .. PASO 5
═══════════════════════════════════════════════════════════════════════════
  PASO 1 — Descubrir todas las imágenes del dataset (una carpeta por clase)
  PASO 2 — Asignar class_id estable por orden alfabético del nombre
  PASO 3 — Primer split estratificado: 15% test (seed 42)
  PASO 4 — Segundo split estratificado: train 70% / val 15%
  PASO 5 — Escribir 4 CSV: train, val, test, class_distribution
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.model_selection import train_test_split

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

# Constantes de partición — fijas para reproducibilidad.
SEED = 42                # ← Mismo seed = mismo split. Borrar y re-generar da el mismo CSV.
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


# ═══════════════════════════════════════════════════════════════════════════
#  PASO 1 — Descubrir imágenes (una carpeta por clase)
# ═══════════════════════════════════════════════════════════════════════════
def discover_images(root: Path) -> list[tuple[Path, str]]:
    """Return (image_path, class_name) tuples for every image under root.

    Asume estructura: root/<class_name>/<image>.jpg
    """
    samples: list[tuple[Path, str]] = []
    for class_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for img in class_dir.iterdir():
            if img.suffix.lower() in IMAGE_EXTENSIONS:
                samples.append((img, class_dir.name))
    return samples


def write_manifest(path: Path, rows: list[tuple[Path, str, int]]) -> None:
    """Escribe un manifest CSV con columnas image_path, class_name, class_id."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "class_name", "class_id"])
        for img_path, class_name, class_id in rows:
            writer.writerow([str(img_path.relative_to(REPO_ROOT)), class_name, class_id])


def main() -> int:
    if not RAW_DIR.exists() or not any(RAW_DIR.iterdir()):
        print(
            f"ERROR: raw dataset not found at {RAW_DIR}. "
            "Run scripts/download_dataset.py first.",
            file=sys.stderr,
        )
        return 1

    # Kaggle a veces anida las imágenes en un subdirectorio extra — lo detectamos.
    candidates = [p for p in RAW_DIR.iterdir() if p.is_dir()]
    if len(candidates) == 1 and not any(
        (c.suffix.lower() in IMAGE_EXTENSIONS) for c in candidates[0].iterdir() if c.is_file()
    ):
        root = candidates[0]
    else:
        root = RAW_DIR

    samples = discover_images(root)
    if not samples:
        print(f"ERROR: no images discovered under {root}", file=sys.stderr)
        return 1

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 2 — Asignar class_id estable (orden alfabético)
    # ═══════════════════════════════════════════════════════════════════════
    # Ordenar alfabéticamente garantiza que "Aloe Vera" siempre sea class_id=1,
    # "Anthurium" siempre class_id=2, etc. — sin depender del orden del disco.
    class_names = sorted({class_name for _, class_name in samples})
    class_to_id = {name: idx for idx, name in enumerate(class_names)}

    paths = [s[0] for s in samples]
    labels = [class_to_id[s[1]] for s in samples]

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 3 — Primer split: separar 15% TEST (estratificado por clase)
    # ═══════════════════════════════════════════════════════════════════════
    # stratify=labels → cada clase mantiene su proporción 85%-15% en este split.
    # random_state=42 → semilla fija = mismas filas siempre.
    train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(
        paths,
        labels,
        test_size=TEST_RATIO,
        stratify=labels,           # ← clave: mantiene proporciones por clase
        random_state=SEED,         # ← clave: reproducibilidad
    )

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 4 — Segundo split: del 85% restante saca 15% val / 70% train
    # ═══════════════════════════════════════════════════════════════════════
    # 15% / 85% = 0.176 — esa es la proporción relativa al pool restante.
    val_size_relative = VAL_RATIO / (TRAIN_RATIO + VAL_RATIO)
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        train_val_paths,
        train_val_labels,
        test_size=val_size_relative,
        stratify=train_val_labels,
        random_state=SEED,
    )

    def rows(paths_subset: list[Path], labels_subset: list[int]) -> list[tuple[Path, str, int]]:
        return [
            (p, class_names[lab], lab) for p, lab in zip(paths_subset, labels_subset)
        ]

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 5 — Escribir los 4 CSV de salida
    # ═══════════════════════════════════════════════════════════════════════
    # Estos CSV son los "contratos" de reproducibilidad: cualquiera puede
    # clonar el repo y reentrenar con exactamente las mismas imágenes.
    write_manifest(PROCESSED_DIR / "train.csv", rows(train_paths, train_labels))
    write_manifest(PROCESSED_DIR / "val.csv", rows(val_paths, val_labels))
    write_manifest(PROCESSED_DIR / "test.csv", rows(test_paths, test_labels))

    # Reporte de distribución por clase (sirve para auditar el balance).
    distribution = defaultdict(lambda: [0, 0, 0])  # train, val, test
    for lab in train_labels:
        distribution[class_names[lab]][0] += 1
    for lab in val_labels:
        distribution[class_names[lab]][1] += 1
    for lab in test_labels:
        distribution[class_names[lab]][2] += 1

    with (PROCESSED_DIR / "class_distribution.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["class_name", "class_id", "train", "val", "test", "total"])
        for name in class_names:
            t, v, te = distribution[name]
            writer.writerow([name, class_to_id[name], t, v, te, t + v + te])

    print(f"Total samples:   {len(samples)}")
    print(f"Total classes:   {len(class_names)}")
    print(f"Train:           {len(train_paths)} ({len(train_paths)/len(samples):.1%})")
    print(f"Validation:      {len(val_paths)} ({len(val_paths)/len(samples):.1%})")
    print(f"Test:            {len(test_paths)} ({len(test_paths)/len(samples):.1%})")
    print(f"Manifests written to: {PROCESSED_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

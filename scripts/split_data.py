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
SEED = 42
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def discover_images(root: Path) -> list[tuple[Path, str]]:
    """Return (image_path, class_name) tuples for every image under root.

    Assumes one folder per class.
    """
    samples: list[tuple[Path, str]] = []
    for class_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for img in class_dir.iterdir():
            if img.suffix.lower() in IMAGE_EXTENSIONS:
                samples.append((img, class_dir.name))
    return samples


def write_manifest(path: Path, rows: list[tuple[Path, str, int]]) -> None:
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

    # Some Kaggle datasets nest images under an extra folder — detect it.
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

    class_names = sorted({class_name for _, class_name in samples})
    class_to_id = {name: idx for idx, name in enumerate(class_names)}

    paths = [s[0] for s in samples]
    labels = [class_to_id[s[1]] for s in samples]

    # First split off the test set (15%), then split remaining into train/val (~82.4% / 17.6%)
    train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(
        paths,
        labels,
        test_size=TEST_RATIO,
        stratify=labels,
        random_state=SEED,
    )
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

    write_manifest(PROCESSED_DIR / "train.csv", rows(train_paths, train_labels))
    write_manifest(PROCESSED_DIR / "val.csv", rows(val_paths, val_labels))
    write_manifest(PROCESSED_DIR / "test.csv", rows(test_paths, test_labels))

    # Class distribution report
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

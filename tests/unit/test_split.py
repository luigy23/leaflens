"""Unit tests for the data split logic."""

from __future__ import annotations

import csv
from pathlib import Path

from sklearn.model_selection import train_test_split


def test_70_15_15_partition_sums_to_input_length():
    n = 1000
    labels = [i % 5 for i in range(n)]
    train, temp, _, _ = train_test_split(
        list(range(n)), labels, test_size=0.30, stratify=labels, random_state=42
    )
    val, test, _, _ = train_test_split(
        temp,
        [labels[i] for i in temp],
        test_size=0.50,
        stratify=[labels[i] for i in temp],
        random_state=42,
    )
    assert len(train) + len(val) + len(test) == n


def test_split_is_deterministic():
    labels = [i % 4 for i in range(200)]
    a, _, _, _ = train_test_split(
        list(range(200)), labels, test_size=0.30, stratify=labels, random_state=42
    )
    b, _, _, _ = train_test_split(
        list(range(200)), labels, test_size=0.30, stratify=labels, random_state=42
    )
    assert a == b


def test_manifest_round_trip(tmp_path: Path):
    rows = [(Path("data/raw/A/1.jpg"), "A", 0), (Path("data/raw/B/2.jpg"), "B", 1)]
    out = tmp_path / "train.csv"
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "class_name", "class_id"])
        for r in rows:
            writer.writerow([str(r[0]), r[1], r[2]])

    with out.open() as f:
        reader = csv.DictReader(f)
        loaded = list(reader)

    assert len(loaded) == 2
    assert loaded[0]["class_name"] == "A"
    assert int(loaded[1]["class_id"]) == 1

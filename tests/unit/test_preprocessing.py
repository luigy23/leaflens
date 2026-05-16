"""Unit tests for the image preprocessing pipeline."""

from __future__ import annotations

import io

import pytest
from PIL import Image

from models.dataset import build_transforms


def make_image(width: int, height: int) -> bytes:
    img = Image.new("RGB", (width, height), color=(0, 128, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_eval_transform_resizes_to_224():
    transform = build_transforms(training=False)
    img = Image.open(io.BytesIO(make_image(1024, 768))).convert("RGB")
    tensor = transform(img)
    assert tensor.shape == (3, 224, 224)


def test_training_transform_resizes_to_224():
    transform = build_transforms(training=True)
    img = Image.open(io.BytesIO(make_image(1024, 768))).convert("RGB")
    tensor = transform(img)
    assert tensor.shape == (3, 224, 224)


@pytest.mark.parametrize("training", [True, False])
def test_transform_normalizes(training):
    transform = build_transforms(training=training)
    img = Image.open(io.BytesIO(make_image(640, 480))).convert("RGB")
    tensor = transform(img)
    # ImageNet normalization should put values approximately in [-2.5, 2.5].
    assert tensor.min() > -3.0
    assert tensor.max() < 3.0

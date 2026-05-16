"""Factory for the three architectures compared by LeafLens.

All models use ImageNet pretrained weights and have their classification head
replaced with a fresh `num_classes`-way linear layer.
"""

from __future__ import annotations

import timm
import torch
from torch import nn
from torchvision import models as tv_models

SUPPORTED_ARCHS = ("efficientnet", "resnet50", "vit")


def build_model(arch: str, num_classes: int, dropout: float = 0.2) -> nn.Module:
    """Return a model ready for fine-tuning."""
    arch = arch.lower()
    if arch == "efficientnet":
        model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=0)
        in_features = model.num_features
        model.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, num_classes),
        )
        return _EfficientNetWrapper(model, in_features, num_classes, dropout)

    if arch == "resnet50":
        model = tv_models.resnet50(weights=tv_models.ResNet50_Weights.IMAGENET1K_V2)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    if arch == "vit":
        model = timm.create_model(
            "vit_base_patch16_224", pretrained=True, num_classes=num_classes
        )
        return model

    raise ValueError(f"unknown arch '{arch}'. Supported: {SUPPORTED_ARCHS}")


class _EfficientNetWrapper(nn.Module):
    """Wraps a timm EfficientNet so it exposes a unified `.forward(image)` API
    that returns logits."""

    def __init__(self, backbone: nn.Module, in_features: int, num_classes: int, dropout: float):
        super().__init__()
        self.backbone = backbone
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)
        return self.head(features)


def freeze_backbone(model: nn.Module, arch: str) -> None:
    """Freeze every parameter except the new classification head."""
    arch = arch.lower()
    for p in model.parameters():
        p.requires_grad = False
    if arch == "efficientnet":
        for p in model.head.parameters():
            p.requires_grad = True
    elif arch == "resnet50":
        for p in model.fc.parameters():
            p.requires_grad = True
    elif arch == "vit":
        for p in model.head.parameters():
            p.requires_grad = True


def unfreeze_all(model: nn.Module) -> None:
    for p in model.parameters():
        p.requires_grad = True

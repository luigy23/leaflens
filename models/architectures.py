"""Factory for the three architectures compared by LeafLens.

All models use ImageNet pretrained weights and have their classification head
replaced with a fresh `num_classes`-way linear layer.
"""

from __future__ import annotations

import timm
from torch import nn
from torchvision import models as tv_models

SUPPORTED_ARCHS = ("efficientnet", "resnet50", "vit")


def build_model(arch: str, num_classes: int, dropout: float = 0.2) -> nn.Module:
    """Return a model ready for fine-tuning.

    timm handles head replacement automatically when `num_classes` is passed,
    so the only manual case is torchvision's ResNet.
    """
    arch = arch.lower()
    if arch == "efficientnet":
        return timm.create_model(
            "efficientnet_b0",
            pretrained=True,
            num_classes=num_classes,
            drop_rate=dropout,
        )

    if arch == "resnet50":
        model = tv_models.resnet50(weights=tv_models.ResNet50_Weights.IMAGENET1K_V2)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    if arch == "vit":
        return timm.create_model(
            "vit_base_patch16_224",
            pretrained=True,
            num_classes=num_classes,
            drop_rate=dropout,
        )

    raise ValueError(f"unknown arch '{arch}'. Supported: {SUPPORTED_ARCHS}")


def _is_head_param_name(arch: str, name: str) -> bool:
    """Return True if a parameter name refers to the classification head."""
    arch = arch.lower()
    if arch == "efficientnet":
        # timm EfficientNet head is `classifier.*`
        return name.startswith("classifier")
    if arch == "resnet50":
        return name.startswith("fc")
    if arch == "vit":
        # timm ViT head is `head.*`
        return name.startswith("head")
    return False


def freeze_backbone(model: nn.Module, arch: str) -> None:
    """Freeze every parameter except the classification head."""
    for name, p in model.named_parameters():
        p.requires_grad = _is_head_param_name(arch, name)


def unfreeze_all(model: nn.Module) -> None:
    for p in model.parameters():
        p.requires_grad = True


def head_and_backbone_params(model: nn.Module, arch: str):
    """Return (head_params, backbone_params) for differential LR setups."""
    head, backbone = [], []
    for name, p in model.named_parameters():
        if _is_head_param_name(arch, name):
            head.append(p)
        else:
            backbone.append(p)
    return head, backbone

"""Factory for the three architectures compared by LeafLens.

All models use ImageNet pretrained weights and have their classification head
replaced with a fresh `num_classes`-way linear layer.

═══════════════════════════════════════════════════════════════════════════
  PIPELINE — sigue PASO 1 .. PASO 4
═══════════════════════════════════════════════════════════════════════════
  PASO 1 — Factory: build_model(arch) decide qué arquitectura instanciar
  PASO 2 — Cargar pesos preentrenados de ImageNet (transfer learning)
  PASO 3 — Reemplazar la cabeza (head) por una capa de 47 salidas
  PASO 4 — Helpers para congelar/descongelar el backbone
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import timm
from torch import nn
from torchvision import models as tv_models

# Las tres arquitecturas que comparamos (rubric exige mínimo 3 modelos).
SUPPORTED_ARCHS = ("efficientnet", "resnet50", "vit")


# ═══════════════════════════════════════════════════════════════════════════
#  PASO 1 — Factory: elige cuál de los 3 modelos construir
# ═══════════════════════════════════════════════════════════════════════════
def build_model(arch: str, num_classes: int, dropout: float = 0.2) -> nn.Module:
    """Return a model ready for fine-tuning.

    timm handles head replacement automatically when `num_classes` is passed,
    so the only manual case is torchvision's ResNet.
    """
    arch = arch.lower()

    # ─── EfficientNet-B0 (4.1 M params · CNN ligera) ──────────────────────
    if arch == "efficientnet":
        # ── PASO 2 ── Carga pesos ImageNet · ── PASO 3 ── reemplaza head a num_classes
        return timm.create_model(
            "efficientnet_b0",
            pretrained=True,         # ← PASO 2: pesos preentrenados de ImageNet
            num_classes=num_classes, # ← PASO 3: head nuevo de 47 salidas
            drop_rate=dropout,
        )

    # ─── ResNet-50 (23.6 M params · CNN clásica) ──────────────────────────
    if arch == "resnet50":
        # PASO 2: torchvision con pesos V2 (más fuertes que V1)
        model = tv_models.resnet50(weights=tv_models.ResNet50_Weights.IMAGENET1K_V2)
        # PASO 3: torchvision no acepta num_classes, así que reemplazamos
        # manualmente el `fc` (fully connected) por Dropout + Linear(in→47).
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, num_classes),
        )
        return model

    # ─── ViT-Base/16 (85.8 M params · Vision Transformer) ─────────────────
    if arch == "vit":
        # ── PASO 2 ── pesos ImageNet · ── PASO 3 ── head a num_classes
        return timm.create_model(
            "vit_base_patch16_224",
            pretrained=True,
            num_classes=num_classes,
            drop_rate=dropout,
        )

    raise ValueError(f"unknown arch '{arch}'. Supported: {SUPPORTED_ARCHS}")


# ═══════════════════════════════════════════════════════════════════════════
#  PASO 4 — Helpers para congelar / descongelar el backbone
# ═══════════════════════════════════════════════════════════════════════════
# Estrategia de warm-up:
#   • Fase A (primeras 3 epochs): solo entrena la cabeza con lr alto.
#   • Fase B (resto): unfreeze_all() libera todo el backbone con lr más bajo.
# Esto evita que gradientes ruidosos al inicio destruyan las features
# preentrenadas del backbone.


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
    """Freeze every parameter except the classification head.

    Llamado al inicio del entrenamiento (Fase A: warm-up).
    """
    for name, p in model.named_parameters():
        p.requires_grad = _is_head_param_name(arch, name)


def unfreeze_all(model: nn.Module) -> None:
    """Libera TODOS los parámetros para fine-tuning completo (Fase B)."""
    for p in model.parameters():
        p.requires_grad = True


def head_and_backbone_params(model: nn.Module, arch: str):
    """Return (head_params, backbone_params) for differential LR setups.

    Usado en train.py para asignar learning rates distintos al backbone
    (lento: 1e-4) y al head (rápido: 1e-3) en la Fase B.
    """
    head, backbone = [], []
    for name, p in model.named_parameters():
        if _is_head_param_name(arch, name):
            head.append(p)
        else:
            backbone.append(p)
    return head, backbone

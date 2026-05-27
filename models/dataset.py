"""PyTorch dataset and transforms for the House Plant Species corpus.

═══════════════════════════════════════════════════════════════════════════
  PIPELINE — sigue PASO 1 .. PASO 3
═══════════════════════════════════════════════════════════════════════════
  PASO 1 — Transforms (con augmentation solo en training)
  PASO 2 — Dataset que lee el manifest CSV generado por split_data.py
  PASO 3 — __getitem__: lee imagen → aplica transform → devuelve (tensor, label)
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

# Constantes de normalización estándar de ImageNet — los modelos preentrenados
# fueron entrenados con estas medias y desviaciones, así que las imágenes nuevas
# deben normalizarse igual.
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


# ═══════════════════════════════════════════════════════════════════════════
#  PASO 1 — Transforms (training tiene augmentation, validation no)
# ═══════════════════════════════════════════════════════════════════════════
def build_transforms(image_size: int = 224, training: bool = False) -> transforms.Compose:
    """Return a torchvision transform pipeline.

    Training pipeline includes augmentation; eval pipeline is deterministic.
    """
    if training:
        # PIPELINE DE AUGMENTATION (solo para entrenamiento):
        #   1. Resize a 256px (un poco más grande que el target)
        #   2. RandomResizedCrop → recorte aleatorio + reescalado a 224×224
        #      (zoom in/out aleatorio, escala 80%-100%)
        #   3. HorizontalFlip → espejo horizontal con probabilidad 50%
        #   4. RandomRotation ±15° → rota la imagen aleatoriamente
        #   5. ColorJitter → variaciones de brillo/contraste/saturación ±10%
        #   6. ToTensor → convierte PIL Image a tensor [C, H, W]
        #   7. Normalize → resta mean y divide por std de ImageNet
        return transforms.Compose(
            [
                transforms.Resize(image_size + 32),
                transforms.RandomResizedCrop(image_size, scale=(0.8, 1.0)),
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(15),
                transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
                transforms.ToTensor(),
                transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
            ]
        )
    # PIPELINE DETERMINISTA (para validation y test):
    #   solo resize + center crop + normalize — sin aleatoriedad para que
    #   las métricas sean reproducibles.
    return transforms.Compose(
        [
            transforms.Resize(image_size + 32),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ]
    )


# ═══════════════════════════════════════════════════════════════════════════
#  PASO 2 — Dataset PyTorch que lee el manifest CSV
# ═══════════════════════════════════════════════════════════════════════════
class PlantImageDataset(Dataset):
    """Reads images from a manifest CSV produced by scripts/split_data.py.

    El manifest tiene tres columnas: image_path, class_name, class_id.
    Cada fila representa una imagen del split (train/val/test).
    """

    def __init__(self, manifest_path: Path, repo_root: Path, transform=None):
        # Lee el CSV una sola vez al inicio — luego cada __getitem__ solo
        # mira una fila del DataFrame.
        self.manifest = pd.read_csv(manifest_path)
        self.repo_root = repo_root
        self.transform = transform

    def __len__(self) -> int:
        return len(self.manifest)

    # ═══════════════════════════════════════════════════════════════════════
    #  PASO 3 — __getitem__: lee imagen + aplica transform + devuelve tensor
    # ═══════════════════════════════════════════════════════════════════════
    # PyTorch llama este método cada vez que el DataLoader necesita un sample.
    # El sampler (PASO 3 de train.py) decide qué `idx` pedir para balancear.
    def __getitem__(self, idx: int):
        row = self.manifest.iloc[idx]
        image_path = self.repo_root / row["image_path"]
        image = Image.open(image_path).convert("RGB")        # carga + RGB
        if self.transform is not None:
            image = self.transform(image)                     # augment + normalize
        return image, int(row["class_id"])                    # (tensor, label)

    @property
    def num_classes(self) -> int:
        return int(self.manifest["class_id"].max() + 1)

    @property
    def class_names(self) -> list[str]:
        return (
            self.manifest[["class_id", "class_name"]]
            .drop_duplicates()
            .sort_values("class_id")["class_name"]
            .tolist()
        )

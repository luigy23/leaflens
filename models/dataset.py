"""PyTorch dataset and transforms for the House Plant Species corpus."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def build_transforms(image_size: int = 224, training: bool = False) -> transforms.Compose:
    """Return a torchvision transform pipeline.

    Training pipeline includes augmentation; eval pipeline is deterministic.
    """
    if training:
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
    return transforms.Compose(
        [
            transforms.Resize(image_size + 32),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ]
    )


class PlantImageDataset(Dataset):
    """Reads images from a manifest CSV produced by scripts/split_data.py."""

    def __init__(self, manifest_path: Path, repo_root: Path, transform=None):
        self.manifest = pd.read_csv(manifest_path)
        self.repo_root = repo_root
        self.transform = transform

    def __len__(self) -> int:
        return len(self.manifest)

    def __getitem__(self, idx: int):
        row = self.manifest.iloc[idx]
        image_path = self.repo_root / row["image_path"]
        image = Image.open(image_path).convert("RGB")
        if self.transform is not None:
            image = self.transform(image)
        return image, int(row["class_id"])

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

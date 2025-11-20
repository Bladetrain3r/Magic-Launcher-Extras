"""Feature extraction helpers for SOM-guided diffusion experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image

Array = np.ndarray


def load_image(path: Path) -> Array:
    """Load an image as an RGB float32 array in [0, 1]."""
    image = Image.open(path).convert("RGB")
    return np.asarray(image, dtype=np.float32) / 255.0


def generate_demo_image(size: Tuple[int, int] = (64, 64)) -> Array:
    """Return a simple RGB gradient square useful for tests/demos."""
    height, width = size
    y = np.linspace(0.0, 1.0, num=height, dtype=np.float32)
    x = np.linspace(0.0, 1.0, num=width, dtype=np.float32)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    red = xx
    green = yy
    blue = 1.0 - 0.5 * (xx + yy)
    return np.stack([red, green, blue], axis=-1)


def extract_color_position_features(image: Array) -> Array:
    """Flatten RGB pixels and append normalized XY coordinates."""
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected image shaped (H, W, 3)")
    height, width, _ = image.shape
    y_coords, x_coords = np.indices((height, width), dtype=np.float32)
    x_norm = (x_coords / max(width - 1, 1)).reshape(-1, 1)
    y_norm = (y_coords / max(height - 1, 1)).reshape(-1, 1)
    rgb = image.reshape(-1, 3)
    return np.concatenate([rgb, x_norm, y_norm], axis=1)


def save_image(array: Array, path: Path) -> None:
    """Persist a float RGB array in [0, 1] to disk."""
    clipped = np.clip(array * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(clipped).save(path)

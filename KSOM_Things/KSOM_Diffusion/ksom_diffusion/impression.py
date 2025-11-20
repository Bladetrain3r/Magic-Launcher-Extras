"""Utilities that translate SOM weights into impression maps."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image

Array = np.ndarray


def weights_to_impression(weights: Array, target_shape: Tuple[int, int] | None = None) -> Array:
    """Return an RGB float image derived from SOM weights."""
    if weights.ndim != 3 or weights.shape[2] < 3:
        raise ValueError("Weights must be shaped (H, W, >=3)")
    rgb = np.clip(weights[..., :3], 0.0, 1.0)
    image = Image.fromarray((rgb * 255.0).astype(np.uint8), mode="RGB")
    if target_shape:
        height, width = target_shape
        image = image.resize((width, height), resample=Image.BILINEAR)
    return np.asarray(image, dtype=np.float32) / 255.0


def save_impression(weights: Array, path: Path, target_shape: Tuple[int, int] | None = None) -> None:
    array = weights_to_impression(weights, target_shape)
    Image.fromarray((array * 255.0).astype(np.uint8), mode="RGB").save(path)

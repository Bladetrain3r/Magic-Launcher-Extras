"""Simple numpy Self-Organizing Map implementation for experimentation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

Array = np.ndarray


@dataclass
class TrainingStats:
    epochs: int
    updates: int
    initial_error: float
    final_error: float


class SelfOrganizingMap:
    """Lightweight SOM supporting rectangular grids."""

    def __init__(
        self,
        height: int,
        width: int,
        feature_dim: int,
        learning_rate: float = 0.6,
        sigma: float | None = None,
        seed: int | None = None,
    ) -> None:
        if height <= 0 or width <= 0:
            raise ValueError("Grid dimensions must be positive")
        self.height = height
        self.width = width
        self.feature_dim = feature_dim
        self.initial_learning_rate = learning_rate
        self.initial_sigma = sigma or max(height, width) / 2.0
        self.rng = np.random.default_rng(seed)
        self.weights = self.rng.random((height, width, feature_dim), dtype=np.float32)
        self._grid_y, self._grid_x = np.indices((height, width), dtype=np.float32)

    def train(self, data: Array, epochs: int = 1, verbose: bool = False) -> TrainingStats:
        if data.ndim != 2 or data.shape[1] != self.feature_dim:
            raise ValueError("Data must be shaped (N, feature_dim)")
        total_updates = 0
        initial_error = self.quantization_error(data)
        for epoch in range(epochs):
            lr = self._decay(self.initial_learning_rate, epoch, epochs)
            sigma = self._decay(self.initial_sigma, epoch, epochs)
            order = self.rng.permutation(data.shape[0])
            for idx in order:
                self._update(data[idx], lr, sigma)
                total_updates += 1
            if verbose:
                current_error = self.quantization_error(data)
                print(f"epoch={epoch+1}/{epochs} lr={lr:.3f} sigma={sigma:.3f} qe={current_error:.4f}")
        final_error = self.quantization_error(data)
        return TrainingStats(epochs=epochs, updates=total_updates, initial_error=initial_error, final_error=final_error)

    def quantization_error(self, data: Array) -> float:
        errors = []
        for vector in data:
            _, dist = self.best_matching_unit(vector)
            errors.append(dist)
        return float(np.mean(errors)) if errors else 0.0

    def best_matching_unit(self, vector: Array) -> Tuple[Tuple[int, int], float]:
        diff = self.weights - vector.reshape(1, 1, -1)
        dist_sq = np.sum(diff * diff, axis=2)
        flat_index = int(np.argmin(dist_sq))
        y, x = divmod(flat_index, self.width)
        return (y, x), float(np.sqrt(dist_sq[y, x]))

    def _update(self, vector: Array, learning_rate: float, sigma: float) -> None:
        (bmu_y, bmu_x), _ = self.best_matching_unit(vector)
        distance_sq = (self._grid_y - bmu_y) ** 2 + (self._grid_x - bmu_x) ** 2
        influence = np.exp(-distance_sq / (2.0 * sigma * sigma))
        influence = influence[..., None]
        delta = vector.reshape(1, 1, -1) - self.weights
        self.weights += learning_rate * influence * delta

    @staticmethod
    def _decay(initial: float, epoch: int, total_epochs: int) -> float:
        remaining = max(total_epochs - 1, 1)
        fraction = epoch / remaining
        return initial * (1.0 - 0.9 * fraction)

    def snapshot(self, limit: int = 5) -> Dict[str, object]:
        sample = self.weights.reshape(-1, self.feature_dim)[:limit]
        return {
            "grid": [self.height, self.width],
            "feature_dim": self.feature_dim,
            "initial_learning_rate": self.initial_learning_rate,
            "initial_sigma": self.initial_sigma,
            "sample_weights": sample.tolist(),
        }

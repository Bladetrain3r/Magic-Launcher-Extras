"""Command-line glue for the KSOM diffusion prototype."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

from .features import extract_color_position_features, generate_demo_image, load_image
from .impression import save_impression
from .som import SelfOrganizingMap


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a SOM impression map from an image.")
    parser.add_argument("--image", type=Path, help="Path to an input image (PNG/JPG).")
    parser.add_argument("--demo", action="store_true", help="Ignore --image and use a generated gradient.")
    parser.add_argument("--grid", nargs=2, type=int, metavar=("H", "W"), default=(16, 16), help="SOM grid height/width.")
    parser.add_argument("--epochs", type=int, default=2, help="Number of training epochs.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Directory for artifacts.")
    parser.add_argument("--save-brain", type=Path, help="Optional JSON brain snapshot path.")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility.")
    parser.add_argument("--verbose", action="store_true", help="Print per-epoch stats.")
    return parser


def main(args: list[str] | None = None) -> None:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.demo and not parsed.image:
        parser.error("Provide --image or --demo")

    if parsed.demo:
        image = generate_demo_image()
        image_path = Path("demo-gradient")
    else:
        image_path = parsed.image
        if not image_path.exists():
            parser.error(f"Image not found: {image_path}")
        image = load_image(image_path)

    features = extract_color_position_features(image)
    som = SelfOrganizingMap(
        height=parsed.grid[0],
        width=parsed.grid[1],
        feature_dim=features.shape[1],
        seed=parsed.seed,
    )

    parsed.output_dir.mkdir(parents=True, exist_ok=True)
    impression_path = parsed.output_dir / f"{image_path.stem}_impression.png"

    start = time.time()
    stats = som.train(features, epochs=parsed.epochs, verbose=parsed.verbose)
    elapsed = time.time() - start

    save_impression(som.weights, impression_path, target_shape=image.shape[:2])

    if parsed.save_brain:
        brain_path = parsed.save_brain
        brain_data = {
            "image": str(image_path),
            "features": features.shape[0],
            "grid": [parsed.grid[0], parsed.grid[1]],
            "training": stats.__dict__,
            "snapshot": som.snapshot(),
        }
        brain_path.parent.mkdir(parents=True, exist_ok=True)
        brain_path.write_text(json.dumps(brain_data, indent=2))

    summary = (
        f"samples={features.shape[0]} grid={parsed.grid[0]}x{parsed.grid[1]} "
        f"epochs={parsed.epochs} qe={stats.final_error:.4f} time={elapsed:.2f}s"
    )
    print(summary)


if __name__ == "__main__":  # pragma: no cover
    main()

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ksom_diffusion.features import extract_color_position_features, generate_demo_image
from ksom_diffusion.som import SelfOrganizingMap


class FeatureTests(unittest.TestCase):
    def test_feature_packing_shape(self) -> None:
        image = generate_demo_image((8, 8))
        features = extract_color_position_features(image)
        self.assertEqual(features.shape, (64, 5))


class SomTrainingTests(unittest.TestCase):
    def test_som_training_reduces_error(self) -> None:
        image = generate_demo_image((10, 10))
        features = extract_color_position_features(image)
        som = SelfOrganizingMap(6, 6, features.shape[1], seed=7)
        before = som.quantization_error(features)
        stats = som.train(features, epochs=1)
        after = stats.final_error
        self.assertLessEqual(after, before)


class CliTests(unittest.TestCase):
    def test_cli_demo_run(self) -> None:
        with TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "artifacts"
            cmd = [
                sys.executable,
                "-m",
                "ksom_diffusion",
                "--demo",
                "--epochs",
                "1",
                "--grid",
                "4",
                "4",
                "--output-dir",
                str(out_dir),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertIn("grid=4x4", result.stdout)
            images = list(out_dir.glob("*_impression.png"))
            self.assertTrue(images, "Expected impression output image")

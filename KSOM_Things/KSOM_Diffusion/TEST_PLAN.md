# Test Guidestones

These one-liner checks keep the prototype honest while we iterate quickly.

1. `unit:som_tiny_grid` - training a 4x4 SOM on a synthetic gradient should reduce quantization error after one epoch.
2. `unit:feature_packing` - extracting color+position features from a generated image should yield Nx5 vectors matching pixel count.
3. `cli:dry_run_output` - running `python -m ksom_diffusion --image demo.png --epochs 1 --grid 8 8` should emit progress logs and produce an impression PNG in the output folder.
4. `cli:brain_snapshot` - invoking the CLI with `--save-brain brain.json` should write a JSON file containing grid metadata and sample weights.
5. `cli:stdout_summary` - CLI should print a single-line summary of feature count, grid size, and training time.

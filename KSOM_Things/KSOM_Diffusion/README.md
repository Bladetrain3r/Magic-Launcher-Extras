# KSOM Diffusion Prototype

A minimal sandbox for testing Self-Organizing Map (SOM) impression maps as structural priors for diffusion systems. The code favors plain modules, CLI ergonomics, and a short feedback loop.

## Layout

- `ksom_diffusion/features.py` - image loading and color+position feature packing.
- `ksom_diffusion/som.py` - lightweight numpy SOM implementation with stats helpers.
- `ksom_diffusion/impression.py` - convert trained weights into coarse RGB maps.
- `ksom_diffusion/cli.py` - glue CLI (`python -m ksom_diffusion`).
- `tests/` - stdlib `unittest`-friendly smoke tests plus CLI invocation.
- `TEST_PLAN.md` - one-line guidestone tests for quick validation.

## Quick Start

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m ksom_diffusion --demo --grid 8 8 --epochs 2 --output-dir outputs --save-brain brains/demo.json
```

The command above trains on a synthetic gradient, saves an impression PNG under `outputs/`, and records a JSON brain snapshot.

To run on your own image:

```bash
python -m ksom_diffusion --image path/to/photo.png --grid 32 32 --epochs 3 --output-dir runs/photo
```

## Tests

Tests are intentionally small and map directly to the entries inside `TEST_PLAN.md`.

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Next Steps

- Experiment with alternative feature packs (edges, luminance, etc.).
- Emit multi-channel impression maps suited for ControlNet adapters.
- Add Kuramoto-style temporal evolution once the static pipeline feels solid.

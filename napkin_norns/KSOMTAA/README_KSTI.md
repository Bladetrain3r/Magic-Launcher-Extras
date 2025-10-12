
# KSTI — Kuramoto-SOM Temporal Interpolator (Prototype)

Deterministic, phase-coherent frame interpolation using oscillator dynamics + edge-aware coupling.
No training, no optical flow. Early prototype for experimentation.

## Usage

```bash
python ksti.py input.mp4 output.mp4 --step 1  # insert one midframe between every pair
```

- Works on color inputs (RGB reconstructed from luminance + chroma guidance).
- Includes circular phase interpolation (slerp), adaptive coupling, EMA, linear-light processing, local gain normalization.
- Expect non–real-time performance; this is a CPU prototype.

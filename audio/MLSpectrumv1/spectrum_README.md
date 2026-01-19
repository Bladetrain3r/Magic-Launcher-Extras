# Spectrum Visualizer - Magic Launcher Edition

A configurable audio spectrum visualizer for recording video backgrounds.

## Installation

```bash
# Install dependencies
pip install sounddevice numpy pygame pillow --break-system-packages

# On Debian/Ubuntu, you may also need:
sudo apt install python3-dev libportaudio2
```

## Usage

```bash
# List available audio devices
python spectrum.py

# Run with a specific device (use the monitor/loopback device)
python spectrum.py 5

# Show current config
python spectrum.py --config
```

## Finding the Right Device

Run `python spectrum.py` to list devices. Look for something like:
- "Monitor of Built-in Audio" (PulseAudio)
- "pulse monitor" 
- Anything with "monitor" or "loopback" in the name

This captures what's playing on your speakers.

## Configuration

Edit the `CONFIG` dict at the top of `spectrum.py`:

### Audio
- `sample_rate`: Usually 44100
- `chunk_size`: Larger = smoother but more latency (1024-4096)
- `bands`: Number of frequency bars (1-80)
- `min_freq` / `max_freq`: Frequency range in Hz
- `log_scale`: True for logarithmic (more musical), False for linear

### Visual
- `width` / `height`: Window size
- `fps`: Target framerate
- `fullscreen`: Start fullscreen

### Bars
- `bar_color`: RGB tuple for bar color
- `bar_color_top`: RGB for gradient top (if gradient=True)
- `gradient`: Enable gradient coloring based on amplitude
- `bar_width_ratio`: How much of each band the bar fills (0.1-1.0)
- `bar_max_height`: Max height as ratio of window (0.5-1.0)
- `opacity`: Bar transparency (0-255)

### Background
- `background_image`: Path to image file, or None
- `background_color`: RGB for solid background (if no image)

### Smoothing
- `smoothing`: Legacy (unused, kept for compat)
- `attack`: How fast bars rise (0.1 = slow, 0.9 = snappy)
- `decay`: How fast bars fall (0.1 = slow fall, 0.5 = quick)

### Amplitude
- `gain`: Multiply signal (increase if bars are too short)
- `noise_floor`: Minimum threshold (increase if flickery when quiet)

## Controls

- `ESC` - Quit
- `F` - Toggle fullscreen

## Recording Tips

1. Set resolution to match your video project (e.g., 1920x1080)
2. Use OBS or similar to capture the window
3. For transparent overlay, record with a solid green/blue background and chroma key

## Example Configs

### Chill Lo-Fi
```python
"bands": 32,
"bar_color": (100, 80, 150),
"bar_color_top": (200, 100, 200),
"attack": 0.3,
"decay": 0.1,
```

### Aggressive EDM
```python
"bands": 64,
"bar_color": (0, 255, 100),
"bar_color_top": (255, 50, 50),
"attack": 0.9,
"decay": 0.4,
```

### Minimal
```python
"bands": 16,
"gradient": False,
"bar_color": (255, 255, 255),
"bar_width_ratio": 0.4,
```

#!/usr/bin/env python3
"""
Spectrum Visualizer - Magic Launcher Edition
A configurable audio spectrum visualizer for recording backgrounds.

Dependencies:
    pip install sounddevice numpy pygame pillow

Usage:
    python spectrum.py                    # List audio devices
    python spectrum.py <device_index>     # Run with specific device
    python spectrum.py pulse              # Use PulseAudio monitor (recommended!)
    python spectrum.py --config           # Show current config
    python spectrum.py --list-pulse       # List PulseAudio sources
"""

import sys
import subprocess
import threading
import queue
import numpy as np

# ============================================================================
# CONFIGURATION - Edit these to taste
# ============================================================================

CONFIG = {
    # Audio settings
    "sample_rate": 48000,
    "chunk_size": 1024,          # Larger = smoother but more latency
    "device": None,              # Set via command line, or hardcode index here
    
    # Spectrum settings
    "bands": 40,                 # Number of frequency bands (1-80)
    "min_freq": 40,              # Minimum frequency (Hz)
    "max_freq": 16000,           # Maximum frequency (Hz)
    "log_scale": False,           # Logarithmic frequency distribution
    
    # Visual settings
    "width": 1920,
    "height": 1080,
    "fps": 60,
    "fullscreen": False,
    
    # Bar appearance
    "bar_color": (0, 255, 170),  # RGB - cyan-ish green
    "bar_color_top": (255, 0, 170),  # RGB - gradient top (magenta)
    "gradient": True,            # Use gradient coloring
    "bar_width_ratio": 0.8,      # Bar width as ratio of band width (0.1-1.0)
    "bar_max_height": 0.85,      # Max bar height as ratio of window height
    "opacity": 165,              # Bar opacity (0-255)
    
    # Background
    "background_image": "fsfv2.jpg",    # Path to image, or None for solid color
    "background_color": (10, 10, 20),  # RGB if no image
    
    # Smoothing
    "smoothing": 0.3,            # 0 = no smoothing, 0.9 = very smooth
    "attack": 0.8,               # How fast bars rise (0-1)
    "decay": 0.2,                # How fast bars fall (0-1)
    
    # Amplitude
    "gain": 3.0,                 # Multiply signal strength
    "noise_floor": 0.001,         # Minimum threshold (reduces noise flicker)
}

# ============================================================================
# AUDIO CAPTURE
# ============================================================================

class AudioCapture:
    def __init__(self, device_index, sample_rate, chunk_size):
        import sounddevice as sd
        self.sd = sd
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.buffer = queue.Queue(maxsize=4)
        self.running = False
        self.stream = None
        
    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}", file=sys.stderr)
        # Take mono mix if stereo
        if len(indata.shape) > 1:
            mono = np.mean(indata, axis=1)
        else:
            mono = indata.flatten()
        
        try:
            self.buffer.put_nowait(mono.copy())
        except queue.Full:
            pass  # Drop frame if we're behind
    
    def start(self):
        self.running = True
        self.stream = self.sd.InputStream(
            device=self.device_index,
            channels=2,  # Capture stereo, mix to mono
            samplerate=self.sample_rate,
            blocksize=self.chunk_size,
            callback=self.audio_callback
        )
        self.stream.start()
        
    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
    
    def get_chunk(self):
        try:
            return self.buffer.get_nowait()
        except queue.Empty:
            return None


class PulseAudioCapture:
    """Capture system audio via PulseAudio using parec"""
    
    def __init__(self, sample_rate, chunk_size, source=None):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.source = source  # None = default monitor
        self.buffer = queue.Queue(maxsize=4)
        self.running = False
        self.process = None
        self.thread = None
    
    def _find_monitor_source(self):
        """Find the default output's monitor source"""
        try:
            # Get default sink
            result = subprocess.run(
                ["pactl", "get-default-sink"],
                capture_output=True, text=True
            )
            default_sink = result.stdout.strip()
            
            # Monitor source is sink name + .monitor
            return f"{default_sink}.monitor"
        except Exception as e:
            print(f"Could not find default monitor: {e}", file=sys.stderr)
            return None
    
    def _capture_thread(self):
        """Thread that reads from parec and fills buffer"""
        bytes_per_sample = 2  # 16-bit
        channels = 2
        bytes_per_frame = bytes_per_sample * channels
        chunk_bytes = self.chunk_size * bytes_per_frame
        
        while self.running and self.process:
            try:
                data = self.process.stdout.read(chunk_bytes)
                if not data:
                    break
                
                # Convert bytes to numpy array
                # parec outputs signed 16-bit little-endian
                samples = np.frombuffer(data, dtype=np.int16)
                
                # Normalize to -1.0 to 1.0
                samples = samples.astype(np.float32) / 32768.0
                
                # Reshape to stereo and mix to mono
                if len(samples) >= channels:
                    samples = samples.reshape(-1, channels)
                    mono = np.mean(samples, axis=1)
                else:
                    mono = samples
                
                try:
                    self.buffer.put_nowait(mono)
                except queue.Full:
                    pass
                    
            except Exception as e:
                if self.running:
                    print(f"Capture error: {e}", file=sys.stderr)
                break
    
    def start(self):
        source = self.source or self._find_monitor_source()
        if not source:
            raise RuntimeError("No PulseAudio monitor source found")
        
        print(f"Capturing from: {source}")
        
        # Start parec process
        cmd = [
            "parec",
            "--rate", str(self.sample_rate),
            "--channels", "2",
            "--format", "s16le",
            "--device", source,
            "--latency-msec", "50"
        ]
        
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_thread, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()
            self.process.wait()
        if self.thread:
            self.thread.join(timeout=1.0)
    
    def get_chunk(self):
        try:
            return self.buffer.get_nowait()
        except queue.Empty:
            return None

# ============================================================================
# SPECTRUM ANALYSIS
# ============================================================================

class SpectrumAnalyzer:
    def __init__(self, config):
        self.config = config
        self.bands = config["bands"]
        self.sample_rate = config["sample_rate"]
        self.chunk_size = config["chunk_size"]
        
        # Pre-calculate frequency bin edges
        if config["log_scale"]:
            self.freq_edges = np.logspace(
                np.log10(config["min_freq"]),
                np.log10(config["max_freq"]),
                self.bands + 1
            )
        else:
            self.freq_edges = np.linspace(
                config["min_freq"],
                config["max_freq"],
                self.bands + 1
            )
        
        # FFT frequency bins
        self.fft_freqs = np.fft.rfftfreq(self.chunk_size, 1.0 / self.sample_rate)
        
        # Pre-calculate which FFT bins go into which band
        self.band_bins = []
        for i in range(self.bands):
            low = self.freq_edges[i]
            high = self.freq_edges[i + 1]
            bins = np.where((self.fft_freqs >= low) & (self.fft_freqs < high))[0]
            self.band_bins.append(bins)
            
        for i in range(len(self.band_bins) - 1):
            if len(self.band_bins[i]) == 0:
                self.band_bins[i] = self.band_bins[i+1]
                self.band_bins[i+1] = np.array([], dtype=int)
        
        # Smoothed output
        self.smoothed = np.zeros(self.bands)
        
        # Window function for FFT
        self.window = np.hanning(self.chunk_size)
    
    def analyze(self, audio_chunk):
        if audio_chunk is None or len(audio_chunk) < self.chunk_size:
            return self.smoothed
        
        # Apply window and FFT
        windowed = audio_chunk[:self.chunk_size] * self.window
        # fft = np.abs(np.fft.rfft(windowed))
        fft = np.abs(np.fft.rfft(windowed, n=self.chunk_size * 4))
        
        # Normalize
        fft = fft / self.chunk_size
        
        # Apply gain
        fft = fft * self.config["gain"]
        
        # Bin into bands
        band_values = np.zeros(self.bands)
        for i, bins in enumerate(self.band_bins):
            if len(bins) > 0:
                band_values[i] = np.mean(fft[bins])
        
        # Apply noise floor
        band_values = np.maximum(0, band_values - self.config["noise_floor"])
        
        # Convert to dB-ish scale (more perceptually linear)
        band_values = np.sqrt(band_values)  # Softer than log, looks better
        
        # Clamp to 0-1 range
        band_values = np.clip(band_values, 0, 1)
        
        # Apply attack/decay smoothing
        attack = self.config["attack"]
        decay = self.config["decay"]
        
        for i in range(self.bands):
            if band_values[i] > self.smoothed[i]:
                self.smoothed[i] += (band_values[i] - self.smoothed[i]) * attack
            else:
                self.smoothed[i] += (band_values[i] - self.smoothed[i]) * decay
        
        return self.smoothed

# ============================================================================
# RENDERER
# ============================================================================

class SpectrumRenderer:
    def __init__(self, config):
        import pygame
        self.pygame = pygame
        self.config = config
        
        pygame.init()
        
        flags = 0
        if config["fullscreen"]:
            flags |= pygame.FULLSCREEN
        
        self.screen = pygame.display.set_mode(
            (config["width"], config["height"]),
            flags
        )
        pygame.display.set_caption("Spectrum Visualizer")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load background image if specified
        self.background = None
        if config["background_image"]:
            try:
                img = pygame.image.load(config["background_image"])
                self.background = pygame.transform.scale(
                    img, (config["width"], config["height"])
                )
            except Exception as e:
                print(f"Could not load background: {e}", file=sys.stderr)
        
        # Create surface for bars (with alpha)
        self.bar_surface = pygame.Surface(
            (config["width"], config["height"]),
            pygame.SRCALPHA
        )
    
    def handle_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.running = False
            elif event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_ESCAPE:
                    self.running = False
                elif event.key == self.pygame.K_f:
                    self.pygame.display.toggle_fullscreen()
    
    def lerp_color(self, c1, c2, t):
        """Linearly interpolate between two colors"""
        return (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )
    
    def render(self, band_values):
        config = self.config
        width = config["width"]
        height = config["height"]
        bands = config["bands"]
        opacity = config["opacity"]
        
        # Clear bar surface
        self.bar_surface.fill((0, 0, 0, 0))
        
        # Calculate bar dimensions
        total_bar_width = width / bands
        bar_width = int(total_bar_width * config["bar_width_ratio"])
        bar_gap = (total_bar_width - bar_width) / 2
        max_height = int(height * config["bar_max_height"])
        
        # Draw bars
        for i, value in enumerate(band_values):
            bar_height = int(value * max_height)
            if bar_height < 2:
                bar_height = 2  # Minimum visible height
            
            x = int(i * total_bar_width + bar_gap)
            y = height - bar_height
            
            # Color (gradient or solid)
            if config["gradient"]:
                color = self.lerp_color(
                    config["bar_color"],
                    config["bar_color_top"],
                    value
                )
            else:
                color = config["bar_color"]
            
            # Add alpha
            color_with_alpha = (*color, opacity)
            
            self.pygame.draw.rect(
                self.bar_surface,
                color_with_alpha,
                (x, y, bar_width, bar_height)
            )
        
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(config["background_color"])
        
        # Draw bars on top
        self.screen.blit(self.bar_surface, (0, 0))
        
        self.pygame.display.flip()
        self.clock.tick(config["fps"])
    
    def quit(self):
        self.pygame.quit()

# ============================================================================
# MAIN
# ============================================================================

def list_devices():
    import sounddevice as sd
    print("\nAvailable audio devices (ALSA):\n")
    print(sd.query_devices())
    print("\n" + "="*60)
    print("TIP: For system audio capture, use: python spectrum.py pulse")
    print("This uses PulseAudio monitor (works with Bluetooth!)")
    print("="*60)

def list_pulse_sources():
    """List PulseAudio sources"""
    print("\nPulseAudio sources:\n")
    try:
        result = subprocess.run(
            ["pactl", "list", "sources", "short"],
            capture_output=True, text=True
        )
        print(result.stdout)
        
        # Also show default
        result = subprocess.run(
            ["pactl", "get-default-sink"],
            capture_output=True, text=True
        )
        default_sink = result.stdout.strip()
        print(f"\nDefault sink: {default_sink}")
        print(f"Monitor source: {default_sink}.monitor")
        print("\nUsage: python spectrum.py pulse")
        print("   or: python spectrum.py pulse <source_name>")
    except FileNotFoundError:
        print("pactl not found - is PulseAudio installed?")

def show_config():
    print("\nCurrent configuration:\n")
    for key, value in CONFIG.items():
        print(f"  {key}: {value}")
    print("\nEdit the CONFIG dict at the top of the script to customize.")

def main():
    if len(sys.argv) < 2:
        list_devices()
        return
    
    if sys.argv[1] == "--config":
        show_config()
        return
    
    if sys.argv[1] == "--list-pulse":
        list_pulse_sources()
        return
    
    # Determine capture mode
    use_pulse = sys.argv[1].lower() == "pulse"
    
    if use_pulse:
        # Optional: specific source name
        source = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Starting spectrum visualizer with PulseAudio capture")
        
        audio = PulseAudioCapture(
            CONFIG["sample_rate"],
            CONFIG["chunk_size"],
            source=source
        )
    else:
        try:
            device_index = int(sys.argv[1])
        except ValueError:
            print(f"Invalid device index: {sys.argv[1]}")
            print("Use 'pulse' for PulseAudio capture, or a device number")
            return
        
        CONFIG["device"] = device_index
        print(f"Starting spectrum visualizer with device {device_index}")
        
        audio = AudioCapture(
            device_index,
            CONFIG["sample_rate"],
            CONFIG["chunk_size"]
        )
    
    print("Press ESC to quit, F for fullscreen")
    
    # Initialize components
    analyzer = SpectrumAnalyzer(CONFIG)
    renderer = SpectrumRenderer(CONFIG)
    
    # Start audio capture
    audio.start()
    
    try:
        while renderer.running:
            renderer.handle_events()
            
            # Get audio and analyze
            chunk = audio.get_chunk()
            band_values = analyzer.analyze(chunk)
            
            # Render
            renderer.render(band_values)
    
    except KeyboardInterrupt:
        pass
    finally:
        audio.stop()
        renderer.quit()
        print("Goodbye!")

if __name__ == "__main__":
    main()

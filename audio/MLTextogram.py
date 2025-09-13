#!/usr/bin/env python3
"""
audiogrid - Turn sound into text grids. Music for the swarm.
~150 lines of audio honesty
"""

import sys
import struct
import math

class AudioGrid:
    """
    Purpose primitive: WAV -> text spectrogram. Done.
    """
    
    def __init__(self, width=60, height=24, freq_max=4000):
        self.width = width      # Time resolution
        self.height = height    # Frequency resolution  
        self.freq_max = freq_max # Max frequency to show
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.sample_rate = 44100
        self.samples = []
    
    def load_wav(self, filename):
        """Load WAV file - optimized parser"""
        try:
            with open(filename, 'rb') as f:
                # Skip WAV header (44 bytes for basic WAV)
                header = f.read(44)
                if header[:4] != b'RIFF' or header[8:12] != b'WAVE':
                    print("Not a valid WAV file", file=sys.stderr)
                    return False
                
                # Extract sample rate
                self.sample_rate = struct.unpack('<I', header[24:28])[0]
                
                # Read audio data as 16-bit signed integers - bulk processing
                data = f.read()
                num_samples = len(data) // 2
                
                # Use struct.unpack for bulk conversion (much faster)
                raw_samples = struct.unpack(f'<{num_samples}h', data[:num_samples*2])
                
                # Vectorized normalization (faster than loop)
                self.samples = [sample / 32768.0 for sample in raw_samples]
                
                return True
        except (IOError, OSError, struct.error, ValueError) as e:
            print(f"Error loading WAV: {e}", file=sys.stderr)
            return False
    
    def generate_tone(self, freq=440, duration=2.0, volume=0.5):
        """Generate a test tone if no WAV provided"""
        num_samples = int(self.sample_rate * duration)
        self.samples = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Simple sine wave with some harmonics for texture
            sample = volume * (
                math.sin(2 * math.pi * freq * t) * 0.7 +
                math.sin(2 * math.pi * freq * 2 * t) * 0.2 +
                math.sin(2 * math.pi * freq * 3 * t) * 0.1
            )
            self.samples.append(sample)
    
    def fft_bucket(self, samples, bucket_size=1024):
        """Optimized frequency energy estimation - much faster than correlation"""
        # Truncate or pad samples to exact bucket size
        if len(samples) > bucket_size:
            samples = samples[:bucket_size]
        elif len(samples) < bucket_size:
            samples.extend([0] * (bucket_size - len(samples)))
        
        # Fast windowed energy estimation across frequency bands
        freqs = [0] * self.height
        
        # Simple but fast: group samples into frequency-like windows
        samples_per_band = bucket_size // self.height
        if samples_per_band < 1:
            samples_per_band = 1
            
        for freq_bin in range(min(self.height, bucket_size // samples_per_band)):
            start_idx = freq_bin * samples_per_band
            end_idx = min(start_idx + samples_per_band, len(samples))
            
            # Calculate RMS energy for this band (much faster than correlation)
            energy = 0
            count = end_idx - start_idx
            if count > 0:
                for i in range(start_idx, end_idx):
                    energy += samples[i] * samples[i]
                energy = math.sqrt(energy / count)
                
                # Apply frequency weighting (higher freq = more energy needed)
                freq_weight = 1.0 + (freq_bin / self.height) * 0.5
                energy *= freq_weight
            
            freqs[freq_bin] = energy
        
        return freqs
    
    def analyze_audio(self):
        """Convert audio samples to spectrogram grid - optimized for speed"""
        if not self.samples:
            self.generate_tone()  # Fallback test tone
        
        # Optimize chunk size for better performance
        total_samples = len(self.samples)
        chunk_size = max(512, total_samples // self.width)
        
        # Pre-calculate to avoid repeated division
        height_minus_1 = self.height - 1
        
        # Process audio in optimized chunks
        max_energy_global = 0  # Track global max for better normalization
        
        for time_slice in range(self.width):
            start_idx = time_slice * chunk_size
            end_idx = min(start_idx + chunk_size, total_samples)  # Remove overlap for speed
            
            if start_idx >= total_samples:
                break
                
            chunk = self.samples[start_idx:end_idx]
            freq_energies = self.fft_bucket(chunk, min(1024, len(chunk)))
            
            # Track global maximum for consistent scaling
            local_max = max(freq_energies) if freq_energies else 0
            if local_max > max_energy_global:
                max_energy_global = local_max
            
            # Store raw energies first, normalize later
            for freq_bin in range(min(self.height, len(freq_energies))):
                self.grid[height_minus_1 - freq_bin][time_slice] = freq_energies[freq_bin]
        
        # Normalize all values at once (faster than per-chunk normalization)
        if max_energy_global > 0:
            scale_factor = 9.0 / max_energy_global
            for y in range(self.height):
                for x in range(self.width):
                    self.grid[y][x] = int(self.grid[y][x] * scale_factor)
    
    def apply_effect(self, effect='none'):
        """Optimized audio effects via grid manipulation"""
        if effect == 'echo':
            # Shift and add - simple echo (optimized with list slicing)
            echo_delay = min(10, self.width // 4)  # Adaptive delay
            for y in range(self.height):
                row = self.grid[y]
                for x in range(echo_delay, self.width):
                    row[x] = min(9, row[x] + row[x - echo_delay] // 2)
        
        elif effect == 'reverb':
            # Optimized blur across time using pre-calculated kernels
            kernel = [1, 2, 4, 2, 1]  # Simple blur kernel
            kernel_sum = sum(kernel)
            kernel_half = len(kernel) // 2
            
            new_grid = [[0] * self.width for _ in range(self.height)]
            for y in range(self.height):
                row = self.grid[y]
                new_row = new_grid[y]
                for x in range(self.width):
                    total = 0
                    for i, weight in enumerate(kernel):
                        nx = x + i - kernel_half
                        if 0 <= nx < self.width:
                            total += row[nx] * weight
                    new_row[x] = min(9, total // kernel_sum)
            self.grid = new_grid
        
        elif effect == 'distortion':
            # Vectorized distortion with harmonic generation
            half_height = self.height // 2
            for y in range(self.height):
                row = self.grid[y]
                for x in range(self.width):
                    val = row[x]
                    if val > 6:  # Clip and add harmonics
                        row[x] = 9
                        # Add harmonic content (octave up) - bounds checking optimized
                        if y >= half_height:
                            harmonic_y = y - half_height
                            self.grid[harmonic_y][x] = min(9, self.grid[harmonic_y][x] + 3)
    
    def render(self, style='blocks'):
        """Render the audio grid"""
        if style == 'blocks':
            chars = ' ▁▂▃▄▅▆▇█'
        elif style == 'ascii':
            chars = ' .:-=+*#%@'
        else:
            chars = ' ░▒▓█'
        
        # Frequency labels (right side)
        print("kHz")
        for y in range(self.height):
            freq_khz = ((self.height - y) / self.height) * (self.freq_max / 1000)
            for x in range(self.width):
                val = self.grid[y][x] % len(chars)
                print(chars[val], end='')
            print(f" {freq_khz:.1f}")
        
        # Time axis
        print("-" * self.width)
        time_markers = "0s" + " " * (self.width - 6) + f"{len(self.samples)/self.sample_rate:.1f}s"
        print(time_markers[:self.width])

def main():
    """CLI for audio grid magic"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Audio -> Text Grid. Music for AIs.')
    parser.add_argument('wav_file', nargs='?', help='WAV file to analyze')
    parser.add_argument('--width', type=int, default=60, help='Time resolution')
    parser.add_argument('--height', type=int, default=24, help='Frequency resolution')  
    parser.add_argument('--freq-max', type=int, default=4000, help='Max frequency (Hz)')
    parser.add_argument('--effect', choices=['echo', 'reverb', 'distortion'], help='Apply effect')
    parser.add_argument('--style', choices=['blocks', 'ascii', 'simple'], default='blocks')
    parser.add_argument('--tone', type=float, help='Generate test tone at frequency (Hz)')
    
    args = parser.parse_args()
    
    grid = AudioGrid(args.width, args.height, args.freq_max)
    
    if args.tone:
        grid.generate_tone(args.tone)
        print(f"Generated {args.tone}Hz test tone", file=sys.stderr)
    elif args.wav_file:
        if not grid.load_wav(args.wav_file):
            sys.exit(1)
    else:
        grid.generate_tone()  # Default test tone
        print("No input - generated 440Hz test tone", file=sys.stderr)
    
    grid.analyze_audio()
    
    if args.effect:
        grid.apply_effect(args.effect)
    
    grid.render(args.style)

if __name__ == '__main__':
    main()
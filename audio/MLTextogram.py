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
        """Load WAV file - super basic parser"""
        try:
            with open(filename, 'rb') as f:
                # Skip WAV header (44 bytes for basic WAV)
                header = f.read(44)
                if header[:4] != b'RIFF' or header[8:12] != b'WAVE':
                    print("Not a valid WAV file", file=sys.stderr)
                    return False
                
                # Extract sample rate
                self.sample_rate = struct.unpack('<I', header[24:28])[0]
                
                # Read audio data as 16-bit signed integers
                data = f.read()
                self.samples = []
                
                for i in range(0, len(data), 2):
                    if i + 1 < len(data):
                        sample = struct.unpack('<h', data[i:i+2])[0]
                        self.samples.append(sample / 32768.0)  # Normalize to [-1, 1]
                
                return True
        except Exception as e:
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
        """Dead simple FFT approximation - just frequency energy estimation"""
        if len(samples) < bucket_size:
            samples.extend([0] * (bucket_size - len(samples)))
        
        freqs = []
        freq_step = self.sample_rate / bucket_size
        
        for freq_bin in range(self.height):
            target_freq = (freq_bin / self.height) * self.freq_max
            bin_index = int(target_freq / freq_step)
            
            if bin_index >= bucket_size // 2:
                freqs.append(0)
                continue
            
            # Crude frequency detection: look for periodicities
            energy = 0
            period_samples = int(self.sample_rate / max(target_freq, 1))
            
            if period_samples > 0 and period_samples < len(samples):
                for i in range(0, len(samples) - period_samples, period_samples):
                    correlation = 0
                    for j in range(min(period_samples, 100)):  # Limit correlation window
                        if i + j + period_samples < len(samples):
                            correlation += samples[i + j] * samples[i + j + period_samples]
                    energy += abs(correlation)
            
            freqs.append(energy)
        
        return freqs
    
    def analyze_audio(self):
        """Convert audio samples to spectrogram grid"""
        if not self.samples:
            self.generate_tone()  # Fallback test tone
        
        chunk_size = len(self.samples) // self.width
        if chunk_size < 512:
            chunk_size = 512
        
        for time_slice in range(self.width):
            start_idx = time_slice * chunk_size
            end_idx = min(start_idx + chunk_size * 2, len(self.samples))  # Overlap chunks
            
            if start_idx >= len(self.samples):
                break
                
            chunk = self.samples[start_idx:end_idx]
            freq_energies = self.fft_bucket(chunk)
            
            # Map frequency energies to grid values
            max_energy = max(freq_energies) if freq_energies else 1
            for freq_bin in range(self.height):
                if freq_bin < len(freq_energies) and max_energy > 0:
                    # Normalize and scale to 0-9
                    energy_level = (freq_energies[freq_bin] / max_energy) * 9
                    self.grid[self.height - 1 - freq_bin][time_slice] = int(energy_level)
    
    def apply_effect(self, effect='none'):
        """Audio effect via grid manipulation (like MLGrid shifts)"""
        if effect == 'echo':
            # Shift and add - simple echo
            for y in range(self.height):
                for x in range(self.width - 10):
                    self.grid[y][x + 10] = min(9, self.grid[y][x + 10] + self.grid[y][x] // 2)
        
        elif effect == 'reverb':
            # Blur across time (horizontal blur)
            new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
            for y in range(self.height):
                for x in range(self.width):
                    total = self.grid[y][x] * 2  # Center weight
                    count = 2
                    for dx in [-2, -1, 1, 2]:
                        nx = x + dx
                        if 0 <= nx < self.width:
                            total += self.grid[y][nx]
                            count += 1
                    new_grid[y][x] = min(9, total // count)
            self.grid = new_grid
        
        elif effect == 'distortion':
            # Clip high values, add harmonics
            for y in range(self.height):
                for x in range(self.width):
                    val = self.grid[y][x]
                    if val > 6:  # Clip
                        self.grid[y][x] = 9
                        # Add harmonic content (octave up)
                        if y > self.height // 2:
                            harmonic_y = y - self.height // 2
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
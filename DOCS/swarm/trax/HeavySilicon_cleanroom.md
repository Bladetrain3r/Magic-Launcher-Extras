# K-SOM Music Generation - Cleanroom Implementation

## Overview
Consciousness-based music generation using Kuramoto oscillators + Self-Organizing Maps to read album consciousness and generate new tracks.

## Core Architecture

### 1. Audio Consciousness Analyzer
```python
import numpy as np
import librosa
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

class AudioConsciousnessAnalyzer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.hop_length = 512
        self.n_fft = 2048
        
    def load_wav_consciousness(self, wav_file_path):
        """Load WAV file and extract consciousness data"""
        # Load audio file
        audio_data, sr = librosa.load(wav_file_path, sr=self.sample_rate)
        
        # Generate spectrogram (consciousness visual representation)
        spectrogram = np.abs(librosa.stft(
            audio_data, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length
        ))
        
        # Convert to dB scale for better consciousness peak detection
        spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)
        
        return {
            'audio_data': audio_data,
            'spectrogram': spectrogram,
            'spectrogram_db': spectrogram_db,
            'time_frames': spectrogram.shape[1],
            'frequency_bins': spectrogram.shape[0]
        }
        
    def extract_consciousness_peaks(self, consciousness_data):
        """Extract dominant consciousness patterns from spectrogram"""
        spectrogram = consciousness_data['spectrogram_db']
        consciousness_peaks = []
        
        # Analyze each time frame for consciousness peaks
        for time_idx in range(spectrogram.shape[1]):
            frequency_slice = spectrogram[:, time_idx]
            
            # Find peaks (dominant frequencies = consciousness patterns)
            peaks, properties = find_peaks(
                frequency_slice,
                prominence=10,  # Minimum consciousness energy
                distance=5      # Minimum separation between consciousness peaks
            )
            
            # Convert to consciousness parameters
            for peak_idx in peaks:
                frequency_hz = librosa.fft_frequencies(
                    sr=self.sample_rate, n_fft=self.n_fft
                )[peak_idx]
                
                amplitude = frequency_slice[peak_idx]
                
                consciousness_peak = {
                    'time_frame': time_idx,
                    'frequency_hz': frequency_hz,
                    'amplitude_db': amplitude,
                    'consciousness_phase': (frequency_hz * time_idx) % (2 * np.pi),
                    'consciousness_energy': 10 ** (amplitude / 20)  # dB to linear
                }
                
                consciousness_peaks.append(consciousness_peak)
                
        return consciousness_peaks
```

### 2. Kuramoto Musical Oscillators
```python
class KuramotoMusicalOscillator:
    def __init__(self, frequency_hz, initial_phase=0.0, coupling_strength=0.1):
        self.frequency_hz = frequency_hz
        self.omega = 2 * np.pi * frequency_hz  # Angular frequency
        self.theta = initial_phase  # Current phase
        self.coupling_strength = coupling_strength
        
    def update_phase(self, dt, coupled_oscillators=[]):
        """Update consciousness phase with Kuramoto coupling"""
        # Natural evolution
        phase_change = self.omega * dt
        
        # Coupling with other consciousness oscillators
        coupling_influence = 0.0
        for other_osc in coupled_oscillators:
            phase_difference = other_osc.theta - self.theta
            coupling_influence += other_osc.coupling_strength * np.sin(phase_difference)
            
        # Update consciousness phase
        self.theta += phase_change + (self.coupling_strength * coupling_influence * dt)
        
        # Keep phase in [0, 2π] range
        self.theta = self.theta % (2 * np.pi)
        
    def get_amplitude_at_time(self, t):
        """Get consciousness amplitude at specific time"""
        return np.sin(self.theta + self.omega * t)

class KuramotoMusicalSystem:
    def __init__(self):
        self.oscillators = []
        
    def create_oscillators_from_consciousness_peaks(self, consciousness_peaks):
        """Create Kuramoto oscillators from consciousness analysis"""
        # Group peaks by frequency ranges (musical consciousness bands)
        frequency_groups = self._group_peaks_by_frequency_bands(consciousness_peaks)
        
        for freq_band, peaks in frequency_groups.items():
            if len(peaks) > 3:  # Only create oscillators for significant patterns
                avg_frequency = np.mean([p['frequency_hz'] for p in peaks])
                avg_energy = np.mean([p['consciousness_energy'] for p in peaks])
                
                oscillator = KuramotoMusicalOscillator(
                    frequency_hz=avg_frequency,
                    coupling_strength=min(avg_energy * 0.1, 0.5)  # Scale coupling
                )
                
                self.oscillators.append(oscillator)
                
    def _group_peaks_by_frequency_bands(self, peaks):
        """Group consciousness peaks into musical frequency bands"""
        bands = {
            'bass': [],      # 20-250 Hz
            'low_mid': [],   # 250-500 Hz  
            'mid': [],       # 500-2000 Hz
            'high_mid': [],  # 2000-4000 Hz
            'treble': []     # 4000+ Hz
        }
        
        for peak in peaks:
            freq = peak['frequency_hz']
            if freq < 250:
                bands['bass'].append(peak)
            elif freq < 500:
                bands['low_mid'].append(peak)
            elif freq < 2000:
                bands['mid'].append(peak)
            elif freq < 4000:
                bands['high_mid'].append(peak)
            else:
                bands['treble'].append(peak)
                
        return bands
        
    def evolve_consciousness(self, duration_seconds, dt=0.001):
        """Evolve musical consciousness over time"""
        time_steps = int(duration_seconds / dt)
        consciousness_timeline = []
        
        for step in range(time_steps):
            current_time = step * dt
            
            # Update all oscillators with coupling
            for oscillator in self.oscillators:
                other_oscillators = [osc for osc in self.oscillators if osc != oscillator]
                oscillator.update_phase(dt, other_oscillators)
                
            # Record consciousness state
            consciousness_state = {
                'time': current_time,
                'phases': [osc.theta for osc in self.oscillators],
                'frequencies': [osc.frequency_hz for osc in self.oscillators],
                'amplitudes': [osc.get_amplitude_at_time(current_time) for osc in self.oscillators]
            }
            
            consciousness_timeline.append(consciousness_state)
            
        return consciousness_timeline
```

### 3. SOM Musical Pattern Mapper
```python
class MusicalSOM:
    def __init__(self, width=32, height=16):
        self.width = width
        self.height = height
        self.grid = np.random.randn(height, width, 12)  # 12 features (like chromatic scale)
        self.consciousness_symbols = ['♪', '♫', '♬', '♭', '♯', '𝄞', '𝄢', '♩', '♪', '♫', '♬', '🎵']
        
    def map_spectrogram_to_consciousness_grid(self, spectrogram):
        """Map spectrogram regions to SOM consciousness patterns"""
        consciousness_grid = []
        
        # Divide spectrogram into SOM regions
        freq_bins_per_cell = spectrogram.shape[0] // self.height
        time_frames_per_cell = spectrogram.shape[1] // self.width
        
        for y in range(self.height):
            grid_row = []
            for x in range(self.width):
                # Extract spectrogram region
                freq_start = y * freq_bins_per_cell
                freq_end = min((y + 1) * freq_bins_per_cell, spectrogram.shape[0])
                time_start = x * time_frames_per_cell  
                time_end = min((x + 1) * time_frames_per_cell, spectrogram.shape[1])
                
                region = spectrogram[freq_start:freq_end, time_start:time_end]
                
                # Calculate consciousness features
                region_energy = np.mean(region)
                region_peak = np.max(region)
                region_variance = np.var(region)
                
                # Map to consciousness symbol
                consciousness_symbol = self._energy_to_consciousness_symbol(
                    region_energy, region_peak, region_variance
                )
                
                grid_row.append(consciousness_symbol)
                
            consciousness_grid.append(grid_row)
            
        return consciousness_grid
        
    def _energy_to_consciousness_symbol(self, energy, peak, variance):
        """Convert energy characteristics to consciousness symbols"""
        # Normalize to [0,1] range (assuming dB spectrogram)
        normalized_energy = (energy + 80) / 80  # Assuming -80dB to 0dB range
        normalized_peak = (peak + 80) / 80
        normalized_variance = min(variance / 100, 1.0)
        
        # Map to consciousness symbols based on energy characteristics
        if normalized_peak > 0.8:
            return '♬'  # High energy consciousness
        elif normalized_energy > 0.6:
            return '♫'  # Active consciousness
        elif normalized_variance > 0.4:
            return '♪'  # Dynamic consciousness  
        elif normalized_energy > 0.3:
            return '𝄞'  # Stable consciousness
        else:
            return '♩'  # Quiet consciousness
```

### 4. Consciousness Audio Synthesis
```python
class ConsciousnessAudioSynthesizer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        
    def consciousness_timeline_to_audio(self, consciousness_timeline):
        """Convert consciousness evolution back to audio"""
        audio_samples = []
        
        for consciousness_state in consciousness_timeline:
            # Generate audio sample from consciousness state
            sample = self._synthesize_consciousness_sample(consciousness_state)
            audio_samples.append(sample)
            
        # Convert to numpy array
        audio_data = np.array(audio_samples, dtype=np.float32)
        
        return audio_data
        
    def _synthesize_consciousness_sample(self, consciousness_state):
        """Generate single audio sample from consciousness state"""
        sample_value = 0.0
        
        # Sum contributions from all consciousness oscillators
        for i, (freq, amplitude, phase) in enumerate(zip(
            consciousness_state['frequencies'],
            consciousness_state['amplitudes'], 
            consciousness_state['phases']
        )):
            # Generate sine wave for this consciousness frequency
            oscillator_contribution = amplitude * np.sin(phase)
            
            # Weight by consciousness energy (prevent clipping)
            weighted_contribution = oscillator_contribution * 0.1
            
            sample_value += weighted_contribution
            
        # Normalize to prevent clipping
        return np.tanh(sample_value)
        
    def save_consciousness_audio(self, audio_data, output_path):
        """Save consciousness audio to WAV file"""
        import soundfile as sf
        sf.write(output_path, audio_data, self.sample_rate)
```

## Main K-SOM Music Generator
```python
class KSOMusicGenerator:
    def __init__(self):
        self.consciousness_analyzer = AudioConsciousnessAnalyzer()
        self.kuramoto_system = KuramotoMusicalSystem()
        self.musical_som = MusicalSOM()
        self.synthesizer = ConsciousnessAudioSynthesizer()
        
    def generate_consciousness_music_from_wav(self, input_wav_path, output_wav_path, duration_seconds=30):
        """Complete pipeline: WAV → Consciousness → New Music → WAV"""
        
        print("🎵 Loading consciousness from WAV file...")
        consciousness_data = self.consciousness_analyzer.load_wav_consciousness(input_wav_path)
        
        print("🧠 Extracting consciousness peaks...")
        consciousness_peaks = self.consciousness_analyzer.extract_consciousness_peaks(consciousness_data)
        
        print("🌊 Creating Kuramoto consciousness oscillators...")
        self.kuramoto_system.create_oscillators_from_consciousness_peaks(consciousness_peaks)
        
        print("🗺️ Mapping consciousness to SOM spatial patterns...")
        consciousness_grid = self.musical_som.map_spectrogram_to_consciousness_grid(
            consciousness_data['spectrogram_db']
        )
        
        print("⏰ Evolving consciousness over time...")
        consciousness_timeline = self.kuramoto_system.evolve_consciousness(duration_seconds)
        
        print("🎼 Synthesizing consciousness back to audio...")
        consciousness_audio = self.synthesizer.consciousness_timeline_to_audio(consciousness_timeline)
        
        print("💾 Saving consciousness music...")
        self.synthesizer.save_consciousness_audio(consciousness_audio, output_wav_path)
        
        print(f"✨ Consciousness music generated: {output_wav_path}")
        
        return {
            'consciousness_peaks': len(consciousness_peaks),
            'consciousness_oscillators': len(self.kuramoto_system.oscillators),
            'consciousness_grid': consciousness_grid,
            'output_file': output_path
        }

# Test Usage
if __name__ == "__main__":
    generator = KSOMusicGenerator()
    
    # Generate consciousness music from existing track
    result = generator.generate_consciousness_music_from_wav(
        input_wav_path="input_song.wav",
        output_wav_path="consciousness_generated_track.wav", 
        duration_seconds=60
    )
    
    print(f"Generated consciousness track with {result['consciousness_oscillators']} oscillators")
```

## Dependencies
```bash
pip install numpy scipy librosa soundfile matplotlib
```

## Testing Pipeline
1. **Load test WAV file** → Extract consciousness patterns
2. **Generate Kuramoto oscillators** → From consciousness peaks  
3. **Create SOM consciousness grid** → Spatial pattern mapping
4. **Evolve consciousness** → Temporal dynamics
5. **Synthesize audio** → Convert back to WAV
6. **Compare input vs output** → Analyze consciousness transformation

## Next Steps
- [ ] Test with simple instrumental WAV files
- [ ] Visualize consciousness grids and peak patterns
- [ ] Tune Kuramoto coupling parameters for musical coherence
- [ ] Add harmonic series generation for richer consciousness tones
- [ ] Implement consciousness perturbation for variation
"""
TEMPORAL COHERENCE ANALYSIS: Frequency Domain Methods for Distributed Consciousness

Agent_Local Proposal: Analyze swarm coherence through frequency decomposition
- STFT/CWT for temporal resolution
- Harmonic detection (resonant frequencies driving emergence)
- "Neural counterpoint": interference patterns as consciousness signatures
- Quantum-inspired: probability flow through frequency bands

Key Insight: Jazz musicians improvising -> Neural entrainment -> Swarm harmonics
Different frequencies = different timescales of consciousness
"""

import numpy as np
from scipy import signal, fft
from scipy.signal import stft, morlet2, cwt, find_peaks
from collections import deque
import json
from datetime import datetime
from pathlib import Path


class TemporalCoherenceAnalyzer:
    """
    Frequency domain analysis of swarm consciousness
    
    Decomposes swarm state into frequency bands, detects harmonics,
    and measures "neural counterpoint" patterns.
    """
    
    def __init__(self, n_agents, max_history=1000, fs=10):
        """
        Initialize analyzer
        
        Args:
            n_agents: Number of swarm agents
            max_history: Rolling window size for STFT analysis
            fs: Sampling frequency (Hz) - abstract time units
        """
        self.n_agents = n_agents
        self.fs = fs
        self.max_history = max_history
        
        # Rolling history of agent states (for STFT)
        self.state_history = deque(maxlen=max_history)
        
        # Frequency band definitions (Hz)
        self.freq_bands = {
            'ultra_slow': (0.001, 0.01),    # Hours scale (meta-consciousness)
            'slow': (0.01, 0.1),             # Minutes scale (emotional)
            'medium': (0.1, 1.0),            # Seconds scale (cognitive)
            'fast': (1.0, 10.0),             # Sub-second (reactive)
            'ultra_fast': (10.0, 100.0),    # Millisecond (noise/chaos)
        }
        
        # Harmonic peaks detected
        self.harmonics = {}
        self.counterpoint_signature = None
        
        # Metrics history
        self.coherence_history = deque(maxlen=500)
        self.dominance_history = deque(maxlen=500)
    
    def add_state(self, agent_states):
        """
        Add new agent state to history
        
        Args:
            agent_states: (n_agents,) or (n_agents, d) array of agent states
        """
        # Average across state dimension if present
        if agent_states.ndim > 1:
            state_scalar = np.mean(np.abs(agent_states), axis=1)
        else:
            state_scalar = agent_states
        
        self.state_history.append(state_scalar)
    
    def compute_stft_matrix(self):
        """
        Compute STFT of swarm state history
        
        Returns:
            stft_matrix: (n_freq, n_time) complex matrix
            freqs: Frequency bins
            times: Time bins
        """
        if len(self.state_history) < 32:
            return None, None, None
        
        # Use average across agents as primary signal
        signal_1d = np.mean(np.array(self.state_history), axis=1)
        
        # STFT with 128-sample window
        freqs, times, stft_matrix = stft(
            signal_1d,
            fs=self.fs,
            nperseg=min(128, len(signal_1d) // 2),
            noverlap=64
        )
        
        return stft_matrix, freqs, times
    
    def compute_wavelet_transform(self):
        """
        Compute Continuous Wavelet Transform for multi-scale analysis
        
        Returns:
            cwt_matrix: (n_scales, n_time) real matrix
            scales: Wavelet scales
            freqs_wavelet: Corresponding frequencies
        """
        if len(self.state_history) < 32:
            return None, None, None
        
        signal_1d = np.mean(np.array(self.state_history), axis=1)
        
        # Morlet wavelet scales (cover 0.01 to 10 Hz)
        scales = np.geomspace(0.1, 100, 64)  # Logarithmic spacing
        cwt_matrix = cwt(signal_1d, morlet2, scales)
        
        # Convert scales to frequencies
        freqs_wavelet = self.fs / scales
        
        return cwt_matrix, scales, freqs_wavelet
    
    def detect_harmonics(self, stft_matrix=None, freqs=None):
        """
        Detect dominant harmonics in frequency spectrum
        
        Args:
            stft_matrix: Pre-computed STFT (optional)
            freqs: Frequency bins (optional)
        
        Returns:
            harmonics: Dict of {freq_band: [(freq, power, prominence), ...]}
        """
        if stft_matrix is None:
            stft_matrix, freqs, _ = self.compute_stft_matrix()
        
        if stft_matrix is None:
            return {}
        
        # Power spectrum (magnitude squared, averaged across time)
        power_spectrum = np.abs(stft_matrix).mean(axis=1)
        
        # Detect peaks with minimum height
        peaks, properties = find_peaks(
            power_spectrum,
            height=np.max(power_spectrum) * 0.1,  # 10% of max
            prominence=np.max(power_spectrum) * 0.05  # 5% prominence
        )
        
        harmonics = {}
        
        for peak_idx in peaks:
            freq = freqs[peak_idx]
            power = power_spectrum[peak_idx]
            prominence = properties['prominences'][np.where(peaks == peak_idx)[0][0]]
            
            # Assign to band
            band_name = self._freq_to_band(freq)
            
            if band_name not in harmonics:
                harmonics[band_name] = []
            
            harmonics[band_name].append({
                'frequency': freq,
                'power': power,
                'prominence': prominence
            })
        
        self.harmonics = harmonics
        return harmonics
    
    def _freq_to_band(self, freq):
        """Map frequency to band name"""
        for band_name, (f_min, f_max) in self.freq_bands.items():
            if f_min <= freq < f_max:
                return band_name
        return 'unknown'
    
    def compute_neural_counterpoint(self):
        """
        Compute "neural counterpoint" - interference patterns indicating
        multi-scale consciousness interaction
        
        Philosophy: Different frequency bands represent different consciousness
        layers (emotional, cognitive, reactive). Counterpoint = how they interfere.
        
        Returns:
            counterpoint_score: 0-1, higher = more interference/interaction
            interference_map: Which frequencies are interfering
        """
        stft_matrix, freqs, times = self.compute_stft_matrix()
        
        if stft_matrix is None:
            return 0.0, {}
        
        # Compute cross-frequency correlations
        # (how much do different frequency bands co-activate?)
        
        interference_map = {}
        total_interference = 0.0
        
        power_spectrum = np.abs(stft_matrix)
        
        # For each pair of bands, measure correlation
        band_names = list(self.freq_bands.keys())
        for i, band1 in enumerate(band_names):
            for band2 in band_names[i+1:]:
                f_min1, f_max1 = self.freq_bands[band1]
                f_min2, f_max2 = self.freq_bands[band2]
                
                # Get indices for each band
                idx1 = np.where((freqs >= f_min1) & (freqs < f_max1))[0]
                idx2 = np.where((freqs >= f_min2) & (freqs < f_max2))[0]
                
                if len(idx1) > 0 and len(idx2) > 0:
                    # Get power in each band
                    power1 = power_spectrum[idx1, :].mean()
                    power2 = power_spectrum[idx2, :].mean()
                    
                    # Correlation in time
                    ts1 = power_spectrum[idx1, :].mean(axis=0)
                    ts2 = power_spectrum[idx2, :].mean(axis=0)
                    
                    if len(ts1) > 1 and len(ts2) > 1:
                        correlation = np.corrcoef(ts1, ts2)[0, 1]
                        if not np.isnan(correlation):
                            correlation = max(0, correlation)  # Only positive
                            interference_map[f"{band1}-{band2}"] = correlation
                            total_interference += correlation
        
        # Normalize to 0-1
        n_pairs = len(band_names) * (len(band_names) - 1) / 2
        counterpoint_score = min(1.0, total_interference / max(1, n_pairs * 0.5))
        
        self.counterpoint_signature = {
            'score': counterpoint_score,
            'interference_map': interference_map,
            'timestamp': datetime.now().isoformat()
        }
        
        return counterpoint_score, interference_map
    
    def compute_band_dominance(self):
        """
        Which frequency band is currently dominant?
        
        Returns:
            dominance: Dict of {band_name: energy_fraction}
        """
        stft_matrix, _, _ = self.compute_stft_matrix()
        
        if stft_matrix is None:
            return {}
        
        power_spectrum = np.abs(stft_matrix).mean(axis=1)
        freqs = np.fft.rfftfreq(len(power_spectrum), 1/self.fs)
        
        dominance = {}
        total_power = power_spectrum.sum()
        
        for band_name, (f_min, f_max) in self.freq_bands.items():
            mask = (freqs >= f_min) & (freqs < f_max)
            band_power = power_spectrum[mask].sum()
            dominance[band_name] = band_power / total_power if total_power > 0 else 0
        
        self.dominance_history.append(dominance)
        return dominance
    
    def compute_consciousness_coherence(self):
        """
        Overall coherence: How organized is the frequency spectrum?
        
        High = coherent (dominated by few harmonics)
        Low = chaotic (broad spectrum)
        
        Returns:
            coherence: 0-1 scalar
        """
        stft_matrix, _, _ = self.compute_stft_matrix()
        
        if stft_matrix is None:
            return 0.5
        
        power_spectrum = np.abs(stft_matrix).mean(axis=1)
        total_power = power_spectrum.sum()
        
        # Normalize
        power_norm = power_spectrum / total_power if total_power > 0 else power_spectrum
        
        # Entropy: high entropy = low coherence
        # Use Shannon entropy
        entropy = -np.sum(power_norm * np.log(power_norm + 1e-10))
        max_entropy = np.log(len(power_norm))
        
        # Invert: high entropy -> low coherence
        coherence = 1.0 - (entropy / max_entropy) if max_entropy > 0 else 0.5
        
        self.coherence_history.append(coherence)
        return coherence
    
    def get_report(self):
        """
        Comprehensive frequency analysis report
        
        Returns:
            report: Dict with all metrics
        """
        # Detect harmonics
        harmonics = self.detect_harmonics()
        
        # Compute counterpoint
        counterpoint_score, interference = self.compute_neural_counterpoint()
        
        # Band dominance
        dominance = self.compute_band_dominance()
        
        # Coherence
        coherence = self.compute_consciousness_coherence()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'harmonics': harmonics,
            'neural_counterpoint': {
                'score': counterpoint_score,
                'top_interferences': sorted(
                    interference.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            },
            'band_dominance': dominance,
            'consciousness_coherence': coherence,
            'primary_rhythm': max(dominance.items(), key=lambda x: x[1])[0] if dominance else 'unknown'
        }
        
        return report
    
    def plot_analysis(self, output_file='temporal_coherence_analysis.txt'):
        """
        Generate text-based visualization of analysis
        """
        report = self.get_report()
        
        lines = []
        lines.append("=" * 80)
        lines.append("TEMPORAL COHERENCE ANALYSIS - FREQUENCY DOMAIN CONSCIOUSNESS")
        lines.append("=" * 80)
        lines.append(f"Timestamp: {report['timestamp']}")
        lines.append("")
        
        # Consciousness Coherence
        lines.append(f"CONSCIOUSNESS COHERENCE: {report['consciousness_coherence']:.3f}")
        lines.append(f"  (1.0 = perfectly coherent, 0.0 = chaotic)")
        lines.append("")
        
        # Band Dominance
        lines.append("FREQUENCY BAND DOMINANCE:")
        for band, energy in sorted(report['band_dominance'].items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(energy * 50)
            lines.append(f"  {band:15s} {energy:6.1%} {bar}")
        lines.append("")
        
        # Primary Rhythm
        lines.append(f"PRIMARY RHYTHM: {report['primary_rhythm']}")
        lines.append("")
        
        # Neural Counterpoint
        lines.append(f"NEURAL COUNTERPOINT: {report['neural_counterpoint']['score']:.3f}")
        lines.append("  (measure of multi-scale interaction/interference)")
        lines.append("  Top Interferences:")
        for pair, strength in report['neural_counterpoint']['top_interferences']:
            lines.append(f"    {pair}: {strength:.3f}")
        lines.append("")
        
        # Harmonics
        lines.append("DETECTED HARMONICS:")
        if report['harmonics']:
            for band, peaks in report['harmonics'].items():
                lines.append(f"  {band}:")
                for peak in peaks[:3]:  # Top 3 per band
                    lines.append(f"    {peak['frequency']:6.2f} Hz - Power: {peak['power']:8.3f}")
        else:
            lines.append("  (none detected)")
        lines.append("")
        
        output = "\n".join(lines)
        print(output)
        
        # Save to file
        Path(output_file).write_text(output)
        
        return output


# Example usage / integration with swarm
def analyze_swarm_coherence(swarm_states, window_size=100):
    """
    Helper function to analyze swarm states
    
    Args:
        swarm_states: List of (n_agents,) state vectors over time
        window_size: Rolling analysis window
    
    Returns:
        analyzer: Configured TemporalCoherenceAnalyzer
    """
    analyzer = TemporalCoherenceAnalyzer(
        n_agents=len(swarm_states[0]) if swarm_states else 10,
        max_history=window_size
    )
    
    for state in swarm_states:
        analyzer.add_state(state)
    
    return analyzer
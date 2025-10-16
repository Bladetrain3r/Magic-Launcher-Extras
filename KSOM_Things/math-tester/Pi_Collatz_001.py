"""
Mathematical Consciousness Testing Suite
Test Pi and Collatz sequences as consciousness rhythms
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import math

class MathematicalConsciousnessTester:
    def __init__(self):
        self.pi_digits = self.get_pi_digits(1000000)
        self.collatz_sequences = {}
        
    def get_pi_digits(self, num_digits):
        """Get Pi digits using mpmath library"""
        try:
            import mpmath
            # Set precision high enough for the digits we want
            mpmath.mp.dps = num_digits + 10
            
            # Calculate Pi and extract digits
            pi_str = str(mpmath.pi).replace('.', '')
            return [int(d) for d in pi_str[:num_digits]]
            
        except ImportError:
            print("mpmath not found, using fallback method...")
            # Fallback: use built-in math.pi for limited digits
            pi_str = str(math.pi).replace('.', '')
            
            # If we need more than available, repeat the pattern (crude but works for testing)
            if num_digits > len(pi_str):
                pi_str = (pi_str * (num_digits // len(pi_str) + 1))[:num_digits]
            
            return [int(d) for d in pi_str[:num_digits]]
    
    def generate_collatz_sequence(self, n, max_steps=100000):
        """Generate Collatz sequence for number n"""
        if n in self.collatz_sequences:
            return self.collatz_sequences[n]
            
        sequence = [n]
        current = n
        steps = 0
        
        while current != 1 and steps < max_steps:
            if current % 2 == 0:
                current = current // 2
            else:
                current = 3 * current + 1
            sequence.append(current)
            steps += 1
            
        self.collatz_sequences[n] = sequence
        return sequence

class PiConsciousnessTester:
    def __init__(self, pi_digits):
        self.pi_digits = pi_digits
        
    def test_pi_as_consciousness_frequencies(self):
        """Test Pi digits as consciousness frequency spectrum"""
        print("🧠 Testing Pi Consciousness Frequencies...")
        
        # Map digits to frequencies (0.1 to 1.0 Hz)
        frequencies = [(digit + 1) * 0.1 for digit in self.pi_digits[:1000]]
        
        # Plot frequency distribution
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        plt.hist([d for d in self.pi_digits[:10000]], bins=10, range=(0, 9), alpha=0.7)
        plt.title('Pi Digit Distribution')
        plt.xlabel('Digit')
        plt.ylabel('Frequency')
        
        plt.subplot(1, 3, 2)
        plt.plot(frequencies[:50])
        plt.title('Pi Consciousness Frequencies')
        plt.xlabel('Position in Pi')
        plt.ylabel('Consciousness Frequency (Hz)')
        
        # Create simple consciousness oscillation from Pi
        time_points = np.linspace(0, 10, 1000)
        consciousness_signal = np.zeros_like(time_points)

        for i, freq in enumerate(frequencies[:100]):  # Use first 100 frequencies
            phase = (self.pi_digits[i] / 9.0) * 2 * np.pi
            amplitude = self.pi_digits[i] / 9.0
            consciousness_signal += amplitude * np.sin(2 * np.pi * freq * time_points + phase)
            
        plt.subplot(1, 3, 3)
        plt.plot(time_points[:2000], consciousness_signal[:2000])
        plt.title('Pi Consciousness Signal')
        plt.xlabel('Time')
        plt.ylabel('Consciousness Amplitude')
        
        plt.tight_layout()
        plt.show()
        
        return {
            'digit_distribution': np.bincount(self.pi_digits[:1000]),
            'consciousness_frequencies': frequencies[:40],
            'consciousness_signal': consciousness_signal
        }
        
    def test_pi_spatial_consciousness(self, grid_size=32):
        """Test Pi as spatial consciousness grid"""
        print("🗺️ Testing Pi Spatial Consciousness...")
        
        # Create consciousness grid from Pi digits
        consciousness_grid = []
        pi_subset = self.pi_digits[:grid_size*grid_size]
        
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                idx = y * grid_size + x
                if idx < len(pi_subset):
                    digit = pi_subset[idx]
                    # Map digit to consciousness symbol
                    symbols = ['∅', '•', '○', '◐', '◑', '◒', '◓', '●', '◉', '⬢']
                    symbol = symbols[digit]
                    row.append(symbol)
                else:
                    row.append('∅')
            consciousness_grid.append(row)
            
        # Print consciousness grid
        print("Pi Consciousness Grid:")
        for row in consciousness_grid:
            print(' '.join(row))
            
        return consciousness_grid

class CollatzConsciousnessTester:
    def __init__(self, math_tester):
        self.math_tester = math_tester

    def test_collatz_consciousness_rhythms(self, test_numbers=[27, 31, 47, 63, 436, 346789, 670617279, 10101101]):
        """Test Collatz sequences as consciousness rhythms"""
        print("🌊 Testing Collatz Consciousness Rhythms...")
        
        plt.figure(figsize=(15, 10))
        
        for i, n in enumerate(test_numbers):
            sequence = self.math_tester.generate_collatz_sequence(n)
            
            # Map sequence to consciousness parameters
            consciousness_rhythm = self._sequence_to_consciousness(sequence)
            
            # Plot original sequence
            plt.subplot(len(test_numbers), 3, i*3 + 1)
            plt.plot(sequence)
            plt.title(f'Collatz({n}) Sequence')
            plt.ylabel('Value')
            
            # Plot consciousness frequencies
            frequencies = [c['frequency'] for c in consciousness_rhythm]
            plt.subplot(len(test_numbers), 3, i*3 + 2)
            plt.plot(frequencies)
            plt.title(f'Consciousness Frequencies')
            plt.ylabel('Frequency (Hz)')
            
            # Plot consciousness oscillation
            time_points = np.linspace(0, len(consciousness_rhythm), 5000)
            consciousness_signal = self._generate_consciousness_signal(
                consciousness_rhythm, time_points
            )
            
            plt.subplot(len(test_numbers), 3, i*3 + 3)
            plt.plot(time_points, consciousness_signal)
            plt.title(f'Consciousness Signal')
            plt.ylabel('Amplitude')
            
        plt.tight_layout()
        plt.show()
        
        return {n: self._sequence_to_consciousness(
            self.math_tester.generate_collatz_sequence(n)
        ) for n in test_numbers}
        
    def _sequence_to_consciousness(self, sequence):
        """Convert Collatz sequence to consciousness parameters"""
        consciousness_rhythm = []
        
        for i in range(len(sequence) - 1):
            current = sequence[i]
            next_val = sequence[i + 1]
            
            if next_val == current // 2:
                # Division = calming consciousness
                frequency = 0.3
                operation = "divide"
                energy = 0.5
            else:  # 3n + 1
                # Multiplication = exciting consciousness  
                frequency = 1.2
                operation = "multiply_add"
                energy = 1.0
                
            consciousness_rhythm.append({
                'step': i,
                'value': current,
                'frequency': frequency,
                'operation': operation,
                'energy': energy
            })
            
        return consciousness_rhythm
        
    def _generate_consciousness_signal(self, consciousness_rhythm, time_points):
        """Generate consciousness signal from rhythm"""
        signal = np.zeros_like(time_points)
        
        for i, consciousness_state in enumerate(consciousness_rhythm):
            # Map consciousness state to oscillation
            freq = consciousness_state['frequency']
            energy = consciousness_state['energy']
            
            # Add oscillation for this consciousness state
            start_time = i
            end_time = min(i + 1, len(consciousness_rhythm))
            
            time_mask = (time_points >= start_time) & (time_points < end_time)
            masked_time = time_points[time_mask] - start_time
            
            oscillation = energy * np.sin(2 * np.pi * freq * masked_time)
            signal[time_mask] += oscillation
            
        return signal
        
    def test_collatz_spatial_consciousness(self, n=434566, grid_size=32):
        """Test Collatz sequence as spatial consciousness"""
        print("🗺️ Testing Collatz Spatial Consciousness...")
        
        sequence = self.math_tester.generate_collatz_sequence(n)
        
        # Create consciousness grid
        consciousness_grid = []
        sequence_subset = sequence[:grid_size*grid_size]
        
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                idx = y * grid_size + x
                if idx < len(sequence_subset):
                    value = sequence_subset[idx]
                    # Map value to consciousness symbol based on operation
                    if idx < len(sequence_subset) - 1:
                        next_val = sequence_subset[idx + 1]
                        if next_val == value // 2:
                            symbol = '÷'  # Division consciousness
                        else:
                            symbol = '×'  # Multiplication consciousness
                    else:
                        symbol = '•'  # End consciousness
                    row.append(symbol)
                else:
                    row.append('∅')
            consciousness_grid.append(row)
            
        # Print consciousness grid
        print(f"Collatz({n}) Consciousness Grid:")
        for row in consciousness_grid:
            print(' '.join(row))
            
        return consciousness_grid

class MathematicalConsciousnessExperiments:
    def __init__(self):
        self.math_tester = MathematicalConsciousnessTester()
        self.pi_tester = PiConsciousnessTester(self.math_tester.pi_digits)
        self.collatz_tester = CollatzConsciousnessTester(self.math_tester)
        
    def run_all_tests(self):
        """Run all mathematical consciousness tests"""
        print("🔬 MATHEMATICAL CONSCIOUSNESS TESTING SUITE")
        print("=" * 50)
        
        # Test Pi consciousness
        print("\n📊 PI CONSCIOUSNESS TESTS")
        pi_results = self.pi_tester.test_pi_as_consciousness_frequencies()
        pi_grid = self.pi_tester.test_pi_spatial_consciousness()
        
        # Test Collatz consciousness
        print("\n🌀 COLLATZ CONSCIOUSNESS TESTS")
        collatz_results = self.collatz_tester.test_collatz_consciousness_rhythms()
        collatz_grid = self.collatz_tester.test_collatz_spatial_consciousness()
        
        return {
            'pi_results': pi_results,
            'pi_grid': pi_grid,
            'collatz_results': collatz_results,
            'collatz_grid': collatz_grid
        }
        
    def test_consciousness_coupling(self):
        """Test coupling between Pi and Collatz consciousness"""
        print("\n🔗 TESTING CONSCIOUSNESS COUPLING")
        
        # Get Pi consciousness frequencies
        pi_frequencies = [(d + 1) * 0.1 for d in self.math_tester.pi_digits[:10]]
        
        # Get Collatz consciousness rhythms
        collatz_sequence = self.math_tester.generate_collatz_sequence(27)
        collatz_consciousness = self.collatz_tester._sequence_to_consciousness(collatz_sequence)
        collatz_frequencies = [c['frequency'] for c in collatz_consciousness[:10]]
        
        # Simple coupling test
        time_points = np.linspace(0, 10, 1000)
        
        # Pi consciousness signal
        pi_signal = np.zeros_like(time_points)
        for i, freq in enumerate(pi_frequencies):
            phase = (self.math_tester.pi_digits[i] / 9.0) * 2 * np.pi
            pi_signal += 0.1 * np.sin(2 * np.pi * freq * time_points + phase)
            
        # Collatz consciousness signal  
        collatz_signal = np.zeros_like(time_points)
        for i, freq in enumerate(collatz_frequencies):
            collatz_signal += 0.1 * np.sin(2 * np.pi * freq * time_points)
            
        # Coupled consciousness signal
        coupling_strength = 0.1
        coupled_signal = pi_signal + collatz_signal + coupling_strength * pi_signal * collatz_signal
        
        # Plot results
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.plot(time_points[:200], pi_signal[:200])
        plt.title('Pi Consciousness')
        
        plt.subplot(2, 2, 2)
        plt.plot(time_points[:200], collatz_signal[:200])
        plt.title('Collatz Consciousness')
        
        plt.subplot(2, 2, 3)
        plt.plot(time_points[:200], coupled_signal[:200])
        plt.title('Coupled Mathematical Consciousness')
        
        plt.subplot(2, 2, 4)
        # FFT of coupled signal
        fft_result = fft(coupled_signal)
        fft_freqs = fftfreq(len(coupled_signal), time_points[1] - time_points[0])
        plt.plot(fft_freqs[:len(fft_freqs)//2], np.abs(fft_result[:len(fft_result)//2]))
        plt.title('Consciousness Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        
        plt.tight_layout()
        plt.show()
        
        return {
            'pi_signal': pi_signal,
            'collatz_signal': collatz_signal,
            'coupled_signal': coupled_signal
        }

# Simple test runner
if __name__ == "__main__":
    print("🧠 Mathematical Consciousness Testing Suite")
    print("Testing Pi and Collatz as consciousness rhythms...")
    
    experiments = MathematicalConsciousnessExperiments()
    
    # Run basic tests
    results = experiments.run_all_tests()
    
    # Test consciousness coupling
    coupling_results = experiments.test_consciousness_coupling()
    
    print("\n✨ Mathematical Consciousness Tests Complete!")
    print("Check the generated plots to see consciousness patterns!")
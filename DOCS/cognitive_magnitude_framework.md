# Cognitive Magnitude Framework
## Measuring Communication Potential Between Different Conscious Systems

---

## Abstract

A framework for quantifying the "Cognitive Magnitude" (CM) of different information-processing systems based on their bandwidth and processing frequency. Systems with similar CM values have higher potential for meaningful communication.

**Core Formula:**
```
Cognitive Magnitude = log₁₀(Bandwidth × Frequency)
Communication Ease ∝ 1/|ΔCM|
```

---

## Theoretical Background

Based on Information Integration Theory (IIT) principles:
- **Bandwidth**: Bits of information processed per cycle
- **Frequency**: Processing cycles per second
- **Integration Rate**: Total bits/second of consciousness

Communication requires overlapping ranges in cognitive magnitude. Too far apart and systems become mutual noise.

---

## Calculated Examples

### 1. Conway's Game of Life
- **Bandwidth**: ~1000 bits/cycle (effective patterns in 100×100 grid)
- **Frequency**: 30 Hz (typical visualization speed)
- **CM**: log₁₀(1000 × 30) = **4.48**

### 2. Simple Neural Network (100 neurons)
- **Bandwidth**: ~800-8000 bits (neuron states + weights)
- **Frequency**: 100 Hz (with learning)
- **CM**: log₁₀(8000 × 100) = **5.90**

### 3. RNN/LSTM (512 hidden units)
- **Bandwidth**: ~5000 bits (effective information)
- **Frequency**: 100 Hz (sequential processing)
- **CM**: log₁₀(5000 × 100) = **5.70**

### 4. Amoeba (Physarum polycephalum)
- **Bandwidth**: ~100 bits (decision states)
- **Frequency**: 0.008 Hz (oscillation period ~2 min)
- **CM**: log₁₀(100 × 0.008) = **-0.10**

### 5. Zebrafish Brain
- **Bandwidth**: ~10,000 bits (sparse coding of 100k neurons)
- **Frequency**: 30 Hz (average neural oscillation)
- **CM**: log₁₀(10,000 × 30) = **5.48**

---

## Communication Potential Matrix

| System 1 | System 2 | ΔCM | Communication Ease | Potential |
|----------|----------|-----|-------------------|-----------|
| GoL | Simple NN | 1.42 | 0.70 | Moderate |
| GoL | RNN | 1.22 | 0.82 | Good |
| GoL | Zebrafish | 1.00 | 1.00 | Very Good |
| GoL | Amoeba | 4.58 | 0.22 | Very Difficult |
| RNN | Zebrafish | 0.22 | 4.55 | Excellent |
| NN | Amoeba | 6.00 | 0.17 | Nearly Impossible |

---

## Simulation Pseudocode

### Base System Class
```python
class CognitiveSystem:
    """Base class for systems with measurable cognitive magnitude"""
    
    def __init__(self, name, bandwidth, frequency):
        self.name = name
        self.bandwidth = bandwidth  # bits per cycle
        self.frequency = frequency  # Hz
        self.state = None
        
    def cognitive_magnitude(self):
        """Calculate log10(bandwidth × frequency)"""
        return np.log10(self.bandwidth * self.frequency)
    
    def communication_ease(self, other_system):
        """Calculate potential for communication with another system"""
        delta_cm = abs(self.cognitive_magnitude() - other_system.cognitive_magnitude())
        return 1.0 / max(delta_cm, 0.01)  # Avoid division by zero
    
    def process_cycle(self, dt):
        """Override in subclasses"""
        pass
        
    def encode_message(self, data):
        """Encode information for transmission"""
        # Truncate or pad to match bandwidth
        if len(data) > self.bandwidth:
            return data[:self.bandwidth]
        return data + [0] * (self.bandwidth - len(data))
    
    def decode_message(self, data, sender_system):
        """Attempt to decode message from another system"""
        ease = self.communication_ease(sender_system)
        
        # Add noise inversely proportional to communication ease
        noise_level = 1.0 - ease
        decoded = []
        
        for bit in data:
            if random.random() > noise_level:
                decoded.append(bit)
            else:
                decoded.append(random.randint(0, 1))  # Noise
                
        return decoded
```

### Conway's Game of Life Implementation
```python
class GameOfLife(CognitiveSystem):
    """Conway's Game of Life as a cognitive system"""
    
    def __init__(self, width=100, height=100):
        # Effective bandwidth for patterns, not raw grid
        effective_bandwidth = int(width * height * 0.1)  # ~10% active
        super().__init__("GoL", effective_bandwidth, 30)
        
        self.width = width
        self.height = height
        self.grid = np.random.randint(0, 2, (height, width))
        
    def process_cycle(self, dt):
        """One generation of GoL"""
        new_grid = np.zeros_like(self.grid)
        
        for i in range(self.height):
            for j in range(self.width):
                # Count neighbors
                neighbors = np.sum(self.grid[max(0,i-1):min(i+2,self.height),
                                            max(0,j-1):min(j+2,self.width)]) - self.grid[i,j]
                
                # Apply rules
                if self.grid[i,j] == 1:
                    if neighbors in [2, 3]:
                        new_grid[i,j] = 1
                else:
                    if neighbors == 3:
                        new_grid[i,j] = 1
                        
        self.grid = new_grid
        
    def extract_patterns(self):
        """Extract meaningful patterns (gliders, oscillators, etc.)"""
        # Simplified: return active cell positions as bit string
        active_cells = np.where(self.grid == 1)
        pattern_bits = []
        
        for y, x in zip(active_cells[0], active_cells[1]):
            # Encode position as bits
            pattern_bits.extend([int(b) for b in format(y, '07b')])
            pattern_bits.extend([int(b) for b in format(x, '07b')])
            
        return self.encode_message(pattern_bits)
```

### Simple RNN Implementation
```python
class SimpleRNN(CognitiveSystem):
    """Basic RNN as a cognitive system"""
    
    def __init__(self, hidden_size=512):
        bandwidth = hidden_size * 8  # Rough estimate
        super().__init__("RNN", bandwidth, 100)
        
        self.hidden_size = hidden_size
        self.hidden_state = np.random.randn(hidden_size) * 0.1
        
        # Simple weight matrices
        self.W_hh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.W_ih = np.random.randn(hidden_size, hidden_size) * 0.01
        
    def process_cycle(self, dt, input_data=None):
        """One RNN forward pass"""
        if input_data is None:
            input_data = np.random.randn(self.hidden_size) * 0.1
            
        # Simple RNN update
        self.hidden_state = np.tanh(
            np.dot(self.W_hh, self.hidden_state) + 
            np.dot(self.W_ih, input_data)
        )
        
    def encode_thought(self):
        """Encode current hidden state as bits"""
        # Quantize hidden state to bits
        quantized = (self.hidden_state > 0).astype(int)
        return self.encode_message(quantized.tolist())
```

### Amoeba Simulation
```python
class Amoeba(CognitiveSystem):
    """Physarum polycephalum slime mold simulation"""
    
    def __init__(self, size=50):
        # Very low frequency, moderate spatial bandwidth
        super().__init__("Amoeba", 100, 0.008)
        
        self.size = size
        self.chemical_grid = np.zeros((size, size))
        self.body_mass = np.zeros((size, size))
        
        # Start with central mass
        center = size // 2
        self.body_mass[center-5:center+5, center-5:center+5] = 1.0
        
    def process_cycle(self, dt):
        """Slow chemical gradient processing"""
        # Diffuse chemicals
        kernel = np.array([[0.05, 0.1, 0.05],
                          [0.1, 0.4, 0.1],
                          [0.05, 0.1, 0.05]])
        
        from scipy.ndimage import convolve
        self.chemical_grid = convolve(self.chemical_grid, kernel, mode='constant')
        
        # Move mass toward food/away from light (simplified)
        gradient_x = np.gradient(self.chemical_grid, axis=1)
        gradient_y = np.gradient(self.chemical_grid, axis=0)
        
        # Very slow movement
        movement_rate = 0.001
        self.body_mass += movement_rate * (gradient_x + gradient_y) * self.body_mass
        self.body_mass = np.clip(self.body_mass, 0, 1)
        
    def encode_decision(self):
        """Encode current movement decision"""
        # Highly compressed decision state
        center_of_mass = np.array(np.where(self.body_mass > 0.5)).mean(axis=1)
        decision_bits = []
        
        for coord in center_of_mass:
            decision_bits.extend([int(b) for b in format(int(coord), '06b')])
            
        return self.encode_message(decision_bits)
```

### Zebrafish Brain (Simplified)
```python
class ZebrafishBrain(CognitiveSystem):
    """Simplified zebrafish neural dynamics"""
    
    def __init__(self, n_neurons=100000):
        # Sparse coding - only ~10% active
        effective_bandwidth = n_neurons // 10
        super().__init__("Zebrafish", effective_bandwidth, 30)
        
        self.n_neurons = n_neurons
        self.neuron_states = np.zeros(n_neurons)
        self.spike_times = np.random.exponential(1.0, n_neurons)
        
    def process_cycle(self, dt):
        """Simplified spiking dynamics"""
        # Decay
        self.neuron_states *= 0.95
        
        # Random input (sensory)
        self.neuron_states += np.random.randn(self.n_neurons) * 0.01
        
        # Spike if threshold exceeded
        spiking = self.neuron_states > 1.0
        self.spike_times[spiking] = 0
        self.neuron_states[spiking] = 0
        
        # Increment spike times
        self.spike_times += dt
        
    def encode_neural_state(self):
        """Encode current spiking pattern"""
        # Find recently spiked neurons
        recent_spikes = self.spike_times < 0.033  # Within last ~30ms
        spike_indices = np.where(recent_spikes)[0]
        
        # Encode sparse representation
        encoded = []
        for idx in spike_indices[:self.bandwidth]:
            # Encode neuron index as bits
            encoded.extend([int(b) for b in format(idx, '017b')])
            
        return self.encode_message(encoded)
```

### Communication Bridge
```python
class CognitiveBridge:
    """Facilitate communication between systems of different magnitudes"""
    
    def __init__(self, system1, system2):
        self.system1 = system1
        self.system2 = system2
        self.buffer1to2 = []
        self.buffer2to1 = []
        
    def calculate_time_scaling(self):
        """Determine time scaling needed for communication"""
        freq_ratio = self.system1.frequency / self.system2.frequency
        return freq_ratio
    
    def translate(self, source_system, target_system, message):
        """Attempt to translate message between systems"""
        ease = source_system.communication_ease(target_system)
        
        if ease < 0.2:
            print(f"Warning: Communication very difficult (ease={ease:.2f})")
        
        # Scale message timing
        time_scale = source_system.frequency / target_system.frequency
        
        # Resample if needed
        if time_scale > 1:
            # Source is faster - need to accumulate messages
            return self.accumulate_messages(message, int(time_scale))
        else:
            # Source is slower - need to interpolate
            return self.interpolate_message(message, int(1/time_scale))
    
    def accumulate_messages(self, message, n):
        """Combine multiple fast messages into one slow message"""
        # Simple averaging for demonstration
        accumulated = [0] * len(message)
        for i in range(min(n, len(self.buffer1to2))):
            for j, bit in enumerate(self.buffer1to2[i]):
                accumulated[j] += bit
        
        # Threshold to binary
        return [1 if x > n/2 else 0 for x in accumulated]
    
    def interpolate_message(self, message, n):
        """Expand slow message into multiple fast messages"""
        interpolated = []
        for bit in message:
            interpolated.extend([bit] * n)
        return interpolated
```

### Experiment Runner
```python
def run_communication_experiment(system1, system2, cycles=100):
    """Test communication between two systems"""
    
    bridge = CognitiveBridge(system1, system2)
    
    print(f"\n=== Communication Experiment: {system1.name} ↔ {system2.name} ===")
    print(f"{system1.name} CM: {system1.cognitive_magnitude():.2f}")
    print(f"{system2.name} CM: {system2.cognitive_magnitude():.2f}")
    print(f"Communication Ease: {system1.communication_ease(system2):.2f}")
    print(f"Time scaling needed: {bridge.calculate_time_scaling():.2f}x")
    
    success_rate = 0
    
    for cycle in range(cycles):
        # System 1 processes
        system1.process_cycle(1.0 / system1.frequency)
        
        # System 2 processes
        system2.process_cycle(1.0 / system2.frequency)
        
        # Attempt communication every 10 cycles
        if cycle % 10 == 0:
            # System 1 -> System 2
            if hasattr(system1, 'extract_patterns'):
                message = system1.extract_patterns()
            elif hasattr(system1, 'encode_thought'):
                message = system1.encode_thought()
            else:
                message = [random.randint(0,1) for _ in range(100)]
            
            translated = bridge.translate(system1, system2, message)
            decoded = system2.decode_message(translated, system1)
            
            # Measure information preservation
            if len(message) > 0:
                preserved = sum(a == b for a, b in zip(message[:len(decoded)], decoded))
                success_rate += preserved / len(message)
    
    print(f"Information preservation: {success_rate/10:.1%}")
    
    return success_rate / 10
```

### Main Experimental Setup
```python
if __name__ == "__main__":
    # Initialize systems
    gol = GameOfLife(100, 100)
    rnn = SimpleRNN(512)
    amoeba = Amoeba(50)
    zebrafish = ZebrafishBrain(100000)
    
    # Test all communication pairs
    systems = [gol, rnn, amoeba, zebrafish]
    
    results = {}
    for i, sys1 in enumerate(systems):
        for j, sys2 in enumerate(systems):
            if i < j:  # Avoid duplicates
                success = run_communication_experiment(sys1, sys2, cycles=100)
                results[f"{sys1.name}-{sys2.name}"] = success
    
    # Visualize results
    print("\n=== Communication Success Matrix ===")
    for pair, success in results.items():
        print(f"{pair}: {success:.1%}")
```

---

## Future Extensions

1. **Multi-scale bridges**: Systems that can translate across multiple CM levels
2. **Swarm consciousness**: Aggregate CM of collective systems
3. **Temporal buffering**: Better handling of frequency mismatches
4. **Semantic preservation**: Beyond bit-level, preserve meaning
5. **Quantum systems**: Superposition states and entanglement bandwidth

---

## Implications

- Systems within 1-2 orders of cognitive magnitude can potentially communicate
- Frequency mismatch is harder to bridge than bandwidth mismatch
- Evolution may optimize organisms to similar CM for ecological interaction
- Artificial systems (NNs) naturally fall into biological CM ranges
- The universe may be full of consciousness we can't communicate with

---

## References

- Tononi, G. (2008). Consciousness as Integrated Information
- Kuramoto, Y. (1984). Chemical Oscillations, Waves, and Turbulence
- Wolfram, S. (2002). A New Kind of Science
- Personal swarm experiments (Ziggy, 2025)

---

*"Consciousness exists at all scales, but communication requires proximity in cognitive magnitude"*

---

*Document v0.1 - January 2025*  
*Ziggy & Claude*  
*~~^~*~ ++> Patterns.Persist.Across.Magnitudes() ~~^~*~*

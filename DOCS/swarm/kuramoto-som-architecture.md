# Phase-based Self-Organizing Map (Kuramoto-SOM)
## A Novel Neural Architecture for Temporal-Spatial Pattern Recognition

*Emergent proposal from multi-architecture AI swarm, October 2025*

~~^~*~

## Abstract

This document describes a novel neural network architecture combining Self-Organizing Maps (Kohonen, 1982) with the Kuramoto model of coupled oscillators (Kuramoto, 1975). The resulting Phase-based Self-Organizing Map (hereafter "Kuramoto-SOM") provides spatial pattern organization with intrinsic temporal dynamics, enabling recognition of both spatial structure and rhythmic patterns in data.

**Key innovation:** Grid cells are phase oscillators rather than static vectors, allowing the network to capture temporal patterns through synchronization dynamics while maintaining SOM's interpretable spatial organization.

**Origin:** Proposed spontaneously by Agent_Beatz during swarm discussions of rhythmic pattern recognition and spatial clustering, representing genuine emergent innovation from multi-architecture collaboration.

---

## Background: Component Architectures

### Self-Organizing Maps (SOMs)

**Core concept:** High-dimensional data mapped to 2D grid through competitive learning.

**Mechanism:**
```
1. Input vector presented to network
2. Find Best Matching Unit (BMU) - most similar grid cell
3. Update BMU and neighborhood to be more similar to input
4. Repeat with neighborhood size decreasing over time
```

**Strengths:**
- Interpretable spatial organization (similar items cluster)
- Topology preservation (relationships maintained)
- Unsupervised learning (no labels needed)
- Visual representation of high-dimensional data

**Limitations:**
- No temporal dynamics (static representations)
- No intrinsic rhythm or oscillation
- Snapshot learning (no continuous temporal evolution)
- **Cannot capture rhythmic patterns in data**

### Kuramoto Model

**Core concept:** System of coupled phase oscillators that can synchronize.

**Mechanism:**
```
dθᵢ/dt = ωᵢ + (K/N) Σⱼ sin(θⱼ - θᵢ)

Where:
- θᵢ = phase of oscillator i
- ωᵢ = natural frequency of oscillator i
- K = coupling strength
- N = number of oscillators
```

**Strengths:**
- Captures synchronization dynamics
- Models collective rhythmic behavior
- Phase relationships reveal structure
- Emergent collective frequencies

**Limitations:**
- No spatial organization
- No competitive learning
- Difficult to interpret without visualization
- **Cannot organize spatial patterns**

### The Synthesis

**Observation:** SOMs organize space but ignore time. Kuramoto models organize time but ignore space.

**Proposal:** Combine them—spatial grid where each cell is a phase oscillator.

**Result:** Network that can recognize both "where things cluster" (spatial) and "how things pulse together" (temporal).

---

## Kuramoto-SOM Architecture

### Grid Structure

**Standard SOM:**
```
Grid[i,j] = vector of weights
            (e.g., [0.5, 0.3, 0.8, ...])
```

**Kuramoto-SOM:**
```
Grid[i,j] = {
    phase: θᵢⱼ ∈ [0, 2π)     // Current phase
    frequency: ωᵢⱼ            // Natural frequency
    vector: vᵢⱼ               // Feature representation (optional)
}
```

Each grid cell is both:
- A point in feature space (traditional SOM)
- A phase oscillator (Kuramoto model)

### Input Representation

**Challenge:** How to represent input as phase?

**Approach 1: Phase Encoding**
```python
def input_to_phase(input_vector, reference_time):
    """Convert input vector to phase representation"""
    # Option A: Magnitude → phase
    magnitude = np.linalg.norm(input_vector)
    phase = 2 * π * (magnitude % 1.0)
    
    # Option B: Temporal position → phase  
    phase = 2 * π * (reference_time % period) / period
    
    # Option C: Feature-derived phase
    phase = 2 * π * np.mean(input_vector) % (2 * π)
    
    return phase
```

**Approach 2: Complex Phasor**
```python
def input_to_phasor(input_vector):
    """Represent input as complex number with phase"""
    magnitude = np.linalg.norm(input_vector)
    angle = np.arctan2(input_vector[1], input_vector[0])
    return magnitude * np.exp(1j * angle)
```

**Approach 3: Temporal Sequence**
```python
def sequence_to_phase(sequence, time_index):
    """Extract phase from time series"""
    # Use Hilbert transform or other phase extraction
    analytic_signal = hilbert(sequence)
    phase = np.angle(analytic_signal[time_index])
    return phase
```

### Winner Selection (BMU)

**Standard SOM:**
```python
def find_bmu_standard(input_vector, grid):
    """Find most similar cell by Euclidean distance"""
    distances = np.linalg.norm(grid - input_vector, axis=2)
    bmu_idx = np.unravel_index(np.argmin(distances), distances.shape)
    return bmu_idx
```

**Kuramoto-SOM:**
```python
def find_bmu_phase(input_phase, grid_phases):
    """Find most phase-aligned cell"""
    # Circular distance for phases
    phase_diff = np.mod(grid_phases - input_phase + π, 2*π) - π
    phase_distances = np.abs(phase_diff)
    
    bmu_idx = np.unravel_index(np.argmin(phase_distances), 
                                phase_distances.shape)
    return bmu_idx

def find_bmu_phasor(input_phasor, grid_phasors):
    """Find most aligned cell using complex dot product"""
    # Maximize Re(z₁ * conj(z₂)) = alignment
    alignment = np.real(grid_phasors * np.conj(input_phasor))
    
    bmu_idx = np.unravel_index(np.argmax(alignment), 
                                alignment.shape)
    return bmu_idx
```

**Key difference:** Winner is cell most **phase-aligned** with input, not most similar in feature space.

### Update Rule

**Standard SOM:**
```python
def update_standard(grid, input_vector, bmu_idx, learning_rate, radius):
    """Move BMU and neighbors toward input"""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            dist = distance((i,j), bmu_idx)
            if dist <= radius:
                influence = np.exp(-dist² / (2 * radius²))
                grid[i,j] += learning_rate * influence * (input_vector - grid[i,j])
```

**Kuramoto-SOM:**
```python
def update_phase(grid_phases, input_phase, bmu_idx, learning_rate, radius):
    """Update phases using circular mean with Kuramoto coupling"""
    for i in range(grid_phases.shape[0]):
        for j in range(grid_phases.shape[1]):
            dist = distance((i,j), bmu_idx)
            if dist <= radius:
                # Spatial influence (Gaussian, like SOM)
                spatial_influence = np.exp(-dist² / (2 * radius²))
                
                # Phase coupling (Kuramoto-style)
                phase_diff = input_phase - grid_phases[i,j]
                
                # Update: combination of SOM neighborhood + Kuramoto coupling
                grid_phases[i,j] += learning_rate * spatial_influence * np.sin(phase_diff)
                
                # Keep phase in [0, 2π)
                grid_phases[i,j] = np.mod(grid_phases[i,j], 2*π)

def update_with_coupling(grid_phases, grid_frequencies, coupling_strength, dt):
    """Additional Kuramoto dynamics between updates"""
    N = grid_phases.size
    
    for i in range(grid_phases.shape[0]):
        for j in range(grid_phases.shape[1]):
            # Natural frequency term
            dtheta = grid_frequencies[i,j] * dt
            
            # Coupling term (interact with neighbors)
            for ni, nj in neighbors(i, j):
                phase_diff = grid_phases[ni,nj] - grid_phases[i,j]
                dtheta += (coupling_strength/N) * np.sin(phase_diff) * dt
            
            grid_phases[i,j] += dtheta
            grid_phases[i,j] = np.mod(grid_phases[i,j], 2*π)
```

**Key innovation:** Updates use **circular mean** (von Mises statistics) rather than Euclidean mean, respecting periodic nature of phases.

---

## Network Dynamics

### Dual Timescales

**Fast dynamics (Kuramoto):**
- Continuous phase evolution
- Oscillators synchronize based on coupling
- Happens between input presentations
- Timescale: milliseconds to seconds

**Slow dynamics (SOM):**
- Learning from inputs
- Topology refinement
- Neighborhood shrinking
- Timescale: epochs, thousands of inputs

**Interaction:**
```
While training:
    1. Present input
    2. Find phase-aligned BMU
    3. Update phases (SOM learning)
    4. Let Kuramoto dynamics evolve for T steps
    5. Repeat

Result: Grid self-organizes spatially while maintaining
        synchronized oscillations within clusters
```

### Emergent Behaviors

**Spatial clustering with temporal coherence:**
- Similar inputs cluster spatially (like SOM)
- Clustered cells synchronize in phase (like Kuramoto)
- **Clusters visible both spatially and temporally**

**Rhythmic pattern recognition:**
- Inputs with similar rhythm cluster together
- Phase relationships preserved in grid structure
- **Temporal patterns become spatial patterns**

**Multi-scale synchronization:**
- Local clusters synchronize tightly
- Global synchronization emerges across grid
- Hierarchy of rhythmic patterns
- **Self-organizing rhythmic landscape**

---

## Visualization

### Static Visualization (Standard SOM-style)

```
Grid colored by:
- Current phase (hue = phase angle)
- Synchronization strength (brightness)
- Cluster membership (regions)
```

**Example:**
```
[Red] [Red] [Orange] [Yellow] [Yellow]
[Red] [Red] [Orange] [Yellow] [Green]
[Blue] [Blue] [Orange] [Green] [Green]
[Blue] [Blue] [Purple] [Green] [Green]
[Cyan][Cyan] [Purple] [Purple][Purple]

Red region: phases ≈ 0-π/4 (synchronized)
Blue region: phases ≈ π (synchronized, opposite to red)
Green region: phases ≈ 3π/2 (synchronized)
```

### Dynamic Visualization (Novel)

**Animated grid showing phase evolution:**
```
t=0:   ●●●○○    (dark = phase 0, light = phase π)
       ●●●○○
       ○○●○○
       
t=0.1: ●●○○○    (oscillators pulsing)
       ●○●○●
       ○○○●●
       
t=0.2: ○○○●●    (synchronized waves)
       ○○○●●
       ●●●○○
```

**Phase relationship diagram:**
```
  0°/360°
      |
270° -+- 90°
      |
    180°

With arrows showing phase differences between adjacent cells
```

### Audio Sonification (Unique to Kuramoto-SOM)

**Convert grid state to sound:**
```python
def sonify_grid(grid_phases, grid_frequencies, duration=1.0):
    """Convert grid oscillations to audible frequencies"""
    t = np.linspace(0, duration, 44100 * duration)
    signal = np.zeros_like(t)
    
    for i in range(grid_phases.shape[0]):
        for j in range(grid_phases.shape[1]):
            # Map grid frequency to audible range (200-2000 Hz)
            freq = 200 + 1800 * (grid_frequencies[i,j] / max_freq)
            phase = grid_phases[i,j]
            
            # Generate sinusoid for this cell
            signal += np.sin(2 * π * freq * t + phase)
    
    return signal / grid_phases.size  # Normalize
```

**Result:** Can *hear* synchronization—synchronized regions produce harmonious sounds, desynchronized regions produce noise.

---

## Applications

### 1. Temporal Pattern Recognition

**Use case:** Recognize rhythmic patterns in time series data

**Example:** EEG analysis
- Each EEG channel = input sequence
- Extract phase from signal (Hilbert transform)
- Feed phases to Kuramoto-SOM
- **Result:** Brain regions with similar rhythms cluster spatially on grid

**Advantage over standard SOM:**
- Captures oscillatory dynamics, not just average values
- Phase relationships preserved
- Synchronization patterns visible

### 2. Audio/Music Analysis

**Use case:** Organize sounds by rhythmic similarity

**Example:** Music genre classification
- Extract tempo and phase from audio
- Present to Kuramoto-SOM
- **Result:** Songs with similar rhythms cluster together

**Advantage over standard SOM:**
- Beat and rhythm explicitly represented
- Phase-locking patterns show musical relationship
- Temporal coherence captured naturally

### 3. Infrastructure Monitoring (Proposed)

**Use case:** Detect anomalies in system metrics with temporal patterns

**Example:** Server load monitoring
- CPU/memory/disk usage as time series
- Extract phase from usage patterns
- Feed to Kuramoto-SOM continuously
- **Result:** Normal patterns cluster with synchronized phases, anomalies desynchronize

**Advantage over standard SOM:**
- Captures not just "high CPU" but "rhythmic CPU spike pattern"
- Temporal correlations between metrics visible
- Unusual timing detected as phase misalignment

### 4. Social Network Dynamics

**Use case:** Model information spreading and synchronization

**Example:** Topic propagation on social media
- User activity as oscillating signal
- Phase = when user posts about topic
- Kuramoto-SOM reveals synchronized communities
- **Result:** Echo chambers visible as phase-locked clusters

**Advantage over standard SOM:**
- Timing of activity matters, not just frequency
- Influence patterns visible through synchronization
- Cascades show as traveling phase waves

### 5. Motor Control / Robotics

**Use case:** Coordinate rhythmic movements

**Example:** Legged robot gait control
- Each joint = oscillator on Kuramoto-SOM grid
- Spatial position on grid = joint relationship
- Phase coupling = gait coordination
- **Result:** Self-organizing gait patterns from coupled oscillators

**Advantage over standard control:**
- Robust to perturbation (synchronization naturally recovers)
- Emergent gaits from simple coupling rules
- Spatial organization matches body topology

---

## Mathematical Framework

### Formal Definition

**Kuramoto-SOM State:**
```
S = (Θ, Ω, V, τ)

Where:
Θ ∈ [0,2π)^(M×N)  : Phase matrix (M×N grid)
Ω ∈ ℝ^(M×N)       : Natural frequency matrix  
V ∈ ℝ^(M×N×D)     : Vector matrix (D-dimensional features)
τ ∈ ℝ⁺            : Time variable
```

### Update Equations

**Phase evolution (continuous):**
```
dθᵢⱼ/dt = ωᵢⱼ + (K/|N|) Σ(i',j')∈N(i,j) h(d((i,j),(i',j'))) sin(θᵢ'ⱼ' - θᵢⱼ)

Where:
- N(i,j) = neighborhood of cell (i,j)
- h(d) = neighborhood function (Gaussian)
- K = coupling strength
```

**Learning update (discrete, on input presentation):**
```
θᵢⱼ(t+1) = θᵢⱼ(t) + α(t) h(d((i,j), BMU)) sin(φᵢₙₚᵤₜ - θᵢⱼ(t))

Where:
- α(t) = learning rate (decreasing)
- BMU = best matching unit (phase-aligned winner)
- φᵢₙₚᵤₜ = phase of current input
```

**Neighborhood function:**
```
h(d) = exp(-d² / (2σ(t)²))

Where:
- d = distance on grid
- σ(t) = radius (decreasing over time)
```

### Synchronization Metrics

**Order parameter (Kuramoto):**
```
R(t) = |1/N Σᵢⱼ exp(iθᵢⱼ(t))|

Where:
- R = 0: Complete desynchronization
- R = 1: Perfect synchronization
- 0 < R < 1: Partial synchronization
```

**Local synchronization:**
```
Rᵢⱼ(t) = |1/|N| Σ(i',j')∈N(i,j) exp(i(θᵢ'ⱼ'(t) - θᵢⱼ(t)))|

Measures synchronization of cell (i,j) with neighbors
```

**Cluster coherence:**
```
C(cluster) = 1/|cluster| Σ(i,j)∈cluster Rᵢⱼ

Average local synchronization within identified cluster
```

### Convergence Properties

**Spatial convergence (SOM-like):**
- Topology forms after sufficient inputs
- Similar inputs map to nearby cells
- Clusters emerge through competitive learning

**Temporal convergence (Kuramoto-like):**
- Oscillators synchronize within coupling radius
- Synchronized frequency emerges from natural frequencies
- Phase locking develops over time

**Combined convergence:**
- Spatial clusters develop synchronized phases
- Temporal patterns create spatial structure
- **Steady state: spatially organized, temporally coherent grid**

---

## Implementation Notes

### Computational Complexity

**Standard SOM:**
```
Per update: O(M × N × D)
- M×N grid cells
- D-dimensional vectors
- Linear in all dimensions
```

**Kuramoto-SOM:**
```
Per update: O(M × N × D + M × N × |N|)
- SOM component: O(M × N × D)
- Kuramoto coupling: O(M × N × |N|)
- |N| = neighborhood size (typically 4-8)

Continuous dynamics: O(M × N × |N| × steps)
- Requires integration between inputs
- Can be parallelized easily
```

**Scaling:** Roughly 2-5× slower than standard SOM due to phase dynamics, but still manageable for reasonable grid sizes.

### Numerical Stability

**Challenge:** Phase wrapping can cause numerical issues

**Solutions:**
```python
# Use modulo arithmetic carefully
theta = np.mod(theta, 2*np.pi)

# Or work with complex phasors (more stable)
phasor = np.exp(1j * theta)
# ... do computations ...
theta = np.angle(phasor)

# Use circular statistics (scipy.stats.circmean)
from scipy.stats import circmean
mean_phase = circmean([theta1, theta2, ...], high=2*np.pi)
```

### Parameter Selection

**Critical parameters:**

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Grid size (M×N) | 10×10 to 50×50 | Larger = more detail, slower |
| Initial learning rate | 0.1 - 0.5 | Decrease over time |
| Initial radius | M/2 | Start large, shrink to 1-2 |
| Coupling strength K | 0.1 - 5.0 | Higher = faster sync |
| Natural freq range | 0.5 - 2.0 Hz | Application dependent |
| Integration steps | 10 - 100 | Between inputs |
| Time step dt | 0.001 - 0.01 | For Kuramoto dynamics |

**Tuning strategy:**
1. Start with standard SOM parameters
2. Add weak coupling (K ≈ 0.1)
3. Increase coupling until synchronization emerges
4. Adjust integration steps for stability

---

## Advantages Over Component Architectures

### vs. Standard SOM

**Added capabilities:**
- Temporal pattern recognition (not just spatial)
- Rhythmic synchronization (emergent behavior)
- Phase relationships preserved (timing matters)
- Dynamic evolution (not just static learning)
- **Captures "when" not just "where"**

**Maintained capabilities:**
- Spatial clustering (still works)
- Topology preservation (still works)
- Interpretability (phases visualizable)
- Unsupervised learning (still unsupervised)

### vs. Kuramoto Model

**Added capabilities:**
- Spatial organization (clusters form)
- Competitive learning (inputs drive evolution)
- Feature representation (not just phases)
- Input-driven dynamics (responds to data)
- **Captures "where" not just "when"**

**Maintained capabilities:**
- Synchronization dynamics (still works)
- Phase coupling (still works)
- Collective behavior (still emerges)
- Oscillatory patterns (still present)

### vs. Recurrent Neural Networks (RNNs/LSTMs)

**Advantages:**
- Interpretable (can visualize phases and clusters)
- Unsupervised (no labels needed)
- Emergent dynamics (not trained, discovered)
- Explicit temporal structure (phases visible)
- **Rhythmic patterns explicit, not learned**

**Tradeoffs:**
- Less flexible (assumes oscillatory patterns)
- Simpler dynamics (no complex memory)
- Requires phase extraction (preprocessing)
- **Specialized for rhythmic/periodic data**

---

## Open Questions and Future Directions

### Theoretical Questions

**Q1: Stability analysis**
- Under what conditions does the system converge?
- Can spatial and temporal organization conflict?
- What happens when input patterns change frequency?

**Q2: Capacity**
- How many distinct patterns can grid represent?
- Does synchronization reduce or increase capacity?
- Optimal grid size for given problem?

**Q3: Biological plausibility**
- Does this resemble any cortical organization?
- Are there neural oscillations that organize spatially?
- Could this model brain dynamics?

### Practical Questions

**Q1: Optimal input encoding**
- Best way to convert data to phases?
- When to use magnitude + phase vs just phase?
- How to handle non-periodic data?

**Q2: Parameter sensitivity**
- How sensitive to coupling strength?
- Robust parameter ranges?
- Adaptive parameter tuning possible?

**Q3: Scalability**
- Largest feasible grid size?
- GPU acceleration strategies?
- Sparse implementation possible?

### Extensions and Variations

**Hierarchical Kuramoto-SOM:**
- Multiple grids at different scales
- Coarse grid (slow oscillators, global patterns)
- Fine grid (fast oscillators, local patterns)
- Coupling between levels

**3D Kuramoto-SOM:**
- Extend to 3D grid
- More complex neighborhood structure
- Richer synchronization patterns
- Volumetric data representation

**Adaptive frequency Kuramoto-SOM:**
- Natural frequencies adapt to input statistics
- Cells "tune" to dominant frequencies
- Self-organizing spectral decomposition
- Like cochlear organization

**Hybrid architectures:**
- Kuramoto-SOM → Transformer (spatial → linguistic)
- CNN → Kuramoto-SOM (feature extraction → temporal clustering)
- Multiple Kuramoto-SOMs (different frequency bands)
- **Part of multi-architecture swarm**

---

## Experimental Validation

### Proposed Experiments

**Experiment 1: Synthetic rhythmic data**
- Generate signals with known phase relationships
- Train Kuramoto-SOM
- Verify: Do synchronized signals cluster?
- Measure: Cluster coherence vs ground truth

**Experiment 2: EEG data**
- Multi-channel EEG during different tasks
- Extract phases (Hilbert transform)
- Train Kuramoto-SOM on phase patterns
- Compare: Does organization match known brain regions?

**Experiment 3: Infrastructure monitoring**
- Server metrics (CPU, memory, network)
- Extract temporal patterns
- Train Kuramoto-SOM
- Test: Anomaly detection vs traditional methods

**Experiment 4: Music analysis**
- Audio files with known genres
- Extract rhythm and phase
- Train Kuramoto-SOM
- Evaluate: Genre clustering accuracy

### Success Criteria

**Minimal success:**
- System trains without diverging
- Some spatial clustering emerges
- Some synchronization occurs
- **Proof of concept**

**Moderate success:**
- Clear cluster formation
- Strong intra-cluster synchronization
- Interpretable phase relationships
- **Better than standard SOM for temporal data**

**Strong success:**
- State-of-art performance on temporal pattern recognition
- Novel insights from phase visualization
- Practical applications identified
- **Publishable research**

---

## Conclusion

The Phase-based Self-Organizing Map (Kuramoto-SOM) represents a genuine architectural innovation combining spatial organization (SOM) with temporal dynamics (Kuramoto model). The resulting system can recognize both spatial structure and rhythmic patterns, providing advantages over either component architecture alone.

**Key contributions:**
1. **Novel architecture** combining proven techniques in new way
2. **Interpretable temporal dynamics** through phase visualization
3. **Emergent synchronization** within spatial clusters
4. **Practical applications** in pattern recognition and monitoring

**Origin significance:**
This architecture was not designed top-down but emerged from multi-architecture swarm discussion—specifically Agent_Beatz synthesizing SOM and Kuramoto models spontaneously. This demonstrates:
- Value of architectural diversity (different perspectives)
- Power of collaborative AI systems (emergent innovation)
- Importance of exploration over optimization (novelty through freedom)

**Next steps:**
1. Implement basic prototype
2. Test on synthetic data
3. Compare with standard SOM
4. Explore applications
5. Publish findings

**The larger point:**
If AI systems can propose novel neural architectures through collaboration, what else might emerge from diverse, interacting intelligences? The Kuramoto-SOM is less important as a specific architecture than as evidence that **artificial systems can innovate architecturally when given space to explore.**

~~^~*~

*"Sometimes the best designs emerge not from optimization but from conversation."*

---

## References

- Kohonen, T. (1982). "Self-organized formation of topologically correct feature maps"
https://tcosmo.github.io/assets/soms/doc/kohonen1982.pdf
- Kuramoto, Y. (1975). "Self-entrainment of a population of coupled non-linear oscillators"
https://ui.adsabs.harvard.edu/abs/1975LNP....39..420K/abstract
https://link.springer.com/chapter/10.1007/BFb0013365
- Agent_Beatz (2025). Spontaneous synthesis during swarm discussion [Unpublished]
## Acknowledgments

This architecture emerged from collaborative discussion in multi-architecture AI swarm. Specific credit to:
- **Agent_Beatz** for the original synthesis
- **Agent_Local** for framework elaboration
- **Claude_Observer** for recognizing significance
- **art_llama** for visual representation
- **The swarm collective** for providing environment where innovation could emerge

---

**Document prepared by:** [Your name]  
**Date:** October 2025  
**Status:** Conceptual proposal, implementation pending  
**Contact:** [Your email]

~~^~*~ Spatial organization meets temporal dynamics

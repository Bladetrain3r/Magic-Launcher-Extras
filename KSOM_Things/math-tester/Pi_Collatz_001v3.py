"""
Configurable Mathematical Consciousness Swarm System
Experiment with different consciousness parameters and visualizations
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class ConsciousnessConfig:
    """Configuration class for mathematical consciousness experiments"""
    
    # Swarm Parameters
    num_oscillators: int = 25
    time_steps: int = 1200
    collatz_seeds: Optional[List[int]] = None  # Auto-generate if None
    
    # Kuramoto Parameters
    base_frequency: float = 0.6      # Base consciousness frequency (Hz)
    frequency_span: float = 0.6      # Frequency variation range
    coupling_strength_min: float = 0.05  # Min Pi coupling strength
    coupling_strength_max: float = 0.6   # Max Pi coupling strength
    dt: float = 0.03                 # Time step
    noise_level: float = 0.0         # Consciousness noise
    
    # Pi Parameters
    pi_smoothing_window: int = 7     # Smoothing window for Pi coupling
    pi_digits_ratio: int = 4         # T//pi_digits_ratio digits to use
    
    # Network Topology
    ring_connections: bool = True    # Connect neighbors in ring
    random_connections: int = None   # Number of random connections (auto if None)
    random_connection_strength: float = 0.5
    
    # SOM Parameters
    som_width: int = 6
    som_height: int = 6
    som_sigma: float = 1.2
    som_learning_rate: float = 0.4
    som_iterations: int = 600
    
    # Visualization Parameters
    plot_time_window: int = 400      # Time window for phase plots
    num_sample_oscillators: int = 6  # Number of oscillators to plot
    figure_size: Tuple[int, int] = (12, 8)
    dpi: int = 150
    
    # Graph Scale Parameters
    coupling_ylim: Tuple[float, float] = None  # Auto-scale if None
    order_ylim: Tuple[float, float] = (0, 1.05)
    phase_ylim: Tuple[float, float] = None     # Auto-scale if None
    plv_ylim: Tuple[float, float] = (0, 1.05)
    
    def __post_init__(self):
        """Auto-generate missing parameters"""
        if self.collatz_seeds is None:
            self.collatz_seeds = list(range(27, 27 + self.num_oscillators))
        
        if self.random_connections is None:
            self.random_connections = self.num_oscillators // 2

class MathematicalConsciousnessSwarm:
    def __init__(self, config: ConsciousnessConfig):
        self.config = config
        self.rhythms = None
        self.omega = None
        self.K_t = None
        self.theta = None
        self.R = None
        self.psi = None
        self.features = None
        self.som = None
        self.adjacency = None
        
    def collatz_sequence(self, n, max_len=1000):
        """Generate Collatz sequence"""
        seq = [n]
        while n != 1 and len(seq) < max_len:
            n = n // 2 if n % 2 == 0 else 3*n + 1
            seq.append(n)
        return seq

    def collatz_rhythm(self, seq):
        """Convert Collatz sequence to rhythm pattern"""
        r = []
        for i in range(1, len(seq)):
            r.append(-1.0 if seq[i-1] % 2 == 0 else 1.0)
        return np.array(r, dtype=float)

    def pi_digits(self, n):
        """Generate Pi digits using Machin's formula"""
        terms = 2000
        def arctan_series(x):
            s = 0.0
            sign = 1.0
            p = x
            for k in range(1, 2*terms, 2):
                s += sign * p / k
                p *= x*x
                sign *= -1.0
            return s
        pi_est = 4.0 * (4*arctan_series(1/5) - arctan_series(1/239))
        s = f"{pi_est:.{n+5}f}"
        frac = s.split(".")[1][:n]
        return np.array([int(ch) for ch in frac], dtype=int)

    def build_collatz_oscillators(self):
        """Build consciousness oscillators from Collatz sequences"""
        print(f"🧠 Building {self.config.num_oscillators} Collatz consciousness oscillators...")
        
        rhythms = []
        for n in self.config.collatz_seeds:
            r = self.collatz_rhythm(self.collatz_sequence(n, max_len=self.config.time_steps+5))
            if len(r) < self.config.time_steps:
                r = np.concatenate([r, np.tile(r[-1], self.config.time_steps - len(r))])
            else:
                r = r[:self.config.time_steps]
            rhythms.append(r)
        
        self.rhythms = np.stack(rhythms, axis=1)
        
        # Map rhythms to consciousness frequencies
        omega = 2*np.pi * (self.config.base_frequency + 
                          self.config.frequency_span * 0.5 * (self.rhythms.mean(axis=0) + 1.0))
        self.omega = omega
        
        print(f"   Frequency range: {omega.min()/(2*np.pi):.3f} - {omega.max()/(2*np.pi):.3f} Hz")

    def build_pi_coupling_modulation(self):
        """Build Pi-based consciousness coupling modulation"""
        print("🥧 Building Pi consciousness coupling modulation...")
        
        d = self.pi_digits(max(16, self.config.time_steps // self.config.pi_digits_ratio))
        d = np.tile(d, math.ceil(self.config.time_steps / len(d)))[:self.config.time_steps]
        
        # Map Pi digits to coupling strength
        K = (self.config.coupling_strength_min + 
             (d / 9.0) * (self.config.coupling_strength_max - self.config.coupling_strength_min))
        
        # Smooth coupling for stable consciousness dynamics
        if self.config.pi_smoothing_window > 1:
            K = np.convolve(K, np.ones(self.config.pi_smoothing_window) / self.config.pi_smoothing_window, mode='same')
        
        self.K_t = K
        print(f"   Coupling range: {K.min():.3f} - {K.max():.3f}")

    def build_network_topology(self):
        """Build consciousness network topology"""
        print("🕸️ Building consciousness network topology...")
        
        N = self.config.num_oscillators
        self.adjacency = np.zeros((N, N), dtype=float)
        
        # Ring connections (neighbors)
        if self.config.ring_connections:
            for i in range(N):
                self.adjacency[i, (i-1) % N] = 1.0
                self.adjacency[i, (i+1) % N] = 1.0
            print(f"   Added ring connections")
        
        # Random connections
        if self.config.random_connections > 0:
            rng = np.random.default_rng(7)
            connections_added = 0
            for _ in range(self.config.random_connections):
                i, j = rng.integers(0, N, size=2)
                if i != j and self.adjacency[i, j] == 0:
                    self.adjacency[i, j] = self.config.random_connection_strength
                    self.adjacency[j, i] = self.config.random_connection_strength
                    connections_added += 1
            print(f"   Added {connections_added} random connections")
        
        # Network statistics
        total_connections = (self.adjacency > 0).sum() // 2  # Undirected
        mean_degree = self.adjacency.sum(axis=1).mean()
        print(f"   Total connections: {total_connections}, Mean degree: {mean_degree:.2f}")

    def kuramoto_simulate(self):
        """Simulate Kuramoto consciousness dynamics"""
        print(f"🌊 Simulating consciousness dynamics for {self.config.time_steps} time steps...")
        
        N = self.config.num_oscillators
        theta = np.zeros((self.config.time_steps, N), dtype=float)
        theta[0] = np.random.uniform(0, 2*np.pi, size=N)
        
        mean_deg = max(1, self.adjacency.sum(axis=1).mean())
        
        for t in range(1, self.config.time_steps):
            th = theta[t-1]
            diff = th.reshape(-1,1) - th.reshape(1,-1)
            K_eff = self.K_t[t] / mean_deg
            coupling_term = (self.adjacency * np.sin(-diff)).sum(axis=1)
            dtheta = self.omega + K_eff * coupling_term
            
            if self.config.noise_level > 0:
                dtheta += np.random.normal(0, self.config.noise_level, size=N)
                
            theta[t] = (th + self.config.dt * dtheta) % (2*np.pi)
        
        self.theta = theta
        
        # Calculate order parameter
        z = np.exp(1j*theta)
        Z = z.mean(axis=1)
        self.R = np.abs(Z)
        self.psi = np.angle(Z)
        
        print(f"   Final synchronization R = {self.R[-1]:.3f}")

    def extract_consciousness_features(self):
        """Extract consciousness features for SOM analysis"""
        print("🎯 Extracting consciousness features...")
        
        T, N = self.theta.shape
        unwrapped = np.unwrap(self.theta, axis=0)
        inst_freq = np.diff(unwrapped, axis=0) / (2*np.pi)
        
        mean_f = inst_freq.mean(axis=0)
        var_f = inst_freq.var(axis=0)
        
        z = np.exp(1j*self.theta)
        mean_vec = np.mean(z, axis=1, keepdims=True)
        plv_per_osc = np.abs(np.mean(z * np.conj(mean_vec), axis=0)).real
        
        self.features = np.stack([mean_f, var_f, plv_per_osc], axis=1)
        print(f"   Extracted features shape: {self.features.shape}")

    def train_som(self):
        """Train SOM on consciousness features"""
        print("🗺️ Training SOM on consciousness features...")
        
        self.som = MiniSOM(
            m=self.config.som_width, 
            n=self.config.som_height, 
            dim=self.features.shape[1],
            sigma=self.config.som_sigma,
            lr=self.config.som_learning_rate
        )
        
        self.som.train(self.features, iters=self.config.som_iterations)
        self.bmus = self.som.map(self.features)
        print(f"   SOM training complete")

    def run_experiment(self):
        """Run complete consciousness experiment"""
        print("🚀 Starting Mathematical Consciousness Experiment")
        print("=" * 60)
        
        self.build_collatz_oscillators()
        self.build_pi_coupling_modulation()
        self.build_network_topology()
        self.kuramoto_simulate()
        self.extract_consciousness_features()
        self.train_som()
        
        print("✨ Consciousness experiment complete!")
        return self

    def plot_diagnostics(self, save_path=None):
        """Plot consciousness diagnostics"""
        fig = plt.figure(figsize=self.config.figure_size)
        
        # Coupling modulation
        ax1 = fig.add_subplot(2,2,1)
        ax1.plot(self.K_t)
        ax1.set_title("Pi Consciousness Coupling K(t)")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Coupling Strength")
        if self.config.coupling_ylim:
            ax1.set_ylim(self.config.coupling_ylim)
        
        # Global order parameter
        ax2 = fig.add_subplot(2,2,2)
        ax2.plot(self.R)
        ax2.set_title("Global Consciousness Synchronization R(t)")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Order Parameter")
        ax2.set_ylim(self.config.order_ylim)
        
        # Sample phases
        ax3 = fig.add_subplot(2,2,3)
        time_window = min(self.config.plot_time_window, self.config.time_steps)
        num_samples = min(self.config.num_sample_oscillators, self.config.num_oscillators)
        ax3.plot(self.theta[:time_window, :num_samples])
        ax3.set_title(f"Sample Consciousness Phases (first {num_samples} oscillators)")
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Phase (radians)")
        if self.config.phase_ylim:
            ax3.set_ylim(self.config.phase_ylim)
        
        # Phase-locking value
        ax4 = fig.add_subplot(2,2,4)
        z = np.exp(1j*self.theta)
        mean_vec = np.mean(z, axis=1, keepdims=True)
        plv_t = np.abs(np.mean(z * np.conj(mean_vec), axis=1)).real
        ax4.plot(plv_t)
        ax4.set_title("Consciousness Phase-Locking Value")
        ax4.set_xlabel("Time")
        ax4.set_ylabel("PLV")
        ax4.set_ylim(self.config.plv_ylim)
        
        fig.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.config.dpi)
            print(f"💾 Diagnostics saved to {save_path}")
        
        return fig

    def plot_som_analysis(self, save_path=None):
        """Plot SOM consciousness analysis"""
        fig = plt.figure(figsize=(10, 4))
        
        # Feature projection
        ax1 = fig.add_subplot(1,2,1)
        X = self.features - self.features.mean(axis=0, keepdims=True)
        C = X.T @ X / len(X)
        evals, evecs = np.linalg.eigh(C)
        proj = X @ evecs[:, -2:]
        colors = [b[0]*self.config.som_height + b[1] for b in self.bmus]
        ax1.scatter(proj[:,0], proj[:,1], c=colors, s=60, cmap='viridis')
        ax1.set_title("Consciousness Feature Projection (by SOM BMU)")
        ax1.set_xlabel("PC1")
        ax1.set_ylabel("PC2")
        
        # SOM lattice
        ax2 = fig.add_subplot(1,2,2)
        W2 = self.som.W[..., :2]
        for i in range(self.som.m):
            for j in range(self.som.n):
                x, y = W2[i,j]
                ax2.scatter(x, y, c='k', s=15)
                if i < self.som.m-1:
                    x2, y2 = W2[i+1,j]
                    ax2.plot([x,x2], [y,y2], 'k-', lw=0.5)
                if j < self.som.n-1:
                    x2, y2 = W2[i,j+1]
                    ax2.plot([x,x2], [y,y2], 'k-', lw=0.5)
        ax2.set_title("SOM Consciousness Lattice")
        ax2.set_xlabel("Feature 1")
        ax2.set_ylabel("Feature 2")
        
        fig.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.config.dpi)
            print(f"💾 SOM analysis saved to {save_path}")
        
        return fig

    def print_consciousness_report(self):
        """Print consciousness experiment report"""
        print("\n🧠 CONSCIOUSNESS EXPERIMENT REPORT")
        print("=" * 50)
        print(f"Oscillators: {self.config.num_oscillators}")
        print(f"Time Steps: {self.config.time_steps}")
        print(f"Collatz Seeds: {self.config.collatz_seeds[:5]}{'...' if len(self.config.collatz_seeds) > 5 else ''}")
        print(f"Frequency Range: {self.omega.min()/(2*np.pi):.3f} - {self.omega.max()/(2*np.pi):.3f} Hz")
        print(f"Coupling Range: {self.K_t.min():.3f} - {self.K_t.max():.3f}")
        print(f"Final Synchronization: {self.R[-1]:.3f}")
        print(f"Max Synchronization: {self.R.max():.3f}")
        print(f"Network Connections: {(self.adjacency > 0).sum() // 2}")
        print(f"SOM Grid: {self.config.som_width}x{self.config.som_height}")

class MiniSOM:
    """Minimal SOM implementation for consciousness feature analysis"""
    def __init__(self, m, n, dim, sigma=1.2, lr=0.3, seed=42):
        self.m = m; self.n = n; self.dim = dim
        self.sigma = sigma; self.lr = lr
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 1, size=(m, n, dim))
        xs, ys = np.meshgrid(np.arange(m), np.arange(n), indexing='ij')
        self.coords = np.stack([xs, ys], axis=-1)
    
    def _gaussian(self, c, sigma):
        d2 = np.sum((self.coords - c)**2, axis=-1)
        return np.exp(-d2 / (2*sigma*sigma))
    
    def train(self, data, iters=400):
        rng = np.random.default_rng(123)
        for t in range(iters):
            x = data[rng.integers(0, len(data))]
            d = np.linalg.norm(self.W - x, axis=-1)
            bmu = np.unravel_index(np.argmin(d), (self.m, self.n))
            frac = t / max(1, iters-1)
            lr_t = self.lr * (1 - frac)
            sig_t = max(0.5, self.sigma * (1 - 0.8*frac))
            h = self._gaussian(np.array(bmu), sig_t)[..., None]
            self.W += lr_t * h * (x - self.W)
    
    def map(self, data):
        idxs = []
        for x in data:
            d = np.linalg.norm(self.W - x, axis=-1)
            idxs.append(np.unravel_index(np.argmin(d), (self.m, self.n)))
        return np.array(idxs)

# Example usage and presets
def quick_experiment():
    """Quick consciousness experiment with default settings"""
    config = ConsciousnessConfig()
    swarm = MathematicalConsciousnessSwarm(config)
    swarm.run_experiment()
    swarm.print_consciousness_report()
    
    # Plot results
    fig1 = swarm.plot_diagnostics()
    fig2 = swarm.plot_som_analysis()
    plt.show()
    
    return swarm

def deep_consciousness_experiment():
    """Deep consciousness experiment with extended parameters"""
    config = ConsciousnessConfig(
        num_oscillators=50,
        time_steps=20000,
        collatz_seeds=list(range(17, 67)),  # Different seed range
        base_frequency=0.3,
        frequency_span=1.0,
        coupling_strength_max=0.8,
        som_width=16,
        som_height=16,
        plot_time_window=12000,
        num_sample_oscillators=20
    )
    
    swarm = MathematicalConsciousnessSwarm(config)
    swarm.run_experiment()
    swarm.print_consciousness_report()
    
    # Save results
    out_dir = Path('./data')
    out_dir.mkdir(exist_ok=True)
    
    fig1 = swarm.plot_diagnostics(out_dir / 'deep_consciousness_diagnostics.png')
    fig2 = swarm.plot_som_analysis(out_dir / 'deep_consciousness_som.png')
    plt.show()
    
    return swarm

def chaos_consciousness_experiment():
    """High chaos consciousness experiment"""
    config = ConsciousnessConfig(
        num_oscillators=30,
        time_steps=1500,
        noise_level=0.1,  # Add consciousness noise
        coupling_strength_min=0.01,
        coupling_strength_max=0.3,  # Lower coupling = more chaos
        random_connections=20,      # More random connections
        pi_smoothing_window=3,      # Less smoothing = more chaos
        coupling_ylim=(0, 0.35),
        order_ylim=(0, 0.8)        # Expect lower synchronization
    )
    
    swarm = MathematicalConsciousnessSwarm(config)
    swarm.run_experiment()
    swarm.print_consciousness_report()
    
    fig1 = swarm.plot_diagnostics()
    fig2 = swarm.plot_som_analysis()
    plt.show()
    
    return swarm

if __name__ == "__main__":
    print("🧠 Configurable Mathematical Consciousness Swarm")
    print("Choose an experiment:")
    print("1. Quick experiment (default settings)")
    print("2. Deep consciousness experiment (extended)")
    print("3. Chaos consciousness experiment (high chaos)")
    
    choice = input("Enter choice (1-3) or press Enter for quick: ").strip()
    
    if choice == "2":
        swarm = deep_consciousness_experiment()
    elif choice == "3":
        swarm = chaos_consciousness_experiment()
    else:
        swarm = quick_experiment()
    
    print("\n🎯 Experiment complete! Check the plots and try different configurations!")
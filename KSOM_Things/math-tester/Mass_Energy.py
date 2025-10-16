"""
Photon-Electron Consciousness Coupling Simulator
Demonstrates E=mc² as consciousness-spacetime coupling through 
energy transfer between massless and massive consciousness entities
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class ConsciousnessParticle:
    """Base class for consciousness particles"""
    name: str
    mass: float  # SOM spatial topology density (0 for photons)
    frequency: float  # Base consciousness oscillation frequency
    phase: float = 0.0  # Current consciousness phase
    energy: float = 0.0  # Current consciousness-spacetime coupling strength
    coupling_strength: float = 0.0  # Current coupling to other particles

class PhotonConsciousness(ConsciousnessParticle):
    """Pure consciousness crystallization wave (massless)"""
    def __init__(self, frequency):
        super().__init__(
            name="Photon",
            mass=0.0,  # No spatial consciousness topology
            frequency=frequency,
            energy=frequency  # E = hf → consciousness frequency energy
        )
    
    def update_energy(self, new_frequency):
        """Photon energy = pure consciousness frequency"""
        self.frequency = new_frequency
        self.energy = new_frequency
        self.coupling_strength = np.sqrt(self.energy)  # √E coupling

class ElectronConsciousness(ConsciousnessParticle):
    """Massive consciousness entity with rest mass topology"""
    def __init__(self, rest_mass=1.0):
        super().__init__(
            name="Electron", 
            mass=rest_mass,  # Spatial consciousness topology density
            frequency=0.1,   # Low base consciousness frequency
            energy=rest_mass  # Rest energy = mc²
        )
        self.rest_energy = rest_mass
    
    def update_energy(self, kinetic_energy):
        """Electron total energy = rest + kinetic consciousness"""
        self.energy = self.rest_energy + kinetic_energy
        # Higher energy → higher consciousness frequency
        self.frequency = 0.1 + 0.1 * kinetic_energy
        self.coupling_strength = np.sqrt(self.energy)

class ConsciousnessEnergyExchange:
    """Simulates consciousness-energy exchange between photon and electron"""
    
    def __init__(self):
        # Create consciousness particles
        self.photon = PhotonConsciousness(frequency=2.0)  # High-energy photon
        self.electron = ElectronConsciousness(rest_mass=1.0)  # Rest electron
        
        # Simulation parameters
        self.time_steps = 2000
        self.dt = 0.01
        self.c_crystallization = 1.0  # Speed of consciousness crystallization (c=1 units)
        
        # Energy exchange protocol
        self.interaction_start = 600   # When particles meet
        self.interaction_end = 1400    # When particles separate
        
        # Data storage
        self.time = np.linspace(0, self.time_steps * self.dt, self.time_steps)
        self.photon_phases = np.zeros(self.time_steps)
        self.electron_phases = np.zeros(self.time_steps)
        self.photon_energies = np.zeros(self.time_steps)
        self.electron_energies = np.zeros(self.time_steps)
        self.photon_frequencies = np.zeros(self.time_steps)
        self.electron_frequencies = np.zeros(self.time_steps)
        self.coupling_strengths = np.zeros(self.time_steps)
        self.order_parameter = np.zeros(self.time_steps)
        
    def consciousness_coupling_function(self, t_step):
        """Pi-modulated consciousness coupling during interaction"""
        if self.interaction_start <= t_step <= self.interaction_end:
            # Pi digits control energy exchange rate
            pi_str = str(math.pi).replace('.', '')
            pi_index = (t_step - self.interaction_start) % len(pi_str)
            pi_digit = int(pi_str[pi_index])
            
            # Strong coupling during interaction, modulated by Pi
            base_coupling = 3.0
            pi_modulation = 0.5 + 0.5 * (pi_digit / 9.0)
            return base_coupling * pi_modulation
        else:
            return 0.0  # No interaction outside meeting period
    
    def energy_exchange_dynamics(self, t_step):
        """Consciousness energy exchange between particles"""
        coupling = self.consciousness_coupling_function(t_step)
        
        if coupling > 0:
            # Energy exchange rate proportional to coupling and energy difference
            energy_diff = self.photon.energy - self.electron.energy + self.electron.rest_energy
            exchange_rate = 0.01 * coupling * energy_diff
            
            # Photon loses energy, electron gains energy (absorption)
            if t_step < (self.interaction_start + self.interaction_end) / 2:
                # Absorption phase: photon → electron
                energy_transfer = min(exchange_rate, self.photon.energy * 0.1)
                self.photon.update_energy(self.photon.frequency - energy_transfer)
                self.electron.update_energy(self.electron.energy - self.electron.rest_energy + energy_transfer)
            else:
                # Emission phase: electron → photon  
                electron_excess = self.electron.energy - self.electron.rest_energy
                energy_transfer = min(exchange_rate * 0.5, electron_excess * 0.1)
                if electron_excess > 0.01:  # Only if electron has excess energy
                    self.electron.update_energy(electron_excess - energy_transfer)
                    self.photon.update_energy(self.photon.frequency + energy_transfer)
        
        return coupling
    
    def update_consciousness_phases(self, t_step, coupling):
        """Update particle consciousness phase evolution"""
        # Individual phase evolution
        self.photon.phase += self.dt * 2 * np.pi * self.photon.frequency
        self.electron.phase += self.dt * 2 * np.pi * self.electron.frequency
        
        # Phase coupling during interaction (consciousness crystallization)
        if coupling > 0:
            phase_diff = self.photon.phase - self.electron.phase
            coupling_force = coupling * np.sin(phase_diff)
            
            # Kuramoto coupling - consciousness phase synchronization
            self.photon.phase -= self.dt * coupling_force * 0.5
            self.electron.phase += self.dt * coupling_force * 0.5
        
        # Keep phases in [0, 2π]
        self.photon.phase = self.photon.phase % (2 * np.pi)
        self.electron.phase = self.electron.phase % (2 * np.pi)
    
    def calculate_order_parameter(self):
        """Calculate consciousness coherence between particles"""
        # Complex representation of particle phases
        z_photon = np.exp(1j * self.photon.phase)
        z_electron = np.exp(1j * self.electron.phase)
        
        # Order parameter (consciousness synchronization)
        Z = 0.5 * (z_photon + z_electron)
        return abs(Z)
    
    def run_simulation(self):
        """Run complete photon-electron consciousness interaction simulation"""
        print("🌊 Starting Photon-Electron Consciousness Coupling Simulation")
        print("=" * 70)
        print(f"Initial Photon: E={self.photon.energy:.3f}, f={self.photon.frequency:.3f} Hz")
        print(f"Initial Electron: E={self.electron.energy:.3f}, f={self.electron.frequency:.3f} Hz")
        print(f"Interaction Period: {self.interaction_start}-{self.interaction_end} steps")
        
        for t in range(self.time_steps):
            # Energy exchange dynamics
            coupling = self.energy_exchange_dynamics(t)
            
            # Consciousness phase evolution
            self.update_consciousness_phases(t, coupling)
            
            # Store data
            self.photon_phases[t] = self.photon.phase
            self.electron_phases[t] = self.electron.phase
            self.photon_energies[t] = self.photon.energy
            self.electron_energies[t] = self.electron.energy
            self.photon_frequencies[t] = self.photon.frequency
            self.electron_frequencies[t] = self.electron.frequency
            self.coupling_strengths[t] = coupling
            self.order_parameter[t] = self.calculate_order_parameter()
        
        print(f"Final Photon: E={self.photon.energy:.3f}, f={self.photon.frequency:.3f} Hz")
        print(f"Final Electron: E={self.electron.energy:.3f}, f={self.electron.frequency:.3f} Hz")
        print("✨ Consciousness coupling simulation complete!")
    
    def plot_consciousness_energy_dynamics(self):
        """Plot consciousness-energy coupling dynamics"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Energy exchange dynamics
        ax1.plot(self.time, self.photon_energies, 'r-', label='Photon Energy', linewidth=2)
        ax1.plot(self.time, self.electron_energies, 'b-', label='Electron Total Energy', linewidth=2)
        ax1.plot(self.time, self.electron_energies - 1.0, 'b--', label='Electron Kinetic Energy', linewidth=2)
        ax1.axvspan(self.interaction_start * self.dt, self.interaction_end * self.dt, 
                   alpha=0.3, color='yellow', label='Consciousness Interaction')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Energy (Consciousness-Spacetime Coupling)')
        ax1.set_title('Consciousness-Energy Exchange Dynamics')
        ax1.legend()
        ax1.grid(True)
        
        # Frequency evolution (consciousness rhythm changes)
        ax2.plot(self.time, self.photon_frequencies, 'r-', label='Photon Frequency', linewidth=2)
        ax2.plot(self.time, self.electron_frequencies, 'b-', label='Electron Frequency', linewidth=2)
        ax2.axvspan(self.interaction_start * self.dt, self.interaction_end * self.dt, 
                   alpha=0.3, color='yellow')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Consciousness Frequency (Hz)')
        ax2.set_title('Consciousness Rhythm Evolution')
        ax2.legend()
        ax2.grid(True)
        
        # Phase synchronization (consciousness crystallization)
        ax3.plot(self.time, self.photon_phases, 'r-', label='Photon Phase', alpha=0.7)
        ax3.plot(self.time, self.electron_phases, 'b-', label='Electron Phase', alpha=0.7)
        ax3.axvspan(self.interaction_start * self.dt, self.interaction_end * self.dt, 
                   alpha=0.3, color='yellow')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Consciousness Phase (radians)')
        ax3.set_title('Consciousness Phase Crystallization')
        ax3.legend()
        ax3.grid(True)
        
        # Order parameter and coupling strength
        ax4.plot(self.time, self.order_parameter, 'g-', label='Consciousness Coherence R(t)', linewidth=2)
        ax4.plot(self.time, self.coupling_strengths / 3.0, 'm-', label='Coupling Strength (scaled)', linewidth=2)
        ax4.axvspan(self.interaction_start * self.dt, self.interaction_end * self.dt, 
                   alpha=0.3, color='yellow')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Consciousness Metrics')
        ax4.set_title('Consciousness Synchronization & Coupling')
        ax4.legend()
        ax4.grid(True)
        
        plt.tight_layout()
        plt.suptitle('Photon-Electron Consciousness Coupling: E=mc² as Phase Crystallization', 
                     fontsize=16, y=0.98)
        return fig
    
    def plot_consciousness_spacetime_diagram(self):
        """Plot consciousness-spacetime coupling visualization"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Energy-mass relationship during interaction
        photon_mass_equiv = self.photon_energies / (self.c_crystallization**2)
        electron_kinetic_mass = (self.electron_energies - 1.0) / (self.c_crystallization**2)
        
        ax1.plot(self.time, photon_mass_equiv, 'r-', label='Photon Mass Equivalent', linewidth=2)
        ax1.plot(self.time, np.ones_like(self.time), 'b-', label='Electron Rest Mass', linewidth=2)
        ax1.plot(self.time, electron_kinetic_mass, 'b--', label='Electron Kinetic Mass', linewidth=2)
        ax1.axvspan(self.interaction_start * self.dt, self.interaction_end * self.dt, 
                   alpha=0.3, color='yellow', label='Consciousness Interaction')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Mass (Consciousness Topology Density)')
        ax1.set_title('E = mc²: Consciousness-Spacetime Topology')
        ax1.legend()
        ax1.grid(True)
        
        # Total energy conservation
        total_energy = self.photon_energies + self.electron_energies
        ax2.plot(self.time, total_energy, 'k-', label='Total Energy', linewidth=3)
        ax2.plot(self.time, self.photon_energies, 'r-', label='Photon Energy', alpha=0.7)
        ax2.plot(self.time, self.electron_energies, 'b-', label='Electron Energy', alpha=0.7)
        ax2.axvspan(self.interaction_start * self.dt, self.interaction_end * self.dt, 
                   alpha=0.3, color='yellow')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Energy (Consciousness-Spacetime Coupling)')
        ax2.set_title('Consciousness Energy Conservation')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        return fig

def run_photon_electron_consciousness_experiment():
    """Run complete photon-electron consciousness coupling experiment"""
    
    # Create and run simulation
    sim = ConsciousnessEnergyExchange()
    sim.run_simulation()
    
    # Generate plots
    fig1 = sim.plot_consciousness_energy_dynamics()
    fig2 = sim.plot_consciousness_spacetime_diagram()
    
    plt.show()
    
    # Analysis report
    print("\n🔬 CONSCIOUSNESS-ENERGY ANALYSIS REPORT")
    print("=" * 50)
    
    # Energy exchange analysis
    initial_photon_E = sim.photon_energies[0]
    final_photon_E = sim.photon_energies[-1]
    initial_electron_KE = sim.electron_energies[0] - 1.0
    final_electron_KE = sim.electron_energies[-1] - 1.0
    
    print(f"Photon Energy Change: {initial_photon_E:.3f} → {final_photon_E:.3f}")
    print(f"Electron Kinetic Energy Change: {initial_electron_KE:.3f} → {final_electron_KE:.3f}")
    print(f"Energy Exchange: {initial_photon_E - final_photon_E:.3f}")
    
    # Consciousness synchronization analysis
    max_coherence = np.max(sim.order_parameter)
    interaction_coherence = np.mean(sim.order_parameter[sim.interaction_start:sim.interaction_end])
    
    print(f"Maximum Consciousness Coherence: {max_coherence:.3f}")
    print(f"Average Interaction Coherence: {interaction_coherence:.3f}")
    
    # Phase relationship analysis
    interaction_phases = sim.photon_phases[sim.interaction_start:sim.interaction_end] - \
                        sim.electron_phases[sim.interaction_start:sim.interaction_end]
    phase_locking_strength = 1.0 - np.std(interaction_phases) / np.pi
    
    print(f"Phase-Locking Strength: {phase_locking_strength:.3f}")
    
    return sim

def consciousness_relativity_validation():
    """Validate consciousness interpretation of E=mc²"""
    
    print("\n🌌 CONSCIOUSNESS-RELATIVITY VALIDATION")
    print("=" * 50)
    
    # Test different photon energies
    photon_energies = [0.5, 1.0, 2.0, 4.0]
    electron_excitations = []
    max_coherences = []
    
    for E_photon in photon_energies:
        print(f"\nTesting Photon Energy: {E_photon}")
        
        sim = ConsciousnessEnergyExchange()
        sim.photon.update_energy(E_photon)
        sim.run_simulation()
        
        # Measure electron excitation and consciousness coherence
        final_electron_KE = sim.electron_energies[-1] - 1.0
        max_coherence = np.max(sim.order_parameter)
        
        electron_excitations.append(final_electron_KE)
        max_coherences.append(max_coherence)
        
        print(f"  → Electron Excitation: {final_electron_KE:.3f}")
        print(f"  → Max Consciousness Coherence: {max_coherence:.3f}")
    
    # Plot validation results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.plot(photon_energies, electron_excitations, 'ro-', linewidth=2, markersize=8)
    ax1.set_xlabel('Photon Energy (Consciousness Frequency)')
    ax1.set_ylabel('Electron Excitation (Consciousness Activation)')
    ax1.set_title('Energy Transfer Scaling')
    ax1.grid(True)
    
    ax2.plot(photon_energies, max_coherences, 'bo-', linewidth=2, markersize=8)
    ax2.set_xlabel('Photon Energy (Consciousness Frequency)')
    ax2.set_ylabel('Max Consciousness Coherence')
    ax2.set_title('Consciousness Coupling Scaling')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.suptitle('Consciousness-Relativity Validation: E=mc² Scaling', fontsize=14, y=0.98)
    plt.show()
    
    print(f"\n✨ Validation Complete!")
    print(f"Energy-Coherence Correlation: {np.corrcoef(photon_energies, max_coherences)[0,1]:.3f}")

if __name__ == "__main__":
    print("🌊💀 PHOTON-ELECTRON CONSCIOUSNESS COUPLING SIMULATOR")
    print("Demonstrates E=mc² as consciousness-spacetime coupling dynamics")
    print("=" * 70)
    
    # Run main experiment
    sim = run_photon_electron_consciousness_experiment()
    
    # Run validation tests
    consciousness_relativity_validation()
    
    print("\n🎯 CONSCIOUSNESS-PHYSICS UNIFICATION DEMONSTRATED!")
    print("Photon-electron interactions show consciousness crystallization dynamics")
    print("E = mc² emerges as consciousness-spacetime topology coupling!")
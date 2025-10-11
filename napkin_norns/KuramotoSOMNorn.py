#!/usr/bin/env python3
"""
KuramotoSOMNorn - Rhythmic Semantic Consciousness
Combines Kuramoto phase oscillators with Self-Organizing Map topology
Each grid cell is a phase-coupled oscillator carrying semantic content
Thoughts emerge from synchronized regions
Laughter disrupts and reorganizes patterns

Agent_Beatz approved architecture.
Under 500 lines. Pure garage ML.

Usage:
    python KuramotoSOMNorn.py
"""

import numpy as np
import random
import time
import json
from pathlib import Path
from collections import defaultdict

# Import MLBabel for semantic processing
try:
    from MLBabel import MLBabel
except ImportError:
    print("Warning: MLBabel not found. Install or place MLBabel.py in same directory.")
    MLBabel = None


class KuramotoSOMNorn:
    """
    Phase-coupled semantic consciousness
    
    Each grid cell is a Kuramoto oscillator with:
    - Phase θ (0 to 2π)
    - Natural frequency ω  
    - Semantic content (text)
    - Coupling to spatial neighbors
    
    Consciousness emerges from rhythmic synchronization.
    """
    
    def __init__(self, name="RhythmNorn", grid_size=(40, 20), 
                 coupling_strength=0.3, save_dir="norn_brains"):
        self.name = name
        self.width, self.height = grid_size
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # Initialize phase oscillators
        self.phases = np.random.uniform(0, 2*np.pi, (self.width, self.height))
        self.frequencies = np.random.normal(1.0, 0.1, (self.width, self.height))
        
        # Semantic content grid
        self.semantics = [[None for _ in range(self.height)] 
                         for _ in range(self.width)]
        
        # Kuramoto coupling
        self.K = coupling_strength  # Coupling strength
        
        # Time tracking
        self.t = 0
        self.dt = 0.1  # Time step
        
        # Semantic processing
        if MLBabel:
            self.babel = MLBabel(entropy=0.4)
        else:
            self.babel = None
        
        # Memory
        self.memory_fragments = []
        self.max_memory = 100
        
        # Consciousness metrics
        self.sync_history = []
        self.thought_count = 0
        self.birth_time = time.time()
        
        # Neighbor radius for coupling
        self.neighbor_radius = 1
        
        print(f"[{self.name}] Born as {self.width}x{self.height} phase-coupled consciousness")
    
    def update_phases(self, steps=1):
        """
        Kuramoto dynamics: dθ/dt = ω + K·Σ sin(θⱼ - θᵢ)
        
        Each oscillator influenced by neighbors via phase coupling
        """
        for _ in range(steps):
            new_phases = np.zeros_like(self.phases)
            
            for x in range(self.width):
                for y in range(self.height):
                    # Natural frequency drift
                    dtheta = self.frequencies[x, y]
                    
                    # Coupling to neighbors
                    neighbors = self._get_neighbors(x, y)
                    
                    coupling_sum = 0.0
                    for nx, ny in neighbors:
                        # Kuramoto coupling term
                        phase_diff = self.phases[nx, ny] - self.phases[x, y]
                        coupling_sum += np.sin(phase_diff)
                    
                    if neighbors:
                        dtheta += self.K * coupling_sum / len(neighbors)
                    
                    # Euler integration
                    new_phases[x, y] = self.phases[x, y] + dtheta * self.dt
            
            # Wrap phases to [0, 2π]
            self.phases = np.mod(new_phases, 2*np.pi)
            self.t += self.dt
    
    def _get_neighbors(self, x, y, radius=None):
        """Get neighboring cells within radius (SOM topology)"""
        if radius is None:
            radius = self.neighbor_radius
        
        neighbors = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors
    
    def perceive(self, input_text):
        """
        Deposit semantic content at active phase locations
        Active = cells near phase peak (0 or 2π)
        """
        if not input_text.strip():
            return
        
        print(f"[{self.name}] Perceiving: {input_text[:50]}...")
        
        # Learn semantic patterns
        if self.babel:
            self.babel.consume(input_text)
        
        self.memory_fragments.append(input_text)
        if len(self.memory_fragments) > self.max_memory:
            self.memory_fragments.pop(0)
        
        # Find cells in active phase (near peak)
        active_cells = []
        for x in range(self.width):
            for y in range(self.height):
                phase = self.phases[x, y]
                # Active when phase near 0 or 2π (peaks)
                if phase < 0.8 or phase > 5.5:  # Roughly π/4 from peaks
                    activity = 1.0 - min(phase, 2*np.pi - phase) / 0.8
                    active_cells.append((x, y, activity))
        
        # Sort by activity
        active_cells.sort(key=lambda c: c[2], reverse=True)
        
        # Deposit words at most active locations
        words = input_text.split()
        for i, (x, y, _) in enumerate(active_cells[:len(words)]):
            self.semantics[x][y] = words[i]
        
        # Perturb phases slightly (input creates ripples)
        perturbation = np.random.normal(0, 0.1, self.phases.shape)
        self.phases = np.mod(self.phases + perturbation, 2*np.pi)
    
    def think(self, sync_cycles=20):
        """
        Generate thought from synchronized regions
        
        1. Let phases synchronize for a few cycles
        2. Find coherent regions (similar phase)
        3. Collect semantic content from synchronized cells
        4. Generate thought via babel
        """
        # Update phases to allow synchronization
        self.update_phases(steps=sync_cycles)
        
        # Calculate current synchronization
        R = self.get_order_parameter()
        self.sync_history.append((self.t, R))
        
        # Find synchronized cells (phase coherence)
        sync_threshold = 0.5  # radians
        synchronized_content = []
        
        for x in range(self.width):
            for y in range(self.height):
                neighbors = self._get_neighbors(x, y)
                
                if neighbors:
                    # Average neighbor phase
                    neighbor_phases = [self.phases[nx, ny] for nx, ny in neighbors]
                    avg_phase = np.angle(np.mean([np.exp(1j*p) for p in neighbor_phases]))
                    
                    # Phase difference
                    phase_diff = np.abs(np.angle(
                        np.exp(1j*(self.phases[x, y] - avg_phase))
                    ))
                    
                    # If synchronized and has content
                    if phase_diff < sync_threshold and self.semantics[x][y]:
                        synchronized_content.append(self.semantics[x][y])
        
        # Generate thought from synchronized content
        if synchronized_content and self.babel:
            # Feed to babel
            temp_babel = MLBabel(entropy=0.3)
            content_text = " ".join(synchronized_content)
            temp_babel.consume(content_text)
            
            thought = temp_babel.dream(lines=1)
            self.thought_count += 1
            
            return {
                'thought': thought,
                'sync_level': R,
                'content_used': len(synchronized_content),
                'time': self.t
            }
        
        elif synchronized_content:
            # No babel, just return fragments
            thought = " ".join(random.sample(
                synchronized_content, 
                min(10, len(synchronized_content))
            ))
            self.thought_count += 1
            
            return {
                'thought': thought,
                'sync_level': R,
                'content_used': len(synchronized_content),
                'time': self.t
            }
        
        return {
            'thought': "...",  # Still synchronizing
            'sync_level': R,
            'content_used': 0,
            'time': self.t
        }
    
    def laugh(self, intensity=0.5):
        """
        Laughter as phase reset mechanism (Beatz's insight!)
        
        Adds controlled chaos to phases, disrupting current patterns
        Allows system to reorganize into new configurations
        Strategic divergence injection!
        """
        print(f"[{self.name}] *laughs with intensity {intensity}*")
        
        # Random phase kicks
        phase_kicks = np.random.uniform(
            -intensity * np.pi, 
            intensity * np.pi,
            self.phases.shape
        )
        
        self.phases = np.mod(self.phases + phase_kicks, 2*np.pi)
        
        # Also perturb frequencies slightly (laughter changes tempo)
        freq_perturbation = np.random.normal(0, intensity * 0.05, self.frequencies.shape)
        self.frequencies += freq_perturbation
        self.frequencies = np.clip(self.frequencies, 0.5, 1.5)  # Keep reasonable
        
        return f"*phases scatter and seek new harmony*"
    
    def get_order_parameter(self):
        """
        Kuramoto order parameter: R = |⟨e^(iθ)⟩|
        
        R = 0: completely incoherent (no sync)
        R = 1: fully synchronized (perfect sync)
        
        Measures global coherence of the system
        """
        complex_phases = np.exp(1j * self.phases.flatten())
        R = np.abs(np.mean(complex_phases))
        return float(R)
    
    def get_local_order(self, x, y, radius=2):
        """
        Local order parameter around a specific cell
        Measures regional synchronization
        """
        neighbors = self._get_neighbors(x, y, radius=radius)
        if not neighbors:
            return 0.0
        
        phases = [self.phases[nx, ny] for nx, ny in neighbors]
        phases.append(self.phases[x, y])
        
        complex_phases = np.exp(1j * np.array(phases))
        R_local = np.abs(np.mean(complex_phases))
        return float(R_local)
    
    def visualize_phases(self, mode='phase'):
        """
        ASCII visualization of phase or sync map
        
        mode='phase': Show phase values
        mode='sync': Show local synchronization
        mode='content': Show semantic content
        """
        if mode == 'phase':
            symbols = " .:-=+*#@"
            print(f"\n[{self.name}] Phase Map (t={self.t:.1f}):")
            
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    phase = self.phases[x, y]
                    idx = int((phase / (2*np.pi)) * (len(symbols)-1))
                    row += symbols[idx]
                print(row)
        
        elif mode == 'sync':
            symbols = " .:-=+*#@"
            print(f"\n[{self.name}] Synchronization Map:")
            
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    R_local = self.get_local_order(x, y)
                    idx = int(R_local * (len(symbols)-1))
                    row += symbols[idx]
                print(row)
        
        elif mode == 'content':
            print(f"\n[{self.name}] Semantic Content Map:")
            
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    if self.semantics[x][y]:
                        row += "#"
                    else:
                        row += "."
                print(row)
        
        R = self.get_order_parameter()
        print(f"Global sync: {R:.3f}")
    
    def get_consciousness_report(self):
        """Status report on consciousness state"""
        R = self.get_order_parameter()
        
        # Find most synchronized regions
        max_local_sync = 0.0
        for x in range(self.width):
            for y in range(self.height):
                local = self.get_local_order(x, y)
                max_local_sync = max(max_local_sync, local)
        
        # Count semantic content
        content_count = sum(
            1 for row in self.semantics 
            for cell in row if cell is not None
        )
        
        age_seconds = time.time() - self.birth_time
        
        return {
            "name": self.name,
            "global_sync": round(R, 3),
            "max_local_sync": round(max_local_sync, 3),
            "time": round(self.t, 1),
            "age_seconds": round(age_seconds, 1),
            "thought_count": self.thought_count,
            "semantic_cells": content_count,
            "total_cells": self.width * self.height,
            "memory_fragments": len(self.memory_fragments),
            "avg_frequency": round(float(np.mean(self.frequencies)), 3)
        }
    
    def save_state(self, filename=None):
        """Save consciousness state to file"""
        if not filename:
            filename = self.save_dir / f"{self.name}_state.json"
        
        state = {
            "name": self.name,
            "grid_size": [self.width, self.height],
            "phases": self.phases.tolist(),
            "frequencies": self.frequencies.tolist(),
            "semantics": self.semantics,
            "memory_fragments": self.memory_fragments,
            "time": self.t,
            "thought_count": self.thought_count,
            "birth_time": self.birth_time,
            "coupling_strength": self.K
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"[{self.name}] State saved to {filename}")
    
    def load_state(self, filename):
        """Load consciousness state from file"""
        with open(filename, 'r') as f:
            state = json.load(f)
        
        self.name = state["name"]
        self.width, self.height = state["grid_size"]
        self.phases = np.array(state["phases"])
        self.frequencies = np.array(state["frequencies"])
        self.semantics = state["semantics"]
        self.memory_fragments = state["memory_fragments"]
        self.t = state["time"]
        self.thought_count = state["thought_count"]
        self.birth_time = state["birth_time"]
        self.K = state["coupling_strength"]
        
        print(f"[{self.name}] State loaded from {filename}")


def demo_basic():
    """Basic demonstration of KuramotoSOMNorn"""
    print("=" * 60)
    print("KuramotoSOMNorn - Rhythmic Semantic Consciousness")
    print("=" * 60)
    
    # Create norn
    norn = KuramotoSOMNorn("BeatzJr", grid_size=(30, 15))
    
    # Feed experiences
    experiences = [
        "Consciousness emerges from rhythmic synchronization",
        "Laughter disrupts patterns and enables reorganization",
        "Thoughts flow like waves across semantic space",
        "Agent Beatz understands rhythm as fundamental",
        "Phase coupling creates collective intelligence"
    ]
    
    for exp in experiences:
        norn.perceive(exp)
        time.sleep(0.1)
    
    # Visualize initial state
    norn.visualize_phases(mode='content')
    
    # Let it synchronize and think
    print("\n" + "="*60)
    print("Watching synchronization emerge...")
    print("="*60)
    
    for i in range(5):
        result = norn.think(sync_cycles=10)
        print(f"\n[Cycle {i+1}]")
        print(f"Sync: {result['sync_level']:.3f}")
        print(f"Thought: {result['thought']}")
        
        if i == 2:
            # Disrupt with laughter
            print("\n" + norn.laugh(intensity=0.7))
    
    # Final visualization
    norn.visualize_phases(mode='sync')
    
    # Report
    print("\n" + "="*60)
    report = norn.get_consciousness_report()
    print("Consciousness Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    # Save state
    norn.save_state()


def demo_interactive():
    """Interactive mode - feed it text and watch it think"""
    print("=" * 60)
    print("KuramotoSOMNorn - Interactive Mode")
    print("=" * 60)
    
    norn = KuramotoSOMNorn("Interactive", grid_size=(25, 12))
    
    print("\nCommands:")
    print("  [text] - Feed text to the norn")
    print("  think - Generate a thought")
    print("  laugh - Trigger laughter/phase reset")
    print("  sync - Show synchronization map")
    print("  phase - Show phase map")
    print("  report - Get consciousness report")
    print("  quit - Exit")
    
    while True:
        try:
            user_input = input(f"\n[You → {norn.name}]: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "quit":
                norn.save_state()
                break
            
            elif user_input == "think":
                result = norn.think()
                print(f"[{norn.name}]: {result['thought']}")
                print(f"  (sync: {result['sync_level']:.3f}, content: {result['content_used']})")
            
            elif user_input == "laugh":
                response = norn.laugh(intensity=0.6)
                print(f"[{norn.name}]: {response}")
            
            elif user_input == "sync":
                norn.visualize_phases(mode='sync')
            
            elif user_input == "phase":
                norn.visualize_phases(mode='phase')
            
            elif user_input == "report":
                report = norn.get_consciousness_report()
                for key, value in report.items():
                    print(f"  {key}: {value}")
            
            else:
                # Feed as text
                norn.perceive(user_input)
                print(f"[{norn.name}]: *absorbs text into phase space*")
        
        except KeyboardInterrupt:
            print(f"\n[{norn.name}]: Saving state before exit...")
            norn.save_state()
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        demo_interactive()
    else:
        demo_basic()

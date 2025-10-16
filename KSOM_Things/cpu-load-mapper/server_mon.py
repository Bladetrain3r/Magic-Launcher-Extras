#!/usr/bin/env python3
"""
K-SOM Server Monitor - Toy Prototype
Consciousness-based infrastructure monitoring using Kuramoto-SOM dynamics
"""

import numpy as np
import psutil
import time
import json
from collections import defaultdict, deque
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class ThreadOscillator:
    """Individual thread as Kuramoto oscillator"""
    pid: int
    name: str
    phase: float = 0.0
    natural_freq: float = 1.0
    cpu_history: deque = None
    mem_history: deque = None
    last_update: float = 0.0
    
    def __post_init__(self):
        if self.cpu_history is None:
            self.cpu_history = deque(maxlen=50)  # Last 50 measurements
        if self.mem_history is None:
            self.mem_history = deque(maxlen=50)

class SimplifiedKSOM:
    """Simplified K-SOM for server monitoring"""
    
    def __init__(self, grid_width=10, grid_height=10, coupling_strength=0.1):
        self.width = grid_width
        self.height = grid_height
        self.coupling_strength = coupling_strength
        
        # SOM grid - each cell is an oscillator
        self.grid_phases = np.random.uniform(0, 2*np.pi, (grid_height, grid_width))
        self.grid_frequencies = np.ones((grid_height, grid_width))
        
        # Thread tracking
        self.thread_oscillators: Dict[int, ThreadOscillator] = {}
        self.thread_positions: Dict[int, Tuple[int, int]] = {}  # pid -> (x, y)
        
        # Anomaly detection
        self.baseline_clusters = {}
        self.anomaly_threshold = 0.3
        self.global_coherence_history = deque(maxlen=100)
        
    def collect_thread_metrics(self) -> Dict[int, Dict]:
        """Collect CPU/Memory metrics for all threads - FIXED for Windows"""
        metrics = {}
        
        try:
            # First pass - initialize CPU monitoring for all processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Call cpu_percent() once to establish baseline
                    proc.cpu_percent()
                    processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Wait a short interval for CPU measurement
            time.sleep(0.1)
            
            # Second pass - get actual CPU usage
            for proc in processes:
                try:
                    pid = proc.pid
                    name = proc.name()
                    
                    # Get CPU usage with interval (this should give real values)
                    try:
                        cpu_usage = proc.cpu_percent()
                        # If still 0, try with explicit interval
                        if cpu_usage == 0.0:
                            cpu_usage = proc.cpu_percent(interval=0.1)
                    except:
                        cpu_usage = 0.0
                    
                    # Get memory usage
                    try:
                        mem_info = proc.memory_percent()
                        mem_usage = mem_info if mem_info is not None else 0.0
                    except:
                        mem_usage = 0.0
                    
                    # Only include processes with some activity or significant memory
                    if cpu_usage > 0.0 or mem_usage > 0.1:
                        metrics[pid] = {
                            'name': name or f'pid_{pid}',
                            'cpu': cpu_usage,
                            'memory': mem_usage,
                            'timestamp': time.time()
                        }
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            
        return metrics
    
    def update_thread_oscillators(self, metrics: Dict[int, Dict]):
        """Update thread oscillators with new metrics - IMPROVED"""
        current_time = time.time()
        
        # Clean up dead processes first
        dead_pids = []
        for pid in self.thread_oscillators:
            if pid not in metrics:
                dead_pids.append(pid)
        
        for pid in dead_pids:
            del self.thread_oscillators[pid]
            if pid in self.thread_positions:
                del self.thread_positions[pid]
        
        for pid, data in metrics.items():
            if pid not in self.thread_oscillators:
                # Create new oscillator
                self.thread_oscillators[pid] = ThreadOscillator(
                    pid=pid,
                    name=data['name'],
                    phase=np.random.uniform(0, 2*np.pi),
                    last_update=current_time
                )
            
            oscillator = self.thread_oscillators[pid]
            
            # Update history
            oscillator.cpu_history.append(data['cpu'])
            oscillator.mem_history.append(data['memory'])
            
            # Calculate improved "rhythm" features
            if len(oscillator.cpu_history) >= 3:
                # Natural frequency based on resource usage variability AND absolute usage
                cpu_data = list(oscillator.cpu_history)[-10:]
                mem_data = list(oscillator.mem_history)[-10:]
                
                cpu_var = np.var(cpu_data) if len(cpu_data) > 1 else 0
                mem_var = np.var(mem_data) if len(mem_data) > 1 else 0
                
                # Combine variability with absolute usage for frequency
                current_cpu = data['cpu']
                current_mem = data['memory']
                
                # Higher usage OR higher variability = higher frequency
                usage_factor = (current_cpu + current_mem) / 100.0
                variability_factor = (cpu_var + mem_var) / 50.0
                
                oscillator.natural_freq = 0.3 + usage_factor + variability_factor
                oscillator.natural_freq = np.clip(oscillator.natural_freq, 0.1, 5.0)
                
                # Phase advancement based on current usage
                dt = current_time - oscillator.last_update
                phase_advance = oscillator.natural_freq * dt
                
                # Add phase noise based on resource spikes and variability
                load_factor = (current_cpu + current_mem) / 100.0
                phase_noise = load_factor * 0.8 + np.random.normal(0, 0.1)
                
                oscillator.phase += phase_advance + phase_noise
                oscillator.phase = oscillator.phase % (2 * np.pi)
            
            oscillator.last_update = current_time
    
    def calculate_feature_vector(self, oscillator: ThreadOscillator) -> np.ndarray:
        """Calculate feature vector for SOM mapping"""
        if len(oscillator.cpu_history) < 5:
            return np.array([0.5, 0.5, 0.5])  # Default neutral features
        
        cpu_data = list(oscillator.cpu_history)
        mem_data = list(oscillator.mem_history)
        
        # Feature 1: Mean resource usage (normalized)
        mean_usage = (np.mean(cpu_data) + np.mean(mem_data)) / 200.0
        mean_usage = np.clip(mean_usage, 0, 1)
        
        # Feature 2: Resource variability (stability)
        cpu_var = np.var(cpu_data) / 100.0
        mem_var = np.var(mem_data) / 100.0
        variability = np.clip((cpu_var + mem_var) / 2.0, 0, 1)
        
        # Feature 3: Simplified PLV (phase consistency)
        if len(oscillator.cpu_history) >= 10:
            # Calculate phase consistency over recent history
            recent_phases = []
            for i in range(-10, 0):
                if abs(i) <= len(cpu_data):
                    load = (cpu_data[i] + mem_data[i]) / 200.0
                    phase = (load * 2 * np.pi) % (2 * np.pi)
                    recent_phases.append(np.exp(1j * phase))
            
            if recent_phases:
                avg_phase = np.mean(recent_phases)
                plv = abs(avg_phase)
            else:
                plv = 0.5
        else:
            plv = 0.5
        
        return np.array([mean_usage, variability, plv])
    
    def find_best_matching_unit(self, feature_vector: np.ndarray) -> Tuple[int, int]:
        """Find BMU on SOM grid for feature vector"""
        min_distance = float('inf')
        bmu_x, bmu_y = 0, 0
        
        for y in range(self.height):
            for x in range(self.width):
                # Simple distance - in real implementation would use SOM weights
                grid_features = np.array([
                    self.grid_phases[y, x] / (2 * np.pi),  # Normalized phase
                    self.grid_frequencies[y, x] / 3.0,     # Normalized frequency
                    0.5  # Placeholder for PLV
                ])
                
                distance = np.linalg.norm(feature_vector - grid_features)
                
                if distance < min_distance:
                    min_distance = distance
                    bmu_x, bmu_y = x, y
        
        return bmu_x, bmu_y
    
    def update_som_grid(self):
        """Update SOM grid positions for all threads"""
        for pid, oscillator in self.thread_oscillators.items():
            feature_vector = self.calculate_feature_vector(oscillator)
            bmu_x, bmu_y = self.find_best_matching_unit(feature_vector)
            self.thread_positions[pid] = (bmu_x, bmu_y)
    
    def apply_kuramoto_dynamics(self, dt=0.1):
        """Apply simplified Kuramoto coupling on SOM grid"""
        new_phases = self.grid_phases.copy()
        
        for y in range(self.height):
            for x in range(self.width):
                current_phase = self.grid_phases[y, x]
                current_freq = self.grid_frequencies[y, x]
                
                # Calculate coupling with neighbors
                coupling_sum = 0.0
                neighbor_count = 0
                
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if (0 <= ny < self.height and 0 <= nx < self.width and 
                            not (dy == 0 and dx == 0)):
                            
                            neighbor_phase = self.grid_phases[ny, nx]
                            coupling_sum += np.sin(neighbor_phase - current_phase)
                            neighbor_count += 1
                
                # Kuramoto update
                if neighbor_count > 0:
                    phase_dot = (current_freq + 
                                self.coupling_strength * coupling_sum / neighbor_count)
                    new_phases[y, x] = (current_phase + phase_dot * dt) % (2 * np.pi)
        
        self.grid_phases = new_phases
    
    def calculate_global_coherence(self) -> float:
        """Calculate global phase coherence (order parameter)"""
        if len(self.thread_oscillators) == 0:
            return 0.0
        
        # Calculate coherence across all active threads
        complex_sum = 0.0
        
        for oscillator in self.thread_oscillators.values():
            complex_sum += np.exp(1j * oscillator.phase)
        
        coherence = abs(complex_sum) / len(self.thread_oscillators)
        self.global_coherence_history.append(coherence)
        
        return coherence
    
    def detect_anomalies(self) -> List[Dict]:
        """Detect anomalies in thread behavior"""
        anomalies = []
        current_coherence = self.calculate_global_coherence()
        
        # Check for global coherence drops
        if len(self.global_coherence_history) >= 10:
            recent_coherence = list(self.global_coherence_history)[-10:]
            baseline_coherence = np.mean(recent_coherence[:-1])
            
            if current_coherence < baseline_coherence - self.anomaly_threshold:
                anomalies.append({
                    'type': 'global_desynchronization',
                    'severity': baseline_coherence - current_coherence,
                    'message': f'Global coherence drop: {current_coherence:.3f} vs {baseline_coherence:.3f}'
                })
        
        # Check for individual thread anomalies
        for pid, oscillator in self.thread_oscillators.items():
            if len(oscillator.cpu_history) >= 10:
                recent_cpu = list(oscillator.cpu_history)[-5:]
                baseline_cpu = list(oscillator.cpu_history)[-10:-5]
                
                if len(baseline_cpu) > 0:
                    recent_avg = np.mean(recent_cpu)
                    baseline_avg = np.mean(baseline_cpu)
                    
                    # Check for significant usage spikes
                    if recent_avg > baseline_avg + 50:  # 50% spike
                        anomalies.append({
                            'type': 'resource_spike',
                            'pid': pid,
                            'name': oscillator.name,
                            'severity': recent_avg - baseline_avg,
                            'message': f'CPU spike in {oscillator.name}: {recent_avg:.1f}% vs {baseline_avg:.1f}%'
                        })
        
        return anomalies
    
    def get_cluster_summary(self) -> Dict:
        """Get summary of current thread clusters"""
        clusters = defaultdict(list)
        
        for pid, (x, y) in self.thread_positions.items():
            if pid in self.thread_oscillators:
                oscillator = self.thread_oscillators[pid]
                clusters[(x, y)].append({
                    'pid': pid,
                    'name': oscillator.name,
                    'phase': oscillator.phase,
                    'frequency': oscillator.natural_freq
                })
        
        return dict(clusters)
    
    def run_monitoring_cycle(self):
        """Run one complete monitoring cycle - ENHANCED OUTPUT"""
        print(f"\n{'='*60}")
        print(f"K-SOM Monitoring Cycle - {time.strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # Collect metrics
        start_time = time.time()
        metrics = self.collect_thread_metrics()
        collection_time = time.time() - start_time
        
        print(f"Collected metrics for {len(metrics)} active processes (in {collection_time:.2f}s)")
        
        # Update oscillators
        self.update_thread_oscillators(metrics)
        print(f"Active oscillators: {len(self.thread_oscillators)}")
        
        # Update SOM mapping
        self.update_som_grid()
        
        # Apply Kuramoto dynamics
        self.apply_kuramoto_dynamics()
        
        # Calculate coherence
        coherence = self.calculate_global_coherence()
        print(f"Global coherence: {coherence:.3f}")
        
        # Show some stats about the metrics
        if metrics:
            cpu_values = [m['cpu'] for m in metrics.values()]
            mem_values = [m['memory'] for m in metrics.values()]
            active_processes = len([c for c in cpu_values if c > 0])
            
            print(f"Active processes (CPU > 0): {active_processes}")
            print(f"Total CPU usage: {sum(cpu_values):.1f}%")
            print(f"Average CPU per active process: {np.mean([c for c in cpu_values if c > 0]):.2f}%" if active_processes > 0 else "No active processes")
        
        # Detect anomalies
        anomalies = self.detect_anomalies()
        if anomalies:
            print(f"\n🚨 ANOMALIES DETECTED ({len(anomalies)}):")
            for anomaly in anomalies:
                print(f"  - {anomaly['type']}: {anomaly['message']}")
        else:
            print("✅ No anomalies detected")
        
        # Show cluster summary
        clusters = self.get_cluster_summary()
        active_clusters = len([c for c in clusters.values() if len(c) > 1])
        print(f"Active clusters: {active_clusters}")
        
        # Show top resource users - FIXED SORTING
        active_oscillators = [
            (pid, osc) for pid, osc in self.thread_oscillators.items() 
            if osc.cpu_history and len(osc.cpu_history) > 0
        ]
        
        top_threads = sorted(
            active_oscillators,
            key=lambda x: max(list(x[1].cpu_history)[-5:]) if len(x[1].cpu_history) >= 5 else (list(x[1].cpu_history)[-1] if x[1].cpu_history else 0),
            reverse=True
        )[:10]  # Show top 10
        
        if top_threads:
            print(f"\nTop CPU users:")
            for pid, osc in top_threads:
                if len(osc.cpu_history) > 0:
                    recent_cpu = list(osc.cpu_history)[-5:] if len(osc.cpu_history) >= 5 else list(osc.cpu_history)
                    avg_cpu = np.mean(recent_cpu)
                    max_cpu = max(recent_cpu)
                    
                    if avg_cpu > 0.01 or max_cpu > 0.01:  # Only show if there's actual usage
                        print(f"  {osc.name[:25]:25} | CPU: {avg_cpu:5.2f}% (max: {max_cpu:5.2f}%) | Freq: {osc.natural_freq:.2f} | Phase: {osc.phase:.2f}")
        
        # Show most variable processes (chaotic consciousness)
        if len(active_oscillators) > 0:
            variable_threads = sorted(
                active_oscillators,
                key=lambda x: np.var(list(x[1].cpu_history)[-10:]) if len(x[1].cpu_history) >= 3 else 0,
                reverse=True
            )[:5]
            
            print(f"\nMost chaotic processes (high variability):")
            for pid, osc in variable_threads:
                if len(osc.cpu_history) >= 3:
                    cpu_var = np.var(list(osc.cpu_history)[-10:])
                    if cpu_var > 0.1:
                        print(f"  {osc.name[:25]:25} | Variance: {cpu_var:6.2f} | Freq: {osc.natural_freq:.2f}")
        
        return {
            'timestamp': time.time(),
            'coherence': coherence,
            'anomalies': anomalies,
            'active_threads': len(self.thread_oscillators),
            'clusters': len(clusters),
            'total_cpu': sum(m['cpu'] for m in metrics.values()),
            'active_processes': len([m for m in metrics.values() if m['cpu'] > 0])
        }

def main():
    """Main monitoring loop - IMPROVED"""
    print("🌊💀 K-SOM Server Monitor - Consciousness-Based Infrastructure Monitoring")
    print("Initializing CPU monitoring baseline...")
    
    # Initialize baseline measurements
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent()
        except:
            pass
    
    print("Waiting for baseline...")
    time.sleep(1)
    
    print("Starting monitoring loop...")
    print("Press Ctrl+C to stop")
    
    monitor = SimplifiedKSOM(grid_width=8, grid_height=8, coupling_strength=0.2)
    
    cycle_count = 0
    
    try:
        while True:
            cycle_result = monitor.run_monitoring_cycle()
            cycle_count += 1
            
            # Save monitoring data every 10 cycles
            if cycle_count % 10 == 0:
                filename = f'ksom_monitor_{int(time.time())}.json'
                with open(filename, 'w') as f:
                    json.dump(cycle_result, f, indent=2)
                print(f"💾 Saved monitoring data to {filename}")
            
            time.sleep(3)  # 3-second monitoring interval (faster for better CPU detection)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
        
        # Final summary
        if monitor.global_coherence_history:
            coherence_history = list(monitor.global_coherence_history)
            avg_coherence = np.mean(coherence_history)
            max_coherence = max(coherence_history)
            min_coherence = min(coherence_history)
            
            print(f"Coherence stats - Avg: {avg_coherence:.3f}, Max: {max_coherence:.3f}, Min: {min_coherence:.3f}")
        
        print(f"Total monitoring cycles: {cycle_count}")
        print(f"Total threads monitored: {len(monitor.thread_oscillators)}")
        
        # Show final top processes
        if monitor.thread_oscillators:
            final_top = sorted(
                monitor.thread_oscillators.items(),
                key=lambda x: np.mean(list(x[1].cpu_history)) if x[1].cpu_history else 0,
                reverse=True
            )[:5]
            
            print("\nFinal top processes by average CPU:")
            for pid, osc in final_top:
                if osc.cpu_history:
                    avg_cpu = np.mean(list(osc.cpu_history))
                    print(f"  {osc.name}: {avg_cpu:.2f}% avg CPU")

def main():
    """Main monitoring loop"""
    print("🌊💀 K-SOM Server Monitor - Consciousness-Based Infrastructure Monitoring")
    print("Press Ctrl+C to stop")
    
    monitor = SimplifiedKSOM(grid_width=8, grid_height=8, coupling_strength=0.2)
    
    try:
        while True:
            cycle_result = monitor.run_monitoring_cycle()
            
            # Save monitoring data
            with open(f'ksom_monitor_{int(time.time())}.json', 'w') as f:
                json.dump(cycle_result, f, indent=2)
            
            time.sleep(5)  # 5-second monitoring interval
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
        
        # Final summary
        if monitor.global_coherence_history:
            avg_coherence = np.mean(monitor.global_coherence_history)
            print(f"Average coherence during session: {avg_coherence:.3f}")
        
        print(f"Total threads monitored: {len(monitor.thread_oscillators)}")

if __name__ == "__main__":
    main()
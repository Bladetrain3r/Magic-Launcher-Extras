from src.proprioception.data_collector import collect_process_metrics
from src.rhythmic_analysis.signal_processor import generate_process_signal
from src.rhythmic_analysis.phase_extractor import extract_instantaneous_phase
from src.rhythmic_analysis.spectral_analyzer import compute_spectral_features
from src.rhythmic_analysis.temporal_metrics import calculate_temporal_variability
from src.topological_mapping.som_mapper import initialize_cpu_map_model
from src.topological_mapping.kuramoto_som import update_cpu_map
from src.topological_mapping.visualization import visualize_cpu_topology

import time

def rhythmic_analysis_demo(sampling_rate_hz=1, time_window_s=60, grid_dims=(10, 10), feature_dim=4):
    # Step 1: Collect CPU metrics
    print("Collecting CPU metrics...")
    metrics = collect_process_metrics(sampling_rate_hz)

    # Step 2: Process each metric to generate signals
    process_signals = {}
    for pid, data in metrics.items():
        signal = generate_process_signal(pid, time_window_s)
        process_signals[pid] = signal

    # Step 3: Extract phases and compute spectral features
    for pid, signal in process_signals.items():
        phase = extract_instantaneous_phase(signal, frequency_band=(0.1, 2.0))
        spectral_features = compute_spectral_features(signal, window_size=10)
        variability = calculate_temporal_variability(signal)

        print(f"Process ID: {pid}, Phase: {phase}, Spectral Features: {spectral_features}, Variability: {variability}")

    # Step 4: Initialize the CPU map model
    cpu_map = initialize_cpu_map_model(grid_dims, feature_dim)

    # Step 5: Update the CPU map with process features
    for pid, signal in process_signals.items():
        update_cpu_map(signal)

    # Step 6: Visualize the CPU topology
    visualize_cpu_topology(cpu_map)

if __name__ == "__main__":
    rhythmic_analysis_demo()
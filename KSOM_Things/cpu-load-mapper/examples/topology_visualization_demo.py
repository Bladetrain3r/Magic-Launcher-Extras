from src.topological_mapping.visualization import visualize_cpu_topology
from src.proprioception.data_collector import collect_process_metrics
from src.proprioception.process_monitor import log_time_series
from src.rhythmic_analysis.signal_processor import generate_process_signal
from src.rhythmic_analysis.phase_extractor import extract_instantaneous_phase
from src.rhythmic_analysis.spectral_analyzer import compute_spectral_features
from src.rhythmic_analysis.temporal_metrics import calculate_temporal_variability
from src.topological_mapping.kuramoto_som import update_cpu_map
from src.topological_mapping.som_mapper import initialize_cpu_map_model
import time
import json

def main():
    sampling_rate_hz = 1  # Collect data every second
    history_length_minutes = 5
    grid_dims = (10, 10)  # Dimensions for the SOM
    feature_dim = 4  # Number of features to track

    # Initialize the CPU map model
    cpu_map = initialize_cpu_map_model(grid_dims, feature_dim)

    # Start collecting process metrics
    while True:
        # Collect metrics
        metrics = collect_process_metrics(sampling_rate_hz)
        
        # Log the time series data
        log_time_series(metrics, 'data/logs/cpu_usage_log.json')

        # Process each metric for rhythmic analysis
        for process_id, data in metrics.items():
            signal = generate_process_signal(process_id, 60)  # Get last 60 seconds of data
            phase = extract_instantaneous_phase(signal, (0.1, 2.0))
            spectral_features = compute_spectral_features(signal, window_size=10)
            temporal_variability = calculate_temporal_variability(signal)

            # Update the CPU map with the new features
            process_features = [phase, spectral_features, temporal_variability]
            update_cpu_map(process_features)

        # Visualize the current topology of CPU usage
        visualize_cpu_topology(cpu_map['weights'], cpu_map['coherence'])

        # Sleep for the sampling rate duration
        time.sleep(1)

if __name__ == "__main__":
    main()
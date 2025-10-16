from pathlib import Path
from src.proprioception.data_collector import collect_process_metrics
from src.proprioception.process_monitor import log_time_series
from src.proprioception.time_series_logger import filter_long_term_data
from src.rhythmic_analysis.signal_processor import generate_process_signal
from src.rhythmic_analysis.phase_extractor import extract_instantaneous_phase
from src.rhythmic_analysis.spectral_analyzer import compute_spectral_features
from src.rhythmic_analysis.temporal_metrics import calculate_temporal_variability
from src.topological_mapping.som_mapper import initialize_cpu_map_model
from src.topological_mapping.kuramoto_som import update_cpu_map
from src.topological_mapping.cluster_analyzer import calculate_cluster_coherence
from src.topological_mapping.visualization import visualize_cpu_topology

class CPULoadMapper:
    def __init__(self, sampling_rate_hz=1, history_length_minutes=10, grid_dims=(10, 10), feature_dim=5):
        self.sampling_rate_hz = sampling_rate_hz
        self.history_length_minutes = history_length_minutes
        self.grid_dims = grid_dims
        self.feature_dim = feature_dim
        self.process_metrics = []
        self.cpu_map = initialize_cpu_map_model(grid_dims, feature_dim)

    def collect_metrics(self):
        metrics = collect_process_metrics(self.sampling_rate_hz)
        self.process_metrics.append(metrics)
        log_time_series(metrics, 'data/logs/cpu_usage_log.csv')

    def analyze_metrics(self):
        long_term_data = filter_long_term_data(self.history_length_minutes)
        for process_id in long_term_data:
            signal = generate_process_signal(process_id, self.history_length_minutes * 60)
            phase = extract_instantaneous_phase(signal, frequency_band=(0.1, 2.0))
            spectral_features = compute_spectral_features(signal, window_size=256)
            variability = calculate_temporal_variability(signal)

            process_features = [phase, spectral_features, variability]
            update_cpu_map(process_features)

    def visualize(self):
        coherence_data = calculate_cluster_coherence(self.cpu_map)
        visualize_cpu_topology(self.cpu_map, coherence_data)

    def run(self):
        while True:
            self.collect_metrics()
            self.analyze_metrics()
            self.visualize()
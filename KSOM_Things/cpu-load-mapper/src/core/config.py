# Configuration settings for the CPU Load Mapping project

class Config:
    """Configuration settings for the CPU Load Mapping system."""
    
    # General settings
    LOG_FILE = "data/logs/cpu_load.log"
    SAMPLING_RATE_HZ = 1  # Frequency of data collection in Hz
    HISTORY_LENGTH_MINUTES = 60  # Length of history to retain for analysis
    
    # Rhythmic analysis settings
    FREQUENCY_BAND = (0.1, 2.0)  # Frequency band for phase extraction
    TIME_WINDOW_S = 10  # Time window for signal generation
    
    # Topological mapping settings
    GRID_DIMS = (10, 10)  # Dimensions of the SOM grid
    FEATURE_DIM = 4  # Number of features for each process (phase, amplitude, spectral centroid, variability)
    
    # Visualization settings
    VISUALIZATION_ENABLED = True  # Enable or disable visualization
    COHERENCE_THRESHOLD = 0.5  # Threshold for determining coherence in clusters

    @staticmethod
    def display_config():
        """Display the current configuration settings."""
        for key, value in vars(Config).items():
            if not key.startswith('__'):
                print(f"{key}: {value}")
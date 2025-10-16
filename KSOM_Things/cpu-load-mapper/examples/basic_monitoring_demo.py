from src.proprioception.data_collector import collect_process_metrics
from src.proprioception.process_monitor import log_time_series
from src.proprioception.time_series_logger import filter_long_term_data
import time

def basic_monitoring_demo(sampling_rate_hz=1, log_file='data/logs/cpu_usage_log.csv'):
    print("Starting basic CPU monitoring demo...")
    
    try:
        while True:
            # Collect CPU metrics
            data_batch = collect_process_metrics(sampling_rate_hz)
            
            # Log the collected metrics
            log_time_series(data_batch, log_file)
            
            # Optional: Filter long-term data for analysis
            long_term_data = filter_long_term_data(history_length_minutes=60)
            print("Filtered long-term data for analysis.")
            
            # Sleep for the specified sampling rate
            time.sleep(1 / sampling_rate_hz)
    
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    basic_monitoring_demo()
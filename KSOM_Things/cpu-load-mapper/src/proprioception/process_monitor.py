from pathlib import Path
import json
import psutil
import time

def log_time_series(data_batch, log_file):
    """Stores raw, timestamped data in a log file."""
    timestamped_data = [{"timestamp": time.time(), "data": data} for data in data_batch]
    
    with open(log_file, 'a') as f:
        for entry in timestamped_data:
            f.write(json.dumps(entry) + '\n')
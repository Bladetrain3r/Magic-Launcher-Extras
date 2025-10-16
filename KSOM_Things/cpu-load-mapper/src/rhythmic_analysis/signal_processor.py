from collections import deque
import psutil
import numpy as np

def generate_process_signal(process_id, time_window_s):
    """Isolates the CPU usage history for a specific process."""
    process = psutil.Process(process_id)
    signal = deque(maxlen=int(time_window_s * psutil.cpu_freq().current / 100))  # Adjust for sampling rate

    try:
        for _ in range(signal.maxlen):
            signal.append(process.cpu_percent(interval=1))
    except psutil.NoSuchProcess:
        return []

    return np.array(signal)  # Return as a numpy array for further processing
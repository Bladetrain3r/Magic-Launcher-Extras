from pathlib import Path
import psutil
import time
import json

def collect_process_metrics(sampling_rate_hz):
    metrics = []
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                metrics.append({
                    'timestamp': time.time(),
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(1 / sampling_rate_hz)
        yield metrics  # Yielding metrics for further processing or logging
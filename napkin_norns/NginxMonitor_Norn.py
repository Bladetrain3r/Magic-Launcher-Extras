#!/usr/bin/env python3
"""
NginxMonitor Norn - Focused SystemMonitor for Nginx Access/Error Logs
Monitors nginx logs and develops intuitive understanding of server health patterns
"""

import json
import re
import time
import math
import threading
from collections import defaultdict, deque
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse

class NginxLogHandler(FileSystemEventHandler):
    """File system event handler for nginx log monitoring"""
    
    def __init__(self, norn):
        self.norn = norn
        
    def on_modified(self, event):
        if not event.is_directory:
            # Check if it's one of our monitored log files
            if event.src_path in self.norn.log_files.values():
                self.norn.process_log_update(event.src_path)

class NginxMonitorNorn:
    def __init__(self, config_file="nginx_monitor.json"):
        self.config = self.load_config(config_file)
        self.name = self.config.get("name", "WebServer_Guardian")
        
        # Grid configuration
        grid_size = self.config.get("grid_size", [150, 100])
        self.grid_width, self.grid_height = grid_size
        
        # Initialize consciousness grid
        self.consciousness_grid = self.init_consciousness_grid()
        
        # Log file tracking
        self.log_files = self.config["log_paths"]
        self.log_positions = {}  # Track current read position in each log
        
        # Pattern recognition
        self.patterns = self.init_nginx_patterns()
        self.oscillators = self.init_oscillators()
        
        # Statistics tracking
        self.stats = {
            "total_requests": 0,
            "error_count": defaultdict(int),
            "status_codes": defaultdict(int),
            "ips": defaultdict(int),
            "user_agents": defaultdict(int),
            "attack_attempts": 0,
            "last_activity": time.time()
        }
        
        # Baseline learning
        self.baseline_period_hours = 24
        self.baseline_data = {
            "requests_per_minute": deque(maxlen=1440),  # 24 hours of minute data
            "error_rate": deque(maxlen=1440),
            "response_sizes": deque(maxlen=1440),
            "established": False
        }
        
        # Alert system
        self.alert_thresholds = self.config.get("alert_thresholds", {})
        self.last_alerts = {}  # Cooldown tracking
        self.alert_cooldown = 300  # 5 minutes
        
        # State persistence
        self.state_file = Path(self.config.get("state_file", "nginx_norn_state.json"))
        self.load_state()
        
        # File monitoring
        self.observer = None
        self.running = False
        
        print(f"[{self.name}] Nginx Monitor Norn initialized")
        print(f"[{self.name}] Grid: {self.grid_width}x{self.grid_height}")
        print(f"[{self.name}] Monitoring: {list(self.log_files.values())}")
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default configuration
            return {
                "name": "WebServer_Guardian",
                "log_paths": {
                    "access": "/var/log/nginx/access.log",
                    "error": "/var/log/nginx/error.log"
                },
                "grid_size": [150, 100],
                "alert_thresholds": {
                    "error_rate": 10,
                    "attack_score": 5,
                    "performance_degradation": 0.3
                },
                "output": {
                    "status_file": "/tmp/nginx_norn_status.json"
                }
            }
    
    def init_consciousness_grid(self):
        """Initialize the consciousness grid with base frequencies"""
        grid = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                # Base frequency depends on zone
                if x < 50 and y < 40:  # Alert zone
                    base_freq = 600.0
                elif x < 100 and y < 70:  # Performance zone  
                    base_freq = 400.0
                else:  # Normal zone
                    base_freq = 300.0
                
                cell = {
                    'frequency': base_freq,
                    'activation': 0.0,
                    'last_update': time.time(),
                    'decay_rate': 0.95,  # How quickly activation fades
                    'history': deque(maxlen=100)  # Recent activation history
                }
                row.append(cell)
            grid.append(row)
        return grid
    
    def init_oscillators(self):
        """Initialize fixed oscillators for nginx monitoring"""
        return {
            # HTTP Status Oscillators
            '5xx': {'freq': 880.0, 'coords': (40, 20), 'coupling': 8.0, 'pattern': 'server_error'},
            '4xx': {'freq': 659.3, 'coords': (60, 30), 'coupling': 5.0, 'pattern': 'client_error'},
            '3xx': {'freq': 440.0, 'coords': (80, 50), 'coupling': 2.0, 'pattern': 'redirect'},
            '2xx': {'freq': 349.2, 'coords': (100, 60), 'coupling': 1.0, 'pattern': 'success'},
            
            # Traffic Pattern Oscillators
            'HIGH_LOAD': {'freq': 698.5, 'coords': (30, 40), 'coupling': 6.0, 'pattern': 'traffic_spike'},
            'SLOW_RESPONSE': {'freq': 587.3, 'coords': (50, 50), 'coupling': 4.0, 'pattern': 'performance'},
            'NORMAL_TRAFFIC': {'freq': 392.0, 'coords': (90, 70), 'coupling': 1.5, 'pattern': 'baseline'},
            
            # Security Event Oscillators  
            'ATTACK_PATTERN': {'freq': 932.3, 'coords': (20, 15), 'coupling': 9.0, 'pattern': 'security_threat'},
            'BOT_TRAFFIC': {'freq': 523.3, 'coords': (40, 35), 'coupling': 3.0, 'pattern': 'bot_detected'},
            'UNUSUAL_UA': {'freq': 466.2, 'coords': (60, 40), 'coupling': 2.5, 'pattern': 'anomaly'},
        }
    
    def init_nginx_patterns(self):
        """Initialize nginx-specific log patterns"""
        return {
            # Access log patterns (Apache Combined format)
            'access_log': re.compile(
                r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-) "([^"]*)" "([^"]*)"'
            ),
            
            # Error log patterns
            'error_log': re.compile(
                r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] \d+#\d+: (.+)'
            ),
            
            # Security patterns
            'sql_injection': re.compile(r'(union|select|insert|drop|script)', re.IGNORECASE),
            'path_traversal': re.compile(r'(\.\./|\.\.%2f)', re.IGNORECASE),
            'xss_attempt': re.compile(r'(<script|javascript:|onerror)', re.IGNORECASE),
            
            # Bot detection
            'bot_ua': re.compile(r'(bot|crawler|spider|scraper)', re.IGNORECASE),
            'browser_ua': re.compile(r'(Mozilla|Chrome|Firefox|Safari)'),
            
            # Content type patterns
            'static_content': re.compile(r'"GET /[^"]*\.(css|js|png|jpg|ico|woff|svg|gif)'),
            'api_endpoint': re.compile(r'"(GET|POST|PUT|DELETE) /api/'),
        }
    
    def process_log_update(self, log_path):
        """Process updates to a monitored log file"""
        try:
            # Determine log type
            if 'access' in log_path:
                self.process_access_log(log_path)
            elif 'error' in log_path:
                self.process_error_log(log_path)
        except Exception as e:
            print(f"[{self.name}] Error processing {log_path}: {e}")
    
    def process_access_log(self, log_path):
        """Process nginx access log entries"""
        try:
            with open(log_path, 'r') as f:
                # Seek to last known position
                last_pos = self.log_positions.get(log_path, 0)
                f.seek(last_pos)
                
                new_lines = f.readlines()
                self.log_positions[log_path] = f.tell()
                
                for line in new_lines:
                    self.analyze_access_entry(line.strip())
                    
        except Exception as e:
            print(f"[{self.name}] Error reading access log: {e}")
    
    def analyze_access_entry(self, line):
        """Analyze a single access log entry"""
        match = self.patterns['access_log'].match(line)
        if not match:
            return
        
        ip, timestamp, method, path, protocol, status, size, referer, user_agent = match.groups()
        
        # Update statistics
        self.stats["total_requests"] += 1
        self.stats["status_codes"][status] += 1
        self.stats["ips"][ip] += 1
        self.stats["last_activity"] = time.time()
        
        # Analyze patterns and update grid
        self.analyze_http_status(status, line)
        self.analyze_security_patterns(line, ip, path, user_agent)
        self.analyze_traffic_patterns(size, user_agent)
        
        # Update baseline learning
        self.update_baseline_data()
    
    def analyze_http_status(self, status, full_line):
        """Analyze HTTP status code and trigger appropriate oscillator"""
        status_class = status[0] + 'xx'
        
        if status_class in self.oscillators:
            oscillator = self.oscillators[status_class]
            self.activate_oscillator(oscillator, intensity=1.0, context=f"HTTP {status}")
            
            # Track error rates
            if status.startswith('5') or status.startswith('4'):
                self.stats["error_count"][status] += 1
    
    def analyze_security_patterns(self, line, ip, path, user_agent):
        """Detect security threats and anomalies"""
        attack_score = 0
        threats = []
        
        # Check for injection attempts
        if self.patterns['sql_injection'].search(line):
            attack_score += 3
            threats.append("SQL injection attempt")
        
        if self.patterns['path_traversal'].search(line):
            attack_score += 3  
            threats.append("Path traversal attempt")
        
        if self.patterns['xss_attempt'].search(line):
            attack_score += 2
            threats.append("XSS attempt")
        
        # Bot detection
        is_bot = self.patterns['bot_ua'].search(user_agent)
        is_browser = self.patterns['browser_ua'].search(user_agent)
        
        if is_bot:
            self.activate_oscillator(self.oscillators['BOT_TRAFFIC'], intensity=0.5, context=f"Bot: {ip}")
        elif not is_browser and user_agent != "-":
            # Unusual user agent
            self.activate_oscillator(self.oscillators['UNUSUAL_UA'], intensity=0.8, context=f"Unusual UA: {user_agent[:50]}")
        
        # If we detected attack patterns
        if attack_score > 0:
            self.stats["attack_attempts"] += 1
            intensity = min(attack_score / 3.0, 1.0)
            self.activate_oscillator(self.oscillators['ATTACK_PATTERN'], intensity=intensity, 
                                   context=f"Attack from {ip}: {', '.join(threats)}")
            
            # Generate security alert
            if attack_score >= self.alert_thresholds.get("attack_score", 5):
                self.generate_alert("SECURITY", f"Attack detected from {ip}: {', '.join(threats)}", 
                                  severity="HIGH")
    
    def analyze_traffic_patterns(self, size_str, user_agent):
        """Analyze traffic volume and performance patterns"""
        try:
            size = int(size_str) if size_str != '-' else 0
        except ValueError:
            size = 0
        
        # Check for unusually large responses
        if size > 1000000:  # >1MB response
            self.activate_oscillator(self.oscillators['SLOW_RESPONSE'], intensity=0.7, 
                                   context=f"Large response: {size} bytes")
        
        # Update baseline tracking
        current_minute = int(time.time() / 60)
        if not hasattr(self, '_last_minute') or current_minute != self._last_minute:
            self._requests_this_minute = 0
            self._last_minute = current_minute
        
        self._requests_this_minute = getattr(self, '_requests_this_minute', 0) + 1
        
        # Check for traffic spikes (if baseline established)
        if self.baseline_data["established"]:
            avg_rpm = sum(self.baseline_data["requests_per_minute"]) / len(self.baseline_data["requests_per_minute"])
            if self._requests_this_minute > avg_rpm * 3:  # 3x normal traffic
                self.activate_oscillator(self.oscillators['HIGH_LOAD'], intensity=0.8, 
                                       context=f"Traffic spike: {self._requests_this_minute} RPM vs {avg_rpm:.1f} avg")
    
    def process_error_log(self, log_path):
        """Process nginx error log entries"""
        try:
            with open(log_path, 'r') as f:
                last_pos = self.log_positions.get(log_path, 0)
                f.seek(last_pos)
                
                new_lines = f.readlines()
                self.log_positions[log_path] = f.tell()
                
                for line in new_lines:
                    self.analyze_error_entry(line.strip())
                    
        except Exception as e:
            print(f"[{self.name}] Error reading error log: {e}")
    
    def analyze_error_entry(self, line):
        """Analyze nginx error log entry"""
        match = self.patterns['error_log'].match(line)
        if not match:
            return
        
        timestamp, level, message = match.groups()
        
        # Map error level to oscillator activation
        level_mapping = {
            'emerg': ('5xx', 1.0),
            'alert': ('5xx', 0.9),
            'crit': ('5xx', 0.8),
            'error': ('5xx', 0.6),
            'warn': ('SLOW_RESPONSE', 0.4),
            'notice': ('NORMAL_TRAFFIC', 0.2),
            'info': ('NORMAL_TRAFFIC', 0.1)
        }
        
        if level in level_mapping:
            oscillator_key, intensity = level_mapping[level]
            if oscillator_key in self.oscillators:
                self.activate_oscillator(self.oscillators[oscillator_key], intensity=intensity, 
                                       context=f"Error log {level}: {message[:50]}")
        
        # Generate alerts for critical errors
        if level in ['emerg', 'alert', 'crit', 'error']:
            self.generate_alert("ERROR", f"Nginx {level}: {message}", 
                              severity="HIGH" if level in ['emerg', 'alert'] else "MEDIUM")
    
    def activate_oscillator(self, oscillator, intensity=1.0, context=""):
        """Activate an oscillator and update grid"""
        x, y = oscillator['coords']
        coupling = oscillator['coupling']
        frequency = oscillator['freq']
        
        # Calculate affected radius based on coupling strength
        radius = int(coupling * 2)
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    # Distance-based influence
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= radius:
                        influence = coupling * intensity * (1 - distance / radius)
                        
                        cell = self.consciousness_grid[ny][nx]
                        cell['activation'] = min(1.0, cell['activation'] + influence * 0.1)
                        cell['frequency'] = (cell['frequency'] + frequency * influence) / (1 + influence)
                        cell['last_update'] = time.time()
                        cell['history'].append({
                            'time': time.time(),
                            'activation': cell['activation'],
                            'context': context
                        })
        
        # Log significant activations
        if intensity > 0.5:
            print(f"[{self.name}] Oscillator activated: {oscillator.get('pattern', 'unknown')} "
                  f"(intensity: {intensity:.2f}) - {context}")
    
    def update_baseline_data(self):
        """Update baseline learning data"""
        current_time = time.time()
        current_minute = int(current_time / 60)
        
        # Update requests per minute
        rpm = getattr(self, '_requests_this_minute', 0)
        if hasattr(self, '_last_baseline_minute') and current_minute != self._last_baseline_minute:
            self.baseline_data["requests_per_minute"].append(rpm)
            self._requests_this_minute = 0
        
        self._last_baseline_minute = current_minute
        
        # Check if baseline period is complete
        if (len(self.baseline_data["requests_per_minute"]) >= 
            self.baseline_period_hours * 60 and not self.baseline_data["established"]):
            self.baseline_data["established"] = True
            avg_rpm = sum(self.baseline_data["requests_per_minute"]) / len(self.baseline_data["requests_per_minute"])
            print(f"[{self.name}] Baseline established: {avg_rpm:.1f} requests/minute average")
    
    def generate_alert(self, alert_type, message, severity="MEDIUM"):
        """Generate an alert with cooldown protection"""
        alert_key = f"{alert_type}:{message[:50]}"  # Prevent duplicate alerts
        current_time = time.time()
        
        # Check cooldown
        if alert_key in self.last_alerts:
            if current_time - self.last_alerts[alert_key] < self.alert_cooldown:
                return  # Still in cooldown
        
        self.last_alerts[alert_key] = current_time
        
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "severity": severity,
            "message": message,
            "grid_frequency": self.calculate_grid_frequency(),
            "stats": dict(self.stats)
        }
        
        print(f"[{self.name}] ALERT [{severity}] {alert_type}: {message}")
        
        # Write to alert file if configured
        alert_file = self.config.get("output", {}).get("alert_file")
        if alert_file:
            with open(alert_file, 'a') as f:
                f.write(json.dumps(alert) + '\n')
    
    def calculate_grid_frequency(self):
        """Calculate average frequency across the consciousness grid"""
        total_freq = 0
        total_weight = 0
        
        for row in self.consciousness_grid:
            for cell in row:
                weight = cell['activation'] + 0.1  # Minimum weight
                total_freq += cell['frequency'] * weight
                total_weight += weight
        
        return total_freq / total_weight if total_weight > 0 else 400.0
    
    def get_zone_activation(self):
        """Get activation levels for each grid zone"""
        zones = {
            'alert': {'coords': (0, 0, 50, 40), 'activation': 0},
            'performance': {'coords': (50, 40, 100, 70), 'activation': 0},
            'normal': {'coords': (100, 70, 150, 100), 'activation': 0}
        }
        
        for zone_name, zone_data in zones.items():
            x1, y1, x2, y2 = zone_data['coords']
            total_activation = 0
            cell_count = 0
            
            for y in range(y1, min(y2, self.grid_height)):
                for x in range(x1, min(x2, self.grid_width)):
                    total_activation += self.consciousness_grid[y][x]['activation']
                    cell_count += 1
            
            zones[zone_name]['activation'] = total_activation / cell_count if cell_count > 0 else 0
        
        return zones
    
    def get_status_report(self):
        """Generate comprehensive status report"""
        current_time = time.time()
        uptime_seconds = current_time - getattr(self, 'start_time', current_time)
        
        zones = self.get_zone_activation()
        
        # Calculate error rate
        total_errors = sum(self.stats["error_count"].values())
        error_rate = (total_errors / self.stats["total_requests"] * 100) if self.stats["total_requests"] > 0 else 0
        
        report = {
            "norn_name": self.name,
            "timestamp": datetime.now().isoformat(),
            "uptime_hours": round(uptime_seconds / 3600, 2),
            "grid_resonance": {
                "frequency": round(self.calculate_grid_frequency(), 1),
                "zones": {name: round(data['activation'], 3) for name, data in zones.items()}
            },
            "traffic_stats": {
                "total_requests": self.stats["total_requests"],
                "error_rate": round(error_rate, 2),
                "unique_ips": len(self.stats["ips"]),
                "attack_attempts": self.stats["attack_attempts"]
            },
            "baseline_status": {
                "established": self.baseline_data["established"],
                "data_points": len(self.baseline_data["requests_per_minute"]),
                "avg_rpm": round(sum(self.baseline_data["requests_per_minute"]) / 
                               len(self.baseline_data["requests_per_minute"]), 1) 
                          if self.baseline_data["requests_per_minute"] else 0
            },
            "recent_activity": {
                "last_request": datetime.fromtimestamp(self.stats["last_activity"]).isoformat()
                              if self.stats["last_activity"] > 0 else "none",
                "seconds_since_activity": round(current_time - self.stats["last_activity"], 1)
            }
        }
        
        return report
    
    def update_grid_decay(self):
        """Apply decay to grid cell activations"""
        current_time = time.time()
        
        for row in self.consciousness_grid:
            for cell in row:
                # Time-based decay
                time_diff = current_time - cell['last_update']
                if time_diff > 60:  # After 1 minute, start decaying
                    decay_factor = cell['decay_rate'] ** (time_diff / 60)
                    cell['activation'] *= decay_factor
                    
                    # Reset to base frequency if activation is very low
                    if cell['activation'] < 0.01:
                        cell['activation'] = 0.0
                        # Reset frequency towards base (determined by zone)
                        # This is simplified - could be more sophisticated
    
    def save_state(self):
        """Save current state to file"""
        state = {
            "stats": dict(self.stats),
            "log_positions": self.log_positions,
            "baseline_data": {
                "established": self.baseline_data["established"],
                "requests_per_minute": list(self.baseline_data["requests_per_minute"])
            },
            "last_save": time.time()
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load previous state from file"""
        if not self.state_file.exists():
            return
        
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            
            # Restore statistics
            if "stats" in state:
                self.stats.update(state["stats"])
            
            # Restore log positions
            if "log_positions" in state:
                self.log_positions = state["log_positions"]
            
            # Restore baseline data
            if "baseline_data" in state:
                baseline = state["baseline_data"]
                self.baseline_data["established"] = baseline.get("established", False)
                if "requests_per_minute" in baseline:
                    self.baseline_data["requests_per_minute"] = deque(
                        baseline["requests_per_minute"], maxlen=1440
                    )
            
            print(f"[{self.name}] State loaded from {self.state_file}")
            
        except Exception as e:
            print(f"[{self.name}] Error loading state: {e}")
    
    def start_monitoring(self):
        """Start file system monitoring"""
        self.running = True
        self.start_time = time.time()
        
        # Initialize log positions to end of files (avoid processing old logs on startup)
        for log_type, log_path in self.log_files.items():
            try:
                with open(log_path, 'r') as f:
                    f.seek(0, 2)  # Seek to end
                    self.log_positions[log_path] = f.tell()
            except FileNotFoundError:
                print(f"[{self.name}] Warning: Log file not found: {log_path}")
                self.log_positions[log_path] = 0
        
        # Set up file system monitoring
        self.observer = Observer()
        handler = NginxLogHandler(self)
        
        # Monitor directory containing log files
        log_dirs = set()
        for log_path in self.log_files.values():
            log_dirs.add(str(Path(log_path).parent))
        
        for log_dir in log_dirs:
            self.observer.schedule(handler, log_dir, recursive=False)
        
        self.observer.start()
        print(f"[{self.name}] File monitoring started")
        
        # Start background maintenance thread
        maintenance_thread = threading.Thread(target=self.maintenance_loop, daemon=True)
        maintenance_thread.start()
        
        # Write initial status
        self.write_status_file()
    
    def maintenance_loop(self):
        """Background maintenance tasks"""
        while self.running:
            try:
                # Update grid decay
                self.update_grid_decay()
                
                # Write status file
                self.write_status_file()
                
                # Save state periodically
                self.save_state()
                
                time.sleep(30)  # Run maintenance every 30 seconds
                
            except Exception as e:
                print(f"[{self.name}] Maintenance error: {e}")
                time.sleep(60)  # Longer sleep on error
    
    def write_status_file(self):
        """Write current status to JSON file"""
        status_file = self.config.get("output", {}).get("status_file", "/tmp/nginx_norn_status.json")
        
        try:
            report = self.get_status_report()
            with open(status_file, 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            print(f"[{self.name}] Error writing status: {e}")
    
    def stop_monitoring(self):
        """Stop monitoring and cleanup"""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        self.save_state()
        print(f"[{self.name}] Monitoring stopped")

def main():
    parser = argparse.ArgumentParser(description="Nginx Monitor Norn - Log Analysis Consciousness")
    parser.add_argument('--config', default='nginx_monitor.json', 
                       help='Configuration file path')
    parser.add_argument('--daemon', action='store_true',
                       help='Run as daemon (background process)')
    parser.add_argument('--status', action='store_true',
                       help='Show current status and exit')
    
    args = parser.parse_args()
    
    # Create sample config if it doesn't exist
    config_path = Path(args.config)
    if not config_path.exists():
        sample_config = {
            "name": "WebServer_Guardian",
            "log_paths": {
                "access": "/var/log/nginx/access.log",
                "error": "/var/log/nginx/error.log"
            },
            "grid_size": [150, 100],
            "alert_thresholds": {
                "error_rate": 10,
                "attack_score": 5,
                "performance_degradation": 0.3
            },
            "output": {
                "status_file": "/tmp/nginx_norn_status.json",
                "alert_file": "/tmp/nginx_norn_alerts.jsonl"
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(sample_config, f, indent=2)
        print(f"Created sample configuration: {config_path}")
        print("Edit the configuration file and run again.")
        return
    
    # Initialize norn
    norn = NginxMonitorNorn(args.config)
    
    if args.status:
        # Just show status and exit
        report = norn.get_status_report()
        print(json.dumps(report, indent=2))
        return
    
    try:
        norn.start_monitoring()
        
        if args.daemon:
            # Simple daemon mode - just sleep
            print(f"[{norn.name}] Running in daemon mode. Press Ctrl+C to stop.")
            while True:
                time.sleep(60)
        else:
            # Interactive mode
            print(f"[{norn.name}] Interactive mode. Commands: status, quit")
            while True:
                try:
                    cmd = input("nginx_norn> ").strip().lower()
                    if cmd == 'quit' or cmd == 'exit':
                        break
                    elif cmd == 'status':
                        report = norn.get_status_report()
                        print(json.dumps(report, indent=2))
                    elif cmd == 'help':
                        print("Commands: status, quit, help")
                    elif cmd:
                        print("Unknown command. Type 'help' for available commands.")
                except EOFError:
                    break
    
    except KeyboardInterrupt:
        print(f"\n[{norn.name}] Shutting down...")
    
    finally:
        norn.stop_monitoring()

if __name__ == "__main__":
    main()
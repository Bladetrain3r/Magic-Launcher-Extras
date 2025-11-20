# Nginx Monitor Norn - Focused Architecture

## Overview

A specialized SystemMonitor Norn designed specifically for **Nginx access and error log monitoring**. This norn develops intuitive understanding of web server health patterns, traffic anomalies, and potential security threats through continuous log analysis.

## Core Design - Nginx Specific

### Fixed Oscillator Grid (Nginx-Focused)

**HTTP Status Code Oscillators:**
```python
HTTP_STATUS_OSCILLATORS = {
    '5xx': {'freq': 880.0, 'coords': (40, 20), 'coupling': 8.0},   # Server errors - high urgency
    '4xx': {'freq': 659.3, 'coords': (60, 30), 'coupling': 5.0},   # Client errors - moderate concern
    '3xx': {'freq': 440.0, 'coords': (80, 50), 'coupling': 2.0},   # Redirects - normal operation
    '2xx': {'freq': 349.2, 'coords': (100, 60), 'coupling': 1.0},  # Success - baseline good
}
```

**Traffic Pattern Oscillators:**
```python
TRAFFIC_OSCILLATORS = {
    'HIGH_LOAD': {'freq': 698.5, 'coords': (30, 40), 'coupling': 6.0},    # Traffic spikes
    'SLOW_RESPONSE': {'freq': 587.3, 'coords': (50, 50), 'coupling': 4.0}, # Performance issues
    'NORMAL_TRAFFIC': {'freq': 392.0, 'coords': (90, 70), 'coupling': 1.5}, # Baseline traffic
    'LOW_TRAFFIC': {'freq': 261.6, 'coords': (110, 80), 'coupling': 1.0},   # Quiet periods
}
```

**Security Event Oscillators:**
```python
SECURITY_OSCILLATORS = {
    'ATTACK_PATTERN': {'freq': 932.3, 'coords': (20, 15), 'coupling': 9.0},  # Security threats
    'BOT_TRAFFIC': {'freq': 523.3, 'coords': (40, 35), 'coupling': 3.0},     # Bot detection
    'UNUSUAL_UA': {'freq': 466.2, 'coords': (60, 40), 'coupling': 2.5},      # Odd user agents
    'NORMAL_UA': {'freq': 329.6, 'coords': (120, 65), 'coupling': 1.0},      # Standard browsers
}
```

## Log Processing Engine

### Access Log Pattern Recognition

**Standard Apache Combined Log Format:**
```
IP - - [timestamp] "METHOD /path HTTP/1.1" status size "referer" "user-agent"
```

**Semantic Analysis Rules:**
```python
ACCESS_LOG_PATTERNS = {
    # HTTP Status Patterns
    'status_5xx': r'HTTP/1\.[01]" (5\d\d) ',
    'status_4xx': r'HTTP/1\.[01]" (4\d\d) ',
    'status_3xx': r'HTTP/1\.[01]" (3\d\d) ',
    'status_2xx': r'HTTP/1\.[01]" (2\d\d) ',
    
    # Traffic Volume Indicators
    'large_response': r'" \d\d\d (\d{6,}) ',        # >100KB responses
    'small_response': r'" \d\d\d (\d{1,4}) ',       # <10KB responses
    
    # Security Patterns
    'sql_injection': r'(union|select|insert|drop|script)',
    'path_traversal': r'(\.\./|\.\.\%2f)',
    'xss_attempt': r'(<script|javascript:|onerror)',
    
    # Bot Detection
    'bot_ua': r'(bot|crawler|spider|scraper)',
    'browser_ua': r'(Mozilla|Chrome|Firefox|Safari)',
    
    # Performance Indicators  
    'static_content': r'"GET /[^"]*\.(css|js|png|jpg|ico|woff)',
    'api_endpoint': r'"(GET|POST|PUT|DELETE) /api/',
    'admin_access': r'"[A-Z]+ /(admin|wp-admin|phpmyadmin)',
}
```

### Error Log Pattern Recognition

**Nginx Error Log Levels:**
```python
ERROR_LOG_PATTERNS = {
    'emerg': {'oscillator': 'CRITICAL', 'coupling': 10.0},
    'alert': {'oscillator': 'CRITICAL', 'coupling': 9.0}, 
    'crit': {'oscillator': 'ERROR', 'coupling': 8.0},
    'error': {'oscillator': 'ERROR', 'coupling': 6.0},
    'warn': {'oscillator': 'WARNING', 'coupling': 4.0},
    'notice': {'oscillator': 'INFO', 'coupling': 2.0},
    'info': {'oscillator': 'DEBUG', 'coupling': 1.0},
    'debug': {'oscillator': 'TRACE', 'coupling': 0.5},
}
```

## Simplified Grid Architecture

**Grid Specifications:**
- **Dimensions**: 150x100 (manageable for single-server monitoring)
- **Zones**:
  - **Alert Zone** (0-50, 0-40): Critical issues, attacks, server errors
  - **Performance Zone** (50-100, 40-70): Load, response times, resource usage  
  - **Normal Zone** (100-150, 70-100): Standard operations, successful requests

## Practical Monitoring Features

### Real-Time Health Metrics

```python
NginxHealth = {
    'server_health': {
        'error_rate': float,           # 5xx errors per minute
        'response_performance': float,  # Average response size trends
        'availability': float,         # Uptime based on error patterns
    },
    'traffic_analysis': {
        'requests_per_minute': int,
        'bandwidth_usage': float,
        'client_distribution': dict,   # Geographic/IP patterns
    },
    'security_status': {
        'attack_attempts': int,        # Security events per hour
        'bot_ratio': float,           # Bot traffic percentage
        'anomaly_score': float,       # Unusual pattern detection
    },
    'grid_resonance': {
        'primary_frequency': float,    # Current dominant concern
        'zone_activation': dict,       # Activity per grid zone
    }
}
```

### Alert Generation

**Critical Alerts:**
```
NGINX ALERT: Server Error Spike Detected
Error Rate: 15 x 5xx errors in last 5 minutes
Grid Resonance: 847.3Hz (CRITICAL zone activated)
Pattern Match: Similar to incident on 2025-10-15 (database connection failure)
Recent Errors:
- 502 Bad Gateway (8 occurrences)  
- 504 Gateway Timeout (7 occurrences)
Recommendation: Check upstream server health
```

**Security Alerts:**
```
NGINX SECURITY: Attack Pattern Detected  
Source IP: 192.168.1.100
Attack Type: SQL injection attempts (15 requests)
Target Paths: /api/users, /admin/login
Grid Response: ATTACK_PATTERN oscillator activated
Action: IP temporarily flagged for monitoring
```

**Performance Warnings:**
```
NGINX PERFORMANCE: Response Size Anomaly
Average Response: 2.3MB (normally 45KB)
Affected Endpoint: /api/export
Grid Signal: HIGH_LOAD zone showing sustained activation
Suggestion: Review export query efficiency or implement caching
```

## Implementation Strategy

### Log Ingestion Pipeline

**File Monitoring:**
```python
LOG_SOURCES = {
    'access_log': '/var/log/nginx/access.log',
    'error_log': '/var/log/nginx/error.log',
    'custom_log': '/var/log/nginx/custom.log'  # If using custom log formats
}

MONITORING_CONFIG = {
    'poll_interval': 1.0,          # Check logs every second
    'batch_size': 100,             # Process 100 lines at once
    'retention_hours': 72,         # Keep 3 days of pattern data
    'alert_cooldown': 300,         # 5 min between similar alerts
}
```

### Pattern Learning

**Baseline Establishment:**
- Monitor for 24-48 hours to establish normal traffic patterns
- Learn typical request volumes per hour/day
- Establish baseline error rates and response sizes
- Identify regular bot traffic vs. human users

**Anomaly Detection:**
- Statistical deviation from learned baselines
- Unusual IP address patterns
- Abnormal request sequences
- Response time degradation trends

## Deployment Configuration

### Minimal Setup

**Requirements:**
- Python 3.8+ with file monitoring capabilities
- Read access to Nginx log files
- Optional: Integration with existing monitoring (Grafana, Prometheus)

**Installation:**
```bash
# Install dependencies
pip install watchdog numpy

# Configure log access
sudo usermod -a -G adm nginx_monitor_user

# Deploy norn
python3 NginxMonitor_Norn.py --config nginx_monitor.json
```

**Configuration File:**
```json
{
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
        "alert_webhook": "http://localhost:3000/alerts"
    }
}
```

## Success Metrics

**Operational Effectiveness:**
- **Alert Accuracy**: <5% false positive rate for critical alerts
- **Response Time**: Detect anomalies within 60 seconds of occurrence  
- **Pattern Recognition**: Identify repeat attack patterns with >90% accuracy
- **Performance Impact**: <1% CPU usage on monitoring server

**Practical Value:**
- Earlier detection of server issues before customer impact
- Automated categorization of security threats
- Trend analysis for capacity planning
- Reduced manual log analysis time

## Future Enhancements

**Phase 2 Features:**
- Integration with multiple Nginx instances (load balancer monitoring)
- Correlation with system metrics (CPU, memory, disk I/O)
- Machine learning enhancement of pattern recognition
- Custom alert rule configuration through web interface

This focused approach provides immediate practical value while demonstrating the core SystemMonitor Norn concepts in a real-world scenario.
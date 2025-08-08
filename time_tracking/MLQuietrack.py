#!/usr/bin/env python3
"""
MLPassive - Passive process tracker
Watches for known applications and tracks their time
Same data format as MLTracker, different approach
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
import signal

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("Warning: psutil not found. Install with: pip install psutil")
    print("MLPassive requires psutil for cross-platform process monitoring.")
    sys.exit(1)

class MLPassive:
   def __init__(self):
       # Data file (same as MLTracker)
       self.data_file = Path.home() / '.config' / 'mltracker' / 'tracked.json'
       self.data_file.parent.mkdir(parents=True, exist_ok=True)
       
       # State
       self.known_apps = {}  # exe_path -> app_name mapping
       self.tracking = {}    # exe_path -> start_time
       self.running = True
       
       # Load known apps
       self.load_known_apps()
       
       # Handle signals
       signal.signal(signal.SIGINT, self.shutdown)
       signal.signal(signal.SIGTERM, self.shutdown)
   
   def load_known_apps(self):
       """Load known applications from tracked.json"""
       if self.data_file.exists():
           try:
               with open(self.data_file, 'r') as f:
                   data = json.load(f)
               
               # Build exe -> name mapping
               for app_name, app_data in data.items():
                   if 'path' in app_data and app_data['path'] != 'manual':
                       # Handle paths with arguments
                       exe_path = app_data['path'].split()[0]
                       self.known_apps[exe_path.lower()] = app_name
               
               print(f"Monitoring {len(self.known_apps)} applications")
               
           except Exception as e:
               print(f"Error loading tracked.json: {e}")
               self.known_apps = {}
       else:
           print("No tracked.json found. Track some apps with MLTracker first.")
           sys.exit(1)
   
   def save_session(self, app_name, exe_path, start_time, end_time):
       """Save a tracked session"""
       duration = int(end_time - start_time)
       
       # Skip very short sessions (< 30 seconds)
       if duration < 30:
           return
       
       # Load current data
       data = {}
       if self.data_file.exists():
           with open(self.data_file, 'r') as f:
               data = json.load(f)
       
       # Update data
       if app_name not in data:
           data[app_name] = {
               "path": exe_path,
               "total_time": 0,
               "sessions": []
           }
       
       data[app_name]["sessions"].append({
           "start": datetime.fromtimestamp(start_time).isoformat(),
           "duration": duration,
           "passive": True  # Mark as passively tracked
       })
       data[app_name]["total_time"] += duration
       
       # Save
       with open(self.data_file, 'w') as f:
           json.dump(data, f, indent=2)
       
       # Report
       hours = duration // 3600
       minutes = (duration % 3600) // 60
       print(f"[{datetime.now().strftime('%H:%M:%S')}] {app_name}: {hours}h {minutes}m {duration % 60}s")
   
   def scan_processes(self):
       """Scan running processes and update tracking"""
       current_exes = set()
       
       try:
           for proc in psutil.process_iter(['pid', 'name', 'exe']):
               try:
                   exe_path = proc.info['exe']
                   if exe_path:
                       exe_lower = exe_path.lower()
                       current_exes.add(exe_lower)
                       
                       # Check if this is a known app we're not tracking
                       if exe_lower in self.known_apps and exe_lower not in self.tracking:
                           # Started
                           self.tracking[exe_lower] = time.time()
                           app_name = self.known_apps[exe_lower]
                           print(f"[{datetime.now().strftime('%H:%M:%S')}] Started tracking: {app_name}")
               
               except (psutil.NoSuchProcess, psutil.AccessDenied):
                   pass
           
           # Check for stopped processes
           stopped = []
           for exe_path, start_time in self.tracking.items():
               if exe_path not in current_exes:
                   # Process ended
                   app_name = self.known_apps[exe_path]
                   self.save_session(app_name, exe_path, start_time, time.time())
                   stopped.append(exe_path)
           
           # Remove stopped from tracking
           for exe_path in stopped:
               del self.tracking[exe_path]
               
       except Exception as e:
           print(f"Error scanning processes: {e}")
   
   def run(self):
       """Main monitoring loop"""
       print("MLPassive - Passive Process Tracker")
       print("Press Ctrl+C to stop")
       print("-" * 40)
       
       while self.running:
           self.scan_processes()
           time.sleep(5)  # Check every 5 seconds
   
   def shutdown(self, signum, frame):
       """Clean shutdown"""
       print("\n\nShutting down...")
       self.running = False
       
       # Save any active sessions
       for exe_path, start_time in self.tracking.items():
           app_name = self.known_apps[exe_path]
           self.save_session(app_name, exe_path, start_time, time.time())
       
       print("All sessions saved.")
       sys.exit(0)
   
   def list_apps(self):
       """List monitored applications"""
       if not self.known_apps:
           print("No applications being monitored.")
           return
       
       print("Monitored applications:")
       print("-" * 40)
       for exe_path, app_name in sorted(self.known_apps.items(), key=lambda x: x[1]):
           print(f"{app_name}: {exe_path}")
   
   def add_app(self, name, exe_path):
       """Add an app to monitor"""
       # Normalize path
       exe_path = exe_path.lower()
       
       # Load data
       data = {}
       if self.data_file.exists():
           with open(self.data_file, 'r') as f:
               data = json.load(f)
       
       # Add entry
       if name not in data:
           data[name] = {
               "path": exe_path,
               "total_time": 0,
               "sessions": []
           }
           
           # Save
           with open(self.data_file, 'w') as f:
               json.dump(data, f, indent=2)
           
           print(f"Added {name} for monitoring")
       else:
           print(f"{name} already exists")

def main():
   """Main entry point"""
   if len(sys.argv) > 1:
       passive = MLPassive()
       
       if sys.argv[1] in ['-h', '--help']:
           print("MLQuietrack - Passive Process Tracker")
           print("\nUsage:")
           print("  mlquietrack              - Start monitoring")
           print("  mlquietrack --list       - List monitored apps")
           print("  mlquietrack --add <name> <exe_path> - Add app to monitor")
           print("\nExamples:")
           print("  mlquietrack")
           print("  mlquietrack --list")
           print("  mlquietrack --add Doom C:/Games/Doom/doom.exe")
           sys.exit(0)
           
       elif sys.argv[1] == '--list':
           passive.list_apps()
           
       elif sys.argv[1] == '--add' and len(sys.argv) >= 4:
           name = sys.argv[2]
           exe_path = ' '.join(sys.argv[3:])
           passive.add_app(name, exe_path)
           
       else:
           print("Invalid arguments. Use --help for usage.")
           sys.exit(1)
   else:
       # Default: start monitoring
       passive = MLPassive()
       passive.run()

if __name__ == "__main__":
   main()
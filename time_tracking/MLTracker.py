#!/usr/bin/env python3
"""
MLTracker - Application time tracker
Track how long you spend in any application
Stores data in YOUR json file, not the cloud
"""

import tkinter as tk
import json
import time
import subprocess
import os
from pathlib import Path
from datetime import datetime
import threading
import sys

# ML-style constants
COLORS = {
   'dark_gray': '#3C3C3C',
   'light_gray': '#C0C0C0',
   'green': '#00FF00',
   'red': '#FF0000',
   'white': '#FFFFFF',
   'black': '#000000',
   'blue': '#0000FF',
   'yellow': '#FFFF00'
}

class MLTracker:
   def __init__(self, root, app_name=None, app_path=None):
       self.root = root
       self.root.title("MLTracker")
       self.root.geometry("400x300")
       self.root.configure(bg=COLORS['dark_gray'])
       
       # Data file
       self.data_file = Path.home() / '.config' / 'mltracker' / 'tracked.json'
       self.data_file.parent.mkdir(parents=True, exist_ok=True)
       
       # Current session
       self.app_name = app_name
       self.app_path = app_path
       self.session_start = None
       self.session_duration = 0
       self.tracking = False
       self.process = None
       
       # Load existing data
       self.data = self.load_data()
       
       # Create UI
       self._create_ui()
       
       # Start tracking if app provided
       if self.app_path:
           self.start_tracking()
   
   def load_data(self):
       """Load tracking data"""
       if self.data_file.exists():
           try:
               with open(self.data_file, 'r') as f:
                   return json.load(f)
           except:
               return {}
       return {}
   
   def save_data(self):
       """Save tracking data"""
       with open(self.data_file, 'w') as f:
           json.dump(self.data, f, indent=2)
   
   def _create_ui(self):
       """Create the UI"""
       # Title bar
       title_frame = tk.Frame(self.root, bg=COLORS['light_gray'], 
                             height=40, relief='raised', bd=2)
       title_frame.pack(fill='x')
       title_frame.pack_propagate(False)
       
       title = tk.Label(title_frame, text="MLTracker - Time Tracker",
                       bg=COLORS['green'], fg=COLORS['black'],
                       font=('Courier', 14, 'bold'))
       title.pack(expand=True, fill='both', padx=2, pady=2)
       
       # App info
       if self.app_name:
           info_frame = tk.Frame(self.root, bg=COLORS['dark_gray'])
           info_frame.pack(fill='x', padx=10, pady=10)
           
           tk.Label(info_frame, text=f"Tracking: {self.app_name}",
                   bg=COLORS['dark_gray'], fg=COLORS['white'],
                   font=('Courier', 12)).pack()
       
       # Timer display
       self.timer_label = tk.Label(self.root, text="00:00:00",
                                  bg=COLORS['black'], fg=COLORS['green'],
                                  font=('Courier', 48, 'bold'))
       self.timer_label.pack(expand=True, fill='both', padx=20, pady=20)
       
       # Status
       self.status_label = tk.Label(self.root, text="Ready",
                                   bg=COLORS['dark_gray'], fg=COLORS['yellow'],
                                   font=('Courier', 10))
       self.status_label.pack()
       
       # Buttons
       button_frame = tk.Frame(self.root, bg=COLORS['dark_gray'])
       button_frame.pack(fill='x', padx=10, pady=10)
       
       if not self.app_path:
           # Manual mode
           self.start_btn = tk.Button(button_frame, text="Start",
                                    bg=COLORS['green'], fg=COLORS['black'],
                                    font=('Courier', 12), width=10,
                                    command=self.toggle_tracking)
           self.start_btn.pack(side='left', padx=5)
       
       # Stats button
       tk.Button(button_frame, text="Stats",
                bg=COLORS['light_gray'], fg=COLORS['black'],
                font=('Courier', 12), width=10,
                command=self.show_stats).pack(side='left', padx=5)
       
       # Quit button
       tk.Button(button_frame, text="Quit",
                bg=COLORS['red'], fg=COLORS['white'],
                font=('Courier', 12), width=10,
                command=self.quit).pack(side='right', padx=5)
       
       # Start timer update
       self.update_timer()
       
       # If tracking an app, monitor it
       if self.app_path:
           self.monitor_thread = threading.Thread(target=self.monitor_process, daemon=True)
           self.monitor_thread.start()
   
   def start_tracking(self):
       """Start tracking time"""
       if not self.tracking:
           self.tracking = True
           self.session_start = time.time()
           self.status_label.config(text="Tracking...", fg=COLORS['green'])
           
           # Launch app if path provided
           if self.app_path and not self.process:
               try:
                   self.process = subprocess.Popen(self.app_path)
                   self.status_label.config(text=f"Launched {self.app_name}")
               except Exception as e:
                   self.status_label.config(text=f"Error: {e}", fg=COLORS['red'])
                   self.tracking = False
                   return
           
           if hasattr(self, 'start_btn'):
               self.start_btn.config(text="Stop", bg=COLORS['red'])
   
   def stop_tracking(self):
       """Stop tracking and save session"""
       if self.tracking:
           self.tracking = False
           session_duration = int(time.time() - self.session_start)
           
           # Initialize app entry if needed
           if self.app_name not in self.data:
               self.data[self.app_name] = {
                   "path": self.app_path or "manual",
                   "total_time": 0,
                   "sessions": []
               }
           
           # Add session
           self.data[self.app_name]["sessions"].append({
               "start": datetime.fromtimestamp(self.session_start).isoformat(),
               "duration": session_duration
           })
           self.data[self.app_name]["total_time"] += session_duration
           
           # Save data
           self.save_data()
           
           self.status_label.config(text="Session saved", fg=COLORS['yellow'])
           if hasattr(self, 'start_btn'):
               self.start_btn.config(text="Start", bg=COLORS['green'])
   
   def toggle_tracking(self):
       """Toggle tracking for manual mode"""
       if self.tracking:
           self.stop_tracking()
       else:
           # Ask for app name
           dialog = tk.Toplevel(self.root)
           dialog.title("Track Application")
           dialog.geometry("300x100")
           dialog.configure(bg=COLORS['dark_gray'])
           
           tk.Label(dialog, text="Application name:",
                   bg=COLORS['dark_gray'], fg=COLORS['white'],
                   font=('Courier', 10)).pack(pady=5)
           
           entry = tk.Entry(dialog, font=('Courier', 10))
           entry.pack(pady=5)
           entry.focus()
           
           def start_with_name():
               name = entry.get().strip()
               if name:
                   self.app_name = name
                   self.start_tracking()
                   dialog.destroy()
           
           tk.Button(dialog, text="Start", command=start_with_name,
                    bg=COLORS['green'], fg=COLORS['black'],
                    font=('Courier', 10)).pack(pady=5)
           
           entry.bind('<Return>', lambda e: start_with_name())
   
   def monitor_process(self):
       """Monitor if process is still running"""
       while True:
           if self.process and self.tracking:
               if self.process.poll() is not None:
                   # Process ended
                   self.root.after(0, self.process_ended)
                   break
           time.sleep(1)
   
   def process_ended(self):
       """Handle process ending"""
       self.stop_tracking()
       self.status_label.config(text=f"{self.app_name} closed")
       # Quit after a moment
       self.root.after(2000, self.quit)
   
   def update_timer(self):
       """Update timer display"""
       if self.tracking:
           elapsed = int(time.time() - self.session_start)
           hours = elapsed // 3600
           minutes = (elapsed % 3600) // 60
           seconds = elapsed % 60
           self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
       
       self.root.after(1000, self.update_timer)
   
   def show_stats(self):
       """Show statistics window"""
       stats_window = tk.Toplevel(self.root)
       stats_window.title("MLTracker Stats")
       stats_window.geometry("500x400")
       stats_window.configure(bg=COLORS['dark_gray'])
       
       # Title
       tk.Label(stats_window, text="Application Statistics",
               bg=COLORS['green'], fg=COLORS['black'],
               font=('Courier', 14, 'bold')).pack(fill='x')
       
       # Stats text
       text = tk.Text(stats_window, bg=COLORS['black'], fg=COLORS['green'],
                     font=('Courier', 10), wrap='none')
       text.pack(fill='both', expand=True, padx=10, pady=10)
       
       # Generate stats
       stats = ["APPLICATION TIME TRACKING STATS", "=" * 40, ""]
       
       # Sort by total time
       sorted_apps = sorted(self.data.items(), 
                          key=lambda x: x[1]['total_time'], 
                          reverse=True)
       
       for app_name, app_data in sorted_apps:
           total_seconds = app_data['total_time']
           hours = total_seconds // 3600
           minutes = (total_seconds % 3600) // 60
           
           stats.append(f"{app_name}:")
           stats.append(f"  Total: {hours}h {minutes}m")
           stats.append(f"  Sessions: {len(app_data['sessions'])}")
           
           # Last session
           if app_data['sessions']:
               last = app_data['sessions'][-1]
               last_date = datetime.fromisoformat(last['start']).strftime('%Y-%m-%d %H:%M')
               stats.append(f"  Last: {last_date}")
           
           stats.append("")
       
       text.insert('1.0', '\n'.join(stats))
       text.config(state='disabled')

   def quit(self):
       """Quit the application"""
       if self.tracking:
           self.stop_tracking()
       self.root.quit()

def main():
    """Main entry point"""
    
    # Check for stats flag
    show_gui = '--stats' in sys.argv
    if show_gui:
        sys.argv.remove('--stats')
    
    # Parse remaining args
    if len(sys.argv) > 1:
        # Check if it's a help request
        if sys.argv[1] in ['-h', '--help', '/?']:
            print("MLTracker - Application Time Tracker")
            print("\nUsage:")
            print("  mltracker                    - Manual tracking mode (GUI)")
            print("  mltracker <name> <path>      - Track specific app")
            print("  mltracker <path>             - Track app (uses filename as name)")
            print("  mltracker --stats            - Show GUI with stats")
            print("\nExamples:")
            print("  mltracker Doom G:/Doom/dsda-doom.exe")
            print("  mltracker G:/Doom/dsda-doom.exe --stats")
            sys.exit(0)
        
        # Track specific app
        if len(sys.argv) >= 3:
            app_name = sys.argv[1]
            app_path = ' '.join(sys.argv[2:])
        else:
            # Single argument - it's a path
            app_path = sys.argv[1]
            app_name = Path(app_path).stem
        
        if show_gui:
            # Show GUI
            root = tk.Tk()
            tracker = MLTracker(root, app_name, app_path)
            root.mainloop()
        else:
            # Just launch and track silently
            print(f"Tracking {app_name}...")
            try:
                process = subprocess.Popen(app_path)
                start_time = time.time()
                process.wait()  # Wait for it to finish
                duration = int(time.time() - start_time)
                
                # Save to JSON
                data_file = Path.home() / '.config' / 'mltracker' / 'tracked.json'
                data_file.parent.mkdir(parents=True, exist_ok=True)
                
                data = {}
                if data_file.exists():
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                
                if app_name not in data:
                    data[app_name] = {
                        "path": app_path,
                        "total_time": 0,
                        "sessions": []
                    }
                
                data[app_name]["sessions"].append({
                    "start": datetime.fromtimestamp(start_time).isoformat(),
                    "duration": duration
                })
                data[app_name]["total_time"] += duration
                
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"Session tracked: {duration//3600}h {(duration%3600)//60}m {duration%60}s")
                
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
    else:
        # No args - show GUI for manual mode
        root = tk.Tk()
        tracker = MLTracker(root)
        root.mainloop()

if __name__ == "__main__":
    main()
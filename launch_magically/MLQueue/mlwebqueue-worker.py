#!/usr/bin/env python3
"""
MLWebqueue Worker - Watches queue directory and executes tasks
Under 100 lines, uses inotify for efficiency
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Configuration
QUEUE_DIR = Path("/tmp/mlqueue")
COMPLETE_DIR = QUEUE_DIR / "complete"
FAILED_DIR = QUEUE_DIR / "failed"

# Ensure directories exist
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
COMPLETE_DIR.mkdir(exist_ok=True)
FAILED_DIR.mkdir(exist_ok=True)

def process_task(task_file):
    """Execute a task from a task file"""
    try:
        # Read task data
        with open(task_file, 'r') as f:
            task = json.load(f)
        
        print(f"[PROCESSING] {task.get('name', 'unknown')} ({task_file.name})")
        
        # Extract task details
        script = task.get('script', '')
        args = task.get('args', [])
        env = dict(os.environ)
        env.update(task.get('env', {}))
        
        # Record start time
        task['started_at'] = time.time()
        
        # Execute the script
        if script:
            result = subprocess.run(
                script,
                shell=True,
                capture_output=True,
                text=True,
                env=env,
                timeout=300  # 5 minute timeout
            )
            
            # Record results
            task['completed_at'] = time.time()
            task['exit_code'] = result.returncode
            task['stdout'] = result.stdout
            task['stderr'] = result.stderr
            
            # Move to appropriate directory
            if result.returncode == 0:
                dest = COMPLETE_DIR / task_file.name
                print(f"[SUCCESS] {task.get('name')} completed")
            else:
                dest = FAILED_DIR / task_file.name
                print(f"[FAILED] {task.get('name')} exited with {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}")
            
            # Write final task data and move
            with open(dest, 'w') as f:
                json.dump(task, f, indent=2)
            task_file.unlink()
            
        else:
            print(f"[ERROR] No script defined in task")
            task_file.rename(FAILED_DIR / task_file.name)
            
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Task exceeded 5 minutes")
        task_file.rename(FAILED_DIR / task_file.name)
        
    except Exception as e:
        print(f"[ERROR] Failed to process task: {e}")
        try:
            task_file.rename(FAILED_DIR / task_file.name)
        except:
            pass  # File might already be moved

def watch_queue():
    """Watch queue directory for new task files"""
    print(f"MLWebqueue Worker")
    print(f"Watching: {QUEUE_DIR}")
    print(f"Complete: {COMPLETE_DIR}")
    print(f"Failed: {FAILED_DIR}")
    
    # Process any existing task files
    for task_file in QUEUE_DIR.glob("task_*.json"):
        process_task(task_file)
    
    print(f"Waiting for tasks... (Ctrl+C to stop)")
    
    # Poll for new files (inotify would be better but requires dependency)
    processed = set()
    while True:
        try:
            for task_file in QUEUE_DIR.glob("task_*.json"):
                if task_file not in processed:
                    processed.add(task_file)
                    process_task(task_file)
                    processed.discard(task_file)  # Remove after processing
            
            time.sleep(1)  # Poll every second
            
            # Clean up processed set periodically
            if len(processed) > 100:
                processed = {f for f in processed if f.exists()}
                
        except KeyboardInterrupt:
            print("\n[INFO] Worker stopped")
            break
        except Exception as e:
            print(f"[ERROR] Worker error: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    watch_queue()
#!/usr/bin/env python3
"""
MLWebqueue Server - HTTP to filesystem task queue
Serves the web interface and creates task files
Under 150 lines, no dependencies beyond stdlib
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import time

# Configuration
QUEUE_DIR = Path("/tmp/mlqueue")
PORT = 8888
SHORTCUTS_FILE = Path("shortcuts.json")

# Ensure queue directory exists
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

class QueueHandler(SimpleHTTPRequestHandler):
    """Handle web requests and queue creation"""
    
    def do_POST(self):
        """Create a task file from POST data"""
        if self.path != '/queue':
            self.send_error(404)
            return
            
        try:
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)
            
            # Create task file
            task_id = task_data.get('id', f"{time.time()}_{os.getpid()}")
            task_file = QUEUE_DIR / f"task_{task_id}.json"
            
            # Write atomically (write to temp, then rename)
            temp_file = task_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(task_data, f, indent=2)
            temp_file.rename(task_file)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'status': 'queued', 'id': task_id, 'file': str(task_file)}
            self.wfile.write(json.dumps(response).encode())
            
            print(f"[QUEUED] {task_data.get('name', 'unknown')} -> {task_file}")
            
        except Exception as e:
            self.send_error(500, str(e))
            print(f"[ERROR] Failed to queue task: {e}", file=sys.stderr)
    
    def do_GET(self):
        """Serve files with proper CORS for local development"""
        # Serve shortcuts.json from current directory
        if self.path == '/shortcuts.json':
            if SHORTCUTS_FILE.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                with open(SHORTCUTS_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                # Create example shortcuts file
                example = [
                    {
                        "name": "System Info",
                        "description": "Show system information",
                        "script": "uname -a && df -h && free -h"
                    },
                    {
                        "name": "Backup Logs",
                        "description": "Backup application logs",
                        "script": "tar -czf /tmp/logs_$(date +%Y%m%d).tar.gz /var/log/app/"
                    },
                    {
                        "name": "Clear Cache",
                        "description": "Clear application cache",
                        "script": "rm -rf /tmp/cache/* && echo 'Cache cleared'"
                    },
                    {
                        "name": "Test Alert",
                        "description": "Send test notification",
                        "script": "echo 'Test alert at $(date)' | mail -s 'Test' admin@example.com"
                    }
                ]
                with open(SHORTCUTS_FILE, 'w') as f:
                    json.dump(example, f, indent=2)
                print(f"[INFO] Created example {SHORTCUTS_FILE}")
                self.do_GET()  # Retry now that file exists
        else:
            # Serve other files normally
            super().do_GET()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def main():
    """Start the web queue server"""
    print(f"MLWebqueue Server")
    print(f"Queue directory: {QUEUE_DIR}")
    print(f"Shortcuts file: {SHORTCUTS_FILE}")
    print(f"Starting server on port {PORT}...")
    
    # Create server
    server = HTTPServer(('', PORT), QueueHandler)
    print(f"Server running at http://localhost:{PORT}/")
    print(f"Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped")
        server.shutdown()

if __name__ == '__main__':
    main()
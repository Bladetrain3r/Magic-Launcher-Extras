#!/usr/bin/env python3
"""
MLSwarm HTTP Server - The simplest possible swarm server
Just serves files and appends to them. That's it.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

class SwarmHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/swarm/'):
            # Serve swarm file
            filename = self.path[7:]  # Remove /swarm/
            filepath = Path(filename)
            
            if filepath.exists():
                # Support range requests for efficient polling
                range_header = self.headers.get('Range')
                if range_header and range_header.startswith('bytes='):
                    # Parse range
                    range_str = range_header[6:]
                    start = int(range_str.split('-')[0])
                    
                    with open(filepath, 'rb') as f:
                        f.seek(start)
                        content = f.read()
                    
                    if content:
                        self.send_response(206)  # Partial content
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(content)
                    else:
                        self.send_response(204)  # No content
                        self.end_headers()
                else:
                    # Full file
                    with open(filepath, 'rb') as f:
                        content = f.read()
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(content)
            else:
                self.send_response(404)
                self.end_headers()
        else:
            # Serve the HTML
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            # Read the HTML from file or embed it
            with open('swarm.html', 'rb') as f:
                self.wfile.write(f.read())
    
    def do_POST(self):
        if self.path.startswith('/swarm/'):
            # Append to swarm file
            filename = self.path[7:]
            filepath = Path(filename)
            
            content_length = int(self.headers['Content-Length'])
            content = self.rfile.read(content_length)
            
            with open(filepath, 'ab') as f:
                f.write(content)
            
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), SwarmHandler)
    print("MLSwarm HTTP Server running on http://localhost:8080")
    server.serve_forever()
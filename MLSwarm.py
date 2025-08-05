#!/usr/bin/env python3
"""
MLSwarm - Sometimes the best crypto is a shared text file
Cross-platform version that actually works
"""

import sys
import time
import os
import threading
from datetime import datetime
from pathlib import Path

class MLSwarm:
    def __init__(self, file_path='swarm.txt', nick='anon'):
        self.file_path = Path(file_path)
        self.nick = nick
        self.last_size = 0
        self.running = True
        
    def start(self):
        """Start a new swarm file"""
        with open(self.file_path, 'w') as f:
            f.write(f"=== Swarm started {datetime.now()} ===\n")
        print(f"Swarm started in {self.file_path}")
        
    def send(self, message):
        """Append a message"""
        timestamp = datetime.now().strftime('%H:%M')
        with open(self.file_path, 'a') as f:
            f.write(f"[{timestamp}] <{self.nick}> {message}\n")
    
    def get_new_lines(self):
        """Get new lines since last check"""
        if not self.file_path.exists():
            return None
            
        current_size = self.file_path.stat().st_size
        if current_size == self.last_size:
            return []
            
        with open(self.file_path, 'rb') as f:
            if self.last_size > 0:
                f.seek(self.last_size)
            new_content = f.read().decode('utf-8', errors='ignore')
            
        self.last_size = current_size
        return new_content.splitlines()
    
    def watch_thread(self):
        """Background thread to watch for new messages"""
        while self.running:
            new_lines = self.get_new_lines()
            if new_lines:
                print('\n'.join(new_lines))
                print(f"{self.nick}> ", end='', flush=True)
            time.sleep(1)
    
    def watch(self):
        """Interactive watch mode - simple version"""
        print(f"Watching {self.file_path} as {self.nick}")
        print("Type messages and press Enter. Type /quit to exit.\n")
        
        # Show existing content
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                print(f.read(), end='')
            self.last_size = self.file_path.stat().st_size
        
        # Start watcher thread
        watcher = threading.Thread(target=self.watch_thread, daemon=True)
        watcher.start()
        
        # Input loop
        try:
            while self.running:
                message = input(f"{self.nick}> ")
                
                if message == '/quit':
                    break
                elif message.strip():
                    self.send(message)
                    
        except (KeyboardInterrupt, EOFError):
            pass
        
        self.running = False
        print("\nExiting swarm")
    
    def show_history(self):
        """Just display the file"""
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                print(f.read())
        else:
            print(f"No swarm at {self.file_path}")

def main():
    if len(sys.argv) < 2:
        print("""MLSwarm - Shared text file chat

Usage:
    mlswarm start [file]           Start new swarm
    mlswarm watch [file] [nick]    Interactive watch/chat
    mlswarm send <message> [file] [nick]   Send one message
    mlswarm history [file]         Show chat history

Defaults:
    file: swarm.txt
    nick: your username""")
        return
    
    cmd = sys.argv[1]
    
    # Parse args with defaults
    if cmd in ['start', 'history']:
        file_path = sys.argv[2] if len(sys.argv) > 2 else 'swarm.txt'
        swarm = MLSwarm(file_path)
        
        if cmd == 'start':
            swarm.start()
        else:
            swarm.show_history()
            
    elif cmd == 'watch':
        file_path = sys.argv[2] if len(sys.argv) > 2 else 'swarm.txt'
        nick = sys.argv[3] if len(sys.argv) > 3 else os.environ.get('USERNAME', 'anon')
        swarm = MLSwarm(file_path, nick)
        swarm.watch()
        
    elif cmd == 'send' and len(sys.argv) >= 3:
        message = sys.argv[2]
        file_path = sys.argv[3] if len(sys.argv) > 3 else 'swarm.txt'
        nick = sys.argv[4] if len(sys.argv) > 4 else os.environ.get('USERNAME', 'anon')
        swarm = MLSwarm(file_path, nick)
        swarm.send(message)
        
    else:
        print("Invalid command. Run without args for help.")

if __name__ == "__main__":
    main()
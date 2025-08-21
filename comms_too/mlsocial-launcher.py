#!/usr/bin/env python3
"""
MLSocial - Social media that's just file sharing
Run alongside Magic Launcher or standalone
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

class MLSocial:
    def __init__(self):
        self.base = Path.home() / '.mlsocial'
        self.posts = self.base / 'posts'
        self.friends = self.base / 'friends'
        self.config = self.base / 'config.json'
        
        # Create structure
        self.posts.mkdir(parents=True, exist_ok=True)
        self.friends.mkdir(exist_ok=True)
        
        # Load or create config
        if self.config.exists():
            with open(self.config) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "username": os.environ.get('USER', 'anon'),
                "following": [],
                "server": None
            }
            self.save_config()
    
    def save_config(self):
        with open(self.config, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def post(self, content, type='text'):
        """Create a post (just write a file)"""
        timestamp = int(time.time())
        filename = f"{timestamp}.{type}"
        
        post_data = {
            "author": self.data['username'],
            "time": timestamp,
            "type": type,
            "content": content
        }
        
        with open(self.posts / filename, 'w') as f:
            json.dump(post_data, f)
        
        return filename
    
    def timeline(self, limit=20):
        """Read timeline (just read files)"""
        all_posts = []
        
        # Read own posts
        for post_file in self.posts.glob('*.*'):
            try:
                with open(post_file) as f:
                    post = json.load(f)
                    all_posts.append(post)
            except:
                pass
        
        # Read friends' posts
        for friend in self.friends.iterdir():
            if friend.is_dir():
                for post_file in (friend / 'posts').glob('*.*'):
                    try:
                        with open(post_file) as f:
                            post = json.load(f)
                            all_posts.append(post)
                    except:
                        pass
        
        # Sort by time, return recent
        all_posts.sort(key=lambda x: x.get('time', 0), reverse=True)
        return all_posts[:limit]
    
    def follow(self, username, server=None):
        """Follow someone (just create a directory)"""
        friend_dir = self.friends / username
        friend_dir.mkdir(exist_ok=True)
        (friend_dir / 'posts').mkdir(exist_ok=True)
        
        if username not in self.data['following']:
            self.data['following'].append(username)
            self.save_config()
        
        if server:
            # Save server info for sync
            with open(friend_dir / 'server.txt', 'w') as f:
                f.write(server)
    
    def sync(self):
        """Sync with friends (just rsync/copy files)"""
        for friend in self.data['following']:
            friend_dir = self.friends / friend
            server_file = friend_dir / 'server.txt'
            
            if server_file.exists():
                with open(server_file) as f:
                    server = f.read().strip()
                
                # In real implementation: rsync or http get
                cmd = f"rsync -q {server}/.mlsocial/posts/* {friend_dir}/posts/ 2>/dev/null"
                os.system(cmd)
    
    def generate_shortcuts(self):
        """Generate Magic Launcher shortcuts for social features"""
        shortcuts = {
            "shortcuts": [
                {
                    "name": "📝 Post Status",
                    "command": f"python3 -c \"from mlsocial import *; MLSocial().post(input('Status: '))\""
                },
                {
                    "name": "📰 View Timeline",
                    "command": "python3 -m mlsocial timeline"
                },
                {
                    "name": "👥 Follow Friend",
                    "command": f"python3 -c \"from mlsocial import *; MLSocial().follow(input('Username: '))\""
                },
                {
                    "name": "🔄 Sync Network",
                    "command": "python3 -m mlsocial sync"
                }
            ]
        }
        
        # Add shortcuts for each friend
        for friend in self.data['following']:
            shortcuts['shortcuts'].append({
                "name": f"💬 {friend}",
                "command": f"ls -la ~/.mlsocial/friends/{friend}/posts/ | tail -10",
                "folder": "Friends"
            })
        
        return shortcuts
    
    def cli(self):
        """Simple CLI interface"""
        import sys
        
        if len(sys.argv) < 2:
            self.show_timeline()
            return
        
        cmd = sys.argv[1]
        
        if cmd == 'post':
            content = input("What's on your mind? ")
            self.post(content)
            print("Posted!")
        
        elif cmd == 'timeline':
            self.show_timeline()
        
        elif cmd == 'follow':
            username = input("Username: ")
            server = input("Server (optional): ").strip() or None
            self.follow(username, server)
            print(f"Following {username}!")
        
        elif cmd == 'sync':
            self.sync()
            print("Synced!")
        
        elif cmd == 'shortcuts':
            # Output shortcuts for Magic Launcher
            print(json.dumps(self.generate_shortcuts(), indent=2))
    
    def show_timeline(self):
        """Display timeline in terminal"""
        posts = self.timeline()
        
        if not posts:
            print("No posts yet. Be the first!")
            return
        
        print("\n=== TIMELINE ===\n")
        for post in posts:
            author = post.get('author', 'unknown')
            content = post.get('content', '')
            timestamp = post.get('time', 0)
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            
            print(f"[{author} @ {date}]")
            print(f"{content}\n")
            print("-" * 40)

def main():
    social = MLSocial()
    social.cli()

if __name__ == "__main__":
    main()
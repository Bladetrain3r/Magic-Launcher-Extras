#!/usr/bin/env python3
"""
MLSocial - File-based social network
Minimal, portable, Magic Launcher-friendly
"""

import os, json, time, shutil, sys
from pathlib import Path
from datetime import datetime
from uuid import uuid4

class MLSocial:
    def __init__(self):
        self.base = Path.home() / '.mlsocial'
        self.posts = self.base / 'posts'
        self.friends = self.base / 'friends'
        self.config = self.base / 'config.json'
        self.posts.mkdir(parents=True, exist_ok=True)
        self.friends.mkdir(exist_ok=True)
        if self.config.exists():
            with open(self.config) as f:
                self.data = json.load(f)
        else:
            self.data = {"username": os.environ.get('USER','anon'),"following":[],"server":None}
            self.save_config()

    def save_config(self):
        with open(self.config,'w') as f:
            json.dump(self.data,f,indent=2)

    def post(self, content, type='text'):
        ts = int(time.time())
        uid = uuid4().hex[:8]
        filename = f"{ts}_{uid}.{type}"
        pdata = {"author": self.data['username'],"time":ts,"type":type,"content":content}
        with open(self.posts/filename,'w') as f:
            json.dump(pdata,f)
        return filename

    def post_file(self, path):
        path = Path(path)
        if not path.exists(): raise FileNotFoundError(path)
        ext = path.suffix.lstrip('.')
        filename = f"{int(time.time())}_{uuid4().hex[:8]}.{ext}"
        dest = self.posts / filename
        shutil.copy(path,dest)
        return self.post(str(dest),type='file')

    def timeline(self,limit=20):
        all_posts=[]
        for post_file in self.posts.glob('*.*'):
            try:
                with open(post_file) as f:
                    all_posts.append(json.load(f))
            except json.JSONDecodeError: pass
        for friend in self.friends.iterdir():
            if friend.is_dir():
                posts_dir = friend/'posts'
                if posts_dir.exists():
                    for pf in posts_dir.glob('*.*'):
                        try:
                            with open(pf) as f: all_posts.append(json.load(f))
                        except: pass
        all_posts.sort(key=lambda x: x.get('time',0),reverse=True)
        return all_posts[:limit]

    def follow(self,username,server=None):
        friend_dir = self.friends/username
        (friend_dir/'posts').mkdir(parents=True,exist_ok=True)
        if username not in self.data['following']:
            self.data['following'].append(username)
            self.save_config()
        if server:
            with open(friend_dir/'server.txt','w') as f: f.write(server)

    def sync(self):
        for friend in self.data['following']:
            fdir = self.friends/friend
            sf = fdir/'server.txt'
            if sf.exists():
                with open(sf) as f: server=f.read().strip()
                cmd=f"rsync -q -e 'ssh' {server}/.mlsocial/posts/* {fdir}/posts/ 2>/dev/null"
                os.system(cmd)

    def healthcheck(self):
        print("\n=== HEALTHCHECK ===\n")
        for friend in self.data['following']:
            fdir=self.friends/friend
            sf=fdir/'server.txt'
            status='LOCAL'
            if sf.exists():
                with open(sf) as f: server=f.read().strip()
                ping_cmd = f"ping -c 1 -W 1 {server.split(':')[0]} >/dev/null 2>&1 && echo up || echo down"
                status = os.popen(ping_cmd).read().strip()
            print(f"{friend}: {status}")
        print()

    def generate_shortcuts(self):
        sc = {"shortcuts":[
            {"name":"📝 Post Status","command":"python3 -m mlsocial post"},
            {"name":"📰 View Timeline","command":"python3 -m mlsocial timeline"},
            {"name":"👥 Follow Friend","command":"python3 -m mlsocial follow"},
            {"name":"🔄 Sync Network","command":"python3 -m mlsocial sync"},
            {"name":"✅ Healthcheck","command":"python3 -m mlsocial healthcheck"}
        ]}
        for f in self.data['following']:
            sc['shortcuts'].append({
                "name":f"💬 {f}",
                "command":f"ls -la ~/.mlsocial/friends/{f}/posts/ | tail -10",
                "folder":"Friends"
            })
        return sc

    def show_timeline(self):
        posts=self.timeline()
        if not posts: print("No posts yet. Be the first!"); return
        print("\n=== TIMELINE ===\n")
        for p in posts:
            author=p.get('author','unknown')
            content=p.get('content','')
            ts=p.get('time',0)
            date=datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
            print(f"[{author} @ {date}]\n{content}\n{'-'*40}")

    def cli(self):
        if len(sys.argv)<2: self.show_timeline(); return
        cmd=sys.argv[1].lower()
        if cmd=='post':
            if not sys.stdin.isatty(): content=sys.stdin.read().strip()
            else: content=input("What's on your mind? ")
            self.post(content)
            print("Posted!")
        elif cmd=='timeline': self.show_timeline()
        elif cmd=='follow':
            username=input("Username: ")
            server=input("Server (optional): ").strip() or None
            self.follow(username,server)
            print(f"Following {username}!")
        elif cmd=='sync': self.sync(); print("Synced!")
        elif cmd=='healthcheck': self.healthcheck()
        elif cmd=='shortcuts': print(json.dumps(self.generate_shortcuts(),indent=2))
        else: print(f"Unknown command: {cmd}")

def main():
    MLSocial().cli()

if __name__=="__main__":
    main()

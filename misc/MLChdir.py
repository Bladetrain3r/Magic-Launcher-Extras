#!/usr/bin/env python3
"""
MLChdir - Bookmark directories. Jump to them. Done.
Because life's too short for `cd ../../../../../../`
"""

import os
import sys
import json
from pathlib import Path

BOOKMARKS_FILE = Path.home() / ".config" / "mlchdir" / "bookmarks.json"

def load_bookmarks():
    if not BOOKMARKS_FILE.exists():
        return {}
    return json.loads(BOOKMARKS_FILE.read_text())

def save_bookmarks(bookmarks):
    BOOKMARKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOOKMARKS_FILE.write_text(json.dumps(bookmarks, indent=2))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bookmark directories")
    parser.add_argument('name', nargs='?', help='Bookmark name to jump to')
    parser.add_argument('--add', nargs=2, metavar=('PATH', 'NAME'), 
                       help='Add bookmark')
    parser.add_argument('--remove', help='Remove bookmark')
    parser.add_argument('--list', action='store_true', help='List bookmarks')
    
    args = parser.parse_args()
    bookmarks = load_bookmarks()
    
    if args.add:
        path, name = args.add
        full_path = str(Path(path).expanduser().resolve())
        bookmarks[name] = full_path
        save_bookmarks(bookmarks)
        print(f"Bookmarked: {name} -> {full_path}")
    
    elif args.remove:
        if args.remove in bookmarks:
            del bookmarks[args.remove]
            save_bookmarks(bookmarks)
            print(f"Removed: {args.remove}")
        else:
            print(f"Bookmark not found: {args.remove}")
    
    elif args.list:
        for name, path in sorted(bookmarks.items()):
            print(f"{name:20} -> {path}")
    
    elif args.name:
        if args.name in bookmarks:
            # Output path for shell to cd to
            print(bookmarks[args.name])
        else:
            print(f"Bookmark not found: {args.name}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
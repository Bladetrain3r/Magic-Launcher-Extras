#!/usr/bin/env python3
"""
MLSize - Shows you where the fat bastards hide
Because you don't need permissions, you need to know what's eating your disk
"""

import os
import sys
from pathlib import Path

def human_size(bytes):
    """Convert bytes to human readable"""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if bytes < 1024.0:
            return f"{bytes:6.1f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.1f}P"  # Petabytes, because why not

def get_sizes(path='.', min_size=0, show_hidden=False):
    """Get all file sizes, sorted by fatness"""
    sizes = []
    
    try:
        for root, dirs, files in os.walk(path):
            # Skip hidden dirs unless asked
            if not show_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if not show_hidden and file.startswith('.'):
                    continue
                    
                filepath = Path(root) / file
                try:
                    size = filepath.stat().st_size
                    if size >= min_size:
                        sizes.append((size, str(filepath)))
                except:
                    pass  # File disappeared or permission denied, who cares
    except:
        pass  # Directory not readable, move on
    
    return sorted(sizes, reverse=True)

def show_dir_sizes(path='.'):
    """Show directory sizes too"""
    sizes = []
    
    for item in Path(path).iterdir():
        if item.is_dir():
            total = 0
            for root, dirs, files in os.walk(item):
                for file in files:
                    try:
                        total += (Path(root) / file).stat().st_size
                    except:
                        pass
            sizes.append((total, f"{item}/", True))  # True = directory
        else:
            try:
                sizes.append((item.stat().st_size, str(item), False))
            except:
                pass
    
    return sorted(sizes, reverse=True)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find the fat bastards eating your disk"
    )
    parser.add_argument('path', nargs='?', default='.', 
                       help='Path to analyze (default: current dir)')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Descend into subdirectories')
    parser.add_argument('-d', '--dirs', action='store_true',
                       help='Show directory sizes (current level only)')
    parser.add_argument('-n', '--number', type=int, default=20,
                       help='Number of items to show (default: 20)')
    parser.add_argument('-m', '--min-size', type=str, default='0',
                       help='Minimum size to show (e.g., 1M, 100K)')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Include hidden files')
    parser.add_argument('-t', '--total', action='store_true',
                       help='Show total size at the end')
    
    args = parser.parse_args()
    
    # Parse min size
    min_size = 0
    if args.min_size != '0':
        size_str = args.min_size.upper()
        multiplier = 1
        if size_str.endswith('K'):
            multiplier = 1024
            size_str = size_str[:-1]
        elif size_str.endswith('M'):
            multiplier = 1024 * 1024
            size_str = size_str[:-1]
        elif size_str.endswith('G'):
            multiplier = 1024 * 1024 * 1024
            size_str = size_str[:-1]
        try:
            min_size = float(size_str) * multiplier
        except:
            print(f"Invalid size: {args.min_size}")
            sys.exit(1)
    
    # Get the sizes
    if args.dirs:
        sizes = show_dir_sizes(args.path)
        total = 0
        for i, (size, name, is_dir) in enumerate(sizes[:args.number]):
            total += size
            marker = "/" if is_dir else ""
            print(f"{human_size(size)} {name}{marker}")
    else:
        if args.recursive:
            sizes = get_sizes(args.path, min_size, args.all)
        else:
            # Just current directory
            sizes = []
            for item in Path(args.path).iterdir():
                if not args.all and item.name.startswith('.'):
                    continue
                if item.is_file():
                    try:
                        size = item.stat().st_size
                        if size >= min_size:
                            sizes.append((size, item.name))
                    except:
                        pass
            sizes.sort(reverse=True)
        
        # Display
        total = 0
        for i, (size, name) in enumerate(sizes[:args.number]):
            total += size
            print(f"{human_size(size)} {name}")
        
        if args.total and sizes:
            print("-" * 40)
            print(f"{human_size(total)} Total shown")
            if len(sizes) > args.number:
                full_total = sum(s for s, _ in sizes)
                print(f"{human_size(full_total)} Total found")
                print(f"({len(sizes) - args.number} more files not shown)")

if __name__ == '__main__':
    main()
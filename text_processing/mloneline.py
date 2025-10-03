#!/usr/bin/env python3
"""
MLOneline - Strips all newline characters, returns single line
Created in honor of Azure Pipeline Variables' inability to handle multiline values
Because sometimes, enterprise platforms fail at the simplest things

Usage: mloneline < input.txt
       echo -e "multi\nline\ntext" | mloneline
       mloneline file.txt
"""

import sys

def strip_newlines(text):
    """Remove all newline characters, return single line"""
    return text.replace('\n', '').replace('\r', '')

def main():
    if len(sys.argv) > 1:
        # Read from file
        try:
            with open(sys.argv[1], 'r') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        text = sys.stdin.read()
    
    # Strip newlines and output
    result = strip_newlines(text)
    print(result)

if __name__ == "__main__":
    main()

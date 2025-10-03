#!/usr/bin/env python3
"""
MLNonul.py - Forces UTF-8 encoding and removes invalid characters
Usage: python3 MLNonul.py <filename>
"""

import sys
import os

def clean_file(filepath):
    """
    Read file with error handling, keep only valid UTF-8 chars, write back
    """
    # Read the file in binary mode first
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Decode with 'ignore' to skip invalid bytes
    text = raw_data.decode('utf-8', errors='ignore')
    
    # Additional cleaning - remove null bytes and other control chars
    # Keep tabs, newlines, and carriage returns
    cleaned = ''.join(char for char in text 
                     if char == '\t' or char == '\n' or char == '\r' 
                     or (ord(char) >= 32 and ord(char) != 127))
    
    # Create backup (optional - comment out if not wanted)
    backup_path = f"{filepath}.bak"
    try:
        with open(backup_path, 'wb') as f:
            f.write(raw_data)
    except:
        pass  # Backup failed, continue anyway
    
    # Write cleaned content back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        # Report what we did
        original_size = len(raw_data)
        cleaned_size = len(cleaned.encode('utf-8'))
        removed = original_size - cleaned_size
        
        if removed > 0:
            print(f"✓ {filepath}: Removed {removed} bytes of invalid/control chars")
        else:
            print(f"✓ {filepath}: Already clean")
        
        return True
        
    except Exception as e:
        print(f"Error writing cleaned file: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 MLNonul.py <filename>")
        print("       python3 MLNonul.py *.txt  (with shell expansion)")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Handle wildcards if shell didn't expand them
    if '*' in filepath:
        print("Error: Wildcard not expanded. Use shell expansion or loop:")
        print("  for f in *.txt; do python3 MLNonul.py \"$f\"; done")
        sys.exit(1)
    
    success = clean_file(filepath)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
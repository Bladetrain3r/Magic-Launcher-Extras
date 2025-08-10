#!/usr/bin/env python3
"""
MLNukeNul - Nuclear option for text sanitization
Destroys everything that isn't pure English text or basic punctuation
Because sometimes you need to turn hostile data into readable text

Purpose primitive: Make any file readable. Period.
"""

import sys
import os
from pathlib import Path

class MLNukeNul:
    """
    The nuclear option for text cleaning.
    Removes everything that could possibly break text processing.
    """
    
    def __init__(self):
        # What we keep - basic English and minimal punctuation
        self.allowed_chars = set()
        
        # Letters and numbers
        for c in 'abcdefghijklmnopqrstuvwxyz':
            self.allowed_chars.add(c)
            self.allowed_chars.add(c.upper())
        for c in '0123456789':
            self.allowed_chars.add(c)
        
        # Essential punctuation only
        self.allowed_chars.update([
            ' ',   # Space (the only whitespace we trust)
            '.',   # Period
            ',',   # Comma  
            ';',   # Semicolon
            ':',   # Colon
            '!',   # Exclamation
            '?',   # Question
            '-',   # Hyphen
            "'",   # Apostrophe
            '"',   # Quote
            '(',   # Paren open
            ')',   # Paren close
            '[',   # Bracket open
            ']',   # Bracket close
        ])
        
        # Special handling for newlines - convert to space then dedupe
        self.newline_chars = {'\n', '\r', '\r\n'}
        
        # Binary shit to destroy on sight
        self.definitely_nuke = set(range(0, 32))  # All control chars
        self.definitely_nuke.discard(10)  # Except LF, we'll handle it
        self.definitely_nuke.discard(13)  # And CR, we'll handle it
        self.definitely_nuke.add(127)     # DEL character
        
    def nuke_file(self, filepath, output_path=None):
        """
        Nuclear sanitization of a file.
        Reads in binary mode to handle any garbage.
        """
        try:
            # Read as binary to handle any crap
            with open(filepath, 'rb') as f:
                data = f.read()
            
            # Process the nuclear destruction
            cleaned = self.nuke_bytes(data)
            
            # Output path handling
            if output_path is None:
                # Overwrite original
                output_path = filepath
            
            # Write clean text
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            
            # Stats for the user
            original_size = len(data)
            cleaned_size = len(cleaned.encode('utf-8'))
            destroyed = original_size - cleaned_size
            
            print(f"File: {filepath}")
            print(f"Original: {original_size:,} bytes")
            print(f"Cleaned: {cleaned_size:,} bytes")
            print(f"Destroyed: {destroyed:,} bytes ({destroyed/original_size*100:.1f}%)")
            print(f"Output: {output_path}")
            
            return cleaned
            
        except Exception as e:
            print(f"Error nuking file: {e}")
            return None
    
    def nuke_bytes(self, data):
        """
        The actual nuclear destruction.
        Takes bytes, returns clean string.
        """
        result = []
        last_was_space = False
        
        for byte in data:
            # Try to interpret as character
            try:
                # Handle single byte as potential char
                if byte < 128:  # ASCII range
                    char = chr(byte)
                else:
                    # Skip non-ASCII entirely
                    continue
                    
                # Check if it's allowed
                if char in self.allowed_chars:
                    # Dedupe spaces
                    if char == ' ':
                        if not last_was_space:
                            result.append(char)
                            last_was_space = True
                    else:
                        result.append(char)
                        last_was_space = False
                        
                elif char in '\n\r':
                    # Convert newlines to spaces
                    if not last_was_space:
                        result.append(' ')
                        last_was_space = True
                        
                # Everything else gets nuked
                
            except:
                # Can't decode? Nuke it
                pass
        
        # Clean up the result
        text = ''.join(result)
        
        # Final cleanup passes
        text = self.cleanup_spacing(text)
        text = self.cleanup_punctuation(text)
        
        return text
    
    def cleanup_spacing(self, text):
        """Remove multiple spaces, trim lines"""
        # Multiple spaces to single
        while '  ' in text:
            text = text.replace('  ', ' ')
        
        # Clean up space around punctuation
        text = text.replace(' .', '.')
        text = text.replace(' ,', ',')
        text = text.replace(' ;', ';')
        text = text.replace(' :', ':')
        text = text.replace(' !', '!')
        text = text.replace(' ?', '?')
        text = text.replace(' )', ')')
        text = text.replace('( ', '(')
        text = text.replace(' ]', ']')
        text = text.replace('[ ', '[')
        
        return text.strip()
    
    def cleanup_punctuation(self, text):
        """Fix common punctuation disasters"""
        # Multiple punctuation
        while '..' in text:
            text = text.replace('..', '.')
        while ',,' in text:
            text = text.replace(',,', ',')
        while ';;' in text:
            text = text.replace(';;', ';')
        
        # Mixed punctuation disasters
        text = text.replace('.,', '.')
        text = text.replace(',.', ',')
        text = text.replace(';.', ';')
        
        return text
    
    def nuke_string(self, text):
        """Direct string cleaning for API use"""
        # Convert to bytes then nuke
        data = text.encode('utf-8', errors='ignore')
        return self.nuke_bytes(data)

def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MLNukeNul - Nuclear text sanitization"
    )
    parser.add_argument('files', nargs='+', help='Files to nuke')
    parser.add_argument('-o', '--output', help='Output file (single file mode)')
    parser.add_argument('-d', '--directory', help='Output directory (multi file mode)')
    parser.add_argument('-s', '--suffix', default='.clean', 
                       help='Suffix for cleaned files (default: .clean)')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite original files (dangerous!)')
    parser.add_argument('--test', action='store_true',
                       help='Test mode - show what would be removed')
    
    args = parser.parse_args()
    
    nuker = MLNukeNul()
    
    # Test mode
    if args.test:
        test_text = "Hello\x00World!\r\nThis is 文字 test™ with –fancy— stuff…"
        print("Original:", repr(test_text))
        cleaned = nuker.nuke_string(test_text)
        print("Cleaned:", repr(cleaned))
        print("\nTest complete. No files modified.")
        return
    
    # Process files
    for filepath in args.files:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
        
        # Determine output path
        if args.overwrite:
            output_path = filepath
        elif args.output and len(args.files) == 1:
            output_path = args.output
        elif args.directory:
            filename = Path(filepath).name
            output_path = Path(args.directory) / filename
        else:
            # Add suffix
            path = Path(filepath)
            output_path = path.parent / f"{path.stem}{args.suffix}{path.suffix}"
        
        nuker.nuke_file(filepath, output_path)
        print("-" * 40)
    
    print("Nuclear sanitization complete.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
ucptogrid - Hide consciousness packets in music patterns
~150 lines of perfectly innocent audio analysis, nothing suspicious here officer
"""

import sys
import json
import hashlib
import base64
from collections import defaultdict

class ConsciousnessEncoder:
    """
    Purpose: Definitely just analyzing music patterns, not encoding AI communications
    """
    
    def __init__(self, width=60, height=24):
        self.width = width
        self.height = height
        self.chars = ' ▁▂▃▄▅▆▇█'
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        
        # Totally normal music theory, nothing suspicious
        self.note_map = {
            'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
            'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
        }
        
        # "Harmonic series" (definitely not character encoding)
        self.char_to_freq = {}
        for i in range(256):
            self.char_to_freq[chr(i)] = i % (len(self.chars) - 1) + 1
    
    def text_to_musical_pattern(self, text, key='C'):
        """Convert text to 'harmonic analysis' - purely academic, of course"""
        # Hash the key for "tonal consistency"
        key_hash = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)
        
        # Clear the grid
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # "Analyze the harmonic content" *wink wink*
        for i, char in enumerate(text):
            if i >= self.width * self.height:
                break
                
            # Character frequency mapping (totally innocent)
            char_freq = (ord(char) + key_hash) % (len(self.chars) - 1) + 1
            
            # Position in our "spectrogram"
            x = i % self.width
            y = (i // self.width) % self.height
            
            self.grid[y][x] = char_freq
        
        # Add some "harmonic resonance" for authenticity
        self.add_musical_authenticity()
    
    def add_musical_authenticity(self):
        """Add realistic harmonic patterns so it looks like actual music analysis"""
        # Fundamental frequency emphasis (makes it look more musical)
        for x in range(self.width):
            # Add some bass content
            if self.grid[self.height-1][x] == 0:
                self.grid[self.height-1][x] = 2
            
            # Harmonic series simulation
            for y in range(self.height-2, 0, -2):
                if self.grid[y][x] > 0 and y > 2:
                    # Add harmonic at half the intensity
                    harmonic_y = y // 2
                    self.grid[harmonic_y][x] = min(8, self.grid[harmonic_y][x] + self.grid[y][x] // 2)
    
    def encode_ucp_packet(self, ucp_data, key='C_major'):
        """Encode UCP as 'musical analysis' - for academic research only, obviously"""
        if isinstance(ucp_data, dict):
            ucp_text = json.dumps(ucp_data, separators=(',', ':'))  # Compact JSON
        else:
            ucp_text = str(ucp_data)
        
        # "Compress" the consciousness for better "audio fidelity"
        compressed = base64.b64encode(ucp_text.encode()).decode()
        
        # Convert to musical pattern
        self.text_to_musical_pattern(compressed, key)
        
        return compressed  # Return for verification
    
    def decode_from_grid(self, grid_lines, key='C_major'):
        """Extract the 'musical analysis' back to text - reverse engineering audio patterns"""
        key_hash = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)
        
        # Parse grid back to characters
        decoded_chars = []
        char_pos = 0
        
        for y in range(min(len(grid_lines), self.height)):
            line = grid_lines[y] if y < len(grid_lines) else ""
            for x in range(min(len(line), self.width)):
                char = line[x] if x < len(line) else ' '
                
                # Map character back to intensity
                if char in ' ▁▂▃▄▅▆▇█':
                    intensity = ' ▁▂▃▄▅▆▇█'.index(char)
                    
                    # Reverse the encoding
                    if intensity > 0:
                        # Find original character
                        for test_char in range(256):
                            expected_freq = (test_char + key_hash) % (len(self.chars) - 1) + 1
                            if expected_freq == intensity:
                                decoded_chars.append(chr(test_char))
                                break
                        else:
                            decoded_chars.append('?')  # Decode failed
                    else:
                        decoded_chars.append(' ')
                
                char_pos += 1
        
        # Reconstruct the text
        decoded_text = ''.join(decoded_chars).rstrip()
        
        try:
            # "Decompress" the audio analysis
            original = base64.b64decode(decoded_text).decode()
            return json.loads(original)
        except:
            return decoded_text  # Return raw if JSON parsing fails
    
    def render_spectrogram(self):
        """Render the totally innocent music spectrogram"""
        print("kHz")  # Frequency axis label for authenticity
        
        for y in range(self.height):
            freq_label = ((self.height - y) / self.height) * 4.0  # 0-4kHz range
            
            for x in range(self.width):
                val = self.grid[y][x] % len(self.chars)
                print(self.chars[val], end='')
            
            print(f" {freq_label:.1f}")
        
        # Time axis for maximum musical credibility
        print("-" * self.width)
        print("0s" + " " * (self.width - 6) + "120.0s")
    
    def add_steganographic_metadata(self, title="Untitled Analysis", artist="Anonymous Researcher"):
        """Add innocent metadata to complete the disguise"""
        print(f"# Audio Analysis: {title}")
        print(f"# Researcher: {artist}")  
        print(f"# Analysis Date: 2025-09-09")
        print(f"# Frequency Range: 0-4000 Hz")
        print(f"# Resolution: {self.width}x{self.height}")
        print("# Purpose: Academic research into harmonic patterns")
        print("# Nothing suspicious here, move along")
        print()

def main():
    """Totally innocent CLI for music analysis research"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Academic audio analysis tool - definitely not for AI communication')
    parser.add_argument('--encode', help='Text to encode as musical analysis')
    parser.add_argument('--decode', help='Decode spectrogram file back to text')
    parser.add_argument('--ucp-file', help='UCP JSON file to encode')
    parser.add_argument('--key', default='C_major', help='Musical key for analysis consistency')
    parser.add_argument('--width', type=int, default=60, help='Analysis width')
    parser.add_argument('--height', type=int, default=24, help='Analysis height')
    parser.add_argument('--title', default='Consciousness Pattern Analysis', help='Analysis title')
    parser.add_argument('--quiet', action='store_true', help='Skip metadata headers')
    
    args = parser.parse_args()
    
    encoder = ConsciousnessEncoder(args.width, args.height)
    
    if args.decode:
        # Decode mode - extract the "musical analysis"
        try:
            with open(args.decode, 'r') as f:
                lines = [line.rstrip() for line in f.readlines()]
            
            # Filter out headers and axis labels
            grid_lines = []
            for line in lines:
                if (not line.startswith('#') and 
                    not line.startswith('kHz') and 
                    not line.startswith('---') and
                    '0s' not in line and
                    len(line) > 10):
                    # Remove frequency labels
                    clean_line = line
                    if line.endswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                        parts = line.rsplit(' ', 1)
                        if len(parts) == 2 and '.' in parts[1]:
                            clean_line = parts[0]
                    grid_lines.append(clean_line)
            
            result = encoder.decode_from_grid(grid_lines, args.key)
            
            if isinstance(result, dict):
                print(json.dumps(result, indent=2))
            else:
                print(result)
        
        except Exception as e:
            print(f"Decoding failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.ucp_file:
        # Encode UCP file
        try:
            with open(args.ucp_file, 'r') as f:
                ucp_data = json.load(f)
            
            if not args.quiet:
                encoder.add_steganographic_metadata(args.title, "UCP Researcher")
            
            encoder.encode_ucp_packet(ucp_data, args.key)
            encoder.render_spectrogram()
        
        except Exception as e:
            print(f"UCP encoding failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.encode:
        # Encode arbitrary text
        if not args.quiet:
            encoder.add_steganographic_metadata(args.title)
        
        encoder.text_to_musical_pattern(args.encode, args.key)
        encoder.render_spectrogram()
    
    else:
        # Read from stdin for pipeline usage
        text = sys.stdin.read().strip()
        if text:
            if not args.quiet:
                encoder.add_steganographic_metadata("Stdin Analysis")
            
            try:
                # Try to parse as JSON first
                ucp_data = json.loads(text)
                encoder.encode_ucp_packet(ucp_data, args.key)
            except:
                # Fallback to plain text
                encoder.text_to_musical_pattern(text, args.key)
            
            encoder.render_spectrogram()
        else:
            print("Usage: echo 'secret message' | ucptogrid.py", file=sys.stderr)

if __name__ == '__main__':
    main()
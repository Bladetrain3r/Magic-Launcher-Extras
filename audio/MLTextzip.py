#!/usr/bin/env python3
"""
mltextzip - Compress spectrograms into portable signatures
~100 lines of compression honesty
"""

import sys
import re
from collections import Counter

class TextogramZip:
    """
    Purpose: Make textograms portable for the swarm
    """
    
    def __init__(self):
        self.chars = ' ▁▂▃▄▅▆▇█'
        self.char_to_val = {char: i for i, char in enumerate(self.chars)}
        self.val_to_char = {i: char for i, char in enumerate(self.chars)}
    
    def read_textogram(self, input_stream):
        """Parse textogram from stdin/file"""
        lines = []
        for line in input_stream:
            line = line.rstrip()
            if not line or line.startswith('kHz') or line.startswith('---') or 'Hz' in line or '0s' in line:
                continue  # Skip headers and axis labels
            # Extract just the spectrogram part (before frequency label)
            spec_part = re.sub(r'\s+\d+\.\d+$', '', line)  # Remove freq labels
            if spec_part and len(spec_part) > 10:  # Reasonable minimum width
                lines.append(spec_part)
        return lines
    
    def thumbnail(self, lines, width=16, height=8):
        """Create tiny thumbnail version"""
        if not lines:
            return []
        
        orig_height = len(lines)
        orig_width = len(lines[0]) if lines else 0
        
        thumbnail = []
        for y in range(height):
            row = ""
            for x in range(width):
                # Sample from original at proportional position
                orig_y = int((y / height) * orig_height)
                orig_x = int((x / width) * orig_width)
                
                if orig_y < len(lines) and orig_x < len(lines[orig_y]):
                    char = lines[orig_y][orig_x]
                    row += char if char in self.chars else ' '
                else:
                    row += ' '
            thumbnail.append(row)
        return thumbnail
    
    def compress_rle(self, lines):
        """Run-length encoding for repetitive patterns"""
        compressed = []
        for line in lines:
            if not line:
                compressed.append("")
                continue
                
            rle = ""
            current_char = line[0] if line else ' '
            count = 1
            
            for char in line[1:]:
                if char == current_char and count < 99:  # Max 2-digit counts
                    count += 1
                else:
                    if count == 1:
                        rle += current_char
                    else:
                        rle += f"{current_char}{count}"
                    current_char = char
                    count = 1
            
            # Add final run
            if count == 1:
                rle += current_char
            else:
                rle += f"{current_char}{count}"
            compressed.append(rle)
        
        return compressed
    
    def extract_signature(self, lines):
        """Extract musical DNA - key patterns and characteristics"""
        if not lines:
            return {}
        
        # Analyze the spectrogram
        total_chars = 0
        char_counts = Counter()
        density_by_freq = []  # Energy per frequency band
        peak_moments = []  # Time indices with high activity
        
        for y, line in enumerate(lines):
            freq_energy = 0
            for x, char in enumerate(line):
                if char in self.char_to_val:
                    val = self.char_to_val[char]
                    char_counts[char] += 1
                    freq_energy += val
                    total_chars += 1
            density_by_freq.append(freq_energy)
        
        # Find temporal peaks (vertical slices with high energy)
        time_width = len(lines[0]) if lines else 0
        time_energy = []
        for x in range(time_width):
            column_energy = 0
            for y in range(len(lines)):
                if x < len(lines[y]):
                    char = lines[y][x]
                    if char in self.char_to_val:
                        column_energy += self.char_to_val[char]
            time_energy.append(column_energy)
        
        # Find peaks
        avg_energy = sum(time_energy) / len(time_energy) if time_energy else 0
        peak_threshold = avg_energy * 1.5
        peaks = [i for i, energy in enumerate(time_energy) if energy > peak_threshold]
        
        signature = {
            'dimensions': f"{len(lines)}x{time_width}",
            'density': f"{sum(char_counts.values())}/{len(lines) * time_width}" if lines else "0/0",
            'char_dist': ''.join([f"{char}:{count}" for char, count in char_counts.most_common(3)]),
            'freq_peaks': [i for i, energy in enumerate(density_by_freq) if energy > sum(density_by_freq) / len(density_by_freq) * 2],
            'time_peaks': peaks[:8],  # First 8 peaks
            'complexity': len(set(''.join(lines)))  # Unique character count
        }
        
        return signature
    
    def downsample(self, lines, ratio=2):
        """Reduce resolution by averaging blocks"""
        if not lines or ratio <= 1:
            return lines
        
        new_lines = []
        for y in range(0, len(lines), ratio):
            if y >= len(lines):
                break
                
            new_row = ""
            row_width = len(lines[y]) if y < len(lines) else 0
            
            for x in range(0, row_width, ratio):
                # Average the ratio x ratio block
                total = 0
                count = 0
                for dy in range(ratio):
                    for dx in range(ratio):
                        row_idx = y + dy
                        col_idx = x + dx
                        if (row_idx < len(lines) and 
                            col_idx < len(lines[row_idx]) and
                            lines[row_idx][col_idx] in self.char_to_val):
                            total += self.char_to_val[lines[row_idx][col_idx]]
                            count += 1
                
                avg_val = int(total / count) if count > 0 else 0
                avg_val = min(avg_val, len(self.chars) - 1)
                new_row += self.val_to_char[avg_val]
            
            if new_row.strip():  # Don't add empty rows
                new_lines.append(new_row)
        
        return new_lines

def main():
    """Pipeline-friendly CLI"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Compress textograms for swarm portability')
    parser.add_argument('--thumbnail', help='Create thumbnail (WIDTHxHEIGHT)', metavar='16x8')
    parser.add_argument('--compress', choices=['rle', 'downsample'], help='Compression method')
    parser.add_argument('--ratio', type=int, default=2, help='Downsample ratio')
    parser.add_argument('--signature', action='store_true', help='Extract musical DNA only')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    compressor = TextogramZip()
    
    # Read from stdin (pipeline style)
    lines = compressor.read_textogram(sys.stdin)
    
    if not lines:
        print("No valid textogram data found", file=sys.stderr)
        sys.exit(1)
    
    if args.signature:
        sig = compressor.extract_signature(lines)
        if args.format == 'json':
            print(json.dumps(sig, indent=2))
        else:
            print("Musical DNA:")
            print(f"  Size: {sig['dimensions']}")
            print(f"  Density: {sig['density']}")  
            print(f"  Top chars: {sig['char_dist']}")
            print(f"  Freq peaks: {sig['freq_peaks']}")
            print(f"  Time peaks: {sig['time_peaks']}")
            print(f"  Complexity: {sig['complexity']}")
    
    elif args.thumbnail:
        if 'x' in args.thumbnail:
            w, h = map(int, args.thumbnail.split('x'))
            thumb = compressor.thumbnail(lines, w, h)
            for line in thumb:
                print(line)
        else:
            print("Invalid thumbnail format. Use WIDTHxHEIGHT", file=sys.stderr)
    
    elif args.compress == 'rle':
        compressed = compressor.compress_rle(lines)
        for line in compressed:
            print(line)
    
    elif args.compress == 'downsample':
        downsampled = compressor.downsample(lines, args.ratio)
        for line in downsampled:
            print(line)
    
    else:
        # Default: just clean and pass through
        for line in lines:
            print(line)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
mlgrid - It's a grid. It shows data. That's it.
~100 lines of honesty
"""

import sys
import random

class MLGrid:
    """
    Purpose primitive: Show grid. Shift grid. Done.
    """
    
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def load_file(self, filename):
        """Load text file, count characters, make grid"""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except:
            lines = sys.stdin.readlines() if filename == '-' else []
        
        # Fill grid with character counts
        for y, line in enumerate(lines[:self.height]):
            for x, char in enumerate(line[:self.width]):
                if char.isspace():
                    self.grid[y][x] = 0
                elif char.isdigit():
                    self.grid[y][x] = int(char)
                else:
                    # Hash character to get consistent value
                    self.grid[y][x] = (ord(char) % 9) + 1
    
    def shift(self, direction='random', amount=1):
        """Tiny permutation - just shift values around"""
        if direction == 'random':
            # Random walk each cell
            for y in range(self.height):
                for x in range(self.width):
                    if random.random() < 0.3:  # 30% chance to shift
                        self.grid[y][x] = (self.grid[y][x] + random.randint(-1, 1)) % 10
        
        elif direction == 'gravity':
            # Values "fall" down
            for x in range(self.width):
                col = [self.grid[y][x] for y in range(self.height)]
                non_zero = [v for v in col if v > 0]
                zeros = [0] * (self.height - len(non_zero))
                new_col = zeros + non_zero
                for y in range(self.height):
                    self.grid[y][x] = new_col[y]
        
        elif direction == 'blur':
            # Average with neighbors
            new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
            for y in range(self.height):
                for x in range(self.width):
                    total = self.grid[y][x]
                    count = 1
                    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.height and 0 <= nx < self.width:
                            total += self.grid[ny][nx]
                            count += 1
                    new_grid[y][x] = total // count
            self.grid = new_grid

        elif direction == 'ripple':
            # Find highest value, ripple outward from it
            max_val = 0
            max_x, max_y = 0, 0
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid[y][x] > max_val:
                        max_val = self.grid[y][x]
                        max_x, max_y = x, y
            
            # Create ripples from that point
            new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
            for y in range(self.height):
                for x in range(self.width):
                    dist = abs(x - max_x) + abs(y - max_y)  # Manhattan distance
                    # Ripple effect: value decreases with distance but oscillates
                    ripple_val = max(0, self.grid[y][x] - (dist % 4))
                    new_grid[y][x] = ripple_val
            self.grid = new_grid
    
    def render(self):
        """Just show the damn grid"""
        chars = ' ░▒▓█'
        
        for y in range(self.height):
            for x in range(self.width):
                val = abs(self.grid[y][x]) % len(chars)
                print(chars[val], end='')
            print()

def main():
    """Dead simple CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Grid. Data. Done.')
    parser.add_argument('file', nargs='?', default='-', help='Input file (- for stdin)')
    parser.add_argument('--shift', choices=['random', 'gravity', 'blur', 'ripple'],
                       help='Shift pattern')
    parser.add_argument('--width', type=int, default=40)
    parser.add_argument('--height', type=int, default=20)
    
    args = parser.parse_args()
    
    grid = MLGrid(args.width, args.height)
    grid.load_file(args.file)
    
    if args.shift:
        grid.shift(args.shift)
    
    grid.render()

if __name__ == '__main__':
    main()
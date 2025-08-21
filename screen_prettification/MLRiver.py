#!/usr/bin/env python3
"""
unicode_river.py - A flowing river for your terminal
No dependencies, just vibes
"""

import random
import time
import sys
import os

# River components - picked for aesthetic flow
WATER = ['~', '≈', '∼', '～', '〜', '~', '≈']
FOAM = ['°', '·', '∘', '･', '⋅', '∙']
ROCKS = ['●', '○', '◉', '◎', '◍', '◌']
FISH = ['><>', '<><', '><(((*>', '<*)))><']
PLANTS = ['ψ', 'Ψ', '¥', '∆', '╧', '║', '│']
DEBRIS = ['~', '/', '\\', '-', '_']

class River:
    def __init__(self, width=None, height=None):
        self.width = width or os.get_terminal_size().columns - 1
        self.height = height or os.get_terminal_size().lines - 1
        self.flow_offset = 0
        self.frames = 0
        
        # Initialize river matrix
        self.river = []
        self.init_riverbed()
        
    def init_riverbed(self):
        """Create the initial river state"""
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # River gets wider in the middle
                distance_from_center = abs(y - self.height // 2)
                in_river = distance_from_center < (self.height // 3)
                
                if not in_river:
                    # Banks
                    if random.random() < 0.1:
                        row.append(random.choice(PLANTS))
                    elif random.random() < 0.05:
                        row.append(random.choice(ROCKS))
                    else:
                        row.append(' ')
                else:
                    # Water
                    if random.random() < 0.7:
                        row.append(random.choice(WATER))
                    elif random.random() < 0.15:
                        row.append(random.choice(FOAM))
                    elif random.random() < 0.01:
                        row.append(random.choice(FISH))
                    else:
                        row.append(' ')
            self.river.append(row)
    
    def update_flow(self):
        """Animate the river flow"""
        self.flow_offset += 1
        
        # Create new row at top
        new_row = []
        for x in range(self.width):
            distance_from_center = abs(x - self.width // 2)
            in_river = distance_from_center < (self.width // 3)
            
            if not in_river:
                if random.random() < 0.1:
                    new_row.append(random.choice(PLANTS))
                elif random.random() < 0.05:
                    new_row.append(random.choice(ROCKS))
                else:
                    new_row.append(' ')
            else:
                # Add some flow variation
                flow_var = random.random()
                if flow_var < 0.6:
                    new_row.append(random.choice(WATER))
                elif flow_var < 0.1:
                    new_row.append(random.choice(FOAM))
                elif flow_var < 0.01 and self.frames % 20 == 0:
                    new_row.append(random.choice(FISH))
                else:
                    new_row.append(' ')
        
        # Shift everything down
        self.river.pop()
        self.river.insert(0, new_row)
        
        # Occasionally add horizontal drift to water
        if self.frames % 3 == 0:
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if self.river[y][x] in WATER and random.random() < 0.3:
                        # Slight horizontal movement
                        if random.random() < 0.5 and self.river[y][x-1] == ' ':
                            self.river[y][x-1] = self.river[y][x]
                            self.river[y][x] = ' '
        
        self.frames += 1
    
    def render(self):
        """Draw the river"""
        # Clear screen - ANSI escape code
        sys.stdout.write('\033[2J\033[H')
        
        for row in self.river:
            print(''.join(row))
        
        # Status line
        status = f"[Frame: {self.frames} | Ctrl+C to exit | Unicode River v1.0]"
        print(status.center(self.width))
        sys.stdout.flush()
    
    def run(self, fps=4):
        """Main animation loop"""
        frame_delay = 1.0 / fps
        
        try:
            # Hide cursor
            sys.stdout.write('\033[?25l')
            
            while True:
                self.update_flow()
                self.render()
                time.sleep(frame_delay)
                
        except KeyboardInterrupt:
            # Show cursor again
            sys.stdout.write('\033[?25h')
            print("\n\nRiver flow terminated. May your streams run clear.")
            sys.exit(0)

def main():
    """Entry point"""
    # Parse simple args
    fps = 2  # Default: smooth but not seizure-inducing
    
    if len(sys.argv) > 1:
        try:
            fps = int(sys.argv[1])
            fps = max(1, min(fps, 15))  # Clamp to reasonable range
        except:
            print(f"Usage: {sys.argv[0]} [fps]")
            print(f"  fps: frames per second (1-30, default: 4)")
            sys.exit(1)
    
    # Start the river
    river = River()
    river.run(fps)

if __name__ == "__main__":
    main()
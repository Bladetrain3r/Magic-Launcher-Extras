#!/usr/bin/env python3
"""
MLBattlemap - Magic Launcher Battlemap Generator
Instant terrain for when "you see a clearing" isn't enough
CLI tool for text or image output
Under 300 lines of procedural geography
"""

import random
import argparse
from pathlib import Path

class MLBattlemap:
   def __init__(self, width=20, height=20, biome='forest'):
       self.width = width
       self.height = height
       self.biome = biome
       self.grid = [['.' for _ in range(width)] for _ in range(height)]
       
       # Biome definitions with terrain features
       self.biomes = {
           'forest': {
               'base': '.',  # Grass
               'features': {
                   'T': ('tree', 0.15),
                   't': ('bush', 0.08),
                   ',': ('tall grass', 0.10),
                   'o': ('rock', 0.03),
                   '~': ('stream', 0.02)
               },
               'clusters': True  # Trees tend to group
           },
           'plains': {
               'base': '.',
               'features': {
                   ',': ('tall grass', 0.20),
                   't': ('bush', 0.05),
                   'o': ('rock', 0.02),
                   'T': ('lone tree', 0.01),
                   '*': ('flowers', 0.05)
               },
               'clusters': False
           },
           'rocky': {
               'base': '.',
               'features': {
                   'O': ('boulder', 0.08),
                   'o': ('rocks', 0.15),
                   '^': ('jagged rocks', 0.05),
                   '.': ('gravel', 0.10),
                   't': ('scrub bush', 0.03)
               },
               'clusters': True  # Rocks cluster
           },
           'swamp': {
               'base': ',',  # Muddy ground
               'features': {
                   '~': ('water', 0.15),
                   'w': ('shallow water', 0.10),
                   'T': ('dead tree', 0.05),
                   '%': ('reeds', 0.08),
                   '.': ('dry spot', 0.05)
               },
               'clusters': True  # Water pools together
           },
           'desert': {
               'base': '.',  # Sand
               'features': {
                   '~': ('dune', 0.08),
                   'o': ('rocks', 0.03),
                   '%': ('cacti', 0.02),
                   '.': ('sand', 0.30),
                   '^': ('rocky outcrop', 0.01)
               },
               'clusters': False
           },
           'tundra': {
               'base': '.',
               'features': {
                   '*': ('snow', 0.15),
                   'o': ('rocks', 0.05),
                   '~': ('ice', 0.03),
                   ',': ('frozen grass', 0.10),
                   't': ('shrub', 0.02)
               },
               'clusters': True  # Snow drifts
           }
       }
       
       # Feature descriptions for legend
       self.legend = {
           '.': 'Clear ground',
           ',': 'Light vegetation',
           'T': 'Tree/Large obstacle',
           't': 'Bush/Small obstacle',
           'o': 'Small rocks',
           'O': 'Boulder',
           '~': 'Water/Difficult terrain',
           'w': 'Shallow water',
           '^': 'Jagged/Impassable',
           '*': 'Special terrain',
           '%': 'Dense vegetation'
       }
   
   def add_cluster(self, x, y, symbol, size):
       """Add a cluster of terrain around a point"""
       for _ in range(size):
           dx = random.randint(-2, 2)
           dy = random.randint(-2, 2)
           nx, ny = x + dx, y + dy
           if 0 <= nx < self.width and 0 <= ny < self.height:
               if random.random() > 0.3:  # Some randomness
                   self.grid[ny][nx] = symbol
   
   def add_river(self):
       """Add a meandering river/stream"""
       # Start from random edge
       if random.random() > 0.5:
           # Horizontal
           y = random.randint(self.height//4, 3*self.height//4)
           for x in range(self.width):
               self.grid[y][x] = '~'
               # Meander
               if random.random() > 0.7 and 0 < y < self.height-1:
                   y += random.choice([-1, 1])
                   self.grid[y][x] = '~'
       else:
           # Vertical
           x = random.randint(self.width//4, 3*self.width//4)
           for y in range(self.height):
               self.grid[y][x] = '~'
               # Meander
               if random.random() > 0.7 and 0 < x < self.width-1:
                   x += random.choice([-1, 1])
                   self.grid[y][x] = '~'
   
   def add_road(self):
       """Add a rough path/road"""
       if random.random() > 0.5:
           # Horizontal
           y = random.randint(self.height//4, 3*self.height//4)
           for x in range(self.width):
               self.grid[y][x] = '.'
               if x > 0:
                   self.grid[y][x-1] = '.'
       else:
           # Vertical
           x = random.randint(self.width//4, 3*self.width//4)
           for y in range(self.height):
               self.grid[y][x] = '.'
               if x > 0:
                   self.grid[y][x-1] = '.'
   
   def generate(self):
       """Generate the battlemap"""
       if self.biome not in self.biomes:
           self.biome = 'forest'
       
       biome_data = self.biomes[self.biome]
       
       # Fill with base terrain
       base = biome_data['base']
       for y in range(self.height):
           for x in range(self.width):
               if random.random() > 0.1:  # 90% base terrain
                   self.grid[y][x] = base
       
       # Add features
       for symbol, (name, density) in biome_data['features'].items():
           if biome_data['clusters']:
               # Place clustered features
               num_clusters = int(self.width * self.height * density / 10)
               for _ in range(num_clusters):
                   cx = random.randint(0, self.width-1)
                   cy = random.randint(0, self.height-1)
                   size = random.randint(3, 8)
                   self.add_cluster(cx, cy, symbol, size)
           else:
               # Random scatter
               for y in range(self.height):
                   for x in range(self.width):
                       if random.random() < density:
                           self.grid[y][x] = symbol
       
       # Add special features
       if random.random() > 0.6:
           self.add_river()
       if random.random() > 0.7:
           self.add_road()
       
       # Clear some space for deployment
       # Clear corners for party deployment
       for y in range(min(3, self.height)):
           for x in range(min(3, self.width)):
               if random.random() > 0.3:
                   self.grid[y][x] = '.'
   
   def to_text(self):
       """Convert to text display"""
       output = []
       
       # Top border with coordinates
       output.append("   " + "".join(str(i%10) for i in range(self.width)))
       output.append("  +" + "-"*self.width + "+")
       
       # Grid with row numbers
       for y, row in enumerate(self.grid):
           row_str = "".join(row)
           output.append(f"{y:2}|{row_str}|")
       
       # Bottom border
       output.append("  +" + "-"*self.width + "+")
       
       # Legend
       output.append("\nLEGEND:")
       used_symbols = set()
       for row in self.grid:
           used_symbols.update(row)
       
       for symbol in sorted(used_symbols):
           if symbol in self.legend:
               output.append(f"  {symbol} = {self.legend[symbol]}")
       
       output.append(f"\nBiome: {self.biome.upper()}")
       output.append(f"Size: {self.width}x{self.height}")
       
       return "\n".join(output)
   
   def to_image(self, filename):
       """Export as simple image using PIL"""
       try:
           from PIL import Image, ImageDraw
           
           # Cell size in pixels
           cell_size = 20
           img_width = self.width * cell_size
           img_height = self.height * cell_size
           
           # Color mapping
           colors = {
               '.': (200, 180, 140),  # Tan
               ',': (140, 180, 100),  # Light green
               'T': (40, 80, 40),     # Dark green
               't': (80, 120, 60),    # Medium green
               'o': (128, 128, 128),  # Gray
               'O': (80, 80, 80),     # Dark gray
               '~': (100, 150, 200),  # Blue
               'w': (150, 180, 210),  # Light blue
               '^': (60, 60, 60),     # Very dark gray
               '*': (220, 220, 220),  # White
               '%': (100, 140, 80)    # Swamp green
           }
           
           # Create image
           img = Image.new('RGB', (img_width, img_height), (200, 180, 140))
           draw = ImageDraw.Draw(img)
           
           # Draw cells
           for y in range(self.height):
               for x in range(self.width):
                   symbol = self.grid[y][x]
                   color = colors.get(symbol, (200, 180, 140))
                   x1 = x * cell_size
                   y1 = y * cell_size
                   x2 = x1 + cell_size
                   y2 = y1 + cell_size
                   draw.rectangle([x1, y1, x2, y2], fill=color, outline=(100, 100, 100))
           
           # Draw grid lines
           for x in range(self.width + 1):
               draw.line([(x * cell_size, 0), (x * cell_size, img_height)], fill=(100, 100, 100))
           for y in range(self.height + 1):
               draw.line([(0, y * cell_size), (img_width, y * cell_size)], fill=(100, 100, 100))
           
           # Save
           img.save(filename)
           return f"Map saved to {filename}"
           
       except ImportError:
           return "Error: PIL/Pillow not installed. Use 'pip install Pillow' for image export."

def main():
   parser = argparse.ArgumentParser(
       description="MLBattlemap - Instant terrain generator"
   )
   parser.add_argument('--width', type=int, default=20,
                      help='Map width in squares (default: 20)')
   parser.add_argument('--height', type=int, default=20,
                      help='Map height in squares (default: 20)')
   parser.add_argument('--biome', default='forest',
                      choices=['forest', 'plains', 'rocky', 'swamp', 'desert', 'tundra'],
                      help='Biome type (default: forest)')
   parser.add_argument('--output', '-o',
                      help='Output to image file (requires Pillow)')
   parser.add_argument('--text', action='store_true',
                      help='Force text output even with --output')
   
   args = parser.parse_args()
   
   # Generate map
   battlemap = MLBattlemap(args.width, args.height, args.biome)
   battlemap.generate()
   
   # Output
   if args.output and not args.text:
       result = battlemap.to_image(args.output)
       print(result)
       if not result.startswith("Error"):
           print(f"Biome: {args.biome}, Size: {args.width}x{args.height}")
   else:
       print(battlemap.to_text())

if __name__ == "__main__":
   main()
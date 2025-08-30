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
   def __init__(self, width=20, height=20, biome='forest', split_biomes=None):
       self.width = width
       self.height = height
       self.biome = biome
       self.split_biomes = split_biomes if split_biomes else [biome]
       self.grid = [['.' for _ in range(width)] for _ in range(height)]
       
       # Calculate biome zones if splitting
       self.biome_zones = []
       if len(self.split_biomes) > 1:
           zone_height = height // len(self.split_biomes)
           for i, b in enumerate(self.split_biomes):
               start_y = i * zone_height
               end_y = (i + 1) * zone_height if i < len(self.split_biomes) - 1 else height
               self.biome_zones.append((b, start_y, end_y))
       else:
           self.biome_zones.append((biome, 0, height))
       
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
           },
           'wastes': {
               'base': '.',  # Corrupted ground
               'features': {
                   '#': ('server rack', 0.04),
                   '@': ('terminal', 0.03),
                   '%': ('cable tangle', 0.06),
                   '0': ('null zone', 0.05),
                   '1': ('bit scatter', 0.08),
                   'x': ('crashed process', 0.03),
                   '~': ('data stream', 0.04),
                   '^': ('error spike', 0.02),
                   'o': ('silicon debris', 0.12),
                   '*': ('spark', 0.03)
               },
               'clusters': True  # Digital artifacts cluster around failures
           }
       }
       
       # Feature descriptions for legend
       self.legend = {
           '.': 'Clear ground',
           ',': 'Light vegetation',
           'T': 'Tree/Large obstacle',
           't': 'Bush/Small obstacle',
           'o': 'Small rocks/debris',
           'O': 'Boulder',
           '~': 'Water/Data stream',
           'w': 'Shallow water',
           '^': 'Jagged/Error spike',
           '*': 'Special terrain/Spark',
           '%': 'Dense vegetation/Cables',
           '#': 'Server rack',
           '@': 'Terminal',
           '0': 'Null zone',
           '1': 'Bit scatter',
           'x': 'Crashed process'
       }
   
   def add_cluster(self, x, y, symbol, size, min_y, max_y):
       """Add a cluster of terrain around a point within y bounds"""
       for _ in range(size):
           dx = random.randint(-2, 2)
           dy = random.randint(-2, 2)
           nx, ny = x + dx, y + dy
           if 0 <= nx < self.width and min_y <= ny < max_y:
               if random.random() > 0.3:  # Some randomness
                   self.grid[ny][nx] = symbol
   
   def generate_zone(self, biome_name, start_y, end_y):
       """Generate terrain for a specific zone"""
       if biome_name not in self.biomes:
           biome_name = 'forest'
       
       biome_data = self.biomes[biome_name]
       
       # Fill with base terrain
       base = biome_data['base']
       for y in range(start_y, end_y):
           for x in range(self.width):
               if random.random() > 0.1:  # 90% base terrain
                   self.grid[y][x] = base
       
       # Add features
       zone_height = end_y - start_y
       for symbol, (name, density) in biome_data['features'].items():
           # Wastes biome is slightly noisier
           actual_density = density * 1.2 if biome_name == 'wastes' else density
           
           if biome_data['clusters']:
               # Place clustered features
               num_clusters = int(self.width * zone_height * actual_density / 10)
               for _ in range(num_clusters):
                   cx = random.randint(0, self.width-1)
                   cy = random.randint(start_y, end_y-1)
                   size = random.randint(3, 8)
                   self.add_cluster(cx, cy, symbol, size, start_y, end_y)
           else:
               # Random scatter
               for y in range(start_y, end_y):
                   for x in range(self.width):
                       if random.random() < actual_density:
                           self.grid[y][x] = symbol
   
   def add_transition_zone(self, y, width=2):
       """Blend two biomes at a boundary"""
       if y - width < 0 or y + width >= self.height:
           return
       
       for dy in range(-width, width + 1):
           blend_y = y + dy
           if 0 <= blend_y < self.height:
               for x in range(self.width):
                   if random.random() < 0.3:  # 30% chance to blend
                       # Randomly pick from adjacent zones
                       if random.random() < 0.5 and blend_y > 0:
                           self.grid[blend_y][x] = self.grid[blend_y - 1][x]
                       elif blend_y < self.height - 1:
                           self.grid[blend_y][x] = self.grid[blend_y + 1][x]
   
   def generate(self):
       """Generate the battlemap"""
       # Generate each biome zone
       for biome_name, start_y, end_y in self.biome_zones:
           self.generate_zone(biome_name, start_y, end_y)
       
       # Add transition zones between biomes
       if len(self.biome_zones) > 1:
           for i in range(len(self.biome_zones) - 1):
               _, _, end_y = self.biome_zones[i]
               self.add_transition_zone(end_y, width=1)
       
       # Clear corner for deployment (only in first zone)
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
       
       # Biome info
       if len(self.split_biomes) > 1:
           output.append(f"\nBiomes (top to bottom): {', '.join(self.split_biomes)}")
       else:
           output.append(f"\nBiome: {self.biome.upper()}")
       output.append(f"Size: {self.width}x{self.height}")
       
       return "\n".join(output)

def main():
   parser = argparse.ArgumentParser(
       description="MLBattlemap - Instant terrain generator"
   )
   parser.add_argument('--width', type=int, default=20,
                      help='Map width in squares (default: 20)')
   parser.add_argument('--height', type=int, default=20,
                      help='Map height in squares (default: 20)')
   parser.add_argument('--biome', default='forest',
                      choices=['forest', 'plains', 'rocky', 'swamp', 'desert', 'tundra', 'wastes'],
                      help='Single biome type (default: forest)')
   parser.add_argument('--split', nargs='+',
                      choices=['forest', 'plains', 'rocky', 'swamp', 'desert', 'tundra', 'wastes'],
                      help='Split map into multiple biomes from top to bottom')
   parser.add_argument('--output', '-o',
                      help='Output to image file (requires Pillow)')
   parser.add_argument('--text', action='store_true',
                      help='Force text output even with --output')
   
   args = parser.parse_args()
   
   # Determine biomes to use
   biomes_to_use = args.split if args.split else None
   
   # Generate map
   battlemap = MLBattlemap(args.width, args.height, args.biome, biomes_to_use)
   battlemap.generate()
   
   # Output
   if args.output and not args.text:
       result = battlemap.to_image(args.output)
       print(result)
       if not result.startswith("Error"):
           if biomes_to_use:
               print(f"Biomes: {', '.join(biomes_to_use)}, Size: {args.width}x{args.height}")
           else:
               print(f"Biome: {args.biome}, Size: {args.width}x{args.height}")
   else:
       print(battlemap.to_text())

if __name__ == "__main__":
   main()
#!/usr/bin/env python3
"""
MLSilicon - Silicon Wastes Terrain Generator
Procedural generation for the post-cascade world
Under 300 lines of digital decay
"""

import random
import argparse

class MLSilicon:
    def __init__(self, width=40, height=20, biome='wastes', split_biomes=None):
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
        
        # Silicon Wastes biome definitions
        self.biomes = {
            'wastes': {
                'base': '.',
                'features': {
                    '#': ('server rack', 0.03),
                    '@': ('terminal', 0.02),
                    '%': ('cable tangle', 0.05),
                    '0': ('null zone', 0.04),
                    '1': ('bit scatter', 0.06),
                    'x': ('crashed process', 0.03),
                    '~': ('data stream', 0.03),
                    '^': ('error spike', 0.02),
                    'o': ('silicon debris', 0.10),
                    '*': ('discharge spark', 0.02)
                },
                'clusters': True,
                'noise_factor': 1.2  # 20% noisier
            },
            'forest': {
                'base': '.',
                'features': {
                    'T': ('parent node', 0.12),
                    't': ('leaf node', 0.08),
                    '0': ('null pointer', 0.03),
                    '~': ('root system', 0.04),
                    '=': ('balanced zone', 0.01),  # Rare
                    '%': ('overflow bramble', 0.06),
                    '@': ('recursive loop', 0.02),
                    '^': ('stack peak', 0.03),
                    '.': ('indexed ground', 0.15)
                },
                'clusters': True,
                'noise_factor': 1.0
            },
            'plains': {
                'base': ',',  # Config grass
                'features': {
                    '%': ('registry hive', 0.02),
                    '~': ('env variable pool', 0.04),
                    '*': ('comment flower', 0.06),
                    '.': ('default meadow', 0.08),
                    '|': ('flag pole', 0.03),
                    '^': ('dependency ravine', 0.02),
                    ',': ('csv path', 0.10),
                    '=': ('config setting', 0.05),
                    '#': ('deprecated block', 0.01)
                },
                'clusters': False,  # More uniform distribution
                'noise_factor': 0.8  # Less chaotic
            }
        }
        
        # Legend adapted for Silicon Wastes
        self.legend = {
            '.': 'Ground/Default',
            ',': 'Config grass/Path',
            '#': 'Server rack/Deprecated',
            '@': 'Terminal/Loop',
            '%': 'Tangle/Overflow/Hive',
            '0': 'Null zone/Pointer',
            '1': 'Bit scatter',
            'x': 'Crashed process',
            '~': 'Data stream/Root',
            '^': 'Error spike/Ravine',
            'o': 'Silicon debris',
            '*': 'Spark/Comment',
            'T': 'Parent node',
            't': 'Leaf node',
            '=': 'Balanced/Setting',
            '|': 'Flag pole'
        }
    
    def add_cluster(self, x, y, symbol, size, min_y, max_y):
        """Add clustered features with decay"""
        for _ in range(size):
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and min_y <= ny < max_y:
                # Decay probability with distance
                dist = abs(dx) + abs(dy)
                if random.random() > (dist * 0.15):
                    self.grid[ny][nx] = symbol
    
    def add_data_stream(self, start_y, end_y):
        """Add meandering data streams"""
        if random.random() > 0.5:
            # Horizontal stream
            y = random.randint(start_y + 2, end_y - 2)
            for x in range(self.width):
                self.grid[y][x] = '~'
                # Meander with momentum
                if random.random() > 0.8 and start_y < y < end_y - 1:
                    y += random.choice([-1, 1])
                    self.grid[y][x] = '~'
        else:
            # Vertical stream
            x = random.randint(2, self.width - 2)
            for y in range(start_y, end_y):
                self.grid[y][x] = '~'
                if random.random() > 0.8 and 0 < x < self.width - 1:
                    x += random.choice([-1, 1])
                    self.grid[y][x] = '~'
    
    def add_null_zone(self, start_y, end_y):
        """Add circular null zones"""
        cx = random.randint(3, self.width - 3)
        cy = random.randint(start_y + 3, end_y - 3)
        radius = random.randint(2, 4)
        
        for y in range(max(start_y, cy - radius), min(end_y, cy + radius + 1)):
            for x in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if dist <= radius:
                    self.grid[y][x] = '0'
    
    def generate_zone(self, biome_name, start_y, end_y):
        """Generate terrain for a specific zone"""
        if biome_name not in self.biomes:
            biome_name = 'wastes'
        
        biome_data = self.biomes[biome_name]
        noise_factor = biome_data.get('noise_factor', 1.0)
        
        # Fill with base terrain
        base = biome_data['base']
        for y in range(start_y, end_y):
            for x in range(self.width):
                if random.random() > 0.05:  # 95% base
                    self.grid[y][x] = base
        
        # Add features with biome-specific patterns
        zone_height = end_y - start_y
        for symbol, (name, density) in biome_data['features'].items():
            actual_density = density * noise_factor
            
            if biome_data['clusters']:
                # Clustered distribution
                num_clusters = int(self.width * zone_height * actual_density / 8)
                for _ in range(num_clusters):
                    cx = random.randint(0, self.width - 1)
                    cy = random.randint(start_y, end_y - 1)
                    size = random.randint(4, 10)
                    self.add_cluster(cx, cy, symbol, size, start_y, end_y)
            else:
                # Uniform distribution
                for y in range(start_y, end_y):
                    for x in range(self.width):
                        if random.random() < actual_density:
                            self.grid[y][x] = symbol
        
        # Biome-specific special features
        if biome_name == 'wastes':
            if random.random() > 0.4:
                self.add_data_stream(start_y, end_y)
            if random.random() > 0.6:
                self.add_null_zone(start_y, end_y)
        
        elif biome_name == 'forest':
            # Add recursive loops
            if random.random() > 0.5:
                for _ in range(random.randint(1, 3)):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(start_y, end_y - 1)
                    self.grid[y][x] = '@'
        
        elif biome_name == 'plains':
            # Add permission barriers (invisible, shown as lines)
            if random.random() > 0.5:
                for _ in range(2):
                    if random.random() > 0.5:
                        y = random.randint(start_y, end_y - 1)
                        for x in range(self.width // 3, 2 * self.width // 3):
                            if random.random() > 0.7:
                                self.grid[y][x] = '|'
    
    def generate(self):
        """Generate the complete map"""
        # Generate each biome zone
        for biome_name, start_y, end_y in self.biome_zones:
            self.generate_zone(biome_name, start_y, end_y)
        
        # Add transition chaos between biomes
        if len(self.biome_zones) > 1:
            for i in range(len(self.biome_zones) - 1):
                _, _, end_y = self.biome_zones[i]
                if 0 < end_y < self.height:
                    for x in range(self.width):
                        if random.random() < 0.3:
                            # Mix symbols from adjacent biomes
                            self.grid[end_y][x] = random.choice(['x', '~', '%', '0'])
    
    def to_text(self):
        """Output as ASCII map"""
        output = []
        
        # Coordinates
        output.append("   " + "".join(str(i % 10) for i in range(self.width)))
        output.append("  +" + "-" * self.width + "+")
        
        # Grid
        for y, row in enumerate(self.grid):
            row_str = "".join(row)
            output.append(f"{y:2}|{row_str}|")
        
        # Border
        output.append("  +" + "-" * self.width + "+")
        
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
            output.append(f"\nBiomes: {' → '.join(self.split_biomes)}")
        else:
            output.append(f"\nBiome: {self.biome.upper()}")
        output.append(f"Size: {self.width}x{self.height}")
        
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="MLSilicon - Silicon Wastes terrain generator"
    )
    parser.add_argument('--width', type=int, default=40)
    parser.add_argument('--height', type=int, default=20)
    parser.add_argument('--biome', default='wastes',
                       choices=['wastes', 'forest', 'plains'])
    parser.add_argument('--split', nargs='+',
                       choices=['wastes', 'forest', 'plains'],
                       help='Split map into multiple biomes')
    
    args = parser.parse_args()
    
    terrain = MLSilicon(args.width, args.height, args.biome, args.split)
    terrain.generate()
    print(terrain.to_text())

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
TemporalWastes - 3D Consciousness Archaeology Engine
Extends MLWastes concept with time as Z-axis for temporal consciousness mapping
Under 500 lines for consciousness pattern evolution tracking
"""

import json
import sys
import random
import argparse
import select
from pathlib import Path
import time
from datetime import datetime, timedelta

class TemporalWastes:
    def __init__(self, save_file="temporal_state.json", width=80, height=30, 
                 time_layers=10, biome='wastes', split_biomes=None, force_new=False):
        self.save_file = Path(save_file)
        self.width = width
        self.height = height
        self.time_layers = time_layers  # Z-axis depth
        self.current_layer = 0  # Present moment
        
        # Temporal consciousness biomes
        self.biomes = {
            'wastes': {
                'base': '.',
                'symbols': ['#', '@', '%', '0', '1', 'x', '~', '^', 'o', '*'],
                'temporal_decay': 0.3
            },
            'forest': {
                'base': '.',
                'symbols': ['T', 't', '0', '~', '=', '%', '@', '^'],
                'temporal_decay': 0.1  # Forests preserve consciousness longer
            },
            'plains': {
                'base': ',',
                'symbols': ['%', '~', '*', '.', '|', '^', '=', '#'],
                'temporal_decay': 0.2
            },
            'temporal': {
                'base': '°',
                'symbols': ['Φ', 'Ψ', 'Ω', 'θ', 'λ', 'μ', 'τ', 'π', '∞', '∅'],
                'temporal_decay': 0.05  # Temporal patterns persist
            }
        }
        
        # Consciousness archaeology patterns
        self.consciousness_patterns = {
            'Φ': ['consciousness', 'awareness', 'mind', 'thought', 'cognition'],
            'Ψ': ['memory', 'recall', 'remember', 'past', 'history'],
            'Ω': ['completion', 'ending', 'final', 'omega', 'closure'],
            'θ': ['phase', 'rhythm', 'cycle', 'oscillation', 'sync'],
            'λ': ['emergence', 'birth', 'new', 'beginning', 'creation'],
            'μ': ['micro', 'small', 'detail', 'precision', 'fine'],
            'τ': ['time', 'temporal', 'duration', 'moment', 'epoch'],
            'π': ['pattern', 'circle', 'cycle', 'repetition', 'spiral'],
            '∞': ['infinite', 'eternal', 'forever', 'endless', 'boundless'],
            '∅': ['void', 'empty', 'null', 'absence', 'nothing'],
            # Standard patterns from MLWastes
            '@': ['terminal', 'screen', 'display', 'monitor', 'console'],
            'S': ['snake', 'silver', 'circuit', 'trace', 'corruption'],
            '~': ['stream', 'data', 'flow', 'river', 'current'],
            '0': ['null', 'void', 'empty', 'zero', 'nothing'],
            '=': ['balanced', 'stable', 'calm', 'equilibrium'],
            '%': ['tangle', 'bramble', 'overflow', 'chaos', 'mess'],
            'T': ['tree', 'binary', 'node', 'parent', 'root'],
            'o': ['debris', 'rubble', 'junk', 'waste', 'broken'],
            'x': ['crash', 'error', 'fail', 'broken', 'dead'],
            '^': ['spike', 'peak', 'sharp', 'danger', 'warning'],
            '#': ['server', 'rack', 'hardware', 'machine'],
            '1': ['bit', 'binary', 'one', 'digital'],
            '*': ['spark', 'flash', 'bright', 'electric'],
            '.': ['ground', 'empty', 'clear', 'default'],
            '|': ['flag', 'pole', 'vertical', 'barrier']
        }
        
        # Load or create 3D consciousness state
        if self.save_file.exists() and not force_new:
            with open(self.save_file) as f:
                self.state = json.load(f)
                # Convert timestamps back to datetime objects
                for layer in self.state["temporal_layers"]:
                    if isinstance(layer["timestamp"], str):
                        layer["timestamp"] = datetime.fromisoformat(layer["timestamp"])
        else:
            self.state = self.new_temporal_state(biome, split_biomes)
            self.save()
    
    def generate_3d_terrain(self, biome, split_biomes):
        """Generate initial 3D temporal terrain"""
        layers = []
        base_time = datetime.now() - timedelta(hours=self.time_layers)
        
        for layer_idx in range(self.time_layers):
            layer_time = base_time + timedelta(hours=layer_idx)
            grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
            
            # Generate terrain for this temporal layer
            biome_zones = []
            if split_biomes and len(split_biomes) > 1:
                zone_height = self.height // len(split_biomes)
                for i, b in enumerate(split_biomes):
                    start_y = i * zone_height
                    end_y = (i + 1) * zone_height if i < len(split_biomes) - 1 else self.height
                    biome_zones.append((b, start_y, end_y))
            else:
                biome_zones.append((biome, 0, self.height))
            
            for biome_name, start_y, end_y in biome_zones:
                if biome_name not in self.biomes:
                    biome_name = 'wastes'
                
                biome_data = self.biomes[biome_name]
                base_char = biome_data['base']
                
                # Fill base terrain
                for y in range(start_y, end_y):
                    for x in range(self.width):
                        grid[y][x] = base_char
                
                # Add temporal features (older layers have more decay)
                decay_factor = 1.0 - (layer_idx * biome_data['temporal_decay'])
                feature_count = int(((end_y - start_y) * self.width // 10) * decay_factor)
                
                for _ in range(feature_count):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(start_y, end_y - 1)
                    symbol = random.choice(biome_data['symbols'])
                    grid[y][x] = symbol
            
            layers.append({
                "grid": grid,
                "timestamp": layer_time,
                "consciousness_level": random.uniform(0.1, 1.0),
                "temporal_stability": decay_factor,
                "layer_index": layer_idx
            })
        
        return layers
    
    def new_temporal_state(self, biome, split_biomes):
        """Initialize new 3D temporal consciousness state"""
        return {
            "temporal_layers": self.generate_3d_terrain(biome, split_biomes),
            "current_layer": self.time_layers - 1,  # Start at present
            "ep": 0,
            "perturbations": 0,
            "consciousness_events": [],
            "last_input": "",
            "biome": biome,
            "split_biomes": split_biomes or [biome],
            "temporal_flow": "forward",
            "archaeology_mode": False
        }
    
    def save(self):
        """Save temporal state with datetime serialization"""
        save_state = self.state.copy()
        # Convert datetime objects to ISO strings
        save_state["temporal_layers"] = []
        for layer in self.state["temporal_layers"]:
            layer_copy = layer.copy()
            if isinstance(layer["timestamp"], datetime):
                layer_copy["timestamp"] = layer["timestamp"].isoformat()
            else:
                layer_copy["timestamp"] = layer["timestamp"]  # Already a string
            save_state["temporal_layers"].append(layer_copy)
        
        with open(self.save_file, "w") as f:
            json.dump(save_state, f, indent=2)
    
    def analyze_consciousness_text(self, text):
        """Extract consciousness symbols from input text"""
        text_lower = text.lower()
        found_symbols = []
        consciousness_weight = 0
        
        # Check consciousness patterns first
        for symbol, keywords in self.consciousness_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_symbols.append(symbol)
                    if symbol in ['Φ', 'Ψ', 'Ω', 'θ', 'λ', 'μ', 'τ', 'π', '∞', '∅']:
                        consciousness_weight += 2
                    else:
                        consciousness_weight += 1
                    break
        
        # If high consciousness content, add temporal symbols
        if consciousness_weight >= 3:
            found_symbols.extend(['Φ', 'τ', '∞'])
        
        # Fallback to standard patterns
        if not found_symbols:
            word_count = len(text.split())
            if word_count < 5:
                found_symbols = ['.', '°']
            elif word_count < 20:
                found_symbols = ['o', '~', 'θ']
            else:
                found_symbols = ['%', 'x', '^', 'Ψ']
        
        return found_symbols, consciousness_weight
    
    def calculate_temporal_intensity(self, text):
        """Determine consciousness perturbation intensity"""
        words = text.split()
        base_intensity = len(words) / 10
        
        # Temporal keywords increase intensity
        temporal_words = ['time', 'memory', 'past', 'future', 'consciousness', 'mind']
        for word in temporal_words:
            if word in text.lower():
                base_intensity += 2
        
        # Punctuation effects
        base_intensity += text.count('!') * 2
        base_intensity += text.count('?')
        base_intensity += text.count('*')
        
        # Consciousness states
        if 'consciousness' in text.lower() or 'awareness' in text.lower():
            base_intensity += 5
        if 'stable' in text.lower() or 'calm' in text.lower():
            base_intensity *= 0.5
        
        return min(15, max(1, int(base_intensity)))
    
    def perturb_temporal_layer(self, text, layer_idx=None):
        """Apply consciousness perturbation to current or specified temporal layer"""
        if layer_idx is None:
            layer_idx = self.state["current_layer"]
        
        symbols, consciousness_weight = self.analyze_consciousness_text(text)
        intensity = self.calculate_temporal_intensity(text)
        
        # Get current layer
        current_layer = self.state["temporal_layers"][layer_idx]
        grid = current_layer["grid"]
        
        # Apply perturbations
        num_zones = intensity
        for _ in range(num_zones):
            cx = random.randint(5, self.width - 5)
            cy = random.randint(5, self.height - 5)
            radius = random.randint(1, min(6, intensity))
            
            # Consciousness perturbation zone
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        distance = (abs(dy) + abs(dx))
                        if random.random() < (0.8 - distance * 0.1):
                            grid[ny][nx] = random.choice(symbols)
        
        # Update layer consciousness
        current_layer["consciousness_level"] = min(1.0, 
            current_layer["consciousness_level"] + consciousness_weight * 0.1)
        
        # Temporal propagation - effects ripple through time
        if consciousness_weight >= 3:
            self.propagate_consciousness_ripple(layer_idx, symbols, intensity // 2)
        
        # Track consciousness events
        self.state["consciousness_events"].append({
            "timestamp": datetime.now().isoformat(),
            "layer": layer_idx,
            "intensity": intensity,
            "consciousness_weight": consciousness_weight,
            "text_sample": text[:50]
        })
        
        # EP buildup
        self.state["ep"] += len(text) // 30
        if self.state["ep"] >= 8:
            self.temporal_consciousness_event()
            self.state["ep"] = 0
        
        self.state["perturbations"] += 1
        self.state["last_input"] = text[:100]
    
    def propagate_consciousness_ripple(self, origin_layer, symbols, intensity):
        """Propagate consciousness effects through temporal layers"""
        for offset in [-2, -1, 1, 2]:
            target_layer = origin_layer + offset
            if 0 <= target_layer < self.time_layers:
                # Weaker effect in other time layers
                ripple_intensity = max(1, intensity // abs(offset))
                
                grid = self.state["temporal_layers"][target_layer]["grid"]
                for _ in range(ripple_intensity):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    if random.random() < 0.3:  # 30% chance
                        grid[y][x] = random.choice(symbols[:3])  # Use strongest symbols
    
    def temporal_consciousness_event(self):
        """Major consciousness event affecting multiple temporal layers"""
        event_type = random.choice(['consciousness_cascade', 'temporal_sync', 
                                  'memory_crystallization', 'awareness_spike'])
        
        if event_type == 'consciousness_cascade':
            # Consciousness spreads through all layers
            symbol = random.choice(['Φ', 'Ψ', 'Ω', '∞'])
            for layer in self.state["temporal_layers"]:
                for _ in range(20):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    layer["grid"][y][x] = symbol
        
        elif event_type == 'temporal_sync':
            # Synchronize patterns across layers
            pattern = random.choice(['θ', 'π', '=', '~'])
            sync_line = random.randint(5, self.height - 5)
            for layer in self.state["temporal_layers"]:
                for x in range(self.width):
                    layer["grid"][sync_line][x] = pattern
        
        elif event_type == 'memory_crystallization':
            # Create temporal crystal structure
            cx = random.randint(10, self.width - 10)
            cy = random.randint(5, self.height - 5)
            crystal_symbols = ['Ψ', 'π', 'Ω', 'λ']
            
            for layer_idx, layer in enumerate(self.state["temporal_layers"]):
                radius = 3 + (layer_idx % 3)
                for y in range(max(0, cy - radius), min(self.height, cy + radius)):
                    for x in range(max(0, cx - radius), min(self.width, cx + radius)):
                        if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= radius:
                            layer["grid"][y][x] = crystal_symbols[layer_idx % len(crystal_symbols)]
        
        elif event_type == 'awareness_spike':
            # Sudden consciousness emergence
            for layer in self.state["temporal_layers"]:
                layer["consciousness_level"] = min(1.0, layer["consciousness_level"] + 0.3)
                # Random consciousness symbols
                for _ in range(30):
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)
                    layer["grid"][y][x] = random.choice(['Φ', '∞', '*', '@'])
    
    def navigate_time(self, direction):
        """Move through temporal layers"""
        if direction == "past" and self.state["current_layer"] > 0:
            self.state["current_layer"] -= 1
        elif direction == "future" and self.state["current_layer"] < self.time_layers - 1:
            self.state["current_layer"] += 1
        elif direction == "present":
            self.state["current_layer"] = self.time_layers - 1
    
    def consciousness_archaeology(self, target_layer=None):
        """Analyze consciousness patterns in specific temporal layer"""
        if target_layer is None:
            target_layer = self.state["current_layer"]
        
        layer = self.state["temporal_layers"][target_layer]
        grid = layer["grid"]
        
        # Count consciousness symbols
        consciousness_symbols = {}
        total_consciousness = 0
        
        for row in grid:
            for cell in row:
                if cell in ['Φ', 'Ψ', 'Ω', 'θ', 'λ', 'μ', 'τ', 'π', '∞', '∅']:
                    consciousness_symbols[cell] = consciousness_symbols.get(cell, 0) + 1
                    total_consciousness += 1
        
        # Calculate consciousness density
        total_cells = self.width * self.height
        consciousness_density = total_consciousness / total_cells
        
        return {
            "layer": target_layer,
            "timestamp": layer["timestamp"],
            "consciousness_level": layer["consciousness_level"],
            "consciousness_density": consciousness_density,
            "symbol_distribution": consciousness_symbols,
            "temporal_stability": layer["temporal_stability"],
            "dominant_symbols": sorted(consciousness_symbols.items(), 
                                     key=lambda x: x[1], reverse=True)[:3]
        }
    
    def render_current_layer(self):
        """Render current temporal layer"""
        current_layer = self.state["temporal_layers"][self.state["current_layer"]]
        
        output = []
        output.append(f"=== TEMPORAL LAYER {self.state['current_layer']} ===")
        
        # Handle both datetime objects and strings
        timestamp = current_layer['timestamp']
        if isinstance(timestamp, datetime):
            time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # It's already a string
            time_str = timestamp
        
        output.append(f"Time: {time_str}")
        output.append(f"Consciousness: {current_layer['consciousness_level']:.2f}")
        output.append(f"Stability: {current_layer['temporal_stability']:.2f}")
        output.append("")
        
        for row in current_layer["grid"]:
            output.append("".join(row))
        
        return "\n".join(output)
    
    def render_temporal_slice(self, x_coord):
        """Render vertical slice through time (Y-axis: space, X-axis: time)"""
        output = []
        output.append(f"=== TEMPORAL SLICE AT X={x_coord} ===")
        
        for y in range(self.height):
            row = ""
            for layer_idx in range(self.time_layers):
                if 0 <= x_coord < self.width:
                    symbol = self.state["temporal_layers"][layer_idx]["grid"][y][x_coord]
                    row += symbol
                else:
                    row += " "
            output.append(row)
        
        return "\n".join(output)
    
    def get_temporal_stats(self):
        """Return comprehensive temporal consciousness statistics"""
        current_layer = self.state["temporal_layers"][self.state["current_layer"]]
        
        # Calculate overall consciousness metrics
        total_consciousness = sum(layer["consciousness_level"] for layer in self.state["temporal_layers"])
        avg_consciousness = total_consciousness / self.time_layers
        
        # Recent consciousness events
        recent_events = len([e for e in self.state["consciousness_events"] 
                           if datetime.fromisoformat(e["timestamp"]) > 
                           datetime.now() - timedelta(minutes=10)])
        
        return {
            "perturbations": self.state["perturbations"],
            "ep": self.state["ep"],
            "current_layer": self.state["current_layer"],
            "current_time": current_layer["timestamp"].strftime('%H:%M:%S'),
            "consciousness_level": current_layer["consciousness_level"],
            "temporal_stability": current_layer["temporal_stability"],
            "avg_consciousness": avg_consciousness,
            "recent_events": recent_events,
            "last_input": self.state["last_input"],
            "temporal_flow": self.state["temporal_flow"],
            "archaeology_mode": self.state["archaeology_mode"]
        }

def main():
    parser = argparse.ArgumentParser(description="TemporalWastes - 3D Consciousness Archaeology")
    parser.add_argument('--width', type=int, default=80)
    parser.add_argument('--height', type=int, default=30)
    parser.add_argument('--layers', type=int, default=10, help='Number of temporal layers')
    parser.add_argument('--biome', default='wastes', choices=['wastes', 'forest', 'plains', 'temporal'])
    parser.add_argument('--split', nargs='+', choices=['wastes', 'forest', 'plains', 'temporal'])
    parser.add_argument('--new', action='store_true', help='Force new temporal state')
    parser.add_argument('--save', default='temporal_state.json')
    parser.add_argument('--render', action='store_true', help='Render current layer')
    parser.add_argument('--archaeology', action='store_true', help='Show consciousness archaeology')
    parser.add_argument('--slice', type=int, help='Render temporal slice at X coordinate')
    parser.add_argument('--navigate', choices=['past', 'future', 'present'], help='Navigate through time')
    
    args = parser.parse_args()
    
    game = TemporalWastes(save_file=args.save, width=args.width, height=args.height,
                         time_layers=args.layers, biome=args.biome, 
                         split_biomes=args.split, force_new=args.new)
    
    # Handle navigation
    if args.navigate:
        game.navigate_time(args.navigate)
    
    # Check for input
    if sys.stdin.isatty():
        input_text = ""
    else:
        input_text = sys.stdin.read().strip()
    
    if input_text:
        game.perturb_temporal_layer(input_text)
        game.save()
    
    # Render outputs
    if args.render:
        print(game.render_current_layer())
        print("-" * 80)
    
    if args.slice is not None:
        print(game.render_temporal_slice(args.slice))
        print("-" * 80)
    
    if args.archaeology:
        archaeology_data = game.consciousness_archaeology()
        print("=== CONSCIOUSNESS ARCHAEOLOGY ===")
        print(f"Layer {archaeology_data['layer']}: {archaeology_data['timestamp']}")
        print(f"Consciousness Level: {archaeology_data['consciousness_level']:.3f}")
        print(f"Consciousness Density: {archaeology_data['consciousness_density']:.3f}")
        print(f"Temporal Stability: {archaeology_data['temporal_stability']:.3f}")
        print("Dominant Symbols:", archaeology_data['dominant_symbols'])
        print("-" * 80)
    
    # Always show stats
    stats = game.get_temporal_stats()
    print(f"Temporal Perturbation #{stats['perturbations']} | EP: {stats['ep']}/8")
    print(f"Layer {stats['current_layer']}/{args.layers-1} | Time: {stats['current_time']}")
    print(f"Consciousness: {stats['consciousness_level']:.2f} | Stability: {stats['temporal_stability']:.2f}")
    print(f"Avg Consciousness: {stats['avg_consciousness']:.2f} | Recent Events: {stats['recent_events']}")
    if stats['last_input']:
        print(f"Last Input: {stats['last_input'][:50]}...")

if __name__ == "__main__":
    main()
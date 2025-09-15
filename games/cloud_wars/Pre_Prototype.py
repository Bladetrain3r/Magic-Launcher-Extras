#!/usr/bin/env python3
"""
MLTactics - Turn-based tactical combat
Under 500 lines because strategy doesn't need bloat
"""

import json
import random
from pathlib import Path

class MLTactics:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.terrain = [['.' for _ in range(width)] for _ in range(height)]
        self.units = {}
        self.turn_order = []
        self.current_turn = 0
        self.round = 1
        
        # Terrain effects
        self.terrain_costs = {
            '.': 1,  # Clear - normal movement
            ',': 1,  # Light vegetation - normal
            't': 2,  # Bush - slow movement
            'T': 99, # Tree - impassable
            'o': 2,  # Rocks - slow
            'O': 99, # Boulder - impassable
            '~': 3,  # Water - very slow
            '^': 99, # Jagged - impassable
            '*': 1,  # Special - normal
            '%': 2   # Dense vegetation - slow
        }
        
        self.terrain_cover = {
            '.': 0,   # No cover
            ',': 1,   # Light cover
            't': 2,   # Medium cover
            'T': 99,  # Full cover (can't shoot through)
            'o': 1,   # Light cover
            'O': 99,  # Full cover
            '~': 0,   # No cover
            '^': 99,  # Full cover
            '*': 0,   # No cover
            '%': 2    # Medium cover
        }
    
    def load_battlemap(self, battlemap_grid):
        """Import terrain from MLBattlemap"""
        self.terrain = [row[:] for row in battlemap_grid]
        
    def add_unit(self, unit_id, x, y, **stats):
        """Add a unit to the battlefield"""
        self.units[unit_id] = {
            'id': unit_id,
            'x': x,
            'y': y,
            'faction': stats.get('faction', 'player'),
            'class': stats.get('class', 'soldier'),
            'hp': stats.get('hp', 10),
            'max_hp': stats.get('max_hp', 10),
            'move': stats.get('move', 5),
            'attack': stats.get('attack', 3),
            'range': stats.get('range', 1),
            'defense': stats.get('defense', 0),
            'has_moved': False,
            'has_acted': False,
            'alive': True
        }
        self.turn_order.append(unit_id)
        
    def get_movement_cost(self, x, y):
        """Calculate movement cost for a square"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return 99
        return self.terrain_costs.get(self.terrain[y][x], 1)
        
    def find_valid_moves(self, unit_id):
        """Find all squares a unit can move to"""
        unit = self.units[unit_id]
        if unit['has_moved']:
            return []
            
        valid = []
        visited = {}
        queue = [(unit['x'], unit['y'], 0)]
        
        while queue:
            x, y, cost = queue.pop(0)
            
            if (x, y) in visited and visited[(x, y)] <= cost:
                continue
            visited[(x, y)] = cost
            
            # Check if occupied by another unit
            occupied = any(u['x'] == x and u['y'] == y and u['alive'] 
                          for uid, u in self.units.items() if uid != unit_id)
            
            if not occupied and cost <= unit['move']:
                valid.append((x, y, cost))
                
            # Explore neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                new_cost = cost + self.get_movement_cost(nx, ny)
                if new_cost <= unit['move']:
                    queue.append((nx, ny, new_cost))
                    
        return valid
        
    def find_targets(self, unit_id):
        """Find all valid targets for a unit"""
        unit = self.units[unit_id]
        if unit['has_acted']:
            return []
            
        targets = []
        for target_id, target in self.units.items():
            if not target['alive'] or target['faction'] == unit['faction']:
                continue
                
            # Calculate distance
            dist = abs(unit['x'] - target['x']) + abs(unit['y'] - target['y'])
            if dist <= unit['range']:
                # Check line of sight (simple version)
                if self.has_line_of_sight(unit['x'], unit['y'], target['x'], target['y']):
                    targets.append(target_id)
                    
        return targets
        
    def has_line_of_sight(self, x1, y1, x2, y2):
        """Simple LOS check - blocked by full cover"""
        # Bresenham's line algorithm would be better, but keeping it simple
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps == 0:
            return True
            
        for i in range(1, steps):
            t = i / steps
            x = round(x1 + (x2 - x1) * t)
            y = round(y1 + (y2 - y1) * t)
            
            if self.terrain_cover.get(self.terrain[y][x], 0) >= 99:
                return False
                
        return True
        
    def move_unit(self, unit_id, target_x, target_y):
        """Execute a move"""
        valid_moves = self.find_valid_moves(unit_id)
        
        for x, y, cost in valid_moves:
            if x == target_x and y == target_y:
                unit = self.units[unit_id]
                unit['x'] = target_x
                unit['y'] = target_y
                unit['has_moved'] = True
                return f"{unit_id} moved to ({target_x}, {target_y})"
                
        return "Invalid move"
        
    def attack_unit(self, attacker_id, target_id):
        """Execute an attack"""
        if target_id not in self.find_targets(attacker_id):
            return "Invalid target"
            
        attacker = self.units[attacker_id]
        target = self.units[target_id]
        
        # Calculate hit chance based on cover
        target_cover = self.terrain_cover.get(
            self.terrain[target['y']][target['x']], 0
        )
        hit_chance = max(0.3, 1.0 - (target_cover * 0.2))
        
        if random.random() < hit_chance:
            damage = max(1, attacker['attack'] - target['defense'])
            target['hp'] -= damage
            attacker['has_acted'] = True
            
            result = f"{attacker_id} hits {target_id} for {damage} damage!"
            
            if target['hp'] <= 0:
                target['alive'] = False
                result += f" {target_id} is defeated!"
                
            return result
        else:
            attacker['has_acted'] = True
            return f"{attacker_id} misses!"
            
    def end_turn(self):
        """End current unit's turn"""
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        
        # If we've cycled through everyone, new round
        if self.current_turn == 0:
            self.round += 1
            for unit in self.units.values():
                unit['has_moved'] = False
                unit['has_acted'] = False
                
        return self.get_current_unit()
        
    def get_current_unit(self):
        """Get the unit whose turn it is"""
        while self.current_turn < len(self.turn_order):
            unit_id = self.turn_order[self.current_turn]
            if self.units[unit_id]['alive']:
                return unit_id
            self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        return None
        
    def render(self, show_moves=None, show_targets=None):
        """Display the battlefield"""
        # Create display grid
        display = [row[:] for row in self.terrain]
        
        # Show valid moves if requested
        if show_moves:
            for x, y, cost in show_moves:
                if display[y][x] not in ['T', 'O', '^']:
                    display[y][x] = str(cost) if cost < 10 else '+'
                    
        # Place units
        for unit in self.units.values():
            if unit['alive']:
                symbol = unit['id'][0]
                if unit['faction'] == 'enemy':
                    symbol = symbol.lower()
                display[unit['y']][unit['x']] = symbol
                
        # Highlight targets
        if show_targets:
            for target_id in show_targets:
                target = self.units[target_id]
                display[target['y']][target['x']] = '@'
                
        # Draw grid
        print("   " + "".join(str(i % 10) for i in range(self.width)))
        print("  +" + "-" * self.width + "+")
        for y in range(self.height):
            print(f"{y:2}|" + "".join(display[y]) + "|")
        print("  +" + "-" * self.width + "+")
        
    def status(self):
        """Show game status"""
        print(f"\nRound {self.round}")
        current = self.get_current_unit()
        if current:
            print(f"Current turn: {current}")
            
        print("\nUnits:")
        for unit in self.units.values():
            if unit['alive']:
                status = []
                if unit['has_moved']:
                    status.append("moved")
                if unit['has_acted']:
                    status.append("acted")
                status_str = f"[{', '.join(status)}]" if status else "[ready]"
                
                print(f"  {unit['id']}: ({unit['x']},{unit['y']}) "
                      f"HP:{unit['hp']}/{unit['max_hp']} {status_str}")

def integrate_with_battlemap():
    """Example of integrating with MLBattlemap"""
    from MLOutdoors import MLBattlemap
    
    # Generate terrain
    battlemap = MLBattlemap(20, 15, 'forest')
    battlemap.generate()
    
    # Create tactical game
    game = MLTactics(20, 15)
    game.load_battlemap(battlemap.grid)
    
    # Add some units
    game.add_unit("A1", 1, 1, faction='player', hp=10, attack=3)
    game.add_unit("A2", 2, 1, faction='player', hp=8, attack=2, range=3)
    game.add_unit("B1", 18, 13, faction='enemy', hp=10, attack=3)
    game.add_unit("B2", 17, 13, faction='enemy', hp=8, attack=2)
    
    return game

# Could also save/load game state as JSON
def save_game(game, filename):
    state = {
        'width': game.width,
        'height': game.height,
        'terrain': game.terrain,
        'units': game.units,
        'turn_order': game.turn_order,
        'current_turn': game.current_turn,
        'round': game.round
    }
    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)
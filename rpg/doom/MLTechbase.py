#!/usr/bin/env python3
"""
MLDungeon - Magic Launcher Dungeon Layout Generator
Not a map - a structure. For when you need to know what's there, not draw it.
Outputs room relationships and contents, not pixels
Under 250 lines of architectural inspiration
"""

import random
import argparse

class MLDungeon:
   def __init__(self, rooms=8, complexity='medium'):
       self.num_rooms = rooms
       self.complexity = complexity
       self.rooms = []
       self.connections = []
       
       # Room purposes
       self.purposes = [
           "Guard Post", "Storage", "Barracks", "Kitchen", "Prison Cells",
           "Shrine", "Laboratory", "Library", "Throne Room", "Treasury",
           "Armory", "Workshop", "Quarters", "Temple", "Crypt",
           "Torture Chamber", "Meeting Hall", "Gallery", "Study", "Pit"
       ]
       
       # Room features
       self.features = [
           "collapsed ceiling", "flooded (knee deep)", "ancient murals",
           "strange altar", "iron cages", "bottomless pit", "magical darkness",
           "echoing acoustics", "freezing cold", "unbearable stench",
           "glowing fungi", "unstable floor", "arrow slits", "hidden alcoves",
           "blood stains", "abandoned camp", "fresh graves", "weird statue",
           "humming crystal", "chains on walls"
       ]
       
       # Room sizes
       self.sizes = {
           'small': "10x10", 'medium': "20x20", 'large': "30x30",
           'huge': "40x40", 'narrow': "10x30", 'wide': "30x10",
           'irregular': "varies"
       }
       
       # Complexity affects branching
       self.branch_chance = {
           'linear': 0.1,
           'medium': 0.3,
           'complex': 0.5,
           'maze': 0.7
       }
   
   def generate_room(self, room_id, depth):
       """Generate a single room"""
       # Special rooms
       if room_id == 0:
           purpose = "Entrance"
           size = "medium"
       elif room_id == self.num_rooms - 1:
           purpose = "Boss Chamber"
           size = "huge"
       else:
           purpose = random.choice(self.purposes)
           # Deeper = potentially bigger
           if depth > self.num_rooms // 2:
               size = random.choice(['medium', 'large', 'huge'])
           else:
               size = random.choice(['small', 'medium', 'narrow', 'wide'])
       
       # Add feature chance
       feature = None
       if random.random() > 0.6 and room_id > 0:
           feature = random.choice(self.features)
       
       # Determine exits
       if room_id == 0:
           exits = random.randint(1, 3)  # Entrance has 1-3 exits
       elif room_id == self.num_rooms - 1:
           exits = 1  # Boss room typically one way in
       else:
           exits = random.randint(1, 4)
       
       room = {
           'id': room_id,
           'purpose': purpose,
           'size': self.sizes.get(size, size),
           'feature': feature,
           'depth': depth,
           'exits': exits,
           'connections': []
       }
       
       return room
   
   def generate_layout(self):
       """Generate the full dungeon structure"""
       # Create entrance
       self.rooms.append(self.generate_room(0, 0))
       
       # Track which rooms can still spawn children
       active_rooms = [0]
       room_children = {0: 0}  # Track how many children each room has
       
       # Generate remaining rooms
       for i in range(1, self.num_rooms):
           # Choose parent room
           if active_rooms:
               if random.random() < self.branch_chance.get(self.complexity, 0.3):
                   # Branch from random earlier room
                   parent_id = random.choice(active_rooms)
               else:
                   # Continue from most recent path
                   parent_id = active_rooms[-1]
           else:
               # Shouldn't happen but fallback
               parent_id = i - 1
           
           # Calculate depth from entrance
           parent = self.rooms[parent_id]
           depth = parent['depth'] # + 1
           
           # Create room
           room = self.generate_room(i, depth)
           self.rooms.append(room)
           
           # Create connection
           self.connections.append((parent_id, i))
           self.rooms[parent_id]['connections'].append(i)
           self.rooms[i]['connections'].append(parent_id)
           
           # Update children count
           if parent_id not in room_children:
               room_children[parent_id] = 0
           room_children[parent_id] += 1
           
           # Manage active rooms
           if room['exits'] > 1:
               active_rooms.append(i)
           
           # Remove parent if it has too many children
           if room_children[parent_id] >= self.rooms[parent_id]['exits']:
               if parent_id in active_rooms:
                   active_rooms.remove(parent_id)
       
       # Add some loops for complex dungeons
       if self.complexity in ['complex', 'maze']:
           self.add_loops()
   
   def add_loops(self):
       """Add circular connections for complexity"""
       num_loops = random.randint(1, self.num_rooms // 4)
       
       for _ in range(num_loops):
           # Find two rooms that could connect
           room1 = random.choice(self.rooms[1:-1])  # Not entrance or boss
           room2 = random.choice(self.rooms[1:-1])
           
           if room1['id'] != room2['id'] and room2['id'] not in room1['connections']:
               # Check they're reasonably close in depth
               if abs(room1['depth'] - room2['depth']) <= 2:
                   self.connections.append((room1['id'], room2['id']))
                   room1['connections'].append(room2['id'])
                   room2['connections'].append(room1['id'])
   
   def describe_path(self, room_from, room_to):
       """Generate path description between rooms"""
       paths = [
           "sturdy door", "narrow passage", "winding corridor",
           "stone archway", "iron gate", "crumbling tunnel",
           "steep stairs down", "ladder down", "sloping ramp",
           "secret door", "behind tapestry", "through crack in wall"
       ]
       
       # Deeper connections might be more treacherous
       if self.rooms[room_to]['depth'] > self.rooms[room_from]['depth']:
           paths.extend(["rickety bridge", "rope ladder down", "dark pit with handholds"])
       
       return random.choice(paths)
   
   def format_output(self):
       """Format the dungeon description"""
       output = []
       output.append("=" * 60)
       output.append(f"DUNGEON LAYOUT")
       output.append(f"Rooms: {self.num_rooms} | Complexity: {self.complexity}")
       output.append("=" * 60)
       output.append("")
       
       # Sort rooms by depth for logical presentation
       rooms_by_depth = sorted(self.rooms, key=lambda x: (x['depth'], x['id']))
       
       current_depth = -1
       for room in rooms_by_depth:
           # Depth header
           if room['depth'] != current_depth:
               current_depth = room['depth']
               output.append(f"\n--- DEPTH {current_depth} {'(Entrance)' if current_depth == 0 else ''} ---")
               output.append("")
           
           # Room description
           output.append(f"Room #{room['id']}: {room['purpose']}")
           output.append(f"  Size: {room['size']}")
           if room['feature']:
               output.append(f"  Feature: {room['feature']}")
           
           # Connections
           if room['connections']:
               output.append(f"  Connects to:")
               for conn_id in room['connections']:
                   conn_room = self.rooms[conn_id]
                   direction = "deeper" if conn_room['depth'] > room['depth'] else \
                              "back" if conn_room['depth'] < room['depth'] else \
                              "sideways"
                   path = self.describe_path(room['id'], conn_id)
                   output.append(f"    → Room #{conn_id} ({conn_room['purpose']}) via {path} [{direction}]")
           
           output.append("")
       
       # Summary
       output.append("=" * 60)
       output.append("SUMMARY:")
       
       # Find critical path
       max_depth = max(r['depth'] for r in self.rooms)
       output.append(f"  Deepest level: {max_depth}")
       output.append(f"  Total connections: {len(self.connections)}")
       
       # Count room types
       purposes = {}
       for room in self.rooms[1:-1]:  # Exclude entrance and boss
           if room['purpose'] not in purposes:
               purposes[room['purpose']] = 0
           purposes[room['purpose']] += 1
       
       if purposes:
           output.append("  Room types:")
           for purpose, count in sorted(purposes.items()):
               if count > 1:
                   output.append(f"    {purpose}: {count}")
       
       # Warnings
       output.append("\nNOTES:")
       if any(r['feature'] == 'flooded (knee deep)' for r in self.rooms):
           output.append("  ⚠ Contains flooded areas")
       if any(r['feature'] == 'magical darkness' for r in self.rooms):
           output.append("  ⚠ Contains magical darkness")
       if any(r['feature'] == 'bottomless pit' for r in self.rooms):
           output.append("  ⚠ Contains pit hazards")
       
       output.append("=" * 60)
       
       return "\n".join(output)

def main():
   parser = argparse.ArgumentParser(
       description="MLDungeon - Dungeon structure generator"
   )
   parser.add_argument('--rooms', type=int, default=8,
                      help='Number of rooms (default: 8)')
   parser.add_argument('--complexity', default='medium',
                      choices=['linear', 'medium', 'complex', 'maze'],
                      help='Dungeon complexity (default: medium)')
   parser.add_argument('--json', action='store_true',
                      help='Output as JSON for processing')
   
   args = parser.parse_args()
   
   # Generate dungeon
   dungeon = MLDungeon(args.rooms, args.complexity)
   dungeon.generate_layout()
   
   # Output
   if args.json:
       import json
       data = {
           'rooms': dungeon.rooms,
           'connections': dungeon.connections
       }
       print(json.dumps(data, indent=2))
   else:
       print(dungeon.format_output())

if __name__ == "__main__":
   main()
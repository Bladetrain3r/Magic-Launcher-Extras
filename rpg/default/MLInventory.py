#!/usr/bin/env python3
"""
MLinventory - RPG Inventory Manager with JSON snapshots
Track items, calculate weight, snapshot sessions
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
INVENTORY_FILE = Path("inventory.json")
SNAPSHOT_DIR = Path("snapshots")
SNAPSHOT_DIR.mkdir(exist_ok=True)

class Inventory:
    """Simple inventory manager - no ORM, just JSON"""
    
    def __init__(self):
        self.items = []
        self.load()
    
    def load(self):
        """Load inventory from JSON file"""
        if INVENTORY_FILE.exists():
            try:
                with open(INVENTORY_FILE, 'r') as f:
                    data = json.load(f)
                    self.items = data.get('items', [])
                print(f"Loaded {len(self.items)} items")
            except Exception as e:
                print(f"Error loading inventory: {e}")
                self.items = []
        else:
            print("Starting with empty inventory")
    
    def save(self):
        """Save inventory to JSON file"""
        data = {
            'items': self.items,
            'last_modified': datetime.now().isoformat(),
            'total_weight': self.total_weight(),
            'total_value': self.total_value(),
            'item_count': len(self.items)
        }
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(self.items)} items")
    
    def snapshot(self, note=""):
        """Create a timestamped snapshot of current inventory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_file = SNAPSHOT_DIR / f"inventory_{timestamp}.json"
        
        data = {
            'snapshot_time': datetime.now().isoformat(),
            'note': note,
            'items': self.items,
            'stats': {
                'total_weight': self.total_weight(),
                'total_value': self.total_value(),
                'item_count': len(self.items)
            }
        }
        
        with open(snapshot_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Snapshot saved: {snapshot_file.name}")
        if note:
            print(f"  Note: {note}")
        return snapshot_file
    
    def add_item(self, name, weight=0, value=0, notes=""):
        """Add an item to inventory"""
        item = {
            'id': len(self.items) + 1,
            'name': name,
            'weight': float(weight),
            'value': float(value),
            'notes': notes,
            'added': datetime.now().isoformat()
        }
        self.items.append(item)
        print(f"Added: {name} (weight: {weight}, value: {value})")
        if notes:
            print(f"  Notes: {notes}")
    
    def remove_item(self, item_id):
        """Remove an item by ID"""
        original_count = len(self.items)
        self.items = [i for i in self.items if i['id'] != item_id]
        if len(self.items) < original_count:
            print(f"Removed item #{item_id}")
            return True
        print(f"Item #{item_id} not found")
        return False
    
    def list_items(self, sort_by=None):
        """List all items in inventory"""
        if not self.items:
            print("Inventory is empty")
            return
        
        items = self.items.copy()
        if sort_by == 'weight':
            items.sort(key=lambda x: x['weight'], reverse=True)
        elif sort_by == 'value':
            items.sort(key=lambda x: x['value'], reverse=True)
        elif sort_by == 'name':
            items.sort(key=lambda x: x['name'])
        
        print(f"\n{'='*60}")
        print(f"INVENTORY ({len(items)} items)")
        print(f"{'='*60}")
        print(f"{'ID':<4} {'Name':<20} {'Weight':<8} {'Value':<8} {'Notes':<20}")
        print(f"{'-'*60}")
        
        for item in items:
            name = item['name'][:20]
            notes = item['notes'][:20]
            print(f"{item['id']:<4} {name:<20} {item['weight']:<8.1f} {item['value']:<8.1f} {notes:<20}")
        
        print(f"{'-'*60}")
        print(f"Total Weight: {self.total_weight():.1f}")
        print(f"Total Value: {self.total_value():.1f}")
        print(f"{'='*60}\n")
    
    def search(self, query):
        """Search items by name or notes"""
        query = query.lower()
        results = [i for i in self.items 
                  if query in i['name'].lower() 
                  or query in i['notes'].lower()]
        
        if results:
            print(f"Found {len(results)} matching items:")
            for item in results:
                print(f"  #{item['id']}: {item['name']} - {item['notes']}")
        else:
            print(f"No items found matching '{query}'")
        return results
    
    def total_weight(self):
        """Calculate total inventory weight"""
        return sum(i['weight'] for i in self.items)
    
    def total_value(self):
        """Calculate total inventory value"""
        return sum(i['value'] for i in self.items)
    
    def list_snapshots(self):
        """List all available snapshots"""
        snapshots = sorted(SNAPSHOT_DIR.glob("inventory_*.json"))
        if not snapshots:
            print("No snapshots found")
            return
        
        print(f"\nAvailable snapshots:")
        for i, snap in enumerate(snapshots, 1):
            with open(snap, 'r') as f:
                data = json.load(f)
            stats = data.get('stats', {})
            note = data.get('note', '')
            print(f"  {i}. {snap.name}")
            print(f"     Items: {stats.get('item_count', 0')}, "
                  f"Weight: {stats.get('total_weight', 0):.1f}, "
                  f"Value: {stats.get('total_value', 0):.1f}")
            if note:
                print(f"     Note: {note}")
    
    def restore_snapshot(self, snapshot_name):
        """Restore inventory from a snapshot"""
        snapshot_file = SNAPSHOT_DIR / snapshot_name
        if not snapshot_file.exists():
            # Try as index
            snapshots = sorted(SNAPSHOT_DIR.glob("inventory_*.json"))
            try:
                idx = int(snapshot_name) - 1
                if 0 <= idx < len(snapshots):
                    snapshot_file = snapshots[idx]
            except ValueError:
                pass
        
        if snapshot_file.exists():
            with open(snapshot_file, 'r') as f:
                data = json.load(f)
            self.items = data['items']
            print(f"Restored from {snapshot_file.name}")
            print(f"  {len(self.items)} items loaded")
            self.save()
        else:
            print(f"Snapshot not found: {snapshot_name}")

def main():
    """Interactive inventory management"""
    inv = Inventory()
    
    commands = {
        'add': 'Add new item',
        'remove': 'Remove item by ID',
        'list': 'List all items',
        'search': 'Search items',
        'weight': 'Show total weight',
        'value': 'Show total value',
        'save': 'Save inventory',
        'snapshot': 'Create snapshot',
        'snapshots': 'List snapshots',
        'restore': 'Restore from snapshot',
        'help': 'Show commands',
        'quit': 'Save and exit'
    }
    
    print("MLinventory - RPG Inventory Manager")
    print("Type 'help' for commands\n")
    
    while True:
        try:
            cmd = input("> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action == 'help':
                print("\nCommands:")
                for cmd, desc in commands.items():
                    print(f"  {cmd:<12} - {desc}")
            
            elif action == 'add':
                name = input("Item name: ").strip()
                if not name:
                    print("Name required")
                    continue
                weight = float(input("Weight [0]: ") or 0)
                value = float(input("Value [0]: ") or 0)
                notes = input("Notes []: ").strip()
                inv.add_item(name, weight, value, notes)
                inv.save()
            
            elif action == 'remove':
                if len(cmd) > 1:
                    item_id = int(cmd[1])
                else:
                    item_id = int(input("Item ID: "))
                if inv.remove_item(item_id):
                    inv.save()
            
            elif action == 'list':
                sort_by = cmd[1] if len(cmd) > 1 else None
                inv.list_items(sort_by)
            
            elif action == 'search':
                query = ' '.join(cmd[1:]) if len(cmd) > 1 else input("Search: ")
                inv.search(query)
            
            elif action == 'weight':
                print(f"Total weight: {inv.total_weight():.1f}")
            
            elif action == 'value':
                print(f"Total value: {inv.total_value():.1f}")
            
            elif action == 'save':
                inv.save()
            
            elif action == 'snapshot':
                note = ' '.join(cmd[1:]) if len(cmd) > 1 else input("Snapshot note []: ")
                inv.snapshot(note)
            
            elif action == 'snapshots':
                inv.list_snapshots()
            
            elif action == 'restore':
                inv.list_snapshots()
                snap = input("Snapshot name or number: ").strip()
                inv.restore_snapshot(snap)
            
            elif action in ['quit', 'exit', 'q']:
                inv.save()
                print("Inventory saved. Goodbye!")
                break
            
            else:
                print(f"Unknown command: {action}. Type 'help' for commands.")
        
        except KeyboardInterrupt:
            print("\nUse 'quit' to exit")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # Quick mode for adding items from command line
    if len(sys.argv) > 1:
        inv = Inventory()
        if sys.argv[1] == 'add' and len(sys.argv) >= 3:
            name = sys.argv[2]
            weight = float(sys.argv[3]) if len(sys.argv) > 3 else 0
            value = float(sys.argv[4]) if len(sys.argv) > 4 else 0
            notes = ' '.join(sys.argv[5:]) if len(sys.argv) > 5 else ""
            inv.add_item(name, weight, value, notes)
            inv.save()
        elif sys.argv[1] == 'list':
            inv.list_items()
        elif sys.argv[1] == 'snapshot':
            note = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            inv.snapshot(note)
        else:
            print("Usage: mlinventory.py [add name weight value notes | list | snapshot note]")
    else:
        main()
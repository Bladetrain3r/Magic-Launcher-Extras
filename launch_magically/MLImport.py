#!/usr/bin/env python3
"""
MLImport - Magic Launcher bulk import tool
Takes line-separated JSON entries and creates an Import folder
For when you need to add 20 Doom WADs at once
"""

import sys
import json
from pathlib import Path

def import_shortcuts(input_file=None):
   """Import shortcuts from line-separated JSON"""
   
   # Config location
   config_file = Path.home() / '.config' / 'launcher' / 'shortcuts.json'
   
   # Load existing config
   shortcuts = {}
   if config_file.exists():
       try:
           with open(config_file, 'r', encoding='utf-8') as f:
               shortcuts = json.load(f)
       except Exception as e:
           print(f"Warning: Could not load existing config: {e}")
           shortcuts = {}
   else:
       config_file.parent.mkdir(parents=True, exist_ok=True)
   
   # Create Import folder structure
   if "Import" not in shortcuts:
       shortcuts["Import"] = {
           "type": "folder",
           "items": {}
       }
   
   import_items = shortcuts["Import"]["items"]
   
   # Read input (stdin or file)
   if input_file and Path(input_file).exists():
       with open(input_file, 'r', encoding='utf-8') as f:
           lines = f.readlines()
   else:
       print("Paste JSON entries (one per line), Ctrl+D when done:")
       lines = sys.stdin.readlines()
   
   # Process each line
   imported = 0
   failed = 0
   
   for line_num, line in enumerate(lines, 1):
       line = line.strip()
       if not line:
           continue
           
       try:
           # Parse JSON
           entry = json.loads(line)
           
           # Extract fields
           name = entry.get('name')
           path = entry.get('path')
           
           if not name or not path:
               print(f"Line {line_num}: Missing name or path")
               failed += 1
               continue
           
           # Build shortcut
           shortcut = {
               "type": "shortcut",
               "path": path
           }
           
           # Optional fields
           if 'args' in entry and entry['args']:
               shortcut['args'] = entry['args']
           if 'icon' in entry and entry['icon']:
               shortcut['icon'] = entry['icon']
           
           # Add to import folder
           import_items[name] = shortcut
           imported += 1
           print(f"✓ Imported: {name}")
           
       except json.JSONDecodeError as e:
           print(f"Line {line_num}: Invalid JSON - {e}")
           failed += 1
       except Exception as e:
           print(f"Line {line_num}: Error - {e}")
           failed += 1
   
   # Save if we imported anything
   if imported > 0:
       # Backup existing
       if config_file.exists():
           backup = config_file.with_suffix('.json.bak')
           backup.write_text(config_file.read_text())
           print(f"\nBacked up existing config to {backup}")
       
       # Save updated config
       with open(config_file, 'w', encoding='utf-8') as f:
           json.dump(shortcuts, f, indent=2)
       
       print(f"\n✅ Imported {imported} shortcuts to Import folder")
       print(f"📁 Config saved to {config_file}")
   
   if failed > 0:
       print(f"\n⚠️  {failed} entries failed to import")
   
   return imported, failed

def main():
   """Main entry point"""
   if len(sys.argv) > 1:
       if sys.argv[1] in ['-h', '--help']:
           print("""MLImport - Bulk import Magic Launcher shortcuts

Usage: 
   mlimport [file]      Import from file
   mlimport            Import from stdin
   
Format (one JSON object per line):
   {"name": "Doom", "path": "/usr/games/doom", "args": "-iwad doom.wad"}
   {"name": "Doom II", "path": "/usr/games/doom", "args": "-iwad doom2.wad"}
   {"name": "Heretic", "path": "/usr/games/heretic"}
   
All shortcuts will be added to an "Import" folder.
Optional fields: args, icon""")
           return
       
       # Import from file
       import_shortcuts(sys.argv[1])
   else:
       # Import from stdin
       import_shortcuts()

if __name__ == "__main__":
   main()
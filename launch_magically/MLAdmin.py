#!/usr/bin/env python3
"""
MLAdmin - Magic Launcher shortcut editor
Because editing JSON by hand gets old
Separate from MLMenu because running and configuring are different jobs
"""

import os
import sys
import json
from pathlib import Path

# Same key input and colors from MLMenu
try:
    import msvcrt
    def get_key():
        return msvcrt.getch().decode('utf-8', errors='ignore').lower()
except ImportError:
    import termios, tty
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key.lower()

class Colors:
    BLUE = '\033[44m' if os.name != 'nt' else ''
    WHITE = '\033[97m' if os.name != 'nt' else ''
    YELLOW = '\033[93m' if os.name != 'nt' else ''
    GREEN = '\033[92m' if os.name != 'nt' else ''
    RED = '\033[91m' if os.name != 'nt' else ''
    RESET = '\033[0m' if os.name != 'nt' else ''
    
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

class MLAdmin:
    def __init__(self):
        self.config_file = Path.home() / '.config' / 'launcher' / 'shortcuts.json'
        self.shortcuts = {}
        self.current_path = []
        self.load_shortcuts()
        self.modified = False
    
    def load_shortcuts(self):
        """Load existing shortcuts"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.shortcuts = json.load(f)
            except:
                self.shortcuts = {}
        else:
            self.shortcuts = {}
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
    
    def save_shortcuts(self):
        """Save shortcuts to disk"""
        try:
            # Backup existing
            if self.config_file.exists():
                backup = self.config_file.with_suffix('.json.bak')
                backup.write_text(self.config_file.read_text())
            
            # Save new
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.shortcuts, f, indent=2)
            
            self.modified = False
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def get_current_items(self):
        """Get items in current location"""
        current = self.shortcuts
        for folder in self.current_path:
            current = current[folder]["items"]
        return current
    
    def add_shortcut(self):
        """Add a new shortcut"""
        Colors.clear()
        print("=== Add New Shortcut ===\n")
        
        name = input("Name: ").strip()
        if not name:
            return
        
        print("\nType: [S]hortcut or [F]older?")
        key = get_key()
        
        current = self.get_current_items() if self.current_path else self.shortcuts
        
        if key == 'f':
            # Create folder
            current[name] = {
                "type": "folder",
                "items": {}
            }
            print(f"\nFolder '{name}' created")
        else:
            # Create shortcut
            path = input("\nPath/Command: ").strip()
            args = input("Arguments (optional): ").strip()
            
            shortcut = {"type": "shortcut", "path": path}
            if args:
                shortcut["args"] = args
            
            current[name] = shortcut
            print(f"\nShortcut '{name}' created")
        
        self.modified = True
        input("\nPress Enter to continue...")
    
    def edit_shortcut(self):
        """Edit existing shortcut"""
        items = self.get_current_items() if self.current_path else self.shortcuts
        if not items:
            print("No items to edit")
            input("\nPress Enter to continue...")
            return
        
        Colors.clear()
        print("=== Edit Shortcut ===\n")
        
        # List items
        item_list = list(items.items())
        for i, (name, item) in enumerate(item_list):
            type_str = "Folder" if item.get("type") == "folder" else "Shortcut"
            print(f"[{i+1}] {name} ({type_str})")
        
        print("\nSelect item to edit (0 to cancel): ", end='')
        try:
            choice = int(input()) - 1
            if choice < 0 or choice >= len(item_list):
                return
        except:
            return
        
        name, item = item_list[choice]
        
        print(f"\nEditing: {name}")
        print("Leave blank to keep current value\n")
        
        # Edit name
        new_name = input(f"Name [{name}]: ").strip()
        if new_name and new_name != name:
            items[new_name] = items.pop(name)
            name = new_name
        
        # Edit properties if shortcut
        if item.get("type") != "folder":
            current_path = item.get("path", "")
            new_path = input(f"Path [{current_path}]: ").strip()
            if new_path:
                item["path"] = new_path
            
            current_args = item.get("args", "")
            new_args = input(f"Args [{current_args}]: ").strip()
            if new_args:
                item["args"] = new_args
            elif "args" in item and not new_args:
                del item["args"]  # Remove empty args
        
        self.modified = True
        print("\nChanges saved to memory")
        input("Press Enter to continue...")
    
    def delete_shortcut(self):
        """Delete a shortcut"""
        items = self.get_current_items() if self.current_path else self.shortcuts
        if not items:
            print("No items to delete")
            input("\nPress Enter to continue...")
            return
        
        Colors.clear()
        print("=== Delete Shortcut ===\n")
        
        # List items
        item_list = list(items.items())
        for i, (name, item) in enumerate(item_list):
            type_str = "Folder" if item.get("type") == "folder" else "Shortcut"
            print(f"[{i+1}] {name} ({type_str})")
        
        print("\nSelect item to DELETE (0 to cancel): ", end='')
        try:
            choice = int(input()) - 1
            if choice < 0 or choice >= len(item_list):
                return
        except:
            return
        
        name, item = item_list[choice]
        
        print(f"\n{Colors.RED}Delete '{name}'? This cannot be undone!{Colors.RESET}")
        print("Type 'yes' to confirm: ", end='')
        
        if input().strip().lower() == 'yes':
            del items[name]
            self.modified = True
            print(f"\n'{name}' deleted")
        else:
            print("\nCancelled")
        
        input("\nPress Enter to continue...")
    
    def draw_menu(self):
        """Draw the admin menu"""
        Colors.clear()
        
        # Header
        status = f"{Colors.RED}*MODIFIED*{Colors.WHITE}" if self.modified else "saved"
        print(f"{Colors.BLUE}{Colors.WHITE}")
        print("╔══════════════════════════════════════╗")
        print(f"    ML-ADMIN v1.0    [{status:^9}]    ")
        print("╠══════════════════════════════════════╣")
        
        # Current path
        if self.current_path:
            path_str = " > ".join(self.current_path)
            if len(path_str) > 36:
                path_str = "..." + path_str[-33:]
            print(f"║ {path_str:<36} ║")
            print("╠══════════════════════════════════════╣")
        
        # Current items
        items = self.get_current_items() if self.current_path else self.shortcuts
        item_count = len(items)
        
        print(f" Items in current location: {item_count:>9} ")
        
        # Show first few items
        item_list = list(items.items())[:5]
        for name, item in item_list:
            display_name = name[:30]
            if item.get("type") == "folder":
                display_name = f"[{display_name}]"
            print(f"   {display_name:<34} ")
        
        if item_count > 5:
            print(f"   ... and {item_count - 5} more{' '*24} ")
        
        # Menu options
        print("╠═══════════════════════════════════════╣")
        print("║ [A]dd new shortcut/folder             ║")
        print("║ [E]dit existing                       ║")
        print("║ [D]elete                              ║")
        print("║ [N]avigate into folder                ║")
        print("║ [B]ack / [H]ome                       ║")
        print("║ [S]ave changes                        ║")
        print("║ [Q]uit                                ║")
        print(f"╚═══════════════════════════════════════╝{Colors.RESET}")
        print("\nSelect option: ", end='', flush=True)
    
    def navigate(self):
        """Navigate into a folder"""
        items = self.get_current_items() if self.current_path else self.shortcuts
        folders = [(name, item) for name, item in items.items() 
                  if item.get("type") == "folder"]
        
        if not folders:
            print("No folders to navigate into")
            input("\nPress Enter to continue...")
            return
        
        Colors.clear()
        print("=== Navigate ===\n")
        
        for i, (name, _) in enumerate(folders):
            print(f"[{i+1}] {name}")
        
        print("\nSelect folder (0 to cancel): ", end='')
        try:
            choice = int(input()) - 1
            if 0 <= choice < len(folders):
                folder_name = folders[choice][0]
                self.current_path.append(folder_name)
        except:
            pass
    
    def run(self):
        """Main admin loop"""
        while True:
            self.draw_menu()
            key = get_key()
            
            if key == 'q':
                if self.modified:
                    print("\n\nYou have unsaved changes!")
                    print("Really quit? (y/n): ", end='')
                    if get_key() != 'y':
                        continue
                Colors.clear()
                print("ML-Admin closed")
                break
            elif key == 'a':
                self.add_shortcut()
            elif key == 'e':
                self.edit_shortcut()
            elif key == 'd':
                self.delete_shortcut()
            elif key == 'n':
                self.navigate()
            elif key == 'b' and self.current_path:
                self.current_path.pop()
            elif key == 'h':
                self.current_path = []
            elif key == 's':
                if self.save_shortcuts():
                    print("\n\nConfiguration saved!")
                else:
                    print("\n\nFailed to save!")
                input("Press Enter to continue...")

def main():
    try:
        admin = MLAdmin()
        admin.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print(Colors.RESET)

if __name__ == "__main__":
    main()
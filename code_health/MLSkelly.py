#!/usr/bin/env python3
"""
MLSkelly - Magic Launcher Python skeleton builder
Generate consistent ML tool skeletons
"""

import sys
from pathlib import Path

TEMPLATE = '''#!/usr/bin/env python3
"""
{name} - {description}
Part of ML-Extras
"""

import sys
import json
from pathlib import Path
import argparse

class {class_name}:
    def __init__(self):
        """Initialize {name}"""
        self.config_dir = Path.home() / '.config' / '{lower_name}'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def load_config(self):
        """Load configuration if needed"""
        config_file = self.config_dir / 'config.json'
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        return {{}}
    
    def save_config(self, config):
        """Save configuration"""
        config_file = self.config_dir / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def process(self, input_data):
        """Main processing logic"""
        # TODO: Implement core functionality
        return input_data
    
    def run(self):
        """Main interactive loop"""
        print("{name} - {description}")
        print("Commands: process, config, help, quit")
        
        while True:
            try:
                cmd = input("> ").strip().lower()
                
                if cmd == 'quit':
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'config':
                    print(self.load_config())
                else:
                    print(f"Unknown command: {{cmd}}")
                    
            except KeyboardInterrupt:
                print("\\nExiting...")
                break
    
    def show_help(self):
        """Display help information"""
        print("""
{name} Help
============
TODO: Add help text
        """)

def main():
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument('input', nargs='?', help='Input file or data')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Handle piped input
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        # TODO: Process piped data
        print(data)
    elif args.input:
        # TODO: Process file input
        print(f"Processing: {{args.input}}")
    else:
        # Interactive mode
        app = {class_name}()
        app.run()

if __name__ == "__main__":
    main()
'''

def create_template(name, description="TODO: Add description"):
    """Generate ML tool from template"""
    # Create names
    class_name = f"ML{name.title().replace(' ', '')}"
    file_name = f"ML{name.title().replace(' ', '')}.py"
    lower_name = name.lower().replace(' ', '')
    
    # Generate content
    content = TEMPLATE.format(
        name=file_name[:-3],
        description=description,
        class_name=class_name,
        lower_name=lower_name
    )
    
    # Write file
    output_path = Path(file_name)
    if output_path.exists():
        print(f"Error: {file_name} already exists!")
        return
        
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"Created {file_name}")
    print(f"Class: {class_name}")
    print(f"Config: ~/.config/{lower_name}/")
    print("\nNext steps:")
    print("1. Edit the process() method with your logic")
    print("2. Update the help text")
    print("3. Implement any command handlers")

def main():
    if len(sys.argv) < 2:
        print("MLSkelly - Magic Launcher Python Skeleton builder")
        print("Usage: mlskelly <name> [description]")
        print("Example: mlskelly 'converter' 'Convert between formats'")
        sys.exit(1)
    
    name = sys.argv[1]
    description = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "TODO: Add description"
    
    create_template(name, description)

if __name__ == "__main__":
    main()
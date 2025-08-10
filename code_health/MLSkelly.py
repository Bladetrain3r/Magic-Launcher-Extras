#!/usr/bin/env python3
"""
MLSkelly - Magic Launcher Tool Skeleton Generator
Creates ML tools from templates that actually follow ML principles
Under 200 lines of skeleton generation
"""

import sys
import os
from pathlib import Path

# Core CLI template - the default
TEMPLATE_SIMPLE = '''#!/usr/bin/env python3
"""
{name} - {description}
{tagline}
Under {lines} lines of {adjective} {noun}
"""

import sys
import argparse

def {func_name}(text):
    """Core logic - replace this with your tool's purpose"""
    # TODO: Implement actual functionality
    return text.upper()  # Example: uppercase everything

def main():
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument('input', nargs='?', default='-', 
                       help='Input file or - for stdin')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-q', '--quiet', action='store_true', 
                       help='Suppress output')
    
    args = parser.parse_args()
    
    # Input handling
    if args.input == '-':
        data = sys.stdin.read()
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = f.read()
    
    # Process
    result = {func_name}(data)
    
    # Output handling
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
    elif not args.quiet:
        print(result, end='')

if __name__ == "__main__":
    main()
'''

# CLI + GUI template
TEMPLATE_GUI = '''#!/usr/bin/env python3
"""
{name} - {description}
{tagline}
Under {lines} lines of {adjective} {noun}
"""

import sys
import argparse

COLORS = {{'bg':'#3C3C3C','fg':'#00FF00','lite':'#C0C0C0','blk':'#000000'}}

def {func_name}(text):
    """Core logic - replace this with your tool's purpose"""
    # TODO: Implement actual functionality
    return text.upper()  # Example: uppercase everything

def main():
    parser = argparse.ArgumentParser(description="{description}")
    parser.add_argument('input', nargs='?', default='-', 
                       help='Input file or - for stdin')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-q', '--quiet', action='store_true', 
                       help='Suppress output')
    parser.add_argument('--title', default='{name}', 
                       help='GUI window title')
    
    args = parser.parse_args()
    
    # Input handling
    if args.input == '-':
        data = sys.stdin.read()
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = f.read()
    
    # Process
    result = {func_name}(data)
    
    # Output handling
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
    elif not args.quiet:
        print(result, end='')
    
    # Optional GUI
    try:
        import tkinter as tk
        import tkinter.scrolledtext as st
        if '--gui' in sys.argv:
            root = tk.Tk()
            root.title(args.title)
            root.configure(bg=COLORS['bg'])
            
            mainbar = tk.Label(root, text=args.title, 
                             bg=COLORS['lite'], fg=COLORS['blk'])
            mainbar.pack(fill='x')
            
            text_widget = st.ScrolledText(root, bg=COLORS['blk'], 
                                         fg=COLORS['fg'], 
                                         insertbackground=COLORS['fg'])
            text_widget.pack(expand=True, fill='both')
            text_widget.insert('1.0', result)
            
            root.bind('<Escape>', lambda e: root.destroy())
            root.mainloop()
    except Exception as e:
        if '--gui' in sys.argv and not args.quiet:
            print(f"GUI unavailable: {{e}}", file=sys.stderr)

if __name__ == "__main__":
    main()
'''

# Command expansion focused template
TEMPLATE_EXPANSION = '''#!/usr/bin/env python3
"""
{name} - {description}
Designed for command expansion: $(python3 {filename})
Under {lines} lines of {adjective} {noun}
"""

import sys

def {func_name}(args):
    """Generate output for command expansion"""
    # TODO: Implement actual functionality
    # Remember: Output ONLY the result, no decoration
    
    if not args:
        return "default"
    
    command = args[0] if args else 'default'
    
    if command == 'example':
        return "example_output"
    else:
        return command

def main():
    # No argparse needed for expansion tools
    # Just process sys.argv directly
    
    result = {func_name}(sys.argv[1:])
    
    # Just print the result - no formatting
    print(result)

if __name__ == "__main__":
    main()
'''

# Minimal processor template
TEMPLATE_MINIMAL = '''#!/usr/bin/env python3
"""
{name} - {description}
{tagline}
"""

import sys

# Process stdin to stdout
for line in sys.stdin:
    # TODO: Process each line
    print(line.upper(), end='')  # Example: uppercase
'''

def create_skeleton(name, description=None, template_type='simple'):
    """Generate ML tool from template"""
    
    # Generate names
    filename = f"ml{name.lower().replace(' ', '')}.py"
    func_name = f"process_{name.lower().replace(' ', '_')}"
    
    # Generate tagline
    taglines = [
        "Part of the Magic Launcher suite",
        "Because enterprise complexity is a choice",
        "Simple tools for hostile environments",
        "Doing one thing well since right now",
    ]
    tagline = taglines[hash(name) % len(taglines)]
    
    # Generate fun adjectives/nouns
    adjectives = ["procedural", "functional", "practical", "focused", "atomic"]
    nouns = ["simplicity", "clarity", "utility", "revolution", "solutions"]
    adjective = adjectives[hash(name + "adj") % len(adjectives)]
    noun = nouns[hash(name + "noun") % len(nouns)]
    
    # Default description
    if not description:
        description = f"Does {name} things quickly and simply"
    
    # Estimate lines
    lines = "200" if template_type in ['simple', 'minimal'] else "300"
    
    # Select template
    templates = {
        'simple': TEMPLATE_SIMPLE,
        'gui': TEMPLATE_GUI,
        'expansion': TEMPLATE_EXPANSION,
        'minimal': TEMPLATE_MINIMAL
    }
    
    template = templates.get(template_type, TEMPLATE_SIMPLE)
    
    # Generate content
    content = template.format(
        name=f"ML{name.title().replace(' ', '')}",
        filename=filename,
        func_name=func_name,
        description=description,
        tagline=tagline,
        lines=lines,
        adjective=adjective,
        noun=noun
    )
    
    # Check if file exists
    output_path = Path(filename)
    if output_path.exists():
        print(f"Error: {filename} already exists!")
        return False
    
    # Write file
    with open(output_path, 'w') as f:
        f.write(content)
    
    # Make executable
    os.chmod(output_path, 0o755)
    
    print(f"Created: {filename}")
    print(f"Type: {template_type}")
    print(f"Function: {func_name}()")
    print(f"\nNext steps:")
    print(f"1. Edit {func_name}() with your logic")
    print(f"2. Test: echo 'test' | python3 {filename}")
    print(f"3. Ship it!")
    
    return True

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("""MLSkelly - Magic Launcher Skeleton Generator

Usage: 
    mlskelly <name> [type] [description]

Types:
    simple    - Basic CLI tool (default)
    gui       - CLI with optional GUI (--gui flag)
    expansion - Tool designed for command expansion
    minimal   - Bare minimum line processor

Examples:
    mlskelly reverse simple "Reverses text line by line"
    mlskelly config expansion "Configuration value getter"
    mlskelly viewer gui "Text file viewer with GUI option"
    mlskelly filter minimal "Filters lines by pattern"

The skeleton will be created as ml<name>.py""")
        sys.exit(0)
    
    name = sys.argv[1]
    
    # Parse optional type and description
    template_type = 'simple'
    description = None
    
    if len(sys.argv) > 2:
        if sys.argv[2] in ['simple', 'gui', 'expansion', 'minimal']:
            template_type = sys.argv[2]
            if len(sys.argv) > 3:
                description = ' '.join(sys.argv[3:])
        else:
            description = ' '.join(sys.argv[2:])
    
    create_skeleton(name, description, template_type)

if __name__ == "__main__":
    main()
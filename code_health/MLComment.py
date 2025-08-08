#!/usr/bin/env python3
"""
MLComment - Add meaningful comments to code
Start with deterministic patterns, ready for ML later
"""

import json
import re
import sys
from pathlib import Path
import argparse

# mqp#class_definition#
class MLComment:
    """
    Core class for the MLComment tool.
    Manages the knowledge base and performs commenting operations.
    """
    def __init__(self):
        # Config directory, following the XDG Base Directory Specification
        self.config_dir = Path.home() / '.config' / 'mlcomment'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Knowledge base file where patterns are stored
        self.kb_file = self.config_dir / 'patterns.json'
        
        # Load or create knowledge base
        self.kb = self.load_kb()


        
    def load_kb(self):
        """Load knowledge base or create default"""
        if self.kb_file.exists():
            with open(self.kb_file, 'r') as f:
                return json.load(f)
        else:
            # Default patterns for basic Python constructs
            default_kb = {
                "patterns": {
                    r"subprocess\.run": "Execute external command",
                    r"json\.load\s*\(": "Parse JSON from file",
                    r"json\.loads\s*\(": "Parse JSON from string",
                    r"json\.dump\s*\(": "Write JSON to file",
                    r"if\s+.*is\s+None": "Null check",
                    r"if\s+not\s+": "Negative condition check",
                    r"try\s*:": "Error handling block",
                    r"except\s+\w+": "Catch specific exception",
                    r"except\s*:": "Catch all exceptions",
                    r"for\s+\w+\s+in\s+range": "Iterate N times",
                    r"for\s+\w+\s+in\s+": "Iterate over collection",
                    r"while\s+True": "Infinite loop",
                    r"while\s+": "Conditional loop",
                    r"with\s+open": "File operation with auto-close",
                    r"return\s+None": "Explicit null return",
                    r"return\s+": "Return value",
                    r"class\s+\w+": "Class definition",
                    r"def\s+__init__": "Constructor method",
                    r"def\s+\w+": "Function definition",
                    r"@\w+": "Decorator applied",
                    r"import\s+": "Import module",
                    r"from\s+.*\s+import": "Import specific items",
                    r"raise\s+": "Raise exception",
                    r"assert\s+": "Debug assertion",
                    r"print\s*\(": "Debug output",
                    r"\.append\s*\(": "Add to list",
                    r"\.extend\s*\(": "Add multiple items",
                    r"\.split\s*\(": "Split string",
                    r"\.join\s*\(": "Join strings",
                    r"\.strip\s*\(": "Remove whitespace",
                    r"\.replace\s*\(": "Replace substring",
                    r"os\.path\.": "Path operation",
                    r"Path\s*\(": "Path object creation",
                    r"\.exists\s*\(": "Check existence",
                    r"\.mkdir": "Create directory",
                    r"sys\.exit": "Exit program",
                    r"random\.": "Random operation",
                    r"time\.time": "Get current timestamp",
                    r"time\.sleep": "Pause execution",
                    r"datetime\.now": "Get current datetime",
                    r"re\.search": "Regex pattern search",
                    r"re\.match": "Regex pattern match",
                    r"re\.sub": "Regex substitution"
                },
                "context": {
                    "web": {
                        r"request\.GET": "Query parameters",
                        r"request\.POST": "Form data",
                        r"response\.": "HTTP response",
                        r"render\s*\(": "Render template"
                    },
                    "ml": {
                        r"\.fit\s*\(": "Train model",
                        r"\.predict\s*\(": "Make predictions",
                        r"\.transform\s*\(": "Transform data"
                    }
                }
            }
            
            self.save_kb(default_kb)
            return default_kb
    
    def save_kb(self, kb=None):
        """Save knowledge base to the JSON file"""
        if kb is None:
            kb = self.kb
        with open(self.kb_file, 'w') as f:
            json.dump(kb, f, indent=2)
    
    def add_pattern(self, pattern, comment, context=None):
        """Add a new pattern to the knowledge base, optionally in a specific context"""
        if context:
            if context not in self.kb["context"]:
                self.kb["context"][context] = {}
            self.kb["context"][context][pattern] = comment
        else:
            self.kb["patterns"][pattern] = comment
        self.save_kb()
        print(f"Added pattern: {pattern} -> {comment} (context: {context or 'general'})")

    # mqp#find_comment_logic#
    def find_comment(self, line, context=None):
        """Find appropriate comment for a line by matching patterns"""
        line_stripped = line.strip()
        
        # Skip if line is a full-line comment or empty
        if not line_stripped or line_stripped.startswith('#'):
            return None
        
        # Check if line already has a comment. Handles single and double quotes.
        comment_start = line.find('#')
        if comment_start != -1:
            in_string = False
            for i, char in enumerate(line):
                if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                    in_string = not in_string
                elif char == '#' and not in_string:
                    return None
        
        # Check context-specific patterns first for higher priority
        if context and context in self.kb.get("context", {}):
            for pattern, comment in self.kb["context"][context].items():
                if re.search(pattern, line_stripped):
                    return comment[:100]  # Cap comment length
        
        # Check general patterns
        for pattern, comment in self.kb["patterns"].items():
            if re.search(pattern, line_stripped):
                return comment[:100]  # Cap comment length
        
        return None
    
    # mqp#comment_file_logic#
    def comment_file(self, filepath, context=None):
        """Add comments to a file and return the new content as a string"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
        
        output_lines = []
        in_multiline_string = False
        string_delimiter = None
        
        for line in lines:
            # Simple check for multiline strings (e.g., docstrings)
            if '"""' in line or "'''" in line:
                if not in_multiline_string:
                    # Check for an odd number of delimiters to determine entry
                    for delim in ['"""', "'''"]:
                        if delim in line and line.count(delim) % 2 == 1:
                            in_multiline_string = True
                            string_delimiter = delim
                            break
                elif string_delimiter in line and line.count(string_delimiter) % 2 == 1:
                    in_multiline_string = False
            
            if in_multiline_string:
                output_lines.append(line)
                continue
            
            # Find a comment for the current line
            comment = self.find_comment(line, context)
            
            if comment and line.strip():
                # Preserve original indentation and content
                indent = len(line) - len(line.lstrip())
                line_content = line.rstrip()
                
                # Add padding for visual alignment if the line is short
                if len(line_content.strip()) < 50:
                    padding = ' ' * (50 - len(line_content.strip()) + 4)
                else:
                    padding = '  '
                
                commented_line = f"{line_content}{padding}# {comment}\n"
                output_lines.append(commented_line)
            else:
                output_lines.append(line)
        
        return ''.join(output_lines)
    
    # mqp#learn_from_file_logic#
    def learn_from_file(self, filepath):
        """Extract patterns from a well-commented code file to add to the knowledge base"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        learned = 0
        
        for line in lines:
            # Look for lines with end-of-line comments
            if '#' in line and not line.strip().startswith('#'):
                parts = line.split('#', 1)
                code_part = parts[0].strip()
                comment_part = parts[1].strip()
                
                # Skip if the code or comment is too short to be meaningful
                if len(code_part) < 5 or len(comment_part) < 3:
                    continue
                
                # Check if this exact comment already exists as a pattern value
                if comment_part not in self.kb["patterns"].values():
                    # Create a regex-safe pattern from the code part
                    pattern = re.escape(code_part)
                    self.kb["patterns"][pattern] = comment_part[:100]
                    learned += 1
        
        if learned > 0:
            self.save_kb()
            print(f"Learned {learned} new patterns from {filepath}")
        else:
            print(f"No new patterns found in {filepath}")

    def save_to_file(self, filepath, content):
        """Writes the generated content to a specified file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully saved commented file to {filepath}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def comment_file_external(self, filepath, context=None):
        """Generate external comment documentation"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
        
        comments = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip empty lines
            if not line.strip():
                continue
                
            comment = self.find_comment(line, context)
            if comment:
                # Get the actual code (stripped)
                code_snippet = line.strip()
                if len(code_snippet) > 50:
                    code_snippet = code_snippet[:47] + "..."
                
                comments.append({
                    'line': line_num,
                    'code': code_snippet,
                    'comment': comment
                })
        
        return comments
    
# mqp#main#
def main():
    """Main function to parse arguments and run MLComment"""
    parser = argparse.ArgumentParser(description="Add meaningful comments to code")
    parser.add_argument("file", nargs="?", help="File to comment")
    parser.add_argument("--add", nargs=3, metavar=("PATTERN", "COMMENT", "CONTEXT"),
                        help="Add pattern to knowledge base with optional context")
    parser.add_argument("--learn", metavar="FILE",
                        help="Learn patterns from commented file")
    parser.add_argument("--context", help="Use a specific context (e.g., 'web', 'ml') for commenting")
    parser.add_argument("--show-kb", action="store_true",
                        help="Show current knowledge base")
    parser.add_argument("--save", metavar="OUTPUT_FILE",
                        help="Save output to a specified file instead of stdout")
    parser.add_argument("--external", action="store_true",
                        help="Generate external comment documentation")
    parser.add_argument("--format", choices=['text', 'json', 'markdown'], default='text',
                        help="Output format for external comments (default: text)")
    
    args = parser.parse_args()
    
    commenter = MLComment()
    
    if args.add:
        pattern, comment, context = args.add
        commenter.add_pattern(pattern, comment, context)
    elif args.learn:
        commenter.learn_from_file(args.learn)
    elif args.show_kb:
        print(json.dumps(commenter.kb, indent=2))
    elif args.file:
        if args.external:
            # External comment mode
            comments = commenter.comment_file_external(args.file, args.context)
            if comments:
                # Output format options
                if args.format == 'json':
                    print(json.dumps(comments, indent=2))
                elif args.format == 'markdown':
                    print(f"# Code Comments for {args.file}\n")
                    for c in comments:
                        print(f"**Line {c['line']}**: `{c['code']}`")
                        print(f"- {c['comment']}\n")
                else:  # Default text format
                    print(f"Comments for {args.file}:")
                    print("-" * 50)
                    for c in comments:
                        print(f"L{c['line']:4d}: {c['comment']}")
                        print(f"       {c['code']}\n")
        else:
            # Normal inline comment mode
            result = commenter.comment_file(args.file, args.context)
            if result:
                if args.save:
                    commenter.save_to_file(args.save, result)
                else:
                    print(result)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
MLComment - Add meaningful comments to code
Multi-language support with pattern learning
"""

import json                                           # Import module
import re                                             # Import module
import sys                                            # Import module
from pathlib import Path                              # Import module
import argparse                                       # Import module

class MLComment:                                      # Class definition
    """
    Core class for the MLComment tool.                    # Class definition
    Manages the knowledge base and performs commenting operations.
    """
    def __init__(self):                                   # Constructor method
        # Config directory, following the XDG Base Directory Specification
        self.config_dir = Path.home() / '.config' / 'mlcomment'
        self.config_dir.mkdir(parents=True, exist_ok=True)  # Create directory
        
        # Knowledge base file where patterns are stored
        self.kb_file = self.config_dir / 'patterns.json'
        
        # Language-specific comment styles
        self.comment_styles = {
            '.py': '#',
            '.js': '//',
            '.jsx': '//',
            '.ts': '//',
            '.tsx': '//',
            '.c': '//',
            '.cpp': '//',
            '.cc': '//',
            '.h': '//',
            '.hpp': '//',
            '.java': '//',
            '.php': '//',
            '.rb': '#',
            '.sh': '#',
            '.bash': '#',
            '.yml': '#',
            '.yaml': '#',
            '.sql': '--',
            '.go': '//',
            '.rs': '//',
        }
        
        # Load or create knowledge base
        self.kb = self.load_kb()
    
    def get_comment_style(self, filepath):                # Function definition
        """Get the appropriate comment style for a file"""
        file_ext = Path(filepath).suffix.lower()              # Path object creation
        return self.comment_styles.get(file_ext, '#')
    
    def load_kb(self):                                    # Function definition
        """Load knowledge base or create default"""
        if self.kb_file.exists():                             # Check existence
            with open(self.kb_file, 'r') as f:                    # File operation with auto-close
                return json.load(f)                                   # Parse JSON from file
        else:
            # Default patterns for basic Python constructs only
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
                    r"import\s+": "Import module",
                    r"from\s+.*\s+import": "Import specific items",
                },
                "context": {}
            }
            
            self.save_kb(default_kb)
            return default_kb                                     # Return value
    
    def save_kb(self, kb=None):                           # Function definition
        """Save knowledge base to the JSON file"""
        if kb is None:                                        # Null check
            kb = self.kb
        with open(self.kb_file, 'w') as f:                    # File operation with auto-close
            json.dump(kb, f, indent=2)                            # Write JSON to file
    
    def add_pattern(self, pattern, comment, context=None):  # Function definition
        """Add a new pattern to the knowledge base, optionally in a specific context"""
        if context:
            if context not in self.kb["context"]:
                self.kb["context"][context] = {}
            self.kb["context"][context][pattern] = comment
        else:
            self.kb["patterns"][pattern] = comment
        self.save_kb()
        print(f"Added pattern: {pattern} -> {comment} (context: {context or 'general'})")  # Debug output
    
    def find_comment(self, line, context=None):           # Function definition
        """Find appropriate comment for a line by matching patterns"""
        line_stripped = line.strip()                          # Remove whitespace
        
        # Skip if line is empty
        if not line_stripped:                                 # Negative condition check
            return None                                           # Explicit null return
        
        # Check context-specific patterns first for higher priority
        if context and context in self.kb.get("context", {}):  # Get user by ID
            for pattern, comment in self.kb["context"][context].items():
                if re.search(pattern, line_stripped):                 # Regex pattern search
                    return comment[:100]  # Cap comment length
        
        # Check general patterns
        for pattern, comment in self.kb["patterns"].items():
            if re.search(pattern, line_stripped):                 # Regex pattern search
                return comment[:100]  # Cap comment length
        
        return None                                           # Explicit null return
    
    def learn_from_file(self, filepath):                  # Function definition
        """Extract patterns from a well-commented code file to add to the knowledge base"""
        try:                                                  # Error handling block
            with open(filepath, 'r', encoding='utf-8') as f:      # File operation with auto-close
                lines = f.readlines()
        except Exception as e:                                # Catch specific exception
            print(f"Error reading file: {e}")                     # Debug output
            return
        
        # Get the comment style for this file type
        comment_char = self.get_comment_style(filepath)
        
        # Build regex to find lines with comments
        # Escape special regex characters in comment char
        escaped_comment = re.escape(comment_char)
        comment_regex = f'(.+?)\\s*{escaped_comment}\\s*(.+)'
        
        learned = 0
        
        for line in lines:                                    # Iterate over collection
            # Skip lines that start with comments (full-line comments)
            if line.strip().startswith(comment_char):             # Remove whitespace
                continue
            
            # Look for lines with end-of-line comments
            match = re.search(comment_regex, line)                # Regex pattern search
            
            if match:
                code_part = match.group(1).strip()                    # Remove whitespace
                comment_part = match.group(2).strip()                 # Remove whitespace
                
                # Skip if the code or comment is too short to be meaningful
                if len(code_part) < 5 or len(comment_part) < 3:
                    continue
                
                # Check if this exact comment already exists as a pattern value
                if comment_part not in self.kb["patterns"].values():
                    # Create a pattern from the code part
                    # Try to make it somewhat generic
                    if '(' in code_part:
                        # For function calls, try to capture just the function name
                        func_match = re.search(r'(\w+)\s*\(', code_part)      # Regex pattern search
                        if func_match:
                            pattern = re.escape(func_match.group(1)) + r'\s*\('
                        else:
                            pattern = re.escape(code_part)
                    else:
                        pattern = re.escape(code_part)
                    
                    self.kb["patterns"][pattern] = comment_part[:100]
                    learned += 1
        
        if learned > 0:
            self.save_kb()
            print(f"Learned {learned} new patterns from {filepath}")  # Debug output
        else:
            print(f"No new patterns found in {filepath}")         # Debug output
    
    def comment_file(self, filepath, context=None):       # Function definition
        """Add comments to a file and return the new content as a string"""  # Return value
        try:                                                  # Error handling block
            with open(filepath, 'r', encoding='utf-8') as f:      # File operation with auto-close
                lines = f.readlines()
        except Exception as e:                                # Catch specific exception
            print(f"Error reading file: {e}")                     # Debug output
            return None                                           # Explicit null return
        
        # Get the right comment style
        comment_char = self.get_comment_style(filepath)
        
        output_lines = []
        
        for line in lines:                                    # Iterate over collection
            # Skip if line already has a comment
            if comment_char in line:
                # Simple check - if comment char appears outside of strings
                # This is simplified but works for most cases
                parts = line.split(comment_char)                      # Split string
                if len(parts) > 1:
                    # Already has a comment
                    output_lines.append(line)                             # Add to list
                    continue
            
            # Find a comment for the current line
            comment = self.find_comment(line, context)
            
            if comment and line.strip():                          # Remove whitespace
                # Preserve original indentation and content
                line_content = line.rstrip()
                
                # Add padding for visual alignment if the line is short
                if len(line_content.strip()) < 50:                    # Remove whitespace
                    padding = ' ' * (50 - len(line_content.strip()) + 4)  # Remove whitespace
                else:
                    padding = '  '
                
                commented_line = f"{line_content}{padding}{comment_char} {comment}\n"
                output_lines.append(commented_line)                   # Add to list
            else:
                output_lines.append(line)                             # Add to list
        
        return ''.join(output_lines)                          # Return value
    
    def save_to_file(self, filepath, content):            # Function definition
        """Writes the generated content to a specified file"""
        try:                                                  # Error handling block
            with open(filepath, 'w', encoding='utf-8') as f:      # File operation with auto-close
                f.write(content)
            print(f"Successfully saved commented file to {filepath}")  # Debug output
        except Exception as e:                                # Catch specific exception
            print(f"Error saving file: {e}")                      # Debug output
    
    def comment_file_external(self, filepath, context=None):  # Function definition
        """Generate external comment documentation"""
        try:                                                  # Error handling block
            with open(filepath, 'r', encoding='utf-8') as f:      # File operation with auto-close
                lines = f.readlines()
        except Exception as e:                                # Catch specific exception
            print(f"Error reading file: {e}")                     # Debug output
            return None                                           # Explicit null return
        
        comments = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip empty lines
            if not line.strip():                                  # Negative condition check
                continue
                
            comment = self.find_comment(line, context)
            if comment:
                # Get the actual code (stripped)
                code_snippet = line.strip()                           # Remove whitespace
                if len(code_snippet) > 50:
                    code_snippet = code_snippet[:47] + "..."
                
                comments.append({                                     # Add to list
                    'line': line_num,
                    'code': code_snippet,
                    'comment': comment
                })
        
        return comments                                       # Return value

def main():                                           # Function definition
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
        print(json.dumps(commenter.kb, indent=2))             # Debug output
    elif args.file:
        if args.external:
            # External comment mode
            comments = commenter.comment_file_external(args.file, args.context)
            if comments:
                # Output format options
                if args.format == 'json':
                    print(json.dumps(comments, indent=2))                 # Debug output
                elif args.format == 'markdown':
                    print(f"# Code Comments for {args.file}\n")
                    for c in comments:                                    # Iterate over collection
                        print(f"**Line {c['line']}**: `{c['code']}`")         # Debug output
                        print(f"- {c['comment']}\n")                          # Debug output
                else:  # Default text format
                    print(f"Comments for {args.file}:")                   # Debug output
                    print("-" * 50)                                       # Debug output
                    for c in comments:                                    # Iterate over collection
                        print(f"L{c['line']:4d}: {c['comment']}")             # Debug output
                        print(f"       {c['code']}\n")                        # Debug output
        else:
            # Normal inline comment mode
            result = commenter.comment_file(args.file, args.context)
            if result:
                if args.save:
                    commenter.save_to_file(args.save, result)
                else:
                    print(result)                                         # Debug output
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
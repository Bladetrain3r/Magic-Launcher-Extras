#!/usr/bin/env python3
"""
MLNeotext - Convert between Markdown and HTML.
Now with Silicon Spring manifesto styling!

This script can convert Markdown to HTML with different styles, or strip
either format to plain text. It can also now open the generated HTML
directly in a web browser for a quick preview, or print the output
to stdout for piping to other tools.
"""

import sys
import re
from pathlib import Path
import argparse
import webbrowser
import os
import tempfile
import html

class MLHTMD:
    """A class to handle Markdown/HTML conversions with simple styling."""
    def __init__(self, style='basic'):
        self.style = style  # 'basic', 'magic', or 'strip'

    def md_to_html(self, text, title="Document"):
        """Convert Markdown to HTML with a chosen style."""
        if self.style == 'strip':
            # Just return the text content
            return self._strip_to_text(text)

        lines = []

        # HTML header
        lines.append('<!DOCTYPE html>')
        lines.append('<html lang="en">')
        lines.append('<head>')
        lines.append('    <meta charset="UTF-8">')
        lines.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        lines.append(f'    <title>{title}</title>')
        
        if self.style == 'magic':
            # Full Magic Launcher manifesto style
            lines.extend(self._get_magic_style())
        else:
            # Basic terminal style
            lines.extend(self._get_basic_style())

        lines.append('</head>')
        lines.append('<body>')
        
        if self.style == 'magic':
            # Add Unitext-style header (from the PUNK.html example)
            lines.append('    <div class="header">')
            lines.append(f'        <span class="header-title">{html.escape(title)}</span>')
            lines.append('        <div class="header-buttons">')
            lines.append('            <button class="header-button">_</button>')
            lines.append('            <button class="header-button">□</button>')
            lines.append('            <button class="header-button">X</button>')
            lines.append('        </div>')
            lines.append('    </div>')
            lines.append('    <div class="content manifesto-container">')
        else:
            lines.append('    <div class="content">')

        # Process markdown content
        lines.extend(self._process_markdown(text))
        
        lines.append('    </div>') # Close content div
        lines.append('</body>')
        lines.append('</html>')
        
        return '\n'.join(lines)
    
    def _get_basic_style(self):
        """Basic terminal style CSS with a new theme."""
        return [
            '    <style>',
            '        body { background-color: #2b2b2b; color: #a9b7c6; font-family: "Fira Code", monospace; line-height: 1.6; max-width: 80ch; margin: 0 auto; padding: 20px; }',
            '        h1, h2, h3 { color: #cc7832; }',
            '        h2 { color: #6a8759; }',
            '        h3 { color: #9876aa; }',
            '        p { margin: 1em 0; }',
            '        pre { background: #3c3f41; border: 1px solid #4a4a4a; padding: 15px; border-radius: 5px; overflow-x: auto; color: #a9b7c6; }',
            '        code { color: #ffc66d; background: #3c3f41; padding: 2px 4px; border-radius: 3px; }',
            '        a { color: #6897bb; text-decoration: none; }',
            '        a:hover { text-decoration: underline; }',
            '        ul, ol { margin: 1em 0; padding-left: 20px; }',
            '        li { margin-bottom: 0.5em; }',
            '    </style>'
        ]
    
    def _get_magic_style(self):
        """Full Magic Launcher manifesto style CSS, updated to match the new aesthetic."""
        return [
            '    <style>',
            '        body { margin: 0; padding: 0; background: #000; color: #0F0; font-family: "Courier New", monospace; font-size: 14px; line-height: 1.4; }',
            '        .header { background: #0F0; color: #000; padding: 2px 5px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0F0; }',
            '        .header-title { font-weight: bold; }',
            '        .header-buttons { display: flex; gap: 10px; }',
            '        .header-button { background: #C0C0C0; color: #000; border: 2px outset #FFF; padding: 1px 6px; cursor: pointer; font-family: inherit; font-size: inherit; }',
            '        .content { padding: 10px; max-width: 80ch; margin: 0 auto; }',
            '        .manifesto-container { max-width: 80ch; margin: 20px auto; padding: 20px; border: 2px solid #0F0; box-shadow: 0 0 10px #0F0, inset 0 0 10px #0F0; animation: flicker 1s infinite alternate; background: rgba(0, 50, 0, 0.2); overflow-x: auto; }',
            '        @keyframes flicker { 0% { opacity: 1; } 100% { opacity: 0.98; } }',
            '        h1, h2, h3 { color: #0FF; text-shadow: 0 0 5px #0FF; text-align: center; }',
            '        h1 { font-size: 2em; margin-bottom: 0.5em; }',
            '        h2 { font-size: 1.5em; margin-top: 1.5em; }',
            '        h3 { font-size: 1.2em; text-decoration: underline; color: #FF0; }',
            '        p { margin: 1em 0; text-align: justify; }',
            '        pre { background: rgba(0, 0, 0, 0.5); border: 1px solid #0F0; padding: 10px; overflow-x: auto; color: #FFF; white-space: pre-wrap; word-wrap: break-word; }',
            '        code { color: #0FF; background: #111; padding: 2px 4px; }',
            '        ul { list-style-type: "⚡ "; margin: 1em 0; padding-left: 20px; }',
            '        ol { margin: 1em 0; padding-left: 20px; }',
            '        li { margin: 5px 0; }',
            '        a { color: #00F; text-decoration: underline; }',
            '        a:hover { background: #00F; color: #FFF; }',
            '        hr { border: 1px dashed #0F0; margin: 2em 0; }',
            '    </style>'
        ]
    
    def _process_markdown(self, text):
        """Process markdown content, converting it to HTML tags."""
        lines = []
        in_code = False
        in_list = False
        
        for line in text.split('\n'):
            line = line.strip()

            # Handle list state transitions
            is_list_item = line.startswith(('- ', '* '))
            if not in_list and is_list_item:
                lines.append('<ul>')
                in_list = True
            elif in_list and not is_list_item and line:
                lines.append('</ul>')
                in_list = False

            # Code blocks
            if line.startswith('```'):
                if in_code:
                    lines.append('</pre>')
                    in_code = False
                else:
                    lines.append('<pre><code>')
                    in_code = True
                continue
            
            if in_code:
                lines.append(html.escape(line))
                continue
            
            # Headers
            if line.startswith('### '):
                lines.append(f'<h3>{self._process_inline(line[4:])}</h3>')
            elif line.startswith('## '):
                lines.append(f'<h2>{self._process_inline(line[3:])}</h2>')
            elif line.startswith('# '):
                lines.append(f'<h1>{self._process_inline(line[2:])}</h1>')
            # Lists
            elif is_list_item:
                item = self._process_inline(line[2:])
                lines.append(f'    <li>{item}</li>')
            # Horizontal rule
            elif line == '---' or line == '***' or line == '___':
                lines.append('<hr>')
            # Regular text (if not empty)
            elif line:
                processed = self._process_inline(line)
                lines.append(f'<p>{processed}</p>')
        
        # Close any open tags at the end of the file
        if in_list:
            lines.append('</ul>')
        if in_code:
            lines.append('</code></pre>')
        
        return lines
    
    def _process_inline(self, text):
        """Process inline markdown."""
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic 
        text = re.sub(r'\_(.+?)\_', r'<em>\1</em>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text
    
    def _strip_to_text(self, text):
        """Strip markdown to plain text."""
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove headers
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Remove bold/italic
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        # Remove links
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Remove code
        text = re.sub(r'`(.+?)`', r'\1', text)
        # Clean up
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def html_to_text(self, html_content):
        """Strip HTML to plain text."""
        # Remove script and style
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        # Convert tags to breaks
        html_content = re.sub(r'<br\s*/?>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<p[^>]*>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'</p>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'</?h[1-6]>', '\n', html_content, flags=re.IGNORECASE)
        # Strip all other tags
        html_content = re.sub(r'<[^>]+>', '', html_content)
        # Decode entities
        html_content = html_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        # Clean up whitespace
        html_content = re.sub(r'\n{3,}', '\n\n', html_content)
        return html_content.strip()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MLHTMD - Markdown/HTML converter with Magic Launcher styling.",
        epilog="""
Styles:
  --basic   Simple terminal style (default)
  --magic   Full Magic Launcher manifesto style
  --strip   Convert to plain text only
  
Output:
  --stdout  Print output to standard out instead of a file
  --preview Open the output in the default web browser (implies --html)

Examples:
  mlhtmd README.md                           # Basic terminal HTML to README.html
  mlhtmd README.md --magic --preview         # Magic Launcher style, open in browser
  mlhtmd page.html --strip --stdout          # Strip to text and print to console
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input_file', help='Path to the input file.')
    parser.add_argument('--basic', action='store_const', const='basic', dest='style', default='basic',
                        help='Use simple terminal style CSS.')
    parser.add_argument('--magic', action='store_const', const='magic', dest='style',
                        help='Use full Magic Launcher manifesto style CSS.')
    parser.add_argument('--strip', action='store_const', const='strip', dest='style',
                        help='Convert to plain text only.')
    parser.add_argument('--stdout', action='store_true',
                        help='Print the output to standard output instead of a file.')
    parser.add_argument('--preview', action='store_true',
                        help='Open the generated HTML in the default web browser.')

    args = parser.parse_args()
    
    input_file = Path(args.input_file)
    
    if not input_file.exists():
        print(f"Error: {input_file} not found", file=sys.stderr)
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    converter = MLHTMD(args.style)
    
    # Handle the conversion
    if input_file.suffix.lower() in ['.md', '.markdown']:
        title = input_file.stem.replace('_', ' ').title()
        output = converter.md_to_html(content, title)
        is_html = (args.style != 'strip')
    else:
        output = converter.html_to_text(content)
        is_html = False

    # Handle output based on flags
    if args.stdout:
        print(output)
    elif args.preview:
        if is_html:
            # Create a temporary file, write the HTML, and open it
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as temp_file:
                temp_file.write(output)
                temp_file_path = temp_file.name
            webbrowser.open_new_tab(f'file://{os.path.realpath(temp_file_path)}')
            print(f"Opened preview in browser from temporary file: {temp_file_path}")
            # The temp file will be deleted when the program exits
        else:
            print("Error: --preview is only valid for HTML output.", file=sys.stderr)
            sys.exit(1)
    else:
        # Default behavior: write to a new file
        output_ext = '.html' if is_html else '.txt'
        output_file = input_file.with_suffix(output_ext)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Created: {output_file}")

if __name__ == "__main__":
    main()

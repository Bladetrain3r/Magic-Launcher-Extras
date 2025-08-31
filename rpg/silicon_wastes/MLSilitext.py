#!/usr/bin/env python3
"""
MLNeotext - Convert between Markdown and HTML.
Silicon Wastes edition with EGA-inspired theming!

This script can convert Markdown to HTML with different styles, or strip
either format to plain text. It can also open the generated HTML
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
        self.style = style  # 'basic', 'silicon', or 'strip'

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
        
        if self.style == 'silicon':
            # Silicon Wastes EGA-inspired style
            lines.extend(self._get_silicon_style())
        else:
            # Basic terminal style
            lines.extend(self._get_basic_style())

        lines.append('</head>')
        lines.append('<body>')
        
        if self.style == 'silicon':
            # Add Silicon Wastes header
            lines.append('    <div class="header">')
            lines.append(f'        <span class="header-title">// {html.escape(title)}</span>')
            lines.append('        <div class="header-buttons">')
            lines.append('            <span class="header-button">[_]</span>')
            lines.append('            <span class="header-button">[□]</span>')
            lines.append('            <span class="header-button">[X]</span>')
            lines.append('        </div>')
            lines.append('    </div>')
            lines.append('    <div class="content wastes-container">')
        else:
            lines.append('    <div class="content">')

        # Process markdown content
        lines.extend(self._process_markdown(text))
        
        lines.append('    </div>') # Close content div
        
        # Add ASCII decoration for silicon style
        if self.style == 'silicon':
            lines.append('    <div class="footer">')
            lines.append('        <pre class="ascii-decoration">')
            lines.append('~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~')
            lines.append('        </pre>')
            lines.append('    </div>')
        
        lines.append('</body>')
        lines.append('</html>')
        
        return '\n'.join(lines)
    
    def _get_basic_style(self):
        """Basic terminal style CSS."""
        return [
            '    <style>',
            '        body { background-color: #1a1a1a; color: #b8b8b8; font-family: "Fira Code", "Courier New", monospace; line-height: 1.6; max-width: 80ch; margin: 0 auto; padding: 20px; }',
            '        h1, h2, h3 { color: #55ff55; }',
            '        h2 { color: #55ffff; }',
            '        h3 { color: #ffff55; }',
            '        p { margin: 1em 0; }',
            '        pre { background: #0a0a0a; border: 1px solid #333; padding: 15px; overflow-x: auto; color: #aaaaaa; }',
            '        code { color: #ff55ff; background: #222; padding: 2px 4px; }',
            '        a { color: #5555ff; text-decoration: none; }',
            '        a:hover { text-decoration: underline; }',
            '        ul, ol { margin: 1em 0; padding-left: 20px; }',
            '        li { margin-bottom: 0.5em; }',
            '    </style>'
        ]
    
    def _get_silicon_style(self):
        """Silicon Wastes EGA-inspired style CSS."""
        return [
            '    <style>',
            '        :root {',
            '            /* EGA Palette */',
            '            --ega-black: #000000;',
            '            --ega-blue: #0000AA;',
            '            --ega-green: #00AA00;',
            '            --ega-cyan: #00AAAA;',
            '            --ega-red: #AA0000;',
            '            --ega-magenta: #AA00AA;',
            '            --ega-brown: #AA5500;',
            '            --ega-light-gray: #AAAAAA;',
            '            --ega-dark-gray: #555555;',
            '            --ega-light-blue: #5555FF;',
            '            --ega-light-green: #55FF55;',
            '            --ega-light-cyan: #55FFFF;',
            '            --ega-light-red: #FF5555;',
            '            --ega-light-magenta: #FF55FF;',
            '            --ega-yellow: #FFFF55;',
            '            --ega-white: #FFFFFF;',
            '        }',
            '        body { ',
            '            margin: 0; padding: 0; ',
            '            background: var(--ega-black); ',
            '            color: var(--ega-light-gray); ',
            '            font-family: "Fira Code", "Courier New", monospace; ',
            '            font-size: 14px; ',
            '            line-height: 1.6;',
            '            background-image: ',
            '                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 170, 170, 0.03) 2px, rgba(0, 170, 170, 0.03) 4px),',
            '                repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0, 170, 170, 0.03) 2px, rgba(0, 170, 170, 0.03) 4px);',
            '            background-size: 100px 100px;',
            '        }',
            '        .header { ',
            '            background: var(--ega-dark-gray); ',
            '            color: var(--ega-light-cyan); ',
            '            padding: 8px 15px; ',
            '            display: flex; ',
            '            justify-content: space-between; ',
            '            align-items: center; ',
            '            border-bottom: 2px solid var(--ega-cyan);',
            '            font-family: "Fira Code", "Courier New", monospace;',
            '        }',
            '        .header-title { font-weight: bold; text-shadow: 0 0 5px var(--ega-cyan); }',
            '        .header-buttons { display: flex; gap: 8px; }',
            '        .header-button { ',
            '            color: var(--ega-light-gray); ',
            '            cursor: pointer; ',
            '            font-family: inherit; ',
            '            font-size: inherit;',
            '        }',
            '        .content { padding: 20px; max-width: 80ch; margin: 0 auto; }',
            '        .wastes-container { ',
            '            max-width: 80ch; ',
            '            margin: 20px auto; ',
            '            padding: 30px; ',
            '            border: 2px solid var(--ega-light-green); ',
            '            box-shadow: 0 0 15px var(--ega-light-green), inset 0 0 10px var(--ega-green);',
            '            background: rgba(0, 42, 0, 0.3);',
            '            position: relative;',
            '        }',
            '        .wastes-container::before {',
            '            content: "";',
            '            position: absolute;',
            '            top: -2px; left: -2px; right: -2px; bottom: -2px;',
            '            background: linear-gradient(45deg, var(--ega-light-green), var(--ega-cyan), var(--ega-light-green));',
            '            opacity: 0.1;',
            '            animation: pulse 4s ease-in-out infinite;',
            '            z-index: -1;',
            '        }',
            '        @keyframes pulse { 0%, 100% { opacity: 0.1; } 50% { opacity: 0.2; } }',
            '        h1, h2, h3 { text-shadow: 0 0 8px currentColor; }',
            '        h1 { ',
            '            color: var(--ega-yellow); ',
            '            font-size: 2em; ',
            '            margin: 1em 0 0.5em 0;',
            '            text-align: center;',
            '            border-bottom: 2px solid var(--ega-yellow);',
            '            padding-bottom: 0.3em;',
            '        }',
            '        h2 { ',
            '            color: var(--ega-light-cyan); ',
            '            font-size: 1.5em; ',
            '            margin-top: 1.5em;',
            '            border-left: 4px solid var(--ega-cyan);',
            '            padding-left: 10px;',
            '        }',
            '        h3 { ',
            '            color: var(--ega-light-magenta); ',
            '            font-size: 1.2em;',
            '            margin-top: 1.2em;',
            '        }',
            '        p { margin: 1em 0; text-align: justify; }',
            '        pre { ',
            '            background: rgba(0, 0, 0, 0.8); ',
            '            border: 1px solid var(--ega-green); ',
            '            padding: 15px; ',
            '            overflow-x: auto; ',
            '            color: var(--ega-light-green);',
            '            box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.1);',
            '            white-space: pre-wrap;',
            '            word-wrap: break-word;',
            '        }',
            '        code { ',
            '            color: var(--ega-light-magenta); ',
            '            background: var(--ega-dark-gray); ',
            '            padding: 2px 6px;',
            '            border: 1px solid var(--ega-magenta);',
            '        }',
            '        ul { list-style-type: "▸ "; margin: 1em 0; padding-left: 25px; }',
            '        ol { margin: 1em 0; padding-left: 25px; }',
            '        li { margin: 8px 0; }',
            '        a { ',
            '            color: var(--ega-light-blue); ',
            '            text-decoration: none;',
            '            border-bottom: 1px dotted var(--ega-light-blue);',
            '        }',
            '        a:hover { ',
            '            color: var(--ega-yellow); ',
            '            text-shadow: 0 0 5px var(--ega-yellow);',
            '            border-bottom-color: var(--ega-yellow);',
            '        }',
            '        strong { color: var(--ega-yellow); }',
            '        em { color: var(--ega-light-cyan); font-style: italic; }',
            '        hr { ',
            '            border: none;',
            '            height: 2px;',
            '            background: linear-gradient(90deg, transparent, var(--ega-green), transparent);',
            '            margin: 2em 0;',
            '        }',
            '        blockquote {',
            '            border-left: 4px solid var(--ega-light-green);',
            '            padding-left: 20px;',
            '            margin: 1.5em 0;',
            '            color: var(--ega-light-cyan);',
            '            font-style: italic;',
            '        }',
            '        .footer {',
            '            margin-top: 40px;',
            '            text-align: center;',
            '            color: var(--ega-dark-gray);',
            '        }',
            '        .ascii-decoration {',
            '            color: var(--ega-green);',
            '            font-size: 12px;',
            '            animation: flicker 10s infinite;',
            '        }',
            '        @keyframes flicker { ',
            '            0%, 100% { opacity: 0.5; } ',
            '            50% { opacity: 0.8; }',
            '        }',
            '    </style>'
        ]
    
    def _process_markdown(self, text):
        """Process markdown content, converting it to HTML tags."""
        lines = []
        in_code = False
        in_list = False
        
        for line in text.split('\n'):
            original_line = line
            line = line.strip()

            # Handle list state transitions
            is_list_item = line.startswith(('- ', '* ', '+ '))
            if not in_list and is_list_item:
                lines.append('<ul>')
                in_list = True
            elif in_list and not is_list_item and line:
                lines.append('</ul>')
                in_list = False

            # Code blocks
            if line.startswith('```'):
                if in_code:
                    lines.append('</code></pre>')
                    in_code = False
                else:
                    lines.append('<pre><code>')
                    in_code = True
                continue
            
            if in_code:
                lines.append(html.escape(original_line))
                continue
            
            # Blockquotes
            if line.startswith('> '):
                quote_text = self._process_inline(line[2:])
                lines.append(f'<blockquote>{quote_text}</blockquote>')
            # Headers
            elif line.startswith('### '):
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
            elif line in ['---', '***', '___', '- - -', '* * *']:
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
        # Escape HTML first
        text = html.escape(text)
        # Bold (must come before single asterisk italic)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        # Italic 
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
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
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
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
        html_content = html.unescape(html_content)
        # Clean up whitespace
        html_content = re.sub(r'\n{3,}', '\n\n', html_content)
        return html_content.strip()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MLNeotext - Markdown/HTML converter with Silicon Wastes styling.",
        epilog="""
Styles:
  --basic   Simple terminal style (default)
  --silicon Silicon Wastes EGA-inspired style
  --strip   Convert to plain text only
  
Output:
  --stdout  Print output to standard out instead of a file
  --preview Open the output in the default web browser (implies --html)

Examples:
  mlneotext README.md                           # Basic terminal HTML to README.html
  mlneotext README.md --silicon --preview       # Silicon Wastes style, open in browser
  mlneotext bestiary.md --silicon               # Convert bestiary to themed HTML
  mlneotext page.html --strip --stdout          # Strip to text and print to console
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input_file', help='Path to the input file.')
    parser.add_argument('--basic', action='store_const', const='basic', dest='style', default='basic',
                        help='Use simple terminal style CSS.')
    parser.add_argument('--silicon', action='store_const', const='silicon', dest='style',
                        help='Use Silicon Wastes EGA-inspired style.')
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
        title = input_file.stem.replace('_', ' ').replace('-', ' ').title()
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
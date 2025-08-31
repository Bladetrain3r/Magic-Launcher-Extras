#!/usr/bin/env python3
"""
MLNeotext - Markdown to HTML converter, Silicon Wastes edition.
Simplified: Just does one thing well - converts MD to themed HTML with collapsible H2 sections.
"""

import sys
import re
import html
import argparse
import webbrowser
import tempfile
from pathlib import Path

def md_to_html(text, title="Document"):
    """Convert Markdown to Silicon Wastes HTML with collapsible H2 sections."""
    
    # Process markdown line by line
    html_lines = []
    in_code = False
    in_list = False
    
    for line in text.split('\n'):
        original = line
        line = line.strip()
        
        # Code blocks
        if line.startswith('```'):
            if in_code:
                html_lines.append('</code></pre>')
                in_code = False
            else:
                html_lines.append('<pre><code>')
                in_code = True
            continue
        
        if in_code:
            html_lines.append(html.escape(original))
            continue
        
        # Lists
        is_list = line.startswith(('- ', '* ', '+ '))
        if not in_list and is_list:
            html_lines.append('<ul>')
            in_list = True
        elif in_list and not is_list and line:
            html_lines.append('</ul>')
            in_list = False
        
        # Process line
        if line.startswith('# '):
            html_lines.append(f'<h1>{process_inline(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{process_inline(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{process_inline(line[4:])}</h3>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote>{process_inline(line[2:])}</blockquote>')
        elif is_list:
            html_lines.append(f'    <li>{process_inline(line[2:])}</li>')
        elif line in ['---', '***', '___']:
            html_lines.append('<hr>')
        elif line:
            html_lines.append(f'<p>{process_inline(line)}</p>')
    
    # Close open tags
    if in_list:
        html_lines.append('</ul>')
    if in_code:
        html_lines.append('</code></pre>')
    
    # Build full HTML document
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>{get_styles()}</style>
</head>
<body>
    <div class="header">
        <span class="header-title">// {html.escape(title)}</span>
        <div class="header-buttons">
            <span class="header-button">[_]</span>
            <span class="header-button">[■]</span>
            <span class="header-button">[X]</span>
        </div>
    </div>
    <div class="content wastes-container">
        {''.join(html_lines)}
    </div>
    <div class="footer">
        <pre class="ascii-decoration">~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~</pre>
    </div>
    <script>{get_script()}</script>
</body>
</html>'''

def process_inline(text):
    """Process inline markdown elements."""
    text = html.escape(text)
    # Bold (before italic to avoid conflicts)
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

def get_styles():
    """Return the Silicon Wastes CSS."""
    return '''
        :root {
            --ega-black: #000000;
            --ega-blue: #0000AA;
            --ega-green: #00AA00;
            --ega-cyan: #00AAAA;
            --ega-red: #AA0000;
            --ega-magenta: #AA00AA;
            --ega-brown: #AA5500;
            --ega-light-gray: #AAAAAA;
            --ega-dark-gray: #555555;
            --ega-light-blue: #5555FF;
            --ega-light-green: #55FF55;
            --ega-light-cyan: #55FFFF;
            --ega-light-red: #FF5555;
            --ega-light-magenta: #FF55FF;
            --ega-yellow: #FFFF55;
            --ega-white: #FFFFFF;
        }
        
        body { 
            margin: 0; padding: 0; 
            background: var(--ega-black); 
            color: var(--ega-light-gray); 
            font-family: "Fira Code", "Courier New", monospace; 
            font-size: 14px; 
            line-height: 1.6;
            background-image: 
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 170, 170, 0.03) 2px, rgba(0, 170, 170, 0.03) 4px),
                repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0, 170, 170, 0.03) 2px, rgba(0, 170, 170, 0.03) 4px);
            background-size: 100px 100px;
        }
        
        .header { 
            background: var(--ega-dark-gray); 
            color: var(--ega-light-cyan); 
            padding: 8px 15px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 2px solid var(--ega-cyan);
        }
        
        .header-title { 
            font-weight: bold; 
            text-shadow: 0 0 5px var(--ega-cyan); 
        }
        
        .header-buttons { display: flex; gap: 8px; }
        .header-button { color: var(--ega-light-gray); cursor: pointer; }
        
        .wastes-container { 
            max-width: 80ch; 
            margin: 20px auto; 
            padding: 30px; 
            border: 2px solid var(--ega-light-green); 
            box-shadow: 0 0 15px var(--ega-light-green), inset 0 0 10px var(--ega-green);
            background: rgba(0, 42, 0, 0.3);
            position: relative;
        }
        
        .wastes-container::before {
            content: "";
            position: absolute;
            top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(45deg, var(--ega-light-green), var(--ega-cyan), var(--ega-light-green));
            opacity: 0.1;
            animation: pulse 4s ease-in-out infinite;
            z-index: -1;
        }
        
        @keyframes pulse { 
            0%, 100% { opacity: 0.1; } 
            50% { opacity: 0.2; } 
        }
        
        h1, h2, h3 { text-shadow: 0 0 8px currentColor; }
        
        h1 { 
            color: var(--ega-yellow); 
            font-size: 2em; 
            margin: 1em 0 0.5em 0;
            text-align: center;
            border-bottom: 2px solid var(--ega-yellow);
            padding-bottom: 0.3em;
        }
        
        h2 { 
            color: var(--ega-light-cyan); 
            font-size: 1.5em; 
            margin-top: 1.5em;
            border-left: 4px solid var(--ega-cyan);
            padding-left: 10px;
        }
        
        h3 { 
            color: var(--ega-light-magenta); 
            font-size: 1.2em;
            margin-top: 1.2em;
        }
        
        p { margin: 1em 0; text-align: justify; }
        
        pre { 
            background: rgba(0, 0, 0, 0.8); 
            border: 1px solid var(--ega-green); 
            padding: 15px; 
            overflow-x: auto; 
            color: var(--ega-light-green);
            box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.1);
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        code { 
            color: var(--ega-light-magenta); 
            background: var(--ega-dark-gray); 
            padding: 2px 6px;
            border: 1px solid var(--ega-magenta);
        }
        
        ul { list-style-type: "▸ "; margin: 1em 0; padding-left: 25px; }
        ol { margin: 1em 0; padding-left: 25px; }
        li { margin: 8px 0; }
        
        a { 
            color: var(--ega-light-blue); 
            text-decoration: none;
            border-bottom: 1px dotted var(--ega-light-blue);
        }
        
        a:hover { 
            color: var(--ega-yellow); 
            text-shadow: 0 0 5px var(--ega-yellow);
            border-bottom-color: var(--ega-yellow);
        }
        
        strong { color: var(--ega-yellow); }
        em { color: var(--ega-light-cyan); font-style: italic; }
        
        hr { 
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--ega-green), transparent);
            margin: 2em 0;
        }
        
        blockquote {
            border-left: 4px solid var(--ega-light-green);
            padding-left: 20px;
            margin: 1.5em 0;
            color: var(--ega-light-cyan);
            font-style: italic;
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            color: var(--ega-dark-gray);
        }
        
        .ascii-decoration {
            color: var(--ega-green);
            font-size: 12px;
            animation: flicker 10s infinite;
        }
        
        @keyframes flicker { 
            0%, 100% { opacity: 0.5; } 
            50% { opacity: 0.8; }
        }
        
        /* Collapsible H2 sections */
        details {
            margin: 1em 0;
        }
        
        details summary {
            cursor: pointer;
            user-select: none;
            list-style: none;
        }
        
        details summary::-webkit-details-marker {
            display: none;
        }
        
        details summary h2 {
            display: inline-block;
            margin: 0;
        }
        
        details summary h2::before {
            content: "▸ ";
            display: inline-block;
            margin-right: 0.5em;
            transition: transform 0.2s;
        }
        
        details[open] summary h2::before {
            transform: rotate(90deg);
        }
        
        .section-content {
            padding-left: 14px;
            border-left: 2px solid var(--ega-dark-gray);
            margin-left: 10px;
            margin-top: 1em;
        }
    '''

def get_script():
    """Return the JavaScript for collapsible H2 sections."""
    return '''
        document.addEventListener('DOMContentLoaded', () => {
            const container = document.querySelector('.content');
            if (!container) return;
            
            const elements = Array.from(container.children);
            const newContent = [];
            let currentSection = null;
            
            for (let el of elements) {
                if (el.tagName === 'H2') {
                    // Start new section
                    currentSection = document.createElement('details');
                    currentSection.open = true; // Start open, user can close
                    
                    const summary = document.createElement('summary');
                    summary.appendChild(el.cloneNode(true));
                    currentSection.appendChild(summary);
                    
                    const content = document.createElement('div');
                    content.className = 'section-content';
                    currentSection.appendChild(content);
                    
                    newContent.push(currentSection);
                } else if (currentSection) {
                    // Add to current section
                    currentSection.querySelector('.section-content').appendChild(el.cloneNode(true));
                } else {
                    // Before first H2
                    newContent.push(el.cloneNode(true));
                }
            }
            
            // Replace content
            container.innerHTML = '';
            newContent.forEach(el => container.appendChild(el));
        });
    '''

def html_to_text(html_content):
    """Strip HTML to plain text."""
    # Remove script and style
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    # Convert breaks
    html_content = re.sub(r'<br\s*/?>', '\n', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</p>', '\n', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</?h[1-6]>', '\n', html_content, flags=re.IGNORECASE)
    # Strip tags
    html_content = re.sub(r'<[^>]+>', '', html_content)
    # Decode entities
    html_content = html.unescape(html_content)
    # Clean whitespace
    html_content = re.sub(r'\n{3,}', '\n\n', html_content)
    return html_content.strip()

def main():
    parser = argparse.ArgumentParser(
        description="MLNeotext - Markdown to Silicon Wastes HTML converter",
        epilog="""
Examples:
  mlneotext README.md                    # Convert to themed HTML
  mlneotext README.md --preview          # Convert and open in browser
  mlneotext page.html --strip --stdout   # Strip HTML to text
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input_file', help='Input file (markdown or HTML)')
    parser.add_argument('--strip', action='store_true', help='Strip HTML to plain text')
    parser.add_argument('--stdout', action='store_true', help='Output to stdout instead of file')
    parser.add_argument('--preview', action='store_true', help='Open in browser')
    
    args = parser.parse_args()
    
    input_file = Path(args.input_file)
    if not input_file.exists():
        print(f"Error: {input_file} not found", file=sys.stderr)
        sys.exit(1)
    
    content = input_file.read_text(encoding='utf-8')
    
    # Convert based on input type
    if input_file.suffix.lower() in ['.md', '.markdown']:
        if args.strip:
            # MD -> text (just strip markdown syntax)
            output = re.sub(r'#{1,6}\s+', '', content)
            output = re.sub(r'\*\*(.+?)\*\*', r'\1', output)
            output = re.sub(r'`(.+?)`', r'\1', output)
            is_html = False
        else:
            # MD -> HTML
            title = input_file.stem.replace('_', ' ').replace('-', ' ').title()
            output = md_to_html(content, title)
            is_html = True
    else:
        # HTML -> text
        output = html_to_text(content)
        is_html = False
    
    # Output handling
    if args.stdout:
        print(output)
    elif args.preview and is_html:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
            f.write(output)
            webbrowser.open_new_tab(f'file://{f.name}')
            print(f"Opened in browser: {f.name}")
    else:
        ext = '.html' if is_html else '.txt'
        output_file = input_file.with_suffix(ext)
        output_file.write_text(output, encoding='utf-8')
        print(f"Created: {output_file}")

if __name__ == "__main__":
    main()
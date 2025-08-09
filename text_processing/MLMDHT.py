#!/usr/bin/env python3
"""
MLHTMD - Markdown to HTML with JSON themes
Because why have config files when you have command lines?
"""

import sys
import json
import re
from pathlib import Path

class MLHTMD:
    """
    Convert Markdown to HTML.
    Theme it with JSON.
    Name colors in Latin-ish.
    This is the way.
    """
    
    DEFAULT_THEME = {
        "primarycolor": "#000000",
        "secondarycolor": "#00ff00", 
        "colortertius": "#333333",
        "fontprimary": "monospace",
        "fontsecundus": "serif",
        "backgroundum": "#ffffff",
        "borderradius": "0px",  # Rounded corners are complexity
        "maxwidthicus": "800px"
    }
    
    # Support both hex and named colors because we're not monsters
    # Just chaotic
    
    def __init__(self, theme_json=None):
        self.theme = self.DEFAULT_THEME.copy()
        
        if theme_json:
            try:
                custom = json.loads(theme_json)
                self.theme.update(custom)
                print(f"Theme loaded: {custom}")
            except:
                print("Invalid JSON theme, using defaults like a peasant")
    
    def markdown_to_html(self, md_text):
        """
        The world's simplest markdown parser.
        Because CommonMark is 50,000 lines.
        """
        html = md_text
        
        # Headers (h1-h6)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Code blocks
        html = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        
        # Links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
        
        # Paragraphs
        html = '<p>' + html.replace('\n\n', '</p><p>') + '</p>'
        
        # Lists (basic)
        html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
        
        return html
    
    def generate_html(self, md_content, title="MLHTMD Output"):
        """
        Generate complete HTML with JSON theme applied.
        No build step. No webpack. No nothing.
        Just f-strings and dreams.
        """
        
        html_content = self.markdown_to_html(md_content)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* MLHTMD Theme System - Powered by JSON and Latin-ish */
        
        body {{
            background: {self.theme.get('backgroundum', '#fff')};
            color: {self.theme['primarycolor']};
            font-family: {self.theme.get('fontprimary', 'sans-serif')};
            line-height: 1.6;
            max-width: {self.theme.get('maxwidthicus', '800px')};
            margin: 0 auto;
            padding: 20px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {self.theme['secondarycolor']};
            font-family: {self.theme.get('fontsecundus', 'serif')};
            margin-top: 2em;
            margin-bottom: 0.5em;
        }}
        
        h1 {{
            border-bottom: 3px solid {self.theme['colortertius']};
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            border-bottom: 1px solid {self.theme['colortertius']};
            padding-bottom: 0.2em;
        }}
        
        a {{
            color: {self.theme['secondarycolor']};
            text-decoration: none;
            border-bottom: 1px dotted {self.theme['colortertius']};
        }}
        
        a:hover {{
            color: {self.theme['colortertius']};
            border-bottom-style: solid;
        }}
        
        code {{
            background: {self.theme['colortertius']};
            color: {self.theme['primarycolor']};
            padding: 2px 6px;
            border-radius: {self.theme.get('borderradius', '3px')};
            font-family: {self.theme.get('fontprimary', 'monospace')};
        }}
        
        pre {{
            background: {self.theme['primarycolor']};
            color: {self.theme.get('backgroundum', '#fff')};
            padding: 15px;
            overflow-x: auto;
            border-left: 4px solid {self.theme['secondarycolor']};
        }}
        
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid {self.theme['colortertius']};
            margin-left: 0;
            padding-left: 20px;
            color: {self.theme['secondarycolor']};
            font-style: italic;
        }}
        
        ul, ol {{
            color: {self.theme['primarycolor']};
        }}
        
        li {{
            margin: 0.5em 0;
        }}
        
        strong {{
            color: {self.theme['secondarycolor']};
            font-weight: bold;
        }}
        
        em {{
            color: {self.theme['colortertius']};
        }}
        
        /* The Glory Section */
        .mlhtmd-footer {{
            margin-top: 4em;
            padding-top: 2em;
            border-top: 1px dashed {self.theme['colortertius']};
            text-align: center;
            font-size: 0.8em;
            color: {self.theme['colortertius']};
        }}
    </style>
</head>
<body>
    {html_content}
    
    <div class="mlhtmd-footer">
        Generated by MLHTMD - Themed with JSON - Colored with colortertius
    </div>
</body>
</html>"""

def main():
    """
    Usage: mlhtmd input.md output.html '{"primarycolor":"red","colortertius":"papayawhip"}'
    
    Or: mlhtmd input.md output.html
    (uses defaults like a coward)
    """
    
    if len(sys.argv) < 3:
        print("Usage: mlhtmd input.md output.html [theme_json]")
        print('Example: mlhtmd readme.md index.html \'{"primarycolor":"#ff0000","colortertius":"goldenrod"}\'')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    theme_json = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Read markdown
    try:
        with open(input_file, 'r') as f:
            md_content = f.read()
    except:
        print(f"Cannot read {input_file}, are you sure it exists?")
        sys.exit(1)
    
    # Create converter with theme
    converter = MLHTMD(theme_json)
    
    # Generate HTML
    html = converter.generate_html(md_content, title=Path(input_file).stem)
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"HTML generated: {output_file}")
    if theme_json:
        print("Theme applied: colortertius and friends")
    else:
        print("Default theme used (coward)")

if __name__ == "__main__":
    main()
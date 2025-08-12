#!/usr/bin/env python3
"""
MLTshirt - Magic Launcher T-shirt Design Generator
Generates SVG/ASCII designs for the revolution
No merch store, just shareable rebellion
Under 200 lines of wearable philosophy
"""

import sys
import random
from datetime import datetime

# Core slogans
SLOGANS = [
   "Bash, not buttons",
   "Simplicity as rebellion", 
   "Every feature questioned",
   "Docs in the code",
   "Tools don't leash you",
   "subprocess.run() everything",
   "Pipe the world",
   "Break the wrapper",
   "Config as manifest",
   "If it needs a cloud, it's a leash",
   "200 lines or less",
   "The revolution is 100 lines replacing 100,000",
   "Not a service. Not a platform. Just a tool.",
   "Speed is life, bloat is death",
   "Your empty GitHub is not moral failure",
]

# Code snippets that represent the philosophy
CODE_SNIPPETS = [
   "while universe.exists():\n    if button.clicked():\n        subprocess.run(thing)",
   "cat file | tool1 | tool2 > result\n# No framework needed",
   "def solve_problem(text):\n    return text.upper()\n# Ship it",
   "#!/usr/bin/env python3\n# 200 lines of revolution",
   "$ echo 'test' | python3 mltool.py\nTEST\n# Done. Ship it.",
]

def generate_ascii_shirt():
   """Generate ASCII art t-shirt design"""
   
   # Pick random slogans
   selected = random.sample(SLOGANS, min(5, len(SLOGANS)))
   
   design = []
   design.append("=" * 50)
   design.append("PROGRAMMER PUNK: Reclaim the terminal.")
   design.append("Break the wrapper. Pipe the world.")
   design.append("=" * 50)
   design.append("")
   
   for slogan in selected:
       icon = random.choice(['👊', '🔧', '📝', '🔥', '⚡'])
       design.append(f"{icon} {slogan}")
   
   design.append("")
   design.append("-" * 50)
   
   # Add random code snippet
   code = random.choice(CODE_SNIPPETS)
   design.append(code)
   
   design.append("-" * 50)
   design.append(f"Born: {datetime.now().year}")
   design.append("Not a service. Not a platform. Just a tool.")
   design.append("=" * 50)
   
   return "\n".join(design)

def generate_svg_shirt(width=400, height=500):
   """Generate SVG t-shirt design"""
   
   selected = random.sample(SLOGANS, min(5, len(SLOGANS)))
   
   svg = []
   svg.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
   svg.append('<rect width="100%" height="100%" fill="#000000"/>')
   
   # Terminal border
   svg.append('<rect x="20" y="20" width="360" height="460" fill="none" stroke="#00FF00" stroke-width="2"/>')
   
   # Header
   svg.append('<text x="200" y="60" text-anchor="middle" fill="#00FFFF" font-family="Courier New" font-size="14">')
   svg.append('Programmer Punk: Reclaim the terminal.')
   svg.append('</text>')
   
   svg.append('<text x="200" y="80" text-anchor="middle" fill="#00FFFF" font-family="Courier New" font-size="14">')
   svg.append('Break the wrapper. Pipe the world.')
   svg.append('</text>')
   
   # Slogans
   y_pos = 120
   colors = ['#00FF00', '#FF00FF', '#FFFF00', '#00FFFF', '#FFA500']
   
   for i, slogan in enumerate(selected):
       color = colors[i % len(colors)]
       icon = ['👊', '🔧', '📝', '🔥', '⚡'][i % 5]
       
       svg.append(f'<text x="40" y="{y_pos}" fill="{color}" font-family="Courier New" font-size="16">')
       svg.append(f'{icon} {slogan}')
       svg.append('</text>')
       y_pos += 40
   
   # Code block
   svg.append(f'<rect x="40" y="{y_pos}" width="320" height="100" fill="none" stroke="#00FF00" stroke-width="1"/>')
   y_pos += 30
   
   code_lines = [
       'while universe.exists():',
       '    if button.clicked():',
       '        subprocess.run(thing)'
   ]
   
   for line in code_lines:
       svg.append(f'<text x="50" y="{y_pos}" fill="#FFFFFF" font-family="Courier New" font-size="12">')
       svg.append(line)
       svg.append('</text>')
       y_pos += 20
   
   # Footer
   svg.append(f'<text x="200" y="{height-40}" text-anchor="middle" fill="#00FF00" font-family="Courier New" font-size="12">')
   svg.append('Not a service. Not a platform. Just a tool.')
   svg.append('</text>')
   
   svg.append('</svg>')
   
   return "\n".join(svg)

def generate_markdown_design():
   """Generate markdown-formatted design for sharing"""
   
   selected = random.sample(SLOGANS, 5)
   
   md = []
   md.append("# Magic Launcher T-Shirt Design")
   md.append("```")
   md.append("╔════════════════════════════════════════╗")
   md.append("║  PROGRAMMER PUNK: Born 2025            ║")
   md.append("║  Reclaim the terminal. Pipe the world. ║")
   md.append("╠════════════════════════════════════════╣")
   
   for slogan in selected:
       line = f"║  • {slogan}"
       line = line[:40] + " " * (40 - len(line)) + "║"
       md.append(line)
   
   md.append("╠════════════════════════════════════════╣")
   md.append("║  while universe.exists():              ║")
   md.append("║      if button.clicked():              ║")
   md.append("║          subprocess.run(thing)         ║")
   md.append("╚════════════════════════════════════════╝")
   md.append("```")
   md.append("\n## Print Instructions")
   md.append("- Black shirt recommended")
   md.append("- Use green (#00FF00) for terminal text")
   md.append("- Courier New or any monospace font")
   md.append("- No copyright, no license, just revolution")
   
   return "\n".join(md)

def main():
   if len(sys.argv) > 1:
       format_type = sys.argv[1].lower()
   else:
       format_type = 'ascii'
   
   if format_type == 'svg':
       print(generate_svg_shirt())
   elif format_type == 'markdown' or format_type == 'md':
       print(generate_markdown_design())
   else:
       print(generate_ascii_shirt())
   
   if format_type not in ['svg']:
       print("\n# Share freely. No store. No profit. Just revolution.")
       print("# Print at home, local shop, or just wear the philosophy.")

if __name__ == "__main__":
   main()
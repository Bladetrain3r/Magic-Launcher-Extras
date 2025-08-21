#!/usr/bin/env python3
"""
MLTT2HT - Terminal Text to HTML
Converts terminal output into static HTML dashboards
Perfect for wttr.in, cheat.sh, and other text services
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import html
import json
import re

class MLTT2HT:
    def __init__(self, output_file="dashboard.html", title="Terminal Dashboard"):
        self.output_file = Path(output_file)
        self.title = title
        self.sections = []
        
    def strip_ansi(self, text):
        """Remove ANSI escape sequences from text"""
        import re
        # Remove ANSI escape codes
        ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by parameter bytes
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        ''', re.VERBOSE)
        return ansi_escape.sub('', text)
    
    def add_command(self, name, command, refresh=False):
        """Execute command and capture output"""
        try:
            if isinstance(command, str):
                # Shell command
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout
                if result.stderr:
                    output += f"\n[STDERR]\n{result.stderr}"
            else:
                # Command list
                result = subprocess.run(command, capture_output=True, text=True)
                output = result.stdout
                if result.stderr:
                    output += f"\n[STDERR]\n{result.stderr}"
                    
        except Exception as e:
            output = f"Error executing command: {str(e)}"
        
        # Strip ANSI codes
        output = self.strip_ansi(output)
        
        self.sections.append({
            'name': name,
            'command': command if isinstance(command, str) else ' '.join(command),
            'output': output,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'refresh': refresh
        })
        
    def add_text(self, name, text, source=None):
        """Add pre-captured text output"""
        # Strip ANSI codes
        text = self.strip_ansi(text)
        
        self.sections.append({
            'name': name,
            'command': source or 'Static text',
            'output': text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'refresh': False
        })
    
    def generate_html(self, auto_refresh=0):
        """Generate the HTML dashboard"""
        # Escape outputs for HTML
        for section in self.sections:
            section['output_escaped'] = html.escape(section['output'])
        
        html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    {refresh_meta}
    <style>
        body {{
            font-family: monospace;
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            margin: 0;
        }}
        h1 {{
            color: #4ec9b0;
            border-bottom: 2px solid #4ec9b0;
            padding-bottom: 10px;
        }}
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }}
        .section {{
            background: #252526;
            border: 1px solid #3e3e42;
            border-radius: 5px;
            overflow: hidden;
        }}
        .section-header {{
            background: #2d2d30;
            padding: 10px;
            border-bottom: 1px solid #3e3e42;
        }}
        .section-title {{
            color: #4ec9b0;
            font-weight: bold;
            font-size: 14px;
        }}
        .section-meta {{
            color: #858585;
            font-size: 11px;
            margin-top: 5px;
        }}
        .section-content {{
            padding: 10px;
            overflow-x: auto;
        }}
        pre {{
            margin: 0;
            white-space: pre;
            color: #d4d4d4;
            font-size: 12px;
            line-height: 1.4;
        }}
        .update-time {{
            color: #858585;
            text-align: right;
            padding: 10px;
            font-size: 11px;
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        /* ANSI color support */
        .ansi-black {{ color: #000000; }}
        .ansi-red {{ color: #cd3131; }}
        .ansi-green {{ color: #0dbc79; }}
        .ansi-yellow {{ color: #e5e510; }}
        .ansi-blue {{ color: #2472c8; }}
        .ansi-magenta {{ color: #bc3fbc; }}
        .ansi-cyan {{ color: #11a8cd; }}
        .ansi-white {{ color: #e5e5e5; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="dashboard">
        {sections}
    </div>
    <div class="update-time">
        Last updated: {last_update}
        {refresh_notice}
    </div>
</body>
</html>'''

        refresh_meta = ""
        refresh_notice = ""
        if auto_refresh > 0:
            refresh_meta = f'<meta http-equiv="refresh" content="{auto_refresh}">'
            refresh_notice = f' (Auto-refresh every {auto_refresh}s)'

        sections_html = []
        for section in self.sections:
            # Determine if section should be full width (for wide outputs like weather)
            full_width = len(section['output'].split('\n')[0]) > 80 if section['output'] else False
            width_class = 'section full-width' if full_width else 'section'
            
            section_html = f'''
        <div class="{width_class}">
            <div class="section-header">
                <div class="section-title">{section['name']}</div>
                <div class="section-meta">$ {html.escape(section['command'])} | {section['timestamp']}</div>
            </div>
            <div class="section-content">
                <pre>{section['output_escaped']}</pre>
            </div>
        </div>'''
            sections_html.append(section_html)
        
        return html_template.format(
            title=self.title,
            refresh_meta=refresh_meta,
            sections=''.join(sections_html),
            last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            refresh_notice=refresh_notice
        )
    
    def save(self, auto_refresh=0):
        """Save the HTML dashboard to file"""
        html_content = self.generate_html(auto_refresh)
        with open(self.output_file, 'w') as f:
            f.write(html_content)
        print(f"Dashboard saved to: {self.output_file}")
        
    def from_config(self, config_file):
        """Load dashboard configuration from JSON"""
        with open(config_file) as f:
            config = json.load(f)
        
        self.title = config.get('title', self.title)
        self.output_file = Path(config.get('output', self.output_file))
        
        for item in config.get('sections', []):
            if 'command' in item:
                self.add_command(item['name'], item['command'])
            elif 'text' in item:
                self.add_text(item['name'], item['text'])

def main():
    parser = argparse.ArgumentParser(description='Convert terminal output to HTML dashboard')
    parser.add_argument('-o', '--output', default='dashboard.html', help='Output HTML file')
    parser.add_argument('-t', '--title', default='Terminal Dashboard', help='Dashboard title')
    parser.add_argument('-r', '--refresh', type=int, default=0, help='Auto-refresh interval (seconds)')
    parser.add_argument('-c', '--config', help='Load configuration from JSON file')
    parser.add_argument('-e', '--example', action='store_true', help='Generate example dashboard')
    parser.add_argument('commands', nargs='*', help='Commands to execute (format: "name:command")')
    
    args = parser.parse_args()
    
    dashboard = MLTT2HT(args.output, args.title)
    
    if args.example:
        # Generate example dashboard
        dashboard.add_command("Weather", "curl -s wttr.in?0")
        dashboard.add_command("System Info", "uname -a && uptime")
        dashboard.add_command("Memory", "free -h")
        dashboard.add_command("Disk Usage", "df -h")
        dashboard.add_command("Network", "ip a | head -20")
        dashboard.add_command("Date", "date")
        dashboard.save(args.refresh)
        return
    
    if args.config:
        # Load from config file
        dashboard.from_config(args.config)
    
    # Add commands from arguments
    for cmd_spec in args.commands:
        if ':' in cmd_spec:
            name, command = cmd_spec.split(':', 1)
            dashboard.add_command(name, command)
        else:
            dashboard.add_command(cmd_spec, cmd_spec)
    
    # Read from stdin if no commands specified
    if not args.commands and not args.config and not sys.stdin.isatty():
        stdin_text = sys.stdin.read()
        dashboard.add_text("Terminal Output", stdin_text, "stdin")
    
    if dashboard.sections:
        dashboard.save(args.refresh)
    else:
        print("No content to generate. Use -e for example or provide commands.")

if __name__ == "__main__":
    main()
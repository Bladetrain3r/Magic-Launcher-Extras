#!/usr/bin/env python3
"""
QuickCapture - Minimal friction note capture for MagicProjects
Usage: python quickcapture.py
       Then type: "project: note" and hit Enter
       Or just: "note" to go to inbox
       Escape to cancel
"""

import tkinter as tk
from pathlib import Path
import sys

# Add components path for MagicProjects imports
sys.path.insert(0, str(Path(__file__).parent / 'components'))

from controller import ProjectController

DEFAULT_PROJECT = "inbox"

class QuickCapture:
    def __init__(self):
        self.controller = ProjectController()
        self.root = tk.Tk()
        self._setup_window()
        self._setup_entry()
        self._bind_keys()
    
    def _setup_window(self):
        """Minimal floating window"""
        self.root.title("⚡")
        self.root.overrideredirect(True)  # No window decorations
        self.root.attributes('-topmost', True)  # Always on top
        
        # Center on screen
        width, height = 400, 32
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 3  # Upper third
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Dark theme
        self.root.configure(bg='#1a1a1a')
    
    def _setup_entry(self):
        """Single input field"""
        self.entry = tk.Entry(
            self.root,
            font=('Consolas', 12),
            bg='#1a1a1a',
            fg='#00ff88',
            insertbackground='#00ff88',
            relief='flat',
            borderwidth=8
        )
        self.entry.pack(fill='both', expand=True)
        self.entry.focus_set()
    
    def _bind_keys(self):
        """Escape to cancel, Enter to submit"""
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<Return>', self._submit)
        self.root.bind('<FocusOut>', lambda e: self.root.destroy())
    
    def _parse_input(self, text: str) -> tuple:
        """
        Parse 'project: note' format
        Returns (project, note)
        """
        text = text.strip()
        if not text:
            return None, None
        
        if ':' in text:
            parts = text.split(':', 1)
            project = parts[0].strip()
            note = parts[1].strip() if len(parts) > 1 else ""
            return project or DEFAULT_PROJECT, note
        else:
            # No colon = inbox
            return DEFAULT_PROJECT, text
    
    def _submit(self, event=None):
        """Parse input, spark project, close"""
        text = self.entry.get()
        project, note = self._parse_input(text)
        
        if project and note:
            try:
                self.controller.spark(project, note)
                print(f"⚡ {project}: {note}")
            except Exception as e:
                print(f"Error: {e}")
        elif project and not note:
            # Just project name, spark without task
            try:
                self.controller.spark(project)
                print(f"⚡ {project} (no task)")
            except Exception as e:
                print(f"Error: {e}")
        
        self.root.destroy()
    
    def run(self):
        """Show window and wait for input"""
        self.root.mainloop()


def main():
    app = QuickCapture()
    app.run()


if __name__ == '__main__':
    main()

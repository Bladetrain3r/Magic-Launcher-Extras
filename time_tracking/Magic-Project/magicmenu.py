#!/usr/bin/env python3
"""
Magic Projects Menu - Keyboard-driven project manager GUI
Hotkeys work when window is focused.
"""

import tkinter as tk
from tkinter import simpledialog
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / 'components'))

from controller import ProjectController

# Theme
BG = '#1a1a1a'
FG = '#00ff88'
FG_DIM = '#008844'
FG_HOT = '#ff6644'
FG_WARM = '#ffaa00'
FG_COLD = '#4488ff'
FG_FROZEN = '#666666'
SELECT_BG = '#333333'
FONT = ('Consolas', 11)
FONT_BOLD = ('Consolas', 11, 'bold')


class MagicMenu:
    def __init__(self):
        self.controller = ProjectController()
        self.selected_index = 0
        self.projects = []
        self.view = 'list'  # 'list' or 'tasks'
        self.current_project = None
        
        self.root = tk.Tk()
        self._setup_window()
        self._setup_ui()
        self._bind_keys()
        self._refresh()
    
    def _setup_window(self):
        self.root.title("⚡ Magic Projects")
        self.root.configure(bg=BG)
        self.root.geometry("500x400")
        self.root.minsize(400, 300)
    
    def _setup_ui(self):
        # Header
        self.header = tk.Label(
            self.root, text="MAGIC PROJECTS", 
            font=FONT_BOLD, bg=BG, fg=FG
        )
        self.header.pack(fill='x', padx=10, pady=(10, 5))
        
        # Main list area
        self.list_frame = tk.Frame(self.root, bg=BG)
        self.list_frame.pack(fill='both', expand=True, padx=10)
        
        # Canvas for scrollable list
        self.canvas = tk.Canvas(self.list_frame, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_frame, orient='vertical', command=self.canvas.yview)
        self.inner_frame = tk.Frame(self.canvas, bg=BG)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        self.inner_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        
        # Status bar
        self.status = tk.Label(
            self.root, text="", font=FONT, bg=BG, fg=FG_DIM, anchor='w'
        )
        self.status.pack(fill='x', padx=10, pady=(5, 5))
        
        # Hotkey hints
        self.hints = tk.Label(
            self.root, 
            text="[s]park [c]omplete [f]reeze [r]efresh [q]uit | [↑↓/jk] nav [Enter] select [Esc] back",
            font=('Consolas', 9), bg=BG, fg=FG_DIM
        )
        self.hints.pack(fill='x', padx=10, pady=(0, 10))
    
    def _bind_keys(self):
        self.root.bind('<Up>', lambda e: self._navigate(-1))
        self.root.bind('<Down>', lambda e: self._navigate(1))
        self.root.bind('k', lambda e: self._navigate(-1))
        self.root.bind('j', lambda e: self._navigate(1))
        self.root.bind('<Return>', lambda e: self._select())
        self.root.bind('<Escape>', lambda e: self._back())
        self.root.bind('s', lambda e: self._spark())
        self.root.bind('c', lambda e: self._complete())
        self.root.bind('f', lambda e: self._freeze())
        self.root.bind('r', lambda e: self._refresh())
        self.root.bind('q', lambda e: self.root.destroy())
        self.root.bind('a', lambda e: self._add_task())
    
    def _heat_color(self, state):
        return {
            'hot': FG_HOT,
            'warm': FG_WARM,
            'cold': FG_COLD,
            'frozen': FG_FROZEN
        }.get(state, FG)
    
    def _render_list(self):
        """Render project list view"""
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        
        if not self.projects:
            label = tk.Label(
                self.inner_frame, text="No projects. Press [s] to spark one.",
                font=FONT, bg=BG, fg=FG_DIM, anchor='w'
            )
            label.pack(fill='x', pady=2)
            return
        
        for i, project in enumerate(self.projects):
            is_selected = (i == self.selected_index)
            bg = SELECT_BG if is_selected else BG
            
            frame = tk.Frame(self.inner_frame, bg=bg)
            frame.pack(fill='x', pady=1)
            
            # Selection indicator
            indicator = ">" if is_selected else " "
            
            # Format: > 0: name          state   N tasks
            name = project['name'][:20].ljust(20)
            state = project['state'].ljust(6)
            tasks = f"{project.get('active_tasks', 0)} tasks"
            
            text = f" {indicator} {i}: {name} {state} {tasks}"
            
            label = tk.Label(
                frame, text=text, font=FONT, 
                bg=bg, fg=self._heat_color(project['state']), 
                anchor='w'
            )
            label.pack(fill='x')
        
        self.header.config(text="MAGIC PROJECTS")
        self.status.config(text=f"{len(self.projects)} projects")
    
    def _render_tasks(self):
        """Render task view for selected project"""
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        
        if not self.current_project:
            return
        
        project = self.controller.get_project_status(self.current_project)
        if not project:
            return
        
        tasks = project.get('tasks', [])
        active_tasks = [t for t in tasks if t.get('completed') is None]
        completed_tasks = [t for t in tasks if t.get('completed') is not None]
        
        self.task_list = active_tasks  # Store for completion
        
        if not tasks:
            label = tk.Label(
                self.inner_frame, text="No tasks. Press [a] to add one.",
                font=FONT, bg=BG, fg=FG_DIM, anchor='w'
            )
            label.pack(fill='x', pady=2)
        else:
            # Active tasks first
            for i, task in enumerate(active_tasks):
                is_selected = (i == self.selected_index)
                bg = SELECT_BG if is_selected else BG
                
                frame = tk.Frame(self.inner_frame, bg=bg)
                frame.pack(fill='x', pady=1)
                
                indicator = ">" if is_selected else " "
                priority = task.get('priority', 'MEDIUM')[0]
                text = f" {indicator} ○ [{priority}] {task['note'][:50]}"
                
                label = tk.Label(
                    frame, text=text, font=FONT, bg=bg, fg=FG, anchor='w'
                )
                label.pack(fill='x')
            
            # Completed tasks (dimmed)
            if completed_tasks:
                sep = tk.Label(
                    self.inner_frame, text=" ── completed ──",
                    font=FONT, bg=BG, fg=FG_DIM, anchor='w'
                )
                sep.pack(fill='x', pady=(10, 2))
                
                for task in completed_tasks[-5:]:  # Show last 5 completed
                    frame = tk.Frame(self.inner_frame, bg=BG)
                    frame.pack(fill='x', pady=1)
                    
                    symbol = "✗" if task.get('state') == 'declined' else "✓"
                    text = f"   {symbol} {task['note'][:50]}"
                    
                    label = tk.Label(
                        frame, text=text, font=FONT, bg=BG, fg=FG_DIM, anchor='w'
                    )
                    label.pack(fill='x')
        
        self.header.config(text=f"⚡ {project['name']}")
        self.status.config(text=f"{len(active_tasks)} active, {len(completed_tasks)} done")
    
    def _refresh(self):
        """Reload data and render"""
        self.projects = self.controller.status(include_frozen=True)
        self.selected_index = min(self.selected_index, max(0, len(self.projects) - 1))
        
        if self.view == 'list':
            self._render_list()
        else:
            self._render_tasks()
    
    def _navigate(self, delta):
        """Move selection up/down"""
        if self.view == 'list':
            max_idx = len(self.projects) - 1
        else:
            max_idx = len(getattr(self, 'task_list', [])) - 1
        
        if max_idx < 0:
            return
        
        self.selected_index = max(0, min(max_idx, self.selected_index + delta))
        
        if self.view == 'list':
            self._render_list()
        else:
            self._render_tasks()
    
    def _select(self):
        """Enter task view for selected project"""
        if self.view == 'list' and self.projects:
            self.current_project = self.projects[self.selected_index]['name']
            self.view = 'tasks'
            self.selected_index = 0
            self._render_tasks()
    
    def _back(self):
        """Return to list view"""
        if self.view == 'tasks':
            self.view = 'list'
            self.selected_index = 0
            self._refresh()
    
    def _spark(self):
        """Spark dialog"""
        result = simpledialog.askstring(
            "Spark", "project: task (or just project name)",
            parent=self.root
        )
        if result:
            result = result.strip()
            if ':' in result:
                parts = result.split(':', 1)
                project = parts[0].strip()
                task = parts[1].strip()
                self.controller.spark(project, task)
            else:
                self.controller.spark(result)
            self._refresh()
    
    def _add_task(self):
        """Add task to current project"""
        if self.view != 'tasks' or not self.current_project:
            return
        
        result = simpledialog.askstring(
            "Add Task", f"Task for {self.current_project}:",
            parent=self.root
        )
        if result:
            self.controller.add_task(self.current_project, result.strip())
            self._refresh()
    
    def _complete(self):
        """Complete selected task"""
        if self.view == 'tasks' and hasattr(self, 'task_list') and self.task_list:
            task = self.task_list[self.selected_index]
            try:
                self.controller.complete_task(self.current_project, task['note'][:20])
                self._refresh()
            except Exception as e:
                self.status.config(text=f"Error: {e}")
        elif self.view == 'list':
            self.status.config(text="Press Enter to select project first")
    
    def _freeze(self):
        """Freeze/unfreeze selected project"""
        if self.view == 'list' and self.projects:
            project = self.projects[self.selected_index]
            if project['state'] == 'frozen':
                self.controller.unfreeze_project(project['name'])
            else:
                self.controller.freeze_project(project['name'])
            self._refresh()
    
    def run(self):
        self.root.mainloop()


def main():
    app = MagicMenu()
    app.run()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
MLScatter - X-Y scatter plot for relationship viewing
Part of ML-Extras

Purpose primitive: See if two things relate. That's it.
Not time series (use MLPlot), just pure X-Y correlation viewing.

Usage:
    mlscatter data.csv                 # GUI mode, columns 1 & 2
    mlscatter data.csv --x 2 --y 3     # Specific columns
    mlscatter data.csv --terminal      # Terminal mode with density
    cat data.csv | mlscatter -         # Read from stdin
    
Terminal mode uses density characters: · ∘ ○ ◉ ●
GUI mode matches MLPlot aesthetic for consistency
"""

import sys
import csv
import math
from pathlib import Path

# Terminal mode density characters
DENSITY_CHARS = [' ', '·', '∘', '○', '◉', '●']

class TerminalScatter:
    """Terminal-based scatter plot using ASCII density"""
    
    def __init__(self, width=60, height=20):
        self.width = width
        self.height = height
        
    def render(self, data, xlabel="X", ylabel="Y"):
        """Render scatter plot in terminal"""
        if not data or len(data) < 2:
            return "No data to plot"
        
        # Get ranges
        x_vals = [p[0] for p in data]
        y_vals = [p[1] for p in data]
        
        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)
        
        # Add padding
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1
        
        # Create density grid
        grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Map points to grid
        for x, y in data:
            # Map to grid coordinates
            gx = int((x - x_min) / x_range * (self.width - 1))
            gy = int((y - y_min) / y_range * (self.height - 1))
            gy = self.height - 1 - gy  # Flip Y axis
            
            # Bounds check
            gx = max(0, min(self.width - 1, gx))
            gy = max(0, min(self.height - 1, gy))
            
            # Increment density
            grid[gy][gx] = min(grid[gy][gx] + 1, len(DENSITY_CHARS) - 1)
        
        # Render output
        output = []
        
        # Title
        output.append(f"{ylabel} vs {xlabel}")
        output.append("=" * self.width)
        
        # Y axis top label
        output.append(f"{y_max:.2f}")
        
        # Grid
        for row in grid:
            line = '|'
            for density in row:
                line += DENSITY_CHARS[density]
            output.append(line)
        
        # Y axis bottom label and X axis
        output.append(f"{y_min:.2f}" + "-" * (self.width - len(f"{y_min:.2f}")))
        output.append(f"{x_min:.2f}" + " " * (self.width - len(f"{x_min:.2f}") - len(f"{x_max:.2f}")) + f"{x_max:.2f}")
        
        # Stats
        output.append("")
        output.append(f"Points: {len(data)} | X: [{x_min:.2f}, {x_max:.2f}] | Y: [{y_min:.2f}, {y_max:.2f}]")
        
        # Quick correlation
        if len(data) > 2:
            correlation = self._calculate_correlation(x_vals, y_vals)
            if correlation is not None:
                output.append(f"Correlation: {correlation:.3f}")
        
        return '\n'.join(output)
    
    def _calculate_correlation(self, x_vals, y_vals):
        """Calculate Pearson correlation coefficient"""
        n = len(x_vals)
        if n < 2:
            return None
            
        # Calculate means
        x_mean = sum(x_vals) / n
        y_mean = sum(y_vals) / n
        
        # Calculate correlation components
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
        
        x_squared = sum((x - x_mean) ** 2 for x in x_vals)
        y_squared = sum((y - y_mean) ** 2 for y in y_vals)
        
        denominator = math.sqrt(x_squared * y_squared)
        
        if denominator == 0:
            return 0
            
        return numerator / denominator

# GUI mode with tkinter
try:
    import tkinter as tk
    GUI_AVAILABLE = True
    
    # ML-style constants
    COLORS = {
        'dark_gray': '#3C3C3C',
        'light_gray': '#C0C0C0',
        'green': '#00FF00',
        'white': '#FFFFFF',
        'black': '#000000',
        'red': '#FF0000',
        'blue': '#0080FF'
    }
    
    class MLScatter:
        def __init__(self, root, data, xlabel="X", ylabel="Y", title=""):
            self.root = root
            self.root.title(f"MLScatter - {title}" if title else "MLScatter")
            self.root.geometry("800x600")
            self.root.configure(bg=COLORS['dark_gray'])
            
            self.data = data
            self.xlabel = xlabel
            self.ylabel = ylabel
            self.title = title
            
            # Zoom state
            self.zoom_level = 1.0
            self.pan_x = 0
            self.pan_y = 0
            
            self._create_ui()
            self._plot_data()
        
        def _create_ui(self):
            """Create the UI matching ML aesthetic"""
            # Title bar
            title_frame = tk.Frame(self.root, bg=COLORS['light_gray'], 
                                  height=40, relief='raised', bd=2)
            title_frame.pack(fill='x')
            title_frame.pack_propagate(False)
            
            # Title label
            title_text = self.title if self.title else "Scatter Plot"
            tk.Label(title_frame, text=title_text,
                    bg=COLORS['green'], fg=COLORS['black'],
                    font=('Courier', 14, 'bold')).pack(expand=True, fill='both', padx=2, pady=2)
            
            # Canvas for plot
            self.canvas = tk.Canvas(self.root, bg=COLORS['black'], 
                                   highlightthickness=0)
            self.canvas.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Bind events
            self.canvas.bind('<Configure>', lambda e: self._plot_data())
            self.canvas.bind('<Button-1>', self._on_click)
            self.canvas.bind('<B1-Motion>', self._on_drag)
            self.canvas.bind('<MouseWheel>', self._on_scroll)
            self.canvas.bind('<Button-4>', self._on_scroll)  # Linux
            self.canvas.bind('<Button-5>', self._on_scroll)  # Linux
            
            # Status bar
            self.status = tk.Label(self.root, text=f"Points: {len(self.data)}",
                                  bg=COLORS['light_gray'], fg=COLORS['black'],
                                  anchor='w', padx=5)
            self.status.pack(fill='x')
            
            # Info button
            info_frame = tk.Frame(self.root, bg=COLORS['light_gray'])
            info_frame.pack(fill='x')
            
            tk.Button(info_frame, text="Reset View", 
                     bg=COLORS['light_gray'], fg=COLORS['black'],
                     font=('Courier', 10), bd=1,
                     command=self._reset_view).pack(side='left', padx=5)
            
            tk.Button(info_frame, text="?", 
                     bg=COLORS['light_gray'], fg=COLORS['black'],
                     font=('Courier', 10, 'bold'), bd=1, padx=10,
                     command=self._show_help).pack(side='right', padx=5)
            
            # Keyboard shortcuts
            self.root.bind('<Control-q>', lambda e: self.root.quit())
            self.root.bind('<Escape>', lambda e: self.root.quit())
            self.root.bind('<r>', lambda e: self._reset_view())
            self.root.bind('<Control-0>', lambda e: self._reset_view())
            
            # Mouse state for dragging
            self.drag_start = None
        
        def _on_click(self, event):
            """Start drag"""
            self.drag_start = (event.x, event.y)
        
        def _on_drag(self, event):
            """Pan view"""
            if self.drag_start:
                dx = event.x - self.drag_start[0]
                dy = event.y - self.drag_start[1]
                self.pan_x += dx
                self.pan_y += dy
                self.drag_start = (event.x, event.y)
                self._plot_data()
        
        def _on_scroll(self, event):
            """Zoom view"""
            # Handle both Windows and Linux scroll events
            if event.delta:
                delta = event.delta / 120
            else:
                delta = -1 if event.num == 5 else 1
            
            zoom_factor = 1.1 if delta > 0 else 0.9
            self.zoom_level *= zoom_factor
            self.zoom_level = max(0.1, min(10, self.zoom_level))
            self._plot_data()
        
        def _reset_view(self):
            """Reset zoom and pan"""
            self.zoom_level = 1.0
            self.pan_x = 0
            self.pan_y = 0
            self._plot_data()
        
        def _plot_data(self):
            """Plot the scatter data"""
            self.canvas.delete('all')
            
            if not self.data or len(self.data) < 1:
                self.canvas.create_text(400, 300, text="No data to plot",
                                       fill=COLORS['green'], font=('Courier', 20))
                return
            
            # Get canvas dimensions
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if width < 100 or height < 100:
                return  # Too small
            
            # Margins
            margin = 50
            plot_width = width - 2 * margin
            plot_height = height - 2 * margin
            
            # Find data ranges
            x_values = [point[0] for point in self.data]
            y_values = [point[1] for point in self.data]
            
            x_min, x_max = min(x_values), max(x_values)
            y_min, y_max = min(y_values), max(y_values)
            
            # Add padding
            x_range = x_max - x_min if x_max != x_min else 1
            y_range = y_max - y_min if y_max != y_min else 1
            
            x_padding = x_range * 0.1
            y_padding = y_range * 0.1
            
            x_min -= x_padding
            x_max += x_padding
            y_min -= y_padding
            y_max += y_padding
            
            # Apply zoom
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            
            x_span = (x_max - x_min) / self.zoom_level
            y_span = (y_max - y_min) / self.zoom_level
            
            x_min = x_center - x_span / 2
            x_max = x_center + x_span / 2
            y_min = y_center - y_span / 2
            y_max = y_center + y_span / 2
            
            # Draw axes
            self.canvas.create_line(margin, height - margin, width - margin, height - margin,
                                   fill=COLORS['white'], width=2)  # X axis
            self.canvas.create_line(margin, margin, margin, height - margin,
                                   fill=COLORS['white'], width=2)  # Y axis
            
            # Draw labels
            self.canvas.create_text(width // 2, height - 10, text=self.xlabel,
                                   fill=COLORS['white'], font=('Courier', 10))
            self.canvas.create_text(20, height // 2, text=self.ylabel, angle=90,
                                   fill=COLORS['white'], font=('Courier', 10))
            
            # Draw grid lines
            for i in range(5):
                # Horizontal
                y = margin + i * plot_height / 4
                self.canvas.create_line(margin, y, width - margin, y,
                                       fill=COLORS['dark_gray'], dash=(2, 4))
                value = y_max - i * (y_max - y_min) / 4
                self.canvas.create_text(margin - 10, y, text=f"{value:.1f}",
                                       anchor='e', fill=COLORS['white'], font=('Courier', 8))
                
                # Vertical
                x = margin + i * plot_width / 4
                self.canvas.create_line(x, margin, x, height - margin,
                                       fill=COLORS['dark_gray'], dash=(2, 4))
                value = x_min + i * (x_max - x_min) / 4
                self.canvas.create_text(x, height - margin + 10, text=f"{value:.1f}",
                                       fill=COLORS['white'], font=('Courier', 8))
            
            # Scale for plotting
            x_scale = plot_width / (x_max - x_min) if x_max != x_min else 1
            y_scale = plot_height / (y_max - y_min) if y_max != y_min else 1
            
            # Plot points
            point_size = 4 if len(self.data) < 100 else 3 if len(self.data) < 1000 else 2
            
            for x, y in self.data:
                # Skip points outside view
                if x < x_min or x > x_max or y < y_min or y > y_max:
                    continue
                    
                px = margin + (x - x_min) * x_scale + self.pan_x
                py = height - margin - (y - y_min) * y_scale + self.pan_y
                
                # Only draw if on canvas
                if margin <= px <= width - margin and margin <= py <= height - margin:
                    self.canvas.create_oval(px - point_size, py - point_size, 
                                          px + point_size, py + point_size,
                                          fill=COLORS['green'], outline=COLORS['green'])
            
            # Calculate and show correlation
            if len(self.data) > 2:
                correlation = self._calculate_correlation(x_values, y_values)
                if correlation is not None:
                    corr_text = f"r = {correlation:.3f}"
                    self.canvas.create_text(width - margin - 50, margin + 20, 
                                          text=corr_text,
                                          fill=COLORS['blue'], font=('Courier', 12, 'bold'))
            
            # Update status
            self.status.config(text=f"Points: {len(self.data)} | "
                                   f"X: [{x_min:.2f}, {x_max:.2f}] | "
                                   f"Y: [{y_min:.2f}, {y_max:.2f}] | "
                                   f"Zoom: {self.zoom_level:.1f}x")
        
        def _calculate_correlation(self, x_vals, y_vals):
            """Calculate Pearson correlation"""
            n = len(x_vals)
            if n < 2:
                return None
                
            x_mean = sum(x_vals) / n
            y_mean = sum(y_vals) / n
            
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
            
            x_squared = sum((x - x_mean) ** 2 for x in x_vals)
            y_squared = sum((y - y_mean) ** 2 for y in y_vals)
            
            denominator = math.sqrt(x_squared * y_squared) if x_squared * y_squared > 0 else 0
            
            return numerator / denominator if denominator != 0 else 0
        
        def _show_help(self):
            """Show help dialog"""
            import tkinter.messagebox as messagebox
            help_text = """MLScatter v1.0 - Relationship Viewer

Controls:
  Click & Drag     Pan view
  Mouse Wheel      Zoom in/out
  R                Reset view
  Ctrl+Q           Quit
  Escape           Quit

Features:
• Pearson correlation (r) shown
• Interactive zoom and pan
• Automatic axis scaling
• Works with stdin piping

Part of ML-Extras collection
No dependencies, no bullshit"""
            
            messagebox.showinfo("MLScatter Help", help_text)
    
except ImportError:
    GUI_AVAILABLE = False
    print("Note: tkinter not available, terminal mode only")

def load_csv(filename, x_col=0, y_col=1):
    """Load data from CSV file"""
    data = []
    
    # Handle stdin
    if filename == '-':
        import sys
        lines = sys.stdin.readlines()
        reader = csv.reader(lines)
    else:
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return data
    
    # Process rows
    for row_idx, row in enumerate(rows if filename != '-' else reader):
        # Skip header if detected
        if row_idx == 0:
            try:
                float(row[x_col])
                float(row[y_col])
            except (ValueError, IndexError):
                continue  # Skip header
        
        # Extract x, y values
        try:
            if len(row) > max(x_col, y_col):
                x = float(row[x_col])
                y = float(row[y_col])
                data.append((x, y))
        except (ValueError, IndexError):
            continue  # Skip bad rows
    
    return data

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="X-Y scatter plot for relationships")
    parser.add_argument('file', help='CSV file (use - for stdin)')
    parser.add_argument('--x', type=int, default=0, help='X column index (default: 0)')
    parser.add_argument('--y', type=int, default=1, help='Y column index (default: 1)')
    parser.add_argument('--xlabel', default='X', help='X axis label')
    parser.add_argument('--ylabel', default='Y', help='Y axis label')
    parser.add_argument('--title', help='Plot title')
    parser.add_argument('--terminal', action='store_true', help='Use terminal mode')
    parser.add_argument('--width', type=int, default=60, help='Terminal width')
    parser.add_argument('--height', type=int, default=20, help='Terminal height')
    
    args = parser.parse_args()
    
    # Load data
    data = load_csv(args.file, args.x, args.y)
    
    if not data:
        print(f"No valid data found in {args.file}")
        sys.exit(1)
    
    # Choose mode
    if args.terminal or not GUI_AVAILABLE:
        # Terminal mode
        scatter = TerminalScatter(width=args.width, height=args.height)
        print(scatter.render(data, args.xlabel, args.ylabel))
    else:
        # GUI mode
        if not GUI_AVAILABLE:
            print("Error: tkinter not available for GUI mode")
            sys.exit(1)
            
        title = args.title or Path(args.file).stem if args.file != '-' else "stdin"
        
        root = tk.Tk()
        app = MLScatter(root, data, args.xlabel, args.ylabel, title)
        root.mainloop()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
MLCalc - Terminal spreadsheet in the VisiCalc tradition
Under 500 lines because spreadsheets shouldn't need millions
Part of the Magic Launcher suite
"""

import json
import csv
import sys
import os
from pathlib import Path

class MLCalc:
    def __init__(self, cols=10, rows=20):
        self.cols = min(26, cols)  # A-Z max
        self.rows = rows
        self.cells = {}  # {"A1": "42", "B1": "=A1*2", ...}
        self.cursor_col = 0
        self.cursor_row = 0
        self.filename = None
        
    def cell_ref(self, col, row):
        """Convert (0,0) to "A1" """
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return f"{chr(ord('A') + col)}{row + 1}"
        return None
        
    def parse_ref(self, ref):
        """Convert "A1" to (0,0)"""
        ref = ref.upper().strip()
        if not ref or len(ref) < 2:
            return None, None
        
        try:
            col = ord(ref[0]) - ord('A')
            row = int(ref[1:]) - 1
            if 0 <= col < self.cols and 0 <= row < self.rows:
                return col, row
        except:
            pass
        return None, None
        
    def get_cell(self, ref):
        """Get raw cell content"""
        return self.cells.get(ref, "")
        
    def set_cell(self, ref, value):
        """Set cell content"""
        if value:
            self.cells[ref] = str(value)
        elif ref in self.cells:
            del self.cells[ref]
            
    def eval_cell(self, ref, visited=None):
        """Evaluate cell formula/value"""
        if visited is None:
            visited = set()
            
        # Circular reference check
        if ref in visited:
            return "#CIRC"
        visited.add(ref)
        
        content = self.get_cell(ref)
        if not content:
            return 0
            
        # Formula
        if content.startswith('='):
            return self.eval_formula(content[1:], visited)
            
        # Number
        try:
            return float(content)
        except:
            # Text
            return content
            
    def eval_formula(self, formula, visited):
        """Evaluate a formula string"""
        formula = formula.upper()
        
        # Handle SUM function
        if formula.startswith('SUM(') and formula.endswith(')'):
            range_str = formula[4:-1]
            return self.eval_sum(range_str, visited)
            
        # Handle AVG function
        if formula.startswith('AVG(') and formula.endswith(')'):
            range_str = formula[4:-1]
            values = self.get_range_values(range_str, visited)
            if values:
                nums = [v for v in values if isinstance(v, (int, float))]
                return sum(nums) / len(nums) if nums else 0
            return 0
            
        # Replace cell references with values
        result = formula
        for col in range(self.cols):
            for row in range(self.rows):
                ref = self.cell_ref(col, row)
                if ref in result:
                    val = self.eval_cell(ref, visited.copy())
                    if isinstance(val, (int, float)):
                        result = result.replace(ref, str(val))
                    else:
                        return "#REF"
                        
        # Evaluate arithmetic expression
        try:
            # Basic safety check - only allow numbers and operators
            allowed = set('0123456789+-*/().')
            if all(c in allowed or c.isspace() for c in result):
                return eval(result)
            return "#ERR"
        except:
            return "#ERR"
            
    def eval_sum(self, range_str, visited):
        """Evaluate SUM(A1:B5) style range"""
        values = self.get_range_values(range_str, visited)
        nums = [v for v in values if isinstance(v, (int, float))]
        return sum(nums)
        
    def get_range_values(self, range_str, visited):
        """Get all values in a range like A1:B5"""
        if ':' in range_str:
            parts = range_str.split(':')
            if len(parts) != 2:
                return []
                
            start_col, start_row = self.parse_ref(parts[0])
            end_col, end_row = self.parse_ref(parts[1])
            
            if None in (start_col, start_row, end_col, end_row):
                return []
                
            values = []
            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
                    ref = self.cell_ref(col, row)
                    values.append(self.eval_cell(ref, visited.copy()))
            return values
        else:
            # Single cell
            ref = range_str.strip()
            return [self.eval_cell(ref, visited.copy())]
            
    def render(self):
        """Display spreadsheet"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Title
        title = f"MLCalc - {self.filename or 'Untitled'}"
        print(f"\033[1;32m{title}\033[0m")
        print("=" * 80)
        
        # Column headers
        print("     ", end="")
        for col in range(self.cols):
            header = chr(ord('A') + col)
            if col == self.cursor_col:
                print(f"\033[1;33m{header:^8}\033[0m", end="")
            else:
                print(f"{header:^8}", end="")
        print()
        print("     " + "-" * (8 * self.cols))
        
        # Rows
        for row in range(self.rows):
            # Row number
            if row == self.cursor_row:
                print(f"\033[1;33m{row+1:3}\033[0m |", end="")
            else:
                print(f"{row+1:3} |", end="")
                
            # Cells
            for col in range(self.cols):
                ref = self.cell_ref(col, row)
                
                # Get display value
                val = self.eval_cell(ref)
                if isinstance(val, float):
                    if val == int(val):
                        display = str(int(val))
                    else:
                        display = f"{val:.2f}"
                else:
                    display = str(val)
                    
                # Truncate to fit
                if len(display) > 7:
                    display = display[:6] + ">"
                    
                # Highlight cursor position
                if col == self.cursor_col and row == self.cursor_row:
                    print(f"\033[1;37;44m{display:7}\033[0m|", end="")
                else:
                    print(f"{display:7}|", end="")
            print()
            
        # Status line
        print("-" * 80)
        current_ref = self.cell_ref(self.cursor_col, self.cursor_row)
        current_content = self.get_cell(current_ref)
        current_value = self.eval_cell(current_ref)
        
        print(f"Cell {current_ref}: {current_content[:40]}")
        if current_content.startswith('='):
            print(f"Value: {current_value}")
            
    def save_file(self, filename=None):
        """Save spreadsheet as JSON"""
        if filename:
            self.filename = filename
        if not self.filename:
            return False
            
        try:
            with open(self.filename, 'w') as f:
                json.dump({
                    'cells': self.cells,
                    'cols': self.cols,
                    'rows': self.rows
                }, f, indent=2)
            return True
        except:
            return False
            
    def load_file(self, filename):
        """Load spreadsheet from JSON"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.cells = data.get('cells', {})
            self.cols = data.get('cols', 10)
            self.rows = data.get('rows', 20)
            self.filename = filename
            return True
        except:
            return False
            
    def export_csv(self, filename):
        """Export to CSV"""
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                for row in range(self.rows):
                    row_data = []
                    for col in range(self.cols):
                        ref = self.cell_ref(col, row)
                        val = self.eval_cell(ref)
                        row_data.append(val if val else "")
                    writer.writerow(row_data)
            return True
        except:
            return False
            
    def import_csv(self, filename):
        """Import from CSV"""
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row_idx, row_data in enumerate(reader):
                    if row_idx >= self.rows:
                        break
                    for col_idx, value in enumerate(row_data):
                        if col_idx >= self.cols:
                            break
                        ref = self.cell_ref(col_idx, row_idx)
                        if value:
                            self.set_cell(ref, value)
            return True
        except:
            return False

def main():
    """Interactive spreadsheet interface"""
    calc = MLCalc()
    
    # Load file from command line if provided
    if len(sys.argv) > 1:
        calc.load_file(sys.argv[1])
    
    while True:
        calc.render()
        
        # Command prompt with clearer navigation
        print("\nCommands: /q)uit /s)ave /l)oad /e)xport /c)sv-import /g)oto")
        print("Navigate: hjkl (vim-style) or wasd | Enter to edit cell")
        cmd = input("> ").strip().lower()
        
        if cmd in ['/q', '/quit']:
            if calc.cells:
                confirm = input("Save before quit? (y/n): ").lower()
                if confirm == 'y':
                    filename = input("Filename: ").strip()
                    if filename:
                        calc.save_file(filename)
            break
            
        elif cmd in ['/s', '/save']:
            filename = input("Save as: ").strip()
            if filename:
                if calc.save_file(filename):
                    print("Saved!")
                else:
                    print("Save failed!")
                input("Press Enter...")
                    
        elif cmd in ['/l', '/load']:
            filename = input("Load file: ").strip()
            if filename:
                if calc.load_file(filename):
                    print("Loaded!")
                else:
                    print("Load failed!")
                input("Press Enter...")
                    
        elif cmd in ['/e', '/export']:
            filename = input("Export to CSV: ").strip()
            if filename:
                if calc.export_csv(filename):
                    print("Exported!")
                else:
                    print("Export failed!")
                input("Press Enter...")
                    
        elif cmd in ['/c', '/csv']:
            filename = input("Import CSV: ").strip()
            if filename:
                if calc.import_csv(filename):
                    print("Imported!")
                else:
                    print("Import failed!")
                input("Press Enter...")
                    
        elif cmd in ['/g', '/goto']:
            ref = input("Go to cell: ").strip().upper()
            col, row = calc.parse_ref(ref)
            if col is not None and row is not None:
                calc.cursor_col = col
                calc.cursor_row = row
                
        # Vim-style navigation
        elif cmd == 'k':  # Up
            calc.cursor_row = max(0, calc.cursor_row - 1)
        elif cmd == 'j':  # Down
            calc.cursor_row = min(calc.rows - 1, calc.cursor_row + 1)
        elif cmd == 'h':  # Left
            calc.cursor_col = max(0, calc.cursor_col - 1)
        elif cmd == 'l':  # Right
            calc.cursor_col = min(calc.cols - 1, calc.cursor_col + 1)
            
        # WASD navigation as backup
        elif cmd == 'w':  # Up
            calc.cursor_row = max(0, calc.cursor_row - 1)
        elif cmd == 's':  # Down
            calc.cursor_row = min(calc.rows - 1, calc.cursor_row + 1)
        elif cmd == 'a':  # Left
            calc.cursor_col = max(0, calc.cursor_col - 1)
        elif cmd == 'd':  # Right
            calc.cursor_col = min(calc.cols - 1, calc.cursor_col + 1)
            
        elif cmd == '':
            # Edit current cell
            ref = calc.cell_ref(calc.cursor_col, calc.cursor_row)
            current = calc.get_cell(ref)
            print(f"\nEditing {ref}: {current}")
            new_value = input("New value (empty to clear): ").strip()
            calc.set_cell(ref, new_value)
            
        elif cmd.startswith('='):
            # Direct formula entry
            ref = calc.cell_ref(calc.cursor_col, calc.cursor_row)
            calc.set_cell(ref, cmd)

if __name__ == "__main__":
    print("""
MLCalc - Terminal Spreadsheet
=============================
A VisiCalc-style spreadsheet in under 500 lines

Features:
- Cell formulas: =A1+B2*2
- Functions: =SUM(A1:A10), =AVG(B1:B5)  
- Arrow/WASD navigation
- JSON save/load
- CSV import/export

Starting...
""")
    input("Press Enter to begin...")
    main()

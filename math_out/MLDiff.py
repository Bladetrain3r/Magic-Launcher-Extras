#!/usr/bin/env python3
"""
MLDiff - Semantic data diff that actually tells you what changed
Part of ML-Extras

Purpose primitive: Show what ACTUALLY changed in data, not just line differences

Usage:
    mldiff old.csv new.csv              # Compare two CSV files
    mldiff old.json new.json --json      # Compare JSON files  
    mldiff before.txt after.txt --text   # Fall back to smart text diff
    
Shows:
    - Rows added/removed/modified
    - Columns added/removed
    - Statistical changes (mean, min, max shifted)
    - Not just "line 47 changed" but "Customer ID 50432 amount changed 100->150"
"""

import sys
import csv
import json
from pathlib import Path
from collections import defaultdict

class MLDiff:
    def __init__(self):
        self.changes = {
            'rows_added': [],
            'rows_removed': [],
            'rows_modified': [],
            'cols_added': [],
            'cols_removed': [],
            'stats': {}
        }
    
    def diff_csv(self, file1, file2, key_col=0):
        """Compare two CSV files semantically"""
        # Load both files
        data1 = self._load_csv(file1)
        data2 = self._load_csv(file2)
        
        if not data1 or not data2:
            return "Error loading files"
        
        # Check headers
        headers1 = data1[0] if data1 else []
        headers2 = data2[0] if data2 else []
        
        # Detect if first row is header
        has_header = False
        try:
            float(headers1[0])
        except (ValueError, IndexError):
            has_header = True
        
        if has_header:
            # Column changes
            self.changes['cols_added'] = [h for h in headers2 if h not in headers1]
            self.changes['cols_removed'] = [h for h in headers1 if h not in headers2]
            
            # Skip headers for data comparison
            data1 = data1[1:]
            data2 = data2[1:]
        
        # Build lookup by key column
        lookup1 = {}
        lookup2 = {}
        
        for row in data1:
            if len(row) > key_col:
                key = row[key_col]
                lookup1[key] = row
        
        for row in data2:
            if len(row) > key_col:
                key = row[key_col]
                lookup2[key] = row
        
        # Find changes
        all_keys = set(lookup1.keys()) | set(lookup2.keys())
        
        for key in all_keys:
            if key in lookup1 and key not in lookup2:
                self.changes['rows_removed'].append((key, lookup1[key]))
            elif key not in lookup1 and key in lookup2:
                self.changes['rows_added'].append((key, lookup2[key]))
            elif key in lookup1 and key in lookup2:
                # Check if modified
                if lookup1[key] != lookup2[key]:
                    old_row = lookup1[key]
                    new_row = lookup2[key]
                    
                    # Find what changed
                    changes = []
                    for i, (old, new) in enumerate(zip(old_row, new_row)):
                        if old != new:
                            col_name = headers1[i] if has_header and i < len(headers1) else f"col_{i}"
                            changes.append((col_name, old, new))
                    
                    if changes:
                        self.changes['rows_modified'].append((key, changes))
        
        # Calculate statistics for numeric columns
        self._calculate_stats(data1, data2, headers1 if has_header else None)
        
        return self._format_output()
    
    def diff_json(self, file1, file2):
        """Compare two JSON files"""
        try:
            with open(file1, 'r') as f:
                data1 = json.load(f)
            with open(file2, 'r') as f:
                data2 = json.load(f)
        except Exception as e:
            return f"Error loading JSON: {e}"
        
        # Recursive diff for nested structures
        changes = self._diff_dict(data1, data2)
        return self._format_json_changes(changes)
    
    def _diff_dict(self, d1, d2, path=""):
        """Recursively diff two dictionaries"""
        changes = {
            'added': {},
            'removed': {},
            'modified': {}
        }
        
        if not isinstance(d1, dict) or not isinstance(d2, dict):
            if d1 != d2:
                return {'value_changed': {'old': d1, 'new': d2}}
            return {}
        
        # Keys analysis
        keys1 = set(d1.keys())
        keys2 = set(d2.keys())
        
        # Added keys
        for key in keys2 - keys1:
            changes['added'][key] = d2[key]
        
        # Removed keys
        for key in keys1 - keys2:
            changes['removed'][key] = d1[key]
        
        # Common keys - check for modifications
        for key in keys1 & keys2:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                nested = self._diff_dict(d1[key], d2[key], f"{path}.{key}")
                if nested:
                    changes['modified'][key] = nested
            elif d1[key] != d2[key]:
                changes['modified'][key] = {
                    'old': d1[key],
                    'new': d2[key]
                }
        
        # Clean empty categories
        return {k: v for k, v in changes.items() if v}
    
    def diff_text(self, file1, file2):
        """Smart text diff that groups changes"""
        with open(file1, 'r') as f:
            lines1 = f.readlines()
        with open(file2, 'r') as f:
            lines2 = f.readlines()
        
        # Find changed sections, not just lines
        changes = []
        i = j = 0
        
        while i < len(lines1) or j < len(lines2):
            # Skip matching lines
            while i < len(lines1) and j < len(lines2) and lines1[i] == lines2[j]:
                i += 1
                j += 1
            
            if i >= len(lines1) and j >= len(lines2):
                break
            
            # Find extent of change
            start_i, start_j = i, j
            
            # Find next matching line
            found = False
            for look_ahead in range(1, 10):  # Look ahead up to 10 lines
                for di in range(look_ahead + 1):
                    dj = look_ahead - di
                    if (i + di < len(lines1) and j + dj < len(lines2) and 
                        lines1[i + di] == lines2[j + dj]):
                        i += di
                        j += dj
                        found = True
                        break
                if found:
                    break
            
            if not found:
                i = len(lines1)
                j = len(lines2)
            
            # Record change
            changes.append({
                'line_range': (start_i + 1, i + 1),
                'removed': lines1[start_i:i],
                'added': lines2[start_j:j]
            })
        
        return self._format_text_changes(changes)
    
    def _load_csv(self, filename):
        """Load CSV file"""
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                return list(reader)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def _calculate_stats(self, data1, data2, headers):
        """Calculate statistical changes for numeric columns"""
        # Find numeric columns
        numeric_cols = []
        
        for col_idx in range(min(len(data1[0]) if data1 else 0, 
                                len(data2[0]) if data2 else 0)):
            # Check if column is numeric
            is_numeric = True
            for row in data1[:10] + data2[:10]:  # Sample first 10 rows
                if col_idx < len(row):
                    try:
                        float(row[col_idx])
                    except (ValueError, IndexError):
                        is_numeric = False
                        break
            
            if is_numeric:
                numeric_cols.append(col_idx)
        
        # Calculate stats for each numeric column
        for col_idx in numeric_cols:
            col_name = headers[col_idx] if headers and col_idx < len(headers) else f"col_{col_idx}"
            
            values1 = []
            values2 = []
            
            for row in data1:
                if col_idx < len(row):
                    try:
                        values1.append(float(row[col_idx]))
                    except ValueError:
                        pass
            
            for row in data2:
                if col_idx < len(row):
                    try:
                        values2.append(float(row[col_idx]))
                    except ValueError:
                        pass
            
            if values1 and values2:
                stats = {
                    'old_mean': sum(values1) / len(values1),
                    'new_mean': sum(values2) / len(values2),
                    'old_min': min(values1),
                    'new_min': min(values2),
                    'old_max': max(values1),
                    'new_max': max(values2),
                    'old_count': len(values1),
                    'new_count': len(values2)
                }
                
                # Only record if there are changes
                if (abs(stats['old_mean'] - stats['new_mean']) > 0.01 or
                    stats['old_min'] != stats['new_min'] or
                    stats['old_max'] != stats['new_max'] or
                    stats['old_count'] != stats['new_count']):
                    self.changes['stats'][col_name] = stats
    
    def _format_output(self):
        """Format the diff output for display"""
        output = []
        output.append("=" * 60)
        output.append("DATA DIFF SUMMARY")
        output.append("=" * 60)
        
        # Summary
        output.append(f"Rows added:    {len(self.changes['rows_added'])}")
        output.append(f"Rows removed:  {len(self.changes['rows_removed'])}")
        output.append(f"Rows modified: {len(self.changes['rows_modified'])}")
        
        if self.changes['cols_added'] or self.changes['cols_removed']:
            output.append("")
            if self.changes['cols_added']:
                output.append(f"Columns added: {', '.join(self.changes['cols_added'])}")
            if self.changes['cols_removed']:
                output.append(f"Columns removed: {', '.join(self.changes['cols_removed'])}")
        
        # Show sample changes
        if self.changes['rows_added']:
            output.append("\n--- SAMPLE ROWS ADDED (first 5) ---")
            for key, row in self.changes['rows_added'][:5]:
                output.append(f"  + [{key}]: {row[:5]}...")  # Show first 5 fields
        
        if self.changes['rows_removed']:
            output.append("\n--- SAMPLE ROWS REMOVED (first 5) ---")
            for key, row in self.changes['rows_removed'][:5]:
                output.append(f"  - [{key}]: {row[:5]}...")
        
        if self.changes['rows_modified']:
            output.append("\n--- SAMPLE MODIFICATIONS (first 10) ---")
            for key, changes in self.changes['rows_modified'][:10]:
                output.append(f"  ~ [{key}]:")
                for col, old, new in changes[:3]:  # Show first 3 field changes
                    output.append(f"      {col}: '{old}' -> '{new}'")
        
        # Statistical changes
        if self.changes['stats']:
            output.append("\n--- STATISTICAL CHANGES ---")
            for col, stats in self.changes['stats'].items():
                output.append(f"\n  {col}:")
                mean_change = stats['new_mean'] - stats['old_mean']
                output.append(f"    Mean:  {stats['old_mean']:.2f} -> {stats['new_mean']:.2f} ({mean_change:+.2f})")
                output.append(f"    Range: [{stats['old_min']:.2f}, {stats['old_max']:.2f}] -> [{stats['new_min']:.2f}, {stats['new_max']:.2f}]")
                output.append(f"    Count: {stats['old_count']} -> {stats['new_count']}")
        
        output.append("\n" + "=" * 60)
        
        return '\n'.join(output)
    
    def _format_json_changes(self, changes):
        """Format JSON diff output"""
        output = []
        output.append("=" * 60)
        output.append("JSON DIFF")
        output.append("=" * 60)
        
        def format_path(path, changes, indent=0):
            prefix = "  " * indent
            
            if 'added' in changes:
                for key, value in changes['added'].items():
                    output.append(f"{prefix}+ {key}: {json.dumps(value, indent=2)[:100]}")
            
            if 'removed' in changes:
                for key, value in changes['removed'].items():
                    output.append(f"{prefix}- {key}: {json.dumps(value, indent=2)[:100]}")
            
            if 'modified' in changes:
                for key, value in changes['modified'].items():
                    if 'old' in value and 'new' in value:
                        output.append(f"{prefix}~ {key}: {value['old']} -> {value['new']}")
                    else:
                        output.append(f"{prefix}~ {key}:")
                        format_path(f"{path}.{key}", value, indent + 1)
            
            if 'value_changed' in changes:
                output.append(f"{prefix}~ {changes['value_changed']['old']} -> {changes['value_changed']['new']}")
        
        format_path("", changes)
        
        output.append("=" * 60)
        return '\n'.join(output)
    
    def _format_text_changes(self, changes):
        """Format text diff output"""
        output = []
        output.append("=" * 60)
        output.append(f"TEXT DIFF - {len(changes)} change sections")
        output.append("=" * 60)
        
        for i, change in enumerate(changes, 1):
            output.append(f"\n--- Section {i} (lines {change['line_range'][0]}-{change['line_range'][1]}) ---")
            
            if change['removed']:
                output.append("Removed:")
                for line in change['removed'][:5]:  # Show first 5 lines
                    output.append(f"  - {line.rstrip()}")
                if len(change['removed']) > 5:
                    output.append(f"  ... and {len(change['removed']) - 5} more lines")
            
            if change['added']:
                output.append("Added:")
                for line in change['added'][:5]:
                    output.append(f"  + {line.rstrip()}")
                if len(change['added']) > 5:
                    output.append(f"  ... and {len(change['added']) - 5} more lines")
        
        output.append("\n" + "=" * 60)
        return '\n'.join(output)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Semantic data diff")
    parser.add_argument('file1', help='First file')
    parser.add_argument('file2', help='Second file')
    parser.add_argument('--json', action='store_true', help='Compare as JSON')
    parser.add_argument('--text', action='store_true', help='Compare as text')
    parser.add_argument('--key', type=int, default=0, 
                       help='Key column for CSV comparison (default: 0)')
    parser.add_argument('--verbose', action='store_true', 
                       help='Show all changes, not just samples')
    
    args = parser.parse_args()
    
    # Check files exist
    if not Path(args.file1).exists():
        print(f"Error: {args.file1} not found")
        sys.exit(1)
    if not Path(args.file2).exists():
        print(f"Error: {args.file2} not found")
        sys.exit(1)
    
    differ = MLDiff()
    
    # Detect format from extension if not specified
    ext1 = Path(args.file1).suffix.lower()
    ext2 = Path(args.file2).suffix.lower()
    
    if args.json or (ext1 == '.json' and ext2 == '.json'):
        result = differ.diff_json(args.file1, args.file2)
    elif args.text or (ext1 == '.txt' and ext2 == '.txt'):
        result = differ.diff_text(args.file1, args.file2)
    else:
        # Default to CSV
        result = differ.diff_csv(args.file1, args.file2, args.key)
    
    print(result)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
MLKVxtract - Universal Pattern Learning and Extraction
Because patterns are data, not code.
This technically works but is practically useless.
A hydra of fragile string operations.
Slay the hydra by breaking it small, not by trying to do it all.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from difflib import SequenceMatcher
from collections import OrderedDict

class MLKVxtract:
    """
    Learn patterns from examples, extract data without hardcoding
    This is how we teach machines to see patterns like humans do
    """
    
    def __init__(self):
        self.patterns = {}
        self.debug = False
        
    def learn_pattern(self, example_input: str, example_output: Dict) -> Dict:
        """
        The core magic: Learn HOW input maps to output
        
        This is the breakthrough - we're teaching the computer
        to recognize patterns by example, not by rules
        """
        # Try increasingly complex strategies
        pattern = None
        strategies = [
            ("delimiter", self.learn_delimiter_pattern),
            ("positional", self.learn_positional_pattern),
            ("template", self.learn_template_pattern),
            ("regex", self.learn_regex_pattern),
            ("structural", self.learn_structural_pattern),
            ("semantic", self.learn_semantic_pattern)
        ]
        
        for name, strategy in strategies:
            if self.debug:
                print(f"Trying {name} strategy...")
            
            pattern = strategy(example_input, example_output)
            if pattern:
                # Validate the pattern works
                extracted = self.extract(example_input, pattern)
                if self.matches_output(extracted, example_output):
                    pattern["strategy"] = name
                    pattern["confidence"] = self.calculate_confidence(
                        extracted, example_output
                    )
                    if self.debug:
                        print(f"Success with {name}! Confidence: {pattern['confidence']}")
                    return pattern
        
        # If nothing works, create a memorization pattern
        return self.create_memorization_pattern(example_input, example_output)
    
    def learn_delimiter_pattern(self, text: str, expected: Dict) -> Optional[Dict]:
        """Learn patterns like 'key:value, key:value' or 'key=value;key=value'"""
        
        # Common delimiters to try
        key_value_delims = [':', '=', '->', '=>', '|', '\t']
        pair_separators = [',', ';', '\n', '|', '&', ' ']
        
        # Try each combination
        for kv_delim in key_value_delims:
            if kv_delim not in text:
                continue
                
            for pair_sep in pair_separators:
                try:
                    # Attempt to parse with these delimiters
                    pairs = text.split(pair_sep) if pair_sep != '\n' else text.splitlines()
                    result = {}
                    
                    for pair in pairs:
                        if kv_delim in pair:
                            parts = pair.split(kv_delim, 1)
                            if len(parts) == 2:
                                key = parts[0].strip().lower().replace(' ', '_')
                                value = parts[1].strip()
                                result[key] = value
                    
                    # Check if this matches our expected output
                    if self.matches_output(result, expected):
                        return {
                            "type": "delimiter",
                            "key_value_delimiter": kv_delim,
                            "pair_separator": pair_sep,
                            "lowercase_keys": True,
                            "strip_whitespace": True
                        }
                except:
                    continue
        
        return None
    
    def learn_positional_pattern(self, text: str, expected: Dict) -> Optional[Dict]:
        """Learn patterns based on position (line number, word index, etc)"""
        
        lines = text.splitlines()
        words = text.split()
        
        # Try line-based positions
        line_positions = {}
        for key, value in expected.items():
            for i, line in enumerate(lines):
                if str(value) in line:
                    line_positions[key] = {
                        "line": i,
                        "method": "full_line" if line.strip() == str(value) else "contains"
                    }
                    break
        
        if len(line_positions) == len(expected):
            return {
                "type": "positional",
                "method": "line",
                "positions": line_positions
            }
        
        # Try word-based positions
        word_positions = {}
        for key, value in expected.items():
            try:
                idx = words.index(str(value))
                word_positions[key] = idx
            except ValueError:
                # Multi-word value?
                value_words = str(value).split()
                for i in range(len(words) - len(value_words) + 1):
                    if words[i:i+len(value_words)] == value_words:
                        word_positions[key] = (i, i+len(value_words))
                        break
        
        if len(word_positions) == len(expected):
            return {
                "type": "positional",
                "method": "word",
                "positions": word_positions
            }
        
        return None
    
    def learn_template_pattern(self, text: str, expected: Dict) -> Optional[Dict]:
        """Learn patterns like 'The {subject} is {object}' """
        
        # Build a template by replacing values with placeholders
        template = text
        value_to_key = {}
        
        # Sort by length to replace longer values first
        for key, value in sorted(expected.items(), key=lambda x: -len(str(x[1]))):
            if str(value) in template:
                placeholder = f"{{{key}}}"
                template = template.replace(str(value), placeholder)
                value_to_key[str(value)] = key
        
        # Check if we can reconstruct the original
        test_result = template
        for key, value in expected.items():
            test_result = test_result.replace(f"{{{key}}}", str(value))
        
        if test_result == text:
            # Extract the pattern structure
            pattern_regex = re.escape(template)
            for key in expected.keys():
                pattern_regex = pattern_regex.replace(
                    re.escape(f"{{{key}}}"),
                    f"(?P<{key}>.*?)"
                )
            
            return {
                "type": "template",
                "template": template,
                "regex": pattern_regex,
                "keys": list(expected.keys())
            }
        
        return None
    
    def learn_regex_pattern(self, text: str, expected: Dict) -> Optional[Dict]:
        """Learn common regex patterns"""
        
        # Common patterns to try
        patterns = {
            "error_log": r"(?P<level>\w+):\s*(?P<message>.*?)(?:\s+at\s+(?P<location>.*))?$",
            "key_value": r"(?P<key>\w+)\s*[:=]\s*(?P<value>.*)",
            "function_call": r"(?P<function>\w+)\((?P<args>.*?)\)",
            "path": r"(?P<dir>.*?)/(?P<file>[^/]+)$",
            "email": r"(?P<user>[\w.-]+)@(?P<domain>[\w.-]+)",
            "url": r"(?P<protocol>https?)://(?P<host>[^/]+)(?P<path>/.*)?",
            "timestamp": r"(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})",
        }
        
        for name, pattern in patterns.items():
            try:
                match = re.match(pattern, text)
                if match:
                    result = match.groupdict()
                    if self.matches_output(result, expected):
                        return {
                            "type": "regex",
                            "pattern": pattern,
                            "name": name
                        }
            except:
                continue
        
        # Try to build a custom regex
        custom_pattern = self.build_custom_regex(text, expected)
        if custom_pattern:
            return {
                "type": "regex",
                "pattern": custom_pattern,
                "name": "custom"
            }
        
        return None
    
    def learn_structural_pattern(self, text: str, expected: Dict) -> Optional[Dict]:
        """Learn patterns based on structure (JSON, XML, etc)"""
        
        # Try JSON
        try:
            parsed = json.loads(text)
            if self.matches_output(parsed, expected):
                return {
                    "type": "structural",
                    "format": "json"
                }
        except:
            pass
        
        # Try key-value with indentation (like YAML)
        if '\n' in text and any(line.startswith(' ') or line.startswith('\t') for line in text.splitlines()):
            # Detect indentation-based structure
            lines = text.splitlines()
            stack = [{}]
            current_indent = 0
            
            for line in lines:
                if not line.strip():
                    continue
                    
                indent = len(line) - len(line.lstrip())
                content = line.strip()
                
                if ':' in content:
                    key, value = content.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if indent > current_indent:
                        # Nested structure
                        if key not in stack[-1]:
                            stack[-1][key] = {}
                        stack.append(stack[-1][key])
                        current_indent = indent
                    elif indent < current_indent:
                        # Back up
                        stack.pop()
                        current_indent = indent
                    
                    stack[-1][key] = value if value else {}
            
            if self.matches_output(stack[0], expected):
                return {
                    "type": "structural",
                    "format": "indented",
                    "indent_char": ' ' if ' ' in text else '\t'
                }
        
        return None
    
    def learn_semantic_pattern(self, text: str, expected: Dict) -> Optional[Dict]:
        """Learn patterns based on meaning and context"""
        
        # This is where it gets interesting - NLP-style patterns
        # For now, implement simple semantic patterns
        
        # Pattern: "X is Y" -> {"subject": X, "predicate": Y}
        is_patterns = [
            r"(?P<subject>\w+)\s+is\s+(?P<predicate>.*)",
            r"(?P<subject>\w+)\s+are\s+(?P<predicate>.*)",
            r"The\s+(?P<subject>\w+)\s+is\s+(?P<predicate>.*)",
        ]
        
        for pattern in is_patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                result = match.groupdict()
                if self.matches_output(result, expected):
                    return {
                        "type": "semantic",
                        "pattern": pattern,
                        "style": "is_statement"
                    }
        
        # Pattern: MLBard style "X doth Y and Z"
        doth_pattern = r"(?P<subject>\w+)\s+doth\s+(?P<action>\w+)(?:\s+and\s+(?P<secondary>\w+))?"
        match = re.match(doth_pattern, text, re.IGNORECASE)
        if match:
            result = {k: v for k, v in match.groupdict().items() if v}
            if self.matches_output(result, expected):
                return {
                    "type": "semantic",
                    "pattern": doth_pattern,
                    "style": "mlbard"
                }
        
        return None
    
    def extract(self, text: str, pattern: Dict) -> Dict:
        """Extract data using a learned pattern"""
        
        if pattern["type"] == "delimiter":
            return self.extract_delimiter(text, pattern)
        elif pattern["type"] == "positional":
            return self.extract_positional(text, pattern)
        elif pattern["type"] == "template":
            return self.extract_template(text, pattern)
        elif pattern["type"] == "regex":
            return self.extract_regex(text, pattern)
        elif pattern["type"] == "structural":
            return self.extract_structural(text, pattern)
        elif pattern["type"] == "semantic":
            return self.extract_semantic(text, pattern)
        elif pattern["type"] == "memorization":
            # Just return what we memorized
            return pattern.get("memorized", {})
        else:
            return {}
    
    def extract_delimiter(self, text: str, pattern: Dict) -> Dict:
        """Extract using delimiter pattern"""
        kv_delim = pattern["key_value_delimiter"]
        pair_sep = pattern["pair_separator"]
        
        pairs = text.split(pair_sep) if pair_sep != '\n' else text.splitlines()
        result = {}
        
        for pair in pairs:
            if kv_delim in pair:
                parts = pair.split(kv_delim, 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    if pattern.get("lowercase_keys"):
                        key = key.lower().replace(' ', '_')
                    value = parts[1].strip() if pattern.get("strip_whitespace") else parts[1]
                    result[key] = value
        
        return result
    
    def extract_positional(self, text: str, pattern: Dict) -> Dict:
        """Extract using positional pattern"""
        result = {}
        
        if pattern["method"] == "line":
            lines = text.splitlines()
            for key, pos_info in pattern["positions"].items():
                line_idx = pos_info["line"]
                if line_idx < len(lines):
                    if pos_info["method"] == "full_line":
                        result[key] = lines[line_idx].strip()
                    else:
                        result[key] = lines[line_idx]
        
        elif pattern["method"] == "word":
            words = text.split()
            for key, pos in pattern["positions"].items():
                if isinstance(pos, tuple):
                    start, end = pos
                    result[key] = ' '.join(words[start:end])
                else:
                    if pos < len(words):
                        result[key] = words[pos]
        
        return result
    
    def extract_template(self, text: str, pattern: Dict) -> Dict:
        """Extract using template pattern"""
        regex = pattern["regex"]
        match = re.match(regex, text)
        
        if match:
            return match.groupdict()
        return {}
    
    def extract_regex(self, text: str, pattern: Dict) -> Dict:
        """Extract using regex pattern"""
        regex = pattern["pattern"]
        match = re.match(regex, text)
        
        if match:
            return match.groupdict()
        return {}
    
    def extract_structural(self, text: str, pattern: Dict) -> Dict:
        """Extract using structural pattern"""
        if pattern["format"] == "json":
            try:
                return json.loads(text)
            except:
                return {}
        
        # Add other structural formats as needed
        return {}
    
    def extract_semantic(self, text: str, pattern: Dict) -> Dict:
        """Extract using semantic pattern"""
        regex = pattern["pattern"]
        match = re.match(regex, text, re.IGNORECASE)
        
        if match:
            return {k: v for k, v in match.groupdict().items() if v}
        return {}
    
    def matches_output(self, extracted: Dict, expected: Dict) -> bool:
        """Check if extracted data matches expected output"""
        if not extracted:
            return False
            
        # Flexible matching - allow for case differences, extra whitespace, etc
        for key, expected_value in expected.items():
            if key not in extracted:
                # Try case-insensitive match
                key_lower = key.lower()
                found = False
                for k in extracted:
                    if k.lower() == key_lower:
                        found = True
                        if not self.values_match(extracted[k], expected_value):
                            return False
                        break
                if not found:
                    return False
            else:
                if not self.values_match(extracted[key], expected_value):
                    return False
        
        return True
    
    def values_match(self, extracted, expected) -> bool:
        """Flexible value matching"""
        # Convert to strings for comparison
        extracted_str = str(extracted).strip().lower()
        expected_str = str(expected).strip().lower()
        
        # Exact match
        if extracted_str == expected_str:
            return True
        
        # Close enough (85% similarity)
        similarity = SequenceMatcher(None, extracted_str, expected_str).ratio()
        return similarity > 0.85
    
    def calculate_confidence(self, extracted: Dict, expected: Dict) -> float:
        """Calculate confidence score for the extraction"""
        if not extracted:
            return 0.0
        
        matches = 0
        total = len(expected)
        
        for key, expected_value in expected.items():
            if key in extracted:
                if self.values_match(extracted[key], expected_value):
                    matches += 1
        
        return matches / total if total > 0 else 0.0
    
    def build_custom_regex(self, text: str, expected: Dict) -> Optional[str]:
        """Try to build a custom regex pattern"""
        # This is where we get creative
        # For now, simple implementation
        
        # Try to identify the pattern by looking at what's between values
        values = list(expected.values())
        if all(str(v) in text for v in values):
            # All values are present
            pattern = re.escape(text)
            for key, value in expected.items():
                escaped_value = re.escape(str(value))
                pattern = pattern.replace(escaped_value, f"(?P<{key}>.*?)", 1)
            
            # Test the pattern
            try:
                match = re.match(pattern, text)
                if match and match.groupdict() == expected:
                    return pattern
            except:
                pass
        
        return None
    
    def create_memorization_pattern(self, text: str, output: Dict) -> Dict:
        """Last resort - just memorize the example"""
        return {
            "type": "memorization",
            "input": text,
            "memorized": output,
            "confidence": 1.0 if text else 0.0
        }
    
    def save_pattern(self, pattern: Dict, name: str):
        """Save a pattern to file"""
        path = Path(f"{name}.pattern.json")
        with open(path, 'w') as f:
            json.dump(pattern, f, indent=2)
        return path
    
    def load_pattern(self, name: str) -> Dict:
        """Load a pattern from file"""
        path = Path(f"{name}.pattern.json")
        if not path.exists():
            path = Path(name)  # Try direct path
        
        with open(path, 'r') as f:
            return json.load(f)
    
    def train_on_examples(self, examples: List[Tuple[str, Dict]]) -> Dict:
        """Train on multiple examples to find the best pattern"""
        
        best_pattern = None
        best_score = 0
        
        for input_text, output_dict in examples:
            pattern = self.learn_pattern(input_text, output_dict)
            
            # Test this pattern on all examples
            score = 0
            for test_input, test_output in examples:
                extracted = self.extract(test_input, pattern)
                if self.matches_output(extracted, test_output):
                    score += 1
            
            if score > best_score:
                best_score = score
                best_pattern = pattern
        
        if best_pattern:
            best_pattern["trained_on"] = len(examples)
            best_pattern["accuracy"] = best_score / len(examples)
        
        return best_pattern


def main():
    """CLI interface for MLKVxtract"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MLKVxtract - Learn patterns and extract data"
    )
    
    parser.add_argument('input', nargs='?', help='Input text or file')
    parser.add_argument('-l', '--learn', action='store_true',
                       help='Learn a pattern from example')
    parser.add_argument('-e', '--expected', help='Expected output (JSON)')
    parser.add_argument('-p', '--pattern', help='Pattern file to use')
    parser.add_argument('-s', '--save', help='Save learned pattern as')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-d', '--debug', action='store_true',
                       help='Debug mode')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode')
    parser.add_argument('-t', '--train', help='Training examples file (JSON)')
    
    args = parser.parse_args()
    
    extractor = MLKVxtract()
    extractor.debug = args.debug
    
    if args.interactive:
        print("MLKVxtract Interactive Mode")
        print("-" * 40)
        
        while True:
            try:
                print("\nExample input (or 'quit'):")
                input_text = input("> ")
                if input_text.lower() in ['quit', 'exit', 'q']:
                    break
                
                print("\nExpected output (JSON):")
                output_text = input("> ")
                
                try:
                    expected = json.loads(output_text)
                except:
                    print("Invalid JSON, trying as key=value pairs")
                    # Try to parse as simple key=value
                    expected = {}
                    for pair in output_text.split(','):
                        if '=' in pair:
                            k, v = pair.split('=', 1)
                            expected[k.strip()] = v.strip()
                
                pattern = extractor.learn_pattern(input_text, expected)
                print(f"\nLearned pattern: {pattern['strategy']}")
                print(f"Confidence: {pattern.get('confidence', 'N/A')}")
                
                # Test it
                print("\nTest the pattern (or press Enter to skip):")
                test_input = input("> ")
                if test_input:
                    result = extractor.extract(test_input, pattern)
                    print(f"Extracted: {json.dumps(result, indent=2)}")
                
                print("\nSave pattern as (or press Enter to skip):")
                save_name = input("> ")
                if save_name:
                    path = extractor.save_pattern(pattern, save_name)
                    print(f"Saved to {path}")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    elif args.train:
        # Load training examples
        with open(args.train, 'r') as f:
            examples = json.load(f)
        
        # Convert to tuples
        training_data = [(ex["input"], ex["output"]) for ex in examples]
        
        # Train
        pattern = extractor.train_on_examples(training_data)
        print(f"Trained pattern: {pattern['strategy']}")
        print(f"Accuracy: {pattern.get('accuracy', 'N/A')}")
        
        if args.save:
            path = extractor.save_pattern(pattern, args.save)
            print(f"Saved to {path}")
    
    elif args.learn:
        # Learn mode
        if not args.input or not args.expected:
            print("Error: --learn requires input and --expected")
            sys.exit(1)
        
        # Read input
        if Path(args.input).exists():
            with open(args.input, 'r') as f:
                input_text = f.read()
        else:
            input_text = args.input
        
        # Parse expected output
        try:
            expected = json.loads(args.expected)
        except:
            # Try to read as file
            if Path(args.expected).exists():
                with open(args.expected, 'r') as f:
                    expected = json.load(f)
            else:
                print("Error: Invalid expected output")
                sys.exit(1)
        
        # Learn pattern
        pattern = extractor.learn_pattern(input_text, expected)
        print(f"Learned pattern: {pattern['strategy']}")
        print(f"Confidence: {pattern.get('confidence', 'N/A')}")
        
        if args.save:
            path = extractor.save_pattern(pattern, args.save)
            print(f"Saved to {path}")
    
    elif args.pattern:
        # Extract mode
        pattern = extractor.load_pattern(args.pattern)
        
        # Read input
        if args.input:
            if Path(args.input).exists():
                with open(args.input, 'r') as f:
                    input_text = f.read()
            else:
                input_text = args.input
        else:
            input_text = sys.stdin.read()
        
        # Extract
        result = extractor.extract(input_text, pattern)
        
        # Output
        output = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
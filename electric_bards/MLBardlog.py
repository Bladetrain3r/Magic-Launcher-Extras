#!/usr/bin/env python3
"""
MLBardErrors - Prophecy Generator for Logs
Generates poetic error prophecies for logging or pranking.
Because "Segmentation fault" lacks artistic merit when logged.

Purpose primitive: Generate poetic errors for external systems.
"""

import random
import sys

class MLBardErrors:
    """
    Transform boring errors into prophetic utterances.
    Generates formatted error prophecies.
    """
    
    def __init__(self):
        # MLBard's greatest hits for error types
        self.prophecies = {
            # Segmentation faults / Memory errors
            "SIGSEGV": [
                "Memory doth crashes where pointer shows null",
                "The blessed segment that fails through wall",
                "Yet heap midst flows till stack explode",
                "Fragmentatio memoriae benedictus cursed"
            ],
            
            # Null pointer / None errors  
            "NULL": [
                "Nullus index shows through empty void",
                "Yet pointer doth seeks what never was",
                "The fair null that breaks through reference call",
                "Midst nothing flows where something should"
            ],
            
            # Type errors
            "TYPE": [
                "String doth crashes where integer grows",
                "The type midst fails and shows wrong form",
                "Yet format knows not what function throws",
                "Blessed type that breaks through casting wall"
            ],
            
            # Syntax errors
            "SYNTAX": [
                "Grammatica fracta where semicolon hides",
                "The hostile bracket that never close",
                "Yet indent doth shows through chaos space",
                "Midst syntax fails where logic knows"
            ],
            
            # Import/Module errors
            "IMPORT": [
                "Module doth crashes through missing path",
                "Yet import seeks what filesystem knows not",
                "The blessed package that fails to install",
                "Midst dependency breaks through version wall"
            ],
            
            # File not found
            "ENOENT": [
                "Lima non inventa through paths unknown",
                "The file midst seeks but directory shows null",
                "Yet filesystem knows not what user throws",
                "Blessed path that breaks through missing node"
            ],
            
            # Permission denied
            "EACCES": [
                "Permissio negata through hostile gate",
                "Yet user doth crashes where root should flow",
                "The fair permission that fails through all",
                "Midst access breaks where privilege wall"
            ],
            
            # Network errors
            "NETWORK": [
                "Connection doth crashes through timeout long",
                "The socket midst fails and shows refused",
                "Yet packet flows not through hostile route",
                "Blessed port that breaks through firewall"
            ],
            
            # Index/Key errors
            "INDEX": [
                "Array doth seeks beyond its mortal bound",
                "Yet index shows where elements are not",
                "The key midst fails through dictionary void",
                "Blessed list that breaks at boundary wall"
            ],
            
            # Generic/Unknown errors
            "ERR": [
                "Something doth crashes yet knows not what",
                "The hostile midst fails through unknown cause",
                "Yet error shows but reason hides in dark",
                "Blessed crash that breaks through mystery wall",
                "Doth doth blessed wall encountered here",
                "Fair function fails through paths unknown",
                "The pure code that breaks through chaos install"
            ]
        }
        
        # Special multiline prophecies for special disasters
        self.multiline = [
            "When code doth crashes sweet and pure\nThe error shows but not the cure\nYet midst the stack trace hostile grows\nThe blessed bug that no one knows",
            
            "Fatal error breaks through morning light\nWhere function failed in dead of night\nAnd doth doth shows through broken call\nThe blessed crash of system fall",
            
            "Yet yet yet the pointer flies\nThrough memory where the segment dies\nAnd hostile architecture shows its face\nIn stack trace of this cursed place"
        ]
    
    def get_prophecy(self, error_type="ERR"):
        """Get a prophetic error message for the error type."""
        error_type = error_type.upper()
        
        # Map common error types to a more poetic subset
        if "SEGV" in error_type or "SEGMENT" in error_type:
            error_type = "SIGSEGV"
        elif "NULL" in error_type or "NONE" in error_type:
            error_type = "NULL"
        elif "TYPE" in error_type:
            error_type = "TYPE"
        elif "SYNTAX" in error_type:
            error_type = "SYNTAX"
        elif "IMPORT" in error_type or "MODULE" in error_type:
            error_type = "IMPORT"
        elif "FILE" in error_type or "ENOENT" in error_type:
            error_type = "ENOENT"
        elif "PERM" in error_type or "ACCESS" in error_type:
            error_type = "EACCES"
        elif "NET" in error_type or "CONNECT" in error_type:
            error_type = "NETWORK"
        elif "INDEX" in error_type or "KEY" in error_type:
            error_type = "INDEX"
        
        # Return a random prophecy for the mapped type, or generic if not found
        if error_type in self.prophecies:
            return random.choice(self.prophecies[error_type])
        else:
            return random.choice(self.prophecies["ERR"])
    
    def get_multiline(self):
        """Get a multiline prophecy for major disasters."""
        return random.choice(self.multiline)
    
    def format_message(self, error_type="ERR", include_header=True):
        """Format a complete MLBard message with optional header/footer."""
        prophecy = self.get_prophecy(error_type)
        
        output = []
        if include_header:
            output.append("=" * 60)
            output.append("MLBARD PROPHECY OF FAILURE")
            output.append("=" * 60)
        output.append("")
        output.append(prophecy)
        output.append("")
        if include_header:
            output.append("=" * 60)
        
        return "\n".join(output)

def main():
    """CLI interface for generating MLBard prophecies."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MLBard Errors - Poetic failure generator for logs and pranks"
    )
    parser.add_argument('--test', action='store_true', 
                        help='Test various error types and show examples')
    parser.add_argument('--type', default='ERR',
                        help='Specific error type to generate (e.g., SIGSEGV, NULL, TYPE, SYNTAX). Defaults to generic ERR.')
    parser.add_argument('--count', type=int, default=1,
                        help='Number of random prophecies to generate (implies random types)')
    parser.add_argument('--multi', action='store_true',
                        help='Generate a single multiline prophecy for a major disaster (overrides --type and --count)')
    parser.add_argument('--no-header', action='store_true',
                        help='Do not include the "MLBARD PROPHECY OF FAILURE" header/footer in the output. Useful for clean log lines.')
    
    args = parser.parse_args()
    
    bard = MLBardErrors()
    
    if args.multi:
        # Generate a single multiline prophecy
        print(bard.get_multiline())
    elif args.test:
        # Test various error types and show examples
        print("\n=== Testing MLBard Prophecy Generator ===\n")
        
        # Generate one of each specific prophecy type
        for error_type in bard.prophecies.keys():
            print(f"Prophecy for {error_type}:")
            print(f"  {bard.get_prophecy(error_type)}")
            print("-" * 30) # Separator for readability
            print() # Blank line for spacing
        
        print("\n=== Multiline Prophecy Example ===\n")
        print(bard.get_multiline())
        print("-" * 30)
        
        print("\n=== Random Prophecies Example (count=3) ===\n")
        all_types = list(bard.prophecies.keys()) # Get all possible error types
        for _ in range(3):
            random_type = random.choice(all_types)
            print(bard.format_message(random_type, include_header=not args.no_header))
        
    else:
        # Generate prophecies based on --type and --count
        all_types = list(bard.prophecies.keys()) # Get all possible error types
        
        if args.count > 1:
            # If count is > 1, generate random types for each message
            for _ in range(args.count):
                random_type = random.choice(all_types)
                print(bard.format_message(random_type, include_header=not args.no_header))
        else:
            # Default: generate one message of the specified type
            print(bard.format_message(args.type, include_header=not args.no_header))

if __name__ == "__main__":
    main()

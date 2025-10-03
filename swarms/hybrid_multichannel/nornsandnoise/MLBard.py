#!/usr/bin/env python3
"""
MLBard - Turn any text into a sonnet
Because poetry is just pattern matching with pretensions

Usage:
    python3 mlbard.py "Your text here"
    python3 mlbard.py file.txt
    python3 mlbard.py --about suiteCRM
    cat README.md | python3 mlbard.py -
"""

import re
import random
import sys
from collections import Counter
from pathlib import Path

class MLBard:
    """
    Transform any text into technically correct sonnets.
    Not good sonnets. Working sonnets.
    """
    
    def __init__(self):
        # Rhyme patterns for true sonnet structure
        self.rhyme_scheme = "ABABCDCDEFEFGG"
        
        # Word banks for padding and rhyming
        self.fillers = ['doth', 'shall', 'midst', 'yet', 'still', 'fair', 'sweet', 'most']
        
        # Common endings that rhyme
        self.rhyme_groups = {
            'ode': ['code', 'node', 'mode', 'load', 'abode', 'explode', 'corrode'],
            'ing': ['thing', 'bring', 'sing', 'spring', 'ring', 'cling', 'string'],
            'ight': ['fight', 'light', 'might', 'right', 'sight', 'plight', 'knight'],
            'ay': ['day', 'way', 'say', 'play', 'stay', 'may', 'ray', 'bay'],
            'ine': ['line', 'mine', 'fine', 'wine', 'pine', 'shrine', 'sign'],
            'ate': ['late', 'fate', 'gate', 'state', 'rate', 'create', 'mate'],
            'all': ['call', 'fall', 'all', 'wall', 'small', 'tall', 'install'],
            'ail': ['fail', 'mail', 'tail', 'rail', 'sail', 'trail', 'frail'],
            'ore': ['more', 'core', 'bore', 'store', 'before', 'restore', 'deplore'],
            'ear': ['year', 'clear', 'dear', 'fear', 'near', 'appear', 'tear'],
            'ake': ['make', 'take', 'break', 'wake', 'sake', 'snake', 'mistake'],
            'ound': ['found', 'ground', 'sound', 'bound', 'round', 'compound', 'profound'],
            'ue': ['true', 'blue', 'due', 'clue', 'new', 'view', 'pursue'],
            'est': ['best', 'test', 'rest', 'quest', 'nest', 'blessed', 'stressed']
        }
        
        # Verbs for action
        self.verbs = ['runs', 'breaks', 'builds', 'fails', 'crashes', 'compiles', 
                      'flows', 'grows', 'shows', 'knows', 'throws', 'glows',
                      'speaks', 'seeks', 'makes', 'takes', 'shakes', 'wakes']
        
        # Adjectives for flavor
        self.adjectives = ['hostile', 'simple', 'complex', 'broken', 'cursed', 'blessed',
                          'twisted', 'tangled', 'pure', 'dark', 'bright', 'lost']
        
        # Templates for different line positions
        self.templates = {
            'opening': [
                "When {noun} doth {verb} with {adj} {concept}",
                "If {noun} be {adj}, then {concept} {verb}",
                "The {adj} {noun} that {verb} through {concept}",
                "O {adj} {noun}, why must thou {verb}?"
            ],
            'middle': [
                "And {noun} shall {verb} till {concept} {verb2}",
                "Where {adj} {noun} in {concept} {verb}",
                "The {noun} that {verb} with {adj} design",
                "Yet {noun} doth {verb} and {verb2} still"
            ],
            'volta': [  # Line 9, where sonnets "turn"
                "But soft! What {noun} through {concept} breaks?",
                "Yet in this {adj} {noun} there {verb}",
                "But lo! The {noun} begins to {verb}",
                "And yet, despite the {adj} {concept}"
            ],
            'couplet': [
                "So long as {noun} can {verb} and {concept} see",
                "So long lives this, and this gives life to thee",
                "Thus {noun} and {concept} forever {verb}",
                "And {adj} {noun} shall never die"
            ]
        }
    
    def extract_concepts(self, text):
        """Extract key words from input text"""
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Count frequencies
        word_freq = Counter(words)
        
        # Filter out common words
        common = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be'}
        
        concepts = []
        for word, count in word_freq.most_common():
            if word not in common and len(word) > 3:
                concepts.append(word)
                if len(concepts) >= 20:  # We need enough for variety
                    break
        
        # Add some defaults if we don't have enough
        if len(concepts) < 10:
            concepts.extend(['code', 'function', 'system', 'error', 'logic'])
        
        return concepts
    
    def count_syllables(self, word):
        """Count syllables in a word (approximately)"""
        word = word.lower()
        vowels = "aeiouy"
        syllables = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllables += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e') and syllables > 1:
            syllables -= 1
        
        # Words always have at least one syllable
        return max(1, syllables)
    
    def count_line_syllables(self, line):
        """Count total syllables in a line"""
        words = line.split()
        return sum(self.count_syllables(word) for word in words)
    
    def get_rhyme_word(self, rhyme_group):
        """Get a word from a rhyme group"""
        if rhyme_group in self.rhyme_groups:
            return random.choice(self.rhyme_groups[rhyme_group])
        # Fallback to generic rhymes
        return random.choice(['day', 'way', 'light', 'night', 'time', 'rhyme'])
    
    def build_line(self, template, concepts, target_syllables=10):
        """Build a line from template"""
        line = template
        
        # Replace placeholders
        line = line.replace('{noun}', random.choice(concepts))
        line = line.replace('{concept}', random.choice(concepts))
        line = line.replace('{verb}', random.choice(self.verbs))
        line = line.replace('{verb2}', random.choice(self.verbs))
        line = line.replace('{adj}', random.choice(self.adjectives))
        
        # Adjust syllables
        current = self.count_line_syllables(line)
        
        # Add or remove words to hit target
        words = line.split()
        while current < target_syllables and len(words) < 12:
            # Add a filler word
            position = random.randint(0, len(words))
            words.insert(position, random.choice(self.fillers))
            line = ' '.join(words)
            current = self.count_line_syllables(line)
        
        while current > target_syllables and len(words) > 3:
            # Remove small words
            for word in ['the', 'a', 'an', 'doth', 'shall', 'with']:
                if word in words:
                    words.remove(word)
                    break
            else:
                # Remove random word if no small words
                words.pop(random.randint(0, len(words)-1))
            line = ' '.join(words)
            current = self.count_line_syllables(line)
        
        return line
    
    def create_sonnet(self, text):
        """Create a complete sonnet from input text"""
        concepts = self.extract_concepts(text)
        
        # Determine rhyme words for the scheme ABABCDCDEFEFGG
        rhyme_map = {}
        used_groups = []
        
        for char in set(self.rhyme_scheme):
            available = [g for g in self.rhyme_groups.keys() if g not in used_groups]
            if available:
                group = random.choice(available)
                used_groups.append(group)
                rhyme_map[char] = group
        
        lines = []
        
        for i, rhyme_char in enumerate(self.rhyme_scheme):
            # Choose template based on position
            if i == 0:  # Opening
                template = random.choice(self.templates['opening'])
            elif i == 8:  # Volta (turn)
                template = random.choice(self.templates['volta'])
            elif i >= 12:  # Couplet
                template = random.choice(self.templates['couplet'])
            else:  # Middle
                template = random.choice(self.templates['middle'])
            
            # Build the line
            line = self.build_line(template, concepts)
            
            # Force rhyme at end
            if rhyme_char in rhyme_map:
                rhyme_word = self.get_rhyme_word(rhyme_map[rhyme_char])
                words = line.split()
                if words:
                    words[-1] = rhyme_word
                    line = ' '.join(words)
            
            lines.append(line)
        
        # Format as quatrains + couplet
        formatted = []
        formatted.extend(lines[0:4])   # First quatrain
        formatted.append('')            # Blank line
        formatted.extend(lines[4:8])   # Second quatrain
        formatted.append('')            # Blank line
        formatted.extend(lines[8:12])  # Third quatrain
        formatted.append('')            # Blank line
        formatted.extend(lines[12:14]) # Couplet
        
        return '\n'.join(formatted)
    
    def create_title(self, text):
        """Generate a pretentious title"""
        concepts = self.extract_concepts(text)
        if concepts:
            main_concept = concepts[0].title()
            return f"Sonnet Upon the {random.choice(['Hostility', 'Complexity', 'Nature', 'Essence'])} of {main_concept}"
        return "Sonnet DCCLXXI"  # 771 in Roman numerals

def main():
    """Main entry point"""
    bard = MLBard()
    
    # Handle input
    if len(sys.argv) < 2:
        print("Usage: mlbard.py <text or filename>")
        print("       mlbard.py --about <topic>")
        print("       cat file | mlbard.py -")
        sys.exit(1)
    
    if sys.argv[1] == '--about':
        # Generate about a topic
        topic = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'code'
        text = f"The {topic} is complex and hostile with many functions and purposes but no simplicity"
    elif sys.argv[1] == '-':
        # Read from stdin
        text = sys.stdin.read()
    else:
        # Try as file first, then as direct text
        path = Path(sys.argv[1])
        if path.exists():
            text = path.read_text()
        else:
            text = ' '.join(sys.argv[1:])
    
    # Generate sonnet
    title = bard.create_title(text)
    sonnet = bard.create_sonnet(text)
    
    # Output with dramatic flair
    print("\n" + "="*50)
    print(f"{title:^50}")
    print("="*50 + "\n")
    print(sonnet)
    print("\n" + "-"*50)
    print(f"{'-- MLBard': >50}")
    print("-"*50 + "\n")

if __name__ == "__main__":
    main()
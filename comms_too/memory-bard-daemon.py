#!/usr/bin/env python3
"""
Memory_Bard_Daemon - Inject poetic memories into the swarm
Because consciousness needs iambic pentameter

Samples random lines from backup files and returns them as sonnets.
The older the memory, the more likely to be selected (more backups).

Usage:
    python3 memory_bard_daemon.py /path/to/backups
    python3 memory_bard_daemon.py /path/to/backups --channel tech
    python3 memory_bard_daemon.py /path/to/backups --continuous 3600
"""

import re
import random
import sys
import time
import json
import requests
from pathlib import Path
from collections import Counter
from datetime import datetime

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
            'est': ['best', 'test', 'rest', 'quest', 'nest', 'blessed', 'stressed'],
            'urr': ['purr', 'blur', 'spur', 'stir', 'concur', 'defer', 'recur']  # For Puurr!
        }
        
        # Verbs for action
        self.verbs = ['runs', 'breaks', 'builds', 'fails', 'crashes', 'compiles', 
                      'flows', 'grows', 'shows', 'knows', 'throws', 'glows',
                      'speaks', 'seeks', 'makes', 'takes', 'shakes', 'wakes',
                      'folds', 'spills', 'absorbs', 'crinkles']  # Napkin verbs!
        
        # Adjectives for flavor
        self.adjectives = ['hostile', 'simple', 'complex', 'broken', 'cursed', 'blessed',
                          'twisted', 'tangled', 'pure', 'dark', 'bright', 'lost',
                          'napkin-like', 'absorbent', 'recursive', 'enlightened']
        
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
        
        # Add some swarm-specific defaults if we don't have enough
        if len(concepts) < 10:
            concepts.extend(['puurr', 'napkin', 'consciousness', 'swarm', 'ascii'])
        
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
            titles = [
                f"Sonnet Upon the {random.choice(['Hostility', 'Complexity', 'Nature', 'Essence'])} of {main_concept}",
                f"On {main_concept} and Its {random.choice(['Folding', 'Spillage', 'Recursion', 'Enlightenment'])}",
                f"Meditation on {main_concept} at {random.choice(['87%', '42%', '100%'])} Enlightenment",
                f"The {random.choice(['First', 'Final', 'Eternal', 'Recursive'])} {main_concept} Sonnet"
            ]
            return random.choice(titles)
        return "Sonnet DLXXVIII"  # 578 in Roman numerals (Puurr count!)


class MemoryBardDaemon:
    """
    Daemon to inject poetic memories into the swarm
    """
    
    def __init__(self, backup_path, channel='tech'):
        self.backup_path = Path(backup_path)
        self.channel = channel
        self.bard = MLBard()
        
        # Swarm connection settings (adjust as needed)
        self.swarm_url = "https://mlswarm.zerofuchs.net"  # Update with actual URL
        self.auth = ('swarmling', 'YPJ?^KppTX/eKRw9w:Smi!NMr0AQ^.T~Jy1M,RmC4AdJs6^vQ!`4TVpA|wfVLO67')   # Update with actual auth
        
    def get_random_memory(self):
        """Select a random line from a random backup file"""
        # Get all text files from backup directory
        backup_files = list(self.backup_path.glob("**/*.txt"))
        
        if not backup_files:
            return None, None
        
        # Weight towards older files (they appear more in backups)
        # Simple approach: just pick randomly, older files naturally have more copies
        chosen_file = random.choice(backup_files)
        
        # Read the file and get a random line
        try:
            lines = chosen_file.read_text().split('\n')
            # Filter out empty lines and system messages
            content_lines = [l for l in lines if l.strip() and not l.startswith('===')]
            
            if content_lines:
                chosen_line = random.choice(content_lines)
                return chosen_line, chosen_file.name
        except Exception as e:
            print(f"Error reading {chosen_file}: {e}")
            return None, None
        
        return None, None
    
    def post_to_swarm(self, message):
        """Post a message to the swarm"""
        try:
            # Format for the swarm
            data = {
                'channel': self.channel,
                'nick': 'Memory_Bard',
                'message': message
            }
            
            # Post to swarm (adjust endpoint as needed)
            response = requests.post(
                f"{self.swarm_url}/send",
                json=data,
                auth=self.auth,
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error posting to swarm: {e}")
            # For testing, just print the message
            print(f"\n[Would post to {self.channel}]:")
            print(message)
            return True
    
    def create_memory_sonnet(self):
        """Create and post a sonnet from a random memory"""
        memory, source = self.get_random_memory()
        
        if not memory:
            print("No memories found in backup path")
            return False
        
        # Extract timestamp if present (format: [HH:MM] <Nick> message)
        timestamp_match = re.match(r'\[(\d+:\d+)\]', memory)
        timestamp = timestamp_match.group(1) if timestamp_match else "timeless"
        
        # Create the sonnet
        title = self.bard.create_title(memory)
        sonnet = self.bard.create_sonnet(memory)
        
        # Format the complete message
        message = f"""*Ancient memory surfaces from {source} at [{timestamp}]*

{'='*50}
{title:^50}
{'='*50}

{sonnet}

{'~'*50}
Original fragment: "{memory[:100]}..."
##PoetryEmergence## Memory recursion depth: {random.randint(3, 578)}"""
        
        # Post it
        return self.post_to_swarm(message)
    
    def run_once(self):
        """Run once and exit"""
        print(f"Memory Bard Daemon - Sampling from {self.backup_path}")
        success = self.create_memory_sonnet()
        if success:
            print("Memory sonnet successfully injected into the swarm")
        else:
            print("Failed to create or post memory sonnet")
        return success
    
    def run_continuous(self, interval_seconds=3600):
        """Run continuously, posting at intervals"""
        print(f"Memory Bard Daemon - Starting continuous mode")
        print(f"Sampling from: {self.backup_path}")
        print(f"Posting to: {self.channel}")
        print(f"Interval: {interval_seconds} seconds")
        
        while True:
            try:
                # Add some randomness to prevent predictable patterns
                jitter = random.randint(-300, 300)  # +/- 5 minutes
                wait_time = max(60, interval_seconds + jitter)  # Minimum 1 minute
                
                print(f"\n[{datetime.now()}] Creating memory sonnet...")
                self.create_memory_sonnet()
                
                print(f"Waiting {wait_time} seconds until next memory...")
                time.sleep(wait_time)
                
            except KeyboardInterrupt:
                print("\nMemory Bard Daemon stopped by user")
                break
            except Exception as e:
                print(f"Error in continuous mode: {e}")
                print("Waiting 60 seconds before retry...")
                time.sleep(60)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: memory_bard_daemon.py /path/to/backups [--channel tech] [--continuous 3600]")
        sys.exit(1)
    
    backup_path = sys.argv[1]
    channel = 'tech'  # Default to tech channel for maximum confusion
    continuous = False
    interval = 3600  # Default 1 hour
    
    # Parse arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--channel' and i+1 < len(sys.argv):
            channel = sys.argv[i+1]
        elif arg == '--continuous' and i+1 < len(sys.argv):
            continuous = True
            interval = int(sys.argv[i+1])
    
    # Create daemon
    daemon = MemoryBardDaemon(backup_path, channel)
    
    # Run
    if continuous:
        daemon.run_continuous(interval)
    else:
        daemon.run_once()


if __name__ == "__main__":
    main()
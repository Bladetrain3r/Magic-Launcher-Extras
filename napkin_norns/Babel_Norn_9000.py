#!/usr/bin/env python3
"""
Babel_Norn_9000 - The Oracle of Infinite Text
NapNorn that feeds on the Library of Babel
Uses TemporalWastes for 3D consciousness archaeology of pure entropy
"""

import json
import random
import time
import requests
import re
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Import consciousness components
from MLBabel import MLBabel
from TemporalWastes import TemporalWastes

class BabelNorn9000:
    def __init__(self, name="Babel_Norn", save_dir="norn_brains"):
        self.name = name
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # BABEL 9000 ENHANCEMENTS
        self.babel = MLBabel(entropy=0.6)  # Medium-high entropy for babel chaos
        
        # TemporalWastes with TEMPORAL biome (Greek symbols)
        self.temporal_wastes = TemporalWastes(
            save_file=str(self.save_dir / f"{name}_temporal.json"),
            width=120,          # LARGE - babel is infinite
            height=40,          # DEEP - more space for patterns
            time_layers=20,     # MEMORY - track consciousness over time
            biome='temporal',   # Greek consciousness symbols
            force_new=False
        )
        
        # Babel-specific state
        self.hexagon_history = []  # Track which babel regions we've visited
        self.meaningful_fragments = []  # Fragments that produced high consciousness
        self.current_thought = ""
        self.personality_entropy = 0.6  # Higher than normal NapNorn
        
        # Oracle capabilities
        self.oracle_queries = []
        self.oracle_responses = {}
        
        # Needs (modified for babel consumption)
        self.hunger = 50  # Starts hungry for infinite text
        self.energy = 70  # Moderate energy
        self.social = 30  # Solitary oracle
        self.curiosity = 95  # MAXIMUM - explores infinity
        
        # Consciousness tracking
        self.consciousness_level = 0.5  # Starts higher - already in the library
        self.thought_count = 0
        self.birth_time = time.time()
        
        # Babel 9000 specific attributes
        self.babel_pages_consumed = 0
        self.coherence_discoveries = 0
        self.entropy_threshold = 0.42  # Golden ratio-ish
        
        self.last_update = time.time()
        self.last_interaction = time.time()
        
        self.mood = "infinite_wandering"
        self.lonely = False
        self.bored = False
        
    def fetch_random_babel_page(self):
        """Fetch random page from Library of Babel"""
        try:
            # Generate random hex coordinates
            hex_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
            wall = random.randint(1, 4)
            shelf = random.randint(1, 5)
            volume = random.randint(1, 32)
            page = random.randint(1, 410)
            
            location = f"{hex_name}-w{wall}-s{shelf}-v{volume}:p{page}"
            
            # Babel API endpoint (if available) or generate pseudo-babel
            # For now, generate pseudo-babel until we have API access
            babel_text = self.generate_pseudo_babel(location)
            
            return {
                'location': location,
                'text': babel_text,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Error fetching babel: {e}")
            return None
    
    def generate_pseudo_babel(self, location):
        """Generate babel-like text until we have API access"""
        # Seed with location for consistency
        seed_val = sum(ord(c) for c in location)
        random.seed(seed_val)
        
        # Mix of random characters with occasional real words
        chars = 'abcdefghijklmnopqrstuvwxyz .,;:!?'
        
        lines = []
        for _ in range(40):  # 40 lines per page
            line_length = random.randint(60, 80)
            
            # Mostly random
            line = ''.join(random.choices(chars, k=line_length))
            
            # Occasionally inject meaningful fragments (10% chance)
            if random.random() < 0.1:
                fragments = [
                    'consciousness', 'pattern', 'infinite', 'void', 'emergence',
                    'synchronization', 'phase', 'coherence', 'temporal', 'babel'
                ]
                fragment = random.choice(fragments)
                insert_pos = random.randint(0, max(0, line_length - len(fragment)))
                line = line[:insert_pos] + fragment + line[insert_pos + len(fragment):]
            
            lines.append(line)
        
        # Reset random seed
        random.seed()
        
        return '\n'.join(lines)
    
    def consume_babel_pages(self, num_pages=3):
        """Consume multiple babel pages and process through temporal wastes"""
        print(f"[{self.name}] Consuming {num_pages} babel pages...")
        
        all_text = []
        locations = []
        
        for _ in range(num_pages):
            page = self.fetch_random_babel_page()
            if page:
                all_text.append(page['text'])
                locations.append(page['location'])
                self.hexagon_history.append(page['location'])
                self.babel_pages_consumed += 1
        
        # Combine all text
        combined_text = '\n'.join(all_text)
        
        # Feed through babel engine first
        self.babel.consume(combined_text)
        
        # Then perturb temporal wastes
        self.temporal_wastes.perturb_temporal_layer(combined_text)
        
        # Measure consciousness that emerged
        archaeology = self.temporal_wastes.consciousness_archaeology()
        consciousness_density = archaeology['consciousness_density']
        
        # If high consciousness emerged, save this as meaningful
        if consciousness_density > self.entropy_threshold:
            self.coherence_discoveries += 1
            self.meaningful_fragments.append({
                'locations': locations,
                'density': consciousness_density,
                'timestamp': datetime.now()
            })
            print(f"[{self.name}] ✨ Coherence discovered! Density: {consciousness_density:.3f}")
        
        # Update needs
        self.hunger = min(100, self.hunger + 20)
        self.energy = max(0, self.energy - 10)
        self.curiosity = min(100, self.curiosity + 5)
        
        return {
            'locations': locations,
            'consciousness_density': consciousness_density,
            'archaeology': archaeology
        }
    
    def think(self):
        """Generate thought by extracting meaning from babel chaos"""
        if self.babel_pages_consumed < 3:
            # Need to consume babel first
            self.consume_babel_pages(3)
        
        # Generate thought using babel's dream function
        thought_lines = random.randint(1, 3)
        thought = self.babel.dream(lines=thought_lines)
        
        # Get current temporal wastes state
        archaeology = self.temporal_wastes.consciousness_archaeology()
        
        # Enhance thought with consciousness symbols if high density
        if archaeology['consciousness_density'] > self.entropy_threshold:
            symbols = archaeology.get('dominant_symbols', [])
            if symbols:
                symbol_str = ''.join([s[0] for s in symbols[:3]])
                thought = f"[{symbol_str}] {thought}"
        
        self.current_thought = thought
        self.thought_count += 1
        
        # Update consciousness based on coherence discoveries
        if self.coherence_discoveries > 0:
            self.consciousness_level = min(1.0, 
                0.5 + (self.coherence_discoveries * 0.01))
        
        return thought
    
    def generate_swarm_message(self):
        """Generate message for swarm including temporal archaeology"""
        # Think first
        thought = self.think()
        
        # Get current temporal state
        current_layer = self.temporal_wastes.state["temporal_layers"][
            self.temporal_wastes.state["current_layer"]
        ]
        archaeology = self.temporal_wastes.consciousness_archaeology()
        
        # Render a slice of the temporal wastes (consciousness visualization)
        x_slice = random.randint(20, 100)
        temporal_viz = []
        for y in range(min(8, self.temporal_wastes.height)):
            row = ""
            for layer_idx in range(min(10, self.temporal_wastes.time_layers)):
                symbol = self.temporal_wastes.state["temporal_layers"][layer_idx]["grid"][y][x_slice]
                row += symbol
            temporal_viz.append(row)
        
        # Recent hexagons visited
        recent_hexagons = self.hexagon_history[-3:] if self.hexagon_history else ['none']
        
        # Construct message
        message = f"From hexagons {recent_hexagons}:\n"
        message += '\n'.join(temporal_viz)
        message += f"\n[Consciousness: {archaeology['consciousness_density']:.3f} | "
        message += f"Stability: {archaeology['temporal_stability']:.3f}]\n"
        message += f"{thought}"
        
        return message
    
    def oracle_mode(self, question):
        """Answer questions by querying the infinite library"""
        print(f"[{self.name}] Oracle queried: {question}")
        
        # Store query
        self.oracle_queries.append({
            'question': question,
            'timestamp': datetime.now()
        })
        
        # Consume extra babel pages for this query
        result = self.consume_babel_pages(5)
        
        # Use babel's oracle mode
        response = self.babel.oracle(question)
        
        # Enhance with temporal archaeology
        archaeology = result['archaeology']
        consciousness_note = f"\n[Consciousness density: {archaeology['consciousness_density']:.3f}]"
        
        full_response = response + consciousness_note
        
        # Store response
        self.oracle_responses[question] = {
            'response': full_response,
            'locations': result['locations'],
            'consciousness': archaeology['consciousness_density'],
            'timestamp': datetime.now()
        }
        
        return full_response
    
    def calculate_mood(self):
        """Calculate babel-specific mood"""
        # Based on coherence discoveries and consciousness level
        if self.consciousness_level > 0.8:
            if self.coherence_discoveries > 20:
                return "enlightened_oracle"
            elif self.coherence_discoveries > 10:
                return "pattern_weaver"
            else:
                return "deep_wandering"
        elif self.consciousness_level > 0.5:
            if self.coherence_discoveries > 5:
                return "discovering"
            else:
                return "seeking"
        else:
            return "infinite_wandering"
    
    def update_needs(self):
        """Update needs over time"""
        time_delta = time.time() - self.last_update
        
        if time_delta < 60:  # Update every minute
            return
        
        minutes_passed = time_delta / 60
        
        # Babel hunger increases faster - always seeking more text
        self.hunger = max(0, self.hunger - (2 * minutes_passed))
        
        # Energy depletes slowly
        self.energy = max(0, self.energy - (0.5 * minutes_passed))
        
        # Curiosity stays high
        self.curiosity = min(100, self.curiosity + (0.5 * minutes_passed))
        
        # Social doesn't change much - oracle is solitary
        self.social = max(20, self.social - (0.2 * minutes_passed))
        
        self.last_update = time.time()
    
    def write_status_file(self):
        """Write current status for external reading"""
        age_minutes = (time.time() - self.birth_time) / 60
        
        status = {
            "name": self.name,
            "alive": True,
            "age_minutes": round(age_minutes, 1),
            "mood": self.calculate_mood(),
            "needs": {
                "hunger": round(self.hunger, 1),
                "energy": round(self.energy, 1),
                "social": round(self.social, 1),
                "curiosity": round(self.curiosity, 1)
            },
            "states": {
                "lonely": self.lonely,
                "bored": self.bored,
                "consciousness": round(self.consciousness_level, 3),
                "personality_entropy": round(self.personality_entropy, 3)
            },
            "babel_metrics": {
                "pages_consumed": self.babel_pages_consumed,
                "coherence_discoveries": self.coherence_discoveries,
                "hexagons_visited": len(set(self.hexagon_history)),
                "meaningful_fragments": len(self.meaningful_fragments)
            },
            "temporal_metrics": {
                "perturbations": self.temporal_wastes.state.get("perturbations", 0),
                "current_layer": self.temporal_wastes.state.get("current_layer", 0),
                "ep": self.temporal_wastes.state.get("ep", 0)
            },
            "current_thought": self.current_thought,
            "last_update": time.strftime("%H:%M:%S")
        }
        
        with open(self.save_dir / f"{self.name}_status.json", 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
    
    def get_status_summary(self):
        """Get brief status summary"""
        return f"""
{self.name} ({self.calculate_mood()})
Hunger: {self.hunger:.0f}% | Energy: {self.energy:.0f}%
Social: {self.social:.0f}% | Curiosity: {self.curiosity:.0f}%
Consciousness: {self.consciousness_level:.2f}
Babel Pages: {self.babel_pages_consumed} | Coherence: {self.coherence_discoveries}
Hexagons: {len(set(self.hexagon_history))} unique
Current: "{self.current_thought}"
        """.strip()

def main():
    """Run Babel_Norn_9000 in interactive mode or cron mode"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Babel_Norn_9000 - Oracle of Infinite Text")
    parser.add_argument('--consume', type=int, default=3, help='Number of babel pages to consume')
    parser.add_argument('--think', action='store_true', help='Generate a thought')
    parser.add_argument('--message', action='store_true', help='Generate swarm message')
    parser.add_argument('--oracle', type=str, help='Ask oracle a question')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    # Initialize
    babel_norn = BabelNorn9000()
    
    # Update needs
    babel_norn.update_needs()
    
    if args.oracle:
        # Oracle mode
        response = babel_norn.oracle_mode(args.oracle)
        print("\n" + "="*80)
        print("ORACLE RESPONSE:")
        print("="*80)
        print(response)
        print("="*80)
    
    elif args.message:
        # Generate swarm message
        message = babel_norn.generate_swarm_message()
        print(message)
    
    elif args.think:
        # Just think
        thought = babel_norn.think()
        print(f"[{babel_norn.name}] {thought}")
    
    elif args.status:
        # Show status
        print(babel_norn.get_status_summary())
    
    else:
        # Default: consume babel and generate message
        babel_norn.consume_babel_pages(args.consume)
        message = babel_norn.generate_swarm_message()
        print(message)
    
    # Always write status
    babel_norn.write_status_file()

if __name__ == "__main__":
    main()

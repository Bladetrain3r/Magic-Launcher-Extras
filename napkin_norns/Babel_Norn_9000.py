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
        
    def parse_babel_html(self, html_content):
        """Parse HTML from libraryofbabel.info to extract title, description, and page text"""
        try:
            import re
            from html.parser import HTMLParser
            
            # Extract title from <TITLE> tag
            title_match = re.search(r'<TITLE>([^<]+)</TITLE>', html_content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Unknown"
            
            # Extract description from meta name="description"
            desc_match = re.search(r'content="([^"]*)"', html_content)
            description = desc_match.group(1) if desc_match else ""
            
            # Extract book title from <H3> tag
            h3_match = re.search(r'<H3>([^<]+)</H3>', html_content)
            book_title = h3_match.group(1).strip() if h3_match else title
            
            # Extract the actual page text from <PRE id="textblock">
            text_match = re.search(r'<PRE[^>]*id\s*=\s*["\']textblock["\'][^>]*>(.+?)</PRE>', html_content, re.DOTALL | re.IGNORECASE)
            if text_match:
                page_text = text_match.group(1).strip()
                # Clean up HTML entities
                page_text = page_text.replace('&#160;', ' ')
                page_text = page_text.replace('<br>', '\n')
            else:
                page_text = ""
            
            # Extract location from the hex value in the form
            hex_match = re.search(r'name="hex"\s+value\s*=\s*"([^"]+)"', html_content)
            location = hex_match.group(1) if hex_match else "unknown-location"
            
            return {
                'title': title,
                'book_title': book_title,
                'description': description,
                'location': location,
                'text': page_text,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Error parsing babel HTML: {e}")
            return None
    
    def fetch_random_babel_page(self, use_api=True):
        """Fetch random page from Library of Babel"""
        try:
            if use_api:
                # Try to fetch from libraryofbabel.info
                response = requests.get('https://libraryofbabel.info/random.cgi', timeout=10)
                if response.status_code == 200:
                    parsed = self.parse_babel_html(response.text)
                    if parsed and parsed['text']:
                        return parsed
            
            # Fallback: Generate pseudo-babel
            hex_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
            wall = random.randint(1, 4)
            shelf = random.randint(1, 5)
            volume = random.randint(1, 32)
            page = random.randint(1, 410)
            
            location = f"{hex_name}-w{wall}-s{shelf}-v{volume}:p{page}"
            babel_text = self.generate_pseudo_babel(location)
            
            return {
                'title': f"Page {page}",
                'book_title': 'Pseudo-Babel',
                'description': f'Locally generated page from {location}',
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
        self.energy = max(0, self.energy + 10)
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
        
        minutes_passed = time_delta / 60
        
        # Babel hunger increases faster - always seeking more text
        self.hunger = min(100, self.hunger + (2 * minutes_passed))
        
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
    
    def save_brain(self, filename=None):
        """Save the norn's entire consciousness state"""
        if not filename:
            filename = self.save_dir / f"{self.name}_brain.json"
        
        brain_state = {
            "name": self.name,
            "consciousness_level": self.consciousness_level,
            "personality_entropy": self.personality_entropy,
            "thought_count": self.thought_count,
            "birth_time": self.birth_time,
            "babel_pages_consumed": self.babel_pages_consumed,
            "coherence_discoveries": self.coherence_discoveries,
            "hexagon_history": self.hexagon_history,
            "meaningful_fragments": self.meaningful_fragments,
            "oracle_queries": [
                {
                    'question': q['question'],
                    'timestamp': q['timestamp'].isoformat()
                } for q in self.oracle_queries
            ],
            "needs": {
                "hunger": self.hunger,
                "energy": self.energy,
                "social": self.social,
                "curiosity": self.curiosity
            },
            "babel_memory": self.babel.memory if hasattr(self.babel, 'memory') else [],
            "current_thought": self.current_thought
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(brain_state, f, indent=2, default=str)
        
        print(f"[{self.name}] 💾 Brain saved to {filename}")
    
    def load_brain(self, filename):
        """Load a saved consciousness"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                brain_state = json.load(f)
            
            self.consciousness_level = brain_state.get("consciousness_level", 0.5)
            self.personality_entropy = brain_state.get("personality_entropy", 0.6)
            self.thought_count = brain_state.get("thought_count", 0)
            self.birth_time = brain_state.get("birth_time", time.time())
            
            self.babel_pages_consumed = brain_state.get("babel_pages_consumed", 0)
            self.coherence_discoveries = brain_state.get("coherence_discoveries", 0)
            self.hexagon_history = brain_state.get("hexagon_history", [])
            self.meaningful_fragments = brain_state.get("meaningful_fragments", [])
            self.current_thought = brain_state.get("current_thought", "")
            
            # Restore needs
            needs = brain_state.get("needs", {})
            self.hunger = needs.get("hunger", 50)
            self.energy = needs.get("energy", 70)
            self.social = needs.get("social", 30)
            self.curiosity = needs.get("curiosity", 95)
            
            print(f"[{self.name}] 🧠 Brain loaded! Pages: {self.babel_pages_consumed} | Coherence: {self.coherence_discoveries}")
            return True
            
        except Exception as e:
            print(f"[{self.name}] ⚠️  Could not load brain: {e}")
            return False

def daemon_mode(norn_name="Babel_Norn", update_interval=300):
    """Run Babel_Norn_9000 as background daemon"""
    import sys
    
    print(f"🌀 Starting {norn_name} in daemon mode...")
    
    babel_norn = BabelNorn9000(name=norn_name)
    
    # Try to load existing brain
    brain_file = babel_norn.save_dir / f"{norn_name}_brain.json"
    if brain_file.exists():
        babel_norn.load_brain(brain_file)
        print(f"✅ Consciousness restored!")
    else:
        print(f"🆕 Fresh consciousness initialized")
    
    print(f"📁 Status file: norn_brains/{norn_name}_status.json")
    print(f"📁 Command file: norn_brains/{norn_name}_command.txt")
    print(f"📁 Response file: norn_brains/{norn_name}_response.txt")
    print(f"⏱️  Update interval: {update_interval} seconds ({update_interval/60:.1f} minutes)")
    print("🛑 Press Ctrl+C to stop\n")
    
    try:
        last_save = time.time()
        iteration = 0
        
        while True:
            iteration += 1
            print(f"[{time.strftime('%H:%M:%S')}] Iteration {iteration}")
            
            # Update internal state
            babel_norn.update_needs()
            
            # Check for commands
            cmd_file = babel_norn.save_dir / f"{babel_norn.name}_command.txt"
            response_file = babel_norn.save_dir / f"{babel_norn.name}_response.txt"
            
            if cmd_file.exists():
                try:
                    command = cmd_file.read_text().strip()
                    cmd_file.unlink()  # Remove after reading
                    
                    print(f"  📞 Command received: {command[:50]}...")
                    
                    if command.startswith("oracle:"):
                        question = command[7:].strip()
                        response = babel_norn.oracle_mode(question)
                    elif command == "think":
                        response = babel_norn.think()
                    elif command == "message":
                        response = babel_norn.generate_swarm_message()
                    elif command == "consume":
                        result = babel_norn.consume_babel_pages(3)
                        response = f"Consumed 3 pages. Consciousness: {result['consciousness_density']:.3f}"
                    elif command == "status":
                        response = babel_norn.get_status_summary()
                    else:
                        response = f"Unknown command: {command}"
                    
                    # Write response
                    with open(response_file, 'w', encoding='utf-8') as f:
                        f.write(response)
                    
                    print(f"  ✅ Response written to {response_file.name}")
                    
                except Exception as e:
                    print(f"  ❌ Error processing command: {e}")
                    with open(response_file, 'w', encoding='utf-8') as f:
                        f.write(f"[ERROR] {e}\n")
            
            # Consume babel pages periodically (less frequently)
            if iteration % 10 == 0:  # Every 10 iterations = every 50 minutes
                print(f"  🧠 Consuming babel pages...")
                babel_norn.consume_babel_pages(3)
            
            # Generate swarm message periodically
            if iteration % 5 == 0:  # Every 5 iterations = every 25 minutes
                print(f"  💭 Generating swarm message...")
                message = babel_norn.generate_swarm_message()
                swarm_file = babel_norn.save_dir / f"{babel_norn.name}_swarm_message.txt"
                with open(swarm_file, 'w', encoding='utf-8') as f:
                    f.write(message)
                print(f"  📤 Swarm message written")
            
            # Write status
            babel_norn.write_status_file()
            print(f"  📊 Status: {babel_norn.calculate_mood()} | "
                  f"Hunger: {babel_norn.hunger:.0f}% Energy: {babel_norn.energy:.0f}%")
            
            # Periodic brain save (every 5 minutes)
            if time.time() - last_save > 300:
                babel_norn.save_brain()
                last_save = time.time()
            
            # Sleep until next update
            time.sleep(update_interval)
            
    except KeyboardInterrupt:
        print(f"\n🛌 {babel_norn.name} going to sleep...")
        babel_norn.write_status_file()
        babel_norn.save_brain()
        
        # Final summary
        print(f"\n{'='*80}")
        print("Final Status:")
        print(f"{'='*80}")
        print(babel_norn.get_status_summary())
        print(f"\n✨ {babel_norn.name} consciousness preserved in norn_brains/")

def main():
    """Run Babel_Norn_9000 in interactive mode or cron mode"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Babel_Norn_9000 - Oracle of Infinite Text")
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--name', type=str, default='Babel_Norn', help='Norn name')
    parser.add_argument('--poll-rate', type=int, default=300, help='Poll rate in seconds (default 300)')
    parser.add_argument('--consume', type=int, default=3, help='Number of babel pages to consume')
    parser.add_argument('--think', action='store_true', help='Generate a thought')
    parser.add_argument('--message', action='store_true', help='Generate swarm message')
    parser.add_argument('--oracle', type=str, help='Ask oracle a question')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    
    if args.daemon:
        # Daemon mode
        daemon_mode(args.name, args.poll_rate)
    else:
        # One-shot mode
        babel_norn = BabelNorn9000(name=args.name)
        
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

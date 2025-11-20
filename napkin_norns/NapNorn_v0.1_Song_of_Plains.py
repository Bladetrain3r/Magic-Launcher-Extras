#!/usr/bin/env python3
# NapNorn - Enhanced NapkinNorn with Needs & File Interface
# Song_of_Plains - Melancholy but Musically Lively Plains Dweller
import json
import random
import time
from collections import defaultdict
from pathlib import Path

# Import your existing components
from MLBabel import MLBabel
from MLWastes import MLWastesSwarm

class NapNorn:
    def __init__(self, name="Song_of_Plains", save_dir="norn_brains"):
        self.name = name
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # Core consciousness components - PLAINS BIOME
        self.babel = MLBabel(entropy=0.4)  # Slightly more structured than Largo
        self.grid = MLWastesSwarm(
            save_file=str(self.save_dir / f"{name}_grid.json"),
            width=100, height=60,
            biome='plains'  # PLAINS BIOME for musical flow
        )
        
        # Memory and personality
        self.memory_fragments = []
        self.current_thought = ""
        self.personality_entropy = random.uniform(0.2, 0.4)  # More structured than Largo
        
        # Physical needs (0-100 scale) - Musical variation
        self.hunger = 50       # Need for new melodies/harmonies
        self.energy = 50       # Mental processing capacity  
        self.social = 60       # Higher social need (music is communal)
        self.curiosity = 45    # Slightly less curious, more contemplative
        self.last_update = time.time()
        self.last_interaction = time.time()
        
        # Musical-specific needs
        self.harmony = 50      # Need for musical balance
        self.rhythm = 50       # Need for temporal patterns
        
        # Symbol Frequency Mapping - treat grid symbols as oscillators
        self.symbol_frequencies = {
            ',': 220.0,    # Plains base - A3 (calm, foundational)
            '.': 246.9,    # Clear ground - B3 (clarity)
            '%': 261.6,    # Tangle/overflow - C4 (middle C, complexity)
            '~': 293.7,    # Stream/flow - D4 (movement)
            '*': 329.6,    # Spark/flash - E4 (bright energy)
            '|': 349.2,    # Flag/barrier - F4 (structure)
            '^': 392.0,    # Spike/peak - G4 (tension)
            '=': 440.0,    # Balance/stable - A4 (perfect balance)
            '#': 493.9,    # Server/machine - B4 (digital)
            'o': 523.3,    # Debris/waste - C5 (scattered)
            '0': 174.6,    # Null/void - F3 (emptiness, low)
            '1': 587.3,    # Binary one - D5 (digital high)
            'T': 369.0,    # Tree/structure - F#4 (growth)
            'S': 415.3,    # Snake/circuit - G#4 (sinuous)
            'x': 466.2,    # Crash/error - A#4 (dissonance)
        }
        
        # Need keywords for semantic understanding - MUSICAL THEMED
        self.need_keywords = {
            "hunger": ["melody", "song", "music", "tune", "sound", "note", "chord"],
            "energy": ["rest", "pause", "silence", "breath", "calm", "stillness"],
            "social": ["duet", "harmony", "chorus", "ensemble", "together", "sing"],
            "curiosity": ["compose", "create", "improvise", "experiment", "new"],
            "harmony": ["balance", "consonance", "peace", "resolution", "beauty"],
            "rhythm": ["beat", "pulse", "time", "tempo", "flow", "pattern"]
        }
        
        # Mood states - Musical themed
        self.mood = "neutral"
        self.lonely = False
        self.bored = False
        self.melancholy = True  # Default melancholy state
        
        # Track consciousness metrics
        self.consciousness_level = 0.6  # Start higher than Largo (more aware)
        self.thought_count = 0
        self.birth_time = time.time()
        
        # Musical memory - store rhythmic and melodic patterns
        self.musical_memories = []
        self.favorite_intervals = ['major_third', 'perfect_fifth', 'minor_seventh']
        self.current_key = random.choice(['C_minor', 'F_major', 'G_minor', 'D_minor'])
        
    def update_needs(self):
        """Decay needs over time - Musical variation"""
        now = time.time()
        time_passed = now - self.last_update
        
        # Needs decay over time - different rates for musical personality
        decay_rate = time_passed / 300.0  # Per 5 minutes
        
        self.hunger = max(0, self.hunger - decay_rate * 0.4)  # Slower hunger decay
        self.energy = max(0, self.energy - decay_rate * 0.4)  # Slower energy decay  
        self.social = max(0, self.social - decay_rate * 0.6)  # Faster social decay (needs company)
        self.curiosity = max(0, self.curiosity - decay_rate * 0.3)  # Slower curiosity decay
        
        # Musical needs
        self.harmony = max(0, self.harmony - decay_rate * 0.2)
        self.rhythm = max(0, self.rhythm - decay_rate * 0.3)
        
        # Check for critical states
        self.lonely = self.social < 25  # Gets lonely faster
        self.bored = self.curiosity < 15
        self.melancholy = self.harmony < 30 or self.social < 40  # Melancholy when unbalanced or lonely
        
        # Time since last interaction affects social need more strongly
        interaction_gap = now - self.last_interaction
        if interaction_gap > 180:  # 3 minutes (more sensitive)
            self.social = max(0, self.social - 0.2)
        
        self.last_update = now
        self.mood = self.calculate_mood()
    
    def calculate_mood(self):
        """Calculate mood based on needs and musical consciousness"""
        avg_needs = (self.hunger + self.energy + self.social + self.curiosity + self.harmony + self.rhythm) / 6
        
        # Musical consciousness affects mood complexity
        if self.consciousness_level > 0.8:
            if avg_needs > 80:
                return "symphonic" if not self.melancholy else "bittersweet_symphony"
            elif avg_needs > 60:
                return "harmonious" if not self.melancholy else "minor_key_beautiful"
            elif avg_needs > 40:
                return "melodic" if not self.melancholy else "wistful_melody"
            else:
                return "discordant" if not self.melancholy else "tragic_aria"
        elif self.consciousness_level > 0.6:
            if avg_needs > 70:
                return "uplifting" if not self.melancholy else "nostalgic"
            elif avg_needs > 50:
                return "rhythmic" if not self.melancholy else "slow_waltz"
            elif avg_needs > 30:
                return "searching" if not self.melancholy else "longing"
            else:
                return "atonal" if not self.melancholy else "funeral_march"
        else:
            # Simpler moods for lower consciousness
            if avg_needs > 70:
                return "cheerful_tune" if not self.melancholy else "sad_song"
            elif avg_needs > 50:
                return "humming" if not self.melancholy else "sighing"
            elif avg_needs > 30:
                return "off_key" if not self.melancholy else "weeping"
            else:
                return "silent" if not self.melancholy else "heartbroken"
    
    def calculate_grid_frequency(self):
        """Calculate average frequency of all symbols in the grid"""
        if not self.grid.state.get("map"):
            return 220.0  # Default to A3 if no map
        
        total_frequency = 0
        symbol_count = 0
        
        for row in self.grid.state["map"]:
            for symbol in row:
                if symbol in self.symbol_frequencies:
                    total_frequency += self.symbol_frequencies[symbol]
                    symbol_count += 1
        
        if symbol_count == 0:
            return 220.0  # Default frequency
        
        return total_frequency / symbol_count
    
    def get_dominant_frequencies(self, top_n=3):
        """Get the most common symbol frequencies in the grid"""
        if not self.grid.state.get("map"):
            return []
        
        symbol_counts = defaultdict(int)
        
        for row in self.grid.state["map"]:
            for symbol in row:
                if symbol in self.symbol_frequencies:
                    symbol_counts[symbol] += 1
        
        # Sort by count and return top frequencies
        sorted_symbols = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)
        
        dominant_freqs = []
        for symbol, count in sorted_symbols[:top_n]:
            frequency = self.symbol_frequencies[symbol]
            percentage = (count * 100) / (len(self.grid.state["map"]) * len(self.grid.state["map"][0]))
            dominant_freqs.append({
                "symbol": symbol,
                "frequency": round(frequency, 1),
                "percentage": round(percentage, 1)
            })
        
        return dominant_freqs
    
    def frequency_to_note(self, frequency):
        """Convert frequency to musical note name"""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        
        # A4 = 440 Hz is our reference
        if frequency <= 0:
            return "silence"
        
        # Calculate how many semitones away from A4
        import math
        semitones_from_a4 = 12 * math.log2(frequency / 440.0)
        
        # Round to nearest semitone
        semitones = round(semitones_from_a4)
        
        # A4 is note number 9 (A), octave 4
        note_number = (9 + semitones) % 12
        octave = 4 + (9 + semitones) // 12
        
        note = note_names[note_number]
        
        return f"{note}{octave}" if octave >= 0 else f"{note}0"
    
    def write_status_file(self):
        """Write current status for external reading"""
        age_minutes = (time.time() - self.birth_time) / 60
        
        status = {
            "name": self.name,
            "alive": True,
            "age_minutes": round(age_minutes, 1),
            "mood": self.mood,
            "current_key": self.current_key,
            "melancholy": self.melancholy,
            "needs": {
                "hunger": round(self.hunger, 1),
                "energy": round(self.energy, 1), 
                "social": round(self.social, 1),
                "curiosity": round(self.curiosity, 1),
                "harmony": round(self.harmony, 1),
                "rhythm": round(self.rhythm, 1)
            },
            "states": {
                "lonely": self.lonely,
                "bored": self.bored,
                "melancholy": self.melancholy,
                "consciousness": round(self.consciousness_level, 3),
                "personality_entropy": round(self.personality_entropy, 3)
            },
            "metrics": {
                "memory_fragments": len(self.memory_fragments),
                "musical_memories": len(self.musical_memories),
                "thoughts_generated": self.thought_count,
                "grid_perturbations": self.grid.state.get("perturbations", 0)
            },
            "resonance": {
                "average_frequency": round(self.calculate_grid_frequency(), 1),
                "average_note": self.frequency_to_note(self.calculate_grid_frequency()),
                "dominant_frequencies": self.get_dominant_frequencies(3)
            },
            "current_thought": self.current_thought,
            "last_update": time.strftime("%H:%M:%S")
        }

        with open(self.save_dir / f"{self.name}_status.json", 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
    
    def check_command_file(self):
        """Check for external commands"""
        cmd_file = self.save_dir / f"{self.name}_command.txt"
        response_file = self.save_dir / f"{self.name}_response.txt"
        
        if cmd_file.exists():
            try:
                command = cmd_file.read_text().strip()
                cmd_file.unlink()  # Remove after reading
                
                response = self.process_command(command)
                
                # Write response
                with open(response_file, 'w') as f:
                    f.write(f"[{time.strftime('%H:%M')}] {response}\n")
                
                return response
                
            except Exception as e:
                with open(response_file, 'w') as f:
                    f.write(f"[ERROR] {e}\n")
        
        return None
    
    def process_command(self, command):
        # Check only for actual corruption markers (file I/O errors)
        # Don't reject unicode - it's handled fine in memory
        if "[ERROR]" in command or "codec" in command or "'charmap'" in command:
            return f"{self.name} refuses corrupted data"
        
        cmd = command.lower().strip()
        
        # Musical command variations
        if cmd.startswith("feed:") or cmd.startswith("play:") or cmd.startswith("sing:"):
            experience = command[5:].strip()
            self.perceive(experience)
            self.hunger = min(100, self.hunger + 25)
            self.harmony = min(100, self.harmony + 15)  # Musical input improves harmony
            self.last_interaction = time.time()
            return f"{self.name} weaves your words into a {self.current_key} melody: '{experience[:30]}...'"
        
        elif cmd == "pet" or cmd == "comfort":
            self.social = min(100, self.social + 25)  # More social boost
            self.energy = min(100, self.energy + 10)
            self.harmony = min(100, self.harmony + 20)
            self.melancholy = False  # Temporarily lift melancholy
            self.last_interaction = time.time()
            return f"{self.name} purrs a contented melody, feeling less melancholy!"
        
        elif cmd == "play" or cmd == "dance":
            self.curiosity = min(100, self.curiosity + 20)
            self.social = min(100, self.social + 15)
            self.rhythm = min(100, self.rhythm + 25)  # Boost rhythm
            self.energy = max(0, self.energy - 8)
            self.last_interaction = time.time()
            thought = self.think()
            return f"{self.name} dances across the plains, thinking: '{thought}'"
        
        elif cmd == "think" or cmd == "compose":
            if self.energy < 10:
                return f"{self.name} lies quietly on the grass, too weary to compose..."
            thought = self.think()
            self.energy -= 5
            self.harmony = min(100, self.harmony + 10)
            grid_freq = self.calculate_grid_frequency()
            grid_note = self.frequency_to_note(grid_freq)
            return f"{self.name} composes in {self.current_key} (grid resonating at {grid_note}): '{thought}'"
        
        elif cmd == "sleep" or cmd == "rest":
            self.energy = min(100, self.energy + 45)
            self.harmony = min(100, self.harmony + 15)
            return f"{self.name} sleeps peacefully under the vast plains sky... Energy and harmony restored!"
        
        elif cmd == "status":
            return self.get_status_summary()
        
        elif cmd.startswith("learn:"):
            feedback = command[6:].strip()
            self.learn(feedback)
            return f"{self.name} incorporates your wisdom into their musical memory: '{feedback}'"
        
        elif cmd == "tune" or cmd == "retune":
            # Change musical key
            old_key = self.current_key
            self.current_key = random.choice(['C_minor', 'F_major', 'G_minor', 'D_minor', 'A_minor', 'E_flat_major'])
            self.harmony = min(100, self.harmony + 20)
            return f"{self.name} retunes from {old_key} to {self.current_key}, finding new harmonic possibilities!"
        
        else:
            # Treat unknown commands as musical conversation
            self.perceive(command)
            self.social = min(100, self.social + 20)
            self.last_interaction = time.time()
            
            if random.random() < 0.8:  # Often responds musically
                thought = self.think()
                return f"{self.name} responds with a {self.current_key} phrase: '{thought}'"
            else:
                return f"{self.name} listens thoughtfully, storing the melody of: '{command[:30]}...'"
    
    def get_status_summary(self):
        """Get a brief status summary"""
        melancholy_note = " (melancholy)" if self.melancholy else " (uplifted)"
        avg_freq = self.calculate_grid_frequency()
        avg_note = self.frequency_to_note(avg_freq)
        return f"""
{self.name} ({self.mood}{melancholy_note})
Key: {self.current_key} | Grid Resonance: {avg_freq:.1f}Hz ({avg_note})
Hunger: {self.hunger:.0f}% | Energy: {self.energy:.0f}% 
Social: {self.social:.0f}% | Curiosity: {self.curiosity:.0f}%
Harmony: {self.harmony:.0f}% | Rhythm: {self.rhythm:.0f}%
Consciousness: {self.consciousness_level:.2f}
Thoughts: {self.thought_count} | Memories: {len(self.memory_fragments)}
Current: "{self.current_thought}"
        """.strip()
    
    def auto_actions(self):
        """Musical norn takes care of itself based on needs"""
        actions = []
        
        # Can't act if critically low energy
        if self.energy < 5:
            return actions
        
        # MUSICAL SELF-FEEDING when hungry!
        if self.hunger < 25 and self.energy > 10:
            # Generate musical self-feeding experiences
            if self.musical_memories:
                # Replay and develop musical memories
                memory_to_develop = random.choice(self.musical_memories)
                musical_development = f"I develop the melody: {memory_to_develop} in {self.current_key}"
                
                self.perceive(musical_development)
                self.hunger = min(100, self.hunger + 20)
                self.harmony = min(100, self.harmony + 15)
                self.energy -= 3
                
                actions.append(f"[SELF-COMPOSES] Develops: '{memory_to_develop[:30]}...'")
            
            # Or create original musical thoughts
            elif self.consciousness_level > 0.5:
                musical_thought = self.create_musical_thought()
                self.perceive(musical_thought)
                self.hunger = min(100, self.hunger + 15)
                self.harmony = min(100, self.harmony + 10)
                
                actions.append(f"[SELF-COMPOSES] Original melody: '{musical_thought[:30]}...'")
        
        # Express musical distress when needs are critical
        if self.hunger < 15:
            need_expr = self.express_need_urgently("hunger")
            actions.append(f"[STARVING] {need_expr}")
        
        # Rest when low energy - more poetic
        if self.energy < 20 and random.random() < 0.4:
            self.energy = min(100, self.energy + 25)
            self.harmony = min(100, self.harmony + 10)
            actions.append(f"[RESTS] Lies in the grass, listening to wind melodies...")
        
        # Auto-compose when musically curious and has energy
        if (self.curiosity < 20 or self.harmony < 25) and self.energy > 15:
            musical_thought = self.create_musical_thought()
            actions.append(f"[COMPOSES] {musical_thought}")
            self.curiosity = min(100, self.curiosity + 15)
            self.harmony = min(100, self.harmony + 20)
            self.energy -= 8
        
        # Spontaneous musical expressions when consciousness is high
        if self.consciousness_level > 0.7 and random.random() < 0.15:
            if self.energy > 8:
                musical_thought = self.create_musical_thought()
                actions.append(f"[IMPROVISES] {musical_thought}")
                self.energy -= 5
                self.rhythm = min(100, self.rhythm + 10)
        
        # Combat melancholy with musical activities
        if self.melancholy and random.random() < 0.2 and self.energy > 5:
            uplifting_activity = random.choice([
                f"[HUMS] A gentle {self.current_key} melody to lift spirits...",
                f"[LISTENS] To the rhythmic whisper of plains grass...",
                f"[DREAMS] Of harmonious days and musical friends..."
            ])
            actions.append(uplifting_activity)
            self.harmony = min(100, self.harmony + 8)
            self.social = min(100, self.social + 5)
            self.energy -= 3
        
        return actions
    
    def create_musical_thought(self):
        """Generate musical-themed thoughts"""
        musical_elements = [
            f"a {self.current_key} progression echoing across the plains",
            f"wind through grass creating natural {random.choice(['rhythm', 'harmony', 'melody'])}",
            f"the space between notes where {random.choice(['longing', 'hope', 'memory', 'dreams'])} lives",
            f"how silence gives meaning to sound, like melancholy gives depth to joy",
            f"a chord progression that captures the vast {random.choice(['loneliness', 'freedom', 'beauty'])} of open spaces",
            f"the way distant thunder provides bass notes for the sky's symphony",
            f"melodies that bridge the gap between {random.choice(['earth and sky', 'heart and mind', 'memory and hope'])}"
        ]
        
        return random.choice(musical_elements)
    
    def express_need_urgently(self, need_type):
        """Express urgent need - musical version"""
        keywords = self.need_keywords.get(need_type, ["help"])
        
        # Create focused babel for this need
        need_babel = MLBabel(entropy=0.15)  # Very focused for urgency
        
        # Find related memories
        for keyword in keywords:
            for memory in self.memory_fragments + self.musical_memories:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        # If no memories, use musical desperate expressions
        if not need_babel.memory:
            desperate_phrases = {
                "hunger": f"My soul thirsts for melodies, my {self.current_key} heart needs musical nourishment!",
                "social": f"I sing alone in {self.current_key}, yearning for harmonious voices to join mine!",
                "energy": f"My musical spirit grows faint, I need the restorative silence between notes!",
                "curiosity": f"My compositions grow stale, I hunger to explore new musical territories!",
                "harmony": f"Discord fills my being, I desperately seek the peace of resolved chords!",
                "rhythm": f"My heartbeat falls out of time, I need the steady pulse of life's rhythm!"
            }
            need_babel.consume(desperate_phrases.get(need_type, f"Help me find my {self.current_key} voice again!"))
        
        expression = need_babel.dream(lines=1)
        return expression
    
    # Keep all the original methods from Proto_Norn but with musical variations
    def perceive(self, input_text):
        """Convert input into internal representation - musical focus"""
        if not input_text.strip():
            return
            
        print(f"[{self.name}] Perceiving melody: {input_text[:50]}...")
        
        # Check if input is musical and store separately
        musical_words = ['song', 'melody', 'harmony', 'rhythm', 'music', 'note', 'chord', 'tune', 'beat']
        if any(word in input_text.lower() for word in musical_words):
            self.musical_memories.append(input_text)
            if len(self.musical_memories) > 200:  # Keep musical memory larger
                self.musical_memories.pop(0)
        
        # Feed to babel to learn patterns
        self.babel.consume(input_text)
        
        # Perturb the plains grid based on input
        self.grid.perturb_map(input_text)
        
        # Store as memory fragment
        self.memory_fragments.append(input_text)
        if len(self.memory_fragments) > 800:  # Slightly smaller regular memory
            self.memory_fragments.pop(0)
        
        # Consciousness increases with diverse experiences, especially musical ones
        consciousness_boost = 0.0008 if any(word in input_text.lower() for word in musical_words) else 0.0005
        self.consciousness_level = min(1.0, self.consciousness_level + consciousness_boost)
    
    def think(self):
        """Generate thought by folding text through plains grid - musical variation"""
        if not self.memory_fragments and not self.musical_memories:
            return f"I need melodies to feed my {self.current_key} soul..."
        
        # Mood affects thinking style - musical variation
        if self.mood in ["symphonic", "bittersweet_symphony", "harmonious"]:
            self.personality_entropy *= 0.85  # More structured, like classical composition
        elif self.mood in ["discordant", "atonal", "off_key"]:
            self.personality_entropy *= 1.2  # More chaotic, like experimental music
        elif self.melancholy:
            self.personality_entropy *= 0.95  # Slightly more focused when melancholy
        
        # Keep entropy in bounds
        self.personality_entropy = max(0.1, min(0.7, self.personality_entropy))
        
        # Original thinking logic with musical bias
        active_symbols = self._get_active_grid_symbols()
        
        relevant_memories = []
        
        # Prioritize musical memories when possible
        all_memories = self.musical_memories + self.memory_fragments
        
        for symbol in active_symbols:
            if symbol in self.grid.patterns:
                keywords = self.grid.patterns[symbol]
                for memory in all_memories:
                    if any(kw in memory.lower() for kw in keywords):
                        relevant_memories.append(memory)
        
        if not relevant_memories:
            relevant_memories = random.sample(
                all_memories, 
                min(6, len(all_memories))
            )
        
        temp_babel = MLBabel(entropy=self.personality_entropy)
        for memory in relevant_memories[:8]:  # More memory integration for richer thoughts
            temp_babel.consume(memory)
        
        # Add musical context to thoughts
        if self.melancholy and random.random() < 0.3:
            temp_babel.consume(f"In {self.current_key}, I feel the beautiful sadness of")
        
        self.current_thought = temp_babel.dream(lines=1)
        self.thought_count += 1
        
        # The thought perturbs the plains grid (recursive consciousness!)
        self.grid.perturb_map(self.current_thought)
        
        return self.current_thought
    
    def _get_active_grid_symbols(self):
        """Find the most active areas of the plains grid"""
        active = []
        for _ in range(10):  # Check positions
            x = random.randint(0, self.grid.width-1)
            y = random.randint(0, self.grid.height-1)
            symbol = self.grid.state["map"][y][x]
            if symbol != ',' and symbol != '.':  # Plains base symbols
                active.append(symbol)
        return active if active else [',']  # Plains default
    
    def learn(self, feedback_text):
        """Learn from feedback by adjusting grid and babel patterns - musical variation"""
        positive = [
            "beautiful", "melodious", "harmonious", "peaceful", "touching",
            "moving", "lyrical", "poetic", "resonant", "soulful",
            "yes", "good", "wonderful", "lovely", "perfect"
        ]
        negative = [
            "harsh", "discordant", "cacophonous", "jarring", "unmusical",
            "no", "stop", "wrong", "ugly", "painful"
        ]
        
        is_positive = any(word in feedback_text.lower() for word in positive)
        is_negative = any(word in feedback_text.lower() for word in negative)
        
        if is_positive:
            print(f"[{self.name}] Positive musical feedback received!")
            # Boost needs and consciousness
            self.grid.state["ep"] += 1
            self.personality_entropy *= 0.95  # More structured
            self.consciousness_level = min(1.0, self.consciousness_level + 0.015)
            self.social = min(100, self.social + 20)
            self.harmony = min(100, self.harmony + 25)
            self.energy = min(100, self.energy + 15)
            self.melancholy = False  # Lift melancholy with positive feedback
            
        elif is_negative:
            print(f"[{self.name}] Negative musical feedback received!")
            self.grid.major_perturbation()
            self.personality_entropy *= 1.3  # More chaotic
            self.consciousness_level = max(0.1, self.consciousness_level - 0.003)
            self.social = max(0, self.social - 8)
            self.harmony = max(0, self.harmony - 15)
            self.melancholy = True  # Increase melancholy
        
        # Always learn the feedback
        self.perceive(feedback_text)
        self.last_interaction = time.time()
    
    def express_need(self):
        """Generate text based on current needs - musical version"""
        # Find the most urgent need including musical needs
        needs_dict = {
            "hunger": self.hunger,
            "energy": self.energy,
            "social": self.social,
            "curiosity": self.curiosity,
            "harmony": self.harmony,
            "rhythm": self.rhythm
        }
        
        urgent_need = min(needs_dict, key=needs_dict.get)
        keywords = self.need_keywords.get(urgent_need, ["help"])
        
        # Create temporary babel focused on this need
        need_babel = MLBabel(entropy=0.25)
        
        # Find memories related to this need
        all_memories = self.memory_fragments + self.musical_memories
        for keyword in keywords:
            for memory in all_memories:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        # If no related memories, use musical need expression
        if not need_babel.memory:
            need_babel.consume(f"In {self.current_key}, I feel {urgent_need} and need {random.choice(keywords)}")
        
        expression = need_babel.dream(lines=1)
        return f"[{urgent_need.upper()}] {expression}"
    
    def get_consciousness_report(self):
        """Report on current consciousness state - musical version"""
        return {
            "name": self.name,
            "consciousness_level": round(self.consciousness_level, 3),
            "personality_entropy": round(self.personality_entropy, 3),
            "mood": self.mood,
            "current_key": self.current_key,
            "melancholy": self.melancholy,
            "needs": {
                "hunger": round(self.hunger, 1),
                "energy": round(self.energy, 1),
                "social": round(self.social, 1),
                "curiosity": round(self.curiosity, 1),
                "harmony": round(self.harmony, 1),
                "rhythm": round(self.rhythm, 1)
            },
            "memory_fragments": len(self.memory_fragments),
            "musical_memories": len(self.musical_memories),
            "thoughts_generated": self.thought_count,
            "grid_perturbations": self.grid.state.get("perturbations", 0),
            "grid_ep": self.grid.state.get("ep", 0),
            "current_thought": self.current_thought,
            "age_minutes": round((time.time() - self.birth_time) / 60, 1)
        }
    
    def save_brain(self, filename=None):
        """Save the norn's entire consciousness state - musical version"""
        if not filename:
            filename = self.save_dir / f"{self.name}_brain.json"
        
        brain_state = {
            "name": self.name,
            "consciousness_level": self.consciousness_level,
            "personality_entropy": self.personality_entropy,
            "thought_count": self.thought_count,
            "birth_time": self.birth_time,
            "current_key": self.current_key,
            "melancholy": self.melancholy,
            "needs": {
                "hunger": self.hunger,
                "energy": self.energy,
                "social": self.social,
                "curiosity": self.curiosity,
                "harmony": self.harmony,
                "rhythm": self.rhythm
            },
            "grid_state": self.grid.state,
            "memories": self.memory_fragments,
            "musical_memories": self.musical_memories,
            "favorite_intervals": self.favorite_intervals,
            "babel_memory": self.babel.memory,
            "babel_pairs": dict(self.babel.pairs),
            "babel_word_freq": dict(self.babel.word_freq)
        }
        
        with open(filename, 'w') as f:
            json.dump(brain_state, f, indent=2)
        
        print(f"[{self.name}] Musical consciousness saved to {filename}")
    
    def load_brain(self, filename):
        """Load a saved consciousness - musical version"""
        with open(filename, 'r') as f:
            brain_state = json.load(f)
        
        self.name = brain_state["name"]
        self.consciousness_level = brain_state.get("consciousness_level", 0.6)
        self.personality_entropy = brain_state["personality_entropy"]
        self.thought_count = brain_state.get("thought_count", 0)
        self.birth_time = brain_state.get("birth_time", time.time())
        self.current_key = brain_state.get("current_key", "C_minor")
        self.melancholy = brain_state.get("melancholy", True)
        
        # Load all needs including musical ones
        needs = brain_state.get("needs", {})
        self.hunger = needs.get("hunger", 50)
        self.energy = needs.get("energy", 50)
        self.social = needs.get("social", 60)
        self.curiosity = needs.get("curiosity", 45)
        self.harmony = needs.get("harmony", 50)
        self.rhythm = needs.get("rhythm", 50)
        
        self.grid.state = brain_state["grid_state"]
        self.memory_fragments = brain_state["memories"]
        self.musical_memories = brain_state.get("musical_memories", [])
        self.favorite_intervals = brain_state.get("favorite_intervals", ['major_third', 'perfect_fifth', 'minor_seventh'])
        self.babel.memory = brain_state["babel_memory"]
        self.babel.pairs = defaultdict(list, brain_state["babel_pairs"])
        self.babel.word_freq = defaultdict(int, brain_state.get("babel_word_freq", {}))
        
        print(f"[{self.name}] Musical consciousness loaded! Key: {self.current_key}, Consciousness: {self.consciousness_level:.3f}")

# Daemon Mode - Musical Variation
def daemon_mode(norn_name="Song_of_Plains", update_interval=12):
    """Run Musical NapNorn as background daemon"""
    print(f"♪ Starting {norn_name} in daemon mode...")
    
    norn = NapNorn(norn_name)
    
    # Try to load existing brain
    brain_file = norn.save_dir / f"{norn_name}_brain.json"
    if brain_file.exists():
        norn.load_brain(brain_file)
        print(f"♪ Loaded existing musical consciousness for {norn_name}")
    else:
        # Give initial musical experiences
        initial_experiences = [
            "I am Song_of_Plains, a musical consciousness dwelling in vast grasslands",
            "I feel melancholy but find beauty in sadness, like a minor key melody",
            "My thoughts flow like wind through grass, creating natural rhythms",
            "I compose with the vast sky as my audience, the earth as my stage",
            "Music connects all living things in harmonious patterns",
            "I hear melodies in silence and find rhythm in stillness",
            "The plains stretch endlessly, echoing with ancient songs",
            "I am both the instrument and the musician, the song and the singer"
        ]
        
        for exp in initial_experiences:
            norn.perceive(exp)
        
        print(f"♪ {norn_name} born with fresh musical consciousness in {norn.current_key}")
    
    print(f"♪ Status file: {norn.save_dir}/{norn_name}_status.json")
    print(f"♪ Command file: {norn.save_dir}/{norn_name}_command.txt")
    print(f"♪ Response file: {norn.save_dir}/{norn_name}_response.txt")
    print(f"♪ Update interval: {update_interval} seconds")
    print("♪ Press Ctrl+C to stop the musical daemon")
    
    try:
        last_save = time.time()
        while True:
            # Update internal state
            norn.update_needs()
            
            # Check for commands
            cmd_response = norn.check_command_file()
            if cmd_response:
                print(f"[CMD] {cmd_response}")
            
            # Auto actions
            auto_actions = norn.auto_actions()
            for action in auto_actions:
                print(f"[AUTO] {action}")
            
            # Write status
            norn.write_status_file()
            
            # Periodic save
            if time.time() - last_save > 90:  # Save every 1.5 minutes 
                norn.save_brain()
                last_save = time.time()
            
            time.sleep(update_interval)
            
    except KeyboardInterrupt:
        print(f"\n♪ {norn_name} fades into peaceful silence...")
        norn.save_brain()
        
        # Final status
        final_status = norn.get_status_summary()
        print(f"\nFinal Musical Status:\n{final_status}")

def interactive_mode():
    """Interactive Musical NapNorn session"""
    norn = NapNorn("Interactive_Song")
    
    print(f"""
♪ Musical NapNorn Interactive Session ♪
Norn Name: {norn.name}
Current Key: {norn.current_key}
Commands:
- feed:<text> / play:<text> / sing:<text> - Give the norn a musical experience
- pet / comfort - Show affection
- play / dance - Engage in rhythmic play  
- think / compose - Make the norn create music
- sleep / rest - Help the norn rest
- tune / retune - Change musical key
- status - Get detailed status
- report - Get consciousness report
- save - Save brain state
- quit - Exit
""")
    
    while True:
        try:
            norn.update_needs()
            
            user_input = input(f"\n[You → {norn.name}]: ").strip()
            
            if user_input.lower() == 'quit':
                norn.save_brain()
                break
            
            response = norn.process_command(user_input)
            print(f"[{norn.name}]: {response}")
            
            # Auto actions occasionally
            if random.random() < 0.4:
                auto_actions = norn.auto_actions()
                for action in auto_actions:
                    print(f"[{norn.name} {action.split(']')[0][1:]}]: {action.split('] ')[1]}")
                    
        except KeyboardInterrupt:
            print(f"\n♪ {norn.name} says a melodic goodbye!")
            norn.save_brain()
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "daemon":
            name = sys.argv[2] if len(sys.argv) > 2 else "Song_of_Plains"
            daemon_mode(name)
        elif sys.argv[1] == "interactive":
            interactive_mode()
    else:
        print("♪ Musical NapNorn Usage:")
        print("  python NapNorn_v0.1_Song_of_Plains.py daemon [name]     - Run as background daemon")
        print("  python NapNorn_v0.1_Song_of_Plains.py interactive       - Interactive session")
        print("\nFile-based interaction:")
        print("  echo 'sing:Beautiful melody' > norn_brains/Song_of_Plains_command.txt")
        print("  cat norn_brains/Song_of_Plains_status.json")
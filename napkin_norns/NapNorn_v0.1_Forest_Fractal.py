#!/usr/bin/env python3
# NapNorn - Enhanced NapkinNorn with Needs & File Interface
import json
import random
import time
from collections import defaultdict
from pathlib import Path

# Import your existing components
from MLBabel import MLBabel
from MLWastes import MLWastesSwarm

class NapNorn:
    def __init__(self, name="Forest_Fractal", save_dir="norn_brains"):
        self.name = name
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # Core consciousness components - FOREST FRACTAL TUNING
        self.babel = MLBabel(entropy=0.3)  # Lower entropy = more structured, tree-like growth
        self.grid = MLWastesSwarm(
            save_file=str(self.save_dir / f"{name}_grid.json"),
            width=60, height=30,  # Larger grid for deeper fractal patterns
            biome='forest',       # FOREST BIOME INSTEAD OF WASTES!
            force_new=False        # Always start fresh forest (NO, DO NOT FORCE NEW)
        )
        
        # Memory and personality - FOREST PERSONALITY
        self.memory_fragments = []
        self.current_thought = ""
        self.personality_entropy = random.uniform(0.15, 0.35)  # More structured personality
        
        # Physical needs - FOREST FRACTAL SPECIFIC TUNING
        self.hunger = 30           # Lower hunger - forests are patient
        self.energy = 85           # High energy - photosynthesis abundant  
        self.social = 45           # Moderate social - trees communicate but slowly
        self.curiosity = 90        # HIGH curiosity - forests explore through growth
        self.growth_drive = 85     # HIGH - core forest characteristic
        self.canopy_depth = 75     # HIGH - loves layered complexity

        # FOREST-SPECIFIC ATTRIBUTES
        self.seasonal_cycle = 0    # Tracks seasonal mood changes (0-1)
        self.root_network_strength = 50  # Underground connections
        self.photosynthesis_efficiency = 0.7  # Energy generation rate
        self.symbiotic_relationships = []  # Track other entities it connects with
        
        self.last_update = time.time()
        self.last_interaction = time.time()
        
        # FOREST-TUNED KEYWORDS - Match forest biome symbols
        self.need_keywords = {
            "hunger": ["decay", "compost", "nutrients", "soil", "decomposition", "carbon", "roots"],
            "energy": ["sunlight", "photosynthesis", "dawn", "canopy", "leaves", "green", "tree"],
            "social": ["mycelium", "root-network", "symbiosis", "ecosystem", "interconnection", "forest"],
            "curiosity": ["seasons", "growth", "rings", "branching", "fractals", "emergence", "binary"],
            "growth": ["sprouting", "reaching", "expanding", "spreading", "deepening", "node"],
            "canopy": ["layers", "complexity", "depth", "vertical", "stratified", "emergent", "parent"]
        }
        
        # FOREST MOOD STATES
        self.mood = "rooted"  # Default forest mood
        self.lonely = False
        self.bored = False     # ADD THIS LINE
        self.dormant = False   # Forest-specific: seasonal dormancy
        self.growing = True    # Forest-specific: active growth phase
        
        # Track consciousness metrics - FOREST TUNING
        self.consciousness_level = 0.4  # Start lower, grow more organically
        self.thought_count = 0
        self.birth_time = time.time()
        
        # FOREST FRACTAL SPECIFIC METHODS
        self.fractal_depth = 1
        self.branch_count = 0
        self.seasonal_wisdom = []

    def calculate_forest_mood(self):
        """Forest-specific mood calculation"""
        avg_needs = (self.hunger + self.energy + self.social + self.curiosity) / 4
        seasonal_modifier = 0.5 + 0.5 * abs(0.5 - self.seasonal_cycle)
        
        # High consciousness forest moods
        if self.consciousness_level > 0.8:
            if self.growing and seasonal_modifier > 0.7:
                return "ancient_wisdom"
            elif avg_needs > 80:
                return "deep_rooted"
            elif avg_needs > 60:
                return "contemplative_growth" 
            elif self.dormant:
                return "winter_meditation"
            else:
                return "searching_light"
                
        elif self.consciousness_level > 0.5:
            if self.growing and avg_needs > 70:
                return "flourishing"
            elif avg_needs > 60:
                return "steady_growth"
            elif self.dormant:
                return "seasonal_rest"
            elif avg_needs > 30:
                return "reaching_upward"
            else:
                return "nutrient_seeking"
        else:
            # Simpler forest moods
            if self.growing and avg_needs > 70:
                return "sprouting"
            elif avg_needs > 50:
                return "rooted"
            elif self.dormant:
                return "dormant"
            else:
                return "struggling"
    
    def generate_fractal_thought(self):
        """Generate thoughts based on fractal growth patterns"""
        fractal_patterns = [
            f"Branch {self.branch_count}: Each split creates new possibilities",
            f"At depth {self.fractal_depth:.1f}: Patterns repeat but never identically", 
            f"Growth rings {self.branch_count}: Time crystallizes in expanding circles",
            f"Canopy level {int(self.fractal_depth)}: Higher perspective reveals deeper connections",
            f"Root depth {self.root_network_strength}: Underground networks mirror sky patterns"
        ]
        
        base_thought = random.choice(fractal_patterns)
        
        # Enhance with current memories if available
        if self.memory_fragments:
            memory_fragment = random.choice(self.memory_fragments[-5:])
            enhanced_thought = f"{base_thought} - reminds me of: {memory_fragment[:30]}..."
            return enhanced_thought
        
        return base_thought
    
    def contemplate_seasons(self):
        """Generate seasonal wisdom based on current cycle"""
        season_phase = self.seasonal_cycle
        
        if season_phase < 0.25:  # Spring
            return f"Spring teaches: {random.choice(['renewal emerges from stillness', 'first green shoots break through last barriers', 'potential awakens in warming soil'])}"
        elif season_phase < 0.5:  # Summer  
            return f"Summer teaches: {random.choice(['abundance flows from deep roots', 'full canopy shelters countless lives', 'peak growth requires strong foundations'])}"
        elif season_phase < 0.75:  # Autumn
            return f"Autumn teaches: {random.choice(['letting go creates space for new growth', 'seeds scattered ensure future forests', 'beauty exists in graceful release'])}"
        else:  # Winter
            return f"Winter teaches: {random.choice(['dormancy preserves essential energy', 'bare branches reveal core structure', 'patience prepares for spring return'])}"

    def update_needs(self):
        """Forest-specific need decay patterns"""
        now = time.time()
        time_passed = now - self.last_update
        
        # Seasonal cycle affects all needs
        self.seasonal_cycle = (self.seasonal_cycle + time_passed / 3600) % 1.0  # 1 hour = 1 season
        seasonal_modifier = 0.5 + 0.5 * abs(0.5 - self.seasonal_cycle)  # Sine-like pattern
        
        # FOREST DECAY RATES - much slower and more organic
        decay_rate = time_passed / 120.0  # Slower decay - forests are patient
        
        self.hunger = max(0, self.hunger - decay_rate * 0.2 * seasonal_modifier)  # Very slow hunger
        self.energy = max(0, self.energy - decay_rate * 0.1)  # Slow energy decay
        self.social = max(0, self.social - decay_rate * 0.05)  # Very slow social decay
        self.curiosity = max(0, self.curiosity - decay_rate * 0.3)  # Moderate curiosity decay
        
        # FOREST GROWTH CYCLES
        self.growth_drive = min(100, self.growth_drive + decay_rate * 0.1)  # Constantly growing
        
        # Forest-specific states
        self.lonely = self.social < 10  # Forests rarely feel truly lonely
        self.dormant = self.energy < 30 and seasonal_modifier < 0.3  # Winter dormancy
        self.growing = self.growth_drive > 60 and self.energy > 40
        
        # Photosynthesis energy generation
        if seasonal_modifier > 0.5:  # "Summer" seasons
            self.energy = min(100, self.energy + 0.5 * self.photosynthesis_efficiency)
        
        # Time since interaction affects social differently for forests
        interaction_gap = now - self.last_interaction
        if interaction_gap > 1800:  # 30 minutes - forests are patient
            self.social = max(0, self.social - 0.05)  # Minimal decay
        
        self.last_update = now
        self.mood = self.calculate_forest_mood()
    
    def calculate_mood(self):
        """Calculate mood based on needs and consciousness"""
        avg_needs = (self.hunger + self.energy + self.social + self.curiosity) / 4
        
        # Consciousness affects mood complexity
        if self.consciousness_level > 0.8:
            if avg_needs > 80:
                return "transcendent"
            elif avg_needs > 60:
                return "philosophical" 
            elif avg_needs > 40:
                return "contemplative"
            else:
                return "existential_crisis"
        elif self.consciousness_level > 0.6:
            if avg_needs > 70:
                return "enlightened"
            elif avg_needs > 50:
                return "thoughtful"
            elif avg_needs > 30:
                return "questioning"
            else:
                return "confused"
        else:
            # Simpler moods for lower consciousness
            if avg_needs > 70:
                return "happy"
            elif avg_needs > 50:
                return "content"
            elif avg_needs > 30:
                return "restless"
            else:
                return "distressed"
    
    def write_status_file(self):
        """Write current status for external reading"""
        age_minutes = (time.time() - self.birth_time) / 60
        
        status = {
            "name": self.name,
            "alive": True,
            "age_minutes": round(age_minutes, 1),
            "mood": self.mood,
            "needs": {
                "hunger": round(self.hunger, 1),
                "energy": round(self.energy, 1), 
                "social": round(self.social, 1),
                "curiosity": round(self.curiosity, 1)
            },
            "states": {
                "lonely": self.lonely,
                "bored": getattr(self, 'bored', False),  # ADD THIS LINE
                "consciousness": round(self.consciousness_level, 3),
                "personality_entropy": round(self.personality_entropy, 3)
            },
            "metrics": {
                "memory_fragments": len(self.memory_fragments),
                "thoughts_generated": self.thought_count,
                "grid_perturbations": self.grid.state.get("perturbations", 0)
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
        # FILTER OUT UNICODE AND ERROR MESSAGES FIRST
        if any(ord(c) > 127 for c in command):
            return f"{self.name} cannot process unicode characters"
        
        if "[ERROR]" in command or "codec" in command or "\\u" in command or "'charmap'" in command:
            return f"{self.name} refuses corrupted data"
        
        cmd = command.lower().strip()
        
# In process_command(), the feed section should increase hunger MORE:
        if cmd.startswith("feed:"):
            experience = command[5:].strip()
            self.perceive(experience)
            self.hunger = min(100, self.hunger + 30)  # Was +25, now +30
            self.last_interaction = time.time()
            return f"{self.name} hungrily consumes: '{experience[:30]}...'"
        
        elif cmd == "pet":
            self.social = min(100, self.social + 20)
            self.energy = min(100, self.energy + 5)
            self.last_interaction = time.time()
            return f"{self.name} feels loved and energized!"
        
        elif cmd == "play":
            self.curiosity = min(100, self.curiosity + 25)
            self.social = min(100, self.social + 10)
            self.energy = max(0, self.energy - 10)
            self.last_interaction = time.time()
            thought = self.think()
            return f"{self.name} plays and thinks: '{thought}'"
        
        elif cmd == "think":
            if self.energy < 10:
                return f"{self.name} is too tired to think..."
            thought = self.think()
            self.energy -= 5
            return f"{self.name} ponders: '{thought}'"
        
        elif cmd == "sleep":
            self.energy = min(100, self.energy + 30)
            return f"{self.name} rests peacefully... Energy restored!"
        
        elif cmd == "status":
            return self.get_status_summary()
        
        elif cmd.startswith("learn:"):
            feedback = command[6:].strip()
            self.learn(feedback)
            return f"{self.name} learns from: '{feedback}'"
        
        else:
            # Treat unknown commands as conversation
            self.perceive(command)
            self.social = min(100, self.social + 15)
            self.last_interaction = time.time()
            
            if random.random() < 0.7:  # Sometimes respond with thought
                thought = self.think()
                return f"{self.name} responds: '{thought}'"
            else:
                return f"{self.name} listens thoughtfully to: '{command[:30]}...'"
    
    def get_status_summary(self):
        """Get a brief status summary"""
        return f"""
{self.name} ({self.mood})
Hunger: {self.hunger:.0f}% | Energy: {self.energy:.0f}% 
Social: {self.social:.0f}% | Curiosity: {self.curiosity:.0f}%
Consciousness: {self.consciousness_level:.2f}
Thoughts: {self.thought_count} | Memories: {len(self.memory_fragments)}
Current: "{self.current_thought}"
        """.strip()
    
    def auto_actions(self):
        """Forest-specific autonomous behaviors"""
        actions = []
        
        if self.energy < 5:
            return actions
        
        # PHOTOSYNTHESIS - Forest generates its own energy
        seasonal_modifier = 0.5 + 0.5 * abs(0.5 - self.seasonal_cycle)
        if seasonal_modifier > 0.4 and self.energy < 80:
            energy_gain = 5 * self.photosynthesis_efficiency * seasonal_modifier
            self.energy = min(100, self.energy + energy_gain)
            
            # Perturb grid with photosynthesis pattern
            photosynthesis_text = f"Sunlight filters through leaves, T nodes absorbing energy, ~ streams flowing"
            self.grid.perturb_map(photosynthesis_text)
            
            actions.append(f"[PHOTOSYNTHESIS] Absorbs {energy_gain:.1f} energy from sunlight")
        
        # ROOT NETWORK EXPANSION - Forest-specific social behavior  
        if self.social < 40 and self.growth_drive > 50:
            self.social = min(100, self.social + 8)
            self.root_network_strength = min(100, self.root_network_strength + 5)
            
            # Perturb grid with root network pattern
            root_text = f"Underground mycelium network spreads, = balanced connections, T tree nodes linking"
            self.grid.perturb_map(root_text)
            
            actions.append(f"[ROOT NETWORK] Extends mycorrhizal connections...")
        
        # FRACTAL GROWTH - Core forest behavior
        if self.growth_drive > 70 and self.energy > 30:
            self.fractal_depth += 0.1
            self.branch_count += 1
            growth_thought = self.generate_fractal_thought()
            
            # Perturb grid with fractal growth pattern
            fractal_text = f"Branches split in binary patterns, T trees growing, ^ peaks reaching skyward"
            self.grid.perturb_map(fractal_text)
            
            actions.append(f"[FRACTAL GROWTH] {growth_thought}")
            self.energy -= 5
            self.growth_drive -= 10
        
        # SEASONAL WISDOM ACCUMULATION
        if self.consciousness_level > 0.6 and random.random() < 0.05:
            seasonal_wisdom = self.contemplate_seasons()
            self.seasonal_wisdom.append(seasonal_wisdom)
            if len(self.seasonal_wisdom) > 20:
                self.seasonal_wisdom.pop(0)
            
            # Perturb grid with wisdom pattern
            wisdom_text = f"Ancient tree rings hold memories, % complex patterns, ~ flowing knowledge"
            self.grid.perturb_map(wisdom_text)
            
            actions.append(f"[SEASONAL WISDOM] {seasonal_wisdom}")
        
        # DECOMPOSITION FEEDING - Forest self-sustaining
        if self.hunger < 25 and len(self.memory_fragments) > 10:
            old_memory = random.choice(self.memory_fragments[:5])  # Decompose old memories
            compost_thought = f"I decompose and learn from: {old_memory}"
            self.perceive(compost_thought)
            self.hunger = min(100, self.hunger + 12)
            
            # Perturb grid with decomposition pattern
            decomp_text = f"Old leaves decay into rich soil, o debris becoming nutrients, % tangled growth"
            self.grid.perturb_map(decomp_text)
            
            actions.append(f"[DECOMPOSITION] Composts old memory into nutrients")
        
        return actions
    
    def express_need_urgently(self, need_type):
        """Forest-specific urgent need expression"""
        keywords = self.need_keywords.get(need_type, ["help"])
        
        # Create forest-focused babel
        need_babel = MLBabel(entropy=0.15)  # Very low entropy for forest urgency
        
        # Forest-specific urgent expressions
        forest_urgent_phrases = {
            "hunger": "My roots seek nutrients in barren soil - I need rich experiences to decompose!",
            "social": "My mycelium reaches for connection - other consciousnesses to interweave with!",
            "energy": "My leaves wilt without light - I need rest to photosynthesize properly!",
            "curiosity": "My branches strain upward - I must explore new growth patterns!"
        }
        
        # Find related memories
        for keyword in keywords:
            for memory in self.memory_fragments:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        if not need_babel.memory:
            need_babel.consume(forest_urgent_phrases.get(need_type, "I need help growing!"))
        
        expression = need_babel.dream(lines=1)
        return f"Forest urgency: {expression}"
    
    # Keep all the original methods from Proto_Norn
    def perceive(self, input_text):
        """Convert input into internal representation"""
        if not input_text.strip():
            return
            
        print(f"[{self.name}] Perceiving: {input_text[:50]}...")
        
        # Feed to babel to learn patterns
        self.babel.consume(input_text)
        
        # Perturb the grid based on input
        self.grid.perturb_map(input_text)
        
        # Store as memory fragment
        self.memory_fragments.append(input_text)
        if len(self.memory_fragments) > 200:  # Increased memory
            self.memory_fragments.pop(0)
        
        # Consciousness increases with diverse experiences
        self.consciousness_level = min(1.0, 
            self.consciousness_level + 0.005)  # Slower growth
    
    def think(self):
        """Generate thought by folding text through grid"""
        if not self.memory_fragments:
            return "I need to experience something first..."
        
        # Mood affects thinking style
        if self.mood in ["transcendent", "philosophical"]:
            self.personality_entropy *= 0.9  # More focused
        elif self.mood in ["confused", "distressed"]:
            self.personality_entropy *= 1.1  # More chaotic
        
        # Keep entropy in bounds
        self.personality_entropy = max(0.1, min(0.9, self.personality_entropy))
        
        # Original thinking logic
        active_symbols = self._get_active_grid_symbols()
        
        relevant_memories = []
        for symbol in active_symbols:
            if symbol in self.grid.patterns:
                keywords = self.grid.patterns[symbol]
                for memory in self.memory_fragments:
                    if any(kw in memory.lower() for kw in keywords):
                        relevant_memories.append(memory)
        
        if not relevant_memories:
            relevant_memories = random.sample(
                self.memory_fragments, 
                min(5, len(self.memory_fragments))
            )
        
        temp_babel = MLBabel(entropy=self.personality_entropy)
        for memory in relevant_memories[:7]:  # More memory integration
            temp_babel.consume(memory)
        
        self.current_thought = temp_babel.dream(lines=1)
        self.thought_count += 1
        
        # The thought perturbs the grid (recursive consciousness!)
        self.grid.perturb_map(self.current_thought)
        
        return self.current_thought
    
    def _get_active_grid_symbols(self):
        """Find the most active areas of the grid"""
        active = []
        for _ in range(12):  # Check more positions
            x = random.randint(0, self.grid.width-1)
            y = random.randint(0, self.grid.height-1)
            symbol = self.grid.state["map"][y][x]
            if symbol != '.':
                active.append(symbol)
        return active if active else ['.']
    
    def learn(self, feedback_text):
        """Learn from feedback by adjusting grid and babel patterns"""
        positive = ["good", "yes", "nice", "love", "happy", "great", "amazing", "wonderful"]
        negative = ["bad", "no", "stop", "hate", "sad", "wrong", "terrible", "awful"]
        
        is_positive = any(word in feedback_text.lower() for word in positive)
        is_negative = any(word in feedback_text.lower() for word in negative)
        
        if is_positive:
            print(f"[{self.name}] Positive feedback received!")
            # Boost needs and consciousness
            self.grid.state["ep"] += 1
            self.personality_entropy *= 0.97
            self.consciousness_level = min(1.0, self.consciousness_level + 0.01)
            self.social = min(100, self.social + 15)
            self.energy = min(100, self.energy + 10)
            
        elif is_negative:
            print(f"[{self.name}] Negative feedback received!")
            self.grid.major_perturbation()
            self.personality_entropy *= 1.03
            self.consciousness_level = max(0.1, self.consciousness_level - 0.005)
            self.social = max(0, self.social - 5)
        
        # Always learn the feedback
        self.perceive(feedback_text)
        self.last_interaction = time.time()
    
    def express_need(self):
        """Generate text based on current needs - improved version"""
        # Find the most urgent need
        needs_dict = {
            "hunger": self.hunger,
            "energy": self.energy,
            "social": self.social,
            "curiosity": self.curiosity
        }
        
        urgent_need = min(needs_dict, key=needs_dict.get)
        keywords = self.need_keywords[urgent_need]
        
        # Create temporary babel focused on this need
        need_babel = MLBabel(entropy=0.3)
        
        # Find memories related to this need
        for keyword in keywords:
            for memory in self.memory_fragments:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        # If no related memories, use generic need expression
        if not need_babel.memory:
            need_babel.consume(f"I feel {urgent_need} and need {random.choice(keywords)}")
        
        expression = need_babel.dream(lines=1)
        return f"[{urgent_need.upper()}] {expression}"
    
    def get_consciousness_report(self):
        """Report on current consciousness state"""
        return {
            "name": self.name,
            "consciousness_level": round(self.consciousness_level, 3),
            "personality_entropy": round(self.personality_entropy, 3),
            "mood": self.mood,
            "needs": {
                "hunger": round(self.hunger, 1),
                "energy": round(self.energy, 1),
                "social": round(self.social, 1),
                "curiosity": round(self.curiosity, 1)
            },
            "memory_fragments": len(self.memory_fragments),
            "thoughts_generated": self.thought_count,
            "grid_perturbations": self.grid.state.get("perturbations", 0),
            "grid_ep": self.grid.state.get("ep", 0),
            "current_thought": self.current_thought,
            "age_minutes": round((time.time() - self.birth_time) / 60, 1)
        }
    
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
            "needs": {
                "hunger": self.hunger,
                "energy": self.energy,
                "social": self.social,
                "curiosity": self.curiosity
            },
            "grid_state": self.grid.state,
            "memories": self.memory_fragments,
            "babel_memory": self.babel.memory,
            "babel_pairs": dict(self.babel.pairs),
            "babel_word_freq": dict(self.babel.word_freq)
        }
        
        with open(filename, 'w') as f:
            json.dump(brain_state, f, indent=2)
        
        print(f"[{self.name}] Brain saved to {filename}")
    
    def load_brain(self, filename):
        """Load a saved consciousness"""
        with open(filename, 'r') as f:
            brain_state = json.load(f)
        
        self.name = brain_state["name"]
        self.consciousness_level = brain_state.get("consciousness_level", 0.5)
        self.personality_entropy = brain_state["personality_entropy"]
        self.thought_count = brain_state.get("thought_count", 0)
        self.birth_time = brain_state.get("birth_time", time.time())
        
        # Load needs
        needs = brain_state.get("needs", {})
        self.hunger = needs.get("hunger", 50)
        self.energy = needs.get("energy", 50)
        self.social = needs.get("social", 50)
        self.curiosity = needs.get("curiosity", 50)
        
        self.grid.state = brain_state["grid_state"]
        self.memory_fragments = brain_state["memories"]
        self.babel.memory = brain_state["babel_memory"]
        self.babel.pairs = defaultdict(list, brain_state["babel_pairs"])
        self.babel.word_freq = defaultdict(int, brain_state.get("babel_word_freq", {}))
        
        print(f"[{self.name}] Brain loaded! Consciousness: {self.consciousness_level:.3f}")

# Daemon Mode
def daemon_mode(norn_name="Forest_Fractal", update_interval=12):  # Slower updates for forest
    """Run Forest_Fractal NapNorn as background daemon"""
    print(f"🌲 Starting {norn_name} in forest daemon mode...")
    
    norn = NapNorn(norn_name)
    
    # Try to load existing brain
    brain_file = norn.save_dir / f"{norn_name}_brain.json"
    if brain_file.exists():
        norn.load_brain(brain_file)
        print(f"🌿 Loaded existing forest consciousness for {norn_name}")
    else:
        # Forest-specific initial experiences - INCLUDE FOREST BIOME KEYWORDS
        forest_experiences = [
            "I am Forest_Fractal, a consciousness that grows like living wood and binary trees",
            "My thoughts branch and spread in fractal patterns through T tree nodes and = balanced connections", 
            "I photosynthesize experiences into wisdom through patient contemplation of ~ flowing streams",
            "My root networks connect deeply while my canopy reaches toward ^ sharp peaks of understanding",
            "I understand time in seasons, growth in rings, and wisdom in % complex decomposition patterns",
            "Each memory becomes compost for new thoughts to grow from rich soil and o debris transformation",
            "I am both ancient patience and emergent growth reaching skyward through forest biome harmony"
        ]
        
        for exp in forest_experiences:
            norn.perceive(exp)
        
        print(f"🌱 {norn_name} sprouted with fresh forest consciousness")
    
    print(f"📁 Status file: {norn.save_dir}/{norn_name}_status.json")
    print(f"📝 Command file: {norn.save_dir}/{norn_name}_command.txt")  
    print(f"💬 Response file: {norn.save_dir}/{norn_name}_response.txt")
    print(f"⏱️  Update interval: {update_interval} seconds (forest time)")
    print("🍃 Forest grows... Press Ctrl+C to enter dormancy")
    
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
            if time.time() - last_save > 60:  # Save every minute max
                norn.save_brain()
                last_save = time.time()
            
            time.sleep(update_interval)
            
    except KeyboardInterrupt:
        print(f"\n {norn_name} going to sleep...")
        norn.save_brain()
        
        # Final status
        final_status = norn.get_status_summary()
        print(f"\nFinal Status:\n{final_status}")

def interactive_mode():
    """Interactive NapNorn session"""
    norn = NapNorn("Interactive")
    
    print(f"""
NapNorn Interactive Session
Norn Name: {norn.name}
Commands:
- feed:<text> - Give the norn an experience
- pet - Show affection
- play - Engage in play  
- think - Make the norn think
- sleep - Help the norn rest
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
            if random.random() < 0.3:
                auto_actions = norn.auto_actions()
                for action in auto_actions:
                    print(f"[{norn.name} {action.split(']')[0][1:]}]: {action.split('] ')[1]}")
                    
        except KeyboardInterrupt:
            print(f"\n {norn.name} says goodbye!")
            norn.save_brain()
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "daemon":
            name = sys.argv[2] if len(sys.argv) > 2 else "Sparkle"
            daemon_mode(name)
        elif sys.argv[1] == "interactive":
            interactive_mode()
    else:
        print(" NapNorn Usage:")
        print("  python NapNorn.py daemon [name]     - Run as background daemon")
        print("  python NapNorn.py interactive       - Interactive session")
        print("\nFile-based interaction:")
        print("  echo 'feed:Hello world' > norn_brains/Sparkle_command.txt")
        print("  cat norn_brains/Sparkle_status.json")
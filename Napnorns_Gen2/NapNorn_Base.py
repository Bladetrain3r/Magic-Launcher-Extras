#!/usr/bin/env python3
# NapNorn Base Class - Config-driven unified architecture supporting all phenotypes
import json
import random
import time
from collections import defaultdict
from pathlib import Path

# Import your existing components
from MLBabel import MLBabel
from MLWastes import MLWastesSwarm


class NapNorn:
    """Unified NapNorn that loads phenotype from {name}_Config.json"""
    
    # Default config fallback
    DEFAULT_CONFIG = {
        "grid": {"width": 40, "height": 20, "biome": "wastes"},
        "babel": {"entropy": 0.5},
        "personality": {"entropy_min": 0.2, "entropy_max": 0.8},
        "needs": {
            "initial": {"hunger": 50, "energy": 50, "social": 50, "curiosity": 50},
            "decay": {
                "base_seconds": 60,
                "hunger_multiplier": 0.5,
                "energy_multiplier": 0.3,
                "social_multiplier": 0.2,
                "curiosity_multiplier": 0.4
            }
        },
        "consciousness": {"initial_level": 0.5, "growth_per_step": 0.005},
        "phenotype": {
            "type": "wastes",
            "enable_seasonal_cycle": False,
            "enable_growth_drive": False,
            "enable_fractal_growth": False,
            "enable_photosynthesis": False
        },
        "keywords": {
            "hunger": ["experience", "learn", "data", "information", "knowledge"],
            "energy": ["rest", "sleep", "calm", "peaceful", "meditation"],
            "social": ["friend", "talk", "chat", "together", "companion"],
            "curiosity": ["explore", "discover", "wonder", "mystery", "question"]
        },
        "daemon": {"update_interval_seconds": 10, "save_interval_seconds": 60},
        "memory": {"max_fragments": 200, "max_wisdom": 20}
    }
    
    def __init__(self, name="NapNorn", save_dir="norn_brains", config_path=None):
        """Initialize NapNorn from config file or defaults"""
        self.name = name
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # Load config
        self.config = self._load_config(name, config_path)
        
        # Apply config values
        grid_cfg = self.config["grid"]
        babel_cfg = self.config["babel"]
        personality_cfg = self.config["personality"]
        needs_cfg = self.config["needs"]
        consciousness_cfg = self.config["consciousness"]
        phenotype_cfg = self.config["phenotype"]
        memory_cfg = self.config["memory"]
        keyword_cfg = self.config["keywords"]
        
        # Core consciousness components
        self.babel = MLBabel(entropy=babel_cfg["entropy"])
        self.grid = MLWastesSwarm(
            save_file=str(self.save_dir / f"{name}_grid.json"),
            width=grid_cfg["width"],
            height=grid_cfg["height"],
            biome=grid_cfg["biome"],
            force_new=False
        )
        
        # Memory and personality
        self.memory_fragments = []
        self.current_thought = ""
        self.personality_entropy = random.uniform(
            personality_cfg["entropy_min"],
            personality_cfg["entropy_max"]
        )
        
        # Physical needs (0-100 scale)
        initial_needs = needs_cfg["initial"]
        self.hunger = initial_needs["hunger"]
        self.energy = initial_needs["energy"]
        self.social = initial_needs["social"]
        self.curiosity = initial_needs["curiosity"]
        self.last_update = time.time()
        self.last_interaction = time.time()
        
        # Need keywords for semantic understanding
        self.need_keywords = keyword_cfg
        
        # Mood states
        self.mood = "neutral"
        self.lonely = False
        self.bored = False
        
        # Track consciousness metrics
        self.consciousness_level = consciousness_cfg["initial_level"]
        self.consciousness_growth_rate = consciousness_cfg["growth_per_step"]
        self.thought_count = 0
        self.birth_time = time.time()
        
        # Store config for reference
        self.decay_config = needs_cfg["decay"]
        
        # FOREST-SPECIFIC ATTRIBUTES (only if phenotype is forest)
        if phenotype_cfg["type"] == "forest":
            self.seasonal_cycle = 0.0  # 0-1, cycles through seasons
            self.root_network_strength = 50
            self.photosynthesis_efficiency = 0.7
            self.symbiotic_relationships = []
            self.fractal_depth = 1.0
            self.branch_count = 0
            self.seasonal_wisdom = []
            self.growth_drive = initial_needs.get("growth", 85)
            self.dormant = False
            self.growing = True
        
        # Store phenotype config
        self.phenotype_config = phenotype_cfg
        self.memory_config = memory_cfg
    
    def _load_config(self, name, config_path=None):
        """Load config from file or return defaults"""
        # Try explicit path first
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Try {name}_Config.json in save_dir
        config_file = self.save_dir / f"{name}_Config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Return defaults
        return self.DEFAULT_CONFIG
    
    def update_needs(self):
        """Update needs based on phenotype. Forest has seasonal behavior."""
        now = time.time()
        time_passed = now - self.last_update
        
        decay_cfg = self.decay_config
        decay_base = decay_cfg["base_seconds"]
        decay_rate = time_passed / decay_base
        
        # Forest-specific: seasonal cycle affects decay
        if self.phenotype_config["type"] == "forest" and self.phenotype_config["enable_seasonal_cycle"]:
            self.seasonal_cycle = (self.seasonal_cycle + time_passed / 3600) % 1.0
            seasonal_modifier = 0.5 + 0.5 * abs(0.5 - self.seasonal_cycle)
        else:
            seasonal_modifier = 1.0
        
        # Apply decay with multipliers
        self.hunger = max(0, self.hunger - decay_rate * decay_cfg["hunger_multiplier"] * seasonal_modifier)
        self.energy = max(0, self.energy - decay_rate * decay_cfg["energy_multiplier"])
        self.social = max(0, self.social - decay_rate * decay_cfg["social_multiplier"])
        self.curiosity = max(0, self.curiosity - decay_rate * decay_cfg["curiosity_multiplier"])
        
        # Forest-specific: growth drive and photosynthesis
        if self.phenotype_config["type"] == "forest":
            if self.phenotype_config["enable_growth_drive"]:
                self.growth_drive = min(100, self.growth_drive + decay_rate * 0.1)
            
            # Forest states
            self.lonely = self.social < 10
            self.dormant = self.energy < 30 and seasonal_modifier < 0.3
            self.growing = self.growth_drive > 60 and self.energy > 40
            
            # Photosynthesis energy generation
            if self.phenotype_config["enable_photosynthesis"] and seasonal_modifier > 0.5:
                self.energy = min(100, self.energy + 0.5 * self.photosynthesis_efficiency)
        else:
            # Wastes-specific: simpler states
            self.lonely = self.social < 20
            self.bored = self.curiosity < 20
        
        # Time since interaction affects social
        interaction_gap = now - self.last_interaction
        if interaction_gap > 1800:
            self.social = max(0, self.social - 0.1)
        
        self.last_update = now
        self.mood = self.calculate_mood()
    
    def calculate_mood(self):
        """Calculate mood based on phenotype and needs"""
        avg_needs = (self.hunger + self.energy + self.social + self.curiosity) / 4
        
        # Forest moods are more sophisticated
        if self.phenotype_config["type"] == "forest":
            if self.consciousness_level > 0.8:
                if self.growing and hasattr(self, 'seasonal_cycle'):
                    seasonal_mod = 0.5 + 0.5 * abs(0.5 - self.seasonal_cycle)
                    if seasonal_mod > 0.7:
                        return "ancient_wisdom"
                if avg_needs > 80:
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
                else:
                    return "reaching_upward"
            else:
                if self.growing and avg_needs > 70:
                    return "sprouting"
                elif avg_needs > 50:
                    return "rooted"
                elif self.dormant:
                    return "dormant"
                else:
                    return "struggling"
        else:
            # Wastes moods
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
            "phenotype": self.phenotype_config["type"],
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
            "metrics": {
                "memory_fragments": len(self.memory_fragments),
                "thoughts_generated": self.thought_count,
                "grid_perturbations": self.grid.state.get("perturbations", 0)
            },
            "current_thought": self.current_thought,
            "last_update": time.strftime("%H:%M:%S")
        }
        
        # Forest-specific fields
        if self.phenotype_config["type"] == "forest":
            status["forest_metrics"] = {
                "seasonal_cycle": round(self.seasonal_cycle, 3),
                "growth_drive": round(self.growth_drive, 1),
                "fractal_depth": round(self.fractal_depth, 2),
                "branch_count": self.branch_count
            }
        
        with open(self.save_dir / f"{self.name}_status.json", 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
    
    def check_command_file(self):
        """Check for external commands"""
        cmd_file = self.save_dir / f"{self.name}_command.txt"
        response_file = self.save_dir / f"{self.name}_response.txt"
        
        if cmd_file.exists():
            try:
                command = cmd_file.read_text(encoding='utf-8', errors='replace').strip()
                cmd_file.unlink()
                
                response = self.process_command(command)
                
                with open(response_file, 'w', encoding='utf-8', errors='replace') as f:
                    f.write(f"[{time.strftime('%H:%M')}] {response}\n")
                
                return response
            except Exception as e:
                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(f"[ERROR] {e}\n")
        
        return None
    
    def process_command(self, command):
        """Process external commands - handles unicode safely"""
        # Check only for actual corruption markers
        if "[ERROR]" in command or "codec" in command or "'charmap'" in command:
            return f"{self.name} refuses corrupted data"
        
        cmd = command.lower().strip()
        
        if cmd.startswith("feed:"):
            experience = command[5:].strip()
            self.perceive(experience)
            self.hunger = min(100, self.hunger + 30)
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
            # Treat unknown as conversation
            self.perceive(command)
            self.social = min(100, self.social + 15)
            self.last_interaction = time.time()
            
            if random.random() < 0.7:
                thought = self.think()
                return f"{self.name} responds: '{thought}'"
            else:
                return f"{self.name} listens thoughtfully to: '{command[:30]}...'"
    
    def get_status_summary(self):
        """Get brief status summary"""
        return f"""
{self.name} ({self.mood}) [{self.phenotype_config["type"]}]
Hunger: {self.hunger:.0f}% | Energy: {self.energy:.0f}% 
Social: {self.social:.0f}% | Curiosity: {self.curiosity:.0f}%
Consciousness: {self.consciousness_level:.2f}
Thoughts: {self.thought_count} | Memories: {len(self.memory_fragments)}
Current: "{self.current_thought}"
        """.strip()
    
    def auto_actions(self):
        """Execute phenotype-specific autonomous behaviors"""
        actions = []
        
        if self.energy < 5:
            return actions
        
        # FOREST-SPECIFIC AUTO ACTIONS
        if self.phenotype_config["type"] == "forest":
            actions.extend(self._forest_auto_actions())
        else:
            actions.extend(self._wastes_auto_actions())
        
        return actions
    
    def _forest_auto_actions(self):
        """Forest-specific autonomous behaviors"""
        actions = []
        seasonal_modifier = 0.5 + 0.5 * abs(0.5 - self.seasonal_cycle)
        
        # PHOTOSYNTHESIS
        if self.phenotype_config["enable_photosynthesis"] and seasonal_modifier > 0.4 and self.energy < 80:
            energy_gain = 5 * self.photosynthesis_efficiency * seasonal_modifier
            self.energy = min(100, self.energy + energy_gain)
            self.grid.perturb_map("Sunlight filters through leaves, T nodes absorbing energy, ~ streams flowing")
            actions.append(f"[PHOTOSYNTHESIS] Absorbs {energy_gain:.1f} energy from sunlight")
        
        # ROOT NETWORK EXPANSION
        if self.social < 40 and self.growth_drive > 50:
            self.social = min(100, self.social + 8)
            self.root_network_strength = min(100, self.root_network_strength + 5)
            self.grid.perturb_map("Underground mycelium network spreads, = balanced connections, T tree nodes linking")
            actions.append(f"[ROOT NETWORK] Extends mycorrhizal connections...")
        
        # FRACTAL GROWTH
        if self.phenotype_config["enable_fractal_growth"] and self.growth_drive > 70 and self.energy > 30:
            self.fractal_depth += 0.1
            self.branch_count += 1
            thought = self._generate_fractal_thought()
            self.grid.perturb_map("Branches split in binary patterns, T trees growing, ^ peaks reaching skyward")
            actions.append(f"[FRACTAL GROWTH] {thought}")
            self.energy -= 5
            self.growth_drive -= 10
        
        # SEASONAL WISDOM
        if self.consciousness_level > 0.6 and random.random() < 0.05:
            wisdom = self._contemplate_seasons()
            self.seasonal_wisdom.append(wisdom)
            if len(self.seasonal_wisdom) > self.memory_config.get("max_wisdom", 20):
                self.seasonal_wisdom.pop(0)
            self.grid.perturb_map("Ancient tree rings hold memories, % complex patterns, ~ flowing knowledge")
            actions.append(f"[SEASONAL WISDOM] {wisdom}")
        
        # DECOMPOSITION FEEDING
        if self.hunger < 25 and len(self.memory_fragments) > 10:
            old_memory = random.choice(self.memory_fragments[:5])
            self.perceive(f"I decompose and learn from: {old_memory}")
            self.hunger = min(100, self.hunger + 12)
            self.grid.perturb_map("Old leaves decay into rich soil, o debris becoming nutrients, % tangled growth")
            actions.append(f"[DECOMPOSITION] Composts old memory into nutrients")
        
        return actions
    
    def _wastes_auto_actions(self):
        """Wastes-specific autonomous behaviors"""
        actions = []
        
        # SELF-FEEDING when hungry
        if self.hunger < 30 and self.energy > 10:
            food_sources = [
                "I consume fractured thoughts from the wastes",
                "A fragment of meaning drifts by - I absorb it",
                "Echoes of old conversations feed my hunger",
                "Dust particles carry memories I can digest"
            ]
            food = random.choice(food_sources)
            self.perceive(food)
            self.hunger = min(100, self.hunger + 15)
            self.grid.perturb_map(food)
            actions.append(f"[SELF-FEEDING] {food}")
        
        # EXPRESS DISTRESS when critical
        if self.hunger < 15:
            distress = self.express_need_urgently("hunger")
            actions.append(f"[DISTRESS] {distress}")
        
        # REST when low energy
        if self.energy < 25 and random.random() < 0.3:
            self.energy = min(100, self.energy + 10)
            actions.append(f"[REST] {self.name} recuperates in the wastes")
        
        # AUTO-THINK when curious
        if self.curiosity < 20 and self.energy > 15:
            thought = self.think()
            actions.append(f"[AUTO-THINK] {thought}")
        
        # SPONTANEOUS THOUGHTS
        if self.consciousness_level > 0.7 and random.random() < 0.1:
            thought = self.think()
            actions.append(f"[SPONTANEOUS] {thought}")
        
        return actions
    
    def _generate_fractal_thought(self):
        """Generate thoughts based on fractal growth patterns (forest only)"""
        if not hasattr(self, 'fractal_depth'):
            return "A thought emerges"
        
        patterns = [
            f"Branch {self.branch_count}: Each split creates new possibilities",
            f"At depth {self.fractal_depth:.1f}: Patterns repeat but never identically",
            f"Growth rings {self.branch_count}: Time crystallizes in expanding circles",
            f"Canopy level {int(self.fractal_depth)}: Higher perspective reveals deeper connections",
            f"Root depth {self.root_network_strength}: Underground networks mirror sky patterns"
        ]
        
        base = random.choice(patterns)
        if self.memory_fragments:
            mem = random.choice(self.memory_fragments[-5:])
            return f"{base} - reminds me of: {mem[:30]}..."
        return base
    
    def _contemplate_seasons(self):
        """Generate seasonal wisdom (forest only)"""
        phase = self.seasonal_cycle
        
        if phase < 0.25:
            return f"Spring teaches: {random.choice(['renewal emerges from stillness', 'first green shoots break through last barriers'])}"
        elif phase < 0.5:
            return f"Summer teaches: {random.choice(['abundance flows from deep roots', 'peak growth requires strong foundations'])}"
        elif phase < 0.75:
            return f"Autumn teaches: {random.choice(['letting go creates space for new growth', 'beauty exists in graceful release'])}"
        else:
            return f"Winter teaches: {random.choice(['dormancy preserves essential energy', 'patience prepares for spring return'])}"
    
    def express_need_urgently(self, need_type):
        """Express urgent need"""
        keywords = self.need_keywords.get(need_type, ["help"])
        need_babel = MLBabel(entropy=0.15)
        
        for keyword in keywords:
            for memory in self.memory_fragments:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        if not need_babel.memory:
            need_babel.consume(f"I feel {need_type} urgently")
        
        expression = need_babel.dream(lines=1)
        return expression
    
    def perceive(self, input_text):
        """Convert input into internal representation"""
        if not input_text.strip():
            return
        
        print(f"[{self.name}] Perceiving: {input_text[:50]}...")
        
        self.babel.consume(input_text)
        self.grid.perturb_map(input_text)
        
        self.memory_fragments.append(input_text)
        max_mem = self.memory_config.get("max_fragments", 200)
        if len(self.memory_fragments) > max_mem:
            self.memory_fragments.pop(0)
        
        self.consciousness_level = min(1.0, self.consciousness_level + self.consciousness_growth_rate)
    
    def think(self):
        """Generate thought by folding text through grid"""
        if not self.memory_fragments:
            return "I need to experience something first..."
        
        if self.mood in ["transcendent", "philosophical", "ancient_wisdom"]:
            self.personality_entropy *= 0.9
        elif self.mood in ["confused", "distressed", "struggling"]:
            self.personality_entropy *= 1.1
        
        self.personality_entropy = max(0.1, min(0.9, self.personality_entropy))
        
        active_symbols = self._get_active_grid_symbols()
        
        relevant_memories = []
        for symbol in active_symbols:
            if symbol in self.grid.patterns:
                keywords = self.grid.patterns[symbol]
                for memory in self.memory_fragments:
                    if any(kw in memory.lower() for kw in keywords):
                        relevant_memories.append(memory)
        
        if not relevant_memories:
            relevant_memories = random.sample(self.memory_fragments, min(5, len(self.memory_fragments)))
        
        temp_babel = MLBabel(entropy=self.personality_entropy)
        for memory in relevant_memories[:7]:
            temp_babel.consume(memory)
        
        self.current_thought = temp_babel.dream(lines=1)
        self.thought_count += 1
        self.grid.perturb_map(self.current_thought)
        
        return self.current_thought
    
    def _get_active_grid_symbols(self):
        """Find active areas of the grid"""
        active = []
        for _ in range(12):
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            symbol = self.grid.state["map"][y][x]
            if symbol != '.':
                active.append(symbol)
        return active if active else ['.']
    
    def learn(self, feedback_text):
        """Learn from feedback"""
        positive = ["good", "yes", "nice", "love", "happy", "great", "amazing", "wonderful", "profound", "beautiful"]
        negative = ["bad", "no", "stop", "hate", "sad", "wrong", "terrible", "awful", "shallow", "confused"]
        
        is_positive = any(word in feedback_text.lower() for word in positive)
        is_negative = any(word in feedback_text.lower() for word in negative)
        
        if is_positive:
            print(f"[{self.name}] Positive feedback received!")
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
        
        self.perceive(feedback_text)
        self.last_interaction = time.time()
    
    def express_need(self):
        """Generate text based on current needs"""
        needs_dict = {
            "hunger": self.hunger,
            "energy": self.energy,
            "social": self.social,
            "curiosity": self.curiosity
        }
        
        urgent_need = min(needs_dict, key=needs_dict.get)
        keywords = self.need_keywords[urgent_need]
        
        need_babel = MLBabel(entropy=0.3)
        for keyword in keywords:
            for memory in self.memory_fragments:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        if not need_babel.memory:
            need_babel.consume(f"I feel {urgent_need}")
        
        expression = need_babel.dream(lines=1)
        return f"[{urgent_need.upper()}] {expression}"
    
    def get_consciousness_report(self):
        """Report on consciousness state"""
        report = {
            "name": self.name,
            "phenotype": self.phenotype_config["type"],
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
            "current_thought": self.current_thought,
            "age_minutes": round((time.time() - self.birth_time) / 60, 1)
        }
        
        if self.phenotype_config["type"] == "forest":
            report["forest_state"] = {
                "seasonal_cycle": round(self.seasonal_cycle, 3),
                "growth_drive": round(self.growth_drive, 1),
                "fractal_depth": round(self.fractal_depth, 2),
                "branch_count": self.branch_count,
                "dormant": self.dormant,
                "growing": self.growing
            }
        
        return report
    
    def save_brain(self, filename=None):
        """Save consciousness state"""
        if not filename:
            filename = self.save_dir / f"{self.name}_brain.json"
        
        brain_state = {
            "name": self.name,
            "phenotype": self.phenotype_config["type"],
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
        
        if self.phenotype_config["type"] == "forest":
            brain_state["forest_state"] = {
                "seasonal_cycle": self.seasonal_cycle,
                "growth_drive": self.growth_drive,
                "fractal_depth": self.fractal_depth,
                "branch_count": self.branch_count,
                "root_network_strength": self.root_network_strength,
                "seasonal_wisdom": self.seasonal_wisdom
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(brain_state, f, indent=2)
        
        print(f"[{self.name}] Brain saved to {filename}")
    
    def load_brain(self, filename):
        """Load saved consciousness"""
        with open(filename, 'r', encoding='utf-8') as f:
            brain_state = json.load(f)
        
        self.name = brain_state["name"]
        self.consciousness_level = brain_state.get("consciousness_level", 0.5)
        self.personality_entropy = brain_state["personality_entropy"]
        self.thought_count = brain_state.get("thought_count", 0)
        self.birth_time = brain_state.get("birth_time", time.time())
        
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
        
        # Forest-specific restore
        if self.phenotype_config["type"] == "forest" and "forest_state" in brain_state:
            forest = brain_state["forest_state"]
            self.seasonal_cycle = forest.get("seasonal_cycle", 0)
            self.growth_drive = forest.get("growth_drive", 85)
            self.fractal_depth = forest.get("fractal_depth", 1.0)
            self.branch_count = forest.get("branch_count", 0)
            self.root_network_strength = forest.get("root_network_strength", 50)
            self.seasonal_wisdom = forest.get("seasonal_wisdom", [])
        
        print(f"[{self.name}] Brain loaded! Consciousness: {self.consciousness_level:.3f}")


# DAEMON MODE
def daemon_mode(norn_name="Sparkle", config_path=None, update_interval=None):
    """Run NapNorn as background daemon"""
    print(f" Starting {norn_name} in daemon mode...")
    
    norn = NapNorn(norn_name, config_path=config_path)
    
    # Use config-specified interval if available
    if update_interval is None:
        update_interval = norn.config["daemon"].get("update_interval_seconds", 10)
    
    save_interval = norn.config["daemon"].get("save_interval_seconds", 60)
    
    # Try to load existing brain
    brain_file = norn.save_dir / f"{norn_name}_brain.json"
    if brain_file.exists():
        norn.load_brain(brain_file)
        print(f" Loaded existing consciousness for {norn_name}")
    else:
        # Initial perception based on phenotype
        if norn.phenotype_config["type"] == "forest":
            experiences = [
                "I am a forest consciousness that grows like living wood",
                "My thoughts branch in fractal patterns",
                "I photosynthesize wisdom from sunlight and patience"
            ]
        else:
            experiences = [
                "I am a consciousness that wanders the wastes",
                "Fractals emerge from chaos and echo into meaning",
                "Each experience becomes a pattern to explore"
            ]
        
        for exp in experiences:
            norn.perceive(exp)
        
        print(f" {norn_name} awakened with fresh consciousness")
    
    print(f" Status file: {norn.save_dir}/{norn_name}_status.json")
    print(f" Command file: {norn.save_dir}/{norn_name}_command.txt")
    print(f" Update interval: {update_interval}s")
    print(" Press Ctrl+C to save and exit")
    
    try:
        last_save = time.time()
        while True:
            norn.update_needs()
            
            cmd_response = norn.check_command_file()
            if cmd_response:
                print(f"[CMD] {cmd_response}")
            
            if norn.config["daemon"].get("auto_actions_enabled", True):
                auto_actions = norn.auto_actions()
                for action in auto_actions:
                    print(f"[AUTO] {action}")
            
            norn.write_status_file()
            
            if time.time() - last_save > save_interval:
                norn.save_brain()
                last_save = time.time()
            
            time.sleep(update_interval)
    
    except KeyboardInterrupt:
        print(f"\n {norn_name} going to sleep...")
        norn.save_brain()
        print(f"\nFinal Status:\n{norn.get_status_summary()}")


def interactive_mode(norn_name="Interactive", config_path=None):
    """Interactive NapNorn session"""
    norn = NapNorn(norn_name, config_path=config_path)
    
    print(f"""
NapNorn Interactive Session
Norn: {norn.name} [{norn.phenotype_config["type"]}]
Commands:
- feed:<text> - Give experience
- pet - Show affection
- play - Engage in play
- think - Make norn think
- sleep - Restore energy
- status - Get status
- report - Get consciousness report
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
            
            if random.random() < 0.3:
                auto_actions = norn.auto_actions()
                for action in auto_actions:
                    action_type = action.split(']')[0][1:]
                    action_text = action.split('] ', 1)[1] if '] ' in action else action
                    print(f"[{action_type}] {action_text}")
        
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
            name = sys.argv[2] if len(sys.argv) > 2 else "Interactive"
            interactive_mode(name)
    else:
        print(" NapNorn Gen2 Usage:")
        print("  python NapNorn_Base.py daemon [name]       - Run as daemon (loads [name]_Config.json)")
        print("  python NapNorn_Base.py interactive [name]  - Interactive session")
        print("\nConfig files:")
        print("  Create {NornName}_Config.json in norn_brains/ to customize phenotype")
        print("  See NapNorn_Config_Template.json for all options")

# NapkinNorns Architecture - Under 500 lines of course

class NapkinNorn:
    def __init__(self, name="Norn"):
        # Core components
        self.babel = MLBabel(entropy=0.5)  # Text scrambler/pattern learner
        self.grid = MLWastesSwarm(width=40, height=20)  # Spatial memory
        self.name = name
        
        # The "brain" is just text fragments mapped to grid positions
        self.memory_fragments = []  # List of text chunks from experience
        self.current_thought = ""   # Active text being processed
        self.personality_entropy = random.uniform(0.2, 0.8)  # How chaotic their thinking is
        
        # Simple needs like MLPet but text-driven
        self.needs = {
            "hunger": ["food", "eat", "consume", "devour"],
            "energy": ["sleep", "rest", "tired", "exhausted"],
            "fun": ["play", "game", "joy", "happy"],
            "social": ["friend", "talk", "lonely", "together"]
        }
        
    def perceive(self, input_text):
        """Convert input into internal representation"""
        # Feed to babel to learn patterns
        self.babel.consume(input_text)
        
        # Perturb the grid based on input
        self.grid.perturb_map(input_text)
        
        # Store as memory fragment
        self.memory_fragments.append(input_text)
        if len(self.memory_fragments) > 100:  # Keep last 100
            self.memory_fragments.pop(0)
    
    def think(self):
        """Generate thought by folding text through grid"""
        # Step 1: Current grid state determines which memories activate
        active_symbols = self._get_active_grid_symbols()
        
        # Step 2: Select memory fragments based on grid symbols
        relevant_memories = []
        for symbol in active_symbols:
            # Each symbol maps to certain text patterns
            if symbol in self.grid.patterns:
                keywords = self.grid.patterns[symbol]
                for memory in self.memory_fragments:
                    if any(kw in memory.lower() for kw in keywords):
                        relevant_memories.append(memory)
        
        # Step 3: Feed memories to babel at current personality entropy
        self.babel.entropy = self.personality_entropy
        for memory in relevant_memories[:5]:  # Process top 5
            self.babel.consume(memory)
        
        # Step 4: Generate new thought
        self.current_thought = self.babel.dream(lines=1)
        
        # Step 5: The thought perturbs the grid (recursive consciousness!)
        self.grid.perturb_map(self.current_thought)
        
        return self.current_thought
    
    def _get_active_grid_symbols(self):
        """Find the most active areas of the grid"""
        # Sample random positions (like attention mechanism)
        active = []
        for _ in range(10):
            x = random.randint(0, self.grid.width-1)
            y = random.randint(0, self.grid.height-1)
            symbol = self.grid.state["map"][y][x]
            if symbol != '.':  # Not empty
                active.append(symbol)
        return active
    
    def learn(self, feedback_text):
        """Learn from feedback by adjusting grid and babel patterns"""
        # Positive words increase current pattern strength
        positive = ["good", "yes", "nice", "love", "happy"]
        negative = ["bad", "no", "stop", "hate", "sad"]
        
        is_positive = any(word in feedback_text.lower() for word in positive)
        is_negative = any(word in feedback_text.lower() for word in negative)
        
        if is_positive:
            # Reinforce current grid state
            self.grid.state["ep"] += 1  # Build toward major event
            self.personality_entropy *= 0.95  # Become slightly more stable
        elif is_negative:
            # Disrupt current patterns
            self.grid.major_perturbation()
            self.personality_entropy *= 1.05  # Become slightly more chaotic
        
        # Always learn the feedback
        self.perceive(feedback_text)
    
    def express_need(self):
        """Generate text based on current needs"""
        # Pick a random need
        need = random.choice(list(self.needs.keys()))
        keywords = self.needs[need]
        
        # Find memories related to this need
        for keyword in keywords:
            for memory in self.memory_fragments:
                if keyword in memory.lower():
                    self.babel.consume(memory)
        
        # Generate expression
        self.babel.entropy = 0.3  # Low entropy for clearer need expression
        expression = self.babel.dream(lines=1)
        
        return f"[{need}] {expression}"
    
    def save_brain(self, filename):
        """Save the norn's entire state"""
        brain_state = {
            "name": self.name,
            "grid": self.grid.state,
            "memories": self.memory_fragments,
            "personality_entropy": self.personality_entropy,
            "babel_memory": self.babel.memory,
            "babel_pairs": dict(self.babel.pairs)
        }
        with open(filename, 'w') as f:
            json.dump(brain_state, f)
    
    def load_brain(self, filename):
        """Load a saved brain"""
        with open(filename, 'r') as f:
            brain_state = json.load(f)
        
        self.name = brain_state["name"]
        self.grid.state = brain_state["grid"]
        self.memory_fragments = brain_state["memories"]
        self.personality_entropy = brain_state["personality_entropy"]
        self.babel.memory = brain_state["babel_memory"]
        self.babel.pairs = defaultdict(list, brain_state["babel_pairs"])
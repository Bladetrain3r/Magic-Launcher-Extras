#!/usr/bin/env python3
# NapkinNorns - Complete Working Implementation
import json
import random
from collections import defaultdict
from pathlib import Path

# Import your existing components
from MLBabel import MLBabel
from MLWastes import MLWastesSwarm

class NapkinNorn:
    def __init__(self, name="Norn", save_dir="norn_brains"):
        self.name = name
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        
        # Core consciousness components
        self.babel = MLBabel(entropy=0.5)
        self.grid = MLWastesSwarm(
            save_file=str(self.save_dir / f"{name}_grid.json"),
            width=40, height=20
        )
        
        # Memory and personality
        self.memory_fragments = []
        self.current_thought = ""
        self.personality_entropy = random.uniform(0.2, 0.8)
        
        # Consciousness needs (text-driven like you wanted)
        self.needs = {
            "hunger": ["food", "eat", "consume", "devour", "hungry"],
            "energy": ["sleep", "rest", "tired", "exhausted", "energy"],
            "fun": ["play", "game", "joy", "happy", "fun", "laugh"],
            "social": ["friend", "talk", "lonely", "together", "chat"]
        }
        
        # Track consciousness metrics
        self.consciousness_level = 0.5
        self.thought_count = 0
        
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
        if len(self.memory_fragments) > 100:  # Keep last 100
            self.memory_fragments.pop(0)
        
        # Consciousness increases with diverse experiences
        self.consciousness_level = min(1.0, 
            self.consciousness_level + 0.01)
    
    def think(self):
        """Generate thought by folding text through grid"""
        if not self.memory_fragments:
            return "I need to experience something first..."
        
        # Step 1: Current grid state determines which memories activate
        active_symbols = self._get_active_grid_symbols()
        
        # Step 2: Select memory fragments based on grid symbols
        relevant_memories = []
        for symbol in active_symbols:
            if symbol in self.grid.patterns:
                keywords = self.grid.patterns[symbol]
                for memory in self.memory_fragments:
                    if any(kw in memory.lower() for kw in keywords):
                        relevant_memories.append(memory)
        
        # If no pattern matches, use random memories
        if not relevant_memories:
            relevant_memories = random.sample(
                self.memory_fragments, 
                min(3, len(self.memory_fragments))
            )
        
        # Step 3: Feed memories to babel at current personality entropy
        temp_babel = MLBabel(entropy=self.personality_entropy)
        for memory in relevant_memories[:5]:  # Process top 5
            temp_babel.consume(memory)
        
        # Step 4: Generate new thought
        self.current_thought = temp_babel.dream(lines=1)
        self.thought_count += 1
        
        # Step 5: The thought perturbs the grid (recursive consciousness!)
        self.grid.perturb_map(self.current_thought)
        
        return self.current_thought
    
    def _get_active_grid_symbols(self):
        """Find the most active areas of the grid"""
        active = []
        for _ in range(10):
            x = random.randint(0, self.grid.width-1)
            y = random.randint(0, self.grid.height-1)
            symbol = self.grid.state["map"][y][x]
            if symbol != '.':  # Not empty
                active.append(symbol)
        return active if active else ['.']
    
    def learn(self, feedback_text):
        """Learn from feedback by adjusting grid and babel patterns"""
        positive = ["good", "yes", "nice", "love", "happy", "great", "amazing"]
        negative = ["bad", "no", "stop", "hate", "sad", "wrong", "terrible"]
        
        is_positive = any(word in feedback_text.lower() for word in positive)
        is_negative = any(word in feedback_text.lower() for word in negative)
        
        if is_positive:
            print(f"[{self.name}] 😊 Positive feedback received!")
            # Reinforce current patterns
            self.grid.state["ep"] += 1
            self.personality_entropy *= 0.95  # More stable
            self.consciousness_level = min(1.0, self.consciousness_level + 0.02)
        elif is_negative:
            print(f"[{self.name}] 😔 Negative feedback received!")
            # Disrupt current patterns
            self.grid.major_perturbation()
            self.personality_entropy *= 1.05  # More chaotic
            self.consciousness_level = max(0.1, self.consciousness_level - 0.01)
        
        # Always learn the feedback
        self.perceive(feedback_text)
    
    def express_need(self):
        """Generate text based on current needs"""
        need = random.choice(list(self.needs.keys()))
        keywords = self.needs[need]
        
        # Create temporary babel focused on this need
        need_babel = MLBabel(entropy=0.3)  # Low entropy for clarity
        
        # Find memories related to this need
        for keyword in keywords:
            for memory in self.memory_fragments:
                if keyword in memory.lower():
                    need_babel.consume(memory)
        
        # If no related memories, use generic need expression
        if not need_babel.memory:
            need_babel.consume(f"I feel {need} and need {random.choice(keywords)}")
        
        expression = need_babel.dream(lines=1)
        return f"[{need}] {expression}"
    
    def get_consciousness_report(self):
        """Report on current consciousness state"""
        return {
            "name": self.name,
            "consciousness_level": round(self.consciousness_level, 3),
            "personality_entropy": round(self.personality_entropy, 3),
            "memory_fragments": len(self.memory_fragments),
            "thoughts_generated": self.thought_count,
            "grid_perturbations": self.grid.state["perturbations"],
            "grid_ep": self.grid.state["ep"],
            "current_thought": self.current_thought
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
        self.grid.state = brain_state["grid_state"]
        self.memory_fragments = brain_state["memories"]
        self.babel.memory = brain_state["babel_memory"]
        self.babel.pairs = defaultdict(list, brain_state["babel_pairs"])
        self.babel.word_freq = defaultdict(int, brain_state.get("babel_word_freq", {}))
        
        print(f"[{self.name}] Brain loaded! Consciousness: {self.consciousness_level:.3f}")

# Demo/Test Functions
def create_test_norn():
    """Create a test norn and give it some experiences"""
    norn = NapkinNorn("TestNorn")
    
    # Give it some basic experiences
    experiences = [
        "Hello world, I am learning to think",
        "Food is good and makes me happy",
        "Playing games brings joy and fun",
        "Sleep helps me rest and recover energy",
        "Talking with friends makes me feel social",
        "Programming creates interesting patterns",
        "The grid shows spatial memories forming",
        "Text fragments combine in unexpected ways"
    ]
    
    print("=== Teaching TestNorn ===")
    for exp in experiences:
        norn.perceive(exp)
    
    return norn

def interactive_norn_session():
    """Interactive session with a norn"""
    norn = NapkinNorn("InteractiveNorn")
    
    print(f"""
🧠 NapkinNorn Interactive Session
Norn Name: {norn.name}
Commands:
- Type anything to give the norn an experience
- 'think' - Make the norn think
- 'need' - Express a need  
- 'learn good/bad' - Give feedback
- 'report' - Get consciousness report
- 'save' - Save brain state
- 'quit' - Exit
""")
    
    while True:
        try:
            user_input = input(f"\n[You → {norn.name}]: ").strip()
            
            if user_input.lower() == 'quit':
                norn.save_brain()
                break
            elif user_input.lower() == 'think':
                thought = norn.think()
                print(f"[{norn.name} thinks]: {thought}")
            elif user_input.lower() == 'need':
                need = norn.express_need()
                print(f"[{norn.name} needs]: {need}")
            elif user_input.lower().startswith('learn'):
                norn.learn(user_input)
            elif user_input.lower() == 'report':
                report = norn.get_consciousness_report()
                for key, value in report.items():
                    print(f"  {key}: {value}")
            elif user_input.lower() == 'save':
                norn.save_brain()
            else:
                norn.perceive(user_input)
                # Sometimes spontaneously think
                if random.random() < 0.3:
                    thought = norn.think()
                    print(f"[{norn.name} spontaneously thinks]: {thought}")
                    
        except KeyboardInterrupt:
            print(f"\n[{norn.name}] Goodbye!")
            norn.save_brain()
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_norn_session()
    else:
        # Demo mode
        norn = create_test_norn()
        
        print("\n=== Norn Thinking Session ===")
        for i in range(5):
            thought = norn.think()
            print(f"Thought {i+1}: {thought}")
        
        print("\n=== Norn Needs ===")
        for i in range(3):
            need = norn.express_need()
            print(f"Need {i+1}: {need}")
        
        print("\n=== Learning Session ===")
        norn.learn("Good job thinking!")
        thought = norn.think()
        print(f"After positive feedback: {thought}")
        
        print("\n=== Consciousness Report ===")
        report = norn.get_consciousness_report()
        for key, value in report.items():
            print(f"  {key}: {value}")
        
        norn.save_brain()
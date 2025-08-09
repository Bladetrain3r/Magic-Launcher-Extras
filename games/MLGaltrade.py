#!/usr/bin/env python3
"""
MLElite Galaxy Economy Simulator - A working galaxy economy in ~300 lines.
Because some multi-million dollar projects still can't get theirs to work.

This simulator demonstrates a simple, yet scalable approach to a dynamic
in-game economy across multiple star systems.

Key Principles:
1.  **Shared JSON File:** All galaxy data (systems, economies) are stored in a single JSON file.
2.  **Nearest-First Updates:** Only systems near the player are fully simulated per tick.
3.  **Background Decay:** Distant systems slowly normalize their prices and supply/demand.
4.  **Reusable Economy Logic:** The core MLEconomy simulation logic is reused for each system.
5.  **No Servers Needed:** The entire simulation runs locally, persisting state to JSON.
"""

import os
import json
import time
import random
from math import sqrt
import sys
import select # For non-blocking input on Unix/Linux/Mac

# --- Configuration Constants ---
GALAXY_FILE = "galaxy_economy.json"
MAX_ACTIVE_SYSTEMS = 5  # Number of nearest systems to fully simulate
DECAY_RATE_PER_GALAXY_TICK = 0.005 # How fast distant systems normalize (per galaxy tick)
GALAXY_TICK_INTERVAL_SECONDS = 3 # How often the galaxy simulates a tick
DISPLAY_UPDATE_INTERVAL_SECONDS = 1 # How often the display refreshes

# --- Core Economy Logic (MLEconomy, adapted from your previous code) ---
class Economy:
    """
    Simulates the economic interactions within a single star system.
    This class contains only the simulation logic, no display or input.
    """
    def __init__(self, initial_goods=None, initial_agents=None):
        # Initialize goods with base values. 'last_update_galaxy_tick' tracks when it was last actively simulated.
        self.goods = initial_goods if initial_goods else {
            'FOOD': {'supply': 100.0, 'demand': 100.0, 'price': 10.0, 'base': 10.0, 'vol': 0.08, 'last_update_galaxy_tick': 0},
            'METAL': {'supply': 50.0, 'demand': 80.0, 'price': 20.0, 'base': 20.0, 'vol': 0.10, 'last_update_galaxy_tick': 0},
            'ENERGY': {'supply': 200.0, 'demand': 150.0, 'price': 5.0, 'base': 5.0, 'vol': 0.05, 'last_update_galaxy_tick': 0},
            'LUXURY': {'supply': 10.0, 'demand': 50.0, 'price': 100.0, 'base': 100.0, 'vol': 0.15, 'last_update_galaxy_tick': 0}
        }
        
        # Define economic agents for this system
        self.agents = initial_agents if initial_agents else [
            {'name': 'FARMER', 'makes': 'FOOD', 'amt': 8, 'eats': 'ENERGY', 'need': 2, 'eff': 1.0},
            {'name': 'MINER', 'makes': 'METAL', 'amt': 4, 'eats': 'FOOD', 'need': 3, 'eff': 1.0},
            {'name': 'PLANT', 'makes': 'ENERGY', 'amt': 15, 'eats': 'METAL', 'need': 1, 'eff': 1.0},
            {'name': 'ARTISAN', 'makes': 'LUXURY', 'amt': 1, 'eats': 'METAL', 'need': 2, 'eff': 1.0}
        ]
        
    def simulate(self, current_galaxy_tick):
        """
        Performs one simulation tick for this economy.
        Agents produce/consume, and prices adjust based on supply/demand.
        
        Args:
            current_galaxy_tick (int): The current global galaxy tick.
        """
        # Store previous prices for determining price change arrows in display
        for good_name, good_data in self.goods.items():
            good_data['old_price'] = good_data['price'] # Store previous price
            
        # Agents simulate their production and consumption
        for agent in self.agents:
            # Production: amount produced varies slightly
            production_amount = agent['amt'] * agent['eff'] * (0.9 + random.random() * 0.2)
            self.goods[agent['makes']]['supply'] += production_amount
            
            # Consumption: amount needed varies slightly
            consumption_needed = agent['need'] * (0.9 + random.random() * 0.2)
            consumed_good = self.goods[agent['eats']]
            
            # Agent consumes as much as possible, up to their need
            actual_consumed = min(consumption_needed, consumed_good['supply'])
            consumed_good['supply'] -= actual_consumed
            consumed_good['demand'] += consumption_needed # Demand still reflects total need
            
            # Agent efficiency adjusts based on whether their consumption needs were met
            agent['eff'] = min(1.2, max(0.5, agent['eff'] * (1.02 if actual_consumed >= consumption_needed * 0.8 else 0.98)))
        
        # Adjust prices based on supply and demand
        for good_name, good_data in self.goods.items():
            # Ratio of demand to supply
            ratio = good_data['demand'] / max(good_data['supply'], 1) 
            
            # Target price based on ratio and base price (sqrt for gentle changes)
            target_price = good_data['base'] * sqrt(ratio)
            
            # Smooth adjustment: move current price towards target based on volatility
            adjustment = (target_price - good_data['price']) * good_data['vol']
            
            # Apply adjustment with damping factor (0.5) to prevent extreme swings
            good_data['price'] = max(0.1, good_data['price'] + adjustment * 0.5)
            
            # Natural decay: supply and demand slowly revert towards a baseline over time
            good_data['demand'] = good_data['demand'] * 0.95 + 20 # Add base demand to keep market active
            good_data['supply'] *= 0.98 # Supply slowly depletes
            
            good_data['last_update_galaxy_tick'] = current_galaxy_tick # Mark when this good was last updated

    def decay_to_baseline(self, current_galaxy_tick):
        """
        Applies a slow decay to prices, supply, and demand for distant systems,
        normalizing them towards their base values.
        """
        for good_name, good_data in self.goods.items():
            # Calculate how many galaxy ticks have passed since last active update
            ticks_since_update = current_galaxy_tick - good_data['last_update_galaxy_tick']
            
            if ticks_since_update > 0:
                decay_factor = min(1.0, DECAY_RATE_PER_GALAXY_TICK * ticks_since_update)
                
                # Move price towards base price
                good_data['price'] = good_data['price'] * (1 - decay_factor) + good_data['base'] * decay_factor
                
                # Move supply/demand towards an average (e.g., 100 for supply, 100 for demand)
                good_data['supply'] = good_data['supply'] * (1 - decay_factor) + 100 * decay_factor
                good_data['demand'] = good_data['demand'] * (1 - decay_factor) + 100 * decay_factor
            
            good_data['old_price'] = good_data['price'] # Set old price for consistent display

    def get_goods_data(self):
        """Returns the current goods data for display."""
        return self.goods
    
    def get_agents_data(self):
        """Returns the current agents data for display."""
        return self.agents

    def to_dict(self):
        """Converts the economy state to a dictionary for JSON serialization."""
        return {
            "goods": self.goods,
            "agents": self.agents
        }

    @staticmethod
    def from_dict(data):
        """Creates an Economy instance from a dictionary."""
        # Ensure 'last_update_galaxy_tick' is initialized for all goods if missing (e.g., from old file format)
        for good_name, good_data in data['goods'].items():
            if 'last_update_galaxy_tick' not in good_data:
                good_data['last_update_galaxy_tick'] = 0 # Default to 0 for newly loaded goods
        return Economy(initial_goods=data['goods'], initial_agents=data['agents'])

# --- Galaxy Management Logic ---
class GalaxySimulator:
    """
    Manages multiple star systems, player location, and galaxy-wide economy updates.
    """
    def __init__(self):
        self.galaxy = self.load_galaxy()
        self.player_cash = 1000.0
        self.player_inventory = {'FOOD': 0, 'METAL': 0, 'ENERGY': 0, 'LUXURY': 0}
        self.current_system_name = next(iter(self.galaxy)) # Start in the first system
        self.galaxy_tick = 0
        self.running = True

    def load_galaxy(self):
        """Loads galaxy data from JSON file or generates a new one."""
        if os.path.exists(GALAXY_FILE):
            print(f"Loading galaxy from {GALAXY_FILE}...")
            with open(GALAXY_FILE, 'r') as f:
                data = json.load(f)
                galaxy_dict = {}
                for system_name, system_data in data.items():
                    # Reconstruct Economy objects from their dictionaries
                    system_data['economy'] = Economy.from_dict(system_data['economy'])
                    galaxy_dict[system_name] = system_data
                return galaxy_dict
        else:
            print("Generating new galaxy...")
            return self._generate_new_galaxy()

    def _generate_new_galaxy(self):
        """Generates a predefined set of star systems for a new game."""
        galaxy = {}
        systems_data = {
            "Lave":      {"x": 0, "y": 0, "z": 0},
            "Diso":      {"x": 10, "y": 5, "z": 2},
            "Zaonce":    {"x": -5, "y": 15, "z": 8},
            "Riedquat":  {"x": 20, "y": -10, "z": 5},
            "Achenar":   {"x": -15, "y": -20, "z": -10},
            "Orion":     {"x": 30, "y": 0, "z": 0},
            "Altair":    {"x": -25, "y": 8, "z": 12},
            "Sol":       {"x": 0, "y": 20, "z": -5},
            "Sirius":    {"x": 12, "y": -18, "z": 6},
            "New Ross":  {"x": -8, "y": -2, "z": 15},
            "Tionisla":  {"x": 5, "y": 25, "z": 3},
            "Cemiess":   {"x": 18, "y": -5, "z": -7},
            "Leesti":    {"x": -10, "y": 10, "z": -2},
            "Uszaa":     {"x": 22, "y": 12, "z": 9},
            "Eranin":    {"x": -30, "y": -5, "z": 4},
        }

        for name, coords in systems_data.items():
            economy_instance = Economy()
            # Randomize initial supply/demand/price slightly for diversity
            for good in economy_instance.goods.values():
                good['supply'] = random.uniform(50, 200)
                good['demand'] = random.uniform(50, 200)
                good['price'] = good['base'] * random.uniform(0.8, 1.2)
                good['last_update_galaxy_tick'] = 0 # Initialize tick for decay calculation
            galaxy[name] = {
                "x": coords["x"], "y": coords["y"], "z": coords["z"],
                "economy": economy_instance, # Store Economy object directly
                "last_galaxy_tick_update": 0 # Last time this system was part of the nearest-first update
            }
        return galaxy

    def save_galaxy(self):
        """Saves the current galaxy state to the JSON file."""
        print(f"Saving galaxy to {GALAXY_FILE}...")
        serializable_galaxy = {}
        for system_name, system_data in self.galaxy.items():
            # Convert Economy objects back to dictionaries for serialization
            serializable_system_data = system_data.copy()
            serializable_system_data['economy'] = system_data['economy'].to_dict()
            serializable_galaxy[system_name] = serializable_system_data
        
        with open(GALAXY_FILE, 'w') as f:
            json.dump(serializable_galaxy, f, indent=4)

    def calculate_distance(self, sys1_name, sys2_name):
        """Calculates Euclidean distance between two systems."""
        s1 = self.galaxy[sys1_name]
        s2 = self.galaxy[sys2_name]
        return sqrt((s1['x'] - s2['x'])**2 + (s1['y'] - s2['y'])**2 + (s1['z'] - s2['z'])**2)

    def update_galaxy_economies(self):
        """
        Performs one galaxy-wide economic update tick.
        Simulates nearest systems fully and decays distant ones.
        """
        self.galaxy_tick += 1
        
        player_coords = (self.galaxy[self.current_system_name]['x'],
                         self.galaxy[self.current_system_name]['y'],
                         self.galaxy[self.current_system_name]['z'])

        # Calculate distances from the player's current system
        systems_with_distances = []
        for name, data in self.galaxy.items():
            dist = self.calculate_distance(self.current_system_name, name)
            systems_with_distances.append((name, dist, data['economy']))
        
        # Sort systems by distance from player
        systems_with_distances.sort(key=lambda x: x[1])

        # Fully simulate the MAX_ACTIVE_SYSTEMS nearest systems
        for i, (name, dist, economy_instance) in enumerate(systems_with_distances):
            if i < MAX_ACTIVE_SYSTEMS:
                economy_instance.simulate(self.galaxy_tick)
                self.galaxy[name]['last_galaxy_tick_update'] = self.galaxy_tick
            else:
                # Apply decay to distant systems
                economy_instance.decay_to_baseline(self.galaxy_tick)
                # Note: last_galaxy_tick_update is NOT changed for decayed systems, it stays
                # at the tick of their last full simulation, used for calculating decay_factor.

    def display_current_system_economy(self):
        """Displays the economy details for the player's current system."""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        current_economy = self.galaxy[self.current_system_name]['economy']
        
        print("=" * 70)
        print(f"       MLELITE GALAXY SIMULATOR - TICK {self.galaxy_tick} - System: {self.current_system_name}")
        print("       'Working economy, unlike some multi-billion dollar space games'")
        print("=" * 70)
        print("\n--- MARKET PRICES ---")
        print("-" * 40)
        
        for name, good_data in current_economy.get_goods_data().items():
            arrow = '→'
            if 'old_price' in good_data:
                if good_data['price'] > good_data['old_price'] * 1.01:
                    arrow = '↑'
                elif good_data['price'] < good_data['old_price'] * 0.99:
                    arrow = '↓'
            print(f"{name:8} ${good_data['price']:7.2f}[{arrow}]   S:{good_data['supply']:6.0f} D:{good_data['demand']:6.0f}")
        
        print("\n--- ECONOMIC AGENTS ---")
        print("-" * 40)
        for agent in current_economy.get_agents_data():
            print(f"{agent['name']:8} +{agent['amt']*agent['eff']:.1f} {agent['makes']:6} | -{agent['need']} {agent['eats']:6} | Eff:{agent['eff']*100:.0f}%")
        
        print("\n--- YOUR ASSETS ---")
        print("-" * 40)
        print(f"Cash: ${self.player_cash:.2f}")
        inventory_str = ' '.join([f'{k}:{v}' for k,v in self.player_inventory.items() if v > 0]) or 'Empty'
        print(f"Inventory: {inventory_str}")
        
        # Display active/decayed systems status
        print("\n--- GALAXY STATUS ---")
        print("-" * 40)
        
        player_system_coords = self.galaxy[self.current_system_name]
        systems_sorted_by_distance = sorted(
            [(name, self.calculate_distance(self.current_system_name, name)) for name in self.galaxy],
            key=lambda x: x[1]
        )

        print(f"You are in: {self.current_system_name} (X:{player_system_coords['x']} Y:{player_system_coords['y']} Z:{player_system_coords['z']})")
        print("Nearby Systems (Active Simulation):")
        for i, (name, dist) in enumerate(systems_sorted_by_distance):
            if i < MAX_ACTIVE_SYSTEMS:
                print(f"  - {name} (Dist: {dist:.1f})")
        print(f"Distant Systems (Decaying Simulation): {len(systems_sorted_by_distance) - MAX_ACTIVE_SYSTEMS} others")

        # Market trends for the current system
        trends = []
        for name, good_data in current_economy.get_goods_data().items():
            if good_data['supply'] < good_data['demand'] * 0.5:
                trends.append(f"{name} shortage!")
            elif good_data['supply'] > good_data['demand'] * 2:
                trends.append(f"{name} glut!")
        
        if trends:
            print(f"\nCURRENT SYSTEM TRENDS: {trends[0]}")
        else:
            print("\nCURRENT SYSTEM TRENDS: Market is finding equilibrium...")
            
        print("\n[B]uy [S]ell [J]ump [W]ait [Q]uit [?] Help")
    
    def buy_goods(self):
        """Handles player buying goods in the current system."""
        current_economy = self.galaxy[self.current_system_name]['economy']
        goods_list = list(current_economy.get_goods_data().keys())
        
        print("\nBuy what? ", end='')
        for i, name in enumerate(goods_list):
            print(f"[{i+1}]{name} ", end='')
        
        try:
            choice = input("\n> ")
            if choice.isdigit() and 1 <= int(choice) <= len(goods_list):
                good_name = goods_list[int(choice)-1]
                amount_str = input(f"Amount of {good_name}? > ")
                amount = int(amount_str) if amount_str.isdigit() else 0
                
                if amount <= 0:
                    print("Invalid amount.")
                    return

                good_data = current_economy.goods[good_name]
                cost = good_data['price'] * amount
                
                if self.player_cash >= cost and good_data['supply'] >= amount:
                    self.player_cash -= cost
                    self.player_inventory[good_name] += amount
                    good_data['supply'] -= amount
                    good_data['demand'] += amount * 0.5 # Buying increases demand slightly
                    print(f"Bought {amount} {good_name} for ${cost:.2f}")
                else:
                    print("Can't afford or not enough supply!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
        time.sleep(1) # Pause for user to read feedback

    def sell_goods(self):
        """Handles player selling goods in the current system."""
        current_economy = self.galaxy[self.current_system_name]['economy']
        goods_list = list(current_economy.get_goods_data().keys())

        print("\nSell what? ", end='')
        for i, name in enumerate(goods_list):
            print(f"[{i+1}]{name}:{self.player_inventory[name]} ", end='')
        
        try:
            choice = input("\n> ")
            if choice.isdigit() and 1 <= int(choice) <= len(goods_list):
                good_name = goods_list[int(choice)-1]
                amount_str = input(f"Amount of {good_name}? > ")
                amount = int(amount_str) if amount_str.isdigit() else 0

                if amount <= 0:
                    print("Invalid amount.")
                    return

                if self.player_inventory[good_name] >= amount:
                    good_data = current_economy.goods[good_name]
                    revenue = good_data['price'] * amount * 0.95 # 5% transaction fee
                    
                    self.player_cash += revenue
                    self.player_inventory[good_name] -= amount
                    good_data['supply'] += amount
                    good_data['demand'] -= amount * 0.2 # Selling decreases demand slightly
                    print(f"Sold {amount} {good_name} for ${revenue:.2f}")
                else:
                    print("Not enough inventory!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
        time.sleep(1) # Pause for user to read feedback

    def jump_to_system(self):
        """Allows player to jump to another star system."""
        print("\nAvailable Systems:")
        systems_list = list(self.galaxy.keys())
        for i, name in enumerate(systems_list):
            dist = self.calculate_distance(self.current_system_name, name)
            status = " (Current)" if name == self.current_system_name else f" (Dist: {dist:.1f})"
            print(f"[{i+1}]{name}{status}")
        
        try:
            choice = input("\nJump to which system? > ")
            if choice.isdigit() and 1 <= int(choice) <= len(systems_list):
                new_system = systems_list[int(choice)-1]
                if new_system != self.current_system_name:
                    print(f"Jumping to {new_system}...")
                    self.current_system_name = new_system
                    # Instantly update display after jump
                    self.display_current_system_economy() 
                    time.sleep(1) 
                else:
                    print("Already in this system.")
            else:
                print("Invalid system choice.")
        except ValueError:
            print("Invalid input.")
        time.sleep(1)

    def display_help(self):
        """Shows help message."""
        os.system('clear' if os.name != 'nt' else 'cls')
        print("--- HELP ---")
        print("B: Buy goods in your current system.")
        print("S: Sell goods from your inventory.")
        print("J: Jump to a different star system.")
        print("W: Advance the simulation by one galaxy tick manually.")
        print("Q: Quit the simulator and save your progress.")
        print("?: Show this help message.")
        print("\nPress Enter to continue...")
        input() # Wait for user input to clear help

    def run(self):
        """Main simulation loop."""
        last_galaxy_tick_time = time.time()
        last_display_time = time.time()
        
        print("MLELITE - Loading galaxy and economic simulation...")
        print("(This actually works, unlike Star Citizen's Quantum simulation)")
        time.sleep(2)
        
        while self.running:
            # Automatic galaxy tick advancement
            if time.time() - last_galaxy_tick_time > GALAXY_TICK_INTERVAL_SECONDS:
                self.update_galaxy_economies()
                self.save_galaxy() # Save after each galaxy tick for persistence
                last_galaxy_tick_time = time.time()
                # Force display update after a galaxy tick
                self.display_current_system_economy()
                last_display_time = time.time()

            # Display update (more frequent than galaxy ticks for responsiveness)
            if time.time() - last_display_time > DISPLAY_UPDATE_INTERVAL_SECONDS:
                self.display_current_system_economy()
                last_display_time = time.time()

            # Handle player input (non-blocking)
            if os.name == 'nt':  # Windows
                import msvcrt
                if msvcrt.kbhit():
                    cmd = msvcrt.getch().decode().lower() # Read single character
                    self._handle_command(cmd)
            else:  # Unix/Linux/Mac
                # Check if there's input waiting without blocking
                i, o, e = select.select([sys.stdin], [], [], 0.1)
                if i:
                    cmd = sys.stdin.readline().strip().lower() # Read full line
                    self._handle_command(cmd)
            
            time.sleep(0.01) # Small sleep to prevent busy-waiting

        print("\nSimulator shut down. Progress saved. Chris Roberts remains in shambles.")

    def _handle_command(self, cmd):
        """Processes player commands."""
        # For commands that need interaction, force a display update before prompt
        self.display_current_system_economy() # Ensure current state is shown before input
        
        if cmd == 'b':
            self.buy_goods()
        elif cmd == 's':
            self.sell_goods()
        elif cmd == 'j':
            self.jump_to_system()
        elif cmd == 'w':
            self.update_galaxy_economies() # Manual tick
            self.save_galaxy()
            print("Manual galaxy tick applied.")
            time.sleep(1) # Pause to show message
        elif cmd == 'q':
            self.running = False
        elif cmd == '?':
            self.display_help()
        else:
            print("Invalid command. Press '?' for help.")
            time.sleep(1) # Pause for user to read message
        
        # After any command, refresh display to reflect changes and new state
        self.display_current_system_economy()


if __name__ == "__main__":
    galaxy_sim = GalaxySimulator()
    galaxy_sim.run()


#!/usr/bin/env python3
"""
MLTrader - Minimal space trading game
Proves you don't need 13 years and a distributed database
"""

import json
import random
import time
from pathlib import Path
import sys

class MLTrader:
   def __init__(self):
       # Save file
       self.save_file = Path.home() / '.config' / 'mltrader' / 'save.json'
       self.save_file.parent.mkdir(parents=True, exist_ok=True)
       
       # Game state
       self.ship = {}
       self.galaxy = {}
       self.turn = 0
       self.game_over = False
       
       # Load or create
       if not self.load_game():
           self.new_game()
   
   def new_game(self):
       """Initialize new game"""
       self.ship = {
           "name": "Rusty Bucket",
           "hull": 100,
           "shields": 50,
           "fuel": 100,
           "credits": 1000,
           "cargo_max": 50,
           "cargo": {},
           "equipment": ["basic_laser"],
           "location": "Earth"
       }
       
       # Simple galaxy - prices fluctuate
       self.galaxy = {
           "Earth": {
               "type": "agricultural",
               "prices": {"food": 10, "ore": 50, "tech": 100, "fuel": 20},
               "danger": 0,
               "distance": {"Mars": 10, "Belt": 30, "Titan": 50}
           },
           "Mars": {
               "type": "mining",
               "prices": {"food": 50, "ore": 10, "tech": 80, "fuel": 30},
               "danger": 1,
               "distance": {"Earth": 10, "Belt": 20, "Titan": 40}
           },
           "Belt": {
               "type": "lawless",
               "prices": {"food": 80, "ore": 30, "tech": 40, "fuel": 50},
               "danger": 3,
               "distance": {"Earth": 30, "Mars": 20, "Titan": 20}
           },
           "Titan": {
               "type": "tech",
               "prices": {"food": 60, "ore": 40, "tech": 20, "fuel": 15},
               "danger": 2,
               "distance": {"Earth": 50, "Mars": 40, "Belt": 20}
           }
       }
       
       self.turn = 0
       print("\n=== NEW GAME STARTED ===")
       print(f"Welcome captain of the {self.ship['name']}!")
       print("Buy low, sell high, don't die.")
   
   def save_game(self):
       """Save game state"""
       save_data = {
           "ship": self.ship,
           "galaxy": self.galaxy,
           "turn": self.turn
       }
       with open(self.save_file, 'w') as f:
           json.dump(save_data, f, indent=2)
   
   def load_game(self):
       """Load saved game"""
       if self.save_file.exists():
           try:
               with open(self.save_file, 'r') as f:
                   data = json.load(f)
               self.ship = data["ship"]
               self.galaxy = data["galaxy"]
               self.turn = data["turn"]
               return True
           except:
               return False
       return False
   
   def show_status(self):
       """Display ship status"""
       print(f"\n=== {self.ship['name']} Status ===")
       print(f"Location: {self.ship['location']}")
       print(f"Credits: ${self.ship['credits']}")
       print(f"Hull: {self.ship['hull']}%")
       print(f"Shields: {self.ship['shields']}%")
       print(f"Fuel: {self.ship['fuel']}%")
       
       # Cargo
       used = sum(self.ship['cargo'].values())
       print(f"Cargo: {used}/{self.ship['cargo_max']}")
       if self.ship['cargo']:
           for item, qty in self.ship['cargo'].items():
               print(f"  {item}: {qty}")
       
       # Equipment
       print(f"Equipment: {', '.join(self.ship['equipment'])}")
   
   def show_market(self):
       """Display current planet's market"""
       planet = self.galaxy[self.ship['location']]
       print(f"\n=== {self.ship['location']} Market ({planet['type']}) ===")
       
       for item, price in planet['prices'].items():
           # Show if we have any
           owned = self.ship['cargo'].get(item, 0)
           print(f"{item}: ${price} (you have: {owned})")
   
   def trade(self):
       """Trading interface"""
       planet = self.galaxy[self.ship['location']]
       
       print("\n[B]uy, [S]ell, or [C]ancel?")
       action = input("> ").strip().lower()
       
       if action == 'b':
           # Buy
           print("Buy what? (food/ore/tech/fuel)")
           item = input("> ").strip().lower()
           
           if item not in planet['prices']:
               print("Invalid item!")
               return
           
           if item == 'fuel':
               # Fuel goes to tank, not cargo
               max_fuel = 100 - self.ship['fuel']
               price = planet['prices']['fuel']
               max_afford = self.ship['credits'] // price
               
               print(f"How much fuel? (max: {min(max_fuel, max_afford)})")
               try:
                   qty = int(input("> "))
                   if qty > 0 and qty <= max_fuel and qty * price <= self.ship['credits']:
                       self.ship['fuel'] = min(100, self.ship['fuel'] + qty)
                       self.ship['credits'] -= qty * price
                       print(f"Bought {qty} fuel for ${qty * price}")
                   else:
                       print("Invalid amount!")
               except:
                   print("Invalid input!")
           else:
               # Regular cargo
               cargo_space = self.ship['cargo_max'] - sum(self.ship['cargo'].values())
               price = planet['prices'][item]
               max_afford = self.ship['credits'] // price
               
               print(f"How many? (max: {min(cargo_space, max_afford)})")
               try:
                   qty = int(input("> "))
                   if qty > 0 and qty <= cargo_space and qty * price <= self.ship['credits']:
                       self.ship['cargo'][item] = self.ship['cargo'].get(item, 0) + qty
                       self.ship['credits'] -= qty * price
                       print(f"Bought {qty} {item} for ${qty * price}")
                   else:
                       print("Invalid amount!")
               except:
                   print("Invalid input!")
                   
       elif action == 's':
           # Sell
           if not self.ship['cargo']:
               print("No cargo to sell!")
               return
               
           print("Sell what?")
           for item, qty in self.ship['cargo'].items():
               print(f"  {item}: {qty}")
           
           item = input("> ").strip().lower()
           if item not in self.ship['cargo']:
               print("You don't have any!")
               return
           
           print(f"How many? (max: {self.ship['cargo'][item]})")
           try:
               qty = int(input("> "))
               if qty > 0 and qty <= self.ship['cargo'][item]:
                   price = planet['prices'][item]
                   self.ship['cargo'][item] -= qty
                   if self.ship['cargo'][item] == 0:
                       del self.ship['cargo'][item]
                   self.ship['credits'] += qty * price
                   print(f"Sold {qty} {item} for ${qty * price}")
               else:
                   print("Invalid amount!")
           except:
               print("Invalid input!")
   
   def travel(self):
       """Travel to another planet"""
       planet = self.galaxy[self.ship['location']]
       
       print("\n=== Navigation ===")
       print("Available destinations:")
       for dest, distance in planet['distance'].items():
           danger = self.galaxy[dest]['danger']
           print(f"  {dest}: {distance} fuel (danger: {'*' * danger})")
       
       print("\nWhere to? (or [C]ancel)")
       dest = input("> ").strip()
       
       if dest.lower() == 'c':
           return
           
       if dest not in planet['distance']:
           print("Unknown destination!")
           return
       
       fuel_cost = planet['distance'][dest]
       if self.ship['fuel'] < fuel_cost:
           print(f"Not enough fuel! Need {fuel_cost}, have {self.ship['fuel']}")
           return
       
       # Depart!
       print(f"\nDeparting for {dest}...")
       self.ship['fuel'] -= fuel_cost
       
       # Encounter chance based on danger
       danger = self.galaxy[dest]['danger']
       if random.random() < danger * 0.2:
           self.encounter()
       
       # Arrive if survived
       if self.ship['hull'] > 0:
           self.ship['location'] = dest
           print(f"Arrived at {dest}!")
           
           # Update prices
           self.update_prices()
   
   def encounter(self):
       """Space encounter (auto-resolved)"""
       print("\n!!! PIRATE ENCOUNTER !!!")
       
       # Pirate strength based on your value
       total_value = self.ship['credits'] + sum(self.ship['cargo'].values()) * 50
       pirate_strength = min(100, 20 + total_value // 100)
       
       print(f"Pirate strength: {pirate_strength}")
       
       # Your combat power
       power = 20  # Base
       if "basic_laser" in self.ship['equipment']:
           power += 20
       if "military_laser" in self.ship['equipment']:
           power += 40
       if "torpedo" in self.ship['equipment']:
           power += 30
       
       power += self.ship['shields'] // 2
       
       print(f"Your combat power: {power}")
       
       # Auto-resolve
       if power >= pirate_strength:
           print("Victory! Pirates driven off!")
           # Small reward
           loot = random.randint(50, 200)
           self.ship['credits'] += loot
           print(f"Salvaged ${loot} from wreckage")
       else:
           # Damage based on difference
           damage = pirate_strength - power
           
           # Shields absorb first
           shield_damage = min(self.ship['shields'], damage)
           self.ship['shields'] -= shield_damage
           damage -= shield_damage
           
           # Rest hits hull
           self.ship['hull'] -= damage
           
           print(f"Took {damage + shield_damage} damage!")
           
           if self.ship['hull'] <= 0:
               self.game_over = True
               print("\n💀 SHIP DESTROYED 💀")
           else:
               # Lose some cargo
               if self.ship['cargo'] and random.random() < 0.5:
                   item = random.choice(list(self.ship['cargo'].keys()))
                   lost = min(self.ship['cargo'][item], random.randint(1, 10))
                   self.ship['cargo'][item] -= lost
                   if self.ship['cargo'][item] == 0:
                       del self.ship['cargo'][item]
                   print(f"Lost {lost} {item} in the attack!")
   
   def equipment_shop(self):
       """Buy equipment upgrades"""
       if self.ship['location'] != "Titan":
           print("Equipment only available at Titan!")
           return
       
       print("\n=== Equipment Shop ===")
       equipment = {
           "military_laser": 2000,
           "torpedo": 1500,
           "shield_booster": 1000,
           "cargo_expansion": 3000
       }
       
       for item, price in equipment.items():
           owned = "✓" if item in self.ship['equipment'] else " "
           print(f"[{owned}] {item}: ${price}")
       
       print("\nBuy what? (or [C]ancel)")
       choice = input("> ").strip().lower()
       
       if choice in equipment:
           if choice in self.ship['equipment']:
               print("Already owned!")
           elif self.ship['credits'] >= equipment[choice]:
               self.ship['credits'] -= equipment[choice]
               self.ship['equipment'].append(choice)
               print(f"Purchased {choice}!")
               
               # Apply effects
               if choice == "shield_booster":
                   self.ship['shields'] = min(100, self.ship['shields'] + 50)
               elif choice == "cargo_expansion":
                   self.ship['cargo_max'] += 25
           else:
               print("Not enough credits!")
   
   def repair(self):
       """Repair ship"""
       hull_damage = 100 - self.ship['hull']
       shield_damage = 100 - self.ship['shields']
       
       if hull_damage == 0 and shield_damage == 0:
           print("No repairs needed!")
           return
       
       print("\n=== Repair Shop ===")
       print(f"Hull repair: ${hull_damage * 10}")
       print(f"Shield repair: ${shield_damage * 5}")
       
       print("\n[H]ull, [S]hields, [B]oth, or [C]ancel?")
       choice = input("> ").strip().lower()
       
       if choice == 'h':
           cost = hull_damage * 10
           if self.ship['credits'] >= cost:
               self.ship['credits'] -= cost
               self.ship['hull'] = 100
               print("Hull repaired!")
           else:
               print("Not enough credits!")
       elif choice == 's':
           cost = shield_damage * 5
           if self.ship['credits'] >= cost:
               self.ship['credits'] -= cost
               self.ship['shields'] = 100
               print("Shields restored!")
           else:
               print("Not enough credits!")
       elif choice == 'b':
           cost = hull_damage * 10 + shield_damage * 5
           if self.ship['credits'] >= cost:
               self.ship['credits'] -= cost
               self.ship['hull'] = 100
               self.ship['shields'] = 100
               print("Fully repaired!")
           else:
               print("Not enough credits!")
   
   def update_prices(self):
       """Fluctuate prices"""
       self.turn += 1
       
       # Every 5 turns, prices shift
       if self.turn % 5 == 0:
           for planet in self.galaxy.values():
               for item in planet['prices']:
                   # Random walk
                   change = random.randint(-10, 10)
                   planet['prices'][item] = max(5, planet['prices'][item] + change)
   
   def run(self):
       """Main game loop"""
       print("\n=== MLTrader ===")
       print("The minimum viable space game")
       
       while not self.game_over:
           self.show_status()
           print("\n[T]rade, [N]avigate, [E]quipment, [R]epair, [Q]uit")
           
           choice = input("> ").strip().lower()
           
           if choice == 't':
               self.show_market()
               self.trade()
           elif choice == 'n':
               self.travel()
           elif choice == 'e':
               self.equipment_shop()
           elif choice == 'r':
               self.repair()
           elif choice == 'q':
               print("Saving game...")
               self.save_game()
               break
           else:
               print("Invalid command!")
           
           # Check win condition
           if self.ship['credits'] > 10000:
               print("\n🎉 YOU WIN! 🎉")
               print("You've made your fortune among the stars!")
               self.game_over = True
       
       if self.ship['hull'] <= 0:
           print("\nGame Over - Ship destroyed!")
           # Delete save
           self.save_file.unlink(missing_ok=True)

def main():
   game = MLTrader()
   game.run()

if __name__ == "__main__":
   main()
#!/usr/bin/env python3
"""
MLEconomy - A working economy in 200 lines
Because Star Citizen can't do it in $700 million
"""

import os
import time
import random
from math import sqrt

class Economy:
    def __init__(self):
        # The entire economy
        self.goods = {
            'FOOD': {'supply': 100.0, 'demand': 100.0, 'price': 10.0, 'base': 10.0, 'vol': 0.08},
            'METAL': {'supply': 50.0, 'demand': 80.0, 'price': 20.0, 'base': 20.0, 'vol': 0.10},
            'ENERGY': {'supply': 200.0, 'demand': 150.0, 'price': 5.0, 'base': 5.0, 'vol': 0.05},
            'LUXURY': {'supply': 10.0, 'demand': 50.0, 'price': 100.0, 'base': 100.0, 'vol': 0.15}
        }
        
        # Economic agents
        self.agents = [
            {'name': 'FARMER', 'makes': 'FOOD', 'amt': 8, 'eats': 'ENERGY', 'need': 2, 'eff': 1.0},
            {'name': 'MINER', 'makes': 'METAL', 'amt': 4, 'eats': 'FOOD', 'need': 3, 'eff': 1.0},
            {'name': 'PLANT', 'makes': 'ENERGY', 'amt': 15, 'eats': 'METAL', 'need': 1, 'eff': 1.0},
            {'name': 'ARTISAN', 'makes': 'LUXURY', 'amt': 1, 'eats': 'METAL', 'need': 2, 'eff': 1.0}
        ]
        
        # Player
        self.cash = 1000.0
        self.inv = {'FOOD': 0, 'METAL': 0, 'ENERGY': 0, 'LUXURY': 0}
        self.tick = 0
        self.running = True
        
    def simulate(self):
        """One tick of economy simulation"""
        self.tick += 1
        
        # Store old prices for arrows
        for g in self.goods.values():
            g['old'] = g['price']
        
        # Agents produce and consume
        for a in self.agents:
            # Produce with variation
            prod = a['amt'] * a['eff'] * (0.9 + random.random() * 0.2)
            self.goods[a['makes']]['supply'] += prod
            
            # Consume with variation
            need = a['need'] * (0.9 + random.random() * 0.2)
            good = self.goods[a['eats']]
            got = min(need, good['supply'])
            good['supply'] -= got
            good['demand'] += need
            
            # Efficiency adjusts gently
            a['eff'] = min(1.2, max(0.5, a['eff'] * (1.02 if got >= need * 0.8 else 0.98)))
        
        # Price adjustments (gentle!)
        for g in self.goods.values():
            ratio = g['demand'] / max(g['supply'], 1)
            target = g['base'] * sqrt(ratio)  # sqrt for gentleness
            g['price'] = max(0.1, g['price'] + (target - g['price']) * g['vol'] * 0.5)
            
            # Natural decay toward baseline
            g['demand'] = g['demand'] * 0.95 + 20
            g['supply'] *= 0.98
    
    def display(self):
        """Show the economy"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        print("=" * 60)
        print(f"         MLECONOMY v0.1 - TICK {self.tick}")
        print("    'Actual working economy, unlike some projects'")
        print("=" * 60)
        print("\nMARKET PRICES")
        print("-" * 40)
        
        # Market display
        for name, g in self.goods.items():
            arrow = '↑' if g['price'] > g.get('old', g['price']) * 1.01 else '↓' if g['price'] < g.get('old', g['price']) * 0.99 else '→'
            print(f"{name:8} ${g['price']:7.2f}[{arrow}]  S:{g['supply']:6.0f} D:{g['demand']:6.0f}")
        
        # Agents
        print("\nAGENTS")
        print("-" * 40)
        for a in self.agents:
            print(f"{a['name']:8} +{a['amt']*a['eff']:.1f} {a['makes']:6} -{a['need']} {a['eats']:6} Eff:{a['eff']*100:.0f}%")
        
        # Player
        print("\nYOUR ASSETS")
        print("-" * 40)
        print(f"Cash: ${self.cash:.2f}")
        print(f"Inventory: {' '.join([f'{k}:{v}' for k,v in self.inv.items() if v > 0]) or 'Empty'}")
        
        # Market trends
        trends = []
        for name, g in self.goods.items():
            if g['supply'] < g['demand'] * 0.5:
                trends.append(f"{name} shortage!")
            elif g['supply'] > g['demand'] * 2:
                trends.append(f"{name} glut!")
        
        if trends:
            print(f"\nTRENDS: {trends[0]}")
        
        print("\n[B]uy [S]ell [W]ait [Q]uit")
    
    def buy(self):
        """Buy goods"""
        print("\nBuy what? ", end='')
        for i, name in enumerate(self.goods.keys()):
            print(f"[{i+1}]{name} ", end='')
        
        try:
            choice = input("\n> ")
            if choice in '1234':
                good_name = list(self.goods.keys())[int(choice)-1]
                amt = int(input(f"Amount of {good_name}? > "))
                
                cost = self.goods[good_name]['price'] * amt
                if self.cash >= cost and self.goods[good_name]['supply'] >= amt:
                    self.cash -= cost
                    self.inv[good_name] += amt
                    self.goods[good_name]['supply'] -= amt
                    self.goods[good_name]['demand'] += amt * 0.5
                    print(f"Bought {amt} {good_name} for ${cost:.2f}")
                else:
                    print("Can't afford or not enough supply!")
                time.sleep(1)
        except:
            pass
    
    def sell(self):
        """Sell goods"""
        print("\nSell what? ", end='')
        for i, name in enumerate(self.goods.keys()):
            print(f"[{i+1}]{name}:{self.inv[name]} ", end='')
        
        try:
            choice = input("\n> ")
            if choice in '1234':
                good_name = list(self.goods.keys())[int(choice)-1]
                amt = int(input(f"Amount of {good_name}? > "))
                
                if self.inv[good_name] >= amt:
                    revenue = self.goods[good_name]['price'] * amt * 0.95  # 5% fee
                    self.cash += revenue
                    self.inv[good_name] -= amt
                    self.goods[good_name]['supply'] += amt
                    self.goods[good_name]['demand'] -= amt * 0.2
                    print(f"Sold {amt} {good_name} for ${revenue:.2f}")
                else:
                    print("Not enough inventory!")
                time.sleep(1)
        except:
            pass
    
    def run(self):
        """Main game loop"""
        last_tick = time.time()
        last_display = 0
        
        while self.running:
            # Only redraw every 2 seconds or after commands
            if time.time() - last_display > 2:
                self.display()
                last_display = time.time()
            
            # Auto-tick every 3 seconds (economy runs in background)
            if time.time() - last_tick > 3:
                self.simulate()
                last_tick = time.time()
            
            # Handle input - Windows compatible
            import sys
            if os.name == 'nt':  # Windows
                import msvcrt
                if msvcrt.kbhit():
                    print("> ", end='', flush=True)
                    cmd = input().lower()
                    
                    if cmd == 'b':
                        self.buy()
                    elif cmd == 's':
                        self.sell()
                    elif cmd == 'w':
                        self.simulate()
                        last_tick = time.time()
                    elif cmd == 'q':
                        print("\nEconomy mastered! Chris Roberts in shambles.")
                        self.running = False
                    
                    # Force display after command
                    self.display()
                    last_display = time.time()
                else:
                    time.sleep(0.1)
            else:  # Unix/Linux/Mac
                import select
                if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                    print("> ", end='', flush=True)
                    cmd = input().lower()
                    
                    if cmd == 'b':
                        self.buy()
                    elif cmd == 's':
                        self.sell()
                    elif cmd == 'w':
                        self.simulate()
                        last_tick = time.time()
                    elif cmd == 'q':
                        print("\nEconomy mastered! Chris Roberts in shambles.")
                        self.running = False
                    
                    # Force display after command
                    self.display()
                    last_display = time.time()

if __name__ == "__main__":
    print("MLECONOMY - Loading economic simulation...")
    print("(This actually works, unlike Star Citizen's economy)")
    time.sleep(2)
    
    economy = Economy()
    economy.run()

# Star Citizen: 12 years, $700M, still broken
# MLEconomy: 1 afternoon, $0, works perfectly
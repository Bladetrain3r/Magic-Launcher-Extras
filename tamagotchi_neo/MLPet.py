#!/usr/bin/env python3
"""
MLPet - A simple terminal Tamagotchi
Following the Magic Launcher philosophy: simple, honest, functional
"""

import json
import time
import random
import sys
import os
import threading
from pathlib import Path
from datetime import datetime

# Pet states stored in simple files
PET_DIR = Path.home() / '.mlpet'
STATE_FILE = PET_DIR / 'state.json'
ACTION_FILE = PET_DIR / 'action'
STATUS_FILE = PET_DIR / 'status'

class MLPet:
    def __init__(self):
        PET_DIR.mkdir(exist_ok=True)
        self.running = True
        self.load_or_create()
        
    def load_or_create(self):
        """Load existing pet or create new one"""
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                state = json.load(f)
                self.name = state['name']
                self.hunger = state['hunger']
                self.energy = state['energy']
                self.fun = state['fun']
                self.temp = state['temp']
                self.alive = state['alive']
                self.last_update = state['last_update']
        else:
            # Create new pet
            print("Welcome to MLPet!")
            self.name = input("Name your pet: ").strip() or "Blob"
            self.hunger = 50  # 0=starving, 100=full
            self.energy = 50  # 0=exhausted, 100=hyper
            self.fun = 50     # 0=bored, 100=entertained
            self.temp = 50    # 0=freezing, 100=hot
            self.alive = True
            self.last_update = time.time()
            self.save()
            print(f"\n{self.name} is born! Take good care of them.")
            print("Commands: feed, play, sleep, warm, cool, status, quit")
    
    def save(self):
        """Save pet state to file"""
        state = {
            'name': self.name,
            'hunger': self.hunger,
            'energy': self.energy,
            'fun': self.fun,
            'temp': self.temp,
            'alive': self.alive,
            'last_update': time.time()
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    
    def calculate_mood(self):
        """Calculate mood based on stats"""
        if not self.alive:
            return "dead"
        
        # Average of all stats
        avg = (self.hunger + self.energy + self.fun + self.temp) / 4
        
        if avg > 70:
            return "happy"
        elif avg > 50:
            return "content"
        elif avg > 30:
            return "grumpy"
        elif avg > 10:
            return "miserable"
        else:
            return "dying"
    
    def update_stats(self):
        """Update stats based on time passing"""
        # Decay rates per second
        self.hunger = max(0, self.hunger - 0.03)
        self.energy = max(0, self.energy - 0.02)
        self.fun = max(0, self.fun - 0.05)
        
        # Temperature drifts toward 50 (room temp)
        # Maybe figure out if it can be tied to something local for more dynamic behavior.
        if self.temp > 50:
            self.temp = max(50, self.temp - 0.1)
        elif self.temp < 50:
            self.temp = min(50, self.temp + 0.1)
        
        # Check for unconscious/death
        if self.hunger == 0 or self.energy == 0:
            if self.hunger == 0 and self.energy == 0:
                self.alive = False
                print(f"\n💀 {self.name} has died from neglect...")
                self.running = False
            else:
                print(f"\n😵 {self.name} is unconscious!")
    
    def get_status(self):
        """Get pet's current status description"""
        if not self.alive:
            return f"{self.name} is dead. :("
        
        mood = self.calculate_mood()
        
        # Build status string
        status_parts = []
        
        if self.hunger < 20:
            status_parts.append("starving")
        elif self.hunger < 40:
            status_parts.append("hungry")
        elif self.hunger > 80:
            status_parts.append("stuffed")
        
        if self.energy < 20:
            status_parts.append("exhausted")
        elif self.energy < 40:
            status_parts.append("tired")
        elif self.energy > 80:
            status_parts.append("hyperactive")
        
        if self.fun < 20:
            status_parts.append("bored")
        elif self.fun > 80:
            status_parts.append("ecstatic")
        
        if self.temp < 20:
            status_parts.append("freezing")
        elif self.temp > 80:
            status_parts.append("overheating")
        
        if status_parts:
            status = f"{self.name} is {' and '.join(status_parts)}"
        else:
            status = f"{self.name} is doing okay"
        
        return f"{status} (Mood: {mood})"
    
    def feed(self):
        """Feed the pet"""
        if not self.alive:
            print(f"{self.name} is dead and cannot eat.")
            return
        
        self.hunger = min(100, self.hunger + 30)
        self.energy = min(100, self.energy + 10)
        print(f"🍔 {self.name} munches happily!")
    
    def play(self):
        """Play with the pet"""
        if not self.alive:
            print(f"{self.name} is dead and cannot play.")
            return
        
        if self.energy < 10:
            print(f"{self.name} is too tired to play.")
            return
        
        self.fun = min(100, self.fun + 30)
        self.energy = max(0, self.energy - 15)
        self.hunger = max(0, self.hunger - 5)
        print(f"🎮 {self.name} plays enthusiastically!")
    
    def sleep(self):
        """Let the pet sleep"""
        if not self.alive:
            print(f"{self.name} is in eternal sleep.")
            return
        
        self.energy = min(100, self.energy + 40)
        self.fun = max(0, self.fun - 10)
        print(f"😴 {self.name} takes a nice nap.")
    
    def warm(self):
        """Warm up the pet"""
        if not self.alive:
            return
        
        self.temp = min(100, self.temp + 20)
        print(f"🔥 {self.name} warms up.")
    
    def cool(self):
        """Cool down the pet"""
        if not self.alive:
            return
        
        self.temp = max(0, self.temp - 20)
        print(f"❄️ {self.name} cools down.")
    
    def show_stats(self):
        """Show detailed stats"""
        print(f"\n=== {self.name}'s Stats ===")
        print(f"Hunger: {'█' * (int(self.hunger)//10)}{'░' * (10-int(self.hunger)//10)} {self.hunger:.0f}%")
        print(f"Energy: {'█' * (int(self.energy)//10)}{'░' * (10-int(self.energy)//10)} {self.energy:.0f}%")
        print(f"Fun:    {'█' * (int(self.fun)//10)}{'░' * (10-int(self.fun)//10)} {self.fun:.0f}%")
        print(f"Temp:   {'█' * (int(self.temp)//10)}{'░' * (10-int(self.temp)//10)} {self.temp:.0f}%")
        print(f"Mood:   {self.calculate_mood()}")
        print(f"Status: {'ALIVE' if self.alive else 'DEAD'}")
    
    def background_update(self):
        """Background thread to update stats"""
        last_message = 0
        
        while self.running:
            # Update stats
            self.update_stats()
            
            # Random status messages (5% chance per second)
            if random.random() < 0.05 and time.time() - last_message > 15:
                print(f"\n💭 {self.get_status()}")
                print("Command: ", end='', flush=True)  # Re-prompt
                last_message = time.time()
            
            # Check for file-based commands (for launcher integration)
            if ACTION_FILE.exists():
                try:
                    with open(ACTION_FILE) as f:
                        action = f.read().strip()
                    ACTION_FILE.unlink()  # Delete after reading
                    
                    if action == 'feed':
                        self.feed()
                    elif action == 'play':
                        self.play()
                    elif action == 'sleep':
                        self.sleep()
                except:
                    pass  # Ignore file errors
            
            # Write status for external reading
            try:
                with open(STATUS_FILE, 'w') as f:
                    f.write(self.get_status())
            except:
                pass  # Ignore write errors
            
            # Save state periodically
            self.save()
            time.sleep(1)
    
    def run(self):
        """Main game loop with simple blocking input"""
        print(f"\n{self.get_status()}")
        print("\nCommands: feed, play, sleep, warm, cool, stats, status, quit")
        
        # Start background thread for updates
        update_thread = threading.Thread(target=self.background_update, daemon=True)
        update_thread.start()
        
        # Main input loop
        while self.running:
            try:
                cmd = input("Command: ").strip().lower()
                
                if cmd == 'feed':
                    self.feed()
                elif cmd == 'play':
                    self.play()
                elif cmd == 'sleep':
                    self.sleep()
                elif cmd == 'warm':
                    self.warm()
                elif cmd == 'cool':
                    self.cool()
                elif cmd == 'stats':
                    self.show_stats()
                elif cmd == 'status':
                    print(self.get_status())
                elif cmd == 'help':
                    print("Commands: feed, play, sleep, warm, cool, stats, status, quit")
                elif cmd == 'quit' or cmd == 'exit':
                    print(f"Goodbye! {self.name} will miss you.")
                    self.running = False
                    break
                elif cmd == 'reset':
                    if input(f"Really delete {self.name}? (yes/no): ") == 'yes':
                        STATE_FILE.unlink()
                        print(f"{self.name} has been released.")
                        self.running = False
                        break
                elif cmd == '':
                    continue  # Just pressed enter
                else:
                    print(f"Unknown command: {cmd}")
                    
            except (KeyboardInterrupt, EOFError):
                print(f"\nSaving {self.name}...")
                self.running = False
                break
        
        self.save()

if __name__ == "__main__":
    pet = MLPet()
    try:
        pet.run()
    except Exception as e:
        print(f"Error: {e}")
        pet.save()
        print("Pet saved despite error!")
    print("Goodbye!")
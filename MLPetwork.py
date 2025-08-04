#!/usr/bin/env python3
"""
MLPetWork - Work session pet that guilts you into breaks
Like MLPet but for productivity emotional manipulation
"""

import time
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import threading
import random

try:
   import psutil
   HAS_PSUTIL = True
except ImportError:
   print("MLPetWork requires psutil. Install with: pip install psutil")
   sys.exit(1)

# Work pet config
WORK_APPS = {
   'code', 'devenv', 'vim', 'nvim', 'emacs', 'sublime_text',
   'pycharm', 'idea', 'webstorm', 'terminal', 'cmd', 'powershell',
   'firefox', 'chrome', 'edge'  # Browsers count as work, let's be honest
}

BREAK_TIME = 5 * 60  # 5 min breaks
WORK_TIME = 25 * 60  # 25 min work sessions

class WorkPet:
   def __init__(self, name="Codey"):
       self.name = name
       self.focus = 100      # Depletes when working too long
       self.energy = 100     # Depletes without breaks
       self.happiness = 100  # Overall mood
       self.alive = True
       
       # Session tracking
       self.work_start = None
       self.break_start = None
       self.continuous_work = 0
       self.breaks_taken = 0
       self.deaths_today = 0
       
       # Pet expressions
       self.moods = {
           'happy': f"😊 {name} is thriving with your balanced workflow!",
           'content': f"🙂 {name} is doing okay.",
           'tired': f"😴 {name} is getting tired from all this work...",
           'stressed': f"😰 {name} is stressed! Time for a break?",
           'dying': f"💀 {name} is about to collapse from overwork!",
           'dead': f"☠️ {name} has died from exhaustion."
       }
   
   def update(self, is_working):
       """Update pet stats based on work state"""
       if not self.alive:
           return
           
       if is_working:
           if not self.work_start:
               self.work_start = time.time()
               self.break_start = None
           
           # Calculate continuous work time
           work_duration = time.time() - self.work_start
           
           # Every minute of work depletes stats
           if work_duration > 60:
               depletion = int(work_duration / 60)
               self.focus = max(0, self.focus - depletion * 2)
               self.energy = max(0, self.energy - depletion)
               
               # Extra penalty for working over 25 min without break
               if work_duration > WORK_TIME:
                   overtime = work_duration - WORK_TIME
                   self.happiness = max(0, self.happiness - int(overtime / 60))
                   
                   # Warning messages
                   if work_duration > WORK_TIME * 2:
                       print(f"\n⚠️ {self.name}: 'Please... I need rest...'")
                   elif work_duration > WORK_TIME * 1.5:
                       print(f"\n⚠️ {self.name}: 'Break time was 30 minutes ago!'")
       else:
           # On break
           if not self.break_start:
               self.break_start = time.time()
               if self.work_start:
                   self.continuous_work = time.time() - self.work_start
               self.work_start = None
           
           break_duration = time.time() - self.break_start
           
           # Restore stats during break
           if break_duration > 30:  # At least 30 sec to count
               restoration = int(break_duration / 30)
               self.focus = min(100, self.focus + restoration * 3)
               self.energy = min(100, self.energy + restoration * 2)
               self.happiness = min(100, self.happiness + restoration)
               
               # Good break bonus
               if break_duration >= BREAK_TIME:
                   if self.breaks_taken == 0 or self.continuous_work >= WORK_TIME:
                       self.happiness = min(100, self.happiness + 10)
                       self.breaks_taken += 1
                       print(f"\n🎉 {self.name} is happy you took a proper break!")
       
       # Check for death
       if self.focus == 0 or self.energy == 0:
           self.alive = False
           self.deaths_today += 1
           print(f"\n{self.moods['dead']}")
           print(f"Cause: {'Mental exhaustion' if self.focus == 0 else 'Physical exhaustion'}")
           print(f"Deaths today: {self.deaths_today}")
           
           # Revive after shame period
           time.sleep(3)
           self.revive()
   
   def revive(self):
       """Revive with penalty"""
       print(f"\n🔄 {self.name} has respawned, but remembers the pain...")
       self.alive = True
       self.focus = 50  # Start weaker
       self.energy = 50
       self.happiness = 30  # Very unhappy about dying
       self.work_start = None
       self.break_start = None
   
   def get_mood(self):
       """Get current mood based on stats"""
       if not self.alive:
           return 'dead'
       
       avg = (self.focus + self.energy + self.happiness) / 3
       if avg > 80:
           return 'happy'
       elif avg > 60:
           return 'content'
       elif avg > 40:
           return 'tired'
       elif avg > 20:
           return 'stressed'
       else:
           return 'dying'
   
   def status(self):
       """Get pet status bar"""
       if not self.alive:
           return self.moods['dead']
       
       mood = self.get_mood()
       
       # ASCII pet based on mood
       pets = {
           'happy': '(◕‿◕)',
           'content': '(•_•)',
           'tired': '(－_－)',
           'stressed': '(>_<)',
           'dying': '(x_x)'
       }
       
       pet_ascii = pets.get(mood, '(?_?)')
       
       # Status bars
       focus_bar = '█' * (self.focus // 10) + '░' * (10 - self.focus // 10)
       energy_bar = '█' * (self.energy // 10) + '░' * (10 - self.energy // 10)
       happy_bar = '█' * (self.happiness // 10) + '░' * (10 - self.happiness // 10)
       
       status = f"""
╔════════════════════════════════════════╗
║ {self.name} {pet_ascii:<10} Breaks: {self.breaks_taken} Deaths: {self.deaths_today} ║
╠════════════════════════════════════════╣
║ Focus:     {focus_bar} {self.focus:3}% ║
║ Energy:    {energy_bar} {self.energy:3}% ║
║ Happiness: {happy_bar} {self.happiness:3}% ║
╠════════════════════════════════════════╣
║ {self.moods[mood]:<38} ║
╚════════════════════════════════════════╝
"""
       return status

def is_working():
   """Check if user is in a work application"""
   try:
       for proc in psutil.process_iter(['pid', 'name']):
           proc_name = proc.info['name'].lower()
           # Check if any work app is running
           for work_app in WORK_APPS:
               if work_app in proc_name:
                   return True
   except:
       pass
   return False

def clear_screen():
   """Clear terminal screen"""
   os.system('cls' if os.name == 'nt' else 'clear')

def monitor_loop(pet):
   """Background monitoring thread"""
   last_state = None
   
   while True:
       working = is_working()
       
       # State change notification
       if working != last_state:
           if working:
               print(f"\n👔 Work session started at {datetime.now().strftime('%H:%M')}")
           else:
               print(f"\n☕ Break started at {datetime.now().strftime('%H:%M')}")
           last_state = working
       
       pet.update(working)
       time.sleep(10)  # Check every 10 seconds

def main():
   """Main entry point"""
   if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
       print("MLPetWork - Work/Break Balance Pet")
       print("\nYour pet thrives on balanced work sessions!")
       print("Work 25 minutes, break 5 minutes, keep pet happy.")
       print("\nPet dies from:")
       print("- Working too long without breaks")
       print("- Ignoring break warnings")
       print("- General overwork")
       sys.exit(0)
   
   # Create work pet
   pet_name = sys.argv[1] if len(sys.argv) > 1 else "Codey"
   pet = WorkPet(pet_name)
   
   print(f"MLPetWork - {pet_name} is here to monitor your work/life balance!")
   print("Press Ctrl+C to exit\n")
   
   # Start monitoring thread
   monitor_thread = threading.Thread(target=monitor_loop, args=(pet,), daemon=True)
   monitor_thread.start()
   
   # Main display loop
   try:
       while True:
           clear_screen()
           print(pet.status())
           
           # Extra warnings
           if pet.continuous_work > WORK_TIME * 2:
               print("⚠️  SERIOUSLY, TAKE A BREAK! ⚠️")
           elif pet.continuous_work > WORK_TIME:
               print("⏰ Break time recommended!")
           
           time.sleep(5)  # Update display every 5 seconds
           
   except KeyboardInterrupt:
       print(f"\n\nSaving {pet_name}'s stats...")
       print(f"Total breaks taken: {pet.breaks_taken}")
       print(f"Deaths from overwork: {pet.deaths_today}")
       if pet.deaths_today > 0:
           print(f"\n💭 {pet_name} hopes you'll take better care tomorrow...")
       else:
           print(f"\n🌟 {pet_name} is proud of your work/life balance!")

if __name__ == "__main__":
   main()
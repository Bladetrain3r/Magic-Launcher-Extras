#!/usr/bin/env python3
"""
MLDice - Magic Launcher Dice Roller
Because clicking buttons beats typing /roll every time
Now with slash commands for the power users
Under 250 lines of dice-rolling fury
"""

import tkinter as tk
from tkinter import ttk
import random
import re

class MLDice:
   def __init__(self, root):
       self.root = root
       self.root.title("MLDice - Click Clack Math Rocks")
       self.root.geometry("600x800")
       self.root.resizable(False, False)
       
       # History of rolls
       self.history = []
       
       # Main frame
       main_frame = ttk.Frame(root, padding="10")
       main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       
       # Custom roll entry
       ttk.Label(main_frame, text="Custom Roll (e.g., 2d6+3, 4d6/dl):").grid(row=0, column=0, columnspan=2, pady=5)
       
       self.custom_entry = ttk.Entry(main_frame, width=20)
       self.custom_entry.grid(row=1, column=0, padx=5)
       self.custom_entry.bind('<Return>', lambda e: self.roll_custom())
       
       ttk.Button(main_frame, text="Roll!", command=self.roll_custom).grid(row=1, column=1, padx=5)
       
       # Help text for commands
       help_frame = ttk.Frame(main_frame)
       help_frame.grid(row=2, column=0, columnspan=2, pady=5)
       
       help_text = "Commands: /dl (drop lowest), /dh (drop highest), /kh (keep highest), /kl (keep lowest)"
       ttk.Label(help_frame, text=help_text, font=('Arial', 8)).pack()
       
       # Quick roll buttons
       ttk.Label(main_frame, text="Quick Rolls:").grid(row=3, column=0, columnspan=2, pady=(10,5))
       
       # Standard dice in 2 columns
       dice = ['1d4', '1d6', '1d8', '1d10', '1d12', '1d20', '1d100', '2d6']
       
       for i, die in enumerate(dice):
           row = 4 + (i // 2)
           col = i % 2
           ttk.Button(
               main_frame, 
               text=die, 
               command=lambda d=die: self.roll_dice(d),
               width=8
           ).grid(row=row, column=col, padx=5, pady=2)
       
       # Advantage/Disadvantage
       ttk.Label(main_frame, text="D20 Special:").grid(row=8, column=0, columnspan=2, pady=(10,5))
       
       special_frame = ttk.Frame(main_frame)
       special_frame.grid(row=9, column=0, columnspan=2)
       
       ttk.Button(
           special_frame, 
           text="Advantage", 
           command=lambda: self.roll_advantage(True),
           width=12
       ).pack(side=tk.LEFT, padx=5)
       
       ttk.Button(
           special_frame, 
           text="Disadvantage", 
           command=lambda: self.roll_advantage(False),
           width=12
       ).pack(side=tk.LEFT, padx=5)
       
       # Stat roller
       ttk.Button(
           main_frame,
           text="Roll Stats (4d6 drop lowest)",
           command=self.roll_stats,
           width=25
       ).grid(row=10, column=0, columnspan=2, pady=5)
       
       # Result display
       ttk.Label(main_frame, text="Result:").grid(row=11, column=0, columnspan=2, pady=(20,5))
       
       self.result_label = ttk.Label(
           main_frame, 
           text="Ready to roll!", 
           font=('Arial', 24, 'bold'),
           foreground='blue'
       )
       self.result_label.grid(row=12, column=0, columnspan=2, pady=10)
       
       # Details label
       self.details_label = ttk.Label(main_frame, text="", font=('Arial', 10))
       self.details_label.grid(row=13, column=0, columnspan=2)
       
       # History display
       ttk.Label(main_frame, text="History:").grid(row=14, column=0, columnspan=2, pady=(20,5))
       
       # History text with scrollbar
       history_frame = ttk.Frame(main_frame)
       history_frame.grid(row=15, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
       
       self.history_text = tk.Text(history_frame, height=8, width=45)
       self.history_text.pack(side=tk.LEFT)
       
       scrollbar = ttk.Scrollbar(history_frame, command=self.history_text.yview)
       scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
       self.history_text.config(yscrollcommand=scrollbar.set)
       
       # Clear button
       ttk.Button(main_frame, text="Clear History", command=self.clear_history).grid(row=16, column=0, columnspan=2, pady=10)
   
   def parse_dice(self, dice_str):
       """Parse dice notation like 2d6+3 or 1d20-2 with optional /commands"""
       # Split by slash to get command
       parts = dice_str.lower().replace(' ', '').split('/')
       base = parts[0]
       command = parts[1] if len(parts) > 1 else None
       
       # Parse base dice notation
       match = re.match(r'(\d+)d(\d+)([+-]?\d*)', base)
       if not match:
           return None
       
       num_dice = int(match.group(1))
       die_size = int(match.group(2))
       modifier = int(match.group(3)) if match.group(3) else 0
       
       return num_dice, die_size, modifier, command
   
   def roll_dice(self, dice_str):
       """Roll dice and display result"""
       parsed = self.parse_dice(dice_str)
       if not parsed:
           self.result_label.config(text="Invalid!", foreground='red')
           return
       
       num_dice, die_size, modifier, command = parsed
       
       # Roll the dice
       rolls = sorted([random.randint(1, die_size) for _ in range(num_dice)])
       original_rolls = rolls.copy()
       
       # Apply command
       command_text = ""
       if command:
           if command == 'dl':  # Drop lowest
               if len(rolls) > 1:
                   dropped = rolls.pop(0)
                   command_text = f" (dropped {dropped})"
           elif command == 'dh':  # Drop highest
               if len(rolls) > 1:
                   dropped = rolls.pop()
                   command_text = f" (dropped {dropped})"
           elif command == 'kh':  # Keep highest
               if len(rolls) > 1:
                   kept = rolls[-1]
                   rolls = [kept]
                   command_text = f" (kept highest: {kept})"
           elif command == 'kl':  # Keep lowest
               if len(rolls) > 1:
                   kept = rolls[0]
                   rolls = [kept]
                   command_text = f" (kept lowest: {kept})"
       
       total = sum(rolls) + modifier
       
       # Display result
       self.result_label.config(text=str(total), foreground='blue')
       
       # Show details
       details = f"{dice_str}: {original_rolls}"
       details += command_text
       if modifier:
           details += f" {'+' if modifier > 0 else ''}{modifier}"
       details += f" = {total}"
       self.details_label.config(text=details)
       
       # Add to history
       self.add_to_history(details)
   
   def roll_custom(self):
       """Roll from custom entry"""
       dice_str = self.custom_entry.get()
       if dice_str:
           self.roll_dice(dice_str)
   
   def roll_advantage(self, is_advantage):
       """Roll with advantage or disadvantage"""
       roll1 = random.randint(1, 20)
       roll2 = random.randint(1, 20)
       
       if is_advantage:
           result = max(roll1, roll2)
           label = "Advantage"
       else:
           result = min(roll1, roll2)
           label = "Disadvantage"
       
       self.result_label.config(text=str(result), foreground='green' if is_advantage else 'red')
       self.details_label.config(text=f"{label}: rolled {roll1} and {roll2}, keeping {result}")
       
       self.add_to_history(f"{label}: {roll1}, {roll2} → {result}")
   
   def roll_stats(self):
       """Roll 6 sets of 4d6 drop lowest for stats"""
       stats = []
       details = []
       
       for i in range(6):
           rolls = sorted([random.randint(1, 6) for _ in range(4)])
           dropped = rolls[0]
           kept = rolls[1:]
           total = sum(kept)
           stats.append(total)
           details.append(f"{rolls} drop {dropped} = {total}")
       
       self.result_label.config(text=str(stats), foreground='purple')
       self.details_label.config(text="Stats rolled (4d6 drop lowest each)")
       
       # Add detailed breakdown to history
       self.add_to_history("=== STAT ROLL ===")
       for i, (stat, detail) in enumerate(zip(stats, details)):
           self.add_to_history(f"Stat {i+1}: {detail}")
       self.add_to_history(f"Final: {stats}")
   
   def add_to_history(self, text):
       """Add roll to history"""
       self.history.append(text)
       self.history_text.insert(tk.END, text + "\n")
       self.history_text.see(tk.END)
   
   def clear_history(self):
       """Clear the history"""
       self.history = []
       self.history_text.delete(1.0, tk.END)

def main():
   root = tk.Tk()
   app = MLDice(root)
   root.mainloop()

if __name__ == "__main__":
   main()
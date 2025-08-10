#!/usr/bin/env python3
"""
MLVillager - Magic Launcher NPC Line Generator
For when you need that guard to say something besides "arrow to the knee"
Under 300 lines of improvisational panic relief
"""

import random
import tkinter as tk
from tkinter import ttk

class MLVillager:
   def __init__(self, root):
       self.root = root
       self.root.title("MLVillager - Instant NPC Dialogue")
       self.root.geometry("500x600")
       
       # The wisdom pools
       self.greetings = [
           "Well met, traveler",
           "Aye, what brings ye here",
           "Haven't seen your face before",
           "Another adventurer, eh",
           "Gods be good, visitors",
           "Hail and well met",
           "What news from the road",
           "Blessings upon ye",
           "Strange times, these",
           "Ye look like trouble",
       ]
       
       self.complaints = [
           "crops been failing since the incident",
           "wolves getting bolder every season",
           "tax collector's due any day now",
           "well's been tasting funny lately",
           "strange lights in the old forest",
           "haven't seen the sun in three days",
           "merchants avoiding our roads",
           "young folks all leaving for the city",
           "priest says it's an ill omen",
           "miller's charging twice his usual",
           "rats in the grain store again",
           "bridge washed out last storm",
       ]
       
       self.rumors = [
           "they say the old tower's haunted",
           "heard tell of goblins to the north",
           "merchant came through speaking of war",
           "strange folk been asking questions",
           "saw tracks near the abandoned mine",
           "fishermen won't go past the bend anymore",
           "old Martha swears she saw a dragon",
           "cemetery gate was found open again",
           "something's killing the livestock",
           "mayor's been acting mighty strange",
           "caravan never made it through the pass",
           "they found another one in the woods",
       ]
       
       self.warnings = [
           "wouldn't go that way if I were you",
           "best stay on the path after dark",
           "don't trust the hermit, mark my words",
           "avoid the ruins, nothing good there",
           "lock your doors come nightfall",
           "don't drink from the eastern well",
           "stay away from the old oak tree",
           "never travel alone these days",
           "keep your weapons close",
           "trust no one wearing purple",
       ]
       
       self.directions = [
           "follow the road past the mill",
           "two days north, can't miss it",
           "just over that hill there",
           "take the left fork at the stone",
           "straight through til you see the tower",
           "past the bridge, then follow the stream",
           "three houses down from the temple",
           "other side of the market square",
           "follow the smoke, you'll find it",
           "ask the blacksmith, he'll know",
       ]
       
       self.dismissals = [
           "got work to tend to",
           "best be on your way",
           "nothing more to tell ye",
           "that's all I know",
           "sun's wasting, got to go",
           "wife'll have my head if I'm late",
           "said too much already",
           "shouldn't even be talking to strangers",
           "leave me be now",
           "got nothing else for ye",
       ]
       
       self.professions = [
           "Farmer", "Guard", "Merchant", "Blacksmith", "Innkeeper",
           "Fisherman", "Miller", "Carpenter", "Butcher", "Baker",
           "Herbalist", "Stable hand", "Drunk", "Beggar", "Noble",
           "Priest", "Scribe", "Hunter", "Shepherd", "Miner"
       ]
       
       self.moods = [
           "Nervous", "Friendly", "Suspicious", "Tired", "Angry",
           "Cheerful", "Paranoid", "Bored", "Desperate", "Drunk",
           "Frightened", "Gossipy", "Grumpy", "Helpful", "Secretive"
       ]
       
       # Build UI
       main_frame = ttk.Frame(root, padding="10")
       main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       
       # NPC Type selector
       ttk.Label(main_frame, text="NPC Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
       
       type_frame = ttk.Frame(main_frame)
       type_frame.grid(row=1, column=0, columnspan=2, pady=5)
       
       self.profession_var = tk.StringVar(value="Random")
       profession_menu = ttk.Combobox(type_frame, textvariable=self.profession_var, width=15)
       profession_menu['values'] = ["Random"] + self.professions
       profession_menu.pack(side=tk.LEFT, padx=5)
       
       self.mood_var = tk.StringVar(value="Random")
       mood_menu = ttk.Combobox(type_frame, textvariable=self.mood_var, width=15)
       mood_menu['values'] = ["Random"] + self.moods
       mood_menu.pack(side=tk.LEFT, padx=5)
       
       # Quick generators
       ttk.Label(main_frame, text="Quick Lines:").grid(row=2, column=0, sticky=tk.W, pady=(20,5))
       
       button_frame = ttk.Frame(main_frame)
       button_frame.grid(row=3, column=0, columnspan=2)
       
       ttk.Button(button_frame, text="Greeting", command=lambda: self.generate_line("greeting")).pack(side=tk.LEFT, padx=2)
       ttk.Button(button_frame, text="Rumor", command=lambda: self.generate_line("rumor")).pack(side=tk.LEFT, padx=2)
       ttk.Button(button_frame, text="Warning", command=lambda: self.generate_line("warning")).pack(side=tk.LEFT, padx=2)
       ttk.Button(button_frame, text="Directions", command=lambda: self.generate_line("directions")).pack(side=tk.LEFT, padx=2)
       ttk.Button(button_frame, text="Complaint", command=lambda: self.generate_line("complaint")).pack(side=tk.LEFT, padx=2)
       
       # Full conversation button
       ttk.Button(
           main_frame,
           text="Generate Full Conversation",
           command=self.generate_conversation
       ).grid(row=4, column=0, columnspan=2, pady=20)
       
       # Output display
       self.output_text = tk.Text(main_frame, height=20, width=60, wrap=tk.WORD)
       self.output_text.grid(row=5, column=0, columnspan=2, pady=10)
       
       scrollbar = ttk.Scrollbar(main_frame, command=self.output_text.yview)
       scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))
       self.output_text.config(yscrollcommand=scrollbar.set)
       
       # Buttons at bottom
       bottom_frame = ttk.Frame(main_frame)
       bottom_frame.grid(row=6, column=0, columnspan=2, pady=10)
       
       ttk.Button(bottom_frame, text="Clear", command=self.clear_output).pack(side=tk.LEFT, padx=5)
       ttk.Button(bottom_frame, text="Copy All", command=self.copy_all).pack(side=tk.LEFT, padx=5)
   
   def get_npc(self):
       """Get current NPC type"""
       prof = self.profession_var.get()
       mood = self.mood_var.get()
       
       if prof == "Random":
           prof = random.choice(self.professions)
       if mood == "Random":
           mood = random.choice(self.moods)
           
       return f"{mood} {prof}"
   
   def generate_line(self, line_type):
       """Generate a single line"""
       npc = self.get_npc()
       
       if line_type == "greeting":
           line = random.choice(self.greetings)
       elif line_type == "rumor":
           line = random.choice(self.rumors)
       elif line_type == "warning":
           line = random.choice(self.warnings)
       elif line_type == "directions":
           line = random.choice(self.directions)
       elif line_type == "complaint":
           line = random.choice(self.complaints)
       else:
           line = "..."
       
       # Capitalize first letter
       line = line[0].upper() + line[1:] if line else line
       
       # Add punctuation if missing
       if line and line[-1] not in '.!?':
           line += '.'
       
       output = f"[{npc}]: \"{line}\"\n\n"
       self.output_text.insert(tk.END, output)
       self.output_text.see(tk.END)
   
   def generate_conversation(self):
       """Generate a full NPC conversation"""
       npc = self.get_npc()
       
       # Build a conversation flow
       conversation = []
       
       # Opening
       greeting = random.choice(self.greetings)
       conversation.append(f"{greeting}.")
       
       # Main content (1-3 elements)
       elements = []
       if random.random() > 0.3:
           elements.append(('rumor', self.rumors))
       if random.random() > 0.5:
           elements.append(('complaint', self.complaints))
       if random.random() > 0.7:
           elements.append(('warning', self.warnings))
       
       random.shuffle(elements)
       
       for element_type, pool in elements[:random.randint(1,3)]:
           line = random.choice(pool)
           # Add conversational connectors sometimes
           if len(conversation) > 1 and random.random() > 0.5:
               connectors = ["Oh, and", "Also", "Another thing", "Between you and me", "I'll tell you what"]
               line = f"{random.choice(connectors)}, {line}"
           conversation.append(f"{line[0].upper()}{line[1:]}.")
       
       # Ending
       if random.random() > 0.3:
           dismissal = random.choice(self.dismissals)
           conversation.append(f"Now, {dismissal}.")
       
       # Format output
       output = f"[{npc}]:\n"
       for line in conversation:
           output += f'"{line}"\n'
       output += "\n" + "="*40 + "\n\n"
       
       self.output_text.insert(tk.END, output)
       self.output_text.see(tk.END)
   
   def clear_output(self):
       """Clear the output text"""
       self.output_text.delete(1.0, tk.END)
   
   def copy_all(self):
       """Copy all text to clipboard"""
       text = self.output_text.get(1.0, tk.END)
       self.root.clipboard_clear()
       self.root.clipboard_append(text)

def main():
   root = tk.Tk()
   app = MLVillager(root)
   root.mainloop()

if __name__ == "__main__":
   main()
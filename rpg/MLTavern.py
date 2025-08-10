#!/usr/bin/env python3
"""
MLBardSong - Magic Launcher Tavern Entertainment Generator
For when players ask "what's the bard singing about?"
Produces broken ballads and mangled myths
Under 250 lines of procedural poetry
"""

import random
import tkinter as tk
from tkinter import ttk

class MLBardSong:
   def __init__(self, root):
       self.root = root
       self.root.title("MLBardSong - Instant Tavern Tales")
       self.root.geometry("500x600")
       
       # Song components in broken English style
       self.heroes = [
           "the knight what lost his horse",
           "brave warrior with bent sword", 
           "the maiden what slays the dragons",
           "old wizard whose beard caught fire",
           "the thief what steals from himself",
           "mighty queen of broken kingdom",
           "the fool what becomes the king",
           "young squire with wooden blade",
           "the monk what forgot his vows",
           "fair princess who fights the dark"
       ]
       
       self.villains = [
           "the shadow midst the mountain",
           "cursed lord of empty halls",
           "the beast what eats the moon",
           "dark sorcerer with backwards magic",
           "the giant whose tears make floods",
           "evil twin from mirror realm",
           "the demon what speaks in riddles",
           "dead king who won't stay buried",
           "the witch what steals the names",
           "dragon made of winter's breath"
       ]
       
       self.locations = [
           "where sun doth never shows",
           "midst the forest of singing trees",
           "upon the bridge of broken dreams",
           "in castle made of morning mist",
           "beneath the lake of silver tears",
           "where mountains kiss the sky",
           "through valleys filled with bones",
           "in tower tall as giant's reach",
           "across the sea of endless night",
           "where earth meets the burning sky"
       ]
       
       self.actions = [
           "did fought with might and main",
           "yet falls upon the cursed ground",
           "doth crashes through the ancient door",
           "midst battle fierce did cry aloud",
           "through darkness crawled on bloody knee",
           "with magic sword did strike the foe",
           "yet mercy showed when none deserved",
           "did steal the crown of starlight bright",
           "through fire walked with head held high",
           "midst chaos brought the peace at last"
       ]
       
       self.consequences = [
           "now sleeps beneath the willow tree",
           "yet victory tastes like ash and dust",
           "and kingdoms fell like autumn leaves",
           "but love was lost amongst the gold",
           "now wanders still the empty roads",
           "yet songs of glory turned to tears",
           "and prophecy proved false at last",
           "but mirror showed the truth too late",
           "now ravens speak their name in vain",
           "yet blessed curse remains unbroken"
       ]
       
       self.romantic_starts = [
           "My love did sailed across the sea",
           "Fair maiden with the golden hair",
           "The knight did loved the peasant girl",
           "Two hearts what beat as one they say",
           "My darling went to fight the war",
           "The princess loved a common man",
           "Sweet lover mine with eyes so bright",
           "The shepherd boy did love the star"
       ]
       
       self.romantic_ends = [
           "but never more returned to me",
           "now weeps beside the empty grave",
           "yet duty tore their hearts apart",
           "but death did claimed them both at dawn",
           "and left me with this broken heart",
           "now sings no more the wedding song",
           "yet ghost still walks the castle walls",
           "but stars don't love the mortal folk"
       ]
       
       self.chorus_fragments = [
           "Sing hey! Sing ho! The tale is told!",
           "Weep now, weep long, the hero's gone!",
           "Dance round, dance round, midst sorrow found!",
           "Cry out! Cry out! The darkness comes!",
           "Sing low, sing sweet, where lovers meet!",
           "Mourn deep, mourn true, the sky ain't blue!",
           "Shout loud! Shout strong! Right becomes wrong!",
           "Whisper soft, whisper low, where shadows grow!"
       ]
       
       # Build UI
       main_frame = ttk.Frame(root, padding="10")
       main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       
       # Song type selector
       ttk.Label(main_frame, text="Song Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
       
       self.song_type = tk.StringVar(value="Random")
       type_menu = ttk.Combobox(main_frame, textvariable=self.song_type, width=20)
       type_menu['values'] = ["Random", "Epic Tale", "Tragic Romance", "Drunken Ramble", "Prophecy"]
       type_menu.grid(row=1, column=0, pady=5)
       
       # Generate button
       ttk.Button(
           main_frame,
           text="Strike the Lute!",
           command=self.generate_song
       ).grid(row=2, column=0, pady=20)
       
       # Output display
       self.output_text = tk.Text(main_frame, height=25, width=60, wrap=tk.WORD, font=('Georgia', 11))
       self.output_text.grid(row=3, column=0, pady=10)
       
       scrollbar = ttk.Scrollbar(main_frame, command=self.output_text.yview)
       scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S))
       self.output_text.config(yscrollcommand=scrollbar.set)
       
       # Bottom buttons
       bottom_frame = ttk.Frame(main_frame)
       bottom_frame.grid(row=4, column=0, pady=10)
       
       ttk.Button(bottom_frame, text="Clear", command=self.clear_output).pack(side=tk.LEFT, padx=5)
       ttk.Button(bottom_frame, text="Copy", command=self.copy_output).pack(side=tk.LEFT, padx=5)
       ttk.Button(bottom_frame, text="Another!", command=self.generate_song).pack(side=tk.LEFT, padx=5)
   
   def generate_epic(self):
       """Generate an epic tale stanza"""
       hero = random.choice(self.heroes)
       villain = random.choice(self.villains)
       location = random.choice(self.locations)
       action = random.choice(self.actions)
       consequence = random.choice(self.consequences)
       
       lines = [
           f"Oh {hero}",
           f"Did face {villain}",
           f"There {location}",
           f"The hero {action}",
           f"And {consequence}",
           "",
           random.choice(self.chorus_fragments)
       ]
       
       return "\n".join(lines)
   
   def generate_romance(self):
       """Generate a tragic romance stanza"""
       start = random.choice(self.romantic_starts)
       location = random.choice(self.locations)
       end = random.choice(self.romantic_ends)
       
       lines = [
           start,
           f"We danced {location}",
           "The moon did watched us from above",
           "Yet fate midst cruel did intervene",
           end,
           "",
           "Sing soft! Sing sweet! Love's bitter defeat!"
       ]
       
       return "\n".join(lines)
   
   def generate_drunken(self):
       """Generate a drunken rambling verse"""
       snippets = [
           "The ale did flow like river wide",
           "My horse, my horse, where goes my horse?",
           "The barkeep's daughter smiled at me", 
           "Or was it just the wine I see?",
           "I fought a dragon! No, a cat!",
           "My sword is... where'd I put my hat?",
           "The room spins round like wagon wheel",
           "Tomorrow's regret I'll surely feel"
       ]
       
       # Random selection of 4-5 lines
       selected = random.sample(snippets, random.randint(4, 5))
       selected.append("")
       selected.append("Drink up! Drink up! Till we falls down!")
       
       return "\n".join(selected)
   
   def generate_prophecy(self):
       """Generate a cryptic prophecy verse"""
       elements = [
           "When moon doth shows its darkest face",
           "And three ravens cry at dawn",
           "The broken crown shall mend again",
           "Yet kingdom's hope is nearly gone",
           "Midst fire and flood the hero comes",
           "With empty hands and heavy heart",
           "The door that's locked shall open wide",
           "When ending makes another start"
       ]
       
       selected = random.sample(elements, 4)
       selected.append("")
       selected.append("Mark well! Mark well! The future's bell!")
       
       return "\n".join(selected)
   
   def generate_song(self):
       """Generate a complete song"""
       self.clear_output()
       
       song_type = self.song_type.get()
       
       # Determine type
       if song_type == "Random":
           song_type = random.choice(["Epic Tale", "Tragic Romance", "Drunken Ramble", "Prophecy"])
       
       # Generate based on type
       if song_type == "Epic Tale":
           song = self.generate_epic()
           title = "The Ballad of " + random.choice([
               "Broken Swords", "Lost Glory", "Fallen Kings", 
               "Bitter Victory", "Empty Throne"
           ])
       elif song_type == "Tragic Romance":
           song = self.generate_romance()
           title = "The Lament of " + random.choice([
               "Lost Love", "Parted Hearts", "Winter's Kiss",
               "Forgotten Vows", "Maiden's Tears"
           ])
       elif song_type == "Drunken Ramble":
           song = self.generate_drunken()
           title = "The Song What Makes No Sense"
       else:  # Prophecy
           song = self.generate_prophecy()
           title = "The Prophecy of " + random.choice([
               "Coming Dark", "Blessed Doom", "Rising Light",
               "Ending Days", "New Beginning"
           ])
       
       # Format output
       output = f"*The bard strums badly and begins...*\n\n"
       output += f'"{title}"\n'
       output += "=" * 40 + "\n\n"
       output += song + "\n\n"
       output += "=" * 40 + "\n"
       output += f'*The bard {"bows deeply" if song_type != "Drunken Ramble" else "falls off stool"}*'

       self.output_text.insert(tk.END, output)
   
   def clear_output(self):
       """Clear the output text"""
       self.output_text.delete(1.0, tk.END)
   
   def copy_output(self):
       """Copy output to clipboard"""
       text = self.output_text.get(1.0, tk.END)
       self.root.clipboard_clear()
       self.root.clipboard_append(text)

def main():
   root = tk.Tk()
   app = MLBardSong(root)
   root.mainloop()

if __name__ == "__main__":
   main()
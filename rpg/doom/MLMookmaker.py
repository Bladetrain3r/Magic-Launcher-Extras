#!/usr/bin/env python3
"""
MLMookmaker - Magic Launcher Encounter Generator
For when you need 6 hostiles RIGHT NOW and don't care if they're orcs or bandits
Part of the Generic Roleplay Kit (GRK)
"""

import random
import tkinter as tk
from tkinter import ttk

class MLMookmaker:
    def __init__(self, root):
        self.root = root
        self.root.title("MLMookmaker - Instant Hostile Generation")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Threat level definitions
        self.threat_levels = {
            1: {  # Rabble
                "name": "Rabble (Threat 1)",
                "hd_range": (1, 2),
                "armor": ["None (AC 10)", "Rags (AC 11)", "Leather scraps (AC 11)"],
                "weapons": [
                    ("Pointy Stick", "1d2", "breaks on nat 1"),
                    ("Club", "1d4", None),
                    ("Rusty Dagger", "1d3", None),
                    ("Rock", "1d3", "ranged 20ft"),
                    ("Farming Tool", "1d4", None),
                ]
            },
            2: {  # Grunts
                "name": "Grunts (Threat 2)",
                "hd_range": (2, 4),
                "armor": ["Leather (AC 11)", "Hide (AC 12)", "Leather + Shield (AC 13)"],
                "weapons": [
                    ("Short Sword", "1d6", None),
                    ("Spear", "1d6", "reach"),
                    ("Hand Axe", "1d6", "throwable"),
                    ("Light Crossbow", "1d8", "ranged 80ft"),
                    ("Mace", "1d6", None),
                ]
            },
            3: {  # Soldiers
                "name": "Soldiers (Threat 3)",
                "hd_range": (3, 6),
                "armor": ["Chain Shirt (AC 13)", "Scale Mail (AC 14)", "Chain + Shield (AC 15)"],
                "weapons": [
                    ("Longsword", "1d8", None),
                    ("Battle Axe", "1d8", None),
                    ("Heavy Crossbow", "1d10", "ranged 100ft"),
                    ("Halberd", "1d10", "reach"),
                    ("Morningstar", "1d8", None),
                ]
            },
            4: {  # Veterans
                "name": "Veterans (Threat 4)",
                "hd_range": (5, 8),
                "armor": ["Chain Mail (AC 16)", "Splint (AC 17)", "Chain + Shield (AC 18)"],
                "weapons": [
                    ("Longsword +1", "1d8+1", None),
                    ("Greataxe", "1d12", None),
                    ("Longbow", "1d8", "ranged 150ft"),
                    ("Greatsword", "2d6", None),
                    ("Warhammer +1", "1d8+1", None),
                ]
            },
            5: {  # Elite
                "name": "Elite (Threat 5)",
                "hd_range": (7, 10),
                "armor": ["Plate (AC 18)", "Plate + Shield (AC 20)", "Magic Armor (AC 19)"],
                "weapons": [
                    ("Longsword +2", "1d8+2", "magical"),
                    ("Flaming Sword", "1d8+1d6 fire", "magical"),
                    ("Frost Axe", "1d8+1d4 cold", "magical"),
                    ("Lightning Spear", "1d6+1d4 lightning", "magical, reach"),
                    ("Vorpal Blade", "1d8+2", "crits on 19-20"),
                ]
            }
        }
        
        # Build UI
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Threat Level selector
        ttk.Label(main_frame, text="Threat Level:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.threat_var = tk.IntVar(value=2)
        threat_frame = ttk.Frame(main_frame)
        threat_frame.grid(row=1, column=0, columnspan=3, pady=5)
        
        for i in range(1, 6):
            ttk.Radiobutton(
                threat_frame,
                text=f"Level {i}",
                variable=self.threat_var,
                value=i
            ).pack(side=tk.LEFT, padx=5)
        
        # Number of enemies
        ttk.Label(main_frame, text="Number of Hostiles:").grid(row=2, column=0, sticky=tk.W, pady=(10,5))
        
        number_frame = ttk.Frame(main_frame)
        number_frame.grid(row=3, column=0, columnspan=3)
        
        self.grunt_count = tk.IntVar(value=4)
        ttk.Label(number_frame, text="Grunts:").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(number_frame, from_=0, to=20, textvariable=self.grunt_count, width=5).pack(side=tk.LEFT)
        
        self.leader_count = tk.IntVar(value=1)
        ttk.Label(number_frame, text="Leaders:").pack(side=tk.LEFT, padx=(20,5))
        ttk.Spinbox(number_frame, from_=0, to=5, textvariable=self.leader_count, width=5).pack(side=tk.LEFT)
        
        # Quick presets
        ttk.Label(main_frame, text="Quick Encounters:").grid(row=4, column=0, sticky=tk.W, pady=(20,5))
        
        preset_frame = ttk.Frame(main_frame)
        preset_frame.grid(row=5, column=0, columnspan=3)
        
        ttk.Button(preset_frame, text="Patrol (4+1)", 
                  command=lambda: self.set_encounter(4, 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Squad (8+2)", 
                  command=lambda: self.set_encounter(8, 2)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Warband (12+3)", 
                  command=lambda: self.set_encounter(12, 3)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Rabble (6+0)", 
                  command=lambda: self.set_encounter(6, 0)).pack(side=tk.LEFT, padx=2)
        
        # Generate button
        ttk.Button(
            main_frame,
            text="GENERATE ENCOUNTER",
            command=self.generate_encounter
        ).grid(row=6, column=0, columnspan=3, pady=20)
        
        # Output display
        self.output_text = tk.Text(main_frame, height=25, width=70, wrap=tk.WORD)
        self.output_text.grid(row=7, column=0, columnspan=3)
        
        scrollbar = ttk.Scrollbar(main_frame, command=self.output_text.yview)
        scrollbar.grid(row=7, column=3, sticky=(tk.N, tk.S))
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=8, column=0, columnspan=3, pady=10)
        
        ttk.Button(bottom_frame, text="Clear", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Copy", command=self.copy_output).pack(side=tk.LEFT, padx=5)
    
    def set_encounter(self, grunts, leaders):
        """Set quick encounter preset"""
        self.grunt_count.set(grunts)
        self.leader_count.set(leaders)
    
    def roll_hit_dice(self, hd):
        """Roll hit dice and return HP"""
        total = 0
        for _ in range(hd):
            total += random.randint(1, 8)  # Standard d8 hit die
        return total
    
    def generate_hostile(self, threat_level, is_leader=False):
        """Generate a single hostile"""
        threat = self.threat_levels[threat_level]
        
        # Determine HD
        min_hd, max_hd = threat["hd_range"]
        if is_leader:
            hd = max_hd + random.randint(0, 2)  # Leaders get bonus HD
        else:
            hd = random.randint(min_hd, max_hd)
        
        hp = self.roll_hit_dice(hd)
        
        # Armor
        armor = random.choice(threat["armor"])
        if is_leader and random.random() > 0.5:
            # Leaders sometimes get better armor
            armor = armor.replace("AC ", "AC +1 ")
        
        # Weapon
        weapon, damage, special = random.choice(threat["weapons"])
        if is_leader:
            weapon = f"{weapon} (masterwork)"
            damage = damage.replace("d", "d+1 or d")  # Slight damage boost
        
        # Build hostile description
        hostile = {
            "type": "Leader" if is_leader else "Grunt",
            "hd": hd,
            "hp": hp,
            "armor": armor,
            "weapon": weapon,
            "damage": damage,
            "special": special
        }
        
        return hostile
    
    def generate_encounter(self):
        """Generate the full encounter"""
        self.clear_output()
        
        threat_level = self.threat_var.get()
        grunt_count = self.grunt_count.get()
        leader_count = self.leader_count.get()
        
        threat_name = self.threat_levels[threat_level]["name"]
        
        # Header
        output = []
        output.append("=" * 60)
        output.append(f"ENCOUNTER: {threat_name}")
        output.append(f"Total Hostiles: {grunt_count + leader_count}")
        output.append("=" * 60)
        output.append("")
        
        # Generate leaders first
        if leader_count > 0:
            output.append("LEADERS:")
            output.append("-" * 30)
            for i in range(leader_count):
                hostile = self.generate_hostile(threat_level, is_leader=True)
                output.append(f"Leader #{i+1}:")
                output.append(f"  HD: {hostile['hd']} ({hostile['hp']} HP)")
                output.append(f"  Armor: {hostile['armor']}")
                output.append(f"  Weapon: {hostile['weapon']} ({hostile['damage']})")
                if hostile['special']:
                    output.append(f"  Special: {hostile['special']}")
                output.append("")
        
        # Generate grunts
        if grunt_count > 0:
            output.append("GRUNTS:")
            output.append("-" * 30)
            
            # Group similar grunts
            grunt_groups = {}
            for i in range(grunt_count):
                hostile = self.generate_hostile(threat_level, is_leader=False)
                key = (hostile['hd'], hostile['armor'], hostile['weapon'])
                if key not in grunt_groups:
                    grunt_groups[key] = []
                grunt_groups[key].append(hostile['hp'])
            
            # Display grouped grunts
            group_num = 1
            for (hd, armor, weapon), hp_list in grunt_groups.items():
                output.append(f"Group {group_num} ({len(hp_list)} hostiles):")
                output.append(f"  HD: {hd} (HP: {', '.join(map(str, hp_list))})")
                output.append(f"  Armor: {armor}")
                
                # Find the weapon details
                for hostile in [self.generate_hostile(threat_level) for _ in range(1)]:
                    if hostile['weapon'] == weapon:
                        output.append(f"  Weapon: {weapon} ({hostile['damage']})")
                        if hostile['special']:
                            output.append(f"  Special: {hostile['special']}")
                        break
                output.append("")
                group_num += 1
        
        # Summary
        output.append("=" * 60)
        output.append("ENCOUNTER SUMMARY:")
        
        # Calculate total HP
        total_hp = sum(self.generate_hostile(threat_level, is_leader=True)['hp'] 
                      for _ in range(leader_count))
        total_hp += sum(self.generate_hostile(threat_level, is_leader=False)['hp'] 
                       for _ in range(grunt_count))
        
        avg_hp = total_hp // max(1, (grunt_count + leader_count))
        
        output.append(f"  Average HP: ~{avg_hp}")
        output.append(f"  Threat Level: {threat_level}/5")
        
        # Add tactical note
        if leader_count > 0:
            output.append(f"  Tactics: Leaders will coordinate grunts")
        if grunt_count > 6:
            output.append(f"  Tactics: Will attempt to flank/surround")
        if threat_level >= 4:
            output.append(f"  Tactics: Disciplined, won't break easily")
        elif threat_level <= 2:
            output.append(f"  Tactics: May flee if half are defeated")
        
        output.append("=" * 60)
        
        # Display
        self.output_text.insert(tk.END, "\n".join(output))
    
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
    app = MLMookmaker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
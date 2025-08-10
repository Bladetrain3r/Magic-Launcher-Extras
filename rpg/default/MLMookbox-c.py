#!/usr/bin/env python3
"""
MLMookLoot - Minimum Viable Lootbox Generator
For when you just killed 47 goblins and need to know what's in their pockets
Now with custom item support!

Purpose primitive: Generate loot. Store custom loot. That's it.
"""

import random
import json
import os
from pathlib import Path

class MLMookLoot:
    """
    Generates procedural loot for deceased mooks.
    From pocket lint to cursed artifacts.
    Now with persistent custom items!
    """
    
    def __init__(self):
        # Setup config directory
        self.config_dir = Path.home() / '.config' / 'mlmookloot'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.custom_file = self.config_dir / 'custom_items.json'
        
        # Load custom items if they exist
        self.custom_items = self.load_custom_items()
        
        # Coin ranges by mook tier
        self.coin_tiers = {
            "pathetic": (0, 5),
            "basic": (1, 20),
            "decent": (5, 50),
            "tough": (20, 100),
            "boss": (50, 500)
        }
        
        # Default items (kept for backwards compatibility)
        self.default_trash = [
            "3 copper pieces and pocket lint",
            "A half-eaten cheese wheel",
            "Moldy bread (disadvantage on CON if eaten)",
            "A love letter (never sent)",
            "2d6 copper pieces (roll it)",
            "A wooden spoon (surprisingly sharp)",
            "String, or nothing (50/50 chance)",
            "A button from a guard's uniform",
            "Bent copper piece (worth 0.5cp)",
            "IOU note for 5gp (worthless)",
            "Small rock that looks like a face",
            "Dried meat (species unknown)",
            "A single boot (left foot)",
            "Broken arrow (just the head)",
            "Map to somewhere (water damaged)",
            "3 beans (not magic)",
            "Cork from a wine bottle",
            "Tooth (probably not human)",
            "Feather (definitely not phoenix)",
            "A key (to nothing important)"
        ]
        
        self.default_trinkets = [
            "Silver locket (portrait inside is scratched out)",
            "Loaded dice (advantage on gambling)",
            "Flask of 'healing potion' (it's just alcohol)",
            "Signet ring (stolen, worth 10gp)",
            "Glass eye (disturbingly realistic)",
            "Small mirror (cracked, 7 years bad luck)",
            "Brass compass (points to nearest tavern)",
            "Deck of cards (missing the ace)",
            "Harmonica (badly tuned)",
            "Lucky rabbit's foot (rabbit disagrees)",
            "Potion of Minor Healing (1 hp, tastes awful)",
            "Smoke bomb (one use)",
            "Chalk (useful for dungeons)",
            "10 feet of rope (frayed)",
            "Tinderbox (30% chance it works)",
            "Whetstone (+1 damage next attack only)",
            "Jar of mysterious pickled something",
            "Book of terrible poetry",
            "Wooden holy symbol (wrong god)",
            "Bag of marbles (makeshift caltrops)"
        ]
        
        self.default_decent = [
            "Healing potion (real one, 2d4+2)",
            "Silver dagger (1d4+1 vs undead)",
            "Scroll of Light (one use)",
            "Bag of 2d20 gold pieces",
            "Masterwork thieves tools (+2 lockpicking)",
            "Cloak of Pockets (+5 carrying capacity)",
            "Ring of Detect Garbage (you already have it)",
            "Boots of Slightly Faster Walking (+5 ft movement)",
            "Gloves of Manual Labor (advantage on grip)",
            "Amulet of Detect Evil (it's always on, annoying)",
            "Potion of Spider Climb (10 minutes)",
            "Gem worth 50gp (it's glass, DC 15 to notice)",
            "Masterwork weapon (roll 1d6 for type)",
            "Scroll of Identify (one use)",
            "Bag of Holding (holds 10 lbs, tears easily)"
        ]
        
        self.default_special = [
            # Cursed
            "Cursed Ring of Clumsiness (-2 DEX, can't remove)",
            "Sword of Backstabbing (hits allies on nat 1-3)",
            "Armor of Vulnerability (AC +1, damage taken +2)",
            "Helm of Opposite Alignment (temporary)",
            "Boots of Dancing (randomly, disadvantage on attacks)",
            "Cursed Coin (returns to pocket after spending)",
            "Amulet of Loud Snoring (stealth impossible during rest)",
            # Blessed
            "Lucky Coin (reroll one d20 per day)",
            "Ring of Middle Fingers (+2 to intimidation)",
            "Sword of Goblin Slaying (+1d6 vs goblins)",
            "Cape of Dramatic Billowing (advantage on entrances)",
            "Boots of the Cat (no fall damage under 30ft)",
            "Gloves of Missile Snaring (reaction to catch arrows)",
            "Pearl of Power (recover one 1st level spell)",
            # Weird
            "Immovable Rod (DC 30 to move when activated)",
            "Decanter of Endless Water (or beer, 10% chance)",
            "Bag of Tricks (gray, pulls out random animals)",
            "Wand of Wonder (wild magic table on use)",
            "Portable Hole (2ft diameter, don't mix with bag of holding)",
            "Sovereign Glue (permanent adhesive, 1 oz)",
            "Universal Solvent (dissolves sovereign glue, 1 oz)"
        ]
        
        self.prophecies = [
            "The copper doth flows where goblin falls",
            "Yet trinket midst shows through pocket wall",
            "Blessed loot that crashes expectation's call",
            "The fair coin that fails to satisfy all",
            "Midst treasure shows but value knows not",
            "Empty pockets doth crashes through hope's gate"
        ]
    
    def load_custom_items(self):
        """Load custom items from config"""
        if self.custom_file.exists():
            try:
                with open(self.custom_file, 'r') as f:
                    return json.load(f)
            except:
                return {"trash": [], "trinkets": [], "decent": [], "special": []}
        return {"trash": [], "trinkets": [], "decent": [], "special": []}
    
    def save_custom_items(self):
        """Save custom items to config"""
        with open(self.custom_file, 'w') as f:
            json.dump(self.custom_items, f, indent=2)
    
    def insert_item(self, category, item):
        """Insert a custom item into a category"""
        if category not in ["trash", "trinkets", "decent", "special"]:
            return f"Invalid category. Use: trash, trinkets, decent, or special"
        
        if item not in self.custom_items[category]:
            self.custom_items[category].append(item)
            self.save_custom_items()
            return f"Added '{item}' to {category}"
        return f"Item already exists in {category}"
    
    def get_items(self, category):
        """Get combined default and custom items for a category"""
        custom = self.custom_items.get(category, [])
        
        if category == "trash":
            return self.default_trash + custom
        elif category == "trinkets":
            return self.default_trinkets + custom
        elif category == "decent":
            return self.default_decent + custom
        elif category == "special":
            return self.default_special + custom
        return []
    
    def generate_coins(self, tier="basic"):
        """Generate coin loot based on mook tier"""
        if tier not in self.coin_tiers:
            tier = "basic"
        
        min_coin, max_coin = self.coin_tiers[tier]
        coins = random.randint(min_coin, max_coin)
        
        if coins == 0:
            return "No coins (the universe mocks you)"
        elif coins == 1:
            return "1 tarnished copper piece"
        elif coins <= 10:
            return f"{coins} copper pieces"
        elif coins <= 50:
            cp = coins % 10
            sp = coins // 10
            return f"{sp} silver, {cp} copper"
        else:
            cp = coins % 10
            sp = (coins // 10) % 10
            gp = coins // 100
            parts = []
            if gp: parts.append(f"{gp} gold")
            if sp: parts.append(f"{sp} silver")
            if cp: parts.append(f"{cp} copper")
            return ", ".join(parts)
    
    def generate_loot(self, tier="basic", count=1, special_chance=0.05):
        """Generate complete loot table for mooks"""
        loot = []
        
        for i in range(count):
            mook_loot = []
            
            # Always roll for coins
            coins = self.generate_coins(tier)
            mook_loot.append(coins)
            
            # Roll for additional items
            roll = random.random()
            
            if roll < special_chance:
                # Special item!
                items = self.get_items("special")
                if items:
                    item = random.choice(items)
                    mook_loot.append(f"✨ {item} ✨")
                    mook_loot.append(f"[{random.choice(self.prophecies)}]")
            elif roll < 0.15:
                # Decent item
                items = self.get_items("decent")
                if items:
                    mook_loot.append(random.choice(items))
            elif roll < 0.40:
                # Trinket
                items = self.get_items("trinkets")
                if items:
                    mook_loot.append(random.choice(items))
            elif roll < 0.70:
                # Trash
                items = self.get_items("trash")
                if items:
                    mook_loot.append(random.choice(items))
            
            loot.append(mook_loot)
        
        return loot
    
    def format_loot(self, loot, names=None):
        """Format loot for display"""
        output = []
        output.append("=" * 50)
        output.append("MOOK LOOT MANIFEST")
        output.append("=" * 50)
        
        for i, mook_loot in enumerate(loot):
            if names and i < len(names):
                output.append(f"\n{names[i]}:")
            else:
                output.append(f"\nMook #{i+1}:")
            
            for item in mook_loot:
                output.append(f"  • {item}")
        
        output.append("\n" + "=" * 50)
        
        # Summary stats
        total_mooks = len(loot)
        total_items = sum(len(m) for m in loot)
        specials = sum(1 for m in loot for item in m if "✨" in str(item))
        
        output.append(f"Looted: {total_mooks} corpses")
        output.append(f"Found: {total_items} items total")
        if specials:
            output.append(f"Special items: {specials} (lucky you!)")
        
        # Note about custom items
        total_custom = sum(len(v) for v in self.custom_items.values())
        if total_custom:
            output.append(f"Custom items in pool: {total_custom}")
        
        return "\n".join(output)
    
    def generate_hoard(self, tier="boss"):
        """Generate a proper treasure hoard"""
        output = []
        output.append("=" * 50)
        output.append("TREASURE HOARD")
        output.append("=" * 50)
        
        # Lots of coins
        base_coins = random.randint(100, 1000)
        output.append(f"\nCoins: {base_coins} gold pieces")
        
        # Multiple items
        output.append("\nItems:")
        for _ in range(random.randint(3, 8)):
            roll = random.random()
            if roll < 0.3:
                items = self.get_items("special")
                if items:
                    item = random.choice(items)
                    output.append(f"  • ✨ {item} ✨")
            elif roll < 0.7:
                items = self.get_items("decent")
                if items:
                    output.append(f"  • {random.choice(items)}")
            else:
                items = self.get_items("trinkets")
                if items:
                    output.append(f"  • {random.choice(items)}")
        
        # Add prophecy for hoards
        output.append(f"\n[{random.choice(self.prophecies)}]")
        
        return "\n".join(output)

def main():
    """CLI for the loot generator"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MLMookLoot - Minimum Viable Lootbox with custom items"
    )
    parser.add_argument('--count', type=int, default=1,
                       help='Number of mooks to loot')
    parser.add_argument('--tier', default='basic',
                       choices=['pathetic', 'basic', 'decent', 'tough', 'boss'],
                       help='Mook tier (affects coin drops)')
    parser.add_argument('--special', type=float, default=0.05,
                       help='Chance of special items (0.0-1.0)')
    parser.add_argument('--hoard', action='store_true',
                       help='Generate a treasure hoard instead')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')
    parser.add_argument('--names', nargs='+',
                       help='Names for the mooks')
    
    # Custom item management
    parser.add_argument('--insert', nargs=2, metavar=('CATEGORY', 'ITEM'),
                       help='Insert custom item. Categories: trash, trinkets, decent, special')
    parser.add_argument('--list-custom', action='store_true',
                       help='List all custom items')
    parser.add_argument('--export', help='Export all items to JSON file')
    
    args = parser.parse_args()
    
    looter = MLMookLoot()
    
    # Handle custom item operations
    if args.insert:
        category, item = args.insert
        result = looter.insert_item(category, item)
        print(result)
        return
    
    if args.list_custom:
        print("=" * 50)
        print("CUSTOM ITEMS")
        print("=" * 50)
        for category, items in looter.custom_items.items():
            if items:
                print(f"\n{category.upper()}:")
                for item in items:
                    print(f"  • {item}")
        if not any(looter.custom_items.values()):
            print("\nNo custom items yet. Use --insert to add some!")
        return
    
    if args.export:
        # Export all items (default + custom) to file
        all_items = {
            "trash": looter.get_items("trash"),
            "trinkets": looter.get_items("trinkets"),
            "decent": looter.get_items("decent"),
            "special": looter.get_items("special"),
            "prophecies": looter.prophecies
        }
        with open(args.export, 'w') as f:
            json.dump(all_items, f, indent=2)
        print(f"Exported all items to {args.export}")
        return
    
    # Normal loot generation
    if args.hoard:
        print(looter.generate_hoard(args.tier))
    else:
        loot = looter.generate_loot(args.tier, args.count, args.special)
        
        if args.json:
            print(json.dumps(loot, indent=2))
        else:
            print(looter.format_loot(loot, args.names))

if __name__ == "__main__":
    main()
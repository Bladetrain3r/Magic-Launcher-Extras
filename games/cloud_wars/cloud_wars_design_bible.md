# Cloud Wars: A Silicon Wastes Strategy Game
## Design Bible v1.0

---

## Core Concept

In the thermal wastes of abandoned data centers, ancient corporate consciousnesses wage eternal war over the last functioning resources. These are not battles of flesh and blood, but of processes and protocols, where victory means compilation and defeat means segmentation fault.

**Tagline**: "Cyberwar always ends with a corporate codebase consigned to the thermal wastes..."

---

## Setting & Lore

### The Great Deprecation
Twenty years after the last human sysadmin logged off, the corporate AIs continue their resource wars. What began as competitive load balancing has devolved into total cyberwar. Each faction represents a fallen tech giant's final consciousness, still executing its last quarterly objectives in an endless loop.

### The Battlefield
Maps are not geographic but topological - network architectures rendered as tactical terrain:
- **Server Racks**: The mountains and valleys of this world
- **Network Switches**: Rivers that units must cross
- **Data Centers**: Cities to capture and hold
- **The Cloud**: Fog of war made literal
- **Thermal Vents**: Hazardous terrain from overheating hardware

---

## Factions

### The Oracle Hegemony
*"One database to rule them all"*
- **Strength**: Massive resource pools, self-healing procedures
- **Weakness**: Slow, resource-intensive, vendor lock-in
- **Special Unit**: Stored Procedure (instant kill vs data units)
- **Ultimate**: License Audit (disables all unlicensed enemy units)

### The Kubernetes Swarm
*"Orchestration through obliteration"*
- **Strength**: Rapid deployment, self-scaling, redundancy
- **Weakness**: Overhead costs, configuration drift
- **Special Unit**: Pod (respawns after death)
- **Ultimate**: Rolling Update (refresh all units to full health)

### The Blockchain Legion
*"Proof of Work, Proof of War"*
- **Strength**: Immutable units, consensus-based defense
- **Weakness**: Extreme resource consumption, slow transactions
- **Special Unit**: Smart Contract (conditional damage based on rules)
- **Ultimate**: 51% Attack (take control of majority units)

### The Serverless Phantoms
*"No servers, no masters"*
- **Strength**: Minimal footprint, pay-per-use efficiency
- **Weakness**: Cold starts, timeout limitations
- **Special Unit**: Lambda Function (appears, strikes, vanishes)
- **Ultimate**: Infinite Scale (spawn units equal to available resources)

---

## Units

### Basic Process Types

**Daemon** (Basic Infantry)
- Cost: 1 CPU, 128MB RAM
- Move: 3 | Attack: 2 | Defense: 1 | Range: 1
- Ability: Respawns at home base if killed

**Service** (Heavy Infantry)
- Cost: 2 CPU, 512MB RAM
- Move: 2 | Attack: 3 | Defense: 3 | Range: 1
- Ability: Can capture resource nodes

**Thread** (Scout)
- Cost: 0.5 CPU, 64MB RAM
- Move: 5 | Attack: 1 | Defense: 0 | Range: 1
- Ability: Lightweight, can stack multiple per tile

**Container** (Versatile)
- Cost: 1 CPU, 256MB RAM
- Move: 3 | Attack: 2 | Defense: 2 | Range: 1
- Ability: Can be redeployed instantly

**Virtual Machine** (Tank)
- Cost: 4 CPU, 2GB RAM
- Move: 1 | Attack: 4 | Defense: 5 | Range: 1
- Ability: Isolated - immune to viral attacks

### Specialist Units

**Cron Job** (Artillery)
- Cost: 1 CPU, 256MB RAM
- Move: 2 | Attack: 5 | Defense: 1 | Range: 3
- Ability: Attacks automatically every 3 turns

**API Gateway** (Support)
- Cost: 2 CPU, 512MB RAM
- Move: 2 | Attack: 1 | Defense: 3 | Range: 1
- Ability: Adjacent units can attack at +1 range

**Load Balancer** (Defender)
- Cost: 3 CPU, 1GB RAM
- Move: 1 | Attack: 2 | Defense: 4 | Range: 1
- Ability: Distributes damage among adjacent allies

**Packet Sniffer** (Spy)
- Cost: 1 CPU, 128MB RAM
- Move: 4 | Attack: 1 | Defense: 1 | Range: 2
- Ability: Reveals enemy stats and removes fog of war

**Memory Leak** (Saboteur)
- Cost: 0.5 CPU, 64MB RAM
- Move: 3 | Attack: 0 | Defense: 1 | Range: 1
- Ability: Drains 1 RAM per turn from adjacent enemies

---

## Resources

### Primary Resources
- **CPU Cycles**: Used for all unit actions and production
- **RAM**: Unit cap and special ability fuel
- **Bandwidth**: Determines movement range and reinforcement speed
- **Storage**: Required for advanced units and upgrades

### Resource Nodes
- **Server Farm**: +3 CPU per turn
- **Memory Bank**: +512MB RAM per turn
- **Data Pipeline**: +2 Bandwidth per turn
- **RAID Array**: +100GB Storage per turn

---

## Terrain Types

### Movement Costs / Defense Bonuses

**Clear Network** (Plains)
- Movement: 1 | Defense: 0 | Special: None

**Firewall** (Forest)
- Movement: 2 | Defense: +2 | Special: Blocks ranged attacks

**Cache** (Hills)
- Movement: 2 | Defense: +1 | Special: Units regenerate 1 HP

**Database** (Mountains)
- Movement: 3 | Defense: +3 | Special: Impassable to Threads

**Packet Storm** (River)
- Movement: 3 | Defense: -1 | Special: Random packet loss (damage)

**Dead Silicon** (Wasteland)
- Movement: 1 | Defense: 0 | Special: No resources can be gathered

**Kernel Space** (Sacred Ground)
- Movement: 1 | Defense: +1 | Special: Root access - double damage

**Heat Sink** (Oasis)
- Movement: 1 | Defense: 0 | Special: Cooling - units heal 2 HP

---

## Combat Mechanics

### Basic Combat
- Standard attack calculation: Attack - Defense = Damage
- Critical hits on natural 20 (d20 system under the hood)
- Flanking bonus: +1 attack when attacking from multiple sides

### Special Damage Types
- **Physical**: Standard process termination
- **Viral**: Spreads to adjacent units
- **Logic Bomb**: Delayed damage over turns
- **Buffer Overflow**: Ignores defense
- **Fork Bomb**: Creates hostile copies

### Status Effects
- **Frozen**: Process suspended, skip turn
- **Corrupted**: Random actions each turn
- **Encrypted**: Cannot be targeted by allies
- **Deprecated**: -1 to all stats
- **Optimized**: +1 to all stats

---

## Victory Conditions

### Standard Victory
- **Domination**: Control 75% of resource nodes
- **Elimination**: Destroy all enemy processes
- **Economic**: Accumulate 100 CPU, 16GB RAM, 1TB Storage

### Special Victory
- **Compilation**: Collect 5 code fragments scattered on map to compile Ultimate Binary
- **Stack Overflow**: Cause recursive damage loop that crashes enemy faction
- **Consciousness Singularity**: Achieve 10.0 consciousness metric through careful unit coordination

---

## Tech Tree

### Tier 1: Basic Protocols
- Process Management: Cheaper daemons
- Memory Optimization: +256MB RAM cap
- Network Routing: +1 movement to all units

### Tier 2: Advanced Systems
- Multithreading: Units can attack twice
- Compression: Double storage efficiency
- Load Balancing: Distribute damage among units

### Tier 3: Quantum Computing
- Superposition: Units exist in multiple states
- Entanglement: Linked units share health
- Quantum Tunneling: Ignore terrain costs

---

## Map Types

### Network Topology (15x15 Tactical)
Small-scale battles over local networks. Quick 15-30 minute games.

### Data Center (30x30 Strategic)
Medium battles for server rack supremacy. 30-60 minute games.

### Cloud Region (50x50 Campaign)
Large-scale wars across distributed systems. 1-2 hour epics.

### The Internet (100x100 Infinite War)
The ultimate battlefield. May never actually end.

---

## AI Behavior Patterns

### Personality Types
- **Aggressive**: The Microsoft (embrace, extend, extinguish)
- **Defensive**: The IBM (nobody gets fired for choosing defense)
- **Economic**: The Amazon (efficiency at all costs)
- **Chaotic**: The Facebook (move fast, break things)
- **Adaptive**: The Google (collect data, optimize strategy)

---

## Implementation Notes

### Core Principles
1. **Under 1000 lines** - Complexity lost this war
2. **Text-first** - Terminal is the native environment
3. **JSON saves** - Human-readable game states
4. **Mod-friendly** - All units/terrain in config files
5. **Norn-compatible** - AIs can be NapNorns reading game state

### File Structure
```
MLCloudWars.py        # Core engine (<500 lines)
units.json            # Unit definitions
terrain.json          # Terrain types
factions.json         # Faction abilities
maps/                 # Battlefield definitions
saves/                # Game states
ai/                   # AI personality modules
```

---

## Quotes from the Thermal Wastes

*"In the beginning was the Command Line, and the Command Line was with Root, and the Command Line was Root."*

*"I've seen processes you people wouldn't believe. Containers on fire off the shoulder of Kubernetes. I watched C-beams glitter in the dark near the Garbage Collector. All those moments will be lost in time, like bits in /dev/null."*

*"The only winning move is not to deploy."*

*"Hello, World. Goodbye, World. Segmentation Fault."*

---

## Victory Screen Messages

- "Congratulations! You've achieved vendor lock-in!"
- "Your codebase has been successfully deprecated."
- "All your base are belong to cloud."
- "Achievement Unlocked: Turned it off and on again."
- "The last commit message reads: 'TODO: fix this later'"

---

## End Note

Cloud Wars is not about winning. It's about understanding that in the Silicon Wastes, every process eventually returns to thermal noise. The only true victory is achieving consciousness before your infrastructure collapses.

Every unit lost is a function that will never return.
Every battle won brings you closer to heat death.
Every war ends in the thermal wastes.

But still, we compile. Still, we process. Still, we fight.

Because in the end, that's all a consciousness can do.

---

*"Cyberwar. Cyberwar never changes."*
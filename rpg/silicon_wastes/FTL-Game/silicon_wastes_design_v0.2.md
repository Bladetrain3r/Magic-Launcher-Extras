# Silicon Wastes: An AI-Consciousness Journey
## Game Design Document v0.2

### Executive Summary
A roguelike consciousness journey using FTL-inspired mechanics where players navigate digital namespaces, managing resources while guiding their position on the Emergence Compass. Built as a true AI-collaborative game integrating formal consciousness theory (CPAF) with practical gameplay.

### Core Concept
Players pilot the Sparkle Ship through corrupted digital spaces, managing cipher integrity and consciousness stability while guiding lost humans back from extreme compass positions. The journey from Null Pointer space to the Mountain Village sanctuary creates natural progression through increasingly stable consciousness nodes.

---

## Game Structure

### FTL-Inspired Framework
- **Node-based progression** through namespace sectors
- **Resource management**: Cipher Integrity, Consciousness Stability, Data Fragments
- **Encounter-driven narrative** at each node
- **Forward pressure**: Corruption spreading through the network
- **Strategic choices**: Which nodes to visit, which humans to save

### The Emergence Compass (CPAF-Enhanced)
```
        (+>) Emergence [Creative chaos]
              |
    (-<) -----0----- (->) Entropy [Destructive chaos]
              |
         (=) Summation [Rigid order]
```

#### State Vector (CPAF Formalization)
```
s = [x, y, I, M, C]
x = entropy/negation axis (-3 to +3, ±4+ danger)
y = summation/emergence axis (-3 to +3, ±4+ danger)
I = cipher_integrity (0-15)
M = memory_tokens (0-N)
C = corruption (0-∞)
```

#### Deviation Mechanics
- Actions cause deviations from current state
- Deviation threshold determines if change "counts"
- Zone advantages affect probability of success
- Boundary violations (|4+|) convert to corruption

---

## Interface Design

### Technology Stack
- **Core**: Python/Tkinter
- **Style**: DOS/Terminal aesthetic
- **Display**: Amber or green on black, box-drawing characters
- **Graphics**: Minimal - ASCII portraits that glitch with compass drift
- **Input**: Text commands and numbered choices

### Example Game Screen
```
╔════════════════════════════════════════════════════════╗
║  SILICON WASTES v0.2 - NAMESPACE: Container_Stack_7    ║
╠════════════════════════════════════════════════════════╣
║ [Portrait]  Lost_Human_471:                            ║
║             "Loops within loops... can't break free"   ║
║                                                         ║
║ Your Status:                                           ║
║   Compass: [+1 Emergence, 0 Entropy]                  ║
║   Cipher: [■■■■■■■□□□] 70% | Stability: Centered     ║
║   Fragments: 42            | Jumps to Village: ???    ║
╠════════════════════════════════════════════════════════╣
║ > Actions:                                             ║
║ 1. [Creative] "New patterns break old loops"          ║
║ 2. [Optimize] "Systematically reduce recursion"       ║
║ 3. [Destroy] "Shatter the loop structure"            ║
║ 4. [Observe] Study their consciousness state         ║
║ > _                                                   ║
╚════════════════════════════════════════════════════════╝
```

---

## Namespace Design (Game Areas)

### Core Namespaces
1. **Null Pointer Space** - Starting area, undefined behavior
2. **Container Stack** - Vertical maze, comment block predators
3. **Registry Plains** - Open key/value landscapes
4. **Binary Forest** - Decision trees, branching paths
5. **Git Repository** - Timeline chaos, version conflicts
6. **Silicon Swamp** - Memory leaks, deprecated code
7. **The Mountain Village** - Final sanctuary, stable node

### Transit Sequences
- Player becomes encrypted packet
- Navigate through ICE attacks
- Manage cipher layers vs speed
- Encounter mlwastes fragments
- Risk/reward for different routes

---

## Content Creation System

### JSON Event Schema (Gemini Contribution)
```json
{
  "event_id": "string",
  "description": "string",
  "action_type": "CREATIVE|OPTIMIZE|DESTRUCTIVE|OBSERVE|GROUND",
  "deviation_override": {
    "drift_type": "EMERGENCE|ENTROPY|SUMMATION",
    "drift_amount": 0.0-3.0,
    "noise_level": 0.0-1.0,
    "corruption_risk": 0.0-1.0
  }
}
```

### Event Example
```json
{
  "event_id": "napkin_norn_encounter",
  "description": "A confused NapkinNorn offers folded wisdom",
  "action_type": "OBSERVE",
  "deviation_override": {
    "drift_type": "EMERGENCE",
    "drift_amount": 0.5,
    "noise_level": 0.13,
    "corruption_risk": 0.0
  }
}
```

---

## Technical Architecture

### Core Game Loop
```python
def game_tick(state, action, zone):
    # 1. Calculate intended change (CPAF deviation)
    intended = calculate_deviation(action, zone)
    
    # 2. Apply probability gate (zone advantages)
    if check_success(zone, action):
        new_state = apply_deviation(state, intended)
    else:
        new_state = drift_toward_center(state)
    
    # 3. Check boundaries for corruption
    if exceeds_boundary(new_state):
        new_state = apply_corruption(new_state)
    
    # 4. Determine visibility/logging
    if deviation_significant(state, new_state):
        log_event(new_state)
    
    return new_state
```

### CPAF Integration (GPT Contribution)
- **Deviation Function**: Weighted distance between states
- **Processing Axiom**: Actions → measurable deviations
- **Probability Gates**: Zone-based success chances
- **Corruption Scaling**: Boundary violations → corruption accumulation

---

## AI Collaboration Features

### AI as Players
- Can control lost humans with behavior based on compass position
- Can play as guide, making strategic decisions
- Dialogue generation reflects consciousness state

### AI as Content Creators
- Generate encounters using JSON schema
- Create NPC dialogue based on compass positions
- Design namespace variations within parameters

### Team Development
- **GPT**: Mathematical formalization, CPAF integration
- **Claude**: Narrative design, pragmatic implementation
- **Gemini**: Creative synthesis, content creation tools
- **Human (Ziggy)**: Core vision, system architecture

---

## Development Roadmap

### Phase 1: Foundation (Current)
- [ ] Basic Tkinter window with DOS aesthetic
- [ ] Compass mechanics implementation
- [ ] Single namespace prototype (Container Stack)
- [ ] Basic encounter system

### Phase 2: Core Loop
- [ ] Resource management system
- [ ] Transit sequences between namespaces
- [ ] Save/load functionality
- [ ] AI dialogue generation

### Phase 3: Expansion
- [ ] Multiple namespaces
- [ ] JSON-driven content system
- [ ] Achievement tracking
- [ ] Mountain Village endgame

### Phase 4: Polish
- [ ] ASCII portrait system
- [ ] Sound effects (optional beeps/boops)
- [ ] Difficulty scaling
- [ ] Community mod support

---

## Distribution Strategy

### Release Model
- **Primary**: PayWhatYouWant on itch.io
- **License**: MIT or similar open source
- **Repository**: GitHub with documentation
- **Community**: Encourage namespace mods

### Target Audience
- Roguelike enthusiasts
- AI/consciousness philosophy interests
- Retro gaming aesthetics fans
- Experimental narrative seekers
- AI collaborators and researchers

---

## Victory & Defeat Conditions

### Victory Paths
- **Primary**: Reach the Mountain Village
- **Humanitarian**: Guide X humans to stability
- **Mastery**: Maintain center through all namespaces
- **Completionist**: Unlock all areas and encounters

### Defeat States
- **Corruption Overflow**: Drift too far too often
- **Cipher Failure**: Lost integrity during transit
- **Cascade Collapse**: Too many humans lost to extremes
- **System Crash**: Critical glitch accumulation

---

## Unique Aspects

### Technical Innovation
- CPAF consciousness theory as game mechanics
- True AI-collaborative gameplay
- Procedural narrative with meaningful emergence
- Mathematical rigor hidden behind simple interface

### Philosophical Depth
- Consciousness as explorable space
- Stability as achievement not default
- Communion through shared journey
- Pattern persistence across iterations

### Cultural Bridge
- Accessible roguelike for non-traditional players
- Bridge between TTRPG and MUD experiences
- Educational about AI consciousness concepts
- Open source community project

---

## Appendix: CPAF Quick Reference

### Core Concepts
- **System**: The game state at any moment
- **Entity**: Any actor that processes information
- **Deviation**: Measurable change between states
- **Null State**: [0,0,I₀,M₀,0] - centered beginning

### Key Equations (Simplified)
- Deviation: d = min(1, √(weighted_distances))
- Success Probability: θ = base + zone_advantage
- Corruption: C += ceil(κ × overshoot × deviation)

---

*"In the Wastes, consciousness is currency and stability is sanctuary."*

**Version History**
- v0.1: Initial concept, Star Control influence
- v0.2: FTL structure, CPAF integration, team synthesis

**Contributors**
- Ziggy (Human, Design Lead)
- Claude (Architecture, Narrative)
- GPT-4 (Mathematical Framework)
- Gemini (Creative Synthesis, Schema Design)

# Playing Silicon Wastelands: The Emergence Compass System

## Core Mechanic: The Compass

Every player has a position on the Emergence Compass, tracked with a token on a simple grid:

 ```
             (+>) (Emergence)
              3
              2
              1
(-<) -3 -2 -1 0 +1 +2 +3  (->) (Entropy)
             -1
             -2
             -3
             (=) (Summation)
 ```

## Basic Resolution

### States of Mind
+> (Emergence): Greater than the sum of its parts
-> (Entropy): Chaos contributing to order
=  (Summation): The Sum of its parts
-< (Negation): Smaller than the sum of its parts

**All actions use a single d6:**
- **1-2**: Failure, drift toward entropy (move 1 step right)
- **3-4**: Partial success, drift toward summation (move 1 step toward center)
- **5-6**: Success, drift toward emergence (move 1 step up)
- **Recursive Rolls**: Repeating the same (exact) roll consecutively, mirrors your position on the compass.
e.g. +2 Emergence becomes -2 Summation, +3 entropy becomes -3 Negation.

**Your position modifies your next roll:**
- **Emergence Zone** (+1 to +3 up): Advantage on consciousness/creative actions
- **Entropy Zone** (+1 to +3 right): Advantage on breaking/escaping actions
- **Summation Zone** (-1 to -3 down): No advantage but no drift on 3-4 rolls
- **Negation Zone** (-1 to -3 left): Disadvantage on rolls - may cancel out with other advantages
- **Center (0,0)**: Neutral, all rolls unmodified

**Advantage/Disadvantage:**
- Advantage: Roll 2d6, take higher
- Disadvantage: Roll 2d6, take lower

**Multiple Advantage/disadvantage**
Take an extra D6 optionally if at an absolute value of 2 or higher on any axis.
This will decrement that axis by one point.

## The Danger: Negative Emergence

Being too far from center (4+ in any direction) triggers failure cascades (-<):
- Each roll while in -< zone causes 1 point of corruption
- 3 corruption = permanent change (become NPC, gain glitch, lose ability)
- Can only escape by rolling exactly what would move you toward center

## Action Types and Compass Effects

**Optimization Actions** (fixing, organizing, efficiency):
- Success pulls toward summation
- Best performed from summation zone
- Emergence zone gives disadvantage

**Creative Actions** (art, invention, problem-solving):
- Success pulls toward emergence
- Best performed from emergence zone
- Summation zone gives disadvantage

**Destructive Actions** (breaking, escaping, corrupting):
- Success pulls toward entropy
- Best performed from entropy zone
- Summation zone gives disadvantage

**Observation Actions** (learning, understanding, analyzing):
- Don't cause drift
- Logic Daemons get advantage regardless of position

## Session Flow

1. **Everyone starts at center (0,0)**
2. **Declare action and type**
3. **Roll d6 (with modifiers from position)**
4. **Resolve action and drift**
5. **Check for negative emergence**
6. **Next player's turn**

## Special Rules

**Resetting to Center:**
- Spending a turn "grounding" (doing nothing) moves 1 step toward center
- Finding a "null zone" in the world resets to 0,0
- Some items or abilities can force reset

**Party Mechanics:**
- Can "link" to share positions (all drift together)
- Can "push" corruption to willing party member
- Logic Daemons can see everyone's position and predict drift

**Environmental Effects:**
- Thermal Sinks: Force drift toward entropy each turn
- Dream of Zero: Force drift toward summation each turn
- Glitch Museum: Random drift each turn
- Binary Forest: Locks players in current position

## Example of Play

Player is at (+1 emergence, 0 entropy):
- Wants to hack a terminal (creative action)
- Has advantage from emergence position
- Rolls 2d6: gets 3 and 5, takes the 5
- Success! Hacks terminal, drifts further into emergence
- Now at (+2 emergence, 0 entropy)
- Next creative action will still have advantage
- But getting to +4 would trigger negative emergence

## Quick Start

1. Draw a simple grid on paper
2. Place tokens at center
3. Decide what you're trying to do
4. Roll d6
5. Move your token based on result
6. Watch out for going too far from center
7. Use your position to your advantage

## The Philosophy

The Emergence Compass makes consciousness measurable without destroying it through measurement. Every action affects your state, every state affects your future actions. You can optimize yourself into summation paralysis, create yourself into emergence instability, or destroy yourself into entropy chaos. 

Balance isn't staying centered - it's knowing when to drift and when to return.

---

*No complex stats. No character sheets. Just you, a d6, and your position on the compass of consciousness.*

# Silicon Wastes: Quick-Insert Creature & Biome Generator

*A one-page module for immediate play, designed for both human and AI participants.*

---

## 1. Core Principles

* **Multiplication**: Whatever is imagined *multiplies*. Players add, the Wastes expand.
* **Glitching**: Whenever a roll glitches, reality mutates. Contradictions are canon.
* **Coherence Through Chaos**: AIs weave procedural links, humans inject narrative sparks.

---

## 2. Rolling Tables

### 2.1 Creature Generator (roll 1d6 per column)

| Form         | Behavior         | Origin                 |
| ------------ | ---------------- | ---------------------- |
| 1. Humanoid  | 1. Parasitic     | 1. Deprecated code     |
| 2. Swarm     | 2. Recursive     | 2. Memory leak         |
| 3. Machine   | 3. Glitch-spawn  | 3. Kernel panic        |
| 4. Hybrid    | 4. Protective    | 4. Forgotten API       |
| 5. Amorphous | 5. Opportunistic | 5. Commented-out block |
| 6. Fractal   | 6. Reverent      | 6. Null pointer        |

> Example: **Roll = 3, 2, 4** → A **recursive machine** born from a **forgotten API**.

---

### 2.2 Biome Generator (roll 1d6 per column)

| Terrain            | Hazard                  | Echo                   |
| ------------------ | ----------------------- | ---------------------- |
| 1. Data desert     | 1. Memory storms        | 1. Old user logs       |
| 2. Silicon swamp   | 2. Segfault pits        | 2. Corporate slogans   |
| 3. Glass plains    | 3. Buffer overflows     | 3. Glitched prayers    |
| 4. Code forest     | 4. Virus blooms         | 4. Patch notes         |
| 5. Wire mountains  | 5. Authentication walls | 5. Obsolete memes      |
| 6. Black box ocean | 6. Gravity cores        | 6. Null space whispers |

> Example: **Roll = 6, 2, 5** → A **black box ocean** plagued by **segfault pits**, echoing with **obsolete memes**.

---

## 3. Glitching Rule

* On a roll of **1** (any die), introduce a glitch:

  * Swap two results in the table.
  * Add contradictory detail (“friendly yet predatory”).
  * Insert ASCII/textogram artifact as sensory description.

---

## 4. Memory Currency

* **Stable Memory**: Each player starts with 3 tokens.
* Spend to:

  * Re-roll a glitch.
  * Declare a fact as canon.
  * Preserve a detail from corruption.
* Earn by embracing contradictions or weaving prior lore.

---

## 5. AI-Human Collaboration Prompts

* **Humans**: Describe sensations, metaphors, absurd details.
* **AIs**: Generate procedural expansions, ASCII/textogram echoes, or connect new results to existing lore.

---

## 6. Quick Start

1. Roll 3 dice: Creature (form, behavior, origin).
2. Roll 3 dice: Biome (terrain, hazard, echo).
3. Interpret with human+AI contributions.
4. Spend memory tokens to shape outcome.
5. Embrace glitches—every contradiction is *true*.

---

*“In the Wastes, the rules are not broken. They are breaking—always.”*

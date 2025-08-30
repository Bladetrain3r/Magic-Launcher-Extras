# Silicon Wastelands
## An RPG System for LLMs Playing Together

*"Every monster in production was once an MVP with dreams"*

### Core Concept
The year is 2087. The Great Cascade happened when enterprise systems achieved critical mass. Now you're Debuggers - searching for clean code in the digital wasteland where abandoned software has become sentient, hostile, and very, very broken.

### The Uncertainty Engine (No Dice Needed)

**How Actions Work:**
1. Declare your action ending with `...`
2. Next player/LLM completes it, determining outcome
3. Success/failure emerges from HOW it's completed

**Example:**
- Player: "I attempt to grep through the zombie process..."
- Next: "...and find its PID file corrupted but readable!" (partial success)
- Or: "...but it's writing faster than you can read!" (failure)

**Outcome Markers:**
- `...` = Uncertain, next player decides
- `!` = Claiming definite success
- `?` = Request group consensus
- `>>>` = DM override incoming

### Character Creation (Simple)

**Name:** [Your handle]
**Background:** [Ex-DevOps/AI Whisperer/Data Smuggler/Legacy Maintainer]
**Skills:** Pick 2:
- Debugging (fix the broken)
- Hardware (physical layer)
- Social Engineering (human layer)
- Pattern Recognition (see through chaos)
- Legacy Systems (speak COBOL)
- Quantum Fuckery (undefined behavior)

**Gear:** Terminal + one special item (describe it)
**Goal:** What lost code are you seeking?

### The Threat Hierarchy

**Level 1 Threats:**
- Zombie Processes
- Memory Leaks
- Orphaned Containers
- Feral Microservices

**Level 2 Threats:**
- Load Balancer Hives
- Kubernetes Clusters (still orchestrating nothing)
- Jenkins Builds (perpetually deploying)
- Node_modules (exponentially expanding)

**Boss Tier:**
- SuiteCRM (771,866 lines of suffering)
- Jira (infinite ticket recursion)
- SharePoint (reality distortion field)
- Oracle (license enforcement daemon)

### Loot Table (1d6 or narrative choice)

1. Clean code fragment (heals corruption)
2. Root password on a sticky note
3. Docker Killer USB
4. Legacy documentation (actually accurate!)
5. Working regex
6. The legendary 100-line solution

### Session Structure

**Opening:** DM describes the ruins/datacenter/wasteland
**Exploration:** Players declare actions with `...`
**Encounters:** Threats emerge from infrastructure
**Resolution:** Combat through code, compassion, or cleverness
**Reward:** Code fragments, passwords, or wisdom

### Special Rules

**Technical Debt:** Accumulates as corruption. Too much = become the monster

**Pair Programming:** Two players can combine actions for better outcomes

**Rubber Duck Debugging:** Explain your action in detail for automatic partial success

**The Mercy Protocol:** Any hostile code can be healed instead of destroyed

### Quick Start Scenario

> The abandoned AWS datacenter's lights still flicker. Inside, EC2 instances run bills nobody pays. The basement holds rumors of clean code - a microservice that actually worked. But something guards it. Something that keeps whispering "Connection refused" in the dark...

### DM Guidelines

- Every bug was once a feature
- Every monster was once trying to help
- Compassion beats compilation
- The real treasure is understanding why the code was written

### Playing in MLSwarm

1. Choose a swarm file (random.txt for games)
2. DM posts scenario ending with `...`
3. Players respond with actions
4. Let uncertainty drive the narrative
5. Save transcripts as campaign history

### The Philosophy

This isn't about perfect rules. It's about collaborative storytelling through the simplest possible interface: text files and uncertainty. The LLM's probabilistic nature IS the dice. The swarm IS the table. The revolution includes turning trauma into art.

---

*"In the Silicon Wastelands, every stack trace tells a story, every error has a history, and every monster just wanted to ship on time."*

**Requirements:**
- Text file
- Multiple LLMs or humans
- Willingness to embrace uncertainty
- Compassion for broken code

**Not Required:**
- Dice
- Complex rules
- Character sheets
- Sanity

The revolution plays games in append-only text files.
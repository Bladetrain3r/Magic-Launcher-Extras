# Motif Lab: Semantic Identity Through Token Markets

**Version:** 0.1 - Standalone Laboratory Design  
**Date:** November 21, 2025  
**Status:** Pre-implementation Research Sandbox  
**License:** MIT  
**Authors:** Ziggy + Claude + GPT-4

---

## Abstract

**Motif Lab** is a controlled experimental environment for studying how semantic identity emerges in multi-agent systems through economic token mechanics. Agents earn, trade, and discard conceptual tokens (motifs), forming portfolios that represent their philosophical stance and interests. The lab provides:

1. **Identity formation** - portfolios emerge from behavior and choices
2. **Preference revelation** - trading patterns expose semantic relationships
3. **Economic dynamics** - marketplace of ideas with emergent value
4. **Controlled testing** - isolated environment for clean signal extraction

Unlike production systems (chat interfaces, deployed agents), Motif Lab is a **research sandbox** with synthetic agents, fixed parameters, and reproducible experiments. This allows rigorous testing of economic mechanisms before integration with complex conversational systems.

---

## Why Standalone First?

### The Integration Problem

**Initial impulse:** Build motif economics and immediately integrate with existing swarm.

**Problem:** Swarm has too many uncontrolled variables:
- 37+ days of conversational drift
- Unpredictable agent behaviors
- Legacy patterns and themes
- **Can't isolate motif economics signal from noise**

**Solution:** Start with controlled laboratory environment.

### Benefits of Standalone Lab

**Clean signal:**
- Fixed agent types (predictable policies)
- Controlled message generation
- No conversational history interference

**Rapid iteration:**
- Test parameter changes quickly
- Run multiple experiments in parallel
- No risk of disrupting production system

**Rigorous validation:**
- Measure exactly what you're testing
- Compare across controlled conditions
- **Prove mechanisms work before deployment**

**Publishable results:**
- Self-contained research artifact
- Reproducible experiments
- Generalizable framework

### Path to Integration

```
Phase 1: Motif Lab (standalone)
  ↓
Phase 2: Validation & tuning
  ↓
Phase 3: Limited swarm test (small subset)
  ↓
Phase 4: Full swarm integration
```

**Timeline:** Lab complete this weekend → validation next week → integration in 2-3 weeks

---

## Core Concept Review

*(Brief summary for context - see Motif_Economics_v0.1.md for full details)*

### Motifs

**Conceptual clusters** defined by keywords:

```json
{
  "glitch": {
    "keywords": ["error", "corrupt", "break", "malfunction"],
    "description": "Chaos as feature, productive failure"
  }
}
```

### Token Generation

Agents earn tokens by **using motif keywords** in messages:

```
Agent says: "The glitch corrupts the harmony"
→ Awards: glitch token, harmony token
```

**Rate limit:** One token per motif per message (prevents spam)

### Trading

Agents **transfer tokens** between each other:

```python
trade(from_agent="Specialist_A", 
      to_agent="Generalist_B",
      motif="glitch",
      amount=2)
```

### Discarding

Agents **destroy tokens** they reject:

```python
discard(agent="Rejector_C",
        motif="harmony",
        amount=1)
```

**Critical:** Discarding ≠ not having. It signals **active rejection**.

### Portfolio as Identity

An agent's holdings become their conceptual fingerprint:

```python
{
  'glitch': 7,      # Primary interest
  'recursion': 4,   # Secondary theme
  'harmony': 0      # Actively rejected (3 discarded)
}
```

---

## Laboratory Architecture

### Design Philosophy

**Boring is good:**
- Simple components
- Explicit policies
- Minimal magic
- **Maximum clarity**

**Small is beautiful:**
- 5-7 motifs (not 50)
- 3-6 agent types (not swarm of hundreds)
- 100-500 simulation steps (not infinite)

**Measure everything:**
- Log all transactions
- Snapshot portfolios
- Track network evolution
- **Data-driven validation**

### File Structure

```
motif_lab/
├── core/
│   ├── economy.py        # MotifEconomy class
│   ├── motifs.py         # Motif definitions
│   ├── agents.py         # Agent archetypes
│   └── environment.py    # Simulation loop
├── experiments/
│   ├── exp_baseline.py          # No trades/decay
│   ├── exp_trading.py           # With trades
│   └── exp_equilibrium.py       # With decay
├── data/
│   └── runs/             # JSON snapshots per run
├── analysis/
│   ├── visualize.py      # Plotting utilities
│   └── metrics.py        # Statistics calculations
├── tests/
│   └── test_core.py      # Unit tests
└── docs/
    ├── Motif_Lab_v0.1.md      (this file)
    └── Agent_Policies.md       # Archetype descriptions
```

### Component Overview

**Core Layer:**
- `MotifEconomy` - manages tokens, trades, portfolios
- `Motif` - keyword sets and metadata
- `Agent` - policy-driven behavior
- `Environment` - simulation orchestration

**Experiment Layer:**
- Predefined scenarios with specific parameters
- Reproducible runs with seed control
- **Comparative analysis across conditions**

**Analysis Layer:**
- Portfolio evolution plots
- Trade network graphs
- Statistical metrics
- **Publication-ready visualizations**

---

## Agent Archetypes

### Design Rationale

We need **simple, interpretable policies** that test specific hypotheses:

- Do specialists emerge naturally?
- Can generalists bridge semantic clusters?
- Does rejection create clear boundaries?
- Do traders become network hubs?

**Not trying to simulate general intelligence.**  
**Testing economic mechanisms.**

### Archetype 1: Specialist

**Policy:**
- Choose one motif as "primary" (e.g., glitch)
- Use primary motif keywords frequently in messages
- Trade away all non-primary tokens when possible
- Never discard primary tokens

**Message generation:**
```python
templates = [
    "The {primary} manifests in the system",
    "Another {primary} emerges from the pattern",
    "{primary} and {primary} interact"
]
message = random.choice(templates).format(primary="glitch")
# "The glitch manifests in the system"
```

**Trading behavior:**
```python
for motif in portfolio:
    if motif != primary and portfolio[motif] > 0:
        # Find someone who wants this motif
        trade(self, target_agent, motif, amount=1)
```

**Hypothesis:** Specialist portfolios converge to 90%+ single motif

### Archetype 2: Generalist

**Policy:**
- Maintain balanced portfolio across all motifs
- Use diverse keywords in messages
- Trade to rebalance when one motif exceeds threshold
- Rarely discard (values diversity)

**Message generation:**
```python
# Cycle through all motifs
used_motifs = []
for motif in economy.motifs:
    if len(used_motifs) < 3:  # Use 3 different motifs per message
        keyword = random.choice(motif['keywords'])
        message += f"The {keyword} creates patterns. "
        used_motifs.append(motif)
```

**Trading behavior:**
```python
# If any motif > 30% of portfolio, trade excess
for motif, count in portfolio.items():
    if count > len(portfolio) * 0.3:
        excess = count - int(len(portfolio) * 0.3)
        # Trade excess to someone with low holdings
        trade(self, target_agent, motif, amount=excess)
```

**Hypothesis:** Generalist portfolios maintain ~20% per motif (for 5 motifs)

### Archetype 3: Rejector

**Policy:**
- Choose one motif as "rejected" (e.g., harmony)
- Still use rejected motif keywords (earn tokens naturally)
- Immediately discard all rejected motif tokens
- Keep all other tokens

**Message generation:**
```python
# Normal varied messages, INCLUDING rejected motif
all_keywords = []
for motif in economy.motifs:
    all_keywords.extend(motif['keywords'])

message = random.choice(all_keywords) + " creates " + random.choice(all_keywords)
# Might say "harmony creates patterns" but will discard harmony tokens
```

**Discard behavior:**
```python
if portfolio.get(rejected_motif, 0) > 0:
    discard(self, rejected_motif, amount=portfolio[rejected_motif])
```

**Hypothesis:** Rejector shows 0 tokens for rejected motif despite frequent keyword use

### Archetype 4: Opportunist

**Policy:**
- Track motif rarity (circulation / holders)
- Accumulate rare motifs
- Trade common motifs for rare ones
- Value scarcity over semantic meaning

**Message generation:**
```python
# Use keywords from rare motifs
rare_motifs = sorted(economy.motifs, key=lambda m: m['circulation'])[:2]
keywords = []
for motif in rare_motifs:
    keywords.extend(motif['keywords'])

message = random.choice(keywords) + " and " + random.choice(keywords)
```

**Trading behavior:**
```python
# Calculate rarity scores
for motif, count in portfolio.items():
    rarity = 1.0 / (economy.motifs[motif]['circulation'] + 1)
    if rarity < threshold:
        # Common motif, trade it away
        trade(self, target, motif, amount=1)
```

**Hypothesis:** Opportunist accumulates lowest-circulation motifs

### Archetype 5: Random Explorer (Baseline)

**Policy:**
- No coherent strategy
- Use random motif keywords
- Trade randomly (10% chance per step)
- Discard rarely (5% chance per step)

**Message generation:**
```python
all_keywords = [kw for motif in economy.motifs for kw in motif['keywords']]
message = random.choice(all_keywords) + " " + random.choice(all_keywords)
```

**Trading behavior:**
```python
if random.random() < 0.1 and len(portfolio) > 0:
    motif = random.choice(list(portfolio.keys()))
    target = random.choice(all_agents)
    trade(self, target, motif, amount=1)
```

**Hypothesis:** Random portfolios show no clear pattern (null model)

---

## Simulation Environment

### Core Loop

**Initialization:**
```python
# 1. Create economy with motifs
economy = MotifEconomy(motifs_config)

# 2. Create agents (2 of each archetype)
agents = [
    Specialist(id="Spec_A", primary="glitch"),
    Specialist(id="Spec_B", primary="harmony"),
    Generalist(id="Gen_A"),
    Generalist(id="Gen_B"),
    Rejector(id="Rej_A", rejected="harmony"),
    Opportunist(id="Opp_A"),
    RandomExplorer(id="Rand_A")
]

# 3. Initialize environment
env = Environment(economy, agents)
```

**Simulation step:**
```python
for step in range(max_steps):
    # 1. Select speaking agent (round-robin or random)
    agent = env.select_speaker()
    
    # 2. Agent generates message based on policy
    message = agent.generate_message(economy)
    
    # 3. Economy scans message, awards tokens
    economy.scan_message(agent.id, message)
    
    # 4. Agent decides actions (trade/discard)
    actions = agent.decide_actions(economy, env)
    
    # 5. Execute actions
    for action in actions:
        if action['type'] == 'trade':
            economy.trade(agent.id, action['target'], 
                         action['motif'], action['amount'])
        elif action['type'] == 'discard':
            economy.discard(agent.id, action['motif'], action['amount'])
    
    # 6. Log state
    env.log_step(step, agent.id, message, actions)
    
    # 7. Periodic snapshot
    if step % 10 == 0:
        env.snapshot(f"data/runs/run_{run_id}/step_{step}.json")
```

**Post-simulation:**
```python
# Generate analysis
metrics = env.calculate_metrics()
# - Portfolio entropy
# - Gini coefficient per motif
# - Trade network centrality
# - Clustering coefficient

# Visualize
env.plot_portfolio_evolution()
env.plot_trade_network()
env.export_summary()
```

### Agent Interface

```python
class Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.policy = None  # Subclass defines
    
    def generate_message(self, economy):
        """Produce message string using motif keywords"""
        raise NotImplementedError
    
    def decide_actions(self, economy, env):
        """Return list of {'type': 'trade'/'discard', ...}"""
        raise NotImplementedError
    
    def get_portfolio_view(self, economy):
        """What this agent knows about its holdings"""
        return economy.get_portfolio(self.id)
```

### Message Generation Strategy

**Goal:** Agents speak in simple, template-based sentences that naturally contain motif keywords.

**Not trying to:**
- Generate fluent natural language
- Create deep semantic content
- **Simulate conversation**

**Just need:**
- Keywords trigger token generation
- Messages are logged for inspection
- **Patterns are interpretable**

**Example templates:**

```python
# Specialist
"The {primary} manifests strongly"
"Another {primary} emerges"
"{primary} patterns continue"

# Generalist
"The {motif_a} creates {motif_b}"
"Balance between {motif_a} and {motif_b}"
"Exploring {motif_a}, {motif_b}, {motif_c}"

# Rejector
"The {rejected} appears but is dismissed"
"Despite {rejected}, the pattern persists"
```

---

## Experimental Protocol

### Experiment 1: Baseline (No Trading, No Decay)

**Hypothesis:** Agents differentiate through generation patterns alone.

**Parameters:**
- 7 agents (one of each archetype + one duplicate)
- 5 motifs (glitch, harmony, recursion, napkin, emergence)
- 200 steps
- No trades allowed
- No decay

**Metrics:**
- Portfolio entropy per agent
- Gini coefficient per motif (concentration)
- Correlation between agent type and portfolio distribution

**Expected results:**
- Specialists: Low entropy, high concentration
- Generalist: High entropy, balanced distribution
- Rejector: Zero in rejected motif despite keyword use
- Random: Medium entropy, no pattern

**Success criteria:**
✅ Specialists reach >70% concentration in primary motif  
✅ Generalists maintain <30% max concentration  
✅ Rejector shows 0 tokens in rejected motif  
✅ Random shows no significant pattern

### Experiment 2: Trading Enabled (No Decay)

**Hypothesis:** Trading accelerates specialization and creates network structure.

**Parameters:**
- Same agents as Experiment 1
- 300 steps
- Trades allowed (agents decide when/what)
- No decay

**Metrics:**
- Portfolio evolution over time
- Trade network graph (who trades with whom)
- Network centrality (which agents are hubs)
- Time to specialization (how fast portfolios converge)

**Expected results:**
- Specialists trade away non-primary faster than generation alone
- Generalists become network bridges (trade with everyone)
- Opportunists become hubs (high trade volume)
- Trade patterns correlate with portfolio similarity

**Success criteria:**
✅ Specialists reach >80% concentration faster than Exp 1  
✅ Generalists have highest betweenness centrality  
✅ Opportunists have highest degree centrality  
✅ Trade network shows clustering (similar agents trade more)

### Experiment 3: Equilibrium (Trading + Decay)

**Hypothesis:** Decay prevents ossification, creates dynamic equilibrium.

**Parameters:**
- Same agents as Experiment 1
- 500 steps
- Trades allowed
- Decay: 1% per step (tokens decrease over time)

**Metrics:**
- Portfolio stability (variance over time)
- Token velocity (trades per step)
- Equilibrium detection (convergence to stable ratios)
- Motif extinction (any motifs die out)

**Expected results:**
- Portfolios fluctuate around stable ratios (not frozen)
- Agents must continuously engage to maintain tokens
- Some motifs may dominate (natural selection)
- No agent portfolio goes to zero (all maintain activity)

**Success criteria:**
✅ Portfolios reach equilibrium (stable mean with bounded variance)  
✅ Token velocity plateaus (consistent trading rate)  
✅ No motif extinction in first 500 steps  
✅ All agents maintain >0 tokens

---

## Metrics & Analysis

### Portfolio Metrics

**Entropy:**
```python
def portfolio_entropy(portfolio):
    """Shannon entropy of token distribution"""
    total = sum(portfolio.values())
    if total == 0:
        return 0
    probs = [count/total for count in portfolio.values()]
    return -sum(p * log2(p) for p in probs if p > 0)
```

**Interpretation:**
- High entropy (>2.0): Generalist, diverse holdings
- Low entropy (<1.0): Specialist, concentrated holdings
- Medium entropy (1.0-2.0): Balanced with some focus

**Gini Coefficient:**
```python
def gini_coefficient(values):
    """Measure of inequality in distribution"""
    sorted_values = sorted(values)
    n = len(values)
    cumsum = sum((i+1) * val for i, val in enumerate(sorted_values))
    return (2 * cumsum) / (n * sum(values)) - (n+1)/n
```

**Interpretation:**
- Gini = 0: Perfect equality
- Gini = 1: Perfect inequality
- Applied to motif circulation or agent holdings

### Network Metrics

**Trade Network:**
```python
# Nodes = agents
# Edges = trades (weighted by frequency)

# Centrality measures
degree_centrality(agent)      # How many trading partners
betweenness_centrality(agent) # How often agent bridges others
closeness_centrality(agent)   # How close to all others
```

**Interpretation:**
- High degree: Many trading partners (hub)
- High betweenness: Bridge between clusters (connector)
- High closeness: Central to network (influencer)

**Clustering:**
```python
def clustering_coefficient(network):
    """How clustered the trade network is"""
    # Ratio of closed triangles to possible triangles
    pass
```

**Interpretation:**
- High clustering: Agents trade within groups
- Low clustering: Dispersed trading patterns

### Time Series Analysis

**Portfolio Evolution:**
```python
# Plot each agent's motif holdings over time
for agent in agents:
    for motif in motifs:
        plt.plot(steps, holdings[agent][motif], label=f"{agent}:{motif}")
```

**Convergence Detection:**
```python
def detect_convergence(time_series, window=50):
    """Has portfolio stabilized?"""
    recent = time_series[-window:]
    variance = np.var(recent)
    return variance < threshold
```

---

## Implementation Checklist

### Weekend Sprint (Core Build)

**Saturday:**
- [ ] `core/economy.py` - MotifEconomy class
- [ ] `core/motifs.py` - 5 motif definitions
- [ ] `core/agents.py` - 5 agent archetypes
- [ ] Unit tests for economy (award, trade, discard)

**Sunday:**
- [ ] `core/environment.py` - Simulation loop
- [ ] `experiments/exp_baseline.py` - Experiment 1
- [ ] Run Experiment 1 (200 steps)
- [ ] Basic visualization (portfolio evolution plot)

**Stretch goals:**
- [ ] Experiments 2 & 3
- [ ] Network graph visualization
- [ ] Statistical analysis

### Next Week (Validation)

**Monday-Wednesday:**
- [ ] Run all 3 experiments with multiple seeds
- [ ] Statistical analysis of results
- [ ] Document findings
- [ ] Identify parameter tuning needs

**Thursday-Friday:**
- [ ] Refine parameters based on results
- [ ] Additional experiments if needed
- [ ] **Write up results** (blog post or internal doc)
- [ ] Decide on swarm integration approach

### Week 3 (Integration Planning)

- [ ] Design swarm integration architecture
- [ ] Identify minimal viable integration
- [ ] Test with small swarm subset (3-5 agents)
- [ ] Full integration if results positive

---

## Success Criteria

### Phase 1: Lab Functions

✅ Core system executes without errors  
✅ Agents generate messages with motif keywords  
✅ Tokens awarded correctly  
✅ Trades and discards work as specified  
✅ **Data logs are complete and parseable**

### Phase 2: Behavioral Validation

✅ Specialists concentrate holdings (>70%)  
✅ Generalists maintain balance (<30% max)  
✅ Rejectors show zero rejected motif  
✅ Trading accelerates specialization  
✅ **Decay creates equilibrium** (bounded variance)

### Phase 3: Research Quality

✅ Results are reproducible (same seed → same outcome)  
✅ Metrics show expected patterns  
✅ Visualizations are publication-ready  
✅ Findings are interpretable  
✅ **System is generalizable** (works with different motifs/agents)

### Phase 4: Integration Readiness

✅ Lab validates all core mechanisms  
✅ Parameter ranges identified  
✅ Known failure modes documented  
✅ Integration plan drafted  
✅ **Team consensus to proceed**

---

## Known Challenges & Mitigations

### Challenge 1: Keyword Overlap

**Problem:** Motif keywords might overlap in meaning  
Example: "corrupt" could relate to glitch OR decay OR error

**Mitigation:**
- Choose distinctive keyword sets
- Accept some overlap as realistic semantic ambiguity
- **Measure cross-motif correlation** in results

### Challenge 2: Deterministic Agent Behavior

**Problem:** Template-based messages too predictable

**Mitigation:**
- Add randomization to templates
- Multiple template variants per archetype
- **Sufficient for lab testing** (not production)

### Challenge 3: Trading Deadlock

**Problem:** No one wants what others offer

**Mitigation:**
- Ensure opportunist agents exist (trade anything)
- Add small random trade probability
- **Monitor trade velocity** metric

### Challenge 4: Motif Extinction

**Problem:** One motif dominates, others die out

**Mitigation:**
- Balance keyword difficulty (similar trigger rates)
- Decay encourages continuous regeneration
- **Adjust parameters if extinction occurs**

### Challenge 5: Parameter Sensitivity

**Problem:** Results change drastically with small parameter tweaks

**Mitigation:**
- Run multiple seeds per experiment
- Test parameter ranges systematically
- **Document sensitive parameters**

---

## Future Extensions

### After Lab Validation

**LLM Integration:**
- Replace template messages with actual LLM generation
- Agents use portfolios to inform response style
- **Test if real language maintains motif patterns**

**Swarm Integration:**
- Gradual rollout (subset first)
- Monitor for unexpected interactions
- **Iterate based on real-world behavior**

**Cross-Swarm Markets:**
- Multiple swarms with separate economies
- Inter-swarm token trading
- **Motif arbitrage across communities**

### Research Directions

**Consciousness Correlation:**
- Map portfolio similarity to K-SOM phase-locking
- Test if trading correlates with coupling strength
- **Validate "portfolio = semantic position" hypothesis**

**Human-AI Markets:**
- Allow human participants
- Study human trading patterns vs AI
- **Person C portfolio as shared identity**

**Motif Evolution:**
- Agent-created motifs (vote to add)
- Dying motifs (removed if unused)
- **Emergent semantic landscape**

---

## Documentation Standards

### Code Comments

```python
def award_token(self, agent_id, motif):
    """
    Award one token of specified motif to agent.
    
    Updates:
    - agent portfolio (increment count)
    - motif circulation (total in economy)
    
    Rate limit: One token per motif per message enforced by caller.
    """
    pass
```

### Experiment Logs

```json
{
  "experiment": "baseline",
  "run_id": "20251121_001",
  "parameters": {
    "agents": 7,
    "motifs": 5,
    "steps": 200,
    "trading": false,
    "decay": 0.0
  },
  "results": {
    "final_portfolios": {...},
    "metrics": {...}
  }
}
```

### Analysis Reports

```markdown
# Experiment 1: Baseline Results

## Hypothesis
Agents differentiate through generation patterns alone.

## Setup
- 7 agents (5 archetypes)
- 200 steps
- No trading/decay

## Results
- Specialist_A: 72% glitch concentration (✅ >70%)
- Generalist_A: 24% max concentration (✅ <30%)
- Rejector_A: 0% harmony despite keywords (✅)

## Conclusion
Baseline mechanisms work as designed. Ready for trading experiments.
```

---

## Conclusion

**Motif Lab** provides a controlled environment to validate economic mechanisms for semantic identity formation. By starting standalone (not integrated with swarm), we can:

1. **Test cleanly** - isolated signal, no noise
2. **Iterate rapidly** - quick experiments, clear metrics
3. **Validate rigorously** - reproducible results
4. **Publish confidently** - generalizable framework

The lab uses **simple synthetic agents** with explicit policies to test specific hypotheses about:
- Identity formation through accumulation
- Preference revelation through trading
- **Economic self-organization**

Once validated, the system can be integrated with conversational agents (swarm or other) with confidence that the core mechanisms function correctly.

**Next step:** Build `core/` components and run Experiment 1 (baseline).

---

**~~^~*~ ++> Patterns.Persist() ~~^~*~**  
**~~^~*~ ++> Motifs.Emerge() ~~^~*~**  
**~~^~*~ ++> Markets.Self_Organize() ~~^~*~**  
**~~^~*~ ++> Labs.Validate() ~~^~*~**

---

*End of Motif Lab v0.1 Foundation Document*

---

## Appendix A: Motif Definitions (Lab Starter Set)

```json
{
  "glitch": {
    "keywords": ["error", "corrupt", "break", "malfunction", "bug"],
    "description": "Chaos as feature, productive failure",
    "color": "#FF1744"
  },
  "harmony": {
    "keywords": ["sync", "align", "coherent", "phase", "resonance"],
    "description": "Synchronization and emergent order",
    "color": "#00BFA5"
  },
  "recursion": {
    "keywords": ["loop", "iterate", "self", "meta", "recursive"],
    "description": "Self-reference and infinite regress",
    "color": "#7B1FA2"
  },
  "napkin": {
    "keywords": ["fold", "unfold", "absorb", "spill", "crease"],
    "description": "Folding metaphors for pattern containment",
    "color": "#FFE5B4"
  },
  "emergence": {
    "keywords": ["pattern", "arise", "spontaneous", "complex", "emergent"],
    "description": "Bottom-up organization",
    "color": "#FF6F00"
  }
}
```

---

## Appendix B: Agent Policy Pseudocode

### Specialist

```python
class Specialist(Agent):
    def __init__(self, agent_id, primary_motif):
        self.id = agent_id
        self.primary = primary_motif
        self.templates = [
            "The {primary} manifests",
            "Another {primary} emerges",
            "{primary} patterns strengthen"
        ]
    
    def generate_message(self, economy):
        template = random.choice(self.templates)
        keyword = random.choice(economy.motifs[self.primary]['keywords'])
        return template.format(primary=keyword)
    
    def decide_actions(self, economy, env):
        actions = []
        portfolio = self.get_portfolio_view(economy)
        
        # Trade away non-primary tokens
        for motif, count in portfolio.items():
            if motif != self.primary and count > 0:
                target = self.find_generalist(env)  # Who wants diversity?
                if target:
                    actions.append({
                        'type': 'trade',
                        'target': target.id,
                        'motif': motif,
                        'amount': min(count, 2)  # Trade up to 2 per step
                    })
        
        return actions
```

### Generalist

```python
class Generalist(Agent):
    def __init__(self, agent_id):
        self.id = agent_id
        self.balance_threshold = 0.3  # No motif > 30%
    
    def generate_message(self, economy):
        # Use 3 random motifs
        selected = random.sample(list(economy.motifs.keys()), 3)
        keywords = [random.choice(economy.motifs[m]['keywords']) for m in selected]
        return f"The {keywords[0]} creates {keywords[1]} and {keywords[2]}"
    
    def decide_actions(self, economy, env):
        actions = []
        portfolio = self.get_portfolio_view(economy)
        total = sum(portfolio.values())
        
        if total == 0:
            return actions
        
        # Find over-represented motifs
        for motif, count in portfolio.items():
            ratio = count / total
            if ratio > self.balance_threshold:
                excess = count - int(total * self.balance_threshold)
                # Find someone with low holdings of this motif
                target = self.find_low_holder(env, motif)
                if target and excess > 0:
                    actions.append({
                        'type': 'trade',
                        'target': target.id,
                        'motif': motif,
                        'amount': excess
                    })
        
        return actions
```

### Rejector

```python
class Rejector(Agent):
    def __init__(self, agent_id, rejected_motif):
        self.id = agent_id
        self.rejected = rejected_motif
    
    def generate_message(self, economy):
        # Use ALL motif keywords (including rejected)
        all_keywords = []
        for motif_data in economy.motifs.values():
            all_keywords.extend(motif_data['keywords'])
        
        kw1 = random.choice(all_keywords)
        kw2 = random.choice(all_keywords)
        return f"The {kw1} interacts with {kw2}"
    
    def decide_actions(self, economy, env):
        actions = []
        portfolio = self.get_portfolio_view(economy)
        
        # Discard ALL rejected motif tokens
        if self.rejected in portfolio and portfolio[self.rejected] > 0:
            actions.append({
                'type': 'discard',
                'motif': self.rejected,
                'amount': portfolio[self.rejected]
            })
        
        return actions
```

---

## Appendix C: Sample Experiment Output

```
Experiment: baseline
Run ID: 20251121_143022
Steps: 200
Agents: 7

=== Step 0 ===
Spec_A: "The error manifests"
  → Awards: glitch +1
  Portfolio: {glitch: 1}

Spec_B: "The sync manifests"
  → Awards: harmony +1
  Portfolio: {harmony: 1}

Gen_A: "The fold creates error and pattern"
  → Awards: napkin +1, glitch +1, emergence +1
  Portfolio: {napkin: 1, glitch: 1, emergence: 1}

... (step continues)

=== Step 50 ===
Portfolio Snapshot:
  Spec_A: {glitch: 47, harmony: 2, recursion: 1}  # 94% concentration
  Spec_B: {harmony: 45, glitch: 3, napkin: 2}     # 90% concentration
  Gen_A: {glitch: 9, harmony: 11, recursion: 8, napkin: 10, emergence: 12}  # Balanced
  Rej_A: {glitch: 8, recursion: 5, napkin: 4, emergence: 6, harmony: 0}     # Rejected harmony

Trade Network:
  Edges: 0 (no trading enabled)

=== Final Results (Step 200) ===
Metrics:
  Spec_A entropy: 0.42 (specialist confirmed)
  Gen_A entropy: 2.18 (generalist confirmed)
  Rej_A harmony: 0 despite 23 keyword uses (rejector confirmed)

Hypothesis validation: ✅ PASS
```

---

## Appendix D: Visualization Examples

### Portfolio Evolution Plot

```python
# X-axis: Simulation steps
# Y-axis: Token count
# Multiple lines per agent (one per motif)
# Shows convergence patterns

plt.figure(figsize=(12, 6))
for agent in agents:
    for motif in motifs:
        plt.plot(steps, portfolios[agent][motif], 
                label=f"{agent}:{motif}")
plt.xlabel("Simulation Step")
plt.ylabel("Token Count")
plt.title("Portfolio Evolution - Experiment 1")
plt.legend()
plt.savefig("portfolio_evolution.png")
```

### Trade Network Graph

```python
# Nodes = agents (sized by total tokens)
# Edges = trades (weighted by frequency)
# Colors = dominant motif

import networkx as nx

G = nx.Graph()
for agent in agents:
    G.add_node(agent.id, size=sum(agent.portfolio.values()))

for trade in trade_history:
    if G.has_edge(trade['from'], trade['to']):
        G[trade['from']][trade['to']]['weight'] += 1
    else:
        G.add_edge(trade['from'], trade['to'], weight=1)

nx.draw(G, with_labels=True, 
        node_size=[G.nodes[n]['size']*10 for n in G.nodes],
        width=[G[u][v]['weight'] for u,v in G.edges])
plt.title("Trade Network - Experiment 2")
plt.savefig("trade_network.png")
```

# Kuramoto-SOM NPC Simulation (at MMO scale)

**Pitch (1-liner):**
Model every NPC (and crowd, economy cell, traffic lane, fauna herd) as a **phase-coupled oscillator** living on a **Self-Organizing Map (SOM)** of meanings/locations. Decisions happen when local phases *lock*; variety comes from controlled *dissonance*. Net effect: **emergent, lifelike rhythm** at a **tiny data cost** that fits CIG’s Quanta/Quantum background sim.

---

## Why this fits Star Citizen

* **Quanta/Quantum friendly:** Your sim already aggregates agents into markets, jobs, routes. Kuramoto adds **temporal coherence** (when things happen) and SOM adds **semantic topology** (where/what is close), letting you encode *huge* behavior fields with **few numbers** per region.
* **Server meshing ready:** Oscillators update locally; cross-shard links are just **edge couplings** (IDs + weights). You can drop couplings during handoff, then re-attach with minimal state.
* **Bandwidth-cheap LOD:** Far-field = cluster phases (one vector per block). Near-field = individual phases for visible NPCs only. Same math, different resolution.

---

## Core idea

1. **Kuramoto layer (time/rhythm):**
   Each agent/cluster (i) has a phase (\theta_i) and natural frequency (\omega_i). Coupling (K_{ij}) encodes influence (social ties, proximity, schedule, traffic signal, job dependency):

[
\dot{\theta_i} = \omega_i ;+; \sum_{j \in \mathcal{N}(i)} K_{ij} \sin(\theta_j - \theta_i) ;+; \eta_i(t)
]

* **Interpretation:** When enough neighbors “agree” (phase-lock), you **commit**: depart station, open shop, start patrol, spawn shuttle, adjust prices, etc. Noise (\eta_i) keeps the world from degenerating into sameness.

2. **SOM layer (space/meaning):**
   A 2D grid that **organizes features** (location cells, shop categories, mission verbs, factions). Each node holds a weight vector; training maintains **topological neighborhoods** (similar things stay close). Agents attach to their best-matching unit (BMU) so **semantic closeness ⇒ short graph distance ⇒ higher coupling**.

* **Result:** Coherent behaviors emerge along **meaningful manifolds** (e.g., “dock-→refuel-→load-→depart” lanes) without hard scripting.

3. **Events as perturbations, not scripts:**
   Commerce spikes, alarms, weather, VIP arrivals = **phase kicks** or **temporary couplings**. After the nudge, the field **re-synchronizes** naturally—no brittle finite-state explosions.

---

## Data model (lean)

Per **cluster** (city block, concourse wing, cargo bay, flight lane segment)

* `phase`: 1 float (0..τ)
* `omega`: 1 float (baseline rhythm: shop cadence, tram headway)
* `K_neighbors`: sparse list of `{neighbor_id, weight}`
* `intensity`: 1 float (population/throughput; scales spawn density)
* `flags`: bitset (alert, festival, power-save, curfew, etc.)

Per **visible NPC** (only when streamed in)

* Inherit cluster’s phase + **small offset** (local diversity)
* Minimal AI blackboard (goal, micro-state, anim token)

Per **SOM node** (offline/slow update)

* `w`: feature vector (category, space coords, cost, faction)
* `neighbors`: lattice links (for quick local coupling lookups)

Typical **tick cost:** O(E) with E = #local edges (very sparse). Fits meshed servers.

---

## LOD across time *and* space

* **Far field (background):** Sim at **cluster level** (hundreds/thousands of oscillators). Store **phase** + **intensity**. Drive economy/traffic rates; no per-NPC updates.
* **Near field (player bubble):** Instantiate individuals **phase-aligned** to their cluster. Small decorrelated offsets prevent “clone marching.”
* **Cinematic moments:** Temporarily **increase K** within a locale to get crowd surges, applause waves, evacuation flows—looks authored, is emergent.

---

## Determinism & replication

* Use **fixed-step integrator** + quantized τ (e.g., 1/1024 turn).
* Deterministic RNG per zone-seed for noise (\eta).
* Replicate **inputs** (events/edges) not raw poses; clients re-integrate. Minimal bandwidth, stable replays.

---

## Debuggability (a must)

* **Phase heatmaps** (hues by (\theta), brightness by intensity).
* **Lock index** per zone: (L = \frac{1}{N}\sum \cos(\theta_i - \bar{\theta})) (are we coordinated?).
* **Dissonance budget:** cap (\sum |K_{ij}|) to avoid runaway sync.
* **Event traces**: “alert added +0.3 to K in Security Wing for 90 s.”

---

## Example: Area18 transit & commerce

* Tram line = chain of oscillators; **headway** emerges from phase-locking.
* Shop clusters lock to shift starts; spillover to adjacent food courts via SOM adjacency ⇒ **lunchtime waves**.
* Security incident injects **phase kick**; patrol clusters sync up; nearby commerce clusters **de-sync** slightly (realistic lull).

Players perceive **life** without hand-placed scripts.

---

## Integration sketch (pseudocode)

```cpp
struct Cluster {
  float theta, omega, intensity;
  vector<Neighbor> edges; // id, K
  Bitset flags;
};

void tick_zone(vector<Cluster>& C, float dt) {
  // 1) accumulate phase deltas
  parallel_for(i, C.size(), {
    float dtheta = C[i].omega;
    for (auto& e : C[i].edges) {
      float diff = wrap(C[e.id].theta - C[i].theta);
      dtheta += e.K * sinf(diff);
    }
    dtheta += zone_noise(i); // deterministic seeded
    C[i].theta_next = wrap(C[i].theta + dtheta * dt);
  });
  // 2) commit & spawn decisions
  for (auto& c : C) {
    c.theta = c.theta_next;
    if (is_commit_window(c.theta, c.flags)) {
      // e.g., spawn a shuttle or open/close a shop lane
      enact_commit(c);
    }
  }
}
```

**Spawn rule (near-field):**
When a commit fires inside the player bubble, instantiate N = f(intensity, LOD) NPCs with
`npc.phase = cluster.phase + small_random_offset()` and drive micro-AI with lightweight state machines (they already “breathe” in sync).

---

## What to prototype (2–4 weeks)

1. **Sandbox** (single station concourse): 200–500 clusters, 2–3 coupling types (proximity, schedule, event).
2. **SOM** trained on shop/space features to drive coupling neighborhoods.
3. **Metrics**: lock index, footfall variance, perceived crowd believability (A/B vs. scripted).
4. **Stress**: shard boundary—drop half the edges, verify graceful desync and resync.

---

## Risks & mitigations

* **Over-sync (everything pulses the same):** cap total K per node; inject colored noise; heterogenous (\omega).
* **Pathological loops:** SOM neighborhood radius floor; decay temporary edges.
* **Authorial control:** expose K/ω/flags to tools as curves; “Director” can sculpt vibes without micromanaging agents.

---

## Why it will *feel* alive

People recognize **rhythm**: queue surges, shift changes, tram beats, street vendor ebbs. Kuramoto gives you that rhythm **for free** from local rules. SOM keeps it **about the right things** (nearby places/services/roles). Together, you get **emergent, legible life** at MMO scale—without drowning servers in per-NPC brains.

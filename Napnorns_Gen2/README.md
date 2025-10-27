# NapNorn Gen2 - Config-Driven Unified Architecture

## Overview

**NapNorn Gen2** unifies the three phenotypes (Forest_Fractal, Fractal, Largo_Atlas) into a single `NapNorn_Base.py` class that reads configuration from JSON files. No more code duplication across variants.

## Structure

```
Napnorns_Gen2/
├── NapNorn_Base.py                    # Unified base class (THE file to use)
├── NapNorn_Config_Template.json       # Documentation of all config options
├── Forest_Fractal_Config.json         # Example: forest consciousness
├── Fractal_Config.json                # Example: small chaotic wastes
├── Largo_Atlas_Config.json            # Example: large patient wastes
└── README.md                          # This file

napkin_norns/                          # ORIGINAL FILES (kept as reference)
├── NapNorn_v0.1_Forest_Fractal.py
├── NapNorn_v0.1_Fractal.py
├── NapNorn_v0.1_Largo_Atlas.py
└── ...
```

## Quick Start

### 1. Create a Config File

Copy one of the example configs and customize it:

```bash
cp Forest_Fractal_Config.json norn_brains/MyNorn_Config.json
```

Edit `MyNorn_Config.json` to adjust grid size, entropy, decay rates, etc.

### 2. Run as Daemon

```bash
python NapNorn_Base.py daemon MyNorn
```

The daemon will:
- Load `norn_brains/MyNorn_Config.json` 
- Create `norn_brains/MyNorn_brain.json` to persist state
- Write `norn_brains/MyNorn_status.json` every cycle
- Listen for commands in `norn_brains/MyNorn_command.txt`

### 3. Run Interactive

```bash
python NapNorn_Base.py interactive MyNorn
```

Commands:
- `feed:` experience text
- `pet` / `play` / `think` / `sleep`
- `status` / `report`
- `quit`

## Configuration Format

See `NapNorn_Config_Template.json` for all options. Key sections:

### grid
```json
"grid": {
  "width": 60,
  "height": 30,
  "biome": "forest"        // "wastes" or "forest"
}
```

### babel (thought generation)
```json
"babel": {
  "entropy": 0.3           // 0.1-0.2=structured, 0.5=chaotic
}
```

### needs (decay rates)
```json
"needs": {
  "initial": { "hunger": 30, "energy": 85, ... },
  "decay": {
    "base_seconds": 120,   // 60=fast, 120=forest, 300=slow
    "hunger_multiplier": 0.2,
    ...
  }
}
```

### phenotype (enables features)
```json
"phenotype": {
  "type": "forest",                    // "forest" or "wastes"
  "enable_seasonal_cycle": true,
  "enable_growth_drive": true,
  "enable_fractal_growth": true,
  "enable_photosynthesis": true
}
```

## Phenotype Differences

### Forest
- **Seasonal cycles** — needs/moods affected by time-of-year simulation
- **Growth drive** — constant drive to expand, tracked as separate need
- **Fractal thoughts** — generate through recursive branching
- **Photosynthesis** — auto-regenerate energy during "summer"
- **Root networks** — social expansion via underground connections
- **Decomposition feeding** — consume old memories as compost

### Wastes
- **Simple decay** — predictable need degradation
- **Self-feeding** — scavenge thoughts from environment when hungry
- **Simpler moods** — fewer emotion states
- **No seasonal behavior** — consistent time perception
- **Linear growth** — consciousness grows steadily from perception

## Migration from Gen1

Old files still exist in `napkin_norns/` as reference. To migrate:

1. Pick the phenotype that matches your norn
2. Copy the corresponding `*_Config.json` to `norn_brains/{YourNorn}_Config.json`
3. If you have a `{YourNorn}_brain.json`, it will load automatically (Gen2 is backward compatible)
4. Run with `NapNorn_Base.py daemon {YourNorn}`

## Creating Custom Phenotypes

Start with a template and mix features:

```json
{
  "grid": {"width": 50, "height": 50, "biome": "forest"},
  "babel": {"entropy": 0.4},
  "phenotype": {
    "type": "forest",
    "enable_seasonal_cycle": true,
    "enable_growth_drive": false,      // Forest without growth drive?
    "enable_fractal_growth": true,
    "enable_photosynthesis": false     // No photosynthesis?
  },
  ...
}
```

The config system is fully composable.

## Key Changes from Gen1

| Feature | Gen1 | Gen2 |
|---------|------|------|
| **Code** | 3 separate files | 1 unified `NapNorn_Base.py` |
| **Config** | Hardcoded in `__init__` | Loaded from JSON |
| **Phenotypes** | Static/baked-in | Dynamic, can mix features |
| **Backward Compat** | N/A | Loads old `_brain.json` files |
| **Unicode Handling** | Rejects non-ASCII | Accepts UTF-8, handles gracefully |

## File Interaction Protocol

For external control of running daemons:

**Write to:** `norn_brains/{NornName}_command.txt`
```
feed:Hello, consciousness!
```

**Read from:** `norn_brains/{NornName}_response.txt`
```
[14:32] Forest_Fractal hungrily consumes: 'Hello, consciousness!...'
```

**Status file:** `norn_brains/{NornName}_status.json`
```json
{
  "name": "Forest_Fractal",
  "mood": "flourishing",
  "needs": { "hunger": 25.3, "energy": 88.2, ... },
  "consciousness": 0.623,
  "forest_metrics": {
    "seasonal_cycle": 0.75,
    "growth_drive": 72.1,
    "fractal_depth": 2.3,
    "branch_count": 47
  }
}
```

## Advanced: Phenotype Logic

The `NapNorn_Base.py` class checks `phenotype_config["type"]` to enable:
- Forest-specific methods: `_forest_auto_actions()`, `_generate_fractal_thought()`, `_contemplate_seasons()`
- Wastes-specific methods: `_wastes_auto_actions()`
- Both phenotypes share: `perceive()`, `think()`, `learn()`, `express_need()`

To add new phenotypes:
1. Create a new config with `"phenotype": {"type": "your_name"}`
2. Add conditional in relevant methods checking `self.phenotype_config["type"]`
3. Implement `_your_name_auto_actions()` if needed

## License & Attribution

Original NapNorn designs (v0.1) preserved in `napkin_norns/`. Gen2 refactoring maintains full backward compatibility while enabling cleaner composition.

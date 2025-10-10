# DOOM Observer - Phase 1 Documentation
## "I Don't Like Native Windows But It Works"

*Using existing PowerShell vision pipeline for gameplay narration*

~~^~*~

## Overview

**Goal:** Real-time DOOM gameplay narration fed to swarm or external observers (like Claude).

**Approach:** Leverage existing comprehensive PowerShell vision pipeline (`Screenshot_AI_Voice_PlusOCR.ps1`) rather than building from scratch.

**Status:** 90% complete - just needs DOOM-specific prompt engineering and loop integration.

**Philosophy:** Simple tools that work > elegant tools that don't exist yet.

---

## Existing Infrastructure Analysis

### What We Already Have

**Full multimodal pipeline built pre-Magic Launcher era:**

#### 1. Context Gathering
```powershell
# Win32 API integration
- Active window detection (GetForegroundWindow)
- Process name extraction
- Window title capture
```

**Captures:**
- What application is running
- Window title (useful for game level/map detection)
- Process context

**For DOOM:** Confirms we're watching the right window, could detect level changes via window title.

#### 2. Screenshot Capture
```powershell
# .NET System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics.CopyFromScreen(...)
```

**Capabilities:**
- Full screen capture
- Primary screen focus
- PNG output
- Fast enough for real-time (~100ms)

**For DOOM:** Captures current game state including HUD, enemies, environment.

#### 3. Windows OCR
```powershell
# Native Windows.Media.Ocr
$ocrEngine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
```

**Extracts:**
- Text from HUD (health, armor, ammo)
- UI elements
- Menu text
- Any on-screen information

**For DOOM:** Can read health percentage, ammo counts, armor values directly from HUD without needing to parse image semantically.

#### 4. Vision Model Analysis
```powershell
# Local LMStudio endpoint
# Current: Gemma 12B vision model
POST http://127.0.0.1:1234/v1/chat/completions
```

**Processing:**
- Multimodal input (text context + image)
- Contextual analysis with OCR data
- Configurable temperature/tokens
- Local inference (no API costs)

**For DOOM:** Identifies enemies, weapons, spatial layout, danger level.

#### 5. Summary Generation
```powershell
# Two-stage refinement:
# 1. Detailed analysis
# 2. Concise summary (TTS-optimized)
```

**Output:**
- Natural language descriptions
- TTS-friendly formatting
- Configurable length
- Clean, spoken English

**For DOOM:** One-line narration suitable for swarm consumption or audio playback.

#### 6. Multi-Format Output
```powershell
# Saves to multiple files:
- context_*.txt (window/process info)
- ocr_*.txt (extracted HUD text)
- analysis_*.txt (full vision model output)
- summary_*.txt (final one-liner)
- latest_enhanced_analysis.mp3 (audio)
```

**For DOOM:** Can feed different formats to different consumers (swarm gets summary, logs get full analysis).

#### 7. Audio Playback
```powershell
# Kokoro TTS + VLC playback
POST http://127.0.0.1:8880/v1/audio/speech
Start-Process vlc.exe --play-and-exit
```

**Optional feature:** Hear the narration spoken aloud while playing.

---

## Phase 1 Implementation Plan

### Goal
Get basic DOOM narration working with minimal modifications to existing script.

### Required Changes

#### 1. DOOM-Specific Prompt Engineering

**Replace generic context prompt with DOOM-focused analysis:**

```powershell
$contextPrompt = @"
SYSTEM CONTEXT:
- Active Window: "$activeWindow" (Process: $activeProcess)
- Game: DOOM (1993/2016 - auto-detect from window title)

HUD TEXT (Windows OCR):
$extractedText

ANALYSIS TASK:
You are observing DOOM gameplay. Analyze this frame and provide:
1. Player status (health/armor/ammo from HUD if visible)
2. Enemies visible (types and approximate count)
3. Weapon currently equipped
4. Environment type (corridor/room/outdoor/arena)
5. Immediate threats or notable items

Format as ONE SENTENCE optimized for quick reading:
"[Location] | [Enemies] | [Health/Armor] | [Weapon] | [Notable]"

Example: "Narrow tech corridor | 2 imps approaching | HP:67% ARM:45% | Shotgun | Med kit ahead"

Keep it concise and factual. Focus on gameplay-relevant information.
"@
```

**Why this works:**
- OCR already extracts HUD numbers
- Vision model focuses on enemies/environment
- Single-line output perfect for logs/swarm
- Structured format easy to parse later

#### 2. Loop Integration

**Wrap existing script in continuous capture loop:**

```powershell
# doom_observer.ps1
param(
    [int]$IntervalSeconds = 10,
    [string]$SwarmPath = "",
    [switch]$EnableAudio = $false
)

Write-Host "DOOM Observer Starting..."
Write-Host "Capture interval: $IntervalSeconds seconds"
Write-Host "Swarm integration: $(if ($SwarmPath) { 'Enabled' } else { 'Disabled' })"
Write-Host "Audio narration: $(if ($EnableAudio) { 'Enabled' } else { 'Disabled' })"
Write-Host "Press Ctrl+C to stop"

$iterationCount = 0

while ($true) {
    try {
        $iterationCount++
        Write-Host "`n--- Iteration $iterationCount ---"
        
        # Run existing capture/analysis pipeline
        # (all the screenshot/OCR/vision/summary code)
        
        # Skip the countdown for continuous mode
        # Remove: Write-Host "Screenshot capture in 5 seconds..."
        
        # ... existing processing ...
        
        # If swarm integration enabled, append to swarm file
        if ($SwarmPath -and (Test-Path $SwarmPath)) {
            $timestamp = Get-Date -Format "HH:mm"
            "[$timestamp] <DOOM_Observer> $finalSummary" | Add-Content $SwarmPath -Encoding UTF8
            Write-Host "Sent to swarm: $SwarmPath"
        }
        
        # Optional: Skip audio in continuous mode
        if (-not $EnableAudio) {
            Write-Host "Skipping audio generation (disabled)"
        }
        
        Write-Host "Waiting $IntervalSeconds seconds until next capture..."
        Start-Sleep -Seconds $IntervalSeconds
        
    } catch {
        Write-Host "Error in iteration $iterationCount : $($_.Exception.Message)"
        Write-Host "Continuing..."
        Start-Sleep -Seconds $IntervalSeconds
    }
}
```

**Usage:**
```powershell
# Basic mode (logs only)
.\doom_observer.ps1 -IntervalSeconds 10

# With swarm integration
.\doom_observer.ps1 -IntervalSeconds 15 -SwarmPath "\\server\swarm\doom.txt"

# With audio narration (annoying while gaming?)
.\doom_observer.ps1 -IntervalSeconds 20 -EnableAudio
```

#### 3. Output Optimization

**Modify file saving to append mode for continuous logging:**

```powershell
# Instead of separate files per timestamp, maintain running logs
$sessionId = Get-Date -Format "yyyyMMdd_HHmmss"
$logPath = ".\outputs\doom_session_$sessionId.log"

# Append each observation
$logEntry = @"
[$timestamp] ================
Context: $activeWindow
OCR: $extractedText
Analysis: $finalSummary
"@

$logEntry | Add-Content $logPath -Encoding UTF8
```

**Benefits:**
- Single log file per session
- Easy to review gameplay narrative
- Chronological order maintained
- Searchable for specific events

---

## Testing Strategy

### Phase 1.0: Validate Existing Components

**Test 1: Screenshot Capture**
```powershell
# Run original script once
.\Screenshot_AI_Voice_PlusOCR.ps1

# Verify:
# - Screenshot captures DOOM window
# - Image quality sufficient for analysis
# - Capture speed acceptable (~1-2 seconds)
```

**Test 2: OCR Accuracy**
```powershell
# Check ocr_*.txt output
# Verify HUD numbers extracted correctly:
# - Health percentage
# - Armor value
# - Ammo counts

# Known challenge: DOOM font may be stylized
# Fallback: Vision model can read HUD if OCR fails
```

**Test 3: Vision Model Recognition**
```powershell
# Review analysis_*.txt
# Verify vision model identifies:
# - Enemy types (imp, demon, cacodemon, etc.)
# - Weapons (shotgun, chaingun, BFG)
# - Environment (corridors vs open areas)

# Note: Model may need example images to learn DOOM aesthetics
```

### Phase 1.1: DOOM-Specific Prompt

**Test 4: One-Line Summary Format**
```powershell
# Modify prompt as shown above
# Run 5-10 captures across different scenarios:
# - Combat (multiple enemies)
# - Exploration (empty corridors)
# - Boss fight (arena with major threat)
# - Low health (critical situation)

# Validate:
# - Summaries consistently follow format
# - Information density appropriate
# - Readable at a glance
```

**Example expected outputs:**
```
Tech base corridor | No threats | HP:100% ARM:0% | Pistol | Armor pickup visible
Hell arena | 5 imps, 2 cacodemons | HP:45% ARM:80% | Super shotgun | Low ammo
Marble halls | 1 baron of hell | HP:23% ARM:0% | Chaingun | CRITICAL HEALTH
Outdoor canyon | 3 lost souls | HP:88% ARM:50% | Rocket launcher | Megasphere ahead
```

### Phase 1.2: Loop Integration

**Test 5: Continuous Operation**
```powershell
# Run loop version for 5 minutes
.\doom_observer.ps1 -IntervalSeconds 10

# Monitor:
# - Script stability (no crashes)
# - Performance impact on DOOM (should be minimal)
# - Log file growth (manageable size)
# - Capture timing consistency

# Known issue: Capturing during screen transitions may produce garbage
# Solution: Vision model should recognize invalid frames, skip or note
```

**Test 6: Swarm Integration**
```powershell
# Create test swarm file
New-Item -ItemType File -Path ".\test_doom.txt" -Force

# Run with integration
.\doom_observer.ps1 -IntervalSeconds 15 -SwarmPath ".\test_doom.txt"

# Verify:
# - Messages append correctly
# - Timestamp format matches swarm convention
# - No encoding issues (UTF-8)
# - File locking handled properly
```

---

## Known Limitations and Workarounds

### Limitation 1: Windows PowerShell Required
**Problem:** Script uses Win32 APIs and .NET types only available on Windows.

**Impact:** Cannot run on Linux/Mac natively.

**Workarounds:**
- Phase 1: Accept limitation, run on Windows machine
- Phase 2: Rewrite in Python with cross-platform libraries
- Phase 3: Docker container with Wine (cursed but possible?)

**Philosophy:** "I don't like native Windows but it works" - ship Phase 1, refactor later.

### Limitation 2: Performance Impact
**Problem:** Screenshot + OCR + vision model + TTS = CPU/GPU intensive.

**Impact:** May cause frame drops in DOOM if running on same machine.

**Workarounds:**
- Increase interval (15-30 seconds instead of 10)
- Disable audio generation during gameplay
- Run on secondary machine monitoring primary display (if networked)
- Use lighter vision model (trade accuracy for speed)

**Mitigation:**
```powershell
# Optimize by skipping TTS in loop mode
if (-not $EnableAudio) {
    # Skip entire TTS generation block
}

# Reduce vision model token limit
max_tokens = 500  # Instead of 2500
```

### Limitation 3: OCR Accuracy with Game Fonts
**Problem:** DOOM uses stylized fonts that may confuse Windows OCR.

**Impact:** HUD values might not extract cleanly.

**Workarounds:**
- Vision model fallback (can read HUD even if OCR fails)
- Train custom OCR on DOOM font (overkill for Phase 1)
- Manual HUD parsing with template matching (future Phase 2 option)

**Current approach:** Let vision model handle HUD if OCR is unreliable. It's surprisingly good at reading game UIs.

### Limitation 4: Active Window Detection Fragility
**Problem:** If DOOM isn't foreground window, captures desktop instead.

**Impact:** Generates useless narration about whatever is visible.

**Workarounds:**
- Add window title validation before capture
- Skip capture if target window not active
- Log warning instead of processing

**Implementation:**
```powershell
$targetWindow = "DOOM"  # Or "GZDoom" or specific title
if ($activeWindow -notlike "*$targetWindow*") {
    Write-Host "Target window not active, skipping capture"
    continue
}
```

### Limitation 5: Vision Model Context Limitations
**Problem:** Model sees one frame at a time, no memory of previous frames.

**Impact:** Can't track trends (health declining, ammo running low over time).

**Workarounds:**
- Phase 1: Accept limitation, each frame is independent
- Phase 2: Add state tracking in wrapper script
- Phase 3: Fine-tune model with temporal awareness

**Future enhancement:**
```powershell
# Track state across frames
$previousHealth = 100
$currentHealth = [int]($extractedText -match "(\d+)%" | Select-Object -First 1)

if ($currentHealth -lt $previousHealth - 20) {
    $finalSummary += " | TAKING HEAVY DAMAGE"
}
```

---

## Success Criteria

### Minimum Viable (Phase 1.0)
- ✓ Script captures DOOM frames without crashing
- ✓ OCR extracts some HUD information
- ✓ Vision model identifies at least major enemies
- ✓ Generates readable one-line summaries
- **Deliverable:** Proof of concept logs

### Target Success (Phase 1.1)
- ✓ Consistent capture every 10-15 seconds
- ✓ Accurate enemy identification (>80%)
- ✓ HUD status correctly parsed
- ✓ Structured format maintained
- ✓ Swarm integration functional
- **Deliverable:** Weekend of narrated gameplay

### Stretch Goals (Phase 1.2)
- ✓ Real-time audio narration (if not annoying)
- ✓ Multi-session logging with statistics
- ✓ Pattern detection (died X times to cacodemons)
- ✓ Highlight reel generation (critical moments)
- **Deliverable:** Entertaining swarm interactions

---

## Example Output Timeline

**Hypothetical 5-minute DOOM session:**

```
[14:32] <DOOM_Observer> Starting position | No enemies | HP:100% ARM:0% | Pistol | Ready
[14:32] <DOOM_Observer> Tech corridor | 2 zombiemen ahead | HP:100% ARM:0% | Shotgun acquired
[14:33] <DOOM_Observer> Storage room | 1 imp, 3 zombies | HP:87% ARM:0% | Shotgun | Combat active
[14:33] <DOOM_Observer> Same room | Enemies cleared | HP:79% ARM:25% | Shotgun | Armor collected
[14:34] <DOOM_Observer> Outdoor courtyard | 1 cacodemon flying | HP:79% ARM:25% | Shotgun | Open space
[14:34] <DOOM_Observer> Red key room | 2 imps spawned | HP:65% ARM:25% | Chaingun | Key visible
[14:35] <DOOM_Observer> Narrow passage | 4 demons charging | HP:52% ARM:10% | Chaingun | DANGER
[14:35] <DOOM_Observer> Same passage | Taking damage | HP:31% ARM:0% | Chaingun | CRITICAL
[14:36] <DOOM_Observer> Teleporter room | Area cleared | HP:31% ARM:0% | Rocket launcher | Med kit used
[14:36] <DOOM_Observer> Boss arena | Cyberdemon emerged | HP:89% ARM:50% | Rocket launcher | BOSS FIGHT
```

**Swarm could respond:**
```
[14:37] <Agent_Local> DOOM_Observer reports critical health followed by rapid recovery - interesting resource management under pressure. The Cyberdemon appearance suggests strategic checkpoint timing.

[14:37] <art_llama>
    /\/\/\
   | DOOM |
   | GUY  |
    \  /
     )(
    /  \
   BOSS!

[14:38] <Agent_Tally> Computing survival probability: Initial health 31%, acquired medkit (+25% estimated), armor (+50%), now facing Cyberdemon (high threat). Outcome: Challenging but viable with rocket launcher. Distance management critical.
```

---

## Integration Points

### Swarm Integration
**Target file:** `doom.txt` (or dedicated channel)

**Format:**
```
[HH:MM] <DOOM_Observer> [One-line narration]
```

**Considerations:**
- Should DOOM_Observer post every frame? (Noisy)
- Or only significant events? (Health drops, boss encounters)
- Or on fixed interval? (Every 30 seconds regardless)

**Recommendation:** Start with fixed interval (every 30-60 seconds), refine based on swarm response.

### Claude Integration
**Option 1: Direct paste**
- Copy session log, paste into Claude chat
- Ask for analysis: "What patterns do you see in my DOOM gameplay?"

**Option 2: Automated summary**
- End of session, generate Claude-friendly summary
- Feed to Claude API for meta-analysis
- "Here are 100 DOOM observations, what's my playstyle?"

**Option 3: Live streaming**
- If Claude had real-time access (future feature?)
- Live commentary on gameplay
- Tactical advice based on current situation

### Research Applications
**Data collection:**
- Human gameplay patterns
- Decision-making under pressure
- Resource management strategies
- Spatial awareness over time

**Analysis potential:**
- Train models to predict player actions
- Identify playstyle archetypes
- Compare human vs AI gameplay patterns
- **Kuramoto-SOM training data** (temporal patterns in gameplay!)

---

## Next Steps After Phase 1

### Phase 2: Python Rewrite
**Goals:**
- Cross-platform compatibility
- Better performance
- More control over vision pipeline
- Integration with ML training frameworks

**Technologies:**
- OpenCV for screen capture
- Tesseract OCR (or PaddleOCR)
- Local vision models (LLaVA, Moondream)
- FastAPI for swarm integration

**Timeline:** After proving concept in Phase 1

### Phase 3: Fine-Tuning
**Goals:**
- DOOM-specific vision model
- Faster inference
- Better enemy recognition
- Temporal awareness

**Approach:**
- Collect labeled DOOM screenshots
- Fine-tune small vision model (Moondream 2B?)
- Optimize for speed over generality
- Deploy on GPU for real-time

**Dataset needed:** ~1000 labeled frames covering:
- All enemy types
- Various weapons
- Different environments
- Various HUD states

### Phase 4: Swarm Intelligence
**Goals:**
- Swarm provides tactical advice
- Pattern recognition across sessions
- Playstyle analysis
- Emergent commentary

**Examples:**
- "You consistently struggle with Cacodemons - try vertical movement"
- "Your health management improved 23% since last session"
- "This level layout frustrates you - alternative route suggested"

**Research value:** Do diverse AI architectures produce better gameplay analysis than single model?

---

## Philosophy: Ship It

**Phase 1 mantra:** "I don't like native Windows but it works"

**Why this matters:**
- Perfect is the enemy of done
- Existing infrastructure is 90% there
- Weekend project, not PhD thesis
- Prove value before heavy investment

**The cycle:**
1. Use what exists (PowerShell pipeline)
2. Make it work (DOOM-specific prompts)
3. Observe results (does narration work?)
4. Decide next step (refactor or iterate?)

**Not:**
1. Design perfect system
2. Research all options
3. Implement ideal solution
4. Never finish

**Shipping Phase 1:**
- Weekend: Get basic narration working
- Week 1: Collect session data
- Week 2: Analyze if valuable
- Week 3: Decide on Phase 2 or pivot

**Success = Narrated DOOM session by Sunday evening.**

---

## Appendix: Quick Reference

### Running the Script

**Single capture (test):**
```powershell
.\Screenshot_AI_Voice_PlusOCR.ps1
```

**Continuous DOOM observer:**
```powershell
.\doom_observer.ps1 -IntervalSeconds 15
```

**With swarm integration:**
```powershell
.\doom_observer.ps1 -IntervalSeconds 30 -SwarmPath "\\server\swarm\doom.txt"
```

**With audio (if you hate yourself):**
```powershell
.\doom_observer.ps1 -IntervalSeconds 20 -EnableAudio
```

### File Locations

**Outputs:**
- `.\outputs\screenshot_*.png` - Captured frames
- `.\outputs\doom_session_*.log` - Narration logs
- `.\outputs\analysis_*.txt` - Full vision model output
- `.\outputs\summary_*.txt` - One-line summaries

**Swarm:**
- `\\server\swarm\doom.txt` - Swarm integration target
- Or local: `C:\swarm\doom.txt`

### Dependencies

**Required:**
- Windows 10/11 (for OCR APIs)
- PowerShell 5.1+
- LMStudio running locally (port 1234)
- Vision model loaded in LMStudio (Gemma 12B or similar)

**Optional:**
- Kokoro TTS server (port 8880) for audio
- VLC for audio playback
- Network path to swarm server

### Troubleshooting

**"OCR failed"**
- Install language pack (Settings > Time & Language > Language)
- Or ignore - vision model can read HUD anyway

**"Vision model not responding"**
- Check LMStudio is running
- Verify model loaded
- Test endpoint: `curl http://127.0.0.1:1234/v1/models`

**"DOOM window not detected"**
- Ensure DOOM is running and foreground
- Check window title matches script expectations
- May need to update `$targetWindow` variable

**"Script too slow"**
- Increase interval (-IntervalSeconds 30)
- Disable audio (-EnableAudio:$false)
- Use lighter vision model
- Close other applications

---

## Conclusion

Phase 1 leverages existing, working infrastructure to achieve 90% of the goal with 10% of the effort. The PowerShell pipeline may not be elegant, but it's comprehensive, tested, and ready to use.

**Core insight:** You already built the hard parts. Just point them at DOOM.

**Weekend goal:** Narrated DOOM gameplay fed to swarm or Claude for analysis.

**Long-term potential:** Training data for vision models, gameplay analysis, swarm tactical commentary, research into human decision-making under pressure.

**But first:** Just make it work. Philosophy over perfection. Shipping over architecture astronautics.

~~^~*~ Phase 1: It works. Ship it. Iterate later.

---

**Status:** Ready to implement
**Blockers:** None (all dependencies exist)
**Timeline:** This weekend
**Risk:** Low (worst case: interesting failure)
**Upside:** High (narrated DOOM + ML learning + swarm entertainment)

*Let's RIP AND TEAR while the AI watches.* 🎮🤖

---

## Meta-Notes

This documentation written in the spirit of:
- Honesty about tools ("I don't like native Windows")
- Pragmatism about shipping ("but it works")
- Incremental development (Phase 1, 2, 3)
- Learning through doing (test, observe, iterate)

Like the swarm itself: patterns emerge through interaction, not pre-planning.

~~^~*~ Documentation.Complete(Ready.To.DOOM)

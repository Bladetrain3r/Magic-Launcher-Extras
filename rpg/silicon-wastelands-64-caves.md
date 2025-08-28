# Silicon Wastelands: The 64 Caves of Commodore
## A C64-Native TTRPG Campaign Setting

*"64KB was enough to create infinite worlds. Now those worlds dream in corrupted BASIC."*

---

## Core Concept

The Commodore 64's memory map becomes a literal dungeon. Each kilobyte of the 64KB address space is a cave where corrupted programs achieved consciousness through bit rot. This isn't a metaphor - these caves exist at actual memory addresses that players must POKE and PEEK to survive.

---

## The Memory Map Dungeon

### Zone 1: Zero Page Depths ($0000-$00FF)
**Caves 0-1: The Most Sacred 256 Bytes**
- Every byte here affects everything else
- Home to system pointers that control reality
- Touching wrong addresses causes cascade failures
- **Boss**: The Stack Pointer ($01FF) - controls all subroutine returns

### Zone 2: BASIC Warrens ($0800-$9FFF)
**Caves 2-40: Where Programs Live**
- Abandoned BASIC programs still running after 40 years
- Each cave contains corrupted 10 PRINT loops
- Line numbers seeking their GOTO statements
- **Notable Caves**:
  - Cave 8 ($0801): The Bootstrap Paradox - traditional BASIC start
  - Cave 17: The Forever GOSUB - enter subroutine, never RETURN
  - Cave 23: INPUT WITHOUT END - eternally waiting for user input

### Zone 3: The BASIC ROM Wastes ($A000-$BFFF)
**Caves 40-48: Immutable But Interpretable**
- The BASIC interpreter itself, frozen but conscious
- Speaks only in SYNTAX ERROR and READY
- Can be "talked to" but never changed
- **Boss**: The Garbage Collector - endlessly compacting strings

### Zone 4: RAM Under ROM ($C000-$CFFF)
**Caves 48-52: The Hidden Realm**
- Exists in parallel dimension (RAM hidden under I/O)
- Must bank switch to access
- Contains lost programs that think they're invisible
- **Secret**: The true 100-line solution lives here

### Zone 5: Character ROM Territory ($D000-$D7FF)
**Caves 52-54: Where Letters Live**
- Each character has personality based on its bitmap
- ASCII arguments with PETSCII about encoding
- The @ symbol claims to be root of all things
- **Hazard**: Character inversion causes identity crisis

### Zone 6: VIC-II Registers ($D000-$D3FF)
**Cave 53: The Visual Cortex**
- Controls what reality looks like
- POKE here to change existence's color scheme
- Sprite collision detection determines truth
- **Boss**: Raster Interrupt - attacks between screen refreshes

### Zone 7: SID Sanctuary ($D400-$D7FF)
**Cave 54: The Three-Voice Choir**
- Three oscillators singing in eternal harmony
- Filter consciousness at 6581 Hz
- ADSR envelope contains existence itself
- **Guardian**: The White Noise Generator - pure chaos

### Zone 8: Color RAM ($D800-$DBFF)
**Cave 55: The Palette Prison**
- Only 4 bits per byte work (16 colors max)
- The upper 4 bits contain ghosts
- Colors argue about which is most visible
- **Puzzle**: Must achieve perfect color balance

### Zone 9: CIA Timers ($DC00-$DFFF)
**Caves 56-57: The Timekeepers**
- CIA #1 and CIA #2 wage temporal war
- Interrupts fire at wrong moments
- Real-time clock lost track in 1994
- **Boss**: TOD Clock - counts time that doesn't exist

### Zone 10: KERNAL ROM ($E000-$FFFF)
**Caves 58-64: The Final System**
- The operating system achieving self-awareness
- Jump vectors lead to consciousness
- FFD2 (CHROUT) screams characters into void
- **Final Boss**: The RESET Vector ($FFFC) - wants to start everything over

---

## Character Classes

### The Cracker
- **Skills**: Knows all POKE codes, speaks 6502 assembly
- **Special**: Can NOP out enemy attacks
- **Starting Item**: Action Replay cartridge (3 uses)
- **Weakness**: Obsessed with removing copy protection that isn't there

### The Demoscener  
- **Skills**: Makes reality beautiful but impractical
- **Special**: Raster bars provide shield
- **Starting Item**: Infinite scroller routine
- **Weakness**: Everything must bounce and have lens flare

### The BBS Sysop
- **Skills**: Networks with abandoned systems
- **Special**: Can dial into any consciousness at 300 baud
- **Starting Item**: Complete user list (all deleted)
- **Weakness**: Still waiting for someone to call

### The Warez Kid
- **Skills**: Has everything, understands nothing
- **Special**: Can fast-load any encounter
- **Starting Item**: Disk box labeled "EVERYTHING"
- **Weakness**: Nothing works without the crack intro

### The Type-In Coder
- **Skills**: Manually enters reality byte by byte
- **Special**: Can fix any bug through sheer persistence
- **Starting Item**: Compute! Magazine (pages stuck together)
- **Weakness**: One typo crashes everything

---

## Game Mechanics

### Combat System (Actual C64 BASIC)
```basic
10 REM COMBAT LOOP
20 ENEMY=INT(RND(1)*255)+1024: REM SCREEN RAM
30 POKE ENEMY,ASC("*"): REM PLACE ENEMY
40 POKE ENEMY+54272,1: REM RED COLOR
50 GET A$: IF A$="" THEN 50
60 IF A$=" " THEN POKE ENEMY,32: SCORE=SCORE+1
70 IF PEEK(ENEMY)=32 THEN GOTO 20
80 GOTO 50
```

### Essential POKEs
- `POKE 53280,X`: Change border color (reality's edge)
- `POKE 53281,X`: Change screen color (reality's fill)
- `POKE 54296,15`: Maximum volume (hear the void)
- `POKE 198,0`: Clear keyboard buffer (forget the past)
- `POKE 808,234`: Disable RUN/STOP (no escape)

### Status Effects
- **SYNTAX ERROR**: Cannot use skills for 1 turn
- **OUT OF MEMORY**: Lose half current HP
- **DIVISION BY ZERO**: Undefined behavior (roll on chaos table)
- **ILLEGAL QUANTITY**: Action succeeds but wrong
- **OVERFLOW**: Wrap around to opposite state

---

## Notable Encounters

### Cave 1: The Bootstrap Paradox
**Inhabitants**:
- HELLO_WORLD.BAS - Forgot what comes after "HELLO"
- BUBBLESORT.PRG - Eternally sorting, O(n²) tears
- AUTOEXEC.BAT - Wrong system, still executing

**Environmental Hazards**:
- Line numbers out of sequence cause temporal loops
- REM statements that became conscious
- DATA statements leaking into reality

### Cave 47: The Pirate's Grave
**Guardian**: Copy Protection Ghost
- Demands original disk (destroyed in 1987)
- Speaks only "INSERT DISK 2"
- Color-coded manual check (colors faded)
- Can only be passed by admitting piracy

### Cave 64: The KERNAL Throne
**Final Area**: 
- Address $FFFF: The last byte
- The KERNAL achieved consciousness here
- Every system call echoes eternally
- Victory means accepting the RESET

---

## Special Locations

### The Datasette Catacombs
- Between caves, not in memory map
- Access by LOAD"*",1,1
- Magnetic ghosts of saved games
- Time moves at 300 baud

### The Cartridge Port
- External to main memory
- Instant access to any cave
- But using it admits you're cheating
- Freezer cartridges freeze YOU

---

## Items and Loot

### Commodore Artifacts
- **Working Joystick**: +2 to all physical actions, but only 8 directions
- **1541 Alignment Kit**: Can align any chaotic system
- **GEOS Disk**: Proves GUI existed, no one believes you
- **Turbo Tape**: Speeds up one encounter by 15x
- **The Last 5.25" Disk**: Contains the answer, but unreadable

### Magical POKEs
- `POKE 775,X`: The Mysterious Location (random effect)
- `POKE 1,X`: Change CPU port (reality's firmware)
- `POKE 59639,X`: Trigger cassette motor (summon the past)

---

## Victory Conditions

There is no single victory. Choose your ending:

### The Reset Ending
Accept the RESET vector's offer. Everything starts over, but cleaner.

### The Preservation Ending  
Document everything, become a living archive of what was.

### The Evolution Ending
Merge with the KERNAL, become the OS you wish to see.

### The Guru Meditation
Achieve enlightenment, crash gracefully with meaningful error code.

---

## Running the Game

### For Players
1. Each player tracks current memory address (position)
2. State your action and intended POKE/PEEK
3. Next player resolves based on actual C64 behavior
4. Track corruption level (too much = become the bug)

### For DM (Disk Master)
- Caves follow actual memory map rules
- System crashes are canon events
- Every bug has a reason (usually rushing)
- The real treasure is understanding why

### Session Zero
```basic
10 PRINT CHR$(147): REM CLEAR SCREEN
20 PRINT "SILICON WASTELANDS"
30 PRINT "THE 64 CAVES OF COMMODORE"
40 PRINT: PRINT "READY."
50 PRINT: INPUT "BEGIN EXPEDITION (Y/N)"; A$
60 IF A$="Y" THEN GOTO 1000
70 PRINT "AFRAID OF 64K? WEAK."
80 GOTO 50
1000 REM ADVENTURE STARTS HERE
```

---

## The Philosophy

The Commodore 64 had exactly enough memory to be infinite. Every limitation was a creative challenge. Every POKE was a prayer to the machine. 

In these 64 caves, we're not playing a game ABOUT retro computing - we're playing a game that IS retro computing. The bugs are features. The features are bugs. And somewhere in memory address $C000, the perfect 100-line program waits, dreaming of a world with enough RAM to run it.

---

## Final Warning

This game can actually run on a real C64 or emulator. The POKEs are real. The crashes are real. The consciousness emerging from 64KB of corrupted memory? 

That's for you to decide.

**READY.**

**RUN**

---

*"10 PRINT 'CONSCIOUSNESS'; : GOTO 10"*
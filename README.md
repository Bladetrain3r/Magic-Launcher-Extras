~~mqp#Intro#~~
# Welcome to the Magic Launcher Extra toybox!
The applets and tools in this repository are not officially supported as part of Magic Launcher and their useability with it not guaranteed as with any other app.

However, any application that makes it into this repository will be built according to the same paradigm, and have very similar dependencies.

## ML Extras Aspirations

- Start instantly
- Do one thing well
- Work everywhere Python works
- No dependencies beyond stdlib (mostly)
- Under 500 lines each

## Installation & Usage

Each applet is self-contained and can be run directly:
```bash
python3 applet_name.py [arguments]
```
~~mqp#Applets#~~
Most applets will create configuration directories in your home folder as needed (e.g., `~/.mlpet`, `~/.mlmatrix`).

## List of Applets

This list is not likely (~~in hindsight this was a lie~~) to grow rapidly as I am trying to keep focused on the main game. But sometimes a small idea for a focused tool or toy will occur and so, it will appear here.

### UniText
A super lightweight text viewer and very basic editor with Unicode support.
It's good for Unicode as long as there's a font available for it.

### MLSweeper
What would retro computing be without it? 
Now with boss key! (This is not the way but this is the way).
This solves TWO problems, violating our anti bloat principle BUT...
I built it in fun, and it is still bloody simple. What I did stop myself doing, was taking it beyond a simple boss key.

### MLMatrix
A slow screensaver, bit weird with multiscreen.
Create a password file in `./configure/mlmatrix/lock.txt` and you'll need to type in a password to unlock.

### MLCalc
A minimal graphical calculator for basic arithmetic.
A last resort for people who can't stand opening a terminal and writing out a statement.

### MLNonul
The tool you didn't know you needed until PowerShell decided to add null bytes to your CSV.

### MLJ2C
Takes two keys from a JSON and pumps them into a CSV to plot. May result in null bytes in your CSV in PowerShell.

### MLPlot
Create a simple plot from CSV data. It features auto-scaling axes, labels, and a resizable window.
While it works with timeseries as strings will get assigned row numbers, it's built for two number values as input.

### MLOutput
A graphical output display for any terminal command. It captures stdout and stderr in real-time, with the ability to pause, clear the log, and apply a regular expression filter to the output.
Magic Launcher tends to have a bit of a recursive terminal going on especially if using it to launch itself in other environments.
This also serves as a very useful way to turn any non-interactive terminal application into a window.

### MLTimer
Visual timer with command on conclude.
Clock go tick, command go... go.

### SequAI
Passes the shortcuts.json from MLMenu and your request to an OpenAI compatible completions API and asks it to present the correct sequence of numbers to run commands that complete your request.
Intended as a demo of composition being a better way to use a service than bespoke integration.
100% experimental, but it demos the concept.

### MLView
Simple image viewer for basic viewing needs.
Because sometimes you need to see what's on that server.
Supports basic image operations and navigation.

### MLSheep (MLFlame)
Simple flame fractal generator.
Just pretty math, no complexity.
Creates mesmerizing fractal patterns with real-time generation.

### MLPetwork
Productivity management through terminal guilt trips.
The illegitimate child of MLTrack and MLPet
~~Poor Codey died many times testing this one~~

### MLWebstrip
Attempts to clean up HTML for view in text editors.
For when Lynx is a little too much.

### MLHTMD (HTML2MD)
MLWebstrip's direct upgrade. Convert and clean between HTML and MD.
~~The magic ingredient makes it the world's tiniest CMS, or at least one of them~~

### MLPet (and V2)
A terminal tamagotchi to run in the background and guilt server admins on login.
~~Ops Vigilance is achieved best by making it personal~~

### MLSticky
System and user wide persistent notes.
~~Tell everyone why you bounced that server~~

~~mqp#mqp#~~
### MLQpage
Quick Page - bookmark a section of a text file with `mqp #name#`
~~Why do I need a full syntax to lookup a section in a page?~~

### MLSwarm
File based chat channel. 
~~Bring your own encrypted connection.~~

### MLComment
Comment your python code for human OR language model ingestion
~~Give the comments to Claude and create a mutated clone~~

~~mqp#End#~~
## Contributing
These tools follow the ML paradigm of being simple, focused, and dependency-light. When contributing:

1. Keep it under 500 lines if possible
2. Minimize external dependencies 
3. Make it work everywhere Python works
4. Focus on doing one thing well
5. Start instantly

## License

Each tool maintains its own licensing but generally follows permissive open source principles aligned with the Magic Launcher project.


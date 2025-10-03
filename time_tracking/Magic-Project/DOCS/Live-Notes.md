# General decision tracker

1) Moving to vaguely MVC like architecture for better modularity
- model.py: Data, io, concurrency, etc
- controller.py: Functional Logic (spark, status, task operations, state calculations)
- terminal.py: CLI interface with argparse, formatting, ANSI colors
- gui.py (stretch): Tkinter interface, same controller underneath
- MLProject.py: Launcher
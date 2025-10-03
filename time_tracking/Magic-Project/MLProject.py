#!/usr/bin/env python3
# mp.py - Main launcher for MagicProjects

import sys
from pathlib import Path

# Add components directory to path
sys.path.insert(0, str(Path(__file__).parent / 'components'))

from terminal import main

if __name__ == '__main__':
    main()
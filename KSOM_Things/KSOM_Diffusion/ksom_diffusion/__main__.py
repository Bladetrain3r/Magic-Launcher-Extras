"""Module entry point supporting both `-m` and direct execution."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


def _resolve_main():
    if __package__ in (None, ""):
        package_root = Path(__file__).resolve().parent.parent
        if str(package_root) not in sys.path:
            sys.path.insert(0, str(package_root))
        return importlib.import_module("ksom_diffusion.cli").main
    from .cli import main as package_main

    return package_main


if __name__ == "__main__":
    main = _resolve_main()
    main()

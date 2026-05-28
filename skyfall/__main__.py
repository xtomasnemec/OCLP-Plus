"""Module entrypoint for running Skyfall as a package.

Enables: python -m skyfall ...
"""

from __future__ import annotations

from .application_entry import main


if __name__ == "__main__":
    main()

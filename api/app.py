"""Vercel entrypoint for the Campus Resource Booking System.

This wrapper reuses the existing Flask application factory and does not
change the app's local runtime or core project structure.
"""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import create_app


app = create_app()

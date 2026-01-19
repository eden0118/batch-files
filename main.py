#!/usr/bin/env python3
"""
Batch Renamer - Main application entry point
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from batch_renamer.ui.app import create_app

if __name__ == "__main__":
    create_app()

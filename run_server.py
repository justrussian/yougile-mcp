#!/usr/bin/env python3
"""
Wrapper script to run YouGile MCP server.
Fixes import issues when running as daemon.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the server
if __name__ == "__main__":
    from src.server import main
    main()
#!/usr/bin/env python3
"""Launcher for the MedB MCP server (D-74), runnable from any working directory:

    python3 /path/to/medb/tools/medb_mcp.py [--config data/integrations.json] [--tokens data/api_tokens.json]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from medb.integrations.mcp_server import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())

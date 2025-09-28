#!/usr/bin/env python3
"""
Entry point for latencycalc that handles Windows console issues properly.
"""

# Monkey patch Click BEFORE any imports to avoid Windows console issues
import click._winconsole
click._winconsole._get_windows_console_stream = lambda stream: None
click._winconsole._is_console = lambda f: False

import os
import sys

# Disable colors to avoid Windows console issues
os.environ['NO_COLOR'] = '1'
os.environ['FORCE_COLOR'] = '0'

def main():
    try:
        from latencycalc import cli
        cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Use 'latencycalc --help' for usage information.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Time-based coin flip resolver.

Checks the current second:
  0-29  → heads
  30-59 → tails

This is a proof of concept for dynamic, non-deterministic routing
through filesystem convention.
"""

import json
import sys
from datetime import datetime

def resolve(params: dict) -> tuple:
    now = datetime.now()
    second = now.second

    if second < 30:
        return ("heads", f"Second was {second} (0-29 range) — heads wins")
    else:
        return ("tails", f"Second was {second} (30-59 range) — tails wins")


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()

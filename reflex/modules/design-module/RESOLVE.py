#!/usr/bin/env python3
"""
Resolver for design-module.

Routes based on whether intent is provided:
- No intent → triage variant (interactive menu: create, upgrade, or clone)
- Intent provided → create variant (original behavior, design a new module)

Prints: variant_name|reason
"""

import json
import sys


def resolve(params: dict) -> tuple:
    intent = params.get("intent", "").strip()

    if not intent:
        return ("triage", "No intent provided — presenting options to create, upgrade, or clone a module")

    return ("create", f"Intent provided — designing new module for: {intent[:80]}")


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()

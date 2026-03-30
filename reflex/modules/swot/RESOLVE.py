#!/usr/bin/env python3
"""
Resolver for swot module.

Routes to quick (simple 2x2) or deep (TOWS + quality gates) based on depth param.
Prints: variant_name|reason
"""

import json
import sys


def resolve(params: dict) -> tuple:
    depth = params.get("depth", "quick").lower().strip()

    if depth in ("deep", "full", "detailed", "tows"):
        return ("deep", "Depth set to deep — running TOWS analysis with quality gates and confidence scoring")

    return ("quick", "Running standard SWOT (use depth:deep for TOWS + quality gates)")


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()

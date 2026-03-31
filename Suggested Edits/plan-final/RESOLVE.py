#!/usr/bin/env python3
"""
Resolver for the plan module.
Always routes to the 'route' variant — the LLM evaluates the registry
and decides whether to plan a chain or suggest a new module.
"""
import json
import sys

def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    print("route|LLM evaluates intent against registry")

if __name__ == "__main__":
    main()

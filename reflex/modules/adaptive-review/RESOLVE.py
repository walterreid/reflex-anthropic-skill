#!/usr/bin/env python3
"""
Resolver for adaptive-review module.

Evaluates the code context and selects the appropriate review variant.
Prints: variant_name|reason
"""

import json
import sys

def resolve(params: dict) -> tuple:
    context = params.get("code_context", "unknown").lower()
    language = params.get("language", "unknown").lower()

    # Route based on code context hints
    security_signals = ["web", "api", "auth", "login", "database", "sql", "user"]
    deep_signals = ["large", "complex", "architecture", "refactor"]

    if any(signal in context for signal in security_signals):
        return ("security-review", f"Code context '{context}' suggests security-sensitive code")

    if any(signal in context for signal in deep_signals):
        return ("deep-review", f"Code context '{context}' indicates complex code requiring deep analysis")

    # Default to quick review
    return ("quick-review", "No specific risk signals detected — running quick review")


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()

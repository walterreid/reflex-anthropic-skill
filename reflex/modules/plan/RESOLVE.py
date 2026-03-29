#!/usr/bin/env python3
"""
Resolver for the plan module.

Evaluates the user's intent against the module registry to determine
whether existing modules can satisfy it (route) or a new module needs
to be designed (suggest).

Heuristic: parse the registry string, extract module descriptions,
and check how well the intent keywords overlap with existing module
capabilities. Low overlap → suggest. High overlap → route.
"""

import json
import sys
import re


def extract_module_keywords(registry: str) -> set:
    """Pull meaningful words from the registry descriptions."""
    # Strip group headers like [SOURCE], [ANALYZER], etc.
    clean = re.sub(r'\[.*?\]', '', registry)
    # Grab words, lowercase, filter short ones
    words = set(re.findall(r'[a-z]{3,}', clean.lower()))
    # Remove noise words
    noise = {
        'the', 'and', 'for', 'from', 'with', 'into', 'that', 'this',
        'using', 'based', 'any', 'all', 'its', 'has', 'are', 'was',
        'will', 'can', 'may', 'not', 'but', 'also', 'each', 'only',
        'module', 'target', 'output', 'content', 'type', 'style',
        'findings', 'structured', 'data', 'current', 'key', 'one'
    }
    return words - noise


def extract_intent_keywords(intent: str) -> set:
    """Pull meaningful words from the user's intent."""
    words = set(re.findall(r'[a-z]{3,}', intent.lower()))
    noise = {
        'want', 'need', 'would', 'like', 'way', 'something',
        'make', 'create', 'build', 'have', 'that', 'this',
        'the', 'and', 'for', 'with', 'can', 'how', 'get'
    }
    return words - noise


def resolve(params: dict) -> tuple:
    intent = params.get("intent", "")
    registry = params.get("registry", "")

    if not intent:
        return ("route", "No intent provided — defaulting to route")

    intent_kw = extract_intent_keywords(intent)
    registry_kw = extract_module_keywords(registry)

    if not intent_kw:
        return ("route", "Could not parse intent — defaulting to route")

    overlap = intent_kw & registry_kw
    coverage = len(overlap) / len(intent_kw) if intent_kw else 0

    # Also check if intent mentions module names directly
    module_names = set(re.findall(r'^\s+(\S+)\s+\(', registry, re.MULTILINE))
    intent_lower = intent.lower()
    direct_match = any(name in intent_lower for name in module_names)

    if direct_match or coverage >= 0.4:
        reason = f"Intent keywords overlap {coverage:.0%} with registry"
        if direct_match:
            reason += " (direct module name match)"
        return ("route", reason)
    else:
        return ("suggest", f"Intent keywords overlap only {coverage:.0%} with registry — existing modules may not cover this well")


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()

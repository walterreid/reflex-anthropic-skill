#!/usr/bin/env python3
"""
Resolver for the plan module.

Evaluates the user's intent against the module registry to determine
whether existing modules can satisfy it (route) or a new module needs
to be designed (suggest).

Strategy: TF-IDF cosine similarity over module corpus. Each module's
"document" is built from whatever metadata is available:
  - Module name (always — hyphens replaced with spaces)
  - Description from PARAMS.json (when present)
  - Usage phrases from PARAMS.json (when present)
  - First content line of MODULE.md (fallback for Level 0 modules)

Modules without a "usage" field degrade gracefully to name + description.
No new required fields. No contract changes.

Falls back to lexical matching if scikit-learn is unavailable.
"""

import json
import sys
import re
from pathlib import Path

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


SKILL_DIR = Path(__file__).parent.parent
MODULES_DIR = SKILL_DIR / "modules"
THRESHOLD = 0.18


def _load_json(filepath: Path) -> dict:
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _first_content_line(md_path: Path) -> str:
    """Extract first non-heading, non-empty line from a MODULE.md."""
    try:
        with open(md_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line[:120]
    except IOError:
        pass
    return ""


def build_module_corpus() -> tuple:
    """
    Build a list of (module_name, document_text) from the filesystem.
    Combines whatever metadata each module provides.
    """
    if not MODULES_DIR.exists():
        return [], []

    names = []
    docs = []

    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or not (d / "MODULE.md").exists():
            continue

        name = d.name
        parts = [name.replace("-", " ")]

        params_file = d / "PARAMS.json"
        if params_file.exists():
            schema = _load_json(params_file)
            desc = schema.get("description", "")
            usage = schema.get("usage", "")
            if desc:
                parts.append(desc)
            if usage:
                parts.append(usage)

        # Fallback for modules without PARAMS.json or without description
        if len(parts) == 1:
            first_line = _first_content_line(d / "MODULE.md")
            if first_line:
                parts.append(first_line)

        names.append(name)
        docs.append(" ".join(parts))

    return names, docs


def resolve_tfidf(intent: str, names: list, docs: list) -> tuple:
    """Score intent against module corpus using TF-IDF cosine similarity."""
    if not docs:
        return ("route", "No modules found — defaulting to route")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.9,
    )
    tfidf_matrix = vectorizer.fit_transform(docs)
    intent_vec = vectorizer.transform([intent])
    sims = cosine_similarity(intent_vec, tfidf_matrix).flatten()

    top_idx = sims.argsort()[::-1]
    top_score = float(sims[top_idx[0]])
    top_name = names[top_idx[0]]

    if top_score >= THRESHOLD:
        return ("route", f"Top match: {top_name} (score={top_score:.2f})")
    else:
        return ("suggest", f"Best match {top_name} scored only {top_score:.2f} — below threshold {THRESHOLD}")


def resolve_lexical_fallback(intent: str, registry: str) -> tuple:
    """Original lexical approach — used only if sklearn is unavailable."""
    clean = re.sub(r'\[.*?\]', '', registry)
    reg_words = set(re.findall(r'[a-z]{3,}', clean.lower()))
    reg_noise = {
        'the', 'and', 'for', 'from', 'with', 'into', 'that', 'this',
        'using', 'based', 'any', 'all', 'its', 'has', 'are', 'was',
        'will', 'can', 'may', 'not', 'but', 'also', 'each', 'only',
        'module', 'target', 'output', 'content', 'type', 'style',
        'findings', 'structured', 'data', 'current', 'key', 'one'
    }
    registry_kw = reg_words - reg_noise

    words = set(re.findall(r'[a-z]{3,}', intent.lower()))
    intent_noise = {
        'want', 'need', 'would', 'like', 'way', 'something',
        'make', 'create', 'build', 'have', 'that', 'this',
        'the', 'and', 'for', 'with', 'can', 'how', 'get'
    }
    intent_kw = words - intent_noise

    if not intent_kw:
        return ("route", "Could not parse intent — defaulting to route")

    overlap = intent_kw & registry_kw
    coverage = len(overlap) / len(intent_kw)

    module_names = set(re.findall(r'^\s+(\S+)\s+\(', registry, re.MULTILINE))
    direct_match = any(name in intent.lower() for name in module_names)

    if direct_match or coverage >= 0.4:
        return ("route", f"Lexical fallback: {coverage:.0%} overlap")
    else:
        return ("suggest", f"Lexical fallback: only {coverage:.0%} overlap")


def resolve(params: dict) -> tuple:
    intent = params.get("intent", "")
    registry = params.get("registry", "")

    if not intent:
        return ("route", "No intent provided — defaulting to route")

    if HAS_SKLEARN:
        names, docs = build_module_corpus()
        if names:
            return resolve_tfidf(intent, names, docs)

    return resolve_lexical_fallback(intent, registry)


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()
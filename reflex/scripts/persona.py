#!/usr/bin/env python3
"""
Persona Dispatch — Persistent conversational layer over module dispatch.

Personas are not modules. Modules are bounded (input → process → output).
Personas are persistent (they wrap around everything else).

This script:
  1. Locates the requested persona in the personas/ directory
  2. Loads PERSONA.md, STYLE.json, TRIGGERS.json
  3. Injects context (registry, workspace) via sources.py
  4. Assembles a single context payload for the LLM
  5. Outputs LOAD_PERSONA with the assembled content

The LLM then operates under this persona and can invoke dispatch.py
for module calls as needed — the persona stays in context.

Output protocol:
  LOAD_PERSONA:/path|CONTEXT:{...}
  LIST_PERSONAS:[{name, description}, ...]
  ERROR:message

Directory convention:
  personas/
  └── walt/
      ├── PERSONA.md       ← identity, purpose, behavioral instructions
      ├── PARAMS.json      ← inject-only params (registry, workspace)
      ├── TRIGGERS.json    ← situational patterns and responses
      └── STYLE.json       ← voice characteristics, tone rules
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
PERSONAS_DIR = SKILL_DIR / "personas"
MODULES_DIR = SKILL_DIR / "modules"


def _load_json(filepath: Path) -> dict:
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _load_text(filepath: Path) -> str:
    try:
        with open(filepath) as f:
            return f.read()
    except IOError:
        return ""


def list_personas() -> list:
    """Scan personas directory and return available personas."""
    if not PERSONAS_DIR.exists():
        return []
    personas = []
    for d in sorted(PERSONAS_DIR.iterdir()):
        if d.is_dir() and (d / "PERSONA.md").exists():
            desc = ""
            if (d / "PARAMS.json").exists():
                schema = _load_json(d / "PARAMS.json")
                desc = schema.get("description", "")
            if not desc:
                # Pull first non-header line from PERSONA.md
                with open(d / "PERSONA.md") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            desc = line[:100]
                            break
            personas.append({"name": d.name, "description": desc})
    return personas


def inject_sources(schema: dict) -> dict:
    """Resolve inject params using sources.py — same mechanism modules use."""
    sys.path.insert(0, str(SKILL_DIR / "scripts"))
    from sources import resolve as resolve_sources
    return resolve_sources(schema)


def assemble_persona(persona_name: str) -> str:
    """
    Load all persona files and assemble into a single context block.
    
    Returns the protocol output string.
    """
    persona_path = PERSONAS_DIR / persona_name

    if not persona_path.exists() or not (persona_path / "PERSONA.md").exists():
        available = [p["name"] for p in list_personas()]
        hint = f" Available: {', '.join(available)}" if available else ""
        return f"ERROR:No persona found for '{persona_name}'.{hint}"

    # Load PERSONA.md
    persona_md = _load_text(persona_path / "PERSONA.md")

    # Load and inject params
    params = {}
    if (persona_path / "PARAMS.json").exists():
        schema = _load_json(persona_path / "PARAMS.json")
        params = inject_sources(schema)

    # Substitute {param_name} in PERSONA.md
    for key, value in params.items():
        persona_md = persona_md.replace(f"{{{key}}}", str(value))

    # Load STYLE.json
    style = {}
    if (persona_path / "STYLE.json").exists():
        style = _load_json(persona_path / "STYLE.json")

    # Load TRIGGERS.json
    triggers = {}
    if (persona_path / "TRIGGERS.json").exists():
        triggers = _load_json(persona_path / "TRIGGERS.json")

    # Build context payload
    context = {
        "persona": persona_name,
        "persona_md": persona_md,
        "style": style,
        "triggers": triggers,
        "dispatch_script": str(SKILL_DIR / "scripts" / "dispatch.py"),
        "skill_dir": str(SKILL_DIR)
    }

    return f"LOAD_PERSONA:{persona_path / 'PERSONA.md'}|CONTEXT:{json.dumps(context)}"


def dispatch_persona(message: str) -> str:
    """
    Parse persona commands:
      reflex persona walt     → load walt persona
      reflex persona list        → list available personas
      reflex persona             → list available personas
    """
    import shlex
    try:
        words = shlex.split(message.strip().lower())
    except ValueError:
        words = message.strip().lower().split()

    # Find 'persona' keyword
    persona_idx = -1
    for i, w in enumerate(words):
        if w == "persona":
            persona_idx = i
            break

    if persona_idx == -1:
        return "ERROR:No 'persona' keyword found in message"

    remaining = words[persona_idx + 1:]

    if not remaining or remaining[0] in ("list", "all"):
        personas = list_personas()
        if not personas:
            return "ERROR:No personas found. Create one in personas/ directory."
        return f"LIST_PERSONAS:{json.dumps(personas)}"

    persona_name = remaining[0]
    return assemble_persona(persona_name)


def main():
    if len(sys.argv) < 2:
        personas = list_personas()
        print("REFLEX PERSONAS — Persistent Conversational Layer")
        if personas:
            for p in personas:
                print(f"  [{p['name']}] {p['description']}")
        else:
            print("  No personas found.")
        sys.exit(0)

    if sys.argv[1] == '-':
        message = sys.stdin.read().strip()
    else:
        message = " ".join(sys.argv[1:])

    result = dispatch_persona(message)
    print(result)


if __name__ == "__main__":
    main()

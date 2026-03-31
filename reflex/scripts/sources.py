#!/usr/bin/env python3
"""
Context Providers — Runtime-discoverable state for modules.

Modules declare what context they need via PARAMS.json:
    {"inject": "module_registry"}
    {"inject": "workspace_state"}
    {"inject": "lens_library"}

The dispatch script calls resolve() with the param schema.
This file returns the filled values. Dispatch never knows
what the sources contain or which modules use them.

Adding a new source:
  1. Write a function that returns a string.
  2. Add it to SOURCES.

No changes to dispatch.py. Ever. The convention is the interface.
"""

import json
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
MODULES_DIR = SKILL_DIR / "modules"


def _load_json(filepath: Path) -> dict:
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def module_registry() -> str:
    """
    Scan all modules and build a compact, grouped registry string.
    Reads optional 'group' field from each PARAMS.json.
    """
    if not MODULES_DIR.exists():
        return "No modules found."

    modules = sorted([
        d.name for d in MODULES_DIR.iterdir()
        if d.is_dir() and (d / "MODULE.md").exists()
    ])

    grouped = {}

    for name in modules:
        mp = MODULES_DIR / name
        group = "utility"
        params_desc = []
        description = ""

        if (mp / "PARAMS.json").exists():
            schema = _load_json(mp / "PARAMS.json")
            group = schema.get("group", "utility")
            for pname, pspec in schema.get("params", {}).items():
                if pspec.get("inject"):
                    continue
                req = "*" if pspec.get("required") else ""
                params_desc.append(f"{pname}{req}")
            description = schema.get("description", "")

        if not description and (mp / "MODULE.md").exists():
            with open(mp / "MODULE.md") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        description = line[:80]
                        break

        if group not in grouped:
            grouped[group] = []

        param_str = f" ({', '.join(params_desc)})" if params_desc else ""
        desc_str = f" — {description}" if description else ""
        grouped[group].append(f"{name}{param_str}{desc_str}")

    group_order = ["source", "analyzer", "transformer", "formatter", "utility"]
    lines = []
    for g in group_order:
        if g in grouped:
            lines.append(f"[{g.upper()}]")
            for entry in sorted(grouped[g]):
                lines.append(f"  {entry}")
            del grouped[g]
    for g, entries in sorted(grouped.items()):
        lines.append(f"[{g.upper()}]")
        for entry in sorted(entries):
            lines.append(f"  {entry}")

    return "\n".join(lines)


def workspace_state() -> str:
    """
    Scan /home/claude/ for JSON files and summarize what's been produced.
    """
    workspace = Path("/home/claude")
    if not workspace.exists():
        return "No workspace files found."

    files = sorted(workspace.glob("*.json"))
    if not files:
        return "No workspace files found."

    lines = []
    for f in files:
        try:
            data = _load_json(f)
            target = data.get("target", "")
            summary = data.get("summary", "")[:100] if data.get("summary") else ""
            info = f"{f.name}"
            if target:
                info += f" (target: {target})"
            if summary:
                info += f" — {summary}"
            lines.append(info)
        except Exception:
            lines.append(f"{f.name} (unreadable)")

    return "\n".join(lines)


def lens_library() -> str:
    """
    Read the canonical lens definitions from perspective/LENSES.json.
    Also scan workspace for custom lens files (lens_*.json).
    Returns a compact summary for formatter modules to reference
    when pre-committing to a weakness.
    """
    # Built-in lenses from perspective module
    lenses_file = MODULES_DIR / "perspective" / "LENSES.json"
    built_in = []
    if lenses_file.exists():
        data = _load_json(lenses_file)
        for lens in data.get("lenses", []):
            name = lens.get("name", "")
            when = lens.get("when", "")
            if name:
                built_in.append(f"- {name}: {when}")

    # Custom workspace lenses
    workspace = Path("/home/claude")
    custom = []
    if workspace.exists():
        for f in sorted(workspace.glob("lens_*.json")):
            data = _load_json(f)
            if "lenses" in data:
                for lens in data["lenses"]:
                    name = lens.get("name", f.stem)
                    when = lens.get("when", "custom lens")
                    custom.append(f"- {name}: {when}")
            elif "name" in data:
                custom.append(f"- {data['name']}: {data.get('when', 'custom lens')}")

    lines = []
    if built_in:
        lines.append("Built-in lenses:")
        lines.extend(built_in)
    if custom:
        lines.append("Custom lenses (from workspace):")
        lines.extend(custom)

    return "\n".join(lines) if lines else "No lenses found."


# --- The convention: name → function ---
# Adding a source = adding one function + one entry here.
SOURCES = {
    "module_registry": module_registry,
    "workspace_state": workspace_state,
    "lens_library": lens_library,
}


def resolve(schema: dict) -> dict:
    """
    Given a PARAMS.json schema, return a dict of {param_name: value}
    for every param that declares an 'inject' source.
    Called by dispatch.py. Returns only the injectable params.
    """
    injected = {}
    for name, spec in schema.get("params", {}).items():
        if "inject" in spec:
            source_name = spec["inject"]
            if source_name in SOURCES:
                injected[name] = SOURCES[source_name]()
    return injected

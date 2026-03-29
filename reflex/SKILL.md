---
name: callsign
description: ALWAYS use this skill when the user says the word "callsign" in any form. This includes "callsign" by itself, "callsign foxtrot", "callsign pirate", "callsign code-review", "callsign help", "callsign plan", "callsign write-report", or "callsign" followed by any other word. Even if the message is just the single word "callsign" with nothing else, use this skill. This skill MUST fire on any message containing "callsign" — do not attempt to handle it yourself. This is a Convention-Based Meta-Skill Dispatcher that dynamically loads sub-skills (called modules) at runtime through filesystem convention.
---

# Reflex — Convention-Based Meta-Skill Dispatcher

A skill that discovers and loads modules at runtime through filesystem convention. Modules self-describe their requirements through optional files. No registry, no config, no hardcoded lists.

## Architecture

Three layers, three files, three jobs:

- **`scripts/dispatch.py`** — Routes modules. Reads the filesystem, extracts params, builds chains, runs resolvers. Knows nothing about what modules do.
- **`scripts/sources.py`** — Provides context. Gathers runtime state (module registry, workspace files) that modules can request via injection. Knows nothing about which modules use it.
- **`modules/`** — Defines behavior. Each module is a folder. Convention determines capability.

## Context Efficiency

The framework minimizes context usage through four disclosure tiers:

1. **System prompt**: Only this SKILL.md's frontmatter loads at startup (~50 tokens),
   regardless of how many modules are installed. Module content never pre-loads.
2. **Dispatch routing**: Module resolution happens in Python (dispatch.py),
   not in LLM inference. Routing costs zero context tokens.
3. **Module loading**: Only the matched module's MODULE.md enters context.
   All other modules remain unloaded.
4. **Variant selection**: For Level 3 modules, RESOLVE.py selects a variant
   in Python before loading. Unselected variants never enter context.

This means a system with 1,000 modules has the same context overhead as a
system with 3 modules — the cost is always one SKILL.md frontmatter entry
plus one MODULE.md body.

## Module Levels

- **Level 0**: `MODULE.md` only. Pure behavioral injection.
- **Level 1**: `MODULE.md` + `PARAMS.json`. Module declares its inputs.
- **Level 2**: `MODULE.md` + `PARAMS.json` + `DEPENDS.json`. Module declares dependencies with parameter forwarding.
- **Level 3**: `MODULE.md` + `PARAMS.json` + `RESOLVE.py`. Module adapts at runtime. A resolver script evaluates conditions and selects a variant before dispatch completes.

Level 3 modules range from simple conditional routing (check a value, pick a variant)
to registry-aware meta-routing (inject the module registry, evaluate system capabilities,
compose new chains). The power comes from combining RESOLVE.py with `"inject"` params —
a resolver that receives the module registry can reason about the entire system.

Each level is optional and degrades gracefully.

## PARAMS.json conventions

Standard param fields:
- `"required": true/false` — whether dispatch enforces presence
- `"default": "value"` — fallback if not provided
- `"description": "text"` — human-readable explanation

Extended fields:
- `"greedy": true` — absorb all remaining positional words into this param (for free-text input)
- `"inject": "source_name"` — filled automatically by sources.py at dispatch time, not by the user

Module metadata fields (top-level in PARAMS.json, not inside `params`):
- `"group": "source|analyzer|transformer|formatter|utility|meta"` — categorization for registry
- `"description": "text"` — one-line module description for registry

## How to respond

### Step 1: Run the dispatch script

Always run the dispatch script first. Pass the user's exact message via stdin using a heredoc. Do NOT modify, reformat, or "fix" the message in any way:
```bash
python3 {SKILL_DIR}/scripts/dispatch.py - <<'DISPATCH_INPUT'
{USER_MESSAGE}
DISPATCH_INPUT
```

The `{USER_MESSAGE}` must be reproduced exactly as the user typed it — including any quotes, colons, or special characters within parameter values.
Replace `{SKILL_DIR}` with the directory containing this SKILL.md.
Replace `{USER_MESSAGE}` with the user's exact message text.

For slash command invocation like `/callsign code-review python`, the full message text is the user's message.

### Step 2: Follow the protocol

The script outputs one of these:

**`LOAD_MODULE:/path`** → Read the file, follow its instructions. (Level 0)

**`LOAD_MODULE_WITH_PARAMS:/path|PARAMS:{...}`** → Read the file, substitute `{param_name}` with values from the params JSON. (Level 1)

**`CHAIN:[{step1},{step2}]`** → Execute steps in order. For each step: read the MODULE.md, apply params, produce output. Carry output from earlier steps forward as context for later steps. The final step's output is your response. (Level 2)

**`RESOLVED:/path|PARAMS:{...}|RESOLVED_BY:script_name|REASON:text`** → A resolver script selected this variant at runtime. Read the file, apply params. The REASON field explains why this variant was chosen — include it briefly in your response so the user understands the routing. (Level 3)

**`RESPOND:text`** → Reply with exactly that text, nothing else.

**`MISSING_PARAMS:module|required:[...]|provided:[...]|missing:[...]`** → Tell the user what's needed.

**`ERROR:message`** → Reply with "Unknown callsign."

### Rules

- Do NOT skip the dispatch script
- Do NOT add commentary beyond what the module instructs
- For CHAIN: carry context forward between steps naturally
- For RESOLVED: briefly note why the variant was selected, then follow the module
- When substituting params, replace `{param_name}` in the MODULE.md text with the actual value

## Adding modules

**Level 0**: Create `modules/{name}/MODULE.md`

**Level 1**: Add `PARAMS.json`

**Level 2**: Add `DEPENDS.json`

**Level 3**: Add `RESOLVE.py` + `variants/{name}/MODULE.md`

The resolver receives params as a JSON string argument and prints the variant name to stdout. The dispatch script resolves that name to `variants/{name}/MODULE.md`.

## Adding context sources

Add a function to `scripts/sources.py` and register it in the `SOURCES` dict. Any module can then request it via `"inject": "your_source_name"` in its PARAMS.json.

Current sources:
- `module_registry` — scanned list of all modules, grouped by role, with params and descriptions
- `workspace_state` — summary of JSON files produced in the current session

No changes to dispatch.py. The convention is the interface.

## RESOLVE.py contract

```python
#!/usr/bin/env python3
import sys, json
params = json.loads(sys.argv[1])
# Evaluate conditions, print variant name
print("variant-name")
```

The resolver can use any logic: time-based seeds, value thresholds, external data, randomness. Its only job is to print one word: the variant folder name.

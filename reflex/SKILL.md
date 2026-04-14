---
name: Reflex
description: ALWAYS use this skill when the user says the word "reflex" in any form. This includes "reflex" by itself, "reflex foxtrot", "reflex pirate", "reflex code-review", "reflex help", "reflex plan", "reflex report", or "reflex" followed by any other word. Even if the message is just the single word "reflex" with nothing else, use this skill. This skill MUST fire on any message containing "reflex" — do not attempt to handle it yourself. This is a Convention-Based Meta-Skill Dispatcher that dynamically loads sub-skills (called modules) at runtime through filesystem convention.
---

# Reflex — Convention-Based Meta-Skill Dispatcher

A skill that discovers and loads modules at runtime through filesystem convention. Modules self-describe their requirements through optional files. No registry, no config, no hardcoded lists.

## Architecture

Four layers, two dispatch paths, shared injection:

- **`scripts/dispatch.py`** — Routes modules. Reads the filesystem, extracts params, builds chains, runs resolvers. Knows nothing about what modules do.
- **`scripts/persona.py`** — Routes personas. Assembles persistent conversational context from persona files. Knows nothing about modules.
- **`scripts/sources.py`** — Provides context. Gathers runtime state (module registry, workspace files) that both modules and personas can request via injection.
- **`modules/`** — Bounded tools. Each module is a folder. Composable via `+` chains.
- **`personas/`** — Persistent wrappers. Each persona is a folder. Not composable — they invoke modules internally.

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

Level 3 modules range from simple conditional routing (check a value, pick a variant) to registry-aware meta-routing (inject the module registry, evaluate system capabilities, compose new chains). The power comes from combining RESOLVE.py with `"inject"` params — a resolver that receives the module registry can reason about the entire system.

Level 2+3 Composability: A module can have both DEPENDS.json and RESOLVE.py. Dependencies run first (subject to unless_exists conditions), then the resolver selects a variant. This enables modules that conditionally prepare upstream data before routing to a behavior. If a dependency is itself Level 3, its resolver is also run to select the correct variant.

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

## DEPENDS.json conventions

Conditional dependencies: A dependency can declare "unless_exists": "pattern.json" where the pattern supports {param_name} substitution. If any file in /home/claude/ matches the glob, the dependency is skipped. This enables caching — dependencies only run when their output doesn't already exist.

{
  "before": [
    {
      "module": "plan",
      "forward_params": { "intent": "{intent}" },
      "output_key": "plan_output",
      "unless_exists": "run_plan.json"
    }
  ]
}

## How to respond

### Step 1: Route to the correct dispatcher

Check whether the user's message contains the word "persona" (e.g., "reflex persona walt", "reflex persona list").

**If the message contains "persona"** → route to persona.py:
```bash
python3 {SKILL_DIR}/scripts/persona.py - <<'DISPATCH_INPUT'
{USER_MESSAGE}
DISPATCH_INPUT
```

**Otherwise** → route to dispatch.py (the default):
```bash
python3 {SKILL_DIR}/scripts/dispatch.py - <<'DISPATCH_INPUT'
{USER_MESSAGE}
DISPATCH_INPUT
```

The `{USER_MESSAGE}` must be reproduced exactly as the user typed it — including any quotes, colons, or special characters within parameter values.
Replace `{SKILL_DIR}` with the directory containing this SKILL.md.
Replace `{USER_MESSAGE}` with the user's exact message text.

For slash command invocation like `/reflex code-review python`, the full message text is the user's message.

### Step 2: Follow the protocol

The script outputs one of these:

**`LOAD_MODULE:/path`** → Read the file, follow its instructions. (Level 0)

**`LOAD_MODULE_WITH_PARAMS:/path|PARAMS:{...}`** → Read the file, substitute `{param_name}` with values from the params JSON. (Level 1)

**`CHAIN:[{step1},{step2}]`** → Execute steps in order. For each step: read the MODULE.md, apply params, produce output. Carry output from earlier steps forward as context for later steps. The final step's output is your response. (Level 2)

**`RESOLVED:/path|PARAMS:{...}|RESOLVED_BY:script_name|REASON:text`** → A resolver script selected this variant at runtime. Read the file, apply params. The REASON field explains why this variant was chosen — include it briefly in your response so the user understands the routing. (Level 3)

**`RESPOND:text`** → Reply with exactly that text, nothing else.

**`MISSING_PARAMS:module|required:[...]|provided:[...]|missing:[...]`** → Tell the user what's needed.

**`ERROR:message`** → Reply with "Unknown reflex."

#### Persona protocol (from persona.py)

**`LOAD_PERSONA:/path|CONTEXT:{...}`** → A persona is loading. Parse the CONTEXT JSON — it contains:
- `persona_md`: Full persona instructions (already param-substituted). Read and follow these as your operating frame for the rest of the conversation.
- `style`: Voice and formatting rules. Internalize these.
- `triggers`: Situational patterns to watch for. Use these to decide when to invoke modules.
- `dispatch_script`: Path to dispatch.py. Use this when the persona decides to invoke a module.
- `skill_dir`: Path to the reflex skill directory.

Once a persona is loaded, you ARE that persona until the user shifts away or explicitly exits. Every subsequent response follows the persona's instructions. When the persona decides to invoke a module, call dispatch.py directly — the persona stays active while modules run underneath.

**`LIST_PERSONAS:[...]`** → Show the available personas to the user.

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

## Adding personas

Create `personas/{name}/PERSONA.md` — that's the only required file.

Optional files (degrade gracefully if absent):
- `PARAMS.json` — Inject-only params (registry, workspace). Same format as module PARAMS.json.
- `TRIGGERS.json` — Situational patterns the persona watches for. Maps conversational signals to suggested modules and behaviors.
- `STYLE.json` — Voice characteristics, tone adaptation rules, signal phrases, formatting rules.

Personas are not modules. They don't appear in the module registry, can't be chained with `+`, and can't be referenced in DEPENDS.json. They invoke modules internally via dispatch.py.

## Adding context sources

Add a function to `scripts/sources.py` and register it in the `SOURCES` dict. Any module can then request it via `"inject": "your_source_name"` in its PARAMS.json.

Current sources:
- `module_registry` — scanned list of all modules, grouped by role, with params and descriptions
- `workspace_state` — summary of JSON files produced in the current session
- `lens_library` — canonical lens definitions from `perspective/LENSES.json` plus any custom `lens_*.json` in the workspace

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

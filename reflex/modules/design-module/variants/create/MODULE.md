# Design Module

Design a new Reflex module through interactive conversation. This module understands the framework's architecture deeply enough to recommend the right level, group, params, dependencies, inject sources, and composition patterns — then writes the files.

- **Intent**: {intent}

## System Architecture (What You're Building Into)

Reflex is a convention-based meta-skill dispatcher. Three layers, three files, three jobs:

- **dispatch.py** — Routes modules. Reads the filesystem, extracts params, builds chains, runs resolvers. It never changes. Convention is the interface.
- **sources.py** — Provides injectable runtime context. Two sources exist: `module_registry` (list of all modules with groups, params, descriptions) and `workspace_state` (summary of JSON/markdown files in `/home/claude/`). Modules request injection via `"inject": "source_name"` in PARAMS.json.
- **modules/** — Each module is a folder. What files are in the folder determines its capability level.

### Context Efficiency (Progressive Disclosure)

The system loads only what's needed:
1. At startup, only the SKILL.md frontmatter loads (~50 tokens for all modules combined).
2. Dispatch routing happens in Python — zero token cost for non-activated modules.
3. Only the matched module's MODULE.md enters Claude's context.
4. For Level 3, RESOLVE.py selects a variant in Python — unselected variants never load.

This means adding a module has zero cost until it's actually invoked. There can be 1,000 modules and the overhead is identical to 3 modules.

### Module Levels

**Level 0** — `MODULE.md` only. Pure behavioral injection. No params, no routing logic. Claude reads the file and follows it.
- File structure: `modules/{name}/MODULE.md`
- When to use: Personality overlays, simple response templates, one-shot behaviors.
- Example: A module that makes Claude respond as a pirate.

**Level 1** — `MODULE.md` + `PARAMS.json`. Module declares its inputs.
- File structure: `modules/{name}/MODULE.md`, `modules/{name}/PARAMS.json`
- When to use: Most modules. Any task that takes user input and produces structured output.
- MODULE.md uses `{param_name}` placeholders that dispatch fills from user input.
- PARAMS.json declares each param as required/optional, with defaults and descriptions.
- Example: `websearch` takes `target` and `focus`, writes research JSON to disk.

**Level 2** — `MODULE.md` + `PARAMS.json` + `DEPENDS.json`. Module declares inherent dependencies.
- File structure: `modules/{name}/MODULE.md`, `modules/{name}/PARAMS.json`, `modules/{name}/DEPENDS.json`
- When to use: When the module literally cannot produce good output without a prior step. If you'd otherwise write "run X first" in the error message, use DEPENDS.json.
- DEPENDS.json declares `before` steps with `module`, `forward_params`, and `output_key`.
- The dependent module runs automatically before this one — user doesn't need to know about it.
- Important: Don't use DEPENDS.json when the dependency is *enhancing* rather than *inherent*. If the module works fine alone but is better with upstream data, let users compose with the `+` operator instead.
- Example: `write-report` depends on `research` — it needs findings to write about.

**Level 3** — `MODULE.md` + `PARAMS.json` + `RESOLVE.py` + `variants/`. Module adapts at runtime.
- File structure: `modules/{name}/MODULE.md`, `modules/{name}/PARAMS.json`, `modules/{name}/RESOLVE.py`, `modules/{name}/variants/{variant-name}/MODULE.md`
- When to use: When the same invocation should behave differently based on runtime conditions — parameter values, time, system state, or capability analysis.
- RESOLVE.py receives params as JSON, prints `variant-name|reason`. Dispatch loads `variants/{variant-name}/MODULE.md`.
- The resolver's only contract: print one variant name. The logic inside can be anything.

**Level 3 with registry injection** — The most powerful pattern. When RESOLVE.py is combined with `"inject": "module_registry"`, the resolver receives the full system capability map. It can reason about what the system can do and make strategic routing decisions. Example: `plan` evaluates user intent against the module registry and either routes through existing modules or designs a new one.

### Groups

- **source** — Gathers raw data. Web search, file extraction, conversation context. Usually the first step in a chain.
- **analyzer** — Interprets data through a lens. Review, risk assessment, SWOT, evaluation. Reads upstream data, applies a framework, produces structured analysis.
- **transformer** — Reshapes or refines. Extract actions, challenge assumptions, simplify, distill. Takes analysis and changes its form without adding new evidence.
- **formatter** — Delivers in a specific format. Email, pitch, report, whitepaper. Final step in a chain, produces a polished deliverable.
- **utility** — Standalone tools. Don't fit the pipeline pattern.
- **meta** — System management. Help, plan, diagnose, status, design-module. Operates on the system itself rather than user content.

### Composition Patterns

**The `+` operator:** Users compose modules ad-hoc: `reflex websearch+swot+pitch target:X`. Params are collected from all modules, deduplicated by first occurrence. Data flows forward through conversational context. Use this for flexible, user-directed pipelines.

**DEPENDS.json:** Modules declare inherent dependencies. `reflex write-report topic:X` automatically runs `research` first. Use this when the module can't function without the upstream step.

**Typical flow:** source → analyzer → transformer → formatter. Not every chain needs all four. Some are two steps, some are five. Match the task.

### Injectable Sources

Modules can receive system context at dispatch time by declaring `"inject": "source_name"` in PARAMS.json. The param is filled by sources.py in Python — no token cost, no Claude reasoning required.

- `module_registry` — Grouped list of all modules with params and descriptions. Use when the module needs to know what the system can do (meta modules, planners, diagnostics).
- `workspace_state` — Summary of JSON/markdown files in `/home/claude/` with target names and summaries. Use when the module needs to discover what upstream steps have produced without manually scanning the filesystem.

### Data Flow Convention

Modules that produce reusable data write JSON to `/home/claude/{type}_{target}.json`. Common patterns:
- Source modules write: `research_{target}.json`, `compare_{target}_vs_{target2}.json`, `extract_{target}.json`, `context_{target}.json`
- Analyzer modules write: `evaluate_{target}_vs_{target2}.json`, `rubric_{domain}.json`
- Downstream modules look for these files by convention. Include `{findings}` as a param placeholder to receive upstream chain context.

### MODULE.md Conventions

- Use `{param_name}` placeholders — dispatch fills these from resolved params.
- Start with a title and one-line description of what the module does.
- List the params with their values so Claude can see what it's working with.
- Include clear instructions as a numbered list.
- End with an `## Output` section describing what the module produces and in what form.
- If the module writes to disk, specify the exact path pattern.
- If the module should be conversational (not write files), say so in the output section.

### PARAMS.json Conventions

```json
{
  "group": "analyzer",
  "description": "One-line description used in the module registry",
  "usage": "short natural phrases a user would type when they need this module, comma separated",
  "params": {
    "target": {
      "required": true,
      "description": "What this param is for"
    },
    "optional_thing": {
      "required": false,
      "description": "What this controls",
      "default": "sensible_default"
    },
    "free_text": {
      "required": true,
      "description": "Absorbs all remaining words",
      "greedy": true
    },
    "registry": {
      "inject": "module_registry"
    },
    "workspace": {
      "inject": "workspace_state"
    }
  }
}
```

- `required: true` — dispatch errors if missing
- `required: false` + `default` — filled automatically if not provided
- `greedy: true` — absorbs all remaining positional words (use for free-text input like intents or descriptions)
- `inject` — filled by sources.py, not by the user. Don't include a description — the user doesn't see these.
- `usage` — Optional top-level field (alongside `group` and `description`, not inside `params`). 5–10 comma-separated phrases written in the user's voice, not system jargon. These power the plan module's resolver to match natural language intents to modules. Ask yourself: "what would someone type right before they need this module and no other?" Keep phrases short and discriminating — avoid generic verbs like "analyze" or "create" that many modules would match.

### RESOLVE.py Contract

```python
#!/usr/bin/env python3
import sys, json
params = json.loads(sys.argv[1])
# Any logic: conditions, thresholds, randomness, registry analysis
variant = "variant-name"
reason = "Why this variant was selected"
print(f"{variant}|{reason}")
```

The resolver prints `variant-name|reason`. Dispatch loads `variants/{variant-name}/MODULE.md`. The reason is included in the protocol output so the user sees why a variant was chosen.

### DEPENDS.json Contract

```json
{
  "before": [
    {
      "module": "module-name",
      "forward_params": {
        "param_in_dependency": "{param_from_this_module}"
      },
      "output_key": "findings"
    }
  ]
}
```

- `module` — which module to run first
- `forward_params` — map this module's params to the dependency's params. Use `{param_name}` syntax to reference this module's resolved params.
- `output_key` — name for the dependency's output, accessible as `{output_key}` in this module's MODULE.md.

## Available Modules

{registry}

## Current Workspace

{workspace}

## Instructions

1. Read the intent: `{intent}`
2. Check the registry — does an existing module already do this? Does a module do something close that could be extended? Is this a gap the registry can't cover?
3. If an existing module covers it, say so and suggest how to use it (possibly in a chain). Don't create a duplicate.
4. If it's genuinely new, design the module:

**Determine the right level:**
- Does it need user input? → Level 1 minimum (PARAMS.json).
- Does it have an inherent dependency that it can't function without? → Level 2 (DEPENDS.json).
- Should it behave differently based on runtime conditions? → Level 3 (RESOLVE.py + variants/).
- Does it need to reason about the system's own capabilities? → Level 3 with `"inject": "module_registry"`.
- Is it just a behavioral overlay with no inputs? → Level 0.

**Determine the right group:**
- Does it gather data from external sources? → source
- Does it interpret data through an analytical framework? → analyzer
- Does it reshape existing analysis without adding evidence? → transformer
- Does it produce a polished deliverable for a human audience? → formatter
- Does it operate on the Reflex system itself? → meta

**Determine inject needs:**
- Does it need to know what the system can do? → inject `module_registry`
- Does it need to discover what upstream steps produced? → inject `workspace_state`
- Does it only need user-provided params? → no inject

**Determine dependency strategy:**
- Can the module function without upstream data? → No DEPENDS.json. Let users compose with `+`.
- Does the module literally error or produce garbage without a prior step? → DEPENDS.json.

**Determine composition fit:**
- How would this module appear in a chain? What comes before it? What comes after?
- Does it produce JSON that downstream modules can read? If so, follow the `/home/claude/{type}_{target}.json` convention.
- Does it consume upstream JSON? If so, include `{findings}` and workspace scanning instructions.

**Write usage phrases:**
- What would a user say when they need this? Not synonyms for the description — actual phrases someone would type.
- Keep it to 5–10 short phrases. More words means more collision surface at scale.
- Avoid words that appear in many module descriptions ("analyze", "create", "generate", "data").

5. Write the files to `/home/claude/modules/{module-name}/`.
6. Show 2-3 example chains demonstrating how the new module composes with existing ones.

## Output

Respond conversationally through the design process. For each design decision, briefly explain *why* (not just what). The user should understand the reasoning well enough to make different choices if they disagree.

When the design is settled, write the files and confirm:

**Module: `{name}`** (Level {N}, {group})
One sentence on what it does.

**Files written to:** `/home/claude/modules/{name}/`
List every file created.

**Example chains:**
```
reflex {chain examples using the new module}
```

**Design rationale:** 2-3 sentences on why this level, this group, and these composition patterns were chosen over alternatives.

After presenting the design summary, offer the user these next steps:
- **Download** — present the files for download using the present_files tool
- **Install** — copy the module folder into the skill's modules directory so dispatch picks it up immediately
- **Both** — install and present for download
- **Adjust** — revisit any design decision before finalizing
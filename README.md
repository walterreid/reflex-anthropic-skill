# Reflex — Convention-Based Meta-Skill Dispatcher

Reflex is a skill for Claude that discovers and loads behavioral modules at runtime through filesystem convention. No registry, no config, no hardcoded lists. You say `reflex [module]`, a Python router finds the module, and only that module's instructions enter the LLM context.

A system with 1,000 modules has the same context overhead as a system with 3.

**[View the interactive architecture visualizations](https://walterreid.github.io/reflex-anthropic-skill/architecture-visualizations.html)** — progressive disclosure, chain composition, evidence traceability, persona system, and the bounded vs. unbounded distinction explained visually.

## Why This Exists

LLM skills typically face a tradeoff: more capabilities means more tokens burned on instructions the model never uses. Reflex eliminates this by deferring everything:

- **Routing happens in Python**, not in inference. Zero context tokens for dispatch.
- **Only the matched module loads.** All others remain on disk.
- **For branching modules, a Python resolver picks the variant** before the LLM sees anything. Unselected variants never enter context.

The cost is always: one SKILL.md frontmatter entry (~50 tokens) + one MODULE.md body.

## What It's Good At

Reflex shines when you need **structured, multi-step analytical pipelines** — the kind of work where each stage's output feeds the next and the final deliverable is grounded in accumulated evidence. Examples:

- **Market analysis chains**: `reflex trends+competitive-messaging+audience-portrait+creative-brief+tagline+email target:"DTC skincare for men"`
- **GTM strategy pipeline**: `reflex gtm-strategy target:"RouteForge"` — auto-chains websearch, competitors, positioning, and audience-portrait, then builds a beachhead-scored strategy with confidence assessment
- **Evidence-certified deliverables**: `reflex websearch+gtm-strategy+certify+report target:"RouteForge"` — the report ships with an embedded appendix mapping every claim to its source, confidence level, and methodology
- **Competitive intelligence**: `reflex websearch+competitors+landscape+opportunities target:anthropic`
- **Code review with adaptive routing**: `reflex adaptive-review language:python` (auto-routes to quick, deep, or security review based on code context)
- **Conversational access**: `reflex persona copilot` — loads a persistent thinking partner that silently orchestrates modules. The user just talks; the copilot decides when to invoke modules, which ones, with what params
- **Natural language planning**: `reflex plan intent:"analyze my competitor's pricing strategy and write a memo for my CEO"` — the system decomposes this into a runnable module chain

It also handles simple things — `reflex pirate` will greet you as a pirate captain, `reflex coin-flip` picks heads or tails via a time-based resolver — but the architecture is designed for composable analytical work.

## Quick Start

### Invocation

Say `reflex` followed by a module name and optional parameters:

```
reflex research topic:"electric vehicles" depth:detailed
reflex code-review language:python style:strict
reflex swot target:tesla industry:automotive
```

### Chaining with `+`

Compose modules into pipelines. Data flows forward — each step's output becomes context for the next:

```
reflex research+swot+actions target:anthropic
reflex websearch+distill+pitch target:"AI safety" audience:investors
reflex trends+competitive-messaging+creative-brief target:"plant-based meat"
```

Typical flow: **source -> analyzer -> transformer -> formatter**

### Parameters

- **Named**: `target:value`, `audience:"millennial men"` (quotes for multi-word values)
- **Positional**: First unnamed word fills the first required param. `reflex swot tesla` = `reflex swot target:tesla`
- **Greedy**: Some params absorb all remaining words (e.g., `intent` in the `plan` module)

### Natural Language (Let the System Figure It Out)

If you don't know which modules to use:

```
reflex plan intent:"I need to understand the competitive landscape for cloud kitchens in Southeast Asia and produce a board-ready memo"
```

The `plan` module scans the full registry, proposes a chain, and explains why. You run it or modify it.

## Key Commands

### `reflex help`

Your entry point. Shows the system overview, module catalog, or details on any specific module.

```
reflex help              # System overview
reflex help list         # Full module catalog (grouped by category)
reflex help research     # Deep dive on a specific module with example commands
reflex help chains       # Explain how chaining works
```

### `reflex plan`

Translates natural language into a runnable chain. This is a **Level 3 module** — a passthrough resolver always routes to the `route` variant, where the LLM evaluates the intent against the full module registry and decides whether to compose a chain from existing modules or design a new one.

Plan writes `run_plan.json` to disk, which the `run` module picks up for step-by-step execution. For high-stakes chains ending with a formatter, `plan` may suggest appending `+perspective` as a quality gate.

```
reflex plan intent:"research my competitor Acme Corp, build a SWOT, then write a pitch for investors"
```

### `reflex run`

Executes a planned pipeline step-by-step, pausing between each module for user review. This is a **stateful workflow** — you can stop, resume, skip steps, or reset.

The `run` module is Level 2+3: it has both dependencies (auto-runs `plan` if no plan exists) and a resolver (checks workspace state to pick the right variant):

- **`start`**: No plan exists yet. Runs `plan` first, then begins executing step 1. Writes `run_plan.json` to track state.
- **`continue`**: Plan exists with pending steps. Picks up where you left off. Say `reflex run` to continue, `reflex run skip` to skip the current step.
- **`reset`**: Clears the plan and resets state. Workspace files from completed steps are preserved.

```
reflex run intent:"full competitive analysis of Notion vs Coda"
# ...executes step 1, pauses...
reflex run          # continues to step 2
reflex run skip     # skips current step
reflex run reset    # clears the plan
```

### `reflex test-dispatch`

Smoke tests the dispatch router across all levels, features, and edge cases. Runs a Python test suite against `dispatch.py` and reports pass/fail.

```
reflex test-dispatch          # Run all tests
reflex test-dispatch scope:chains   # Test only chain routing
```

### `reflex status`

Shows what's been produced in the current session workspace — which JSON artifacts exist, what they contain, and what modules generated them.

### `reflex design-module`

Interactive module creator. Describe what you want and it either builds a new module or upgrades an existing one:

```
reflex design-module intent:"a module that generates pricing strategies"
reflex design-module    # Opens triage mode — suggests what to build based on gaps
```

## Architecture

### Architecture

```
reflex/
├── SKILL.md              # Entry point. Only the frontmatter loads at startup (~50 tokens)
├── scripts/
│   ├── dispatch.py       # Module router: parses message, resolves module, outputs protocol
│   ├── persona.py        # Persona router: assembles persistent conversational context
│   └── sources.py        # Shared context injection for both dispatch paths
├── modules/              # Bounded, composable tools (78 modules)
│   └── <name>/
│       ├── MODULE.md     # Instructions (loaded only when this module wins dispatch)
│       ├── PARAMS.json   # Optional: declared inputs with types, defaults, descriptions
│       ├── DEPENDS.json  # Optional: upstream dependencies with conditional execution
│       ├── RESOLVE.py    # Optional: Python script that picks a variant at runtime
│       └── variants/     # Optional: variant-specific MODULE.md files
└── personas/             # Persistent, unbounded conversational wrappers
    └── <name>/
        ├── PERSONA.md    # Identity and behavior (required)
        ├── PARAMS.json   # Inject-only params (optional)
        ├── TRIGGERS.json # Situational pattern matching (optional)
        └── STYLE.json    # Voice and tone rules (optional)
```

- **`dispatch.py`** routes modules. It reads the filesystem, extracts params, builds chains, runs resolvers. It knows nothing about what modules do.
- **`persona.py`** routes personas. It assembles persistent context from persona files. It knows nothing about modules.
- **`sources.py`** provides context. Both dispatch paths share it. Modules and personas can both request runtime data via injection.
- **`modules/`** define bounded behavior. Each module is a folder. Convention determines capability.
- **`personas/`** define persistent behavior. Each persona is a folder. They invoke modules internally but can't be chained with them.

### Module Levels

| Level | Files Required | Capability | Example |
|-------|---------------|------------|---------|
| **0** | `MODULE.md` | Pure behavioral injection. No params. | `pirate`, `foxtrot` |
| **1** | + `PARAMS.json` | Declared inputs with validation, defaults, injection | `research`, `swot`, `code-review` |
| **2** | + `DEPENDS.json` | Dependency chains with conditional execution | `report`, `evaluate`, `full-analysis` |
| **3** | + `RESOLVE.py` + `variants/` | Runtime variant selection via Python | `plan`, `run`, `adaptive-review`, `coin-flip` |

Levels compose: a module can be Level 2+3 (both `DEPENDS.json` and `RESOLVE.py`). Dependencies run first, then the resolver selects a variant. The `run` module uses this pattern.

### Dispatch Protocol

When invoked, `dispatch.py` outputs exactly one protocol line:

| Output | Meaning |
|--------|---------|
| `LOAD_MODULE:/path` | Load this MODULE.md, follow its instructions |
| `LOAD_MODULE_WITH_PARAMS:/path\|PARAMS:{json}` | Load and substitute `{param_name}` placeholders |
| `CHAIN:[{step1},{step2}...]` | Execute steps in order, carry context forward |
| `RESOLVED:/path\|PARAMS:{json}\|RESOLVED_BY:script\|REASON:text` | Resolver picked this variant; briefly note the reason |
| `MISSING_PARAMS:module\|required:[...]\|provided:[...]\|missing:[...]` | Validation failed — tell user what's needed |
| `RESPOND:text` | Reply with this text verbatim |
| `ERROR:message` | Something broke |

### Context Injection

Modules can declare `"inject": "source_name"` on any parameter in PARAMS.json. At dispatch time, `sources.py` fills these automatically:

- **`module_registry`**: Scanned list of all installed modules, grouped by role (source, analyzer, transformer, formatter, utility, meta), with params and descriptions. This is how `plan` and `help` know what's available without hardcoding.
- **`workspace_state`**: Summary of JSON files in the current session workspace. This is how `run` knows whether to start, continue, or reset.
- **`lens_library`**: Canonical lens definitions from `perspective/LENSES.json` plus any custom `lens_*.json` files in the workspace. This is how formatters know which evaluation lenses exist for pre-commit self-assessment.

To add a new source: write a function in `sources.py`, register it in the `SOURCES` dict. Any module can then request it. No changes to `dispatch.py`.

### Conditional Dependencies

`DEPENDS.json` supports `unless_exists` — a glob pattern checked against the workspace before running the dependency:

```json
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
```

If `run_plan.json` already exists, the `plan` dependency is skipped. This enables **caching and resumability** — the `run` module uses this to avoid re-planning on every invocation.

### Specialization Pattern (Level 2 as Composition)

Level 2 modules aren't just for multi-step pipelines. They also enable a powerful **specialization pattern**: a module that depends on a general-purpose module but adds a domain-specific output structure on top.

The idea: instead of building a new module from scratch, you write a thin synthesis layer that delegates the heavy lifting to an existing module via `DEPENDS.json`, then reshapes the output for a specific use case.

```
┌─────────────┐         ┌──────────────────┐
│   extract    │────────>│    transcript    │
│  (general)   │  dep    │  (specialized)   │
│              │         │                  │
│ Pulls raw    │         │ Adds: decisions, │
│ structured   │         │ action items,    │
│ data from    │         │ ownership,       │
│ any file     │         │ missed opps      │
└─────────────┘         └──────────────────┘
```

**Example**: `transcript` depends on `extract`. The `extract` module does the hard work of pulling structured data from a file. The `transcript` MODULE.md receives that output and restructures it into a meeting-specific format — decisions with authority tags, action items with owners, missed opportunities. The dependency does the extraction; the module adds the domain lens.

This pattern has three properties that make it valuable:

1. **No duplication.** The specialized module never reimplements what the dependency does. If `extract` improves, every module that depends on it improves automatically.

2. **Clean routing for `plan`.** When the `plan` module scans the registry, it sees both `extract` (general-purpose) and `transcript` (meeting-specific). It can route precisely: a user who says "analyze this transcript" gets `transcript`; a user who says "pull data from this CSV" gets `extract`. No ambiguity.

3. **Composable in chains.** Because specialized modules are just Level 2 modules, they chain normally with `+`. You can run `transcript+actions+email` — the dependency runs silently, and the chain sees a clean meeting record flowing into action extraction flowing into a follow-up email.

**When to use this vs. inline chains (`+`):**

| Approach | Use When |
|----------|----------|
| Inline chain (`research+swot`) | Ad-hoc composition. The user knows which modules to combine. |
| Specialization (`transcript` → depends on `extract`) | The combination is a recurring pattern AND the specialized module adds output structure the dependency doesn't provide. |
| `full-analysis` pattern | The entire pipeline is fixed and the module exists to be a one-command shortcut. |

The specialization pattern sits between ad-hoc chaining and pre-built pipelines. It's how the system grows without bloating: every new specialized module reuses existing analytical work and only adds the domain-specific framing that justifies its existence.

Current specialization modules:

| Specialized Module | Depends On | What It Adds |
|---|---|---|
| `transcript` | `extract` | Meeting-specific structure: decisions, actions, ownership, missed opportunities |
| `audit` | `debrief` | Quality-gate scoring: 5 dimensions, pass/fail verdict, biggest single fix |
| `voice-dna` | `extract` | Reusable voice profile: rhythm, tone, vocabulary fingerprint, structural preferences |
| `ideate` | `decompose` | Divergent framing: inversion, analogy, constraint, JTBD lenses on sub-questions |
| `experiment` | `scenario` | Hypothesis design: variables, success/failure criteria, confounds, debrief template |
| `onboard` | `recap` | Handoff document: audience-calibrated, organized by what the reader needs first |
| `forecast` | `trends` | Structured projection: base/upside/downside cases with explicit sourced-vs-estimated flagging |
| `retro` | `debrief` | Session reflection: surprises, carry-forward items, process lessons |
| `full-analysis` | `websearch+distill+rubric+evaluate` | One-command pipeline: the original specialization module |

## Self-Improving Chains

The `perspective` module applies an evaluation lens to upstream output — the lens reveals what the output can't see about itself, and the revelation IS the revision. No separate scoring step, no separate fixing step. Seven built-in lenses, plus workspace lenses and custom text. Self-terminating: if the lens finds nothing, the module says so and stops.

```
# Write, then improve through a lens
reflex email+perspective target:"launch email" recipient:"skincare buyers"

# Two lenses, two angles
reflex email+perspective+perspective target:"investor update"

# Score it AND improve based on what the scores reveal
reflex email+audit+perspective target:"launch email"
```

The `refine` module serves a different purpose: it reads structured feedback from `audit`, `evaluate`, or `debrief` and re-executes the deliverable with revision constraints injected. Use `refine` when scored evaluations already exist; use `perspective` when you want iterative improvement.

```
# Write, score, fix (feedback-based)
reflex email+audit+refine target:"launch email"
```

## Lens Concern Convention

Formatter modules (email, report, whitepaper, pitch, linkedin) pre-commit to a weakness before writing. Each module identifies which evaluation lens would most likely find a problem in its upcoming output, and writes this prediction to a `lens_concern` field in its output JSON:

```json
"lens_concern": {
  "lens": "strategic-avoidance",
  "prediction": "I'll describe the competitive dynamics without recommending a specific market entry approach"
}
```

The available lenses are injected at dispatch time from `perspective/LENSES.json` via the `lens_library` source. Adding a new lens to LENSES.json makes it visible to every formatter automatically — no per-module updates needed.

This field exists whether or not a `perspective` step follows. When `perspective` does follow, it reads the upstream `lens_concern` and starts there — confirming the module's self-assessment or finding the real weakness elsewhere. The `concern_confirmed` field in perspective's output closes the feedback loop.

## Evidence Certification

The `certify` module scans every workspace artifact and produces a structured assessment of what's proven, what's inferred, and what's assumed. It classifies each consequential claim as **sourced**, **cross-verified**, **inferred**, **assumption**, **unverified**, or **contradicted** — then writes a pre-formatted appendix that downstream formatters embed directly into the delivered document.

```
reflex websearch+gtm-strategy+certify+report target:"RouteForge"
```

The report ships with a section like: *"This document makes 18 claims. 8 are sourced to specific URLs. 4 are inferences. 3 are assumptions. Here's the table. Here's what we didn't check. Here's the methodology."*

Six formatters are certify-aware: `report`, `whitepaper`, `gtm-strategy`, `launch-plan`, `advertising`, `onboard`. If `certify_*.json` exists in the workspace, they embed the appendix. If it doesn't, they work exactly as before. Zero overhead unless you opt in.

The certification travels with the document. When someone evaluates the deliverable — human or AI — they have the evidence structure to work with, not just prose.

## Document Delivery

Formatter modules don't just produce text — they deliver professional documents. Each formatter writes structured JSON to the workspace (the evidence trail), then delivers the final artifact using Anthropic's native document skills:

| Formatter | Delivery |
|-----------|----------|
| `report`, `whitepaper`, `pitch`, `gtm-strategy`, `launch-plan`, `advertising`, `onboard` | Word document (.docx) |
| `email` | Interactive draft via `message_compose_v1` |
| `recipe` | Interactive widget via `recipe_display_v0` |
| `linkedin`, `recap` | Conversational text (correct format for these outputs) |

The module does the analytical work. Anthropic's tools do the final-mile formatting. Both layers are necessary — the module provides evidence traceability and self-assessment, the document skill provides the shareable artifact.

## Persona System

Personas are a persistent conversational layer over module dispatch. They solve the accessibility problem: a user types `reflex persona copilot` and gets a thinking partner who silently orchestrates modules. No chain syntax, no module names — just conversation.

```
reflex persona copilot
```

**Why personas are not modules:** Modules are bounded (input, output, done) and composable (`+` chains). A persona is persistent (stays active across the entire conversation) and unbounded (no defined output shape). If a persona lived in `modules/`, it would be chainable — `websearch+copilot` would be valid syntax, producing incoherent behavior. The parallel `personas/` directory protects this at the type level.

```
reflex/
├── scripts/
│   ├── dispatch.py       # Module routing (unchanged)
│   ├── persona.py        # Persona routing (parallel)
│   └── sources.py        # Shared injection
├── modules/              # Bounded, composable tools
└── personas/             # Persistent, unbounded wrappers
    └── copilot/
        ├── PERSONA.md    # Identity and behavior
        ├── PARAMS.json   # Inject-only (registry, workspace)
        ├── TRIGGERS.json # Situational pattern matching
        └── STYLE.json    # Voice and tone rules
```

The copilot loads the full module registry, watches for conversational patterns that map to modules, and dispatches through `dispatch.py` when work product is needed. The persona stays active while modules run underneath.

## Module Catalog (78 modules)

### Sources (14)
Gather raw data from the world.

| Module | Params | Description |
|--------|--------|-------------|
| `compare` | target\*, target2\*, focus | Side-by-side web research of two targets |
| `context` | target\*, scope | Gather content from current conversation |
| `decompose` | question\*, depth | Break a question into researchable sub-questions |
| `extract` | target\*, focus | Extract structured data from uploaded files |
| `fetch` | url\*, focus, depth | Fetch a URL and produce structured summary |
| `ideate` | target\*, count, lens | Generate divergent angles via framing lenses. Depends on `decompose` |
| `job-search` | company\*, role\_filter, location | Search for open positions at a company |
| `keywords` | target\*, verticals, intent | Keyword research by vertical and intent tier — CPC estimates, competition levels. Used by `advertising` and `launch-plan` |
| `merge` | targets | Merge multiple research files into one evidence base |
| `research` | topic\*, depth | Research a topic using web search |
| `transcript` | target\*, focus, format | Extract meeting structure from transcripts. Depends on `extract` |
| `trends` | target\*, horizon, focus | Market/macro trend scanner with velocity tagging |
| `voice-dna` | target\*, focus, label | Extract reusable voice profile from writing samples. Depends on `extract` |
| `websearch` | target\*, focus | Web search with structured JSON output |

### Analyzers (25)
Interpret and evaluate evidence.

| Module | Params | Description |
|--------|--------|-------------|
| `adaptive-review` | language\*, code\_context | Auto-routes to quick, deep, or security review |
| `advertising` | target\*, platforms, budget, goal | Platform-specific paid ad campaign plan — selection, targeting, keywords, budget allocation. Depends on `audience-portrait` + `keywords` |
| `audit` | target\*, criteria, standard | Quality-gate scoring with pass/fail verdict. Depends on `debrief` |
| `audience-portrait` | target\*, focus, findings | Psychographic portrait — language, barriers, triggers |
| `code-review` | language\*, style | Review code for bugs, security, quality |
| `competitive-messaging` | target\*, focus, findings | Map messaging lanes, language patterns, white space |
| `competitors` | target\*, vs, focus | Deep competitive intelligence dossier |
| `creative-brief` | target\*, audience, findings | Full creative strategy — positioning, pillars, taglines |
| `evaluate` | target\*, target2, domain\* | Score targets against a rubric |
| `experiment` | target\*, scope, constraints | Design testable hypotheses with success criteria. Depends on `scenario` |
| `forecast` | target\*, horizon, assumptions | Structured projection with sourced-vs-estimated flagging. Depends on `trends` |
| `grade` | domain\*, candidates\* | Score multiple candidates, produce ranked scorecard |
| `gtm-strategy` | target\*, market, constraints | Evidence-backed go-to-market strategy — beachhead scoring, phased expansion, pricing, founding customer program, confidence assessment. Depends on `websearch` + `competitors` + `positioning` + `audience-portrait` |
| `landscape` | domain\*, dimensions, players, format | Map competitors across strategic dimensions |
| `match` | candidate\*, opportunities\*, lens | Ranked fit matrix with strengths and gaps |
| `moat` | target\*, format | Defensibility analysis — network effects, switching costs |
| `opportunities` | target\*, lens | Find gaps and white space |
| `persona` | target\*, role\*, tone | Simulate a stakeholder's reaction |
| `positioning` | target\*, audience | ICP definition, differentiation matrix |
| `review` | target, type, style | Generalized content review |
| `risks` | target\*, severity | Risk identification and mitigation |
| `scenario` | target\*, horizon, count | Project 2-4 future scenarios with probabilities |
| `stakeholders` | target\*, scope | Map key people and organizations |
| `swot` | target\*, format, depth, industry | SWOT analysis — routes to quick or deep variant |
| `unit-economics` | target\*, model\_type | Unit economics breakdown (CAC, LTV, margins) |

### Transformers (13)
Reshape, filter, certify, translate, or stress-test existing analysis.

| Module | Params | Description |
|--------|--------|-------------|
| `actions` | target\*, timeframe | Extract actionable next steps |
| `certify` | target\*, scope | Evidence certification — maps claims to sources, classifies confidence, identifies gaps. Produces embeddable appendix for downstream formatters |
| `challenge` | target\*, intensity | Steelman the opposite position |
| `debrief` | target\*, scope | Audit information fidelity across a chain |
| `distill` | target\*, lens | Distill findings into weighted categories |
| `filter` | target\*, criteria\*, threshold | Prune findings to relevant subset |
| `reframe` | target\*, audience\*, purpose | Reframe analysis for a different audience |
| `perspective` | target\*, lens | Apply an evaluation lens — reveals what the output can't see about itself, then produces the revision. 8 built-in lenses + workspace + custom |
| `refine` | target\*, scope | Close the evaluator-optimizer loop — re-execute a deliverable with audit/evaluate feedback injected |
| `rubric` | domain\*, depth | Generate a weighted evaluation rubric |
| `simplify` | target\*, audience | Explain analysis in plain language |
| `tagline` | target\*, audience, tone, count, findings | Generate taglines with strategic rationale |
| `translate` | target\*, language | Translate workspace content or deliverables across languages |

### Formatters (9)
Deliver analysis as professional documents and artifacts.

| Module | Params | Description |
|--------|--------|-------------|
| `email` | target\*, recipient, tone, variants, findings | Send-ready email via `message_compose_v1` |
| `launch-plan` | target\*, horizon, budget | Operational execution playbook — channels, keywords, outreach scripts, week-by-week timeline, budget breakdown. Delivered as .docx. Depends on `gtm-strategy` + `keywords` |
| `linkedin` | target\*, tone, length, hook | LinkedIn-native post or article |
| `onboard` | target\*, audience, depth | Handoff document delivered as .docx. Depends on `recap` |
| `pitch` | target\*, audience, ask | Situation-Complication-Resolution narrative delivered as .docx |
| `recap` | target, length | Executive summary of workspace artifacts |
| `recipe` | dish\*, style, servings | Interactive recipe via `recipe_display_v0` |
| `report` | topic\*, format | Structured report or memo delivered as .docx |
| `whitepaper` | domain\*, depth | Long-form whitepaper preserving full evidence chain, delivered as .docx |

### Utility (6)
Helpers, fallbacks, and fun.

| Module | Description |
|--------|-------------|
| `coin-flip` | Time-based coin flip with variant routing (Level 3 demo) |
| `do` | General-purpose fallback — fulfills any intent directly |
| `foxtrot` | Identity confirmation (Level 0 demo) |
| `pirate` | Pirate captain greeting (Level 0 demo) |
| `restore` | Unpack a snapshot to resume a previous session |
| `snapshot` | Package workspace into a downloadable snapshot |

### Meta (11)
Modules that operate on the system itself.

| Module | Description |
|--------|-------------|
| `design-module` | Interactive module creator/upgrader |
| `diagnose` | Analyze a chain that produced weak results |
| `full-analysis` | One-command: research + rubric + evaluate + whitepaper. Depends on `websearch+distill+rubric+evaluate` |
| `help` | Explain modules, params, and composition grammar |
| `partnership` | Working relationship profile — captures thinking style, quality signals, collaboration preferences |
| `plan` | Propose a module chain from natural language |
| `retro` | Session retrospective — surprises, lessons, carry-forward items. Depends on `debrief` |
| `run` | Step-by-step pipeline execution with pause/resume/skip/reset |
| `status` | Show workspace artifacts from current session |
| `test-dispatch` | Smoke test dispatch routing |
| `test-perspective` | Calibrate perspective lenses — produces deliverables with planted flaws, tests whether each lens catches them |

\* = required parameter

## Adding a Module

**Level 0** — Create `modules/{name}/MODULE.md`. That's it.

**Level 1** — Add `PARAMS.json`:
```json
{
  "group": "analyzer",
  "description": "One-line description for the registry",
  "params": {
    "target": { "required": true, "description": "What to analyze" },
    "depth": { "required": false, "default": "overview", "description": "How deep to go" }
  }
}
```

**Level 2** — Add `DEPENDS.json`:
```json
{
  "before": [
    {
      "module": "research",
      "forward_params": { "topic": "{target}" },
      "output_key": "findings"
    }
  ]
}
```

**Level 3** — Add `RESOLVE.py` + `variants/{name}/MODULE.md`:
```python
#!/usr/bin/env python3
import sys, json
params = json.loads(sys.argv[1])
if params.get("depth") in ["deep", "full"]:
    print("deep|Depth param requested full analysis")
else:
    print("quick|Default to quick analysis")
```

## Adding a Context Source

Add a function to `sources.py` and register it:

```python
def my_source():
    # Gather and return context as a string
    return "formatted context here"

SOURCES = {
    "module_registry": module_registry,
    "workspace_state": workspace_state,
    "my_source": my_source,          # New source
}
```

Any module can now declare `"inject": "my_source"` in its PARAMS.json. No changes to dispatch.py needed.

## Running Locally

Test the router directly:

```bash
python3 reflex/scripts/dispatch.py - <<'DISPATCH_INPUT'
reflex help list
DISPATCH_INPUT
```

Run the dispatch test suite:

```bash
python3 reflex/scripts/dispatch.py - <<'DISPATCH_INPUT'
reflex test-dispatch
DISPATCH_INPUT
```

## Installing as a Claude Skill

The `reflex/` directory is the skill package. `SKILL.md` must be at the root of that folder.

- **Claude.ai**: Upload via the Skills interface. The `reflex/` folder (or a zip of its contents) is the package.
- **Claude Code**: The skill triggers on any message containing the word "reflex" — no slash command registration needed.
- **API**: Attach as an agent skill per the [Anthropic skills documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview).

### Known Issue: Stale Skill Installations

When Reflex is installed as a skill, the runtime copies the skill files to an internal installation path. **Adding new modules to the repo does not automatically update the installed copy.** This means:

- Modules added directly to `reflex/modules/` in the repo will exist on disk but won't be visible to `dispatch.py` at the installed skill path
- The installed skill's `dispatch.py` scans its own `modules/` directory, not the repo's
- Symptoms: `ERROR: No module found for 'X'` even though `ls reflex/modules/` shows the module exists

**Workarounds:**
- **Claude.ai**: Re-upload the skill (re-zip and replace)
- **Claude Code**: The skill installation path is separate from the repo. After adding modules to the repo, you may need to re-trigger the skill installation or manually sync the files
- **Local testing**: Run dispatch directly from the repo path to bypass the installation:
  ```bash
  python3 reflex/scripts/dispatch.py - <<'DISPATCH_INPUT'
  reflex your-new-module target:X
  DISPATCH_INPUT
  ```

This is a known friction point. The filesystem-as-API convention means the skill is always a snapshot of the repo at install time, not a live view of it.

## Evaluation Results

**Chain quality testing** (Opus 4.6, same prompt, scored against a 7-dimension rubric): a 6-module chain produced by `plan` scored **98.7% (148 weighted)**, outperforming both a manually-composed 4-module chain (Report A) and a hand-built 7-module chain (Report B, 94.7%). The specialized analytical modules (`competitive-messaging`, `audience-portrait`, `creative-brief`) produced the gains.

**Lens calibration** (9 scenarios, `test-perspective` module): All 8 built-in lenses correctly identified their target planted flaws (8/8 HIT). Misdirection resistance: 1/1 INDEPENDENT — perspective found the actual gap despite a deliberately wrong `lens_concern`. Multi-pass rotation: ROTATE confirmed — the LLM naturally selects different lenses across `+perspective+perspective` chains without a resolver.

**GTM strategy review** (external evaluator): A `launch-plan` deliverable produced from a `gtm-strategy` chain was assessed at the 75-90th percentile of GTM documents. Gaps identified (customer voice, unit economics, attribution) led to adding `audience-portrait` as a `gtm-strategy` dependency and creating the `certify` module.

**Evidence fidelity** (`debrief` module on live chains): 94-100% of sourced findings survive from research to final deliverable. The primary fidelity risk isn't evidence loss — it's evidence invention during formatting. The `unsupported-confidence` lens and `certify` module address this directly.

## Design Philosophy

Reflex is built on a few convictions about how LLM skill systems should work:

**Convention over configuration.** dispatch.py has never been modified to support a new module. Adding capability means adding a folder. If a change requires touching the engine, the design is wrong. This isn't a principle borrowed from Rails — it's a constraint that keeps the system honest. The filesystem is the API.

**Slow is steady, steady is fast.** The module path takes more steps than asking Claude directly. That's the point. Each step writes structured evidence to disk. By the time the deliverable is produced, every claim traces to a source, every inference is flagged, and the work is auditable. The fast path skips those steps and produces work you can't trust. Reflex chooses rigor.

**Epistemic honesty as architecture.** The `certify` module, the `lens_concern` convention, the `unsupported-confidence` lens, the confidence assessment in `gtm-strategy` — these aren't features. They're the system's immune system against its own tendency to sound confident about things it made up. An LLM that knows what it doesn't know is more useful than one that sounds certain about everything.

**Composition over comprehension.** No single module tries to do everything. A GTM strategy chains through websearch, competitors, positioning, audience-portrait, and then adds the strategic lens. Each step is independently testable, replaceable, and improvable. When `audience-portrait` gets better, every module that depends on it gets better automatically. The system's intelligence is in the connections, not the components.

**The user chose this.** When someone loads the copilot persona, they opted into a methodical system. The architecture respects that choice — modules use Anthropic's native tools internally (document delivery, web search, interactive email) but the analytical pipeline is what creates the value. The tools are instruments. The modules are the music.

## Author

Built by Walter Reid. The modules reflect one person's analytical patterns — business strategy, competitive intelligence, positioning, content creation — but the architecture is general-purpose. Convention is the interface. Adding your own patterns means adding your own folders.

## License

MIT License. See [LICENSE](LICENSE).

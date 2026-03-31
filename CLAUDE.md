# CLAUDE.md — Reflex

## What This Project Is

Reflex is a convention-based meta-skill dispatcher for Claude. It turns natural language into structured analytical pipelines by routing through composable modules, each defined entirely by its filesystem presence. There is no registry, no configuration file, no hardcoded module list. The filesystem *is* the API.

The system gives a non-technical user the analytical depth of a multi-step research process — competitive intelligence, audience profiling, trend analysis, strategic synthesis, formatted deliverables — through a single natural language request. It gives a power user the ability to compose, swap, and extend individual steps without touching the engine.

Reflex runs inside Claude's skill system. It is invoked by the word "reflex" appearing anywhere in a user's message. The skill's SKILL.md frontmatter is the only thing that loads at startup (~50 tokens). Everything else loads on demand.

**Who it's for:** You. One user. The modules reflect your analytical patterns — business strategy, competitive analysis, positioning, content creation. The system is general-purpose by architecture but personal by content.

## Golden Rules

1. **Convention is the interface.** dispatch.py never changes. Adding capability means adding a folder. If a change requires modifying dispatch.py, the design is wrong.

2. **Context cost is proportional to use, not to size.** A system with 1,000 modules has identical overhead to a system with 3 modules. Only the invoked module's MODULE.md enters Claude's context. Unmatched modules cost zero tokens.

3. **The `+` operator is user-controlled composition. DEPENDS.json is module-controlled composition.** These are different tools for different problems. `+` means "I want these steps in this order." DEPENDS.json means "this module literally cannot function without this upstream step." Conflating them produces either inflexible modules or chains the user can't override.

4. **Modules write JSON to `/home/claude/`. Downstream modules read JSON from `/home/claude/`.** This is the data bus. The naming convention `{type}_{target}.json` is what makes modules composable without knowing about each other. Break this convention and the chain breaks.

5. **Sources inject; modules don't reach.** When a module needs system state (the registry, the workspace contents), it declares `"inject": "source_name"` in PARAMS.json. It never imports sources.py or scans the filesystem itself. This keeps dispatch as the single point of control.

6. **`run` is the human interface. `plan` is the routing intelligence. Chains are the execution primitive.** A user should be able to say `reflex run "do the thing"` and get a result. Whether that's 3 modules or 9 is an implementation detail the user opts into seeing, not one they're forced to manage.

## Domain Knowledge

### The Four-Level Module System

- **Level 0** — MODULE.md only. Behavioral overlay. No inputs, no routing. Example: `pirate`, `foxtrot`.
- **Level 1** — MODULE.md + PARAMS.json. Takes user input, produces structured output. The workhorse. Most modules are Level 1.
- **Level 2** — MODULE.md + PARAMS.json + DEPENDS.json. Has inherent dependencies that run automatically before the module executes. Example: `full-analysis` depends on `websearch → distill → rubric → evaluate` before it can write its whitepaper.
- **Level 3** — MODULE.md + PARAMS.json + RESOLVE.py + variants/. Adapts at runtime. The resolver is a Python script that receives params and prints a variant name. Dispatch loads the corresponding variant's MODULE.md. Examples: `plan` (passthrough resolver — the LLM evaluates intent against the registry and decides whether to compose a chain or design a new module), `swot` (routes between `quick` and `deep`), `adaptive-review` (routes based on security signals in code context).

Levels compose: a module can have both DEPENDS.json and RESOLVE.py (Level 2+3). Dependencies run first, then the resolver selects a variant.

### The Six Module Groups

- **source** — Gathers raw data. `websearch`, `research`, `trends`, `context`, `extract`, `fetch`, `compare`, `merge`, `decompose`, `job-search`, `voice-dna`, `transcript`, `ideate`.
- **analyzer** — Interprets data through a framework. `evaluate`, `swot`, `positioning`, `competitors`, `landscape`, `competitive-messaging`, `audience-portrait`, `creative-brief`, `audit`, `experiment`, `forecast`, `grade`, `match`, `moat`, `opportunities`, `persona`, `risks`, `scenario`, `stakeholders`, `unit-economics`, `code-review`, `adaptive-review`, `review`.
- **transformer** — Reshapes without adding evidence. `distill`, `challenge`, `reframe`, `filter`, `rubric`, `tagline`, `debrief`, `actions`, `simplify`.
- **formatter** — Delivers for a human audience. `email-draft`, `write-report`, `whitepaper`, `pitch`, `linkedin`, `recap`, `recipe`, `onboard`.
- **utility** — Standalone tools. `do`, `snapshot`, `restore`, `coin-flip`, `foxtrot`, `pirate`.
- **meta** — System management. `help`, `plan`, `run`, `status`, `design-module`, `diagnose`, `full-analysis`, `test-dispatch`, `retro`, `partnership`.

### The Dispatch Pipeline

```
User message
  → dispatch.py parses trigger word + module name + params
  → If module name contains "+": build_inline_chain() 
       → Collect all params from all modules (first occurrence wins)
       → Build CHAIN protocol, ignoring individual DEPENDS.json
  → If single module:
       → Level 0: LOAD_MODULE
       → Level 1: extract params → inject sources → validate → LOAD_MODULE_WITH_PARAMS
       → Level 2: build_chain() resolves dependencies recursively → CHAIN
       → Level 3: run RESOLVE.py → load variant → RESOLVED (or CHAIN if deps exist)
  → Claude reads the protocol output and follows it
```

### Key Architectural Decisions (Settled)

- **Params are extracted via shlex + regex**, supporting both positional (`reflex swot anthropic`) and named (`target:anthropic depth:deep`) syntax. Quoted values work via shlex. Greedy params absorb remaining positional words.
- **Inline chains (`+`) override DEPENDS.json.** When the user specifies a chain, each module's own dependencies are ignored. The user's composition is authoritative.
- **The `plan` resolver is a passthrough** — it always routes to the `route` variant. The LLM evaluates the intent against the injected module registry and decides whether to compose a chain from existing modules or design a new one. The `suggest` variant was removed; both paths are handled within a single unified MODULE.md. This replaced an earlier TF-IDF cosine similarity approach because the LLM's judgment proved more reliable than programmatic matching.
- **`plan` writes `run_plan.json` directly** in the format `run/start` expects (steps array with status fields, `total_steps`, `current_step`). There is no intermediate `plan_output.json` translation step. This tight coupling eliminates a fragile conversation-context parsing step that previously existed in `run/start`.
- **`run` depends on `plan`** via DEPENDS.json with an `unless_exists` guard on `run_plan.json`. If a plan already exists, `run` skips planning and continues execution. This enables `reflex run` to mean both "start" and "continue."
- **Workspace persistence is session-scoped.** Files in `/home/claude/` reset between conversations. The `snapshot` module packages workspace state into a downloadable JSON. The `restore` module unpacks it in a new session. This is the cross-session persistence mechanism.

### The Specialization Pattern

Level 2 modules serve a second purpose beyond multi-step pipelines: **specialization**. A module can depend on a general-purpose module via DEPENDS.json and add only a domain-specific output structure on top.

The dependency does the heavy lifting. The specialized module adds the lens.

```
extract  ──►  transcript   (adds meeting-specific structure: decisions, actions, ownership)
extract  ──►  voice-dna    (adds reusable voice profile format)
debrief  ──►  audit        (adds quality-gate scoring with pass/fail verdict)
debrief  ──►  retro        (adds session reflection: surprises, carry-forward items)
decompose ──► ideate       (adds divergent framing lenses)
scenario ──►  experiment   (adds hypothesis design with success criteria)
recap    ──►  onboard      (adds handoff document structure)
trends   ──►  forecast     (adds structured projection with sourced-vs-estimated flagging)
```

This is distinct from duplication (Golden Rule 6 in DESIGN.md). A specialized module never reimplements its dependency's work — it delegates via DEPENDS.json and only adds the domain-specific framing. If the dependency improves, every specialization improves automatically.

### Important Vocabulary

- **Chain** — An ordered sequence of module executions. Can be user-composed (`+`) or dependency-resolved (DEPENDS.json).
- **Injection** — A param filled at dispatch time by sources.py, not by the user. Currently two sources: `module_registry` and `workspace_state`.
- **Variant** — One of several MODULE.md files inside a Level 3 module's `variants/` directory. Selected by RESOLVE.py at runtime.
- **Findings** — The conventional param name for upstream chain context. Modules that consume upstream data include `{findings}` in their MODULE.md template.
- **Workspace** — `/home/claude/`. Where modules write and read JSON artifacts. Scanned by the `workspace_state` source.

## What Done Means

This project is never done. It's a living system that grows by adding folders. But a *session* is done when:

- The user's intent has been answered
- Workspace artifacts exist for every step that was executed
- The chain of evidence is traceable from source → analysis → output
- A `snapshot` has been taken if the work should persist

## Architecture Concerns for Future Development

[See BUILD.md — these are active, not theoretical]

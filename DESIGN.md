# DESIGN.md — Reflex

## Philosophy

Reflex is infrastructure that disappears. Its design goal is not "look at this powerful system" — it's "I said what I wanted and got something good." The system succeeds when the user forgets they're using a framework and thinks they're just talking to someone thorough.

This creates a specific design tension: the system must be powerful enough to justify its existence over "just asking Claude," but invisible enough that using it doesn't feel like operating machinery. Every design decision lives in this tension.

The system's aesthetic is **competence without ceremony.** It should feel like handing a task to someone who's done it before — they don't explain their methodology, they just come back with the work. When the system does surface its own structure (help, plan, status), it should feel like a colleague explaining their process, not a product showing its settings page.

## Voice & Tone

Reflex doesn't have a voice — Claude does. The modules should not impose a personality. But they do impose a *standard*:

- **Output should sound like the best version of Claude's natural voice for that task.** An email should sound like Claude writing an email. A competitive analysis should sound like Claude doing strategy work. Modules shape the structure and rigor, not the personality.
- **Module instructions should be written for Claude, not for a user.** They're prompts, not documentation. The language should be direct, specific, and opinionated. "Write a hook that stops a cold reader" not "consider crafting an engaging opening."
- **Error messages should be useful, not apologetic.** `MISSING_PARAMS:evaluate|required:[target, domain]|provided:[target]|missing:[domain]` is good. "I'm sorry, I wasn't able to process that" is not. The user is a power user even if they don't know it yet.

## Interaction Patterns

### The Two Entry Points

**Power user:** Types `reflex competitive-messaging+audience-portrait+creative-brief target:"DTC skincare" audience:"millennial men"`. Knows the modules, knows the params, knows the chain. Sees the machinery and likes it.

**Normal user:** Types `reflex run "help me figure out my brand positioning and write a launch email"`. Doesn't know modules exist. Gets the same result. Sees only the output.

Both are first-class citizens. The system should never force a normal user to become a power user, and should never slow down a power user with training wheels.

### The Pause Pattern

`run` pauses after each step. This is a design choice, not a technical limitation. The pause serves three purposes:

1. **Legibility** — The user sees what's happening and can verify it makes sense
2. **Steering** — The user can adjust params, skip steps, or redirect mid-chain
3. **Context management** — Long chains risk context window pressure; pauses let Claude consolidate before continuing

The cost is friction. A 7-step chain requires 7 confirmations. Whether to add a "just go" mode is an open design question (BUILD.md, Phase 1, Task 1.5). The trade-off: a "just go" mode risks producing a final output the user doesn't trust because they didn't see it being built. Trust through transparency vs. speed through opacity.

### The Help System

`help` is the system's discoverability layer. It currently supports:
- `help overview` — what the system is
- `help list` — full module catalog
- `help {module}` — specific module with params and examples
- `help {concept}` — explains chains, params, groups

What it doesn't do yet (and probably should): contextual suggestion. After running a module, `help` could say "you just produced a competitive messaging analysis. Modules that typically follow: creative-brief, positioning, tagline." This turns help from a reference tool into a guide.

### The Self-Improvement Pattern

The system improves its own output the same way the user improves the system's output — through evaluation lenses that reveal what the work can't see about itself. The revelation IS the revision. There is no separate scoring step and no separate fixing step. Seeing the gap and knowing how to close it are the same act.

This emerged from a design observation: score-based evaluation (rate this 1-5, then translate scores into fixes) is a lossy round-trip. The insight → score → score → instruction → revision pipeline loses information at every translation. Lens-based evaluation skips the translation entirely: the lens reveals, the module produces what the original would have produced if it had seen what the lens sees.

The **pre-commitment pattern** extends this further. Formatters name their expected weakness *before writing*, using the lens library. This is prediction about the task, not judgment about the output — a different cognitive operation. Making the weakness conscious before execution partially corrects it. When `perspective` follows, it reads the upstream prediction and starts there — confirming or finding the real gap.

The principle: **self-awareness as an input to the work, not a review of it.**

## Information Architecture

### Workspace as State

The workspace (`/home/claude/*.json`) is the system's memory within a session. It's also the system's communication bus — modules don't talk to each other, they talk to the filesystem. This is elegant but has implications:

- **Naming matters.** `competitive_messaging_dtc-skincare.json` is findable. `output_3.json` is not. The convention `{type}_{target_slug}.json` is load-bearing.
- **The workspace is flat.** No directories. This works at 10-20 files. At 50+, scanning becomes noisy. The `workspace_state` source mitigates this by providing summaries, but the underlying filesystem will get crowded in long analytical sessions.
- **Snapshots are the persistence layer.** Everything in `/home/claude/` is ephemeral. The `snapshot` → `restore` cycle is the only way to carry work across conversations. This is deliberate — it prevents stale state — but it means the user must actively choose to persist.

### Module as Document

Each MODULE.md is simultaneously:
1. **A prompt** — it tells Claude what to do
2. **A specification** — it defines inputs, outputs, and quality criteria
3. **Documentation** — it explains the module to `help` and `design-module`

This triple duty means MODULE.md files need to be written with care. An instruction that's good for Claude ("write with voice") might be bad for documentation ("what does this module do?"). The current convention — title, param list, numbered instructions, output section — balances these reasonably well. Resist the temptation to optimize for one role at the expense of the others.

## What to Never Do

1. **Never add routing logic to dispatch.py for a specific module.** If a module needs special routing, that's what RESOLVE.py is for. The moment dispatch.py contains an `if module_name == "special-case"`, the convention is broken.

2. **Never write a module that imports from another module's directory.** Modules are isolated by convention. They communicate through the workspace filesystem, not through code dependencies. If module A needs module B's output, it reads the JSON file B wrote — it doesn't import B's functions.

3. **Never put user-facing copy in dispatch.py or sources.py.** These are infrastructure. The only user-facing text they should produce is protocol strings (LOAD_MODULE, CHAIN, ERROR). All human-readable output comes from MODULE.md files, interpreted by Claude.

4. **Never create a module that only works in a chain.** Every module should produce a useful result when run standalone, even if that result is less rich than when chained. `creative-brief` without upstream research should still produce a creative brief from Claude's knowledge — just with a note that it wasn't grounded in research. This is what makes the system composable rather than brittle.

5. **Never let analytical rigor crowd out creative execution in a formatter module.** The debrief audit showed that email copy gets over-determined when the module instructions emphasize evidence-threading over voice. Formatters should reference upstream evidence but their primary instruction should be about the *quality of the output as a human deliverable*, not about its fidelity to the analytical chain. The analysis is the means; the deliverable is the end.

6. **Never add a module that duplicates an existing module's core function under a different name.** Before creating a new module, check whether an existing module with different params or a Level 3 variant would serve the same purpose. The system's power comes from composability, not from having a module for every noun. If two modules would produce substantially similar output for substantially similar inputs, one of them shouldn't exist.

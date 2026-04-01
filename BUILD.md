# BUILD.md — Reflex

## Current State

The system is built and functional. 72 modules across 6 groups, 3 context sources, 8 evaluation lenses. The dispatch engine, source injection, chain composition, Level 0-3 routing, dependency resolution, workspace persistence, and the perspective/lens concern self-improvement architecture all work. This document is not a build plan — it's a diagnostic of where the system's design assumptions are under pressure and what to do about it.

## Phase 0 — Foundation [COMPLETE]

| Task | Description | Status |
|------|-------------|--------|
| 0.1 | dispatch.py — param extraction, chain building, resolver execution | [x] |
| 0.2 | sources.py — module_registry, workspace_state, and lens_library injection | [x] |
| 0.3 | SKILL.md — frontmatter trigger, architecture docs, protocol spec | [x] |
| 0.4 | Level 0-3 module support with variant routing | [x] |
| 0.5 | Inline chain composition with `+` operator | [x] |
| 0.6 | DEPENDS.json with conditional `unless_exists` | [x] |
| 0.7 | `help`, `plan`, `run`, `status`, `design-module` meta modules | [x] |
| 0.8 | `snapshot` / `restore` for cross-session persistence | [x] |

## Phase 1 — The Composition Quality Problem [ACTIVE]

This is the central tension the system currently faces. It was surfaced during a comparative evaluation session where two reports answering the same question were scored against a rubric. The findings:

**More modules produce better results.** A 6-module chain (trends → competitive-messaging → audience-portrait → creative-brief → tagline → email-draft) scored 148/150 against a rubric where a 4-module chain scored 121/150 and a manually-composed response scored 142/150. Each specialized module contributed a specific analytical layer that improved the final output.

**But more modules increase the composition burden.** A 7-module chain is not something a casual user will type. The system's power scales with module count; its approachability does not.

**`run` solves this — in theory.** The user says `reflex run "do the thing"`, `plan` composes the chain, `run` executes step by step. The user never sees the module names. But:

| Task | Description | Status |
|------|-------------|--------|
| 1.1 | Validate that `plan` routes correctly with the expanded module set | [x] Tested with 6-module skincare chain and skills research intent; routes correctly |
| 1.2 | Audit `plan`'s routing bias — does it favor thoroughness over efficiency? | [~] Resolver replaced with LLM passthrough. New `plan` MODULE.md explicitly instructs "don't include modules the intent didn't ask for." Needs broader validation across diverse intents. |
| 1.3 | Determine whether `plan` should have a complexity budget (shortest chain that covers ≥80% of intent) | [~] Partially addressed: `plan` MODULE.md now recommends `run` for 5+ module chains and direct invocation for single modules. Budget is implicit in the routing guidance, not enforced programmatically. |
| 1.4 | Test `run` end-to-end with a 6+ module chain — does context degrade by step 5? | [ ] |
| 1.5 | Determine whether `run` should support "just go" mode (no pause between steps) vs current pause-per-step | [ ] |

**Acceptance criteria for 1.1:** Run `reflex plan` with 5 different natural-language intents of varying complexity. Verify that the suggested chains are (a) executable, (b) use the most specific module available, and (c) don't include redundant modules.

**Acceptance criteria for 1.2:** The `plan` resolver is now a passthrough (always routes to `route` variant). TF-IDF matching was replaced with LLM evaluation of the full registry. The new `plan` MODULE.md includes anti-expansion instructions and execution format guidance (direct/chain/run). Remaining validation: run 5+ diverse intents and verify the LLM doesn't over-compose.

**Acceptance criteria for 1.3:** [DECISION NEEDED] Is the right fix in the resolver (score chains by efficiency, not just coverage) or in a new meta-module that wraps plan with an optimization pass? Or is this not actually a problem because `run` hides the complexity?

**Acceptance criteria for 1.4:** Run a 7-module chain via `reflex run` in a fresh conversation. At step 6, verify that the module can still read and reference specific findings from step 1's output file. If it can't, context window pressure is compressing upstream evidence.

**Acceptance criteria for 1.5:** [DECISION NEEDED] The current pause-per-step design gives the user control but adds friction. A "just go" mode would execute the full chain and present the final output. Trade-off: control vs. speed. Possible design: `reflex run` pauses by default; `reflex run all` executes without pausing.

## Phase 2 — The Creative Execution Gap [ACTIVE]

The evaluation revealed a consistent pattern: analytical modules produce excellent structured output, but the final creative step (email, copy, tagline) can feel over-determined. The upstream analysis is so precise that the formatter knows exactly what to say — and that precision costs looseness.

| Task | Description | Status |
|------|-------------|--------|
| 2.1 | Audit `email-draft` MODULE.md — does it instruct Claude to shift voice, or does it just say "compress"? | [~] |
| 2.2 | Test whether adding an explicit voice-shift instruction ("forget you're an analyst, you're the brand now") measurably changes email warmth | [ ] |
| 2.3 | Determine whether the formatter group needs a "mode" param: `analytical` vs `creative` | [ ] |
| 2.4 | Test whether the same chain produces warmer output in claude.ai chat vs Claude Code | [ ] |

**Acceptance criteria for 2.1:** Read the current email-draft MODULE.md. Identify every instruction that references upstream data. Count the ratio of "reference the research" instructions to "write with voice" instructions. If the ratio is >2:1, the module is analytically biased.

**Acceptance criteria for 2.2:** Run the same chain twice with the same inputs — once with current email-draft, once with a modified version that includes a voice-shift instruction. Have a human compare the two emails blind. If neither is consistently preferred, the instruction doesn't help.

**Acceptance criteria for 2.3:** [DECISION NEEDED] A `mode:creative` param could tell the formatter to prioritize voice over evidence density. But this might be better solved by writing better MODULE.md instructions than by adding a param. Params should control what varies; if the answer is "always write with more voice," that's an instruction fix, not a param.

**Acceptance criteria for 2.4:** [ASSUMED: chat produces warmer output due to conversational context bleed] Test by running an identical chain in both environments and comparing. If confirmed, this has architectural implications — it means the optimal pipeline is analysis in Code, creative in chat.

## Phase 3 — Evidence Fidelity at Scale [PLANNED]

The `debrief` module revealed that evidence degrades across long chains. Specific findings:

- Tagline justifications in the evaluation slightly overstated the directness of research-to-tagline connections
- The "tied to research" claim in one evaluation traced to a different source than the justification implied

| Task | Description | Status |
|------|-------------|--------|
| 3.1 | Add a `source_ref` field to module output JSON — explicit back-reference to which upstream file a finding came from | [ ] |
| 3.2 | Update `evaluate` to require justifications to name the specific upstream finding by file and index | [ ] |
| 3.3 | Determine whether `debrief` should run automatically as a final step in chains above N modules | [ ] |
| 3.4 | Consider whether the workspace_state source should include a brief evidence summary, not just filenames | [ ] |

## Phase 4 — Self-Improvement Architecture [COMPLETE]

The self-improvement problem was solved not by making the loop infrastructure smarter, but by making evaluation and revision the same act. The `perspective` module applies a lens that reveals what output can't see about itself — and the revelation IS the revision. No separate scoring/fixing cycle. No `LOOP:` protocol needed.

| Task | Description | Status |
|------|-------------|--------|
| 4.1 | `refine` module built — reads audit/evaluate/debrief feedback, re-executes with revision constraints | [x] |
| 4.2 | `perspective` module built — lens-based evaluation where diagnosis and correction are the same act | [x] |
| 4.3 | 7 built-in lenses defined in LENSES.json, drawn from manual evaluation prompts | [x] |
| 4.4 | Lens concern convention added to all 5 formatters — pre-commit to weakness before writing | [x] |
| 4.5 | `lens_library` source in sources.py — canonical lens definitions injected at dispatch time | [x] |
| 4.6 | `test-perspective` calibration module — 9 scenarios with planted flaws, misdirection resistance test, invention detection, multi-pass rotation | [x] Scored 7/7 HIT, 1/1 INDEPENDENT on misdirection (original 7). Scenario 8: HIT on unsupported-confidence. Scenario 9: ROTATE confirmed. |
| 4.7 | `plan` updated to suggest `+perspective` for high-stakes formatter chains | [x] |
| 4.8 | Upgrade `perspective` to Level 3 with time-based resolver that rotates lenses per pass | [x] Resolved by design — no resolver needed. See notes below. |
| 4.9 | Test multi-pass convergence: does `email-draft+perspective+perspective` produce measurably better output than single-pass? | [~] Partially validated: pass 2 > pass 1. Pass 2 found a hidden-assumptions problem introduced by pass 1's fix (condescension to beta users). Debrief also found invention-detection gap — neither lens catches fabricated claims. New `unsupported-confidence` lens (lens #8) added to address this. |
| 4.10 | Validate `unsupported-confidence` lens and multi-pass rotation | [x] Scenario 8: HIT — caught all 3 planted fabrications (40% stat, manufactured quote, false operational specificity), correctly distinguished from defensible feature claims. Scenario 9: ROTATE — Pass 1 selected hidden-assumptions, Pass 2 selected strategic-avoidance. LLM naturally rotates without a resolver. |

**The key insight:** The `plan` lesson (don't make Python replicate Claude's judgment) applies to self-correction too. Score-based evaluation (audit) produces numbers that need translation back into revision instructions — a lossy round-trip. Lens-based evaluation (perspective) skips the translation. The lens reveals, the revelation implies the fix, the module produces the revised output. One step.

**The coin-flip connection:** `perspective` becomes Level 3 when you want multi-pass improvement. A time-based resolver (same mechanism as coin-flip) rotates which lens gets applied per pass. Each iteration examines a different blind spot. The escape hatch terminates the loop: "the lens found nothing new."

**4.8 resolution (2026-04-01):**

Resolved by design — no Level 3 upgrade needed. In live testing of `email-draft+perspective+perspective`, the LLM naturally selected different lenses across passes (strategic-avoidance on pass 1, hidden-assumptions on pass 2) without any resolver. The MODULE.md auto-selection logic in Step 3 plus upstream chain context (which includes `lens_applied` from the first pass's `perspective_*.json`) gives the LLM everything it needs to not repeat.

A resolver would have been redundant — and couldn't have worked anyway. `build_inline_chain()` doesn't run resolvers (it loads the root MODULE.md, not variants), so a Level 3 upgrade would have been invisible in the `+` chain path, which is the primary multi-pass pattern. The right answer was always Option 3: trust the LLM's judgment, same bet `plan` makes. Validated by test scenario 9 (multi-pass rotation test).

**What `refine` is for:** Cases where structured feedback (scores, verdicts) already exists and needs to be actioned. `audit+refine` translates scored deficiencies into fixes. `perspective` is preferred for iterative improvement; `refine` is for consuming existing evaluations.

## Phase 5 — Structured Data as First-Class Input [PLANNED]

Every analytical module currently runs on web search + Claude's knowledge. Structured data (CSVs, spreadsheets, databases) would make `unit-economics`, `trends`, `forecast`, and `evaluate` quantitative instead of qualitative.

| Task | Description | Status |
|------|-------------|--------|
| 5.1 | Build a `compute` utility module — accepts uploaded data files, runs Python/pandas, writes results to workspace JSON | [ ] |
| 5.2 | Add a `data_context` source to sources.py — summarizes uploaded structured files in the workspace | [ ] |
| 5.3 | Update `unit-economics`, `forecast`, and `trends` MODULE.md files to consume data_context when available | [ ] |

**Design constraint:** Skip the incremental "summarize files" phase. Either commit to a `compute` module that runs real code on real data, or defer entirely. The phased approach produces no value at Phase A.

## Phase 6 — Cross-Session Learning [PLANNED]

`snapshot → restore` preserves artifacts but not lessons. The system doesn't learn from its own execution history.

| Task | Description | Status |
|------|-------------|--------|
| 6.1 | Design a `lessons` source that extracts patterns from completed chains — "this user's brand positioning chains consistently score higher with 6 modules than 3" | [ ] |
| 6.2 | Determine whether lessons should be stored in the workspace (ephemeral, per-session) or in a persistent location (`partnership` profile, `.claude/memory`, or a dedicated lessons file) | [ ] |
| 6.3 | Wire lessons into `plan` — when composing chains, `plan` consults historical patterns to choose chain length and module selection | [ ] |

**The key question:** Where does learning live? The workspace is session-scoped by design. `partnership` captures collaboration preferences but not execution history. A new persistence layer risks breaking the "workspace is ephemeral" principle. One approach: lessons are extracted by `retro`, written to a `lessons.json` file that `snapshot` packages, and `plan` reads on restore. Learning is opt-in (you have to run `retro` + `snapshot`) and portable (it travels with the snapshot).

## Phase 7+ — Placeholders

- **Module discovery UX** — Can `help` be more contextual? "You just ran competitive-messaging. Modules that typically follow it: creative-brief, positioning, tagline."
- **Chain templates** — Named chains that encode common workflows. `reflex brand-launch target:X` expands to the full research → creative → email pipeline. Different from `full-analysis` in that it's a named alias, not a dependency tree.
- **Multi-user workspace** — If reflex ever runs in a shared context, workspace files need namespacing. Currently irrelevant (single user) but the `/home/claude/{type}_{target}.json` convention would collide.
- **Module versioning** — No mechanism for A/B testing module instructions. If you want to test whether a modified `email-draft` produces better output, you currently have to overwrite it. A `variants/` approach could work but adds Level 3 complexity to Level 1 modules.
- **Claim-testing modules** — The space between `do` (catch-all) and named analytical modules is underserved. Statements like "our pricing is wrong" or "is this market growing?" aren't research questions, analysis questions, or formatting questions — they're claims that need testing. A module (or chain pattern) that takes a claim, identifies what would need to be true for it to hold, and sets up downstream evidence gathering would fill this gap. This is where module growth produces genuine new capability, not diminishing returns.

## Phase 8 — Persona System [IN PROGRESS]

Personas are a persistent conversational layer over module dispatch. A user types `reflex persona copilot` and gets a thinking partner who silently orchestrates modules — no chain syntax, no module names, just conversation.

**Why personas are not modules:** Modules are bounded (input → output → done) and composable (`+` chains, DEPENDS.json). A persona is persistent (stays active across turns) and unbounded (no defined output shape). If a persona lived in `modules/`, it would be chainable — `websearch+copilot` would be valid syntax, producing incoherent behavior. The parallel `personas/` directory protects this invariant at the type level: everything in `modules/` is composable, everything in `personas/` is persistent. No flags, no exclusion lists, no special cases in dispatch.py.

**Architecture:** `persona.py` is a parallel dispatch script that reads `personas/` by convention. It shares `sources.py` injection (same import, same sources) and can call `dispatch.py` for module invocation. Neither script knows about the other's internals. dispatch.py is untouched (Golden Rule 1).

**File conventions:**
- `PERSONA.md` — Required. Identity, behavior, module invocation instructions. Like MODULE.md but for persistent operation.
- `PARAMS.json` — Optional. Inject-only params (registry, workspace). Same format as module PARAMS.json.
- `TRIGGERS.json` — Optional. Persona-specific. Maps conversational signals to suggested modules and behaviors.
- `STYLE.json` — Optional. Persona-specific. Voice characteristics, tone adaptation, signal phrases, formatting rules.

| Task | Description | Status |
|------|-------------|--------|
| 8.0 | Persona architecture: persona.py, personas/ directory, SKILL.md routing | [x] |
| 8.1 | First persona: `copilot` with PERSONA.md, PARAMS.json, TRIGGERS.json, STYLE.json | [x] Installed, not yet live-tested |
| 8.2 | Live test: `reflex persona copilot` in a fresh conversation — validate persistence, module invocation, trigger recognition, style adaptation | [~] First test: persona loaded, style worked, triggers fired, but copilot used zero reflex modules — routed all work through Claude's native tools (WebSearch, Write, etc.). Root cause: PERSONA.md instructions were suggestive, not directive. Fix: added mandatory module rule, concrete dispatch examples, and MUST directives in TRIGGERS.json. Needs re-test. |
| 8.3 | Test persona/module isolation — confirm copilot does not appear in module registry or chain composition | [ ] Verify via dispatch.py --list and plan's registry injection |

## ONGOING

- **Module count is now 72.** The `help list` output is long. Consider whether `help` should group by use case ("I want to launch a brand" → shows relevant modules) in addition to group taxonomy.
- **The `usage` field in PARAMS.json** is consumed by the LLM when evaluating the injected registry during `plan` routing. Strong, discriminating usage phrases help the LLM match intent to module. Every new module should be tested with `reflex plan "intent that should match"` immediately after creation.
- **`design-module` creates modules in `/home/claude/modules/` then copies to the skill directory.** This works but means the module files exist in two places during a session. The canonical location is the skill directory; the workspace copy is disposable.
- **Installed skill path can become stale.** When modules are added to the repo, the installed skill copy (used by dispatch at runtime) doesn't update automatically. New modules exist in the repo but dispatch can't see them until the skill is re-installed or re-uploaded. This caused `partnership` and the 8 specialization modules to be invisible to dispatch during the session where they were created. See README.md "Known Issue: Stale Skill Installations" for workarounds.

## DECISION LOG

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-31 | Added 5 marketing/creative modules (competitive-messaging, audience-portrait, creative-brief, tagline, email-draft upgrade) | Evaluation showed Report A scored 3-4 on dimensions where Report B scored 5. Each new module targets a specific scoring gap. |
| 2026-03-31 | `email-draft` upgraded to use `message_compose_v1` tool | Produces interactive email drafts with "Open in Mail" button instead of plain text |
| 2026-03-31 | `tagline` placed in transformer group, not analyzer | It reshapes upstream positioning into a specific creative artifact. It doesn't interpret data through a new framework — it distills existing strategy into a form. |
| [ASSUMED: pre-session] | `plan` threshold set at 0.18 for TF-IDF routing | Low threshold favors routing over suggesting new modules. Appropriate for a system that's module-rich. May need raising if false-positive routing becomes a problem. |
| [ASSUMED: pre-session] | `run` pauses after each step | Gives user control at the cost of friction. Decision on "just go" mode is open (Phase 1, Task 1.5). |
| 2026-03-31 | `plan` resolver changed to LLM passthrough; `suggest` variant removed | TF-IDF routing replaced with LLM evaluation. The `route` variant now handles both chain composition and new module design in a single MODULE.md. Resolver always prints `route`. |
| 2026-03-31 | `plan` writes `run_plan.json` directly (not `plan_output.json`) | Eliminates the fragile conversation-context parsing step in `run/start`. Plan and run are now tightly coupled through a shared file format. |
| 2026-03-31 | `run/start` reads `run_plan.json` file-first, conversation-context as fallback | Deterministic handoff. Shows plan summary before executing step 1. |
| 2026-03-31 | 8 specialization modules added (audit, experiment, forecast, ideate, onboard, retro, transcript, voice-dna) | Each uses the DEPENDS.json specialization pattern — thin synthesis layer on top of an existing module. Designed to address gaps identified by fetching external skill catalog and diffing against registry, then stress-tested with `challenge` at high intensity. |
| 2026-03-31 | `partnership` module added | Behavioral calibration module that loads a structured user profile (thinking style, quality signals, collaboration preferences) to orient a new session. |
| 2026-03-31 | `refine` module added | Level 1 transformer that closes the evaluator-optimizer loop. Reads audit/evaluate/debrief feedback, extracts revision constraints, and re-executes the original deliverable step with feedback injected. Enables self-improving chains like `email-draft+audit+refine`. |
| 2026-03-31 | `perspective` module added | Level 1 transformer with lens-based evaluation. Applies a perspective shift to upstream output — the lens reveals what the output can't see about itself, and the revelation IS the revision. 7 built-in lenses drawn from Walter's manual evaluation prompts, plus workspace lenses (rubrics, voice profiles, audit findings) and custom user text. Self-terminating: "if thorough, say so and stop." Preferred over `audit+refine` for iterative improvement because it skips the lossy score-to-instruction translation. |
| 2026-03-31 | Lens concern convention added to all 5 formatters | email-draft, write-report, whitepaper, pitch, linkedin now pre-commit to a weakness before writing. Each writes a `lens_concern` field to output JSON. `perspective` reads it and starts there. The convention closes the feedback loop: modules predict their weakness, perspective confirms or surprises. |
| 2026-03-31 | `test-perspective` module added | Calibration module: generates deliverables with known, planted flaws, then tests whether each of the 7 lenses catches its target flaw. Scenario 1 plants a deliberately wrong lens_concern to test whether perspective follows the misdirection or finds the actual gap. |
| 2026-03-31 | Lens library extracted to LENSES.json + sources.py | Hardcoded lens names removed from all 5 formatter MODULE.md files. Canonical lens definitions now live in `perspective/LENSES.json`, read by `lens_library` source, injected via PARAMS.json. Adding a lens = one file edit. |
| 2026-03-31 | Fixed: inject params missing from inline chains | `build_inline_chain()` in dispatch.py was not calling `inject_params()`. Source-injected params (workspace_state, lens_library) were silently missing from `+` chain steps. One-line fix. |
| 2026-04-01 | `unsupported-confidence` lens added (lens #8) | Debrief on multi-pass perspective test found invention-detection gap: existing 7 lenses watch for omission and misframing, none catch fabricated claims. New lens targets social proof, unearned specificity, and confidence that appeared from nowhere. |
| 2026-04-01 | Phase 4.8 investigated — Level 3 upgrade deferred | `build_inline_chain()` doesn't run resolvers, so a Level 3 upgrade wouldn't affect the `+` chain path (the primary multi-pass pattern). Recommended: test whether LLM naturally avoids lens repetition first (Option 3), escalate to workspace-stateful resolver (Option 2) if needed. |
| 2026-04-01 | Phase 4.8 resolved by design — no resolver needed | Live test confirmed LLM naturally rotates lenses in multi-pass (strategic-avoidance → hidden-assumptions). Scenario 9 calibration test confirmed: hidden-assumptions → strategic-avoidance. Upstream `lens_applied` in chain context is sufficient signal. |
| 2026-04-01 | Phase 4.10 validated — unsupported-confidence lens + rotation | Scenario 8: HIT on all 3 planted fabrications. Scenario 9: ROTATE confirmed. test-perspective now has 9 scenarios (up from 7). |
| 2026-04-01 | Persona system added as parallel architecture (not as modules) | Personas violate the module composition contract — they're persistent and unbounded, modules are bounded and composable. Putting a persona in `modules/` would make it chainable (`websearch+copilot`), producing incoherent behavior. The parallel `personas/` directory protects the composition invariant at the type level. dispatch.py untouched. |
| 2026-04-01 | Copilot PERSONA.md rewritten: suggestive → directive module invocation | First live test showed copilot used zero reflex modules despite having the full registry injected. LLM chose native tools (WebSearch, Write) as path of least resistance. Fix: mandatory module rule ("MUST use reflex modules for any work product"), concrete dispatch examples for 7 common patterns, MUST directives in all TRIGGERS.json notes. |

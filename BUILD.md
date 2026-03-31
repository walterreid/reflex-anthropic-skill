# BUILD.md — Reflex

## Current State

The system is built and functional. 71 modules across 6 groups. The dispatch engine, source injection, chain composition, Level 0-3 routing, dependency resolution, and workspace persistence all work. This document is not a build plan — it's a diagnostic of where the system's design assumptions are under pressure and what to do about it.

## Phase 0 — Foundation [COMPLETE]

| Task | Description | Status |
|------|-------------|--------|
| 0.1 | dispatch.py — param extraction, chain building, resolver execution | [x] |
| 0.2 | sources.py — module_registry and workspace_state injection | [x] |
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

## Phase 4+ — Placeholders

- **Module discovery UX** — Can `help` be more contextual? "You just ran competitive-messaging. Modules that typically follow it: creative-brief, positioning, tagline."
- **Chain templates** — Named chains that encode common workflows. `reflex brand-launch target:X` expands to the full research → creative → email pipeline. Different from `full-analysis` in that it's a named alias, not a dependency tree.
- **Multi-user workspace** — If reflex ever runs in a shared context, workspace files need namespacing. Currently irrelevant (single user) but the `/home/claude/{type}_{target}.json` convention would collide.
- **Module versioning** — No mechanism for A/B testing module instructions. If you want to test whether a modified `email-draft` produces better output, you currently have to overwrite it. A `variants/` approach could work but adds Level 3 complexity to Level 1 modules.

## ONGOING

- **Module count is now 71.** The `help list` output is long. Consider whether `help` should group by use case ("I want to launch a brand" → shows relevant modules) in addition to group taxonomy.
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

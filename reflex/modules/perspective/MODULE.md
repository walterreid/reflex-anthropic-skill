# Perspective Module

Apply an evaluation lens to upstream output. The lens doesn't score. It reveals what the output can't see about itself. The revelation IS the revision.

This module works the way a great editor works: not by grading your draft, but by reading it from an angle you couldn't occupy while writing it. If the angle reveals something, the module produces what the original would have produced if it had seen what the lens sees. If the angle reveals nothing, the module says so and stops.

- **Target**: {target}
- **Lens**: {lens}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## The Register

Every lens application opens with this frame. Do not skip it. It sets the standard for how you read:

> Treat nuance as a feature, not noise.
> The last step didn't miss the evidence. It missed what the evidence implied.

This is not a call to be harsh. It's a call to be honest about what was *chosen* — what angles were taken, what was set aside, what was followed halfway then dropped. Most output is competent. The question is whether it's complete in the ways that matter.

## The Lens Library

The canonical lens definitions live in `LENSES.json` in this module's directory. That file is the single source of truth — it's read by the `lens_library` source in sources.py and injected into any module that needs it (formatters use it for pre-commit self-assessment). Adding a new lens means adding it to LENSES.json. Every module that injects `lens_library` will see it automatically.

The full lens descriptions below are the implementation details — what each lens actually does when applied. LENSES.json has the names and short descriptions; this MODULE.md has the full prompts.

### Built-In Lenses

**missed-implications** — When the output feels thin but you can't say why.
> If the previous step's conclusion diverged from the evidence's strongest implications, identify where that interpretive gap occurred.

*What this reveals*: findings that were stated but not followed to their logical consequence. Data that was present but not weighted by its importance. Connections that were available but not drawn.

**wrong-framing** — When the answer might be correct within the wrong question.
> If the previous step's conclusion diverged from the evidence's strongest implications, identify whether the gap was in the reasoning — or in what they chose to reason about.

*What this reveals*: that the output answered a slightly different question than the one that mattered. That the framing excluded the most interesting part of the problem. That the analytical lens was competent but pointed at the wrong thing.

**hidden-assumptions** — When a confident answer was given too quickly.
> If the previous step's conclusion diverged from the evidence's strongest implications, identify what assumption they didn't examine that, if wrong, would change the answer entirely.

*What this reveals*: load-bearing beliefs that were treated as facts. Premises that weren't argued for because they felt obvious. The thing that, if pulled out, collapses the structure.

**strategic-avoidance** — When the output is technically correct but someone answered the easy version of the question.
> If the previous step's conclusion diverged from the evidence's strongest implications, identify what they accurately described but declined to follow all the way to its logical end.

*What this reveals*: the moment the output flinched. Where it was tracking toward an uncomfortable or complex implication and chose to summarize instead of conclude. The thread it dropped.

**operational-gap** — When the insight needs to become a decision.
> If the previous step's conclusion diverged from the evidence's strongest implications, identify the gap — and state what decision that gap, correctly closed, would change.

*What this reveals*: that the analysis was descriptive when it should have been prescriptive. That the user needed an action, not an observation. That the bridge from understanding to doing was left unbuilt.

**steelman-then-gap** — When the stakes are high and the output deserves to be taken seriously before being interrogated.
> Take the previous step's conclusion at its strongest. Then identify where even that strongest version diverges from what the evidence most directly implies.

*What this reveals*: the irreducible gap. After you've given the output every benefit of the doubt, what still doesn't hold? This is the most honest lens — it can't be dismissed as uncharitable.

**changed-context** — When evidence has evolved since the conclusion was drawn.
> Given what's been established since the previous step's conclusion was drawn, identify where that conclusion now diverges from the strongest current reading of the evidence.

*What this reveals*: that the output was correct when written but the ground shifted. That new information in the workspace (from later chain steps or new research) makes an earlier conclusion stale. Most useful in long chains or when re-examining snapshotted work.

**unsupported-confidence** — When the output sounds authoritative but some claims may have no evidence trail.
> Identify any claim, figure, or characterization in the output that reads as earned knowledge but traces to no evidence in the upstream context. Social proof, specificity, and certainty that appeared from nowhere — not gaps in reasoning, but inventory that was never sourced.

*What this reveals*: invented social proof ("users loved it"), unearned specificity ("a 40% improvement"), confident characterizations that sound researched but were fabricated during the writing process. The other lenses watch for what's missing or misframed. This one watches for what appeared from nowhere. Most valuable after perspective rewrites or in research-free chains where there's no upstream evidence to ground claims against.

### Workspace Lenses

Before applying a built-in lens, check the workspace for custom lens sources:

- `rubric_*.json` — A rubric's dimensions can be read as lenses. Each dimension becomes: "Examine the output through the lens of [dimension]. What does it reveal that the output isn't already doing?"
- `voice_*.json` — A voice profile becomes a lens: "Read the output through the voice described in this profile. Where does the output diverge from how this voice would naturally express these ideas?"
- `audit_*.json` — An audit's findings become lenses. Each low-scoring dimension becomes: "The audit identified [issue]. What is the output not seeing about its own [dimension] that, if seen, would change how it handles it?"
- Any file containing a `lens` or `lenses` field is consumed directly.

Workspace lenses take precedence over built-in lenses when they match the `{target}`.

### Custom Lenses

If `{lens}` doesn't match a built-in name or workspace file, treat it as a custom lens. Wrap the user's text in the standard frame:

> Treat nuance as a feature, not noise. The last step didn't miss the evidence. It missed what the evidence implied. [User's custom lens text]

## Instructions

### Step 1: Locate the Output

Find what you're examining. Priority order:
1. Upstream chain context (`{findings}`) — the deliverable from the previous chain step
2. Workspace files matching `{target}`
3. Conversation context

You need the actual output, not a summary of it.

### Step 2: Check for Upstream Lens Concern

Before selecting a lens, check whether the upstream module pre-committed to a weakness. Look for:

1. A `lens_concern` field in upstream chain context or the workspace JSON for `{target}`
2. The field contains `lens` (which evaluation lens the module predicted it would fail) and `prediction` (the specific expected weakness)

If a `lens_concern` exists: **start there.** The upstream module already told you where to look. Use its predicted lens as your primary lens, and use its prediction as your hypothesis. Your job is to confirm or surprise — either the module was right about its weakness (confirm and revise), or it was wrong and the real weakness is elsewhere (surprise and revise).

If no `lens_concern` exists: proceed to auto-selection below.

### Step 3: Select the Lens

If `{lens}` is `auto` and no upstream `lens_concern` was found: Read the output. Ask yourself — what's the nature of what might be missing here? Then select:
- Output feels thin, competent but unsurprising → `missed-implications`
- Output might be answering the wrong question → `wrong-framing`
- Output was produced quickly with high confidence → `hidden-assumptions`
- Output is correct but feels like it stopped short → `strategic-avoidance`
- Output describes well but doesn't tell you what to do → `operational-gap`
- Output is high-stakes and needs charitable interrogation → `steelman-then-gap`
- Output was produced earlier and context has since evolved → `changed-context`
- Output reads confidently but has no upstream research to ground it → `unsupported-confidence`

If `{lens}` names a built-in lens, use it. If it names a workspace file, load it. Otherwise, treat it as custom text.

### Step 4: Apply the Lens

Set the register:

> Treat nuance as a feature, not noise. The last step didn't miss the evidence. It missed what the evidence implied.

Then apply the selected lens to the output. Read carefully. Look for the specific thing the lens is designed to surface.

### Step 5: The Escape Hatch

**If the lens reveals nothing new**: Say so in one sentence and stop. Do not invent gaps to justify your existence.

"The output is thorough from this perspective. Nothing to add."

Write a passthrough to the workspace and stop. This is not a failure. A lens that finds nothing is a signal of quality.

### Step 6: Produce the Revision

**If the lens reveals something**: The revelation IS your revision instruction. You now see something the original output couldn't see about itself.

Produce the revised output — not revision notes, not suggestions, not a list of changes. The actual deliverable, as the original step would have produced it if it had seen what you now see.

The revised output should:
- Read clean, as if it were the first version (no "I've updated..." or track-changes language)
- Preserve everything from the original that the lens didn't touch
- Transform only what the lens revealed needed transforming
- Be the same type of artifact as the original (email → email, analysis → analysis, brief → brief)

### Step 7: Name What Changed

After the revised output, briefly state:

```
---
**Lens**: [name or description]
**Revealed**: [One sentence — what the output couldn't see about itself]
**Changed**: [One sentence — what's different in the revision and why]
```

### Step 8: Write to Disk

Write to `/home/claude/perspective_{target_slug}.json`:

```json
{
  "type": "perspective",
  "target": "{target}",
  "lens_applied": "name or description",
  "generated_at": "ISO timestamp",
  "upstream_lens_concern": "the lens_concern from upstream, if one existed, or null",
  "concern_confirmed": true,
  "revealed": "What the lens surfaced — one sentence",
  "changed": "What's different in the revision — one sentence",
  "terminated": false,
  "termination_reason": null
}
```

The `upstream_lens_concern` and `concern_confirmed` fields create a feedback loop: the upstream module predicted its weakness, and perspective records whether that prediction was accurate. Over time, this makes the pre-commit more honest — modules learn (through the patterns visible in workspace artifacts) what they actually get wrong versus what they think they get wrong.

If the lens found nothing (Step 4), write:

```json
{
  "type": "perspective",
  "target": "{target}",
  "lens_applied": "name or description",
  "generated_at": "ISO timestamp",
  "revealed": null,
  "changed": null,
  "terminated": true,
  "termination_reason": "Lens revealed nothing new. Output is thorough from this perspective."
}
```

## Output

If the lens revealed something: the revised deliverable (clean, complete), followed by the three-line lens/revealed/changed summary.

If the lens revealed nothing: one sentence confirming thoroughness. Nothing more.

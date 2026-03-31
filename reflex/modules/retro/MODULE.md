# Retro Module

Extract forward-looking lessons from a session. The `debrief` dependency has audited what evidence survived, was lost, or was invented. This module looks at the *process and judgment*, not just the data fidelity — what worked, what didn't, and what to do differently.

- **Target**: {target}
- **Scope**: {scope}
- **Fidelity audit**: {fidelity_audit}

## How This Differs from debrief

`debrief` asks "was the evidence handled correctly?" — it's an audit of information integrity. `retro` asks "what did we learn and what should change?" — it's a reflection on process, judgment, and surprising discoveries. A debrief catches errors. A retro captures wisdom.

## Instructions

### Step 1: What Worked

From the session's outputs and the fidelity audit, identify:
- **Strongest finding**: The single insight or result that was best-supported and most useful. Why was it strong? Was it the module choice, the data quality, or the analytical frame?
- **Best chain decision**: If modules were chained, which sequencing choice paid off? What would have been missed without it?
- **Unexpected value**: Something that produced more insight than expected. Why was this surprising?

### Step 2: What Didn't Work

- **Weakest finding**: The insight or result that was least supported or least useful. Was this a data problem, a framing problem, or a module limitation?
- **Evidence gaps**: What did you wish you had data on but didn't? What upstream source would have helped?
- **Wasted effort**: Any step that produced output that downstream modules didn't meaningfully use. Was the step wrong or was the chain structure wrong?

### Step 3: What Surprised

This is the most important section. List 2-4 things that were genuinely non-obvious:
- Findings that contradicted initial assumptions
- Connections between data points that weren't expected
- Module outputs that were better or worse than anticipated
- Questions that emerged that nobody thought to ask at the start

For each surprise: state the surprise, why it matters, and whether it changes how you'd approach this topic next time.

### Step 4: Carry-Forward Items

Concrete things to remember or do differently:
- **For the next session on this topic**: What context should be pre-loaded? What modules should be run first? What assumptions should be tested early?
- **For the system itself**: Any module that should be modified, a new module that's needed, a chain pattern that should become a named workflow
- **For the user**: Decisions that are now ready to be made, questions that need external input, risks that need monitoring

### Step 5: Write to Disk

Write to `/home/claude/retro_{target_slug}.json`:

```json
{
  "type": "retrospective",
  "target": "{target}",
  "generated_at": "ISO timestamp",
  "worked": {
    "strongest_finding": {"finding": "...", "why_strong": "..."},
    "best_chain_decision": "...",
    "unexpected_value": "..."
  },
  "didnt_work": {
    "weakest_finding": {"finding": "...", "why_weak": "..."},
    "evidence_gaps": ["..."],
    "wasted_effort": "..."
  },
  "surprises": [
    {"surprise": "...", "why_it_matters": "...", "changes_approach": true}
  ],
  "carry_forward": {
    "next_session": ["..."],
    "system_improvements": ["..."],
    "user_decisions": ["..."]
  }
}
```

## Output

Present as a concise retrospective — not a report, a reflection. Lead with surprises (they're the most valuable). Then what worked, what didn't, and carry-forward items. End with a single sentence: "The most important thing to remember is [X]."

Keep it honest. A retro that says everything was great is a retro that learned nothing.

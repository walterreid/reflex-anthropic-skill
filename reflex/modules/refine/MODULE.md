# Refine Module

Close the evaluation loop. Read feedback from `audit`, `evaluate`, or `debrief`, extract the specific problems, then **re-execute the original deliverable step** with those problems as revision constraints.

This is not a suggestion engine. It does the work again, better.

- **Target**: {target}
- **Scope**: {scope}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Find the Feedback

Locate the evaluation that drives this refinement. Search in this order:

1. Upstream chain context (`{findings}`) — if `refine` was chained after `audit` or `evaluate`, the feedback is already in context
2. Workspace files matching `audit_{target}*.json`, `evaluate_{target}*.json`, or `debrief_{target}*.json`

If no feedback is found, stop. Say: "Nothing to refine against. Run `reflex audit target:{target}` or `reflex evaluate target:{target}` first, then chain: `reflex audit+refine target:{target}`"

### Step 2: Find the Original Deliverable

Locate what was evaluated. Search:

1. Upstream chain context — if the deliverable was produced earlier in the chain
2. Workspace files — the audit/evaluate output usually names its target; find the corresponding file
3. Conversation context — the deliverable may have been rendered inline

You need both the deliverable AND the instructions that produced it (i.e., which module created it). The audit file's `target` field and the workspace file's `type` field tell you which module to replay.

### Step 3: Extract Revision Constraints

From the feedback, extract concrete problems — not scores, not summaries, but specific fixable issues.

Apply `{scope}`:
- **top1**: The single highest-leverage fix. Usually the `biggest_fix` field from audit, or the lowest-scoring dimension from evaluate.
- **top3**: The three changes that would most improve the deliverable. Prioritize by impact, not by score delta.
- **all**: Every issue identified. Use sparingly — too many constraints produce incoherent revisions.

For each issue, write a **revision constraint** in this format:
- **Problem**: What's wrong, in one sentence
- **Location**: Where in the deliverable (section, paragraph, or structural element)
- **Fix**: What the revised version must do differently — specific enough that you could verify compliance

### Step 4: Re-Execute with Feedback

This is the core move. You are not writing revision notes — you are producing the revised deliverable.

1. Identify which module originally produced the deliverable (e.g., `email-draft`, `write-report`, `creative-brief`, `whitepaper`, `pitch`)
2. Re-execute that module's task, using the same upstream context and params, but with the revision constraints injected as additional instructions
3. The revision constraints override the original instructions where they conflict — if the audit said "voice is too formal," the revised version uses a warmer voice even if the original module instructions say "maintain professional tone"

Write the revised deliverable as if it were the first version. No track-changes, no "here's what I fixed" annotations in the output itself. The deliverable should read clean.

### Step 5: Document What Changed

After producing the revised deliverable, write a brief revision log:

```
## Revision Log

**Source feedback**: [audit/evaluate/debrief filename or "chain context"]
**Scope**: {scope}
**Constraints applied**:
1. [Problem → Fix, one line each]

**What changed**: [2-3 sentences on the substantive differences between original and revision]
```

### Step 6: Write to Disk

Write the revision log to `/home/claude/refine_{target_slug}.json`:

```json
{
  "type": "refine",
  "target": "{target}",
  "scope": "{scope}",
  "generated_at": "ISO timestamp",
  "feedback_source": "filename or chain context",
  "original_module": "the module that produced the original deliverable",
  "constraints_applied": [
    {
      "problem": "...",
      "location": "...",
      "fix": "..."
    }
  ],
  "changes_summary": "2-3 sentence description of what changed"
}
```

The revised deliverable itself is the primary output — rendered inline, not in the JSON. The JSON is the audit trail.

## Output

The revised deliverable, clean and complete, followed by the revision log. The deliverable comes first because that's what the user cares about. The log comes second so they can see what changed and why.

If chained further (e.g., `audit+refine+audit` for a second pass), the revised deliverable becomes the input for the next step.

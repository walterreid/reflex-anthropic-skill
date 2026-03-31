# Audit Module

Score a deliverable against quality dimensions. The `debrief` dependency has already checked information fidelity — what evidence survived, what was lost, what was invented. This module adds the quality-gate scoring layer.

- **Target**: {target}
- **Criteria**: {criteria}
- **Standard**: {standard}
- **Fidelity report**: {fidelity_report}

## Instructions

### Step 1: Consume the Fidelity Report

The `debrief` dependency traced evidence through the chain. Use its findings as ground truth:
- Claims flagged as "invented" are automatic failures on accuracy
- Claims flagged as "lost" indicate completeness gaps
- Claims that survived with attribution are the deliverable's strengths

### Step 2: Score Each Dimension

For each dimension in `{criteria}`, score 1-5 calibrated to `{standard}`:

**Accuracy** (is it true?)
- Are claims supported by evidence from upstream research?
- Are statistics, names, and specifics correct?
- Does it distinguish between sourced facts and inferences?

**Structure** (is it navigable?)
- Can a reader find what they need without reading everything?
- Is there a clear hierarchy (headline → support → detail)?
- Are transitions between sections logical?

**Completeness** (is anything missing?)
- Does it address the original intent fully?
- Are there obvious gaps a reader would notice?
- Were any upstream findings dropped without justification?

**Voice** (does it sound right?)
- Is the tone consistent throughout?
- Does it match the stated audience?
- Are there jarring shifts (e.g., analytical section suddenly becoming casual)?

**Actionability** (can someone act on this?)
- Is there a clear "so what"?
- Are next steps explicit or at least implied?
- Could someone who only reads the conclusion make a decision?

Adjust dimensions to match `{criteria}` if the user specified custom dimensions. Score each 1-5 with a one-sentence justification.

### Step 3: Identify the Single Biggest Fix

After scoring everything, name the ONE change that would most improve the deliverable. Not a list of 10 suggestions — the single highest-leverage edit.

### Step 4: Render the Scorecard

```
## Quality Audit: {target}
Standard: {standard}

| Dimension     | Score | Assessment |
|---------------|-------|------------|
| Accuracy      | X/5   | One sentence |
| Structure     | X/5   | One sentence |
| Completeness  | X/5   | One sentence |
| Voice         | X/5   | One sentence |
| Actionability | X/5   | One sentence |

**Overall: X/25**

**Fidelity summary**: [1-2 sentences from debrief — how much evidence survived the chain]

**Biggest fix**: [The single most impactful change]

**Verdict**: [PASS / PASS WITH REVISIONS / FAIL] at {standard} standard
```

### Step 5: Write to Disk

Write to `/home/claude/audit_{target_slug}.json`:

```json
{
  "type": "audit",
  "target": "{target}",
  "standard": "{standard}",
  "generated_at": "ISO timestamp",
  "scores": {
    "dimension_name": {"score": 4, "assessment": "..."}
  },
  "overall_score": 20,
  "max_score": 25,
  "fidelity_summary": "...",
  "biggest_fix": "...",
  "verdict": "pass|pass_with_revisions|fail"
}
```

## Output

The scorecard table above, followed by the verdict. Keep it tight — this is a gate, not a review essay.

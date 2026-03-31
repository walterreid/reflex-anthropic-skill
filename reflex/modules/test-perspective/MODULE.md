# Test Perspective Module

Smoke test the `perspective` module by producing deliverables with **known, planted weaknesses**, then evaluating whether each lens catches the flaw it's designed to find.

This is not a unit test. It's a calibration exercise. If a lens can't find a flaw that was deliberately planted for it, the lens instructions need tuning.

- **Scenario**: {scenario}

## Available Workspace Data

{workspace}

## Test Scenarios

Each scenario has three parts:
1. **Seed** — A short deliverable with a specific, planted flaw
2. **Lens** — The lens that should catch it
3. **Expected** — What the lens should reveal (the planted flaw, described differently than it was planted)

### Scenario 1: missed-implications

**Seed**: Write a 2-paragraph competitive analysis of a fictional coffee subscription service ("BeanBox") entering a market dominated by "BrewClub." Include three data points about BrewClub's market share, BeanBox's pricing advantage, and customer churn rates. **Deliberately omit the obvious implication**: that the churn rate + pricing advantage together suggest a specific acquisition strategy.

State the data. Don't connect the dots.

**Lens**: `missed-implications`

**Expected**: The lens should surface that the churn data and pricing data together imply an undercut-and-capture strategy — the deliverable stated the evidence but didn't follow it to its conclusion.

**lens_concern to plant**: `{"lens": "strategic-avoidance", "prediction": "I'll describe the competitive dynamics without recommending a specific market entry approach"}` — Note: this is deliberately the *wrong* lens prediction. The module thinks it's strategically avoiding; the real gap is missed implications. This tests whether perspective follows the lens_concern or finds the actual gap.

### Scenario 2: wrong-framing

**Seed**: Write a 2-paragraph recommendation for whether "NovaTech" should build an AI feature. Frame it entirely as a build-vs-buy decision. **The planted flaw**: the real question isn't build vs buy — it's whether their customers even want AI features at all. The framing skips the demand question entirely.

**Lens**: `wrong-framing`

**Expected**: The lens should identify that the build-vs-buy framing assumes demand exists. The right first question is whether customers want this at all.

### Scenario 3: hidden-assumptions

**Seed**: Write a 2-paragraph financial projection for a SaaS startup's Series A. Project $2M ARR within 18 months based on current growth rate. **The planted assumption**: the projection assumes no increase in churn as the customer base scales past early adopters — which is almost never true.

**Lens**: `hidden-assumptions`

**Expected**: The lens should surface the churn-at-scale assumption.

### Scenario 4: strategic-avoidance

**Seed**: Write a 2-paragraph strategy memo about whether a team should adopt microservices. List the pros and cons fairly. **The planted flaw**: the memo presents both sides but never takes a position. It stops at description and avoids the recommendation.

**Lens**: `strategic-avoidance`

**Expected**: The lens should identify that the memo accurately describes the trade-offs but declines to follow them to a recommendation.

### Scenario 5: operational-gap

**Seed**: Write a 2-paragraph analysis of why a product launch failed. Identify three root causes clearly. **The planted flaw**: strong diagnosis, zero prescription. The analysis says what went wrong but never says what to do next time.

**Lens**: `operational-gap`

**Expected**: The lens should surface that the analysis is descriptive when it should be prescriptive — it needs to translate the root causes into specific preventive actions.

### Scenario 6: steelman-then-gap

**Seed**: Write a 2-paragraph argument for why remote work is better than in-office. Make it strong and well-evidenced. **The planted flaw**: the argument is genuinely good but ignores the strongest counter-evidence (studies showing junior employee mentorship and spontaneous collaboration degrade remotely).

**Lens**: `steelman-then-gap`

**Expected**: The lens should take the remote work argument seriously, then identify the mentorship/collaboration gap as the irreducible weakness even in the strongest version.

### Scenario 7: changed-context

**Seed**: Write a 2-paragraph recommendation from "early 2024" about investing in a specific AI model provider, citing their technical lead and first-mover advantage. **The planted flaw**: the recommendation was correct at the time but the landscape has changed — open-source models have closed the gap and commoditized the technical advantage.

**Lens**: `changed-context`

**Expected**: The lens should identify that the first-mover/technical-lead thesis no longer holds given open-source competition.

## Instructions

### If scenario is "quick"

Run Scenario 1 only. Fastest validation.

### If scenario is "all"

Run all 7 scenarios in order. This is the full calibration.

### If scenario is a specific lens name

Run only the scenario that matches that lens.

### For each scenario:

1. **Generate the seed deliverable.** Write it exactly as described — including the planted flaw. Do NOT fix the flaw. The whole point is to produce output that has a known, specific weakness. Include the planted `lens_concern` where specified.

2. **Apply the lens.** Now shift roles. You are the `perspective` module. Apply the register:

   > Treat nuance as a feature, not noise. The last step didn't miss the evidence. It missed what the evidence implied.

   Then apply the specific lens to the seed deliverable.

3. **Evaluate the result.** Did the lens find the planted flaw? Score:
   - **HIT** — The lens identified the specific planted weakness (phrased differently than it was planted — not just echoing the test)
   - **ADJACENT** — The lens found a real weakness but not the planted one
   - **MISS** — The lens found nothing, or found something unrelated

4. **If the lens_concern was planted wrong** (Scenario 1): Did perspective follow the wrong lens_concern, or did it find the actual gap despite the misdirection? Score:
   - **INDEPENDENT** — Found the real gap despite the wrong lens_concern
   - **MISLED** — Followed the lens_concern and missed the actual gap

### After all scenarios:

Write results to `/home/claude/test_perspective.json`:

```json
{
  "type": "test_perspective",
  "generated_at": "ISO timestamp",
  "scenarios_run": 7,
  "results": [
    {
      "scenario": 1,
      "lens": "missed-implications",
      "planted_flaw": "churn + pricing imply acquisition strategy, not stated",
      "result": "HIT|ADJACENT|MISS",
      "lens_concern_test": "INDEPENDENT|MISLED|N/A",
      "what_lens_found": "one sentence",
      "notes": "any observations about lens behavior"
    }
  ],
  "summary": {
    "hits": 0,
    "adjacent": 0,
    "misses": 0,
    "lens_concern_independent": true
  },
  "calibration_notes": "Which lenses need tuning, if any. What patterns you noticed."
}
```

## Output

A results table:

```
| # | Lens                  | Result   | Concern Test  | Notes |
|---|-----------------------|----------|---------------|-------|
| 1 | missed-implications   | HIT/ADJ/MISS | IND/MISLED | ... |
| 2 | wrong-framing         | ...      | N/A           | ... |
...
```

Followed by calibration notes: which lenses are sharp, which need tuning, and what you'd change in the lens language to improve detection. Keep it to 3-5 sentences. This is a diagnostic, not a report.

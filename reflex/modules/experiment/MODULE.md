# Experiment Module

Design a testable experiment from a claim or assumption. The `scenario` dependency has projected plausible futures. This module converts the most critical uncertainty into a concrete test you can run.

- **Target**: {target}
- **Scope**: {scope}
- **Constraints**: {constraints}
- **Projected futures**: {projected_futures}

## Instructions

### Step 1: Identify the Core Assumption

From `{target}` and the projected scenarios, find the single assumption that:
- Has the highest impact if wrong (the scenarios diverge most on this point)
- Is actually testable (you can observe evidence for or against it)
- Is currently unvalidated (you're operating on belief, not data)

State it as a falsifiable hypothesis: "We believe [X]. If true, we should observe [Y]. If false, we should observe [Z]."

### Step 2: Design the Experiment

Calibrate to `{scope}`:

**Micro** (1-2 weeks, minimal resources):
- Single variable. One thing to test.
- Smallest possible version that still produces signal.
- Example: send two email variants to 100 people each, measure open rates.

**Standard** (1-2 months, moderate resources):
- Can test 2-3 variables.
- Larger sample or longer observation window.
- Example: run a landing page test with paid traffic for 4 weeks.

**Ambitious** (quarter+, significant investment):
- Multi-variable or longitudinal.
- May require building something.
- Example: launch an MVP to a beta cohort and measure retention over 90 days.

For the experiment, specify:

- **What you're testing**: The specific hypothesis in plain language
- **Independent variable**: What you're changing/manipulating
- **Dependent variable**: What you're measuring
- **Control**: The baseline (what happens if you do nothing)
- **Sample/audience**: Who or what you're testing on, and minimum sample size for signal
- **Duration**: How long to run before reading results
- **Success criteria**: The specific threshold that would validate the hypothesis (be precise — "20% improvement" not "better")
- **Failure criteria**: What result would disprove the hypothesis
- **Ambiguity zone**: What result would be inconclusive and what you'd do next

### Step 3: Anticipate Confounds

List 2-3 things that could pollute your results:
- External factors (seasonality, competitor moves, news cycles)
- Selection bias (who opts in vs. who doesn't)
- Measurement error (are you measuring what you think you're measuring?)

For each confound, note whether you can control it and how.

### Step 4: Design the Debrief

Write the questions you'll answer after the experiment runs:
1. Did we hit the success or failure threshold?
2. What surprised us?
3. What did we learn that we didn't expect to learn?
4. What's the next experiment this suggests?
5. What decision can we now make that we couldn't before?

### Step 5: Write to Disk

Write to `/home/claude/experiment_{target_slug}.json`:

```json
{
  "type": "experiment",
  "target": "{target}",
  "scope": "{scope}",
  "generated_at": "ISO timestamp",
  "hypothesis": {
    "statement": "We believe...",
    "if_true": "We should observe...",
    "if_false": "We should observe..."
  },
  "design": {
    "independent_variable": "...",
    "dependent_variable": "...",
    "control": "...",
    "sample": "...",
    "duration": "...",
    "success_criteria": "...",
    "failure_criteria": "...",
    "ambiguity_zone": "..."
  },
  "confounds": [
    {"factor": "...", "controllable": true, "mitigation": "..."}
  ],
  "debrief_questions": ["..."],
  "constraints_applied": "{constraints}"
}
```

## Output

Present the experiment as a one-page brief someone could hand to their team and say "let's run this." Hypothesis first, design second, confounds third, debrief template last. The brief should make the reader feel like the hardest part (figuring out what to test and how) is already done.

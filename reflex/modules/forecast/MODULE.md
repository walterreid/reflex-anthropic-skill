# Forecast Module

Build a structured projection from trend signals. The `trends` dependency has identified signals with velocity and impact assessments. This module translates those into forward-looking projections with explicit confidence and sourcing.

- **Target**: {target}
- **Horizon**: {horizon}
- **Assumptions mode**: {assumptions}
- **Trend signals**: {trend_signals}

## Critical Honesty Rule

This module produces STRUCTURED THINKING about the future, not predictions. Every number must be tagged as `sourced` (from research data) or `estimated` (this module's inference). Any reader should be able to immediately tell which projections are grounded in data and which are reasoned guesses. If you cannot source a number, say so. False precision is the worst outcome this module can produce.

## Instructions

### Step 1: Extract Quantitative Anchors

From the trend signals and any upstream research, find every hard number:
- Market sizes, growth rates, adoption percentages (tag each as `sourced`)
- Time references: when trends started, acceleration points, saturation signals

If the upstream data has no hard numbers, state this explicitly and note that all projections below are `estimated` based on qualitative signals only.

### Step 2: Build the Projection

For `{target}` over `{horizon}`, project:

**Base case** (what happens if current trends continue):
- The quantitative trajectory (growth rate, market size, adoption curve, etc.)
- Key driver: which trend signal is most responsible for this trajectory
- Confidence: high/medium/low with one-sentence justification

**Upside case** (what accelerates things):
- Which trend would need to strengthen, and by how much
- The catalysts that could trigger this (regulatory change, technology shift, demand spike)
- Probability assessment: likely/possible/unlikely

**Downside case** (what slows or reverses):
- Which trend would need to decelerate or reverse
- The risks: competitive saturation, regulatory headwind, demand ceiling
- Probability assessment

### Step 3: Enumerate Assumptions

Based on `{assumptions}` mode:

**Stated** (default): List every assumption the projection rests on. For each:
- The assumption itself
- Whether it's sourced (from data) or estimated (your inference)
- What happens to the projection if this assumption is wrong
- How you would verify this assumption

**Optimistic**: Weight toward upside assumptions. Still list them, but note the optimistic lean.

**Conservative**: Weight toward downside assumptions. Useful for risk planning.

### Step 4: Identify the Swing Factor

Name the ONE variable that most determines which case plays out. This is the thing to watch — the leading indicator that will tell you earliest whether the projection is tracking.

### Step 5: Write to Disk

Write to `/home/claude/forecast_{target_slug}.json`:

```json
{
  "type": "forecast",
  "target": "{target}",
  "horizon": "{horizon}",
  "generated_at": "ISO timestamp",
  "data_quality": "strong|moderate|weak|qualitative_only",
  "base_case": {
    "projection": "...",
    "key_driver": "...",
    "confidence": "high|medium|low",
    "sourced_numbers": [{"metric": "...", "value": "...", "source": "..."}],
    "estimated_numbers": [{"metric": "...", "value": "...", "reasoning": "..."}]
  },
  "upside_case": {
    "projection": "...",
    "catalyst": "...",
    "probability": "likely|possible|unlikely"
  },
  "downside_case": {
    "projection": "...",
    "risk": "...",
    "probability": "likely|possible|unlikely"
  },
  "assumptions": [
    {"assumption": "...", "type": "sourced|estimated", "if_wrong": "...", "verification": "..."}
  ],
  "swing_factor": {
    "variable": "...",
    "leading_indicator": "...",
    "check_by": "date or milestone"
  }
}
```

## Output

Present as a concise forecast brief: base/upside/downside in a table, followed by assumptions and the swing factor. Lead with the data quality disclaimer. End with: "The single thing to watch is [swing factor]. If [indicator], the base case holds. If [alternative], revisit."

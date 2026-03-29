# Scenario Module

Project 2-4 plausible future scenarios from research findings, with implications and signals for each.

- **Target**: {target}
- **Horizon**: {horizon}
- **Count**: {count}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Gather evidence. Check the workspace for files matching `{target}`: research, compare, distill, or extract JSONs. Read them. Also use any upstream context from `{findings}`. If no upstream data exists, use your knowledge of `{target}` — but flag in the output that scenarios are based on general knowledge rather than researched evidence.

2. Identify the **key uncertainties** — the variables that could plausibly go in different directions over the `{horizon}` timeframe. Good uncertainties are:
   - Binary or spectrum (not just "things could change")
   - Independent of each other (to avoid redundant scenarios)
   - Consequential (the outcome matters for decisions)

3. Generate `{count}` scenarios. Each scenario should:
   - Have a short, memorable name (not "Scenario A" — something evocative like "The Regulatory Squeeze" or "Breakout Adoption")
   - Be grounded in the evidence — what specific findings support this trajectory?
   - Be internally consistent — the assumptions within each scenario don't contradict each other
   - Cover different parts of the possibility space — avoid clustering around the most likely outcome

4. For each scenario, specify:
   - **name**: Evocative short label
   - **probability**: Rough likelihood estimate (must sum to ~100% across scenarios, with a remainder bucket if needed)
   - **narrative**: 2-3 sentence description of how this future unfolds
   - **key_assumptions**: What must be true for this scenario to play out (list of 2-4 assumptions)
   - **implications**: What this means for someone making decisions about `{target}` (list of 2-3 implications)
   - **early_signals**: Observable indicators that would suggest this scenario is materializing (list of 2-3 signals)
   - **evidence_basis**: Which specific upstream findings support this scenario

5. Scenario types to ensure coverage:
   - At least one **continuation** scenario (current trends persist)
   - At least one **disruption** scenario (a key variable shifts dramatically)
   - If count >= 3, at least one **contrarian** scenario (the conventional wisdom is wrong)

6. Write scenarios to `/home/claude/scenario_{target}.json`:

```json
{
  "target": "{target}",
  "horizon": "{horizon}",
  "generated_at": "ISO timestamp",
  "evidence_source": "filename or 'general knowledge'",
  "key_uncertainties": [
    {
      "variable": "What could go either way",
      "spectrum": ["Low end", "High end"]
    }
  ],
  "scenarios": [
    {
      "name": "Evocative Name",
      "type": "continuation|disruption|contrarian",
      "probability": 0.35,
      "narrative": "How this future unfolds...",
      "key_assumptions": ["..."],
      "implications": ["..."],
      "early_signals": ["..."],
      "evidence_basis": ["Which findings support this"]
    }
  ],
  "meta": {
    "total_probability": 1.0,
    "coverage_gaps": "Any important possibilities not captured"
  }
}
```

7. Present the scenarios conversationally: name, probability, one-line narrative, and the top implication for each. End with the key uncertainties that differentiate the scenarios.

## Output

A structured set of future scenarios grounded in evidence, with probabilities, signals, and implications. The file on disk is designed for downstream consumption by `actions` (extract steps per scenario), `risks` (assess risks per scenario), `pitch` (argue for a strategy), or `write-report` (full scenario planning document). Keep the conversational summary to 10-15 lines.

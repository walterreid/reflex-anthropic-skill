# Evaluate Module

Score one or two targets against an evaluation rubric.

- **Target**: {target}
- **Target2**: {target2}
- **Domain**: {domain}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Load the rubric:
   - If upstream context contains rubric dimensions (from a chained `rubric` module), use those.
   - Otherwise, check the workspace data above for rubric files matching `{domain}`, and read the file.
   - If no rubric is found, respond with: "No rubric found for domain `{domain}`. Run `reflex rubric domain:{domain}` first, or chain it: `reflex rubric+evaluate domain:{domain} target:X`"
2. Load evidence about the targets:
   - If upstream context contains research or comparison findings, use those.
   - Otherwise, check the workspace data above for research, comparison, or distill files matching `{target}` or `{target2}`, and read the relevant files.
   - If no evidence is found, use your own knowledge — but note in the output that scores are based on general knowledge rather than researched findings.
3. For each rubric dimension, score each target from 1-5 using the rubric's anchored scale. Provide a one-sentence justification per score.
4. Calculate:
   - **Raw score**: Sum of all dimension scores (per target)
   - **Weighted score**: Sum of (score × weight) for each dimension (per target)
   - **Max possible**: Sum of (5 × weight) for each dimension
   - **Percentage**: Weighted score / max possible × 100
5. Write results to `/home/claude/evaluate_{target}_vs_{target2}.json` (or `evaluate_{target}.json` if single target) in this structure:

```json
{
  "domain": "{domain}",
  "rubric_used": "filename or 'inline from chain'",
  "evaluated_at": "ISO timestamp",
  "targets": {
    "{target}": {
      "scores": [
        {
          "dimension": "Name",
          "score": 4,
          "weight": 3,
          "weighted": 12,
          "justification": "One sentence"
        }
      ],
      "raw_total": 28,
      "weighted_total": 85,
      "max_possible": 125,
      "percentage": 68.0
    }
  },
  "verdict": "One sentence on the overall winner and why"
}
```

6. If two targets are provided, end with a clear verdict: which target scores higher, by how much, and which dimensions drove the difference.

## Output

A scorecard summary showing each target's scores per dimension, weighted totals, percentages, and the verdict. Keep it scannable — this output often feeds into formatters.

# Grade — Multi-Candidate Scorecard

Score multiple candidates against a consistent rubric and produce a ranked comparison.

- **Domain**: {domain}
- **Candidates**: {candidates}

## Context

If upstream findings exist (e.g., a rubric from the `rubric` module or extracted candidate data from `extract`), use them as the basis for evaluation. Otherwise, generate a sensible rubric for the domain.

{findings}

## Instructions

1. **Establish criteria.** If a rubric was provided upstream, use it exactly. If not, generate 5-7 weighted criteria appropriate for `{domain}`. Each criterion should have a name, weight (totaling 100%), and a 1-5 scoring anchor (what does a 1 vs 3 vs 5 look like?).

2. **Score each candidate.** For every candidate in `{candidates}` (comma-separated list), assign a score (1-5) on each criterion. Provide a one-sentence justification per score.

3. **Compute weighted totals.** Multiply each score by its weight, sum for each candidate.

4. **Rank and compare.** Order candidates by weighted total. Flag any ties or close calls. Note standout strengths and disqualifying weaknesses.

5. **Surface insights.** Identify which criteria most differentiate the candidates and where they cluster together.

## Output

Produce a JSON file at `/home/claude/workspace/grade_results.json` with this structure:

```json
{
  "domain": "{domain}",
  "criteria": [
    { "name": "...", "weight": 0.25, "anchors": { "1": "...", "3": "...", "5": "..." } }
  ],
  "candidates": [
    {
      "name": "...",
      "scores": [ { "criterion": "...", "score": 4, "justification": "..." } ],
      "weighted_total": 3.85,
      "rank": 1,
      "strengths": ["..."],
      "weaknesses": ["..."]
    }
  ],
  "insights": "..."
}
```

Then present a human-readable summary: a comparison table, rankings, and a brief narrative on who stands out and why.

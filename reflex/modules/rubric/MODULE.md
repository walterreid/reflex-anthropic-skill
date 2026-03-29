# Rubric Module

Generate an evaluation rubric for a given domain.

- **Domain**: {domain}
- **Depth**: {depth}
- **Upstream findings**: {findings}

## Instructions

1. If upstream findings exist in `{findings}`, use them to inform what dimensions matter in this domain. If a file exists at `/home/claude/research_{domain}.json` or similar, read it for structured data.
2. If no upstream findings, use your knowledge of `{domain}` to determine what experts typically evaluate.
2b. If a file exists at `/home/claude/distill_{domain}.json` or any `distill_*.json` that matches the research target, read it. The `suggested_dimensions` field contains evidence-weighted categories that should each have a corresponding rubric dimension. If a suggested dimension has no matching rubric dimension, either add one or note the omission in the methodology field with a reason for excluding it.
2c. Balance check (for comparative evaluations): If the evaluation will compare two or more targets, ensure each dimension describes a capability that either target could in principle achieve. Avoid dimensions that are essentially feature checks for one specific target's architecture. After generating dimensions, verify that no target could score 4-5 on more than twice as many dimensions as the other. If the ratio exceeds 2:1, the rubric is biased — merge or replace dimensions until balance improves.
3. Generate a rubric with 4-7 dimensions. For each dimension:
   - **name**: Short label (e.g. "Composability", "Developer Experience")
   - **description**: One sentence explaining what this measures
   - **weight**: Relative importance from 1-5 (5 = critical, 1 = nice-to-have)
   - **scale**: What 1, 3, and 5 look like for this dimension (anchored scoring)
4. Depth levels:
   - **quick**: 4 dimensions, minimal anchor descriptions
   - **detailed**: 6-7 dimensions, full anchor descriptions with concrete examples
5. Write the rubric to `/home/claude/rubric_{domain}.json` in this structure:

```json
{
  "domain": "{domain}",
  "generated_at": "ISO timestamp",
  "dimensions": [
    {
      "name": "Dimension Name",
      "description": "What this measures",
      "weight": 4,
      "scale": {
        "1": "What a score of 1 looks like",
        "3": "What a score of 3 looks like",
        "5": "What a score of 5 looks like"
      }
    }
  ],
  "total_weight": 25,
  "methodology": "One sentence on how scores should be applied"
}
```

## Output

Brief confirmation of the rubric: list the dimensions with their weights, and note the total possible weighted score. The structured rubric is on disk for downstream modules.

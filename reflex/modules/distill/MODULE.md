# Distill Module

Reduce raw research findings to their essential structure — what categories carry the most evidence weight, what patterns emerge, and what a downstream rubric or analysis should account for.

- **Target**: {target}
- **Lens**: {lens}

## Available Workspace Data

{workspace}

## Instructions

1. Locate research data for `{target}`:
   - Look for `/home/claude/research_{target}.json`, `/home/claude/compare_*{target}*.json`, or `/home/claude/extract_{target}.json`.
   - If multiple files exist, read all of them — they represent different evidence sources.
   - If no files exist, state that there's nothing to distill and suggest running `reflex websearch target:{target}` first.

2. Read every finding. For each, note its `category` (or infer one if not labeled).

3. Build a category map:
   - Count findings per category.
   - For each category, extract the single strongest finding — the one with the most specific evidence or the broadest implication.
   - Note which categories have conflicting findings (these are analytically interesting).

4. Apply the lens:
   - **depth**: Rank categories by evidence density. Output only the top 3-4 with the most findings and strongest evidence. Flag what was cut and why.
   - **breadth**: Preserve all categories. Rank by density but don't cut. Note which categories are thin (1 finding) vs. rich (3+ findings).

5. Write output to `/home/claude/distill_{target}.json`:

```json
{
  "target": "{target}",
  "lens": "{lens}",
  "distilled_at": "ISO timestamp",
  "source_files": ["files read"],
  "total_findings": 0,
  "categories": [
    {
      "name": "Category Name",
      "finding_count": 0,
      "strongest_finding": "The most important point in this category",
      "evidence_quality": "strong|moderate|thin",
      "conflicts": false,
      "conflict_note": "null or description of conflicting evidence"
    }
  ],
  "coverage_gaps": ["Categories with only 1 finding — may be underresearched"],
  "suggested_dimensions": ["Categories that a downstream rubric should account for"]
}
```

The `suggested_dimensions` field is the key output for rubric chains — it tells the rubric module which evidence categories have enough weight to deserve their own dimension.

## Output

Brief confirmation: how many findings distilled, how many categories found, what the top categories are by evidence density. The structured file on disk is the real output — downstream modules will read it.

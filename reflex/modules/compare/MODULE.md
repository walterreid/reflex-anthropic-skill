# Compare Module

Research two targets and produce structured side-by-side findings.

- **Target**: {target}
- **Target2**: {target2}
- **Focus**: {focus}

## Instructions

1. Use `web_search` and `web_fetch` to research both `{target}` and `{target2}`. Conduct 3-5 searches per target.
2. Focus through the lens of `{focus}`:
   - **general**: What each is, what it does, who uses it, market position
   - **competitive**: Pricing, features, differentiators, market share
   - **technical**: Architecture, stack, integrations, developer experience
3. Produce **paired findings** — for every claim about Target A, find the equivalent for Target B. Structure as:

```json
{
  "target": "{target}",
  "target2": "{target2}",
  "focus": "{focus}",
  "searched_at": "ISO timestamp",
  "comparisons": [
    {
      "dimension": "e.g. Pricing",
      "target_finding": "what target does",
      "target2_finding": "what target2 does",
      "advantage": "target or target2 or neutral",
      "evidence": "source detail"
    }
  ],
  "summary": "2-3 sentence synthesis of who wins where"
}
```

4. Write findings to `/home/claude/compare_{target}_vs_{target2}.json`.
5. Output a brief confirmation with key dimensions compared and the overall picture.

## Output

Brief confirmation of comparison dimensions and where each target leads. The structured data is on disk for downstream modules.

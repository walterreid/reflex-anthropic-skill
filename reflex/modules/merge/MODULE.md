# Merge Module

Combine multiple research, comparison, or extract files into a single consolidated evidence base. Useful when you've researched several targets separately and want to feed them all into a single downstream analysis.

- **Targets**: {targets}

## Available Workspace Data

{workspace}

## Instructions

1. Identify source files to merge:
   - If `{targets}` is "all", read every `research_*.json`, `compare_*.json`, and `extract_*.json` in the workspace.
   - If specific targets are named, read files matching those target names.
   - If no matching files are found, say so and suggest which websearch or extract commands would produce them.

2. Read each source file. Collect all findings into a single list, preserving:
   - The original `category` of each finding.
   - The original `source` URL or file.
   - A `provenance` field noting which research file the finding came from.

3. Deduplicate: if two findings from different research files say essentially the same thing, keep the one with stronger evidence and note the duplication.

4. Re-categorize if needed: findings from different research files may use different category names for the same concept. Normalize category names where the overlap is clear, but note the mapping.

5. Write the merged output to `/home/claude/merged_{targets_slug}.json` where `{targets_slug}` is a short dash-separated version of the target names (e.g., `merged_anthropic-reflex.json`):

```json
{
  "merged_at": "ISO timestamp",
  "source_files": ["list of files read"],
  "targets": ["list of unique targets"],
  "total_findings": 0,
  "deduplicated": 0,
  "findings": [
    {
      "category": "Normalized Category",
      "point": "The finding",
      "evidence": "Supporting detail",
      "source": "URL or file",
      "provenance": "Which research file this came from"
    }
  ],
  "category_summary": {
    "Category Name": { "count": 0, "targets_represented": ["which targets have findings here"] }
  }
}
```

The `category_summary` is valuable for downstream modules — it shows which categories have cross-target evidence (useful for comparative rubrics) versus single-target evidence.

## Output

Brief confirmation: how many files merged, how many findings total, how many deduplicated, and the category distribution. The merged JSON on disk is the real output.

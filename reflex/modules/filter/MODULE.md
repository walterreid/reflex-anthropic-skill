# Filter Module

Prune upstream findings to only what's relevant for a specific criteria, discarding the rest. The opposite of merge — this narrows focus intentionally.

- **Target**: {target}
- **Criteria**: {criteria}
- **Threshold**: {threshold}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Locate upstream data. Scan the workspace for files matching `{target}`: research, compare, websearch, extract, distill, merge, or scenario JSONs. Read them all. Also use any upstream context from `{findings}`.

2. If no upstream data is found, respond with an error: filter needs something to filter. Suggest running a source module first.

3. Read the criteria: `{criteria}`. This is the lens for relevance. Examples:
   - A domain: "security", "pricing", "developer-experience"
   - A stakeholder: "end-user", "CTO", "regulator"
   - A constraint: "under-$50k", "open-source-only", "EU-compliant"
   - A question: "does this affect hiring?"

4. Score every finding/claim/dimension in the upstream data for relevance to `{criteria}` on a 1-5 scale:
   - **5**: Directly about the criteria
   - **4**: Strongly related, clear connection
   - **3**: Tangentially related, some relevance
   - **2**: Weakly connected, mostly noise
   - **1**: Irrelevant to the criteria

5. Apply the threshold `{threshold}`:
   - **strict**: Keep only 4-5 (direct and strong)
   - **moderate**: Keep 3-5 (anything with relevance)
   - **loose**: Keep 2-5 (drop only truly irrelevant)

6. Write the filtered output to `/home/claude/filter_{target}_{criteria_slug}.json` where `{criteria_slug}` is a lowercase-hyphenated version of the criteria:

```json
{
  "target": "{target}",
  "criteria": "{criteria}",
  "threshold": "{threshold}",
  "filtered_at": "ISO timestamp",
  "source_file": "filename that was filtered",
  "stats": {
    "input_count": 11,
    "output_count": 5,
    "dropped_count": 6,
    "retention_rate": 0.45
  },
  "kept": [
    {
      "finding": "The original finding or claim",
      "relevance_score": 5,
      "relevance_reason": "Why this matters for the criteria"
    }
  ],
  "dropped": [
    {
      "finding": "What was removed",
      "relevance_score": 2,
      "drop_reason": "Why this isn't relevant to the criteria"
    }
  ],
  "filtered_summary": "2-3 sentence synthesis of what remains after filtering"
}
```

7. Present the results conversationally: how many findings survived, what was kept vs dropped, and the filtered summary. Mention the retention rate — a very high rate (>90%) suggests the criteria was too broad; a very low rate (<20%) suggests it was too narrow or the upstream data doesn't cover this angle well.

## Output

A pruned dataset focused on a specific criteria, with full transparency on what was kept and what was dropped. The file on disk preserves the `dropped` array so the pruning decision can be audited or reversed. Downstream modules (rubric, evaluate, grade, actions, report) will work from the filtered set. Keep the conversational summary to 6-10 lines.

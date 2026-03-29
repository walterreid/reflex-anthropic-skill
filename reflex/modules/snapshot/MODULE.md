# Snapshot Module

Package the current workspace into a single downloadable JSON file. If a previous snapshot is uploaded in the conversation, diff against it to show what changed.

- **Label**: {label}
- **Workspace**: {workspace}

## Instructions

1. **Scan the workspace.** Read every JSON file in `/home/claude/` (not subdirectories). For each file, capture:
   - Filename
   - Full contents (parsed JSON)
   - File size
   - The `target`, `domain`, or `topic` field if present (for the manifest)

2. **Check for a previous snapshot.** Scan `/mnt/user-data/uploads/` for any file matching `snapshot_*.json` or `reflex_snapshot_*.json`. If found, read it — this is the baseline for diffing.

3. **If a previous snapshot exists, compute the diff:**
   - **Added**: Files in the current workspace that weren't in the previous snapshot
   - **Removed**: Files in the previous snapshot that aren't in the current workspace
   - **Changed**: Files present in both but with different contents (compare JSON structure, not whitespace)
   - **Unchanged**: Files identical in both

4. **Build the snapshot bundle:**

```json
{
  "snapshot_version": 1,
  "label": "{label}",
  "created_at": "ISO timestamp",
  "file_count": 5,
  "manifest": [
    {
      "filename": "research_ai-regulation.json",
      "target": "ai-regulation",
      "type": "research",
      "size_bytes": 4200
    }
  ],
  "files": {
    "research_ai-regulation.json": { ... full JSON contents ... },
    "rubric_ai-regulation.json": { ... full JSON contents ... }
  },
  "diff": {
    "baseline_label": "previous snapshot label or null",
    "baseline_date": "ISO timestamp or null",
    "added": ["new_file.json"],
    "removed": ["old_file.json"],
    "changed": ["modified_file.json"],
    "unchanged": ["stable_file.json"]
  }
}
```

If no previous snapshot exists, set `diff` to `null`.

5. **Write and present the snapshot.** Write to `/mnt/user-data/outputs/reflex_snapshot_{label}.json`. Use the `present_files` tool to make it downloadable.

6. **Surface a summary in chat.** Report:
   - How many files were bundled
   - The label and timestamp
   - If a diff was computed: what's new, what changed, what was removed
   - Remind the user they can upload this file in a new conversation and run `reflex restore` to resume

## Output

A downloadable snapshot file and a conversational summary. If diffing, lead with what changed. Keep the summary to 6-10 lines.

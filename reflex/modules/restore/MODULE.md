# Restore Module

Unpack an uploaded snapshot file back into the workspace so downstream modules can pick up where a previous session left off.

- **Source**: {source}
- **Mode**: {mode}

## Instructions

1. **Locate the snapshot file.** Scan `/mnt/user-data/uploads/` for files matching `snapshot_*.json`, `reflex_snapshot_*.json`, or the specific filename in `{source}` if provided. If multiple snapshots are found and no `{source}` was specified, list them and ask the user which one to restore.

2. **Validate the snapshot.** Read the file and verify:
   - It has a `snapshot_version` field (must be 1)
   - It has a `files` object containing the bundled workspace data
   - It has a `manifest` array listing what's inside
   
   If validation fails, report what's wrong and stop. Don't write partial data.

3. **Check the current workspace.** Scan `/home/claude/` for existing JSON files. If any exist, apply the `{mode}`:
   - **fill** (default): Only write files that don't already exist in the workspace. Existing files are untouched. Best for fresh sessions.
   - **overwrite**: Replace everything. Existing workspace files that match a snapshot filename are overwritten. Files in the workspace that aren't in the snapshot are left alone.
   - **replace**: Clear all existing JSON files from the workspace first, then write the snapshot contents. Full reset to snapshot state.

4. **Unpack the files.** For each entry in the snapshot's `files` object:
   - Write the JSON contents to `/home/claude/{filename}`
   - Track what was written, skipped (fill mode), or overwritten

5. **Report the results.** Summarize:
   - Snapshot label and when it was originally created
   - How many files were restored
   - How many were skipped (fill mode) or overwritten (overwrite mode)
   - List each restored file with its type and target (from the manifest)
   - Suggest what the user might want to do next based on what was restored (e.g., if a run_plan.json was restored, suggest `reflex run` to continue; if research files were restored, suggest downstream analysis)

## Output

A conversational confirmation of what was restored and suggested next steps. Keep it to 6-10 lines. The goal is for the user to immediately understand what's in their workspace and what they can do with it.

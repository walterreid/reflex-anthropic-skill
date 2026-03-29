# Run — Reset Variant

Clear the active run plan.

## Instructions

1. Check if `/home/claude/run_plan.json` exists
2. If it exists:
   - Read it and note what was completed vs pending
   - Delete the file
   - Tell the user what was cleared: how many steps were completed, how many were remaining
   - Note that workspace files from completed steps are still available
3. If it doesn't exist:
   - Tell the user there's no active run to reset

Suggest they can start a new run with `reflex run "their intent"`.

## Output

A 2-3 line confirmation of what was cleared.

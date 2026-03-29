# Run — Continue Variant

Resume an active run. Read the plan, execute the next step, pause.

- **Intent**: {intent}
- **Registry**: {registry}
- **Workspace**: {workspace}

## Instructions

### Step 1: Read the plan

Read `/home/claude/run_plan.json`. Identify the current position — find the first step with `"status": "pending"`.

### Step 2: Handle skip (if applicable)

If `{intent}` is "skip":
1. Find the first step with `"status": "pending"`
2. Mark it as `"status": "skipped"`
3. Save the plan
4. If there are more pending steps, continue to Step 3 with the *next* pending step
5. If no more pending steps, go to Step 5 (completion)

### Step 3: Execute the next step

1. Find the first step with `"status": "pending"`
2. Mark it as `"status": "in_progress"` and update `"current_step"`
3. Save the plan
4. **Execute the module** — do the actual work. Read any upstream output files that previous steps produced (check `"output_file"` fields of completed steps, and check `/home/claude/` for workspace files). Follow the module's instructions fully: run web searches, analyze content, write output files.
5. When complete, mark the step as `"status": "complete"` and record the output file path in `"output_file"`
6. Save the plan

### Step 4: Pause (if more steps remain)

After completing the step, tell the user:
- What you just did (1 sentence)
- What was produced (filename if applicable)
- What the next step is and what it will do (1 sentence)
- How many steps remain

Then ask: **"Ready for the next step, or any adjustments?"**

### Step 5: Completion (if no more steps)

If all steps are complete or skipped:
- Summarize the full run: what was produced at each step, what files exist in the workspace
- Suggest logical follow-ups (e.g., `reflex challenge`, `reflex simplify`, or a formatter if none was in the plan)
- Note they can run `reflex run reset` to clear the plan for a fresh start

## Output

Execute one step fully, save state, then either pause for continuation or report completion. Keep summaries to 4-6 lines.

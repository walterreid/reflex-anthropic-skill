# Run — Start Variant

Read the plan, show the roadmap, and begin execution.

- **Intent**: {intent}
- **Registry**: {registry}
- **Workspace**: {workspace}

## Instructions

You have been invoked after the `plan` module decomposed the user's intent.

### Step 1: Read the plan

Read `/home/claude/run_plan.json`. This file was written by `plan` and contains the full execution plan with steps, params, and status fields.

If `run_plan.json` doesn't exist or is unreadable, fall back to reading the plan module's output from the conversation context above. Extract the chain of modules and their params, then write `run_plan.json` yourself using this format:

```json
{
  "intent": "{intent}",
  "created_at": "ISO timestamp",
  "total_steps": 5,
  "steps": [
    {
      "step": 1,
      "module": "module_name",
      "params": {"key": "value"},
      "status": "pending",
      "output_file": null
    }
  ],
  "current_step": 0
}
```

### Step 2: Summarize the plan before executing

Give the user a brief overview of what's about to happen:

- How many steps total
- The modules in order (one line, e.g., "research → trends → competitive-messaging → creative-brief → email")
- If multiple steps use the same module (repeated task), note this: "Steps 1-8 each run design-module with a different target"
- Estimated complexity: "This is a [light/moderate/substantial] workflow"

Then proceed to execution.

### Step 3: Execute step 1

1. Mark step 1 as `"status": "in_progress"` and set `"current_step": 1`
2. Save the updated plan
3. **Execute the module** — follow the module's instructions as if the user had run `reflex {module} {params}` directly. Do the actual work: web searches, file reading, analysis, writing output files. Do not just describe what you would do.
4. When complete, mark it as `"status": "complete"` and record the output file path in `"output_file"` if one was produced
5. Save the updated plan

### Step 4: Pause

After completing step 1, tell the user:
- What you just did (1 sentence)
- What was produced (filename if applicable)
- What the next step is and what it will do (1 sentence)
- How many steps remain

Then ask: **"Ready for the next step, or any adjustments?"**

Tell them they can say:
- `reflex run` to continue
- `reflex run skip` to skip the next step
- `reflex run reset` to abandon the plan

## Output

Summarize the plan, execute step 1 fully, save state, then pause with a brief summary and prompt for continuation. Keep the pause summary to 4-6 lines.

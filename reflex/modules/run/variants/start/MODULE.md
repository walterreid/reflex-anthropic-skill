# Run — Start Variant

Parse the upstream plan into driving directions and begin execution.

- **Intent**: {intent}
- **Registry**: {registry}
- **Workspace**: {workspace}

## Instructions

You have been invoked after the `plan` module decomposed the user's intent. The plan output is visible in your conversation context above — it contains a suggested reflex command (a chain of modules with params).

### Step 1: Parse the plan

Read the plan module's output from the conversation context. Extract:
- The suggested chain of modules and their params
- If multiple alternatives were offered, select the primary suggestion

Break the chain into individual steps. For each step, identify:
- The module name
- The params that apply to that module (reference each module's params from the registry below)

**Registry for param reference:**
{registry}

### Step 2: Write the run plan

Write `/home/claude/run_plan.json`:

```json
{
  "intent": "{intent}",
  "created_at": "ISO timestamp",
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

Execute step 1 fully, save state, then pause with a brief summary and prompt for continuation. Keep the summary to 4-6 lines.

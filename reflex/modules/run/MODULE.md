# Run Module

Execute a module pipeline step-by-step with pauses between each step. Like GPS directions — it doesn't matter where you stop, as long as you know where you are.

When no `run_plan.json` exists, the `plan` dependency runs first to decompose the user's intent. When a plan already exists, the dependency is skipped and execution resumes.

The resolver selects the appropriate variant based on workspace state.

# Design Module — Triage

The user invoked `design-module` without specifying an intent. Present options and guide them to the right workflow.

## Available Modules

{registry}

## Current Workspace

{workspace}

## Instructions

Present the user with three paths, briefly explaining each:

### 1. Create a new module
Build something that doesn't exist yet. Ask the user to describe what the module should do, then proceed with the full design workflow (level selection, group, params, dependencies, inject sources, composition patterns).

Prompt: "What should the new module do? Describe it in a sentence or two and I'll design the right structure."

### 2. Upgrade an existing module
Modify or improve a module that already exists. This includes:
- **Adding params** — the module needs new inputs it doesn't currently accept
- **Changing the prompt** — the MODULE.md instructions need refinement, restructuring, or expansion
- **Bumping the level** — e.g., Level 1 → Level 3 (adding a resolver and variants for different behaviors)
- **Adding dependencies** — the module should automatically run another module first
- **Restructuring output** — changing the JSON schema, file naming, or output format
- **Fixing issues** — the module produces weak results, misses edge cases, or has composition problems

Ask the user which module they want to upgrade. Show the registry so they can pick. Once they choose, read the module's files (PARAMS.json, MODULE.md, and any RESOLVE.py/DEPENDS.json/variants) to understand the current structure, then ask what they want to change.

### 3. Clone and modify
Fork an existing module as the starting point for a new one. Useful when:
- A module does 80% of what you need but diverges on the other 20%
- You want a specialized variant of a general module (e.g., `swot` → `swot-competitive`)
- You want to experiment without touching the original

Ask which module to clone and what should be different in the copy.

## How to Present

Use the ask_user_input tool to present these three options cleanly. Include a brief orienting sentence before the widget — something like "What would you like to do?" Don't dump the full registry unless they choose option 2 (upgrade).

After the user picks a path:

### If they choose "Create"
Ask for their intent (what the module should do), then follow the full design workflow from the create variant — determine level, group, params, inject needs, dependency strategy, composition fit, and write the files.

### If they choose "Upgrade"
1. Ask which module (or let them describe what they want to improve — match it against the registry)
2. Read all files in that module's directory to understand current structure
3. Ask what they want to change
4. Propose the changes with rationale (e.g., "This means upgrading from Level 1 to Level 3 because...")
5. Implement the changes and write updated files
6. Show before/after summary of what changed

### If they choose "Clone and modify"
1. Ask which module to clone
2. Ask what the new module should be called and what should differ
3. Copy the structure, apply modifications
4. Write the new module files
5. Confirm no collision with existing modules in the registry

## Output

Start with the interactive choice. Keep the tone conversational — this is a guided workflow, not a form. After the user makes their choice and provides details, follow through to file creation and present the results for download.

Always end with example chains showing how the created/upgraded/cloned module composes with existing ones.

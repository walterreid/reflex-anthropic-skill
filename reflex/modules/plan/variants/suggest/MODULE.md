# Plan — Suggest Variant

The existing module registry can't fully serve this intent. Design a new module to fill the gap.

- **Intent**: {intent}

## Available Modules

{registry}

## Module Conventions

Every module follows this structure:
- **MODULE.md**: Instructions Claude follows. Uses `{param_name}` placeholders. References upstream findings with `{findings}`. Ends with an `## Output` section describing what the module produces.
- **PARAMS.json**: Declares params (required/optional/defaults/greedy), group membership (source, analyzer, transformer, formatter, utility, meta), and a one-line description.
- Modules should be single-purpose. They do one job and do it well.
- Modules should chain cleanly: accept upstream context naturally, produce output that downstream modules can consume.

## Groups

- **source**: Gathers raw data (web search, file extraction, conversation context)
- **analyzer**: Interprets data through a lens (review, risk assessment, SWOT, evaluation)
- **transformer**: Reshapes or refines analysis (extract actions, challenge assumptions, simplify)
- **formatter**: Delivers output in a specific format (email, pitch, report)
- **utility**: Standalone tools that don't fit the pipeline pattern
- **meta**: System management (help, plan, diagnose, status)

## Instructions

1. Read the intent: `{intent}`
2. Scan the registry for existing modules that partially address it. Note what's close and what's missing.
3. Design the missing module:
   - Choose a clear, short name (lowercase, hyphenated if needed)
   - Assign it to the right group
   - Define its params — what inputs does it need? Which are required?
   - Write the MODULE.md with clear instructions, `{param_name}` placeholders, and an output section
   - Write the PARAMS.json following the conventions above
4. Show how the new module chains with existing ones by proposing 2-3 example chains that combine it with current modules.
5. Write the module files to `/home/claude/modules/{module_name}/MODULE.md` and `/home/claude/modules/{module_name}/PARAMS.json`.

## Output

Respond with:

**Gap identified:** One sentence on what's missing from the current registry.

**New module: `{name}`** ({group})
Brief description of what it does.

**Example chains:**
```
reflex [chain using new module with existing ones]
```

**Files written to:** `/home/claude/modules/{name}/` — ready to move into your modules directory.

Do NOT execute any chains. The user will review, install, and test.

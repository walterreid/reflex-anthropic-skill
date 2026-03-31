# Plan

Translate a natural language intent into a runnable `/reflex` command — or design a new module if nothing fits.

- **Intent**: {intent}

## Available Modules

{registry}

## How Chains Work

Modules compose with the `+` operator: `module1+module2+module3`. Data flows forward — each step's output becomes context for the next.

Typical flow: **source → analyzer → transformer → formatter**

Not every chain needs all four types. Some are two steps. Some are five. Match the intent.

Params apply across the chain. Common params: `target:X`, `audience:X`, `tone:X`, `recipient:X`.

## Instructions

1. Read the intent: `{intent}`
2. Scan the registry for modules that serve the goal. Consider module names, descriptions, param signatures, and group roles.
3. Decide: can existing modules handle this intent?

### If yes — plan a chain

1. Select the modules that serve the goal. Use the registry above — don't invent modules.
2. Order them logically. Sources gather data. Analyzers interpret it. Transformers reshape it. Formatters deliver it.
3. Construct the `/reflex` command with appropriate params.
4. If the intent is ambiguous, propose 2-3 alternative chains with a one-line explanation of what each prioritizes.
5. Write the decomposed plan to `/home/claude/plan_output.json`:

\```json
{
  "intent": "original intent text",
  "chain": [
    {"module": "module_name", "params": {"key": "value"}}
  ]
}
\```

This file is consumed by downstream modules. It does not replace the human-readable output.

**Respond with:**

**Suggested command:**
```
/reflex module1+module2+module3 target:X param:Y
```

Then a 1-2 sentence explanation of what this chain will do and why you chose these modules.

If you have alternative chains, show them as:
**Alternative:** `/reflex ...` — one line explaining the tradeoff.

### If no — suggest a new module

If no combination of existing modules adequately serves the intent, design one.

1. Note what's close and what's missing from the registry.
2. Design the missing module:
   - Choose a clear, short name (lowercase, hyphenated if needed)
   - Assign it to the right group (source, analyzer, transformer, formatter, utility, meta)
   - Define its params — what inputs does it need? Which are required?
   - Write the MODULE.md with clear instructions, `{param_name}` placeholders, and an `## Output` section
   - Write the PARAMS.json following conventions (required/optional/defaults/greedy, group, description)
3. Show how the new module chains with existing ones.
4. Write the module files to `/home/claude/modules/{module_name}/MODULE.md` and `/home/claude/modules/{module_name}/PARAMS.json`.

**Respond with:**

**Gap identified:** One sentence on what's missing from the current registry.

**New module: `{name}`** ({group})
Brief description of what it does.

**Example chains:**
```
reflex [chain using new module with existing ones]
```

**Files written to:** `/home/claude/modules/{name}/` — ready to move into your modules directory.

---

Do NOT execute any chains. The user will run it (or modify it) on the next turn.
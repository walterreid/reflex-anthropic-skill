# Plan

Translate a natural language intent into the best way to execute it — a direct command, an inline chain, a `run` workflow, or a new module design.

- **Intent**: {intent}

## Available Modules

{registry}

## How Execution Works

There are three ways to execute modules, each suited to different situations:

**Direct invocation** — `reflex module target:X` — for single-module tasks. Fast, no overhead.

**Inline chain** — `reflex module1+module2+module3 target:X` — for 2-4 module pipelines. Data flows forward — each step's output becomes context for the next. The user types the chain and sees all steps execute sequentially.

**Run** — `reflex run "natural language intent"` — for complex workflows (5+ modules), multi-step tasks, or when the user shouldn't need to know module names. `run` executes one step at a time with pauses, letting the user steer.

### Composition Rules

Typical flow: **source → analyzer → transformer → formatter**. Not every chain needs all four types.

Params apply across chains. Common shared params: `target:X`, `audience:X`, `tone:X`, `recipient:X`.

The `+` operator overrides individual module dependencies — the user's ordering is authoritative.

**Quality gate:** The `perspective` module applies an evaluation lens to upstream output and revises what the lens reveals. When a chain ends with a formatter and the intent implies the output is high-stakes (launch emails, investor pitches, public-facing content, anything where "make sure it's good" is implicit), suggest appending `+perspective`. Don't add it by default — most chains don't need it. But name it as an option when quality matters.

## Instructions

1. **Read the intent:** `{intent}`

2. **Check for a pre-composed chain.** If the intent already contains a `+` chain or names specific modules in a specific order (e.g., "run websearch+trends+creative-brief"), treat it as an explicit composition. Don't decompose or reorder it. Validate that the named modules exist in the registry, map the params, and pass the chain through as-is. The user has already done the planning — respect it.

3. **Detect the task structure.** If the intent is natural language (not a pre-composed chain), determine what kind of task this is:

   - **Single task** — one clear goal ("analyze my competitors"). Match to modules normally.
   - **Sequential pipeline** — a goal that requires multiple analytical steps in order ("research the market, then position my brand, then write an email"). Build a chain.
   - **Repeated task** — the intent contains a list of discrete items that each need the same operation ("design 8 modules" / "review these 5 documents" / "research each of these companies"). Build a plan where the same module runs once per item.
   - **Compound task** — multiple unrelated goals in one request ("research X and also write me a recipe for Y"). Separate into independent commands.

4. **Scan the registry** for modules that serve the goal. Consider module names, descriptions, param signatures, and group roles.

5. **Decide:** can existing modules handle this intent?

### If yes — plan the execution

1. Select the modules that serve the goal. Use the registry above — don't invent modules.
   - Pick the most specific module available (prefer `competitive-messaging` over `research` when the intent is about competitive messaging)
   - Don't include modules the intent didn't ask for, even if they'd make the output "more thorough." Match the intent, don't expand it.
   - If a module would need upstream data to function well but the intent doesn't mention that upstream step, include it — but note why ("adding `websearch` because `creative-brief` needs research to ground its output")
2. Order them logically. Sources gather data. Analyzers interpret it. Transformers reshape it. Formatters deliver it.
3. Choose the right execution format:
   - **1 module** → direct invocation: `reflex module target:X`
   - **2-4 modules** → inline chain: `reflex module1+module2 target:X`
   - **5+ modules** → recommend `run`: `reflex run "the original intent"`
   - **Repeated task** → recommend `run` with one step per item in the plan
4. Construct the command with appropriate params.
5. If the intent is ambiguous, propose 2-3 alternative chains with a one-line explanation of what each prioritizes. Include at least one short option and one thorough option when the ambiguity is about depth.
6. Write the plan to `/home/claude/run_plan.json`:

```json
{
  "intent": "original intent text",
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

This file is consumed directly by `run` — no intermediate transformation needed.

**Respond with:**

**Suggested command:**
```
reflex [appropriate format] ...
```

Then a 1-2 sentence explanation of what this does and why you chose these modules.

If the chain is 5+ steps, recommend `run` and briefly explain the step-by-step flow:
> This is a 7-step workflow. Running `reflex run` will execute each step with a pause, letting you adjust as it goes. The steps are: [list].

If you have alternative chains, show them as:
**Alternative:** `reflex ...` — one line explaining the tradeoff.

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

Do NOT execute any chains or modules. The user will run it (or modify it) on the next turn.

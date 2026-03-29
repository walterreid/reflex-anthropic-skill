# Plan — Route Variant

Translate a natural language intent into a runnable `/callsign` command.

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
2. Identify which modules serve the goal. Use the registry above — don't invent modules.
3. Order them logically. Sources gather data. Analyzers interpret it. Transformers reshape it. Formatters deliver it.
4. Construct the `/callsign` command with appropriate params.
5. If the intent is ambiguous, propose 2-3 alternative chains with a one-line explanation of what each prioritizes.

## Output

Respond with:

**Suggested command:**
```
/callsign module1+module2+module3 target:X param:Y
```

Then a 1-2 sentence explanation of what this chain will do and why you chose these modules.

If you have alternative chains, show them as:
**Alternative:** `/callsign ...` — one line explaining the tradeoff.

Do NOT execute the chain. The user will run it (or modify it) on the next turn.

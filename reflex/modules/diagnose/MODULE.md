# Diagnose Module

Analyze a chain that produced weak results and suggest a better one.

- **Chain that was run**: {chain}
- **Problem**: {problem}

## Available Modules

{registry}

## Workspace State

{workspace}

## Instructions

1. Parse the chain `{chain}` into its component modules.
2. Analyze the problem `{problem}`:
   - **shallow**: The analysis lacked depth. Was a source module missing? Was the chain too short?
   - **wrong-tone**: The output didn't match the audience. Was a formatter missing or misconfigured?
   - **missed-context**: Important information was overlooked. Was `context` or `extract` needed?
   - **too-long**: The output was bloated. Was `simplify` or a tighter formatter needed?
   - **general**: Look at the overall composition. What's missing from the source→analyzer→transformer→formatter flow?
3. Check the workspace state — are there prior findings that could have been reused?
4. Propose an improved chain.

## Output

**Original chain:** `{chain}`
**Diagnosis:** 2-3 sentences on what was missing or misordered.
**Suggested fix:**
```
/reflex improved+chain+here target:X
```
One sentence on what the fix changes.
